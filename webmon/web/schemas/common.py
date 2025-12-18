"""
通用响应数据模型

定义 API 通用的请求和响应数据结构。
"""

from datetime import datetime
from typing import Optional, Any, Dict, List
from pydantic import BaseModel, Field


class StatusResponse(BaseModel):
    """服务状态响应"""
    status: str = Field(..., description="服务状态: running/stopped")
    version: str = Field(..., description="WebMon 版本号")
    uptime: float = Field(..., description="服务运行时间（秒）")
    monitor_status: str = Field(..., description="监控器状态: running/stopped")
    active_tasks: int = Field(0, description="活跃任务数")
    total_tasks: int = Field(0, description="总任务数")
    timestamp: datetime = Field(default_factory=datetime.now, description="响应时间戳")


class HealthResponse(BaseModel):
    """健康检查响应"""
    healthy: bool = Field(..., description="服务是否健康")
    components: Dict[str, bool] = Field(
        default_factory=dict,
        description="各组件健康状态"
    )
    timestamp: datetime = Field(default_factory=datetime.now)


class ErrorResponse(BaseModel):
    """错误响应"""
    error: str = Field(..., description="错误类型")
    message: str = Field(..., description="错误消息")
    detail: Optional[str] = Field(None, description="详细错误信息")
    timestamp: datetime = Field(default_factory=datetime.now)


class SuccessResponse(BaseModel):
    """成功响应"""
    success: bool = Field(True, description="操作是否成功")
    message: str = Field("操作成功", description="响应消息")
    data: Optional[Any] = Field(None, description="响应数据")


class PaginationParams(BaseModel):
    """分页参数"""
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")


class PaginatedResponse(BaseModel):
    """分页响应"""
    items: List[Any] = Field(..., description="数据列表")
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数量")
    total_pages: int = Field(..., description="总页数")
