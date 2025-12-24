"""
关于页面 API 模块

提供版本信息、项目链接和依赖信息的接口。
"""

import sys
import platform
from datetime import datetime
from typing import Dict, List, Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

# 版本号
VERSION = "1.0.0"

# 项目信息
PROJECT_INFO = {
    "name": "WebMon",
    "description": "网页监控工具 - 监控网页变化并发送通知",
    "version": VERSION,
    "author": "WebMon Team",
    "license": "MIT",
    "repository": "https://github.com/xiedidan/airdrop-watcher",
    "documentation": "https://github.com/xiedidan/airdrop-watcher#readme",
    "issues": "https://github.com/xiedidan/airdrop-watcher/issues",
}

# 核心依赖（手动维护）
CORE_DEPENDENCIES = [
    {"name": "FastAPI", "version": "0.104.0+", "description": "Web API 框架"},
    {"name": "Vue 3", "version": "3.x", "description": "前端框架"},
    {"name": "Naive UI", "version": "2.x", "description": "UI 组件库"},
    {"name": "Playwright", "version": "1.40.0+", "description": "浏览器自动化"},
    {"name": "Pydantic", "version": "2.5.0+", "description": "数据验证"},
    {"name": "Loguru", "version": "0.7.0+", "description": "日志管理"},
    {"name": "BeautifulSoup4", "version": "4.12.0+", "description": "HTML 解析"},
]


class DependencyInfo(BaseModel):
    """依赖信息"""
    name: str = Field(..., description="依赖名称")
    version: str = Field(..., description="版本")
    description: str = Field("", description="描述")


class SystemInfo(BaseModel):
    """系统信息"""
    python_version: str = Field(..., description="Python 版本")
    platform: str = Field(..., description="操作系统平台")
    platform_version: str = Field(..., description="平台版本")


class ProjectLinks(BaseModel):
    """项目链接"""
    repository: str = Field(..., description="GitHub 仓库")
    documentation: str = Field(..., description="文档地址")
    issues: str = Field(..., description="Issue 反馈")


class AboutResponse(BaseModel):
    """关于页面响应"""
    name: str = Field(..., description="项目名称")
    description: str = Field(..., description="项目描述")
    version: str = Field(..., description="版本号")
    author: str = Field(..., description="作者")
    license: str = Field(..., description="许可证")
    links: ProjectLinks = Field(..., description="项目链接")
    system: SystemInfo = Field(..., description="系统信息")
    dependencies: List[DependencyInfo] = Field(..., description="核心依赖")
    timestamp: datetime = Field(..., description="响应时间")


router = APIRouter(prefix="/api/about", tags=["about"])


@router.get(
    "",
    response_model=AboutResponse,
    summary="获取关于信息",
    description="返回项目版本、链接和依赖信息"
)
async def get_about() -> AboutResponse:
    """
    获取关于信息

    返回项目的版本信息、链接和系统依赖。
    """
    return AboutResponse(
        name=PROJECT_INFO["name"],
        description=PROJECT_INFO["description"],
        version=PROJECT_INFO["version"],
        author=PROJECT_INFO["author"],
        license=PROJECT_INFO["license"],
        links=ProjectLinks(
            repository=PROJECT_INFO["repository"],
            documentation=PROJECT_INFO["documentation"],
            issues=PROJECT_INFO["issues"],
        ),
        system=SystemInfo(
            python_version=sys.version.split()[0],
            platform=platform.system(),
            platform_version=platform.release(),
        ),
        dependencies=[
            DependencyInfo(**dep) for dep in CORE_DEPENDENCIES
        ],
        timestamp=datetime.now(),
    )


@router.get(
    "/version",
    response_model=Dict[str, str],
    summary="获取版本号",
    description="仅返回版本号"
)
async def get_version() -> Dict[str, str]:
    """获取版本号"""
    return {"version": VERSION}
