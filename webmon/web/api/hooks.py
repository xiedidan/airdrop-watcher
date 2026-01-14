"""
Hook 管理 API 路由

提供 Hook 配置的读写和执行历史查询接口。
"""

import logging
from typing import Optional
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query

from ..schemas.hook import (
    HookConfigSchema,
    HookConfigCreate,
    HookConfigUpdate,
    HookListResponse,
    HookHistoryResponse,
    HookStatisticsResponse,
    HookTestRequest,
    HookTestResponse,
    HookResultSchema,
)
from ..schemas.common import SuccessResponse, ErrorResponse
from webmon.config import ConfigManager
from webmon.hooks.manager import HookManager
from webmon.hooks.triggers import HookTrigger

router = APIRouter(prefix="/api/hooks", tags=["Hook 管理"])
logger = logging.getLogger(__name__)

# 全局 Hook 管理器实例
_hook_manager: Optional[HookManager] = None


def get_hook_manager() -> HookManager:
    """获取 Hook 管理器实例"""
    global _hook_manager
    if _hook_manager is None:
        config_manager = ConfigManager()
        project_root = Path.cwd()
        _hook_manager = HookManager(
            config_manager=config_manager,
            project_root=project_root
        )
    return _hook_manager


def reset_hook_manager():
    """重置 Hook 管理器（配置更新后调用）"""
    global _hook_manager
    _hook_manager = None


@router.get(
    "",
    response_model=HookListResponse,
    summary="获取所有 Hook 配置",
    description="获取所有全局 Hook 配置，按触发点分组返回",
)
async def list_hooks():
    """获取所有 Hook 配置"""
    try:
        manager = get_hook_manager()
        all_hooks = manager.get_all_hooks()

        # 转换为 schema 格式
        hooks_dict = {}
        for trigger, hook_list in all_hooks.items():
            hooks_dict[trigger] = [
                HookConfigSchema(
                    name=h.name,
                    type=h.type,
                    script=h.script,
                    enabled=h.enabled,
                    timeout=h.timeout,
                    async_exec=h.async_exec,
                    args=h.args,
                    env=h.env,
                    condition=h.condition,
                    working_dir=h.working_dir,
                    max_retries=h.max_retries,
                )
                for h in hook_list
            ]

        return HookListResponse(
            success=True,
            message="获取成功",
            hooks=hooks_dict,
            enabled=manager.is_enabled,
            defaults=manager._defaults,
        )

    except Exception as e:
        logger.error(f"获取 Hook 配置失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/triggers",
    response_model=SuccessResponse,
    summary="获取可用触发点",
    description="获取所有可用的 Hook 触发点",
)
async def list_triggers():
    """获取可用触发点"""
    triggers = [
        {
            "name": t.value,
            "description": _get_trigger_description(t.value),
        }
        for t in HookTrigger
    ]
    return SuccessResponse(
        success=True,
        message="获取成功",
        data={"triggers": triggers}
    )


def _get_trigger_description(trigger: str) -> str:
    """获取触发点描述"""
    descriptions = {
        "on_change_detected": "检测到页面变化时触发",
        "on_before_notify": "发送通知前触发",
        "on_after_notify": "发送通知后触发",
        "on_notify_failed": "通知发送失败时触发",
    }
    return descriptions.get(trigger, "")


@router.post(
    "",
    response_model=SuccessResponse,
    summary="添加 Hook",
    description="添加新的全局 Hook",
)
async def create_hook(data: HookConfigCreate):
    """添加 Hook"""
    try:
        # 验证触发点
        if not HookTrigger.is_valid(data.trigger):
            raise HTTPException(
                status_code=400,
                detail=f"无效的触发点: {data.trigger}"
            )

        # 获取当前配置
        config_manager = ConfigManager()
        hooks_config = config_manager.get_hooks_config()

        # 确保 global_hooks 存在
        if 'global_hooks' not in hooks_config:
            hooks_config['global_hooks'] = {}
        if data.trigger not in hooks_config['global_hooks']:
            hooks_config['global_hooks'][data.trigger] = []

        # 检查名称是否已存在
        existing_names = [
            h.get('name')
            for trigger_hooks in hooks_config['global_hooks'].values()
            for h in trigger_hooks
        ]
        if data.hook.name in existing_names:
            raise HTTPException(
                status_code=400,
                detail=f"Hook 名称已存在: {data.hook.name}"
            )

        # 添加新 Hook
        hook_dict = data.hook.model_dump(by_alias=True)
        hooks_config['global_hooks'][data.trigger].append(hook_dict)

        # 保存配置
        config_manager.update_hooks_config(hooks_config)

        # 重新加载 Hook 管理器
        reset_hook_manager()

        return SuccessResponse(
            success=True,
            message=f"Hook '{data.hook.name}' 已添加到 {data.trigger}",
            data={"hook": hook_dict}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"添加 Hook 失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/{hook_name}",
    response_model=SuccessResponse,
    summary="更新 Hook",
    description="更新指定的全局 Hook",
)
async def update_hook(hook_name: str, data: HookConfigUpdate):
    """更新 Hook"""
    try:
        config_manager = ConfigManager()
        hooks_config = config_manager.get_hooks_config()
        global_hooks = hooks_config.get('global_hooks', {})

        # 查找并更新 Hook
        found = False
        for trigger, hook_list in global_hooks.items():
            for i, hook in enumerate(hook_list):
                if hook.get('name') == hook_name:
                    # 更新字段
                    update_dict = data.model_dump(exclude_unset=True, by_alias=True)
                    hook_list[i].update(update_dict)
                    found = True
                    break
            if found:
                break

        if not found:
            raise HTTPException(
                status_code=404,
                detail=f"未找到 Hook: {hook_name}"
            )

        # 保存配置
        config_manager.update_hooks_config(hooks_config)

        # 重新加载 Hook 管理器
        reset_hook_manager()

        return SuccessResponse(
            success=True,
            message=f"Hook '{hook_name}' 已更新"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新 Hook 失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/{hook_name}",
    response_model=SuccessResponse,
    summary="删除 Hook",
    description="删除指定的全局 Hook",
)
async def delete_hook(hook_name: str):
    """删除 Hook"""
    try:
        config_manager = ConfigManager()
        hooks_config = config_manager.get_hooks_config()
        global_hooks = hooks_config.get('global_hooks', {})

        # 查找并删除 Hook
        found = False
        for trigger, hook_list in global_hooks.items():
            for i, hook in enumerate(hook_list):
                if hook.get('name') == hook_name:
                    hook_list.pop(i)
                    found = True
                    break
            if found:
                break

        if not found:
            raise HTTPException(
                status_code=404,
                detail=f"未找到 Hook: {hook_name}"
            )

        # 保存配置
        config_manager.update_hooks_config(hooks_config)

        # 重新加载 Hook 管理器
        reset_hook_manager()

        return SuccessResponse(
            success=True,
            message=f"Hook '{hook_name}' 已删除"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除 Hook 失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch(
    "/{hook_name}/toggle",
    response_model=SuccessResponse,
    summary="切换 Hook 启用状态",
    description="启用或禁用指定的 Hook",
)
async def toggle_hook(hook_name: str):
    """切换 Hook 启用状态"""
    try:
        config_manager = ConfigManager()
        hooks_config = config_manager.get_hooks_config()
        global_hooks = hooks_config.get('global_hooks', {})

        # 查找并切换状态
        found = False
        new_state = None
        for trigger, hook_list in global_hooks.items():
            for hook in hook_list:
                if hook.get('name') == hook_name:
                    hook['enabled'] = not hook.get('enabled', True)
                    new_state = hook['enabled']
                    found = True
                    break
            if found:
                break

        if not found:
            raise HTTPException(
                status_code=404,
                detail=f"未找到 Hook: {hook_name}"
            )

        # 保存配置
        config_manager.update_hooks_config(hooks_config)

        # 重新加载 Hook 管理器
        reset_hook_manager()

        status = "启用" if new_state else "禁用"
        return SuccessResponse(
            success=True,
            message=f"Hook '{hook_name}' 已{status}",
            data={"enabled": new_state}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"切换 Hook 状态失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch(
    "/global/toggle",
    response_model=SuccessResponse,
    summary="切换全局 Hook 开关",
    description="启用或禁用全局 Hook 功能",
)
async def toggle_global_hooks():
    """切换全局 Hook 开关"""
    try:
        config_manager = ConfigManager()
        hooks_config = config_manager.get_hooks_config()

        # 切换全局开关
        hooks_config['enabled'] = not hooks_config.get('enabled', False)
        new_state = hooks_config['enabled']

        # 保存配置
        config_manager.update_hooks_config(hooks_config)

        # 重新加载 Hook 管理器
        reset_hook_manager()

        status = "启用" if new_state else "禁用"
        return SuccessResponse(
            success=True,
            message=f"Hook 功能已{status}",
            data={"enabled": new_state}
        )

    except Exception as e:
        logger.error(f"切换全局 Hook 状态失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/{hook_name}/test",
    response_model=HookTestResponse,
    summary="测试 Hook",
    description="使用模拟上下文测试指定的 Hook",
)
async def test_hook(hook_name: str, data: HookTestRequest):
    """测试 Hook"""
    try:
        manager = get_hook_manager()
        hook = manager.get_hook_by_name(hook_name)

        if not hook:
            raise HTTPException(
                status_code=404,
                detail=f"未找到 Hook: {hook_name}"
            )

        # 构建测试上下文
        context = {
            'task': {
                'id': data.task_id or 'test-task-id',
                'name': 'Test Task',
                'url': 'https://example.com',
            },
            'change': {
                'type': 'content_change',
                'similarity': 0.85,
            },
            'ai_analysis': 'This is a test AI analysis',
            'notification': {'status': 'pending'},
        }

        # 执行测试
        result = await manager.executor.execute(hook, data.trigger, context)

        return HookTestResponse(
            success=result.success,
            message="测试完成" if result.success else f"测试失败: {result.error_message}",
            result=HookResultSchema(
                id=result.id,
                hook_name=result.hook_name,
                trigger=result.trigger,
                task_id=result.task_id,
                success=result.success,
                exit_code=result.exit_code,
                stdout=result.stdout,
                stderr=result.stderr,
                execution_time=result.execution_time,
                started_at=result.started_at.isoformat() if result.started_at else None,
                finished_at=result.finished_at.isoformat() if result.finished_at else None,
                error_message=result.error_message,
                error_type=result.error_type,
                retry_count=result.retry_count,
            )
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"测试 Hook 失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/history",
    response_model=HookHistoryResponse,
    summary="获取执行历史",
    description="获取 Hook 执行历史记录",
)
async def get_history(
    hook_name: Optional[str] = Query(None, description="按 Hook 名称筛选"),
    trigger: Optional[str] = Query(None, description="按触发点筛选"),
    task_id: Optional[str] = Query(None, description="按任务 ID 筛选"),
    success: Optional[bool] = Query(None, description="按成功/失败筛选"),
    limit: int = Query(50, ge=1, le=500, description="返回数量限制"),
    offset: int = Query(0, ge=0, description="偏移量"),
):
    """获取执行历史"""
    try:
        manager = get_hook_manager()
        results = manager.get_execution_history(
            hook_name=hook_name,
            trigger=trigger,
            task_id=task_id,
            success=success,
            limit=limit,
            offset=offset,
        )

        items = [
            HookResultSchema(
                id=r.id,
                hook_name=r.hook_name,
                trigger=r.trigger,
                task_id=r.task_id,
                success=r.success,
                exit_code=r.exit_code,
                stdout=r.stdout,
                stderr=r.stderr,
                execution_time=r.execution_time,
                started_at=r.started_at.isoformat() if r.started_at else None,
                finished_at=r.finished_at.isoformat() if r.finished_at else None,
                error_message=r.error_message,
                error_type=r.error_type,
                retry_count=r.retry_count,
            )
            for r in results
        ]

        return HookHistoryResponse(
            success=True,
            message="获取成功",
            items=items,
            total=len(items),
        )

    except Exception as e:
        logger.error(f"获取执行历史失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/statistics",
    response_model=HookStatisticsResponse,
    summary="获取执行统计",
    description="获取 Hook 执行统计信息",
)
async def get_statistics(
    hook_name: Optional[str] = Query(None, description="按 Hook 名称筛选"),
    task_id: Optional[str] = Query(None, description="按任务 ID 筛选"),
    days: int = Query(7, ge=1, le=90, description="统计最近多少天"),
):
    """获取执行统计"""
    try:
        manager = get_hook_manager()
        stats = manager.get_execution_statistics(
            hook_name=hook_name,
            task_id=task_id,
            days=days,
        )

        return HookStatisticsResponse(
            success=True,
            message="获取成功",
            total_executions=stats.get('total_executions', 0),
            success_count=stats.get('success_count', 0),
            failure_count=stats.get('failure_count', 0),
            success_rate=stats.get('success_rate', 0.0),
            avg_execution_time=stats.get('avg_execution_time', 0.0),
            by_hook=stats.get('by_hook', {}),
            by_trigger=stats.get('by_trigger', {}),
        )

    except Exception as e:
        logger.error(f"获取执行统计失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/validate",
    response_model=SuccessResponse,
    summary="验证 Hook 配置",
    description="验证 Hook 配置的有效性",
)
async def validate_hook(data: HookConfigSchema):
    """验证 Hook 配置"""
    try:
        from webmon.hooks.validator import ScriptValidator

        validator = ScriptValidator()
        errors = []

        # 验证脚本路径
        is_valid, error_msg = validator.validate_path(data.script)
        if not is_valid:
            errors.append(f"脚本路径: {error_msg}")

        # 验证类型
        if data.type not in ('shell', 'python'):
            errors.append(f"脚本类型必须是 'shell' 或 'python'，当前: {data.type}")

        # 验证超时
        if data.timeout < 1 or data.timeout > 300:
            errors.append("超时时间必须在 1-300 秒之间")

        # 验证重试次数
        if data.max_retries < 0 or data.max_retries > 5:
            errors.append("重试次数必须在 0-5 之间")

        if errors:
            return SuccessResponse(
                success=False,
                message="配置验证失败",
                data={"errors": errors}
            )

        return SuccessResponse(
            success=True,
            message="配置验证通过"
        )

    except Exception as e:
        logger.error(f"验证 Hook 配置失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
