"""
根路由模块

提供基础的状态和健康检查接口。
"""

import time
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends

from webmon.web.schemas.common import StatusResponse, HealthResponse

router = APIRouter(tags=["root"])

# 服务启动时间
_start_time: Optional[float] = None


def get_start_time() -> float:
    """获取服务启动时间"""
    global _start_time
    if _start_time is None:
        _start_time = time.time()
    return _start_time


def set_start_time():
    """设置服务启动时间"""
    global _start_time
    _start_time = time.time()


@router.get(
    "/status",
    response_model=StatusResponse,
    summary="获取服务状态",
    description="返回 WebMon 服务的当前运行状态"
)
async def get_status() -> StatusResponse:
    """
    获取服务状态

    返回服务的运行状态、版本信息和基础统计数据。
    """
    from webmon.web.services.monitor_service import get_monitor_status

    start_time = get_start_time()
    uptime = time.time() - start_time

    # 获取监控状态
    monitor_info = await get_monitor_status()

    return StatusResponse(
        status="running",
        version="1.0.0",
        uptime=uptime,
        monitor_status=monitor_info.get("status", "stopped"),
        active_tasks=monitor_info.get("active_tasks", 0),
        total_tasks=monitor_info.get("total_tasks", 0),
        timestamp=datetime.now()
    )


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="健康检查",
    description="检查服务各组件的健康状态"
)
async def health_check() -> HealthResponse:
    """
    健康检查

    检查各组件（存储、调度器等）的健康状态。
    """
    components = {
        "api": True,
        "storage": True,  # TODO: 实际检查存储状态
        "scheduler": True,  # TODO: 实际检查调度器状态
    }

    healthy = all(components.values())

    return HealthResponse(
        healthy=healthy,
        components=components,
        timestamp=datetime.now()
    )


@router.get(
    "/api",
    response_model=dict,
    summary="API 信息",
    description="返回 API 版本和可用端点信息"
)
async def api_info() -> dict:
    """
    获取 API 信息

    返回 API 版本和文档链接。
    """
    return {
        "name": "WebMon API",
        "version": "v1",
        "description": "WebMon 网页监控工具 API",
        "docs_url": "/docs",
        "openapi_url": "/openapi.json",
        "endpoints": {
            "tasks": "/api/tasks",
            "monitor": "/api/monitor",
            "history": "/api/history",
            "settings": "/api/settings",
            "events": "/api/events"
        }
    }
