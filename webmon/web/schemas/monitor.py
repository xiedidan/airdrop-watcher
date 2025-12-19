"""
监控控制相关的 Pydantic 数据模型

定义监控控制 API 的请求和响应数据结构。
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class MonitorStatus(BaseModel):
    """监控状态响应"""
    status: str = Field(..., description="监控状态: running/stopped")
    is_running: bool = Field(..., description="是否正在运行")
    start_time: Optional[str] = Field(None, description="启动时间")
    uptime: float = Field(0, description="运行时间（秒）")

    # 任务统计
    total_tasks: int = Field(0, description="总任务数")
    active_tasks: int = Field(0, description="活跃任务数")
    running_tasks: int = Field(0, description="正在执行的任务数")

    # 执行统计
    total_executions: int = Field(0, description="总执行次数")
    successful_executions: int = Field(0, description="成功执行次数")
    failed_executions: int = Field(0, description="失败执行次数")
    total_changes: int = Field(0, description="检测到的总变化数")

    # 下次执行
    next_check: Optional[str] = Field(None, description="下次检测时间")


class MonitorActionResponse(BaseModel):
    """监控操作响应"""
    success: bool = Field(..., description="操作是否成功")
    message: str = Field(..., description="响应消息")
    status: Optional[MonitorStatus] = Field(None, description="当前监控状态")


class MonitorStartRequest(BaseModel):
    """启动监控请求（可选参数）"""
    task_ids: Optional[List[str]] = Field(None, description="指定启动的任务ID列表，为空则启动所有")


class MonitorStopRequest(BaseModel):
    """停止监控请求（可选参数）"""
    force: bool = Field(False, description="是否强制停止")
    wait_timeout: int = Field(30, ge=1, le=300, description="等待超时时间（秒）")


class SchedulerStats(BaseModel):
    """调度器统计信息"""
    total_executions: int = Field(0, description="总执行次数")
    successful_executions: int = Field(0, description="成功执行次数")
    failed_executions: int = Field(0, description="失败执行次数")
    total_changes: int = Field(0, description="检测到的总变化数")
    start_time: Optional[str] = Field(None, description="启动时间")
    uptime: float = Field(0, description="运行时间（秒）")

    # 配置信息
    max_concurrent_tasks: int = Field(5, description="最大并发任务数")
    default_interval: int = Field(300, description="默认检测间隔（秒）")
