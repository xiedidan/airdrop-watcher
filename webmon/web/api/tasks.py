"""
任务管理 API 路由

提供任务 CRUD 的 RESTful API 端点。
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Depends

from webmon.web.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
    TaskActionResponse,
    TaskCheckResponse,
)
from webmon.web.services.task_service import TaskService, get_task_service

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


def task_dict_to_response(task: dict) -> TaskResponse:
    """将任务字典转换为响应模型"""
    return TaskResponse(
        id=task.get('id', ''),
        url=task.get('url', ''),
        name=task.get('name', ''),
        description=task.get('description', ''),
        selectors=task.get('selectors', []),
        interval=task.get('interval', 300),
        timeout=task.get('timeout', 30000),
        enabled=task.get('enabled', True),
        ai_prompt=task.get('ai_prompt', ''),
        created_at=task.get('created_at'),
        updated_at=task.get('updated_at'),
        last_check=task.get('last_check'),
        last_change=task.get('last_change'),
        change_count=task.get('change_count', 0),
        status=task.get('status', 'active'),
        error_count=task.get('error_count', 0),
        last_error=task.get('last_error'),
        last_error_message=task.get('last_error_message'),
    )


@router.get(
    "",
    response_model=TaskListResponse,
    summary="获取任务列表",
    description="获取所有监控任务的列表，支持按启用状态筛选"
)
async def list_tasks(
    enabled_only: bool = Query(False, description="是否只返回启用的任务"),
    service: TaskService = Depends(get_task_service)
) -> TaskListResponse:
    """获取任务列表"""
    tasks = service.list_tasks(enabled_only=enabled_only)
    items = [task_dict_to_response(t) for t in tasks]
    return TaskListResponse(items=items, total=len(items))


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="获取任务详情",
    description="根据任务ID获取单个任务的详细信息"
)
async def get_task(
    task_id: str,
    service: TaskService = Depends(get_task_service)
) -> TaskResponse:
    """获取单个任务"""
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"任务不存在: {task_id}")
    return task_dict_to_response(task)


@router.post(
    "",
    response_model=TaskActionResponse,
    status_code=201,
    summary="创建任务",
    description="创建一个新的监控任务"
)
async def create_task(
    task_data: TaskCreate,
    service: TaskService = Depends(get_task_service)
) -> TaskActionResponse:
    """创建新任务"""
    try:
        task = service.create_task(task_data.model_dump())
        return TaskActionResponse(
            success=True,
            message="任务创建成功",
            task=task_dict_to_response(task)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建任务失败: {str(e)}")


@router.put(
    "/{task_id}",
    response_model=TaskActionResponse,
    summary="更新任务",
    description="更新指定任务的配置"
)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    service: TaskService = Depends(get_task_service)
) -> TaskActionResponse:
    """更新任务"""
    try:
        # 只传递非None的字段
        updates = task_data.model_dump(exclude_none=True)
        task = service.update_task(task_id, updates)
        return TaskActionResponse(
            success=True,
            message="任务更新成功",
            task=task_dict_to_response(task)
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新任务失败: {str(e)}")


@router.delete(
    "/{task_id}",
    response_model=TaskActionResponse,
    summary="删除任务",
    description="删除指定的监控任务"
)
async def delete_task(
    task_id: str,
    service: TaskService = Depends(get_task_service)
) -> TaskActionResponse:
    """删除任务"""
    try:
        # 先获取任务信息用于响应
        task = service.get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail=f"任务不存在: {task_id}")

        service.delete_task(task_id)
        return TaskActionResponse(
            success=True,
            message="任务删除成功",
            task=task_dict_to_response(task)
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除任务失败: {str(e)}")


@router.patch(
    "/{task_id}/enable",
    response_model=TaskActionResponse,
    summary="启用任务",
    description="启用指定的监控任务"
)
async def enable_task(
    task_id: str,
    service: TaskService = Depends(get_task_service)
) -> TaskActionResponse:
    """启用任务"""
    try:
        task = service.enable_task(task_id)
        return TaskActionResponse(
            success=True,
            message="任务已启用",
            task=task_dict_to_response(task)
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启用任务失败: {str(e)}")


@router.patch(
    "/{task_id}/disable",
    response_model=TaskActionResponse,
    summary="禁用任务",
    description="禁用指定的监控任务"
)
async def disable_task(
    task_id: str,
    service: TaskService = Depends(get_task_service)
) -> TaskActionResponse:
    """禁用任务"""
    try:
        task = service.disable_task(task_id)
        return TaskActionResponse(
            success=True,
            message="任务已禁用",
            task=task_dict_to_response(task)
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"禁用任务失败: {str(e)}")


@router.post(
    "/{task_id}/check",
    response_model=TaskCheckResponse,
    summary="立即检测",
    description="立即执行指定任务的检测"
)
async def check_task_now(
    task_id: str,
    service: TaskService = Depends(get_task_service)
) -> TaskCheckResponse:
    """立即执行任务检测"""
    try:
        result = await service.check_task_now(task_id)
        return TaskCheckResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"执行检测失败: {str(e)}")
