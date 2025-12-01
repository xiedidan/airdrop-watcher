"""
变化详情数据模型
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional, List
import difflib
import uuid


@dataclass
class ChangeDetails:
    """变化详情数据模型"""
    
    # 基础信息
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str = ""
    url: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    check_result_id: str = ""  # 关联的检测结果ID
    
    # 相似度信息
    similarity: float = 1.0  # 相似度 (0.0-1.0)
    similarity_threshold: float = 0.85  # 相似度阈值
    
    # 变化详情
    changes: Dict[str, Any] = field(default_factory=dict)  # 详细变化信息
    change_count: int = 0  # 变化数量
    
    # 内容对比
    old_content: str = ""  # 旧内容
    new_content: str = ""  # 新内容
    old_content_hash: str = ""  # 旧内容哈希
    new_content_hash: str = ""  # 新内容哈希
    
    # 变化总结
    change_summary: str = ""  # 变化总结
    change_types: List[str] = field(default_factory=list)  # 变化类型列表
    
    # 结构化变化
    field_changes: Dict[str, Dict[str, Any]] = field(default_factory=dict)  # 字段变化
    added_fields: List[str] = field(default_factory=list)  # 新增字段
    removed_fields: List[str] = field(default_factory=list)  # 删除字段
    modified_fields: List[str] = field(default_factory=list)  # 修改字段
    
    # 内容统计
    old_content_size: int = 0  # 旧内容大小
    new_content_size: int = 0  # 新内容大小
    size_change: int = 0  # 大小变化
    
    # 差异信息
    diff_lines: List[str] = field(default_factory=list)  # 差异行
    unified_diff: str = ""  # 统一差异格式
    
    # 扩展字段
    metadata: Dict[str, Any] = field(default_factory=dict)  # 扩展元数据
    
    def __post_init__(self):
        """初始化后的处理"""
        # 计算内容大小变化
        self.size_change = self.new_content_size - self.old_content_size
        
        # 确保相似度在有效范围内
        self.similarity = max(0.0, min(1.0, self.similarity))
        
        # 生成变化总结
        if not self.change_summary and (self.old_content or self.new_content):
            self.generate_change_summary()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'url': self.url,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'check_result_id': self.check_result_id,
            'similarity': self.similarity,
            'similarity_threshold': self.similarity_threshold,
            'changes': self.changes,
            'change_count': self.change_count,
            'old_content': self.old_content,
            'new_content': self.new_content,
            'old_content_hash': self.old_content_hash,
            'new_content_hash': self.new_content_hash,
            'change_summary': self.change_summary,
            'change_types': self.change_types,
            'field_changes': self.field_changes,
            'added_fields': self.added_fields,
            'removed_fields': self.removed_fields,
            'modified_fields': self.modified_fields,
            'old_content_size': self.old_content_size,
            'new_content_size': self.new_content_size,
            'size_change': self.size_change,
            'diff_lines': self.diff_lines,
            'unified_diff': self.unified_diff,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChangeDetails':
        """从字典创建变化详情对象"""
        # 处理时间戳字段
        if 'timestamp' in data and data['timestamp']:
            if isinstance(data['timestamp'], str):
                data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        
        return cls(**data)
    
    def calculate_similarity(self, old_content: str = None, new_content: str = None) -> float:
        """计算内容相似度"""
        old = old_content or self.old_content
        new = new_content or self.new_content
        
        if not old and not new:
            return 1.0
        elif not old or not new:
            return 0.0
        
        # 使用difflib计算相似度
        similarity = difflib.SequenceMatcher(None, old, new).ratio()
        self.similarity = similarity
        return similarity
    
    def generate_diff(self, old_content: str = None, new_content: str = None) -> List[str]:
        """生成差异信息"""
        old = old_content or self.old_content
        new = new_content or self.new_content
        
        if not old and not new:
            self.diff_lines = []
            return self.diff_lines
        
        # 将内容按行分割
        old_lines = old.splitlines() if old else []
        new_lines = new.splitlines() if new else []
        
        # 生成差异
        differ = difflib.Differ()
        diff_lines = list(differ.compare(old_lines, new_lines))
        
        self.diff_lines = diff_lines
        return diff_lines
    
    def generate_unified_diff(self, old_content: str = None, new_content: str = None, 
                            context_lines: int = 3) -> str:
        """生成统一差异格式"""
        old = old_content or self.old_content
        new = new_content or self.new_content
        
        if not old and not new:
            self.unified_diff = ""
            return self.unified_diff
        
        # 将内容按行分割
        old_lines = old.splitlines(keepends=True) if old else []
        new_lines = new.splitlines(keepends=True) if new else []
        
        # 生成统一差异
        unified_diff = difflib.unified_diff(
            old_lines, 
            new_lines,
            fromfile='old_content',
            tofile='new_content',
            n=context_lines
        )
        
        self.unified_diff = ''.join(unified_diff)
        return self.unified_diff
    
    def generate_change_summary(self) -> str:
        """生成变化总结"""
        if not self.old_content and not self.new_content:
            self.change_summary = "无内容可比较"
            return self.change_summary
        
        if not self.old_content:
            self.change_summary = "新增内容"
            return self.change_summary
        
        if not self.new_content:
            self.change_summary = "内容被删除"
            return self.change_summary
        
        # 计算变化统计
        old_lines = self.old_content.splitlines()
        new_lines = self.new_content.splitlines()
        
        added_lines = len([line for line in self.diff_lines if line.startswith('+ ')])
        removed_lines = len([line for line in self.diff_lines if line.startswith('- ')])
        
        # 生成总结
        summary_parts = []
        
        # 相似度信息
        similarity_percent = int(self.similarity * 100)
        summary_parts.append(f"相似度: {similarity_percent}%")
        
        # 变化统计
        if added_lines > 0:
            summary_parts.append(f"新增: {added_lines}行")
        
        if removed_lines > 0:
            summary_parts.append(f"删除: {removed_lines}行")
        
        # 大小变化
        if self.size_change > 0:
            summary_parts.append(f"大小增加: {self.size_change}字节")
        elif self.size_change < 0:
            summary_parts.append(f"大小减少: {abs(self.size_change)}字节")
        
        # 字段变化
        if self.added_fields:
            summary_parts.append(f"新增字段: {', '.join(self.added_fields[:3])}")
            if len(self.added_fields) > 3:
                summary_parts[-1] += f"等{len(self.added_fields)}个"
        
        if self.removed_fields:
            summary_parts.append(f"删除字段: {', '.join(self.removed_fields[:3])}")
            if len(self.removed_fields) > 3:
                summary_parts[-1] += f"等{len(self.removed_fields)}个"
        
        if self.modified_fields:
            summary_parts.append(f"修改字段: {', '.join(self.modified_fields[:3])}")
            if len(self.modified_fields) > 3:
                summary_parts[-1] += f"等{len(self.modified_fields)}个"
        
        self.change_summary = "; ".join(summary_parts)
        return self.change_summary
    
    def analyze_field_changes(self, old_data: Dict[str, Any], new_data: Dict[str, Any]):
        """分析字段变化"""
        self.field_changes = {}
        self.added_fields = []
        self.removed_fields = []
        self.modified_fields = []
        
        # 获取所有字段
        all_fields = set(old_data.keys()) | set(new_data.keys())
        
        for field in all_fields:
            old_value = old_data.get(field)
            new_value = new_data.get(field)
            
            if field not in old_data:
                # 新增字段
                self.added_fields.append(field)
                self.field_changes[field] = {
                    'type': 'added',
                    'new_value': new_value
                }
            elif field not in new_data:
                # 删除字段
                self.removed_fields.append(field)
                self.field_changes[field] = {
                    'type': 'removed',
                    'old_value': old_value
                }
            elif old_value != new_value:
                # 修改字段
                self.modified_fields.append(field)
                self.field_changes[field] = {
                    'type': 'modified',
                    'old_value': old_value,
                    'new_value': new_value
                }
        
        # 更新变化数量
        self.change_count = len(self.added_fields) + len(self.removed_fields) + len(self.modified_fields)
    
    def has_significant_changes(self, similarity_threshold: float = None) -> bool:
        """检查是否有显著变化"""
        threshold = similarity_threshold or self.similarity_threshold
        return self.similarity < threshold
    
    def get_significant_changes(self) -> Dict[str, Any]:
        """获取显著变化信息"""
        if not self.has_significant_changes():
            return {}
        
        return {
            'similarity': self.similarity,
            'change_count': self.change_count,
            'size_change': self.size_change,
            'field_changes': self.field_changes,
            'change_summary': self.change_summary
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """获取变化摘要信息"""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'url': self.url,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'similarity': self.similarity,
            'change_count': self.change_count,
            'change_summary': self.change_summary,
            'size_change': self.size_change,
            'has_significant_changes': self.has_significant_changes()
        }
    
    def validate(self) -> List[str]:
        """验证变化详情数据"""
        errors = []
        
        if not self.task_id:
            errors.append("任务ID不能为空")
        
        if not self.url:
            errors.append("URL不能为空")
        
        if not (0.0 <= self.similarity <= 1.0):
            errors.append("相似度必须在0.0-1.0范围内")
        
        if not (0.0 <= self.similarity_threshold <= 1.0):
            errors.append("相似度阈值必须在0.0-1.0范围内")
        
        if self.change_count < 0:
            errors.append("变化数量不能为负数")
        
        if self.old_content_size < 0 or self.new_content_size < 0:
            errors.append("内容大小不能为负数")
        
        return errors
    
    def get_similarity_display(self) -> str:
        """获取相似度显示"""
        percent = int(self.similarity * 100)
        if self.similarity >= 0.95:
            return f"{percent}% (几乎相同)"
        elif self.similarity >= 0.85:
            return f"{percent}% (高度相似)"
        elif self.similarity >= 0.70:
            return f"{percent}% (中度相似)"
        elif self.similarity >= 0.50:
            return f"{percent}% (低度相似)"
        else:
            return f"{percent}% (差异很大)"
    
    def get_size_change_display(self) -> str:
        """获取大小变化显示"""
        if self.size_change > 0:
            return f"+{self.size_change}字节"
        elif self.size_change < 0:
            return f"{self.size_change}字节"
        else:
            return "大小无变化"
    
    def __str__(self) -> str:
        """字符串表示"""
        similarity = int(self.similarity * 100)
        return f"ChangeDetails(similarity={similarity}%, changes={self.change_count}, summary='{self.change_summary[:50]}...')"
    
    def __repr__(self) -> str:
        """对象表示"""
        return self.__str__()