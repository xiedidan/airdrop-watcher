"""
FastAPI 应用入口

创建和配置 FastAPI 应用实例。
"""

import os
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from webmon.web.api.root import router as root_router, set_start_time
from webmon.web.api.tasks import router as tasks_router
from webmon.web.api.monitor import router as monitor_router
from webmon.web.api.events import router as events_router
from webmon.web.api.history import router as history_router
from webmon.web.api.settings import router as settings_router
from webmon.web.api.notification import router as notification_router


# 全局应用实例
_app: Optional[FastAPI] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理

    处理启动和关闭时的初始化/清理工作。
    """
    # 启动时
    set_start_time()
    print("WebMon API 服务启动...")

    yield

    # 关闭时
    print("WebMon API 服务关闭...")


def create_app() -> FastAPI:
    """
    创建 FastAPI 应用实例

    Returns:
        配置好的 FastAPI 应用实例
    """
    global _app

    if _app is not None:
        return _app

    app = FastAPI(
        title="WebMon API",
        description="WebMon 网页监控工具 - RESTful API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )

    # 配置 CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 生产环境应限制
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 注册路由
    app.include_router(root_router)
    app.include_router(tasks_router)
    app.include_router(monitor_router)
    app.include_router(events_router)
    app.include_router(history_router)
    app.include_router(settings_router)
    app.include_router(notification_router)

    # 挂载静态文件（如果存在）
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    if os.path.exists(static_dir) and os.listdir(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")

    _app = app
    return app


def get_app() -> FastAPI:
    """
    获取 FastAPI 应用实例

    如果实例不存在则创建。

    Returns:
        FastAPI 应用实例
    """
    global _app
    if _app is None:
        _app = create_app()
    return _app


# 创建默认应用实例供 uvicorn 使用
app = create_app()
