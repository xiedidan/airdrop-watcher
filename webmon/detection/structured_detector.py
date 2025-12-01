"""
结构化数据检测

提供结构化数据的变化检测功能，支持字段级别的变化检测。
"""
import json
import logging
from typing import Dict, Any, Optional, List, Set
from abc import ABC, abstractmethod
from datetime import datetime
from collections import defaultdict

from ..exceptions import DetectionError


class BaseStructuredDetector(ABC):
    """结构化数据检测基类"""
    
    def __init__(self, detector_name: str = "structured", **kwargs):
        """
        初始化结构化数据检测器
        
        Args:
            detector_name: 检测器名称
            **kwargs: 其他参数
        """
        self.detector_name = detector_name
        self.config = kwargs
        self.logger = logging.getLogger(__name__)
    
    @abstractmethod
    def detect_field_changes(self, old_data: Dict[str, Any], new_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        检测字段级别的变化
        
        Args:
            old_data: 旧数据
            new_data: 新数据
            **kwargs: 其他参数
            
        Returns:
            变化检测结果
        """
        pass
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """
        验证数据有效性
        
        Args:
            data: 要验证的数据
            
        Returns:
            是否有效
        """
        if not isinstance(data, dict):
            return False
        
        # 检查是否有足够的字段
        if len(data) < 1:
            return False
        
        # 检查字段值类型
        for key, value in data.items():
            if not isinstance(key, str):
                return False
            
            # 值可以是基本类型或列表
            if not isinstance(value, (str, int, float, bool, list)):
                return False
        
        return True
    
    def get_field_info(self, field_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取字段信息
        
        Args:
            field_data: 字段数据
            
        Returns:
            字段信息
        """
        info = {
            "field_count": len(field_data),
            "field_names": list(field_data.keys()),
            "field_types": {}
        }
        
        for key, value in field_data.items():
            info["field_types"][key] = type(value).__name__
        
        return info


class FieldLevelDetector(BaseStructuredDetector):
    """字段级别变化检测器"""
    
    def __init__(self, ignore_fields: Optional[List[str]] = None, 
                 sensitive_fields: Optional[List[str]] = None, **kwargs):
        """
        初始化字段级别检测器
        
        Args:
            ignore_fields: 要忽略的字段列表
            sensitive_fields: 敏感字段列表（变化时需要特殊处理）
            **kwargs: 其他参数
        """
        super().__init__("field_level", **kwargs)
        self.ignore_fields = set(ignore_fields or [])
        self.sensitive_fields = set(sensitive_fields or [])
    
    def detect_field_changes(self, old_data: Dict[str, Any], new_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        检测字段级别的变化
        
        Args:
            old_data: 旧数据
            new_data: 新数据
            **kwargs: 其他参数
            
        Returns:
            变化检测结果
        """
        try:
            # 验证数据
            if not self.validate_data(old_data) or not self.validate_data(new_data):
                return {
                    "changed": False,
                    "error": "数据验证失败",
                    "field_changes": {},
                    "added_fields": [],
                    "removed_fields": [],
                    "modified_fields": [],
                    "detector": self.detector_name
                }
            
            # 获取所有字段
            all_fields = set(old_data.keys()) | set(new_data.keys())
            
            # 过滤忽略的字段
            all_fields = all_fields - self.ignore_fields
            
            field_changes = {}
            added_fields = []
            removed_fields = []
            modified_fields = []
            
            # 检测每个字段的变化
            for field in all_fields:
                old_value = old_data.get(field)
                new_value = new_data.get(field)
                
                # 检测字段变化类型
                if field not in old_data:
                    # 新增字段
                    added_fields.append(field)
                    field_changes[field] = {
                        "type": "added",
                        "new_value": new_value,
                        "is_sensitive": field in self.sensitive_fields
                    }
                elif field not in new_data:
                    # 删除字段
                    removed_fields.append(field)
                    field_changes[field] = {
                        "type": "removed",
                        "old_value": old_value,
                        "is_sensitive": field in self.sensitive_fields
                    }
                elif old_value != new_value:
                    # 修改字段
                    modified_fields.append(field)
                    field_changes[field] = {
                        "type": "modified",
                        "old_value": old_value,
                        "new_value": new_value,
                        "is_sensitive": field in self.sensitive_fields
                    }
            
            # 判断是否有变化
            changed = len(field_changes) > 0
            
            result = {
                "changed": changed,
                "field_changes": field_changes,
                "added_fields": added_fields,
                "removed_fields": removed_fields,
                "modified_fields": modified_fields,
                "total_fields": len(all_fields),
                "changed_fields_count": len(field_changes),
                "detector": self.detector_name,
                "timestamp": datetime.now()
            }
            
            # 如果有变化，添加详细信息
            if changed:
                result.update({
                    "change_summary": self._generate_change_summary(field_changes),
                    "sensitive_changes": self._get_sensitive_changes(field_changes),
                    "change_impact": self._calculate_change_impact(field_changes, len(all_fields))
                })
            
            return result
            
        except Exception as e:
            self.logger.error(f"字段级别变化检测失败: {e}")
            raise DetectionError(f"字段级别变化检测失败: {e}", detector=self.detector_name)
    
    def _generate_change_summary(self, field_changes: Dict[str, Any]) -> str:
        """
        生成变化总结
        
        Args:
            field_changes: 字段变化信息
            
        Returns:
            变化总结
        """
        change_counts = defaultdict(int)
        for field, change in field_changes.items():
            change_type = change["type"]
            change_counts[change_type] += 1
        
        summary_parts = []
        
        if change_counts["added"] > 0:
            summary_parts.append(f"新增 {change_counts['added']} 个字段")
        
        if change_counts["removed"] > 0:
            summary_parts.append(f"删除 {change_counts['removed']} 个字段")
        
        if change_counts["modified"] > 0:
            summary_parts.append(f"修改 {change_counts['modified']} 个字段")
        
        return "；".join(summary_parts) if summary_parts else "无显著变化"
    
    def _get_sensitive_changes(self, field_changes: Dict[str, Any]) -> List[str]:
        """
        获取敏感字段变化
        
        Args:
            field_changes: 字段变化信息
            
        Returns:
            敏感字段变化列表
        """
        sensitive_changes = []
        
        for field, change in field_changes.items():
            if change.get("is_sensitive", False):
                sensitive_changes.append(field)
        
        return sensitive_changes
    
    def _calculate_change_impact(self, field_changes: Dict[str, Any], total_fields: int) -> str:
        """
        计算变化影响
        
        Args:
            field_changes: 字段变化信息
            total_fields: 总字段数
            
        Returns:
            变化影响描述
        """
        change_ratio = len(field_changes) / total_fields if total_fields > 0 else 0
        
        if change_ratio >= 0.5:
            return "高影响（大部分字段发生变化）"
        elif change_ratio >= 0.2:
            return "中等影响（部分字段发生变化）"
        elif change_ratio >= 0.05:
            return "低影响（少量字段发生变化）"
        else:
            return "轻微影响（极少量字段发生变化）"


class ValueChangeDetector(BaseStructuredDetector):
    """值变化检测器"""
    
    def __init__(self, numeric_threshold: float = 0.01, text_similarity_threshold: float = 0.9, **kwargs):
        """
        初始化值变化检测器
        
        Args:
            numeric_threshold: 数值变化阈值（相对变化）
            text_similarity_threshold: 文本相似度阈值
            **kwargs: 其他参数
        """
        super().__init__("value_change", **kwargs)
        self.numeric_threshold = numeric_threshold
        self.text_similarity_threshold = text_similarity_threshold
    
    def detect_field_changes(self, old_data: Dict[str, Any], new_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        检测值级别的变化
        
        Args:
            old_data: 旧数据
            new_data: 新数据
            **kwargs: 其他参数
            
        Returns:
            变化检测结果
        """
        try:
            # 使用字段级别检测器获取基础变化
            field_detector = FieldLevelDetector()
            base_result = field_detector.detect_field_changes(old_data, new_data)
            
            # 对修改的字段进行详细的值变化分析
            detailed_changes = {}
            
            for field in base_result["modified_fields"]:
                old_value = old_data[field]
                new_value = new_data[field]
                
                detailed_change = self._analyze_value_change(old_value, new_value)
                detailed_changes[field] = detailed_change
            
            # 更新结果
            base_result["detailed_changes"] = detailed_changes
            
            return base_result
            
        except Exception as e:
            self.logger.error(f"值变化检测失败: {e}")
            raise DetectionError(f"值变化检测失败: {e}", detector=self.detector_name)
    
    def _analyze_value_change(self, old_value: Any, new_value: Any) -> Dict[str, Any]:
        """
        分析值变化
        
        Args:
            old_value: 旧值
            new_value: 新值
            
        Returns:
            详细的变化分析
        """
        analysis = {
            "old_value": old_value,
            "new_value": new_value,
            "value_type": type(old_value).__name__,
            "change_type": "unknown"
        }
        
        # 数值类型分析
        if isinstance(old_value, (int, float)) and isinstance(new_value, (int, float)):
            if old_value != 0:
                relative_change = abs(new_value - old_value) / abs(old_value)
                absolute_change = abs(new_value - old_value)
                
                analysis.update({
                    "change_type": "numeric_change",
                    "relative_change": relative_change,
                    "absolute_change": absolute_change,
                    "change_direction": "increase" if new_value > old_value else "decrease",
                    "is_significant": relative_change > self.numeric_threshold
                })
        
        # 字符串类型分析
        elif isinstance(old_value, str) and isinstance(new_value, str):
            # 使用简单的相似度计算
            if len(old_value) > 0 and len(new_value) > 0:
                similarity = self._calculate_text_similarity(old_value, new_value)
                
                analysis.update({
                    "change_type": "text_change",
                    "similarity": similarity,
                    "length_change": len(new_value) - len(old_value),
                    "is_similar": similarity > self.text_similarity_threshold,
                    "is_major_change": similarity < 0.7
                })
            else:
                analysis["change_type"] = "text_change"
                analysis["is_empty_change"] = True
        
        # 列表类型分析
        elif isinstance(old_value, list) and isinstance(new_value, list):
            old_set = set(old_value)
            new_set = set(new_value)
            
            added_items = list(new_set - old_set)
            removed_items = list(old_set - new_set)
            common_items = list(old_set & new_set)
            
            analysis.update({
                "change_type": "list_change",
                "added_items": added_items,
                "removed_items": removed_items,
                "common_items": common_items,
                "length_change": len(new_value) - len(old_value),
                "added_count": len(added_items),
                "removed_count": len(removed_items),
                "is_item_change": len(added_items) > 0 or len(removed_items) > 0
            })
        
        # 布尔类型分析
        elif isinstance(old_value, bool) and isinstance(new_value, bool):
            analysis.update({
                "change_type": "boolean_change",
                "value_flipped": old_value != new_value
            })
        
        # 类型变化
        elif type(old_value) != type(new_value):
            analysis.update({
                "change_type": "type_change",
                "old_type": type(old_value).__name__,
                "new_type": type(new_value).__name__
            })
        
        return analysis
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """
        计算文本相似度（简化版）
        
        Args:
            text1: 文本1
            text2: 文本2
            
        Returns:
            相似度分数
        """
        try:
            if not text1 or not text2:
                return 0.0
            
            # 使用字符级相似度
            matches = 0
            total = max(len(text1), len(text2))
            
            for i in range(min(len(text1), len(text2))):
                if text1[i] == text2[i]:
                    matches += 1
            
            return matches / total if total > 0 else 0.0
            
        except Exception:
            return 0.0


class SchemaBasedDetector(BaseStructuredDetector):
    """基于模式的检测器"""
    
    def __init__(self, schema: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化模式检测器
        
        Args:
            schema: 数据模式定义
            **kwargs: 其他参数
        """
        super().__init__("schema_based", **kwargs)
        self.schema = schema or {}
    
    def set_schema(self, schema: Dict[str, Any]):
        """
        设置数据模式
        
        Args:
            schema: 模式定义
        """
        self.schema = schema
    
    def detect_field_changes(self, old_data: Dict[str, Any], new_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        基于模式检测变化
        
        Args:
            old_data: 旧数据
            new_data: 新数据
            **kwargs: 其他参数
            
        Returns:
            变化检测结果
        """
        try:
            # 验证数据与模式的兼容性
            old_validation = self._validate_against_schema(old_data)
            new_validation = self._validate_against_schema(new_data)
            
            # 使用字段级别检测器获取基础变化
            field_detector = FieldLevelDetector()
            base_result = field_detector.detect_field_changes(old_data, new_data)
            
            # 添加模式验证结果
            base_result["schema_validation"] = {
                "old_data_valid": old_validation["valid"],
                "new_data_valid": new_validation["valid"],
                "old_data_errors": old_validation["errors"],
                "new_data_errors": new_validation["errors"]
            }
            
            # 基于模式进行额外检查
            if self.schema:
                schema_changes = self._detect_schema_violations(old_data, new_data)
                base_result["schema_changes"] = schema_changes
            
            return base_result
            
        except Exception as e:
            self.logger.error(f"模式检测失败: {e}")
            raise DetectionError(f"模式检测失败: {e}", detector=self.detector_name)
    
    def _validate_against_schema(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证数据是否符合模式
        
        Args:
            data: 要验证的数据
            
        Returns:
            验证结果
        """
        if not self.schema:
            return {"valid": True, "errors": []}
        
        errors = []
        
        # 检查必需字段
        required_fields = self.schema.get("required", [])
        for field in required_fields:
            if field not in data:
                errors.append(f"缺少必需字段: {field}")
        
        # 检查字段类型
        field_types = self.schema.get("field_types", {})
        for field, expected_type in field_types.items():
            if field in data:
                actual_type = type(data[field]).__name__
                if actual_type != expected_type:
                    errors.append(f"字段 {field} 类型不匹配: 期望 {expected_type}, 实际 {actual_type}")
        
        # 检查字段约束
        field_constraints = self.schema.get("field_constraints", {})
        for field, constraints in field_constraints.items():
            if field in data:
                value = data[field]
                
                # 最小长度约束
                if "min_length" in constraints and isinstance(value, str):
                    if len(value) < constraints["min_length"]:
                        errors.append(f"字段 {field} 长度小于最小值: {len(value)} < {constraints['min_length']}")
                
                # 最大长度约束
                if "max_length" in constraints and isinstance(value, str):
                    if len(value) > constraints["max_length"]:
                        errors.append(f"字段 {field} 长度大于最大值: {len(value)} > {constraints['max_length']}")
                
                # 数值范围约束
                if "min_value" in constraints and isinstance(value, (int, float)):
                    if value < constraints["min_value"]:
                        errors.append(f"字段 {field} 小于最小值: {value} < {constraints['min_value']}")
                
                if "max_value" in constraints and isinstance(value, (int, float)):
                    if value > constraints["max_value"]:
                        errors.append(f"字段 {field} 大于最大值: {value} > {constraints['max_value']}")
                
                # 枚举约束
                if "enum" in constraints:
                    if value not in constraints["enum"]:
                        errors.append(f"字段 {field} 值不在允许范围内: {value}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def _detect_schema_violations(self, old_data: Dict[str, Any], new_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        检测模式违规变化
        
        Args:
            old_data: 旧数据
            new_data: 新数据
            
        Returns:
            模式违规信息
        """
        violations = {
            "new_violations": [],
            "resolved_violations": [],
            "persistent_violations": []
        }
        
        # 验证新旧数据
        old_validation = self._validate_against_schema(old_data)
        new_validation = self._validate_against_schema(new_data)
        
        # 检测新的违规
        for error in new_validation["errors"]:
            if error not in old_validation["errors"]:
                violations["new_violations"].append(error)
        
        # 检测已解决的违规
        for error in old_validation["errors"]:
            if error not in new_validation["errors"]:
                violations["resolved_violations"].append(error)
        
        # 检测持续的违规
        for error in new_validation["errors"]:
            if error in old_validation["errors"]:
                violations["persistent_violations"].append(error)
        
        return violations


class CompositeStructuredDetector(BaseStructuredDetector):
    """组合结构化检测器"""
    
    def __init__(self, detectors: Optional[List[BaseStructuredDetector]] = None, **kwargs):
        """
        初始化组合结构化检测器
        
        Args:
            detectors: 检测器列表
            **kwargs: 其他参数
        """
        super().__init__("composite_structured", **kwargs)
        self.detectors = detectors or []
    
    def add_detector(self, detector: BaseStructuredDetector):
        """
        添加检测器
        
        Args:
            detector: 检测器实例
        """
        self.detectors.append(detector)
    
    def detect_field_changes(self, old_data: Dict[str, Any], new_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        使用多个检测器进行综合检测
        
        Args:
            old_data: 旧数据
            new_data: 新数据
            **kwargs: 其他参数
            
        Returns:
            综合检测结果
        """
        try:
            if not self.detectors:
                return {
                    "changed": False,
                    "error": "没有可用的检测器",
                    "field_changes": {},
                    "detector_results": []
                }
            
            # 收集所有检测结果
            detector_results = []
            change_votes = 0
            
            for detector in self.detectors:
                try:
                    result = detector.detect_field_changes(old_data, new_data, **kwargs)
                    detector_results.append({
                        "detector": detector.detector_name,
                        "result": result,
                        "changed": result.get("changed", False)
                    })
                    
                    if result.get("changed", False):
                        change_votes += 1
                        
                except Exception as e:
                    self.logger.warning(f"检测器 {detector.detector_name} 失败: {e}")
                    detector_results.append({
                        "detector": detector.detector_name,
                        "error": str(e),
                        "changed": False
                    })
            
            # 基于投票结果决定是否变化
            changed = change_votes > 0  # 只要有一个检测器检测到变化就算变化
            
            # 合并字段变化信息
            merged_changes = self._merge_field_changes(detector_results)
            
            result = {
                "changed": changed,
                "field_changes": merged_changes,
                "detector_results": detector_results,
                "change_votes": change_votes,
                "total_detectors": len(self.detectors),
                "detector": self.detector_name
            }
            
            # 如果有变化，添加详细信息
            if changed:
                result.update({
                    "change_summary": f"{change_votes}/{len(self.detectors)} 个检测器检测到变化",
                    "merged_field_changes": len(merged_changes)
                })
            
            return result
            
        except Exception as e:
            self.logger.error(f"组合结构化检测失败: {e}")
            raise DetectionError(f"组合结构化检测失败: {e}", detector=self.detector_name)
    
    def _merge_field_changes(self, detector_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        合并字段变化信息
        
        Args:
            detector_results: 检测器结果列表
            
        Returns:
            合并后的字段变化
        """
        merged_changes = {}
        
        for result_info in detector_results:
            result = result_info["result"]
            field_changes = result.get("field_changes", {})
            
            for field, change in field_changes.items():
                if field not in merged_changes:
                    merged_changes[field] = {
                        "type": change["type"],
                        "detectors": [],
                        "old_value": change.get("old_value"),
                        "new_value": change.get("new_value")
                    }
                
                merged_changes[field]["detectors"].append({
                    "detector": result_info["detector"],
                    "details": change
                })
        
        return merged_changes