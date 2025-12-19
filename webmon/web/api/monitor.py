"""
监控控制 API 路由

提供监控器状态查询、启动、停止的 RESTful API 端点。
"""

from fastapi import APIRouter, HTTPException, Depends

from webmon.web.schemas.monitor import (
    MonitorStatus,
    MonitorActionResponse,
    MonitorStartRequest,
    MonitorStopRequest,
    SchedulerStats,
)
from webmon.web.services.monitor_service import MonitorService, get_monitor_service

router = APIRouter(prefix="/api/monitor", tags=["monitor"])


def dict_to_monitor_status(data: dict) -> MonitorStatus:
    """将字典转换为 MonitorStatus 模型"""
    return MonitorStatus(
        status=data.get('status', 'stopped'),
        is_running=data.get('is_running', False),
        start_time=data.get('start_time'),
        uptime=data.get('uptime', 0),
        total_tasks=data.get('total_tasks', 0),
        active_tasks=data.get('active_tasks', 0),
        running_tasks=data.get('running_tasks', 0),
        total_executions=data.get('total_executions', 0),
        successful_executions=data.get('successful_executions', 0),
        failed_executions=data.get('failed_executions', 0),
        total_changes=data.get('total_changes', 0),
        next_check=data.get('next_check'),
    )


@router.get(
    "/status",
    response_model=MonitorStatus,
    summary="获取监控状态",
    description="获取监控器的当前运行状态和统计信息"
)
async def get_monitor_status(
    service: MonitorService = Depends(get_monitor_service)
) -> MonitorStatus:
    """获取监控器状态"""
    try:
        status = await service.get_status()
        return dict_to_monitor_status(status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取监控状态失败: {str(e)}")


@router.post(
    "/start",
    response_model=MonitorActionResponse,
    summary="启动监控",
    description="启动监控器，开始执行所有启用的监控任务"
)
async def start_monitor(
    request: MonitorStartRequest = None,
    service: MonitorService = Depends(get_monitor_service)
) -> MonitorActionResponse:
    """启动监控器"""
    try:
        task_ids = request.task_ids if request else None
        result = await service.start(task_ids=task_ids)

        status = None
        if result.get('status'):
            status = dict_to_monitor_status(result['status'])

        return MonitorActionResponse(
            success=result.get('success', False),
            message=result.get('message', ''),
            status=status,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动监控器失败: {str(e)}")


@router.post(
    "/stop",
    response_model=MonitorActionResponse,
    summary="停止监控",
    description="停止监控器，等待所有运行中的任务完成后关闭"
)
async def stop_monitor(
    request: MonitorStopRequest = None,
    service: MonitorService = Depends(get_monitor_service)
) -> MonitorActionResponse:
    """停止监控器"""
    try:
        force = request.force if request else False
        wait_timeout = request.wait_timeout if request else 30

        result = await service.stop(force=force, wait_timeout=wait_timeout)

        status = None
        if result.get('status'):
            status = dict_to_monitor_status(result['status'])

        return MonitorActionResponse(
            success=result.get('success', False),
            message=result.get('message', ''),
            status=status,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"停止监控器失败: {str(e)}")


@router.get(
    "/stats",
    response_model=SchedulerStats,
    summary="获取调度器统计",
    description="获取调度器的详细统计信息和配置"
)
async def get_scheduler_stats(
    service: MonitorService = Depends(get_monitor_service)
) -> SchedulerStats:
    """获取调度器统计信息"""
    try:
        stats = await service.get_scheduler_stats()
        return SchedulerStats(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取调度器统计失败: {str(e)}")
