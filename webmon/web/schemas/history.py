"""
历史记录数据模型

定义历史记录 API 的请求和响应数据结构。
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class HistoryEntryBase(BaseModel):
    """历史记录条目基础模型"""
    id: str = Field(..., description="记录ID")
    type: str = Field(..., description="记录类型: check_result/change_details")
    task_id: str = Field(..., description="关联的任务ID")
    url: str = Field(..., description="监控的URL")
    timestamp: str = Field(..., description="记录时间戳")


class CheckResultResponse(BaseModel):
    """检测结果响应"""
    id: str = Field(..., description="结果ID")
    task_id: str = Field(..., description="任务ID")
    url: str = Field(..., description="监控的URL")
    timestamp: Optional[str] = Field(None, description="检测时间")
    success: bool = Field(True, description="检测是否成功")
    content_hash: str = Field("", description="内容哈希")
    content_size: int = Field(0, description="内容大小（字节）")
    load_time: float = Field(0.0, description="加载时间（秒）")
    changed: bool = Field(False, description="是否有变化")
    change_type: str = Field("none", description="变化类型")
    content_diff: Optional[str] = Field(None, description="内容差异")
    added_lines: int = Field(0, description="新增行数")
    removed_lines: int = Field(0, description="删除行数")
    modified_lines: int = Field(0, description="修改行数")
    changes_summary: Optional[str] = Field(None, description="变化摘要")
    change_details: List[Dict[str, Any]] = Field(default_factory=list, description="变化详情")
    error_message: Optional[str] = Field(None, description="错误信息")
    error_type: Optional[str] = Field(None, description="错误类型")
    content_preview: Optional[str] = Field(None, description="内容预览")
    status_code: Optional[int] = Field(None, description="HTTP状态码")


class ChangeDetailsResponse(BaseModel):
    """变化详情响应"""
    id: str = Field(..., description="详情ID")
    task_id: str = Field(..., description="任务ID")
    url: str = Field(..., description="监控的URL")
    timestamp: Optional[str] = Field(None, description="变化时间")
    change_type: str = Field("", description="变化类型")
    change_summary: Optional[str] = Field(None, description="变化摘要")
    old_content: Optional[str] = Field(None, description="旧内容")
    new_content: Optional[str] = Field(None, description="新内容")
    diff: Optional[str] = Field(None, description="差异内容")
    ai_summary: Optional[str] = Field(None, description="AI分析摘要")


class HistoryEntryResponse(BaseModel):
    """历史记录条目响应"""
    id: str = Field(..., description="记录ID")
    type: str = Field(..., description="记录类型: check_result/change_details")
    task_id: str = Field(..., description="关联的任务ID")
    url: str = Field(..., description="监控的URL")
    timestamp: str = Field(..., description="记录时间戳")
    data: Dict[str, Any] = Field(default_factory=dict, description="详细数据")


class HistoryListResponse(BaseModel):
    """历史记录列表响应"""
    items: List[HistoryEntryResponse] = Field(..., description="记录列表")
    total: int = Field(..., description="总数量")
    page: int = Field(1, description="当前页码")
    page_size: int = Field(20, description="每页数量")
    total_pages: int = Field(1, description="总页数")


class HistoryStatisticsResponse(BaseModel):
    """历史统计响应"""
    total_entries: int = Field(0, description="总记录数")
    check_results: int = Field(0, description="检测结果数")
    change_details: int = Field(0, description="变化详情数")
    success_rate: float = Field(0.0, description="成功率")
    change_rate: float = Field(0.0, description="变化率")
    first_date: Optional[str] = Field(None, description="最早记录日期")
    last_date: Optional[str] = Field(None, description="最近记录日期")


class HistorySearchParams(BaseModel):
    """历史记录搜索参数"""
    task_id: Optional[str] = Field(None, description="按任务ID筛选")
    keyword: Optional[str] = Field(None, description="关键词搜索")
    start_date: Optional[str] = Field(None, description="开始日期 (ISO格式)")
    end_date: Optional[str] = Field(None, description="结束日期 (ISO格式)")
    success_only: bool = Field(False, description="只显示成功的记录")
    changed_only: bool = Field(False, description="只显示有变化的记录")
    entry_type: Optional[str] = Field(None, description="记录类型筛选: check_result/change_details")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")


class StorageInfoResponse(BaseModel):
    """存储信息响应"""
    file_path: str = Field(..., description="存储文件路径")
    file_size: int = Field(0, description="文件大小（字节）")
    created_at: Optional[str] = Field(None, description="创建时间")
    modified_at: Optional[str] = Field(None, description="修改时间")
    total_entries: int = Field(0, description="总记录数")
    first_entry_date: Optional[str] = Field(None, description="最早记录日期")
    last_entry_date: Optional[str] = Field(None, description="最近记录日期")
    max_entries: int = Field(1000, description="最大记录数限制")
    auto_cleanup_days: int = Field(30, description="自动清理天数")
