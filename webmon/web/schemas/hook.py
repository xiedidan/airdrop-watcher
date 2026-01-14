"""
Hook 配置 API Schema

定义 Hook 相关的请求和响应模型。
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class HookConfigSchema(BaseModel):
    """Hook 配置模型"""
    name: str = Field(..., description="Hook 名称")
    type: str = Field(default="shell", description="脚本类型 (shell/python)")
    script: str = Field(..., description="脚本路径")
    enabled: bool = Field(default=True, description="是否启用")
    timeout: int = Field(default=30, ge=1, le=300, description="超时时间（秒）")
    async_exec: bool = Field(default=True, alias="async", description="是否异步执行")
    args: List[str] = Field(default_factory=list, description="命令行参数")
    env: Dict[str, str] = Field(default_factory=dict, description="环境变量")
    condition: Optional[str] = Field(default=None, description="执行条件表达式")
    working_dir: Optional[str] = Field(default=None, description="工作目录")
    max_retries: int = Field(default=0, ge=0, le=5, description="最大重试次数")

    class Config:
        populate_by_name = True


class HookConfigCreate(BaseModel):
    """创建 Hook 请求"""
    trigger: str = Field(..., description="触发点")
    hook: HookConfigSchema = Field(..., description="Hook 配置")


class HookConfigUpdate(BaseModel):
    """更新 Hook 请求"""
    name: Optional[str] = Field(default=None, description="Hook 名称")
    type: Optional[str] = Field(default=None, description="脚本类型")
    script: Optional[str] = Field(default=None, description="脚本路径")
    enabled: Optional[bool] = Field(default=None, description="是否启用")
    timeout: Optional[int] = Field(default=None, ge=1, le=300, description="超时时间")
    async_exec: Optional[bool] = Field(default=None, alias="async", description="是否异步执行")
    args: Optional[List[str]] = Field(default=None, description="命令行参数")
    env: Optional[Dict[str, str]] = Field(default=None, description="环境变量")
    condition: Optional[str] = Field(default=None, description="执行条件表达式")
    working_dir: Optional[str] = Field(default=None, description="工作目录")
    max_retries: Optional[int] = Field(default=None, ge=0, le=5, description="最大重试次数")

    class Config:
        populate_by_name = True


class HookResultSchema(BaseModel):
    """Hook 执行结果"""
    id: str = Field(..., description="执行记录 ID")
    hook_name: str = Field(..., description="Hook 名称")
    trigger: str = Field(..., description="触发点")
    task_id: str = Field(..., description="关联任务 ID")
    success: bool = Field(..., description="是否成功")
    exit_code: Optional[int] = Field(default=None, description="退出码")
    stdout: str = Field(default="", description="标准输出")
    stderr: str = Field(default="", description="标准错误")
    execution_time: float = Field(default=0.0, description="执行耗时（秒）")
    started_at: Optional[str] = Field(default=None, description="开始时间")
    finished_at: Optional[str] = Field(default=None, description="结束时间")
    error_message: Optional[str] = Field(default=None, description="错误信息")
    error_type: str = Field(default="none", description="错误类型")
    retry_count: int = Field(default=0, description="重试次数")


class HookListResponse(BaseModel):
    """Hook 列表响应"""
    success: bool = True
    message: str = "获取成功"
    hooks: Dict[str, List[HookConfigSchema]] = Field(
        default_factory=dict,
        description="按触发点分组的 Hook 列表"
    )
    enabled: bool = Field(default=False, description="Hook 功能是否启用")
    defaults: Dict[str, Any] = Field(
        default_factory=dict,
        description="默认配置"
    )


class HookHistoryResponse(BaseModel):
    """Hook 执行历史响应"""
    success: bool = True
    message: str = "获取成功"
    items: List[HookResultSchema] = Field(default_factory=list)
    total: int = Field(default=0, description="总记录数")


class HookStatisticsResponse(BaseModel):
    """Hook 统计响应"""
    success: bool = True
    message: str = "获取成功"
    total_executions: int = Field(default=0, description="总执行次数")
    success_count: int = Field(default=0, description="成功次数")
    failure_count: int = Field(default=0, description="失败次数")
    success_rate: float = Field(default=0.0, description="成功率")
    avg_execution_time: float = Field(default=0.0, description="平均执行时间")
    by_hook: Dict[str, Dict[str, Any]] = Field(default_factory=dict, description="按 Hook 分组统计")
    by_trigger: Dict[str, Dict[str, Any]] = Field(default_factory=dict, description="按触发点分组统计")


class HookTestRequest(BaseModel):
    """测试 Hook 请求"""
    trigger: str = Field(default="on_change_detected", description="模拟的触发点")
    task_id: Optional[str] = Field(default=None, description="模拟的任务 ID")


class HookTestResponse(BaseModel):
    """测试 Hook 响应"""
    success: bool
    message: str
    result: Optional[HookResultSchema] = None
