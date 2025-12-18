"""
WebMon Web API 模块

提供 FastAPI 后端服务，支持 WebUI 界面和 RESTful API。
"""

from webmon.web.app import create_app, get_app

__all__ = [
    'create_app',
    'get_app',
]
