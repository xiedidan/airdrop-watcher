"""
检测结果数据模型
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional, List
import hashlib
import uuid


@dataclass
class CheckResult:
    """检测结果数据模型"""
    
    # 基础信息
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str = ""
    url: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    
    # 检测结果
    success: bool = True  # 是否成功
    content_hash: str = ""  # 内容哈希
    content_size: int = 0  # 内容大小（字节）
    load_time: float = 0.0  # 加载时间（秒）
    
    # 变化信息
    changed: bool = False  # 是否变化
    change_type: str = "none"  # 变化类型: none, content_change, structure_change, new_content
    
    # 错误信息
    error_message: Optional[str] = None  # 错误信息
    error_type: Optional[str] = None  # 错误类型
    
    # 提取的数据
    extracted_data: Dict[str, Any] = field(default_factory=dict)  # 提取的结构化数据
    content_preview: Optional[str] = None  # 内容预览（前500字符）
    
    # HTTP信息
    status_code: Optional[int] = None  # HTTP状态码
    response_headers: Dict[str, str] = field(default_factory=dict)  # 响应头
    
    # 性能指标
    dns_time: float = 0.0  # DNS解析时间
    connect_time: float = 0.0  # 连接时间
    download_time: float = 0.0  # 下载时间
    
    # 扩展字段
    metadata: Dict[str, Any] = field(default_factory=dict)  # 扩展元数据
    
    def __post_init__(self):
        """初始化后的处理"""
        # 确保change_type与changed状态一致
        if self.changed and self.change_type == "none":
            self.change_type = "content_change"
        elif not self.changed and self.change_type != "none":
            self.change_type = "none"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'url': self.url,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'success': self.success,
            'content_hash': self.content_hash,
            'content_size': self.content_size,
            'load_time': self.load_time,
            'changed': self.changed,
            'change_type': self.change_type,
            'error_message': self.error_message,
            'error_type': self.error_type,
            'extracted_data': self.extracted_data,
            'content_preview': self.content_preview,
            'status_code': self.status_code,
            'response_headers': self.response_headers,
            'dns_time': self.dns_time,
            'connect_time': self.connect_time,
            'download_time': self.download_time,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CheckResult':
        """从字典创建检测结果对象"""
        # 处理时间戳字段
        if 'timestamp' in data and data['timestamp']:
            if isinstance(data['timestamp'], str):
                data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        
        return cls(**data)
    
    def calculate_content_hash(self, content: str) -> str:
        """计算内容哈希"""
        if not content:
            return ""
        
        # 使用MD5哈希
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def set_content(self, content: str, calculate_hash: bool = True):
        """设置内容并计算哈希"""
        if content:
            self.content_size = len(content.encode('utf-8'))
            self.content_preview = content[:500] if len(content) > 500 else content
            
            if calculate_hash:
                self.content_hash = self.calculate_content_hash(content)
        else:
            self.content_size = 0
            self.content_preview = None
            self.content_hash = ""
    
    def mark_as_success(self, content: str = None, extracted_data: Dict[str, Any] = None):
        """标记为成功"""
        self.success = True
        self.error_message = None
        self.error_type = None
        
        if content is not None:
            self.set_content(content)
        
        if extracted_data is not None:
            self.extracted_data = extracted_data
    
    def mark_as_failed(self, error_message: str, error_type: str = None):
        """标记为失败"""
        self.success = False
        self.error_message = error_message
        self.error_type = error_type or "unknown_error"
        self.changed = False
        self.change_type = "none"
    
    def mark_as_changed(self, change_type: str = "content_change"):
        """标记为已变化"""
        self.changed = True
        self.change_type = change_type
    
    def mark_as_unchanged(self):
        """标记为未变化"""
        self.changed = False
        self.change_type = "none"
    
    def get_summary(self) -> Dict[str, Any]:
        """获取结果摘要信息"""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'url': self.url,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'success': self.success,
            'changed': self.changed,
            'change_type': self.change_type,
            'content_size': self.content_size,
            'load_time': self.load_time,
            'error_type': self.error_type
        }
    
    def get_error_summary(self) -> Optional[Dict[str, Any]]:
        """获取错误摘要"""
        if self.success:
            return None
        
        return {
            'error_type': self.error_type,
            'error_message': self.error_message,
            'status_code': self.status_code,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """获取性能指标"""
        return {
            'load_time': self.load_time,
            'dns_time': self.dns_time,
            'connect_time': self.connect_time,
            'download_time': self.download_time,
            'total_time': self.load_time
        }
    
    def validate(self) -> List[str]:
        """验证结果数据"""
        errors = []
        
        if not self.task_id:
            errors.append("任务ID不能为空")
        
        if not self.url:
            errors.append("URL不能为空")
        elif not self.url.startswith(('http://', 'https://')):
            errors.append("URL必须以http://或https://开头")
        
        if self.load_time < 0:
            errors.append("加载时间不能为负数")
        
        if self.content_size < 0:
            errors.append("内容大小不能为负数")
        
        valid_change_types = ['none', 'content_change', 'structure_change', 'new_content']
        if self.change_type not in valid_change_types:
            errors.append(f"无效的变化类型: {self.change_type}")
        
        if not self.success and not self.error_message:
            errors.append("失败结果必须有错误信息")
        
        return errors
    
    def is_content_valid(self) -> bool:
        """检查内容是否有效"""
        if not self.success:
            return False
        
        if not self.content_hash and not self.content_preview:
            return False
        
        if self.content_size == 0:
            return False
        
        return True
    
    def get_content_hash_short(self) -> str:
        """获取短哈希"""
        return self.content_hash[:8] if self.content_hash else ""
    
    def get_load_time_display(self) -> str:
        """获取加载时间显示"""
        if self.load_time < 1:
            return f"{int(self.load_time * 1000)}ms"
        else:
            return f"{self.load_time:.2f}s"
    
    def __str__(self) -> str:
        """字符串表示"""
        status = "✓" if self.success else "✗"
        changed = "🔄" if self.changed else "➖"
        return f"CheckResult({status} {changed} {self.url} @ {self.timestamp})"
    
    def __repr__(self) -> str:
        """对象表示"""
        return self.__str__()