"""
任务相关的 Pydantic 数据模型

定义任务 API 的请求和响应数据结构。
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator, HttpUrl
import uuid


class TaskBase(BaseModel):
    """任务基础模型"""
    url: str = Field(..., description="监控的网页URL")
    name: str = Field(..., min_length=1, max_length=100, description="任务名称")
    description: str = Field("", max_length=500, description="任务描述（用于AI分析上下文）")
    selectors: List[str] = Field(default_factory=list, description="CSS选择器列表")
    interval: int = Field(300, ge=10, le=86400, description="检测间隔（秒）")
    timeout: int = Field(30000, ge=1000, le=120000, description="超时时间（毫秒）")
    enabled: bool = Field(True, description="是否启用")
    ai_prompt: str = Field("", description="自定义AI用户提示词")

    @field_validator('url')
    @classmethod
    def validate_url(cls, v: str) -> str:
        """验证URL格式"""
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL必须以 http:// 或 https:// 开头')
        return v

    @field_validator('selectors', mode='before')
    @classmethod
    def parse_selectors(cls, v):
        """解析选择器，支持字符串或列表"""
        if isinstance(v, str):
            if v:
                return [s.strip() for s in v.split(',') if s.strip()]
            return []
        return v or []


class TaskCreate(TaskBase):
    """创建任务请求模型"""
    pass


class TaskUpdate(BaseModel):
    """更新任务请求模型（所有字段可选）"""
    url: Optional[str] = Field(None, description="监控的网页URL")
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="任务名称")
    description: Optional[str] = Field(None, max_length=500, description="任务描述")
    selectors: Optional[List[str]] = Field(None, description="CSS选择器列表")
    interval: Optional[int] = Field(None, ge=10, le=86400, description="检测间隔（秒）")
    timeout: Optional[int] = Field(None, ge=1000, le=120000, description="超时时间（毫秒）")
    enabled: Optional[bool] = Field(None, description="是否启用")
    ai_prompt: Optional[str] = Field(None, description="自定义AI用户提示词")

    @field_validator('url')
    @classmethod
    def validate_url(cls, v: Optional[str]) -> Optional[str]:
        """验证URL格式"""
        if v is not None and not v.startswith(('http://', 'https://')):
            raise ValueError('URL必须以 http:// 或 https:// 开头')
        return v

    @field_validator('selectors', mode='before')
    @classmethod
    def parse_selectors(cls, v):
        """解析选择器"""
        if v is None:
            return None
        if isinstance(v, str):
            if v:
                return [s.strip() for s in v.split(',') if s.strip()]
            return []
        return v


class TaskResponse(BaseModel):
    """任务响应模型"""
    id: str = Field(..., description="任务ID")
    url: str = Field(..., description="监控的网页URL")
    name: str = Field(..., description="任务名称")
    description: str = Field("", description="任务描述")
    selectors: List[str] = Field(default_factory=list, description="CSS选择器列表")
    interval: int = Field(..., description="检测间隔（秒）")
    timeout: int = Field(..., description="超时时间（毫秒）")
    enabled: bool = Field(..., description="是否启用")
    ai_prompt: str = Field("", description="自定义AI用户提示词")

    # 时间戳
    created_at: Optional[str] = Field(None, description="创建时间")
    updated_at: Optional[str] = Field(None, description="更新时间")
    last_check: Optional[str] = Field(None, description="最后检测时间")
    last_change: Optional[str] = Field(None, description="最后变化时间")

    # 统计信息
    change_count: int = Field(0, description="变化次数")
    status: str = Field("active", description="任务状态")

    # 错误信息
    error_count: int = Field(0, description="连续错误次数")
    last_error: Optional[str] = Field(None, description="最后错误时间")
    last_error_message: Optional[str] = Field(None, description="最后错误信息")

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """任务列表响应"""
    items: List[TaskResponse] = Field(..., description="任务列表")
    total: int = Field(..., description="总数量")


class TaskActionResponse(BaseModel):
    """任务操作响应"""
    success: bool = Field(..., description="操作是否成功")
    message: str = Field(..., description="响应消息")
    task: Optional[TaskResponse] = Field(None, description="任务信息")


class TaskCheckResponse(BaseModel):
    """立即检测任务响应"""
    success: bool = Field(..., description="操作是否成功")
    message: str = Field(..., description="响应消息")
    task_id: str = Field(..., description="任务ID")
    changed: Optional[bool] = Field(None, description="是否检测到变化")
    error: Optional[str] = Field(None, description="错误信息")
