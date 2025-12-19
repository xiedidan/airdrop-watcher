"""
API 路由模块

包含所有 RESTful API 端点的定义。
"""

from webmon.web.api.root import router as root_router
from webmon.web.api.tasks import router as tasks_router
from webmon.web.api.monitor import router as monitor_router

__all__ = [
    'root_router',
    'tasks_router',
    'monitor_router',
]
