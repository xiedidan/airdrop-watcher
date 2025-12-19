"""
SSE 事件管理器

管理 SSE 连接和事件广播。
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Set, Any, Optional, AsyncGenerator
from dataclasses import dataclass, field, asdict
from enum import Enum


class EventType(str, Enum):
    """事件类型枚举"""
    # 连接事件
    CONNECTED = "connected"
    HEARTBEAT = "heartbeat"

    # 监控状态事件
    MONITOR_STARTED = "monitor_started"
    MONITOR_STOPPED = "monitor_stopped"
    MONITOR_STATUS = "monitor_status"

    # 任务事件
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_DELETED = "task_deleted"
    TASK_ENABLED = "task_enabled"
    TASK_DISABLED = "task_disabled"

    # 检测事件
    CHECK_STARTED = "check_started"
    CHECK_COMPLETED = "check_completed"
    CHECK_FAILED = "check_failed"
    CHANGE_DETECTED = "change_detected"

    # 通知事件
    NOTIFICATION_SENT = "notification_sent"
    NOTIFICATION_FAILED = "notification_failed"


@dataclass
class SSEEvent:
    """SSE 事件数据结构"""
    event: str
    data: Dict[str, Any]
    id: Optional[str] = None
    retry: Optional[int] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_sse(self) -> str:
        """转换为 SSE 格式字符串"""
        lines = []

        if self.id:
            lines.append(f"id: {self.id}")

        if self.retry:
            lines.append(f"retry: {self.retry}")

        lines.append(f"event: {self.event}")

        # 将数据和时间戳合并
        payload = {**self.data, "timestamp": self.timestamp}
        lines.append(f"data: {json.dumps(payload, ensure_ascii=False)}")

        return "\n".join(lines) + "\n\n"


class EventManager:
    """
    SSE 事件管理器

    负责管理客户端连接和广播事件。
    """

    def __init__(self):
        self._clients: Set[asyncio.Queue] = set()
        self._event_id: int = 0
        self._lock = asyncio.Lock()
        self._heartbeat_interval: int = 30  # 心跳间隔（秒）

    @property
    def client_count(self) -> int:
        """当前连接的客户端数量"""
        return len(self._clients)

    async def connect(self) -> asyncio.Queue:
        """
        创建新的客户端连接

        Returns:
            客户端事件队列
        """
        queue: asyncio.Queue = asyncio.Queue()
        async with self._lock:
            self._clients.add(queue)

        # 发送连接成功事件
        await self._send_to_queue(queue, SSEEvent(
            event=EventType.CONNECTED.value,
            data={"message": "连接成功", "client_id": id(queue)}
        ))

        return queue

    async def disconnect(self, queue: asyncio.Queue):
        """
        断开客户端连接

        Args:
            queue: 客户端事件队列
        """
        async with self._lock:
            self._clients.discard(queue)

    async def broadcast(self, event_type: EventType, data: Dict[str, Any]):
        """
        广播事件到所有连接的客户端

        Args:
            event_type: 事件类型
            data: 事件数据
        """
        if not self._clients:
            return

        self._event_id += 1
        event = SSEEvent(
            event=event_type.value,
            data=data,
            id=str(self._event_id)
        )

        async with self._lock:
            disconnected = set()
            for queue in self._clients:
                try:
                    await self._send_to_queue(queue, event)
                except Exception:
                    disconnected.add(queue)

            # 移除断开的连接
            for queue in disconnected:
                self._clients.discard(queue)

    async def _send_to_queue(self, queue: asyncio.Queue, event: SSEEvent):
        """发送事件到队列"""
        try:
            queue.put_nowait(event)
        except asyncio.QueueFull:
            # 队列满了，丢弃旧事件
            try:
                queue.get_nowait()
            except asyncio.QueueEmpty:
                pass
            queue.put_nowait(event)

    async def event_generator(self, queue: asyncio.Queue) -> AsyncGenerator[str, None]:
        """
        事件生成器

        生成 SSE 格式的事件流。

        Args:
            queue: 客户端事件队列

        Yields:
            SSE 格式的事件字符串
        """
        try:
            while True:
                try:
                    # 等待事件，超时后发送心跳
                    event = await asyncio.wait_for(
                        queue.get(),
                        timeout=self._heartbeat_interval
                    )
                    yield event.to_sse()
                except asyncio.TimeoutError:
                    # 发送心跳
                    heartbeat = SSEEvent(
                        event=EventType.HEARTBEAT.value,
                        data={"time": time.time()}
                    )
                    yield heartbeat.to_sse()
        except asyncio.CancelledError:
            pass
        finally:
            await self.disconnect(queue)


# 全局事件管理器实例
_event_manager: Optional[EventManager] = None


def get_event_manager() -> EventManager:
    """获取全局事件管理器实例"""
    global _event_manager
    if _event_manager is None:
        _event_manager = EventManager()
    return _event_manager


async def broadcast_event(event_type: EventType, data: Dict[str, Any]):
    """
    广播事件的便捷函数

    Args:
        event_type: 事件类型
        data: 事件数据
    """
    manager = get_event_manager()
    await manager.broadcast(event_type, data)
