"""
Pydantic 数据模型模块

定义 API 请求和响应的数据结构。
"""

from webmon.web.schemas.common import (
    StatusResponse,
    HealthResponse,
    ErrorResponse,
)

__all__ = [
    'StatusResponse',
    'HealthResponse',
    'ErrorResponse',
]
