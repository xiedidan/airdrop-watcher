"""
Hook 管理器

负责 Hook 配置管理、触发点协调和执行调度。
"""

import asyncio
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from webmon.utils.logger import get_logger
from webmon.config import ConfigManager
from .config import HookConfig
from .result import HookResult
from .executor import HookExecutor
from .triggers import HookTrigger


class HookManager:
    """
    Hook 管理器

    核心职责：
    1. 从 ConfigManager 加载全局 Hook 配置
    2. 从 Task 对象获取任务级 Hook 配置
    3. 合并全局和任务级配置
    4. 根据触发点和条件筛选需要执行的 Hook
    5. 调用 HookExecutor 执行脚本
    6. 收集和返回执行结果
    """

    def __init__(
        self,
        config_manager: Optional[ConfigManager] = None,
        project_root: Optional[Path] = None
    ):
        """
        初始化 Hook 管理器

        Args:
            config_manager: 配置管理器
            project_root: 项目根目录
        """
        self.logger = get_logger(__name__)
        self.config_manager = config_manager or ConfigManager()
        self.project_root = project_root or Path.cwd()

        # 创建执行器
        self.executor = HookExecutor(project_root=self.project_root)

        # 缓存全局配置
        self._global_hooks: Dict[str, List[HookConfig]] = {}
        self._hooks_enabled: bool = False
        self._defaults: Dict[str, Any] = {}

        # 加载配置
        self._load_global_config()

    def _load_global_config(self):
        """加载全局 Hook 配置"""
        try:
            hooks_config = self.config_manager.get_config().get('hooks', {})

            # 全局开关
            self._hooks_enabled = hooks_config.get('enabled', False)

            if not self._hooks_enabled:
                self.logger.debug("Hook 功能已禁用")
                return

            # 默认配置
            self._defaults = hooks_config.get('defaults', {
                'timeout': 30,
                'async': True,
                'max_retries': 0,
            })

            # 全局 Hooks
            global_hooks = hooks_config.get('global_hooks', {})
            self._global_hooks = {}

            for trigger, hook_list in global_hooks.items():
                if not HookTrigger.is_valid(trigger):
                    self.logger.warning(f"无效的触发点: {trigger}，已跳过")
                    continue

                self._global_hooks[trigger] = []
                for hook_data in hook_list:
                    try:
                        # 应用默认配置
                        hook_data_with_defaults = self._apply_defaults(hook_data)
                        hook_config = HookConfig.from_dict(
                            hook_data_with_defaults,
                            is_global=True
                        )
                        self._global_hooks[trigger].append(hook_config)
                    except Exception as e:
                        self.logger.error(f"解析全局 Hook 配置失败: {e}")

            hook_count = sum(len(hooks) for hooks in self._global_hooks.values())
            self.logger.info(f"加载了 {hook_count} 个全局 Hook")

        except Exception as e:
            self.logger.error(f"加载全局 Hook 配置失败: {e}")
            self._hooks_enabled = False

    def _apply_defaults(self, hook_data: Dict[str, Any]) -> Dict[str, Any]:
        """应用默认配置"""
        result = hook_data.copy()

        for key, default_value in self._defaults.items():
            if key not in result:
                result[key] = default_value

        return result

    def reload_config(self):
        """重新加载配置"""
        self.logger.info("重新加载 Hook 配置")
        self._load_global_config()

    @property
    def is_enabled(self) -> bool:
        """Hook 功能是否启用"""
        return self._hooks_enabled

    def get_hooks_for_trigger(
        self,
        trigger: str,
        task_hooks: Optional[Dict[str, List[Dict]]] = None
    ) -> List[HookConfig]:
        """
        获取指定触发点的所有 Hook

        按顺序返回：先全局 Hook，后任务级 Hook

        Args:
            trigger: 触发点名称
            task_hooks: 任务级 Hook 配置

        Returns:
            Hook 配置列表
        """
        if not self._hooks_enabled:
            return []

        hooks = []

        # 添加全局 Hook
        if trigger in self._global_hooks:
            hooks.extend(self._global_hooks[trigger])

        # 添加任务级 Hook
        if task_hooks and trigger in task_hooks:
            for hook_data in task_hooks[trigger]:
                try:
                    hook_data_with_defaults = self._apply_defaults(hook_data)
                    hook_config = HookConfig.from_dict(
                        hook_data_with_defaults,
                        is_global=False
                    )
                    hooks.append(hook_config)
                except Exception as e:
                    self.logger.error(f"解析任务级 Hook 配置失败: {e}")

        # 过滤禁用的 Hook
        hooks = [h for h in hooks if h.enabled]

        return hooks

    def evaluate_condition(
        self,
        condition: Optional[str],
        context: Dict[str, Any]
    ) -> bool:
        """
        评估条件表达式

        支持的变量：
        - change_type: 变化类型
        - similarity: 相似度数值
        - task_name: 任务名称
        - has_ai_analysis: 是否有 AI 分析结果

        Args:
            condition: 条件表达式字符串
            context: 执行上下文

        Returns:
            条件是否满足
        """
        if not condition:
            return True  # 无条件则始终执行

        try:
            # 构建评估环境
            change = context.get('change', {})
            task = context.get('task', {})

            eval_context = {
                'change_type': change.get('type', ''),
                'similarity': float(change.get('similarity', 0)),
                'task_name': task.get('name', ''),
                'has_ai_analysis': context.get('ai_analysis') is not None,
            }

            # 安全评估：只允许简单的比较和逻辑操作
            # 验证表达式安全性
            if not self._is_safe_expression(condition):
                self.logger.warning(f"不安全的条件表达式: {condition}")
                return False

            # 执行评估
            result = eval(condition, {"__builtins__": {}}, eval_context)
            return bool(result)

        except Exception as e:
            self.logger.warning(f"评估条件表达式失败: {condition}, 错误: {e}")
            return False

    def _is_safe_expression(self, expression: str) -> bool:
        """
        检查表达式是否安全

        只允许：变量名、比较运算符、逻辑运算符、数字、字符串
        """
        # 允许的字符和关键字
        safe_pattern = r'^[\w\s\.\<\>\=\!\&\|\(\)\'\"0-9\-]+$'

        if not re.match(safe_pattern, expression):
            return False

        # 禁止的关键字
        forbidden = [
            'import', 'exec', 'eval', 'compile', 'open', 'file',
            '__', 'getattr', 'setattr', 'delattr', 'globals', 'locals',
            'dir', 'vars', 'type', 'class', 'def', 'lambda',
        ]

        expression_lower = expression.lower()
        for word in forbidden:
            if word in expression_lower:
                return False

        return True

    async def trigger(
        self,
        trigger: str,
        context: Dict[str, Any],
        task_hooks: Optional[Dict[str, List[Dict]]] = None
    ) -> List[HookResult]:
        """
        触发指定触发点的所有 Hook

        Args:
            trigger: 触发点名称
            context: 执行上下文
            task_hooks: 任务级 Hook 配置

        Returns:
            执行结果列表
        """
        if not self._hooks_enabled:
            return []

        if not HookTrigger.is_valid(trigger):
            self.logger.warning(f"无效的触发点: {trigger}")
            return []

        # 获取所有需要执行的 Hook
        hooks = self.get_hooks_for_trigger(trigger, task_hooks)

        if not hooks:
            self.logger.debug(f"触发点 {trigger} 没有配置 Hook")
            return []

        self.logger.info(f"触发点 {trigger}: 准备执行 {len(hooks)} 个 Hook")

        results = []
        sync_hooks = []
        async_hooks = []

        # 分类：同步和异步 Hook
        for hook in hooks:
            # 评估条件
            if not self.evaluate_condition(hook.condition, context):
                self.logger.debug(f"Hook {hook.name} 条件不满足，跳过")
                continue

            if hook.async_exec:
                async_hooks.append(hook)
            else:
                sync_hooks.append(hook)

        # 先执行同步 Hook（按顺序）
        for hook in sync_hooks:
            self.logger.debug(f"执行同步 Hook: {hook.name}")
            result = await self.executor.execute_with_retry(
                hook, trigger, context
            )
            results.append(result)

        # 再执行异步 Hook（并行）
        if async_hooks:
            self.logger.debug(f"并行执行 {len(async_hooks)} 个异步 Hook")
            async_tasks = [
                self.executor.execute_with_retry(hook, trigger, context)
                for hook in async_hooks
            ]
            async_results = await asyncio.gather(*async_tasks, return_exceptions=True)

            for i, result in enumerate(async_results):
                if isinstance(result, Exception):
                    # 创建失败结果
                    error_result = HookResult(
                        hook_name=async_hooks[i].name,
                        trigger=trigger,
                        task_id=context.get('task', {}).get('id', 'unknown')
                    )
                    error_result.mark_failure(f"执行异常: {result}")
                    results.append(error_result)
                else:
                    results.append(result)

        # 统计结果
        success_count = sum(1 for r in results if r.success)
        self.logger.info(
            f"触发点 {trigger}: 执行完成 "
            f"({success_count}/{len(results)} 成功)"
        )

        return results

    async def trigger_on_change_detected(
        self,
        task: Dict[str, Any],
        change: Dict[str, Any],
        task_hooks: Optional[Dict[str, List[Dict]]] = None
    ) -> List[HookResult]:
        """
        触发 on_change_detected 钩子

        Args:
            task: 任务信息
            change: 变化详情
            task_hooks: 任务级 Hook 配置

        Returns:
            执行结果列表
        """
        context = {
            'task': task,
            'change': change,
            'ai_analysis': None,
            'notification': None,
        }
        return await self.trigger(
            HookTrigger.ON_CHANGE_DETECTED.value,
            context,
            task_hooks
        )

    async def trigger_on_before_notify(
        self,
        task: Dict[str, Any],
        change: Dict[str, Any],
        ai_analysis: Optional[str] = None,
        task_hooks: Optional[Dict[str, List[Dict]]] = None
    ) -> List[HookResult]:
        """
        触发 on_before_notify 钩子

        Args:
            task: 任务信息
            change: 变化详情
            ai_analysis: AI 分析结果
            task_hooks: 任务级 Hook 配置

        Returns:
            执行结果列表
        """
        context = {
            'task': task,
            'change': change,
            'ai_analysis': ai_analysis,
            'notification': {'status': 'pending'},
        }
        return await self.trigger(
            HookTrigger.ON_BEFORE_NOTIFY.value,
            context,
            task_hooks
        )

    async def trigger_on_after_notify(
        self,
        task: Dict[str, Any],
        change: Dict[str, Any],
        ai_analysis: Optional[str] = None,
        notification_result: Optional[Dict] = None,
        task_hooks: Optional[Dict[str, List[Dict]]] = None
    ) -> List[HookResult]:
        """
        触发 on_after_notify 钩子

        Args:
            task: 任务信息
            change: 变化详情
            ai_analysis: AI 分析结果
            notification_result: 通知发送结果
            task_hooks: 任务级 Hook 配置

        Returns:
            执行结果列表
        """
        context = {
            'task': task,
            'change': change,
            'ai_analysis': ai_analysis,
            'notification': notification_result or {'status': 'success'},
        }
        return await self.trigger(
            HookTrigger.ON_AFTER_NOTIFY.value,
            context,
            task_hooks
        )

    async def trigger_on_notify_failed(
        self,
        task: Dict[str, Any],
        change: Dict[str, Any],
        ai_analysis: Optional[str] = None,
        error_message: Optional[str] = None,
        task_hooks: Optional[Dict[str, List[Dict]]] = None
    ) -> List[HookResult]:
        """
        触发 on_notify_failed 钩子

        Args:
            task: 任务信息
            change: 变化详情
            ai_analysis: AI 分析结果
            error_message: 错误信息
            task_hooks: 任务级 Hook 配置

        Returns:
            执行结果列表
        """
        context = {
            'task': task,
            'change': change,
            'ai_analysis': ai_analysis,
            'notification': {
                'status': 'failed',
                'error': error_message,
            },
        }
        return await self.trigger(
            HookTrigger.ON_NOTIFY_FAILED.value,
            context,
            task_hooks
        )

    def get_all_hooks(self) -> Dict[str, List[HookConfig]]:
        """获取所有全局 Hook"""
        return self._global_hooks.copy()

    def get_hook_by_name(self, name: str) -> Optional[HookConfig]:
        """按名称查找 Hook"""
        for hooks in self._global_hooks.values():
            for hook in hooks:
                if hook.name == name:
                    return hook
        return None
