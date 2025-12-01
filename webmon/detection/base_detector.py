"""
变化检测算法基类

提供变化检测的基础框架和通用功能。
"""
import hashlib
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Union
from datetime import datetime

from ..exceptions import DetectionError


class BaseChangeDetector(ABC):
    """变化检测算法基类"""
    
    def __init__(self, algorithm_name: str = "base", **kwargs):
        """
        初始化变化检测器
        
        Args:
            algorithm_name: 算法名称
            **kwargs: 其他参数
        """
        self.algorithm_name = algorithm_name
        self.config = kwargs
        self.history = {}  # 存储历史数据用于比较
    
    @abstractmethod
    def detect_changes(self, old_content: str, new_content: str, **kwargs) -> Dict[str, Any]:
        """
        检测内容变化
        
        Args:
            old_content: 旧内容
            new_content: 新内容
            **kwargs: 其他参数
            
        Returns:
            检测结果字典
        """
        pass
    
    def validate_content(self, content: str) -> bool:
        """
        验证内容有效性
        
        Args:
            content: 要验证的内容
            
        Returns:
            是否有效
        """
        if content is None:
            return False
        
        if not isinstance(content, str):
            return False
        
        # 内容长度检查（至少10个字符）
        if len(content.strip()) < 10:
            return False
        
        return True
    
    def store_history(self, key: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """
        存储历史数据
        
        Args:
            key: 历史数据键
            content: 内容
            metadata: 元数据
        """
        self.history[key] = {
            "content": content,
            "timestamp": datetime.now(),
            "metadata": metadata or {}
        }
    
    def get_history(self, key: str) -> Optional[Dict[str, Any]]:
        """
        获取历史数据
        
        Args:
            key: 历史数据键
            
        Returns:
            历史数据，不存在返回None
        """
        return self.history.get(key)
    
    def clear_history(self, key: Optional[str] = None):
        """
        清除历史数据
        
        Args:
            key: 要清除的键，如果为None则清除所有
        """
        if key is None:
            self.history.clear()
        else:
            self.history.pop(key, None)
    
    def get_algorithm_info(self) -> Dict[str, Any]:
        """
        获取算法信息
        
        Returns:
            算法信息字典
        """
        return {
            "algorithm_name": self.algorithm_name,
            "config": self.config,
            "history_count": len(self.history)
        }


class HashChangeDetector(BaseChangeDetector):
    """哈希变化检测器"""
    
    def __init__(self, hash_algorithm: str = "md5", **kwargs):
        """
        初始化哈希变化检测器
        
        Args:
            hash_algorithm: 哈希算法（md5, sha1, sha256）
            **kwargs: 其他参数
        """
        super().__init__("hash", **kwargs)
        self.hash_algorithm = hash_algorithm.lower()
        
        # 验证哈希算法
        valid_algorithms = ["md5", "sha1", "sha256", "sha512"]
        if self.hash_algorithm not in valid_algorithms:
            raise DetectionError(f"不支持的哈希算法: {hash_algorithm}")
    
    def detect_changes(self, old_content: str, new_content: str, **kwargs) -> Dict[str, Any]:
        """
        使用哈希算法检测内容变化
        
        Args:
            old_content: 旧内容
            new_content: 新内容
            **kwargs: 其他参数
            
        Returns:
            检测结果字典
            
        Raises:
            DetectionError: 检测失败
        """
        try:
            start_time = time.time()
            
            # 验证内容
            if not self.validate_content(old_content) or not self.validate_content(new_content):
                return {
                    "changed": False,
                    "error": "内容验证失败",
                    "old_content_valid": self.validate_content(old_content),
                    "new_content_valid": self.validate_content(new_content),
                    "algorithm": self.algorithm_name,
                    "hash_algorithm": self.hash_algorithm
                }
            
            # 计算哈希值
            old_hash = self._calculate_hash(old_content)
            new_hash = self._calculate_hash(new_content)
            
            # 检测变化
            changed = old_hash != new_hash
            
            # 计算检测时间
            detection_time = time.time() - start_time
            
            result = {
                "changed": changed,
                "old_hash": old_hash,
                "new_hash": new_hash,
                "hash_algorithm": self.hash_algorithm,
                "algorithm": self.algorithm_name,
                "detection_time": detection_time,
                "old_content_size": len(old_content),
                "new_content_size": len(new_content)
            }
            
            # 如果有变化，添加详细信息
            if changed:
                result.update({
                    "change_type": "content_change",
                    "change_summary": f"内容哈希从 {old_hash[:8]} 变为 {new_hash[:8]}",
                    "size_change": len(new_content) - len(old_content)
                })
            
            return result
            
        except Exception as e:
            raise DetectionError(f"哈希检测失败: {e}", algorithm=self.algorithm_name)
    
    def _calculate_hash(self, content: str) -> str:
        """
        计算内容哈希值
        
        Args:
            content: 内容
            
        Returns:
            哈希值
        """
        try:
            content_bytes = content.encode('utf-8')
            
            if self.hash_algorithm == "md5":
                return hashlib.md5(content_bytes).hexdigest()
            elif self.hash_algorithm == "sha1":
                return hashlib.sha1(content_bytes).hexdigest()
            elif self.hash_algorithm == "sha256":
                return hashlib.sha256(content_bytes).hexdigest()
            elif self.hash_algorithm == "sha512":
                return hashlib.sha512(content_bytes).hexdigest()
            else:
                raise DetectionError(f"不支持的哈希算法: {self.hash_algorithm}")
                
        except Exception as e:
            raise DetectionError(f"哈希计算失败: {e}")
    
    def get_hash_info(self, content: str) -> Dict[str, Any]:
        """
        获取内容的哈希信息
        
        Args:
            content: 内容
            
        Returns:
            哈希信息字典
        """
        try:
            content_hash = self._calculate_hash(content)
            
            return {
                "hash": content_hash,
                "hash_algorithm": self.hash_algorithm,
                "content_size": len(content),
                "content_preview": content[:100] + "..." if len(content) > 100 else content
            }
        except Exception as e:
            raise DetectionError(f"获取哈希信息失败: {e}")


class LengthChangeDetector(BaseChangeDetector):
    """长度变化检测器"""
    
    def __init__(self, length_threshold: int = 10, **kwargs):
        """
        初始化长度变化检测器
        
        Args:
            length_threshold: 长度变化阈值（字符数）
            **kwargs: 其他参数
        """
        super().__init__("length", **kwargs)
        self.length_threshold = length_threshold
    
    def detect_changes(self, old_content: str, new_content: str, **kwargs) -> Dict[str, Any]:
        """
        基于内容长度检测变化
        
        Args:
            old_content: 旧内容
            new_content: 新内容
            **kwargs: 其他参数
            
        Returns:
            检测结果字典
        """
        try:
            start_time = time.time()
            
            # 验证内容
            if not self.validate_content(old_content) or not self.validate_content(new_content):
                return {
                    "changed": False,
                    "error": "内容验证失败",
                    "algorithm": self.algorithm_name
                }
            
            # 计算长度
            old_length = len(old_content)
            new_length = len(new_content)
            length_diff = abs(new_length - old_length)
            
            # 检测变化（长度变化超过阈值）
            changed = length_diff > self.length_threshold
            
            # 计算检测时间
            detection_time = time.time() - start_time
            
            result = {
                "changed": changed,
                "old_length": old_length,
                "new_length": new_length,
                "length_diff": length_diff,
                "length_threshold": self.length_threshold,
                "algorithm": self.algorithm_name,
                "detection_time": detection_time
            }
            
            # 如果有变化，添加详细信息
            if changed:
                change_type = "increase" if new_length > old_length else "decrease"
                result.update({
                    "change_type": change_type,
                    "change_summary": f"内容长度{change_type}了 {length_diff} 字符"
                })
            
            return result
            
        except Exception as e:
            raise DetectionError(f"长度检测失败: {e}", algorithm=self.algorithm_name)


class ThresholdChangeDetector(BaseChangeDetector):
    """阈值变化检测器"""
    
    def __init__(self, change_threshold: float = 0.1, **kwargs):
        """
        初始化阈值变化检测器
        
        Args:
            change_threshold: 变化阈值（0.0-1.0）
            **kwargs: 其他参数
        """
        super().__init__("threshold", **kwargs)
        self.change_threshold = change_threshold
        
        # 验证阈值
        if not 0.0 <= change_threshold <= 1.0:
            raise DetectionError(f"无效的变化阈值: {change_threshold}")
    
    def detect_changes(self, old_content: str, new_content: str, **kwargs) -> Dict[str, Any]:
        """
        基于变化比例检测变化
        
        Args:
            old_content: 旧内容
            new_content: 新内容
            **kwargs: 其他参数
            
        Returns:
            检测结果字典
        """
        try:
            start_time = time.time()
            
            # 验证内容
            if not self.validate_content(old_content) or not self.validate_content(new_content):
                return {
                    "changed": False,
                    "error": "内容验证失败",
                    "algorithm": self.algorithm_name
                }
            
            # 计算内容差异
            old_length = len(old_content)
            new_length = len(new_content)
            
            # 使用简单的差异计算（可以替换为更复杂的算法）
            diff_count = 0
            max_length = max(old_length, new_length)
            
            # 计算字符级别的差异
            for i in range(max_length):
                old_char = old_content[i] if i < old_length else ""
                new_char = new_content[i] if i < new_length else ""
                if old_char != new_char:
                    diff_count += 1
            
            # 计算变化比例
            change_ratio = diff_count / max_length if max_length > 0 else 0
            
            # 检测变化（变化比例超过阈值）
            changed = change_ratio > self.change_threshold
            
            # 计算检测时间
            detection_time = time.time() - start_time
            
            result = {
                "changed": changed,
                "change_ratio": change_ratio,
                "change_threshold": self.change_threshold,
                "diff_count": diff_count,
                "old_length": old_length,
                "new_length": new_length,
                "algorithm": self.algorithm_name,
                "detection_time": detection_time
            }
            
            # 如果有变化，添加详细信息
            if changed:
                result.update({
                    "change_summary": f"内容变化比例为 {change_ratio:.2%}，超过阈值 {self.change_threshold:.2%}",
                    "change_type": "content_change"
                })
            
            return result
            
        except Exception as e:
            raise DetectionError(f"阈值检测失败: {e}", algorithm=self.algorithm_name)


class CompositeChangeDetector(BaseChangeDetector):
    """组合变化检测器"""
    
    def __init__(self, detectors: Optional[List[BaseChangeDetector]] = None, **kwargs):
        """
        初始化组合变化检测器
        
        Args:
            detectors: 检测器列表
            **kwargs: 其他参数
        """
        super().__init__("composite", **kwargs)
        self.detectors = detectors or []
        self.voting_threshold = kwargs.get("voting_threshold", 0.5)  # 投票阈值
    
    def add_detector(self, detector: BaseChangeDetector):
        """
        添加检测器
        
        Args:
            detector: 检测器实例
        """
        self.detectors.append(detector)
    
    def detect_changes(self, old_content: str, new_content: str, **kwargs) -> Dict[str, Any]:
        """
        使用多个检测器进行综合检测
        
        Args:
            old_content: 旧内容
            new_content: 新内容
            **kwargs: 其他参数
            
        Returns:
            综合检测结果
        """
        try:
            start_time = time.time()
            
            if not self.detectors:
                return {
                    "changed": False,
                    "error": "没有可用的检测器",
                    "algorithm": self.algorithm_name
                }
            
            # 收集所有检测结果
            results = []
            change_votes = 0
            
            for detector in self.detectors:
                try:
                    result = detector.detect_changes(old_content, new_content, **kwargs)
                    results.append(result)
                    
                    if result.get("changed", False):
                        change_votes += 1
                        
                except Exception as e:
                    # 单个检测器失败不影响整体结果
                    results.append({
                        "error": str(e),
                        "detector": detector.algorithm_name
                    })
            
            # 基于投票结果决定是否变化
            vote_ratio = change_votes / len(self.detectors)
            changed = vote_ratio >= self.voting_threshold
            
            # 计算检测时间
            detection_time = time.time() - start_time
            
            result = {
                "changed": changed,
                "vote_ratio": vote_ratio,
                "voting_threshold": self.voting_threshold,
                "change_votes": change_votes,
                "total_detectors": len(self.detectors),
                "individual_results": results,
                "algorithm": self.algorithm_name,
                "detection_time": detection_time
            }
            
            # 如果有变化，添加详细信息
            if changed:
                result.update({
                    "change_summary": f"{change_votes}/{len(self.detectors)} 个检测器检测到变化",
                    "change_type": "composite_change"
                })
            
            return result
            
        except Exception as e:
            raise DetectionError(f"组合检测失败: {e}", algorithm=self.algorithm_name)