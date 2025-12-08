"""
任务数据模型
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
import uuid


@dataclass
class Task:
    """监控任务数据模型"""
    
    # 基础信息
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    url: str = ""
    name: str = ""
    selectors: List[str] = field(default_factory=list)
    
    # 监控配置
    interval: int = 300  # 检测间隔（秒）
    timeout: int = 30000  # 超时时间（毫秒）
    enabled: bool = True  # 是否启用
    
    # 时间戳
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_check: Optional[datetime] = None  # 最后检测时间
    last_change: Optional[datetime] = None  # 最后变化时间
    
    # 统计信息
    change_count: int = 0  # 变化次数
    status: str = "active"  # 任务状态: active, paused, error

    # 错误跟踪（用于自动恢复）
    error_count: int = 0  # 连续错误次数
    last_error: Optional[datetime] = None  # 最后一次错误时间
    last_error_message: Optional[str] = None  # 最后一次错误信息

    # 扩展字段
    metadata: Dict[str, Any] = field(default_factory=dict)  # 扩展元数据
    
    def __post_init__(self):
        """初始化后的处理"""
        if not self.name and self.url:
            self.name = self.url.split('//')[-1].split('/')[0]
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'id': self.id,
            'url': self.url,
            'name': self.name,
            'selectors': self.selectors,
            'interval': self.interval,
            'timeout': self.timeout,
            'enabled': self.enabled,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_check': self.last_check.isoformat() if self.last_check else None,
            'last_change': self.last_change.isoformat() if self.last_change else None,
            'change_count': self.change_count,
            'status': self.status,
            'error_count': self.error_count,
            'last_error': self.last_error.isoformat() if self.last_error else None,
            'last_error_message': self.last_error_message,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """从字典创建任务对象"""
        # 处理时间戳字段
        for field_name in ['created_at', 'updated_at', 'last_check', 'last_change', 'last_error']:
            if field_name in data and data[field_name]:
                if isinstance(data[field_name], str):
                    data[field_name] = datetime.fromisoformat(data[field_name])
        
        # 处理selector/selectors字段兼容性
        if 'selector' in data and 'selectors' not in data:
            selector = data.pop('selector')
            if selector:
                data['selectors'] = [selector]
            else:
                data['selectors'] = []
        
        # 处理单位转换（分钟->秒，秒->毫秒）
        if 'interval' in data and data['interval'] < 60:
            # 假设小于60的值是分钟，需要转换为秒
            data['interval'] = data['interval'] * 60
        
        if 'timeout' in data and data['timeout'] < 1000:
            # 假设小于1000的值是秒，需要转换为毫秒
            data['timeout'] = data['timeout'] * 1000
        
        return cls(**data)
    
    def update_timestamp(self):
        """更新时间戳"""
        self.updated_at = datetime.now()
    
    def mark_as_checked(self):
        """标记为已检测"""
        self.last_check = datetime.now()
        self.update_timestamp()
    
    def mark_as_changed(self):
        """标记为已变化"""
        self.last_change = datetime.now()
        self.change_count += 1
        self.update_timestamp()
    
    def set_status(self, status: str):
        """设置任务状态"""
        valid_statuses = ['active', 'paused', 'error', 'completed']
        if status not in valid_statuses:
            raise ValueError(f"无效的状态: {status}. 有效状态: {valid_statuses}")
        self.status = status
        self.update_timestamp()
    
    def is_active(self) -> bool:
        """检查任务是否活跃"""
        return self.enabled and self.status == 'active'
    
    def get_summary(self) -> Dict[str, Any]:
        """获取任务摘要信息"""
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'enabled': self.enabled,
            'status': self.status,
            'interval': self.interval,
            'last_check': self.last_check.isoformat() if self.last_check else None,
            'last_change': self.last_change.isoformat() if self.last_change else None,
            'change_count': self.change_count
        }
    
    def validate(self) -> List[str]:
        """验证任务数据"""
        errors = []
        
        if not self.url:
            errors.append("URL不能为空")
        elif not self.url.startswith(('http://', 'https://')):
            errors.append("URL必须以http://或https://开头")
        
        if not self.name:
            errors.append("任务名称不能为空")
        
        if self.interval <= 0:
            errors.append("检测间隔必须大于0")
        
        if self.timeout <= 0:
            errors.append("超时时间必须大于0")
        
        if self.status not in ['active', 'paused', 'error', 'completed']:
            errors.append(f"无效的任务状态: {self.status}")
        
        return errors
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"Task(id={self.id}, name='{self.name}', url='{self.url}', status={self.status})"
    
    def __repr__(self) -> str:
        """对象表示"""
        return self.__str__()