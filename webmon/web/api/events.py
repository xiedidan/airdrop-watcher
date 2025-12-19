"""
SSE 事件流 API 路由

提供 Server-Sent Events 端点，用于实时推送事件到前端。
"""

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse

from webmon.web.services.event_manager import get_event_manager, EventType


router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("")
async def events(request: Request):
    """
    SSE 事件流端点

    建立 SSE 连接，接收实时事件推送。

    事件类型:
    - connected: 连接成功
    - heartbeat: 心跳保活（每30秒）
    - monitor_started: 监控启动
    - monitor_stopped: 监控停止
    - monitor_status: 监控状态更新
    - task_created: 任务创建
    - task_updated: 任务更新
    - task_deleted: 任务删除
    - task_enabled: 任务启用
    - task_disabled: 任务禁用
    - check_started: 检测开始
    - check_completed: 检测完成
    - check_failed: 检测失败
    - change_detected: 检测到变化
    - notification_sent: 通知发送成功
    - notification_failed: 通知发送失败

    Returns:
        SSE 事件流
    """
    manager = get_event_manager()
    queue = await manager.connect()

    async def event_stream():
        async for event in manager.event_generator(queue):
            # 检查客户端是否断开
            if await request.is_disconnected():
                break
            yield event

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # 禁用 nginx 缓冲
        }
    )


@router.get("/status")
async def events_status():
    """
    获取 SSE 服务状态

    Returns:
        连接状态信息
    """
    manager = get_event_manager()
    return {
        "code": 0,
        "message": "success",
        "data": {
            "connected_clients": manager.client_count,
            "heartbeat_interval": manager._heartbeat_interval,
        }
    }
