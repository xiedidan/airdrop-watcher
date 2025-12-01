"""
综合变化检测器

整合所有变化检测算法，提供统一的变化检测接口。
"""
import time
import logging
from typing import Dict, Any, Optional, List, Union
from datetime import datetime

from .base_detector import HashChangeDetector, LengthChangeDetector, ThresholdChangeDetector, CompositeChangeDetector
from .content_extractor import TextContentExtractor, StructuredDataExtractor, CompositeExtractor
from .similarity_detector import SequenceMatcherDetector, EditDistanceDetector, JaccardSimilarityDetector, \
                               CosineSimilarityDetector, TokenBasedSimilarityDetector, WeightedSimilarityDetector, \
                               AdaptiveSimilarityDetector
from .structured_detector import FieldLevelDetector, ValueChangeDetector, SchemaBasedDetector, CompositeStructuredDetector
from ..config.config_manager import ConfigManager
from ..exceptions import DetectionError


class ChangeDetector:
    """综合变化检测器"""
    
    def __init__(self, config_manager: ConfigManager):
        """
        初始化变化检测器
        
        Args:
            config_manager: 配置管理器
        """
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)
        
        # 获取检测配置
        self.detection_config = config_manager.get_detection_config()
        
        # 基础配置
        self.similarity_threshold = self.detection_config.get("similarity_threshold", 0.85)
        self.enable_smart_detection = self.detection_config.get("enable_smart_detection", True)
        self.min_change_length = self.detection_config.get("min_change_length", 10)
        
        # 初始化各种检测器
        self._initialize_detectors()
        
        # 历史记录（用于缓存和优化）
        self.history_cache = {}
        self.max_cache_size = 1000
    
    def _initialize_detectors(self):
        """初始化各种检测器"""
        try:
            # 基础检测器
            self.hash_detector = HashChangeDetector(hash_algorithm="md5")
            self.length_detector = LengthChangeDetector(length_threshold=self.min_change_length)
            self.threshold_detector = ThresholdChangeDetector(change_threshold=0.1)
            
            # 相似度检测器
            self.sequence_matcher = SequenceMatcherDetector(threshold=self.similarity_threshold)
            self.edit_distance_detector = EditDistanceDetector(threshold=self.similarity_threshold)
            self.jaccard_detector = JaccardSimilarityDetector(threshold=self.similarity_threshold, n_grams=2)
            self.cosine_detector = CosineSimilarityDetector(threshold=self.similarity_threshold)
            self.token_based_detector = TokenBasedSimilarityDetector(threshold=self.similarity_threshold)
            
            # 加权相似度检测器
            self.weighted_detector = WeightedSimilarityDetector(threshold=self.similarity_threshold)
            
            # 自适应相似度检测器
            self.adaptive_detector = AdaptiveSimilarityDetector(threshold=self.similarity_threshold)
            
            # 内容提取器
            self.text_extractor = TextContentExtractor(max_length=5000)
            self.structured_extractor = StructuredDataExtractor()
            self.composite_extractor = CompositeExtractor([
                self.text_extractor,
                self.structured_extractor
            ])
            
            # 结构化检测器
            self.field_detector = FieldLevelDetector()
            self.value_detector = ValueChangeDetector()
            self.composite_structured_detector = CompositeStructuredDetector([
                self.field_detector,
                self.value_detector
            ])
            
            # 组合基础检测器
            self.composite_basic_detector = CompositeChangeDetector([
                self.hash_detector,
                self.length_detector,
                self.threshold_detector
            ])
            
            # 组合相似度检测器
            self.composite_similarity_detector = CompositeChangeDetector([
                self.sequence_matcher,
                self.edit_distance_detector,
                self.jaccard_detector,
                self.cosine_detector,
                self.token_based_detector
            ])
            
            self.logger.info("变化检测器初始化完成")
            
        except Exception as e:
            self.logger.error(f"初始化检测器失败: {e}")
            raise DetectionError(f"初始化检测器失败: {e}")
    
    async def detect_changes(self, task_id: str, url: str, old_content: str, new_content: str, 
                           selectors: Optional[List[str]] = None, 
                           algorithm: str = "auto") -> Dict[str, Any]:
        """
        检测内容变化
        
        Args:
            task_id: 任务ID
            url: URL
            old_content: 旧内容
            new_content: 新内容
            selectors: CSS选择器列表（可选）
            algorithm: 使用的算法（"auto", "hash", "similarity", "structured", "composite"）
            
        Returns:
            检测结果字典
            
        Raises:
            DetectionError: 检测失败
        """
        try:
            start_time = datetime.now()
            self.logger.info(f"开始检测变化 - 任务: {task_id}, URL: {url}, 算法: {algorithm}")
            
            # 验证输入
            if not old_content or not new_content:
                return {
                    "changed": True,
                    "change_type": "content_missing",
                    "error": "内容为空",
                    "task_id": task_id,
                    "url": url,
                    "algorithm": algorithm,
                    "detection_time": 0.0
                }
            
            # 检查缓存
            cache_key = self._generate_cache_key(task_id, old_content, new_content)
            cached_result = self._get_cached_result(cache_key)
            if cached_result:
                self.logger.debug(f"使用缓存结果 - 任务: {task_id}")
                return cached_result
            
            # 根据算法选择检测方法
            if algorithm == "auto":
                result = await self._auto_detect_changes(old_content, new_content, selectors)
            elif algorithm == "hash":
                result = self._hash_detection(old_content, new_content)
            elif algorithm == "similarity":
                result = self._similarity_detection(old_content, new_content)
            elif algorithm == "structured":
                result = await self._structured_detection(old_content, new_content, selectors)
            elif algorithm == "composite":
                result = await self._composite_detection(old_content, new_content, selectors)
            else:
                raise DetectionError(f"不支持的检测算法: {algorithm}")
            
            # 添加基本信息
            result.update({
                "task_id": task_id,
                "url": url,
                "algorithm": algorithm,
                "detection_time": (datetime.now() - start_time).total_seconds(),
                "timestamp": datetime.now()
            })
            
            # 缓存结果
            self._cache_result(cache_key, result)
            
            self.logger.info(f"变化检测完成 - 任务: {task_id}, 变化: {result.get('changed', False)}, "
                           f"算法: {algorithm}, 耗时: {result.get('detection_time', 0):.3f}秒")
            
            return result
            
        except Exception as e:
            self.logger.error(f"变化检测失败 - 任务: {task_id}, 错误: {e}")
            raise DetectionError(f"变化检测失败: {e}", algorithm=algorithm)
    
    async def _auto_detect_changes(self, old_content: str, new_content: str, 
                                 selectors: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        自动选择最佳检测算法
        
        Args:
            old_content: 旧内容
            new_content: 新内容
            selectors: CSS选择器列表
            
        Returns:
            检测结果
        """
        try:
            # 首先进行快速哈希检测
            hash_result = self._hash_detection(old_content, new_content)
            
            # 如果哈希检测发现变化，进行更详细的检测
            if hash_result["changed"] and self.enable_smart_detection:
                self.logger.debug("哈希检测发现变化，进行详细检测")
                
                # 根据内容长度和类型选择算法
                content_length = len(new_content)
                
                if content_length < 1000:
                    # 短内容：使用相似度检测
                    detailed_result = self._similarity_detection(old_content, new_content)
                elif selectors:
                    # 有选择器：使用结构化检测
                    detailed_result = await self._structured_detection(old_content, new_content, selectors)
                else:
                    # 长内容：使用组合检测
                    detailed_result = await self._composite_detection(old_content, new_content, selectors)
                
                # 合并结果
                hash_result.update(detailed_result)
                hash_result["algorithm"] = "auto"
                hash_result["auto_reason"] = "hash_changed_with_smart_detection"
            
            return hash_result
            
        except Exception as e:
            self.logger.error(f"自动检测失败: {e}")
            # 回退到基础哈希检测
            return self._hash_detection(old_content, new_content)
    
    def _hash_detection(self, old_content: str, new_content: str) -> Dict[str, Any]:
        """
        哈希检测
        
        Args:
            old_content: 旧内容
            new_content: 新内容
            
        Returns:
            检测结果
        """
        try:
            return self.hash_detector.detect_changes(old_content, new_content)
        except Exception as e:
            self.logger.error(f"哈希检测失败: {e}")
            raise
    
    def _similarity_detection(self, old_content: str, new_content: str) -> Dict[str, Any]:
        """
        相似度检测
        
        Args:
            old_content: 旧内容
            new_content: 新内容
            
        Returns:
            检测结果
        """
        try:
            # 提取文本内容进行相似度检测
            old_text_result = self.text_extractor.extract(old_content)
            new_text_result = self.text_extractor.extract(new_content)
            
            old_text = old_text_result.get("extracted_text", "")
            new_text = new_text_result.get("extracted_text", "")
            
            if not old_text or not new_text:
                return {
                    "changed": True,
                    "change_type": "text_extraction_failed",
                    "error": "文本提取失败"
                }
            
            # 使用加权相似度检测器
            similarity_result = self.weighted_detector.detect_changes(old_text, new_text)
            
            # 添加文本提取信息
            similarity_result.update({
                "text_extraction": {
                    "old_text_length": len(old_text),
                    "new_text_length": len(new_text),
                    "old_extraction_success": old_text_result.get("success", False),
                    "new_extraction_success": new_text_result.get("success", False)
                }
            })
            
            return similarity_result
            
        except Exception as e:
            self.logger.error(f"相似度检测失败: {e}")
            raise
    
    async def _structured_detection(self, old_content: str, new_content: str, 
                                  selectors: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        结构化检测
        
        Args:
            old_content: 旧内容
            new_content: 新内容
            selectors: CSS选择器列表
            
        Returns:
            检测结果
        """
        try:
            # 提取结构化数据
            old_structured_result = self.structured_extractor.extract(old_content)
            new_structured_result = self.structured_extractor.extract(new_content)
            
            old_data = old_structured_result.get("extracted_data", {})
            new_data = new_structured_result.get("extracted_data", {})
            
            if not old_data and not new_data:
                return {
                    "changed": False,
                    "change_type": "no_structured_data",
                    "error": "未提取到结构化数据"
                }
            
            # 使用结构化检测器
            structured_result = self.composite_structured_detector.detect_field_changes(old_data, new_data)
            
            # 添加提取信息
            structured_result.update({
                "structured_extraction": {
                    "old_extraction_success": old_structured_result.get("success", False),
                    "new_extraction_success": new_structured_result.get("success", False),
                    "old_fields_extracted": old_structured_result.get("fields_extracted", 0),
                    "new_fields_extracted": new_structured_result.get("fields_extracted", 0)
                }
            })
            
            return structured_result
            
        except Exception as e:
            self.logger.error(f"结构化检测失败: {e}")
            raise
    
    async def _composite_detection(self, old_content: str, new_content: str, 
                                 selectors: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        组合检测
        
        Args:
            old_content: 旧内容
            new_content: 新内容
            selectors: CSS选择器列表
            
        Returns:
            检测结果
        """
        try:
            # 并行执行多种检测
            tasks = [
                self._basic_detection_async(old_content, new_content),
                self._similarity_detection_async(old_content, new_content),
                self._structured_detection_async(old_content, new_content, selectors)
            ]
            
            basic_result, similarity_result, structured_result = await asyncio.gather(*tasks)
            
            # 综合分析结果
            changed = (basic_result.get("changed", False) or 
                      similarity_result.get("changed", False) or 
                      structured_result.get("changed", False))
            
            # 找出最详细的检测结果
            detailed_result = self._select_most_detailed_result([
                basic_result, similarity_result, structured_result
            ])
            
            return {
                "changed": changed,
                "change_type": "composite_change",
                "detailed_result": detailed_result,
                "all_results": {
                    "basic": basic_result,
                    "similarity": similarity_result,
                    "structured": structured_result
                },
                "algorithm": "composite"
            }
            
        except Exception as e:
            self.logger.error(f"组合检测失败: {e}")
            raise
    
    async def _basic_detection_async(self, old_content: str, new_content: str) -> Dict[str, Any]:
        """异步基础检测"""
        return self.composite_basic_detector.detect_changes(old_content, new_content)
    
    async def _similarity_detection_async(self, old_content: str, new_content: str) -> Dict[str, Any]:
        """异步相似度检测"""
        return self._similarity_detection(old_content, new_content)
    
    async def _structured_detection_async(self, old_content: str, new_content: str, 
                                        selectors: Optional[List[str]] = None) -> Dict[str, Any]:
        """异步结构化检测"""
        return await self._structured_detection(old_content, new_content, selectors)
    
    def _select_most_detailed_result(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        选择最详细的检测结果
        
        Args:
            results: 检测结果列表
            
        Returns:
            最详细的结果
        """
        # 按详细程度排序
        def get_detail_level(result: Dict[str, Any]) -> int:
            detail_level = 0
            
            # 检查包含的信息量
            if "field_changes" in result:
                detail_level += 3
            if "detailed_changes" in result:
                detail_level += 2
            if "similarity" in result:
                detail_level += 1
            if "old_hash" in result and "new_hash" in result:
                detail_level += 1
            
            return detail_level
        
        return max(results, key=get_detail_level)
    
    def _generate_cache_key(self, task_id: str, old_content: str, new_content: str) -> str:
        """
        生成缓存键
        
        Args:
            task_id: 任务ID
            old_content: 旧内容
            new_content: 新内容
            
        Returns:
            缓存键
        """
        import hashlib
        content_hash = hashlib.md5(f"{task_id}:{old_content}:{new_content}".encode()).hexdigest()
        return f"change_detection:{content_hash}"
    
    def _get_cached_result(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """
        获取缓存结果
        
        Args:
            cache_key: 缓存键
            
        Returns:
            缓存的结果
        """
        return self.history_cache.get(cache_key)
    
    def _cache_result(self, cache_key: str, result: Dict[str, Any]):
        """
        缓存结果
        
        Args:
            cache_key: 缓存键
            result: 结果
        """
        # 控制缓存大小
        if len(self.history_cache) >= self.max_cache_size:
            # 移除最旧的条目（简单实现）
            oldest_key = next(iter(self.history_cache))
            del self.history_cache[oldest_key]
        
        self.history_cache[cache_key] = result
    
    def extract_content_for_comparison(self, html_content: str, selectors: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        提取用于比较的内容
        
        Args:
            html_content: HTML内容
            selectors: CSS选择器列表
            
        Returns:
            提取的内容
        """
        try:
            if selectors:
                # 使用结构化提取
                return self.structured_extractor.extract(html_content, selectors=selectors)
            else:
                # 使用复合提取
                return self.composite_extractor.extract(html_content)
        except Exception as e:
            self.logger.error(f"内容提取失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "extracted_data": {}
            }
    
    def get_supported_algorithms(self) -> List[str]:
        """
        获取支持的算法列表
        
        Returns:
            算法列表
        """
        return [
            "auto", "hash", "similarity", "structured", "composite",
            "sequence_matcher", "edit_distance", "jaccard", "cosine", "token_based",
            "weighted", "adaptive"
        ]
    
    def get_algorithm_info(self, algorithm: str) -> Dict[str, Any]:
        """
        获取算法信息
        
        Args:
            algorithm: 算法名称
            
        Returns:
            算法信息
        """
        if algorithm == "hash":
            return self.hash_detector.get_algorithm_info()
        elif algorithm == "similarity":
            return self.weighted_detector.get_algorithm_info()
        elif algorithm == "structured":
            return self.composite_structured_detector.get_algorithm_info()
        elif algorithm == "adaptive":
            return self.adaptive_detector.get_adaptive_info()
        else:
            return {"algorithm": algorithm, "info": "基本信息不可用"}
    
    def clear_cache(self):
        """清空缓存"""
        self.history_cache.clear()
        self.logger.info("变化检测缓存已清空")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        获取缓存统计
        
        Returns:
            缓存统计信息
        """
        return {
            "cache_size": len(self.history_cache),
            "max_cache_size": self.max_cache_size,
            "cache_utilization": len(self.history_cache) / self.max_cache_size
        }


# 为了支持异步操作，添加必要的导入
import asyncio