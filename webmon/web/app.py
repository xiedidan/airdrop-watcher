"""
FastAPI 应用入口

创建和配置 FastAPI 应用实例。
"""

import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse

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

    # 静态文件目录
    static_dir = Path(__file__).parent / "static"

    # 挂载静态文件（如果存在）
    if static_dir.exists() and any(static_dir.iterdir()):
        # 挂载 assets 子目录（JS/CSS 文件）
        assets_dir = static_dir / "assets"
        if assets_dir.exists():
            app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

        # 挂载其他静态资源
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

        # 添加前端路由处理 - SPA 支持
        index_html = static_dir / "index.html"

        @app.get("/", response_class=HTMLResponse)
        async def serve_frontend():
            """服务前端首页"""
            if index_html.exists():
                return FileResponse(str(index_html))
            return HTMLResponse(content="<h1>WebMon</h1><p>Frontend not built. Run: cd frontend && npm run build</p>")

        # 捕获所有非 API 路由，返回 index.html（SPA 路由支持）
        @app.get("/{full_path:path}")
        async def serve_spa(request: Request, full_path: str):
            """SPA 路由支持 - 所有非 API/静态资源路径返回 index.html"""
            # 排除 API 和静态资源路径
            if full_path.startswith(("api/", "docs", "redoc", "openapi.json", "health", "status", "assets/", "static/")):
                return None
            # 检查是否是静态文件请求
            static_file = static_dir / full_path
            if static_file.exists() and static_file.is_file():
                return FileResponse(str(static_file))
            # 其他路径返回 index.html（SPA 路由）
            if index_html.exists():
                return FileResponse(str(index_html))
            return HTMLResponse(content="<h1>404 Not Found</h1>", status_code=404)

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
