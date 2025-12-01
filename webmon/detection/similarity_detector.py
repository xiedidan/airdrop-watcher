"""
相似度检测算法

提供各种文本相似度检测功能，包括编辑距离、余弦相似度、Jaccard相似度等。
"""
import re
import math
import difflib
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Set, Tuple
from collections import Counter
from datetime import datetime

try:
    import jieba
    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False

from ..exceptions import DetectionError


class BaseSimilarityDetector(ABC):
    """相似度检测算法基类"""
    
    def __init__(self, algorithm_name: str = "base", threshold: float = 0.85, **kwargs):
        """
        初始化相似度检测器
        
        Args:
            algorithm_name: 算法名称
            threshold: 相似度阈值（0.0-1.0）
            **kwargs: 其他参数
        """
        self.algorithm_name = algorithm_name
        self.threshold = threshold
        self.config = kwargs
        self.logger = logging.getLogger(__name__)
        
        # 验证阈值
        if not 0.0 <= threshold <= 1.0:
            raise ValueError(f"相似度阈值必须在0.0-1.0之间: {threshold}")
    
    @abstractmethod
    def calculate_similarity(self, text1: str, text2: str, **kwargs) -> float:
        """
        计算文本相似度
        
        Args:
            text1: 文本1
            text2: 文本2
            **kwargs: 其他参数
            
        Returns:
            相似度分数（0.0-1.0）
        """
        pass
    
    def detect_changes(self, old_text: str, new_text: str, **kwargs) -> Dict[str, Any]:
        """
        基于相似度检测变化
        
        Args:
            old_text: 旧文本
            new_text: 新文本
            **kwargs: 其他参数
            
        Returns:
            检测结果字典
        """
        try:
            start_time = datetime.now()
            
            # 验证输入
            if not old_text or not new_text:
                return {
                    "changed": True,  # 任一文本为空视为变化
                    "similarity": 0.0,
                    "threshold": self.threshold,
                    "old_text_length": len(old_text) if old_text else 0,
                    "new_text_length": len(new_text) if new_text else 0,
                    "algorithm": self.algorithm_name,
                    "error": "输入文本为空"
                }
            
            # 计算相似度
            similarity = self.calculate_similarity(old_text, new_text, **kwargs)
            
            # 基于阈值判断变化
            changed = similarity < self.threshold
            
            # 计算检测时间
            detection_time = (datetime.now() - start_time).total_seconds()
            
            result = {
                "changed": changed,
                "similarity": similarity,
                "threshold": self.threshold,
                "old_text_length": len(old_text),
                "new_text_length": len(new_text),
                "algorithm": self.algorithm_name,
                "detection_time": detection_time
            }
            
            # 如果有变化，添加详细信息
            if changed:
                similarity_percent = round(similarity * 100, 2)
                threshold_percent = round(self.threshold * 100, 2)
                result.update({
                    "change_type": "similarity_change",
                    "change_summary": f"相似度为 {similarity_percent}%，低于阈值 {threshold_percent}%",
                    "similarity_gap": self.threshold - similarity
                })
            
            return result
            
        except Exception as e:
            self.logger.error(f"相似度检测失败: {e}")
            raise DetectionError(f"相似度检测失败: {e}", algorithm=self.algorithm_name)
    
    def preprocess_text(self, text: str) -> str:
        """
        预处理文本
        
        Args:
            text: 原始文本
            
        Returns:
            预处理后的文本
        """
        if not text or not isinstance(text, str):
            return ""
        
        # 转换为小写
        text = text.lower()
        
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text)
        
        # 移除标点符号（保留空格）
        text = re.sub(r'[^\w\s]', '', text)
        
        # 去除首尾空白
        text = text.strip()
        
        return text
    
    def get_similarity_level(self, similarity: float) -> str:
        """
        获取相似度等级描述
        
        Args:
            similarity: 相似度分数
            
        Returns:
            等级描述
        """
        if similarity >= 0.95:
            return "几乎相同"
        elif similarity >= 0.85:
            return "高度相似"
        elif similarity >= 0.70:
            return "中度相似"
        elif similarity >= 0.50:
            return "低度相似"
        else:
            return "差异很大"
    
    def get_algorithm_info(self) -> Dict[str, Any]:
        """
        获取算法信息
        
        Returns:
            算法信息字典
        """
        return {
            "algorithm_name": self.algorithm_name,
            "threshold": self.threshold,
            "config": self.config
        }


class SequenceMatcherDetector(BaseSimilarityDetector):
    """序列匹配相似度检测器（基于difflib）"""
    
    def __init__(self, threshold: float = 0.85, **kwargs):
        """
        初始化序列匹配检测器
        
        Args:
            threshold: 相似度阈值
            **kwargs: 其他参数
        """
        super().__init__("sequence_matcher", threshold, **kwargs)
        self.isjunk = kwargs.get("isjunk", None)  # 垃圾字符判断函数
    
    def calculate_similarity(self, text1: str, text2: str, **kwargs) -> float:
        """
        使用difflib.SequenceMatcher计算相似度
        
        Args:
            text1: 文本1
            text2: 文本2
            **kwargs: 其他参数
            
        Returns:
            相似度分数
        """
        try:
            # 预处理文本
            processed_text1 = self.preprocess_text(text1)
            processed_text2 = self.preprocess_text(text2)
            
            # 计算相似度
            matcher = difflib.SequenceMatcher(self.isjunk, processed_text1, processed_text2)
            similarity = matcher.ratio()
            
            return similarity
            
        except Exception as e:
            self.logger.error(f"序列匹配计算失败: {e}")
            raise DetectionError(f"序列匹配计算失败: {e}", algorithm=self.algorithm_name)


class EditDistanceDetector(BaseSimilarityDetector):
    """编辑距离相似度检测器"""
    
    def __init__(self, threshold: float = 0.85, **kwargs):
        """
        初始化编辑距离检测器
        
        Args:
            threshold: 相似度阈值
            **kwargs: 其他参数
        """
        super().__init__("edit_distance", threshold, **kwargs)
    
    def calculate_similarity(self, text1: str, text2: str, **kwargs) -> float:
        """
        基于编辑距离计算相似度
        
        Args:
            text1: 文本1
            text2: 文本2
            **kwargs: 其他参数
            
        Returns:
            相似度分数
        """
        try:
            # 预处理文本
            processed_text1 = self.preprocess_text(text1)
            processed_text2 = self.preprocess_text(text2)
            
            # 计算编辑距离
            distance = self._levenshtein_distance(processed_text1, processed_text2)
            
            # 计算相似度（基于距离）
            max_length = max(len(processed_text1), len(processed_text2))
            if max_length == 0:
                return 1.0  # 两个空文本完全相似
            
            similarity = 1.0 - (distance / max_length)
            
            return max(0.0, similarity)  # 确保不为负数
            
        except Exception as e:
            self.logger.error(f"编辑距离计算失败: {e}")
            raise DetectionError(f"编辑距离计算失败: {e}", algorithm=self.algorithm_name)
    
    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """
        计算Levenshtein距离
        
        Args:
            s1: 字符串1
            s2: 字符串2
            
        Returns:
            编辑距离
        """
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = list(range(len(s2) + 1))
        
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]


class JaccardSimilarityDetector(BaseSimilarityDetector):
    """Jaccard相似度检测器（基于集合）"""
    
    def __init__(self, threshold: float = 0.85, n_grams: int = 2, **kwargs):
        """
        初始化Jaccard相似度检测器
        
        Args:
            threshold: 相似度阈值
            n_grams: n-gram大小
            **kwargs: 其他参数
        """
        super().__init__("jaccard", threshold, **kwargs)
        self.n_grams = n_grams
    
    def calculate_similarity(self, text1: str, text2: str, **kwargs) -> float:
        """
        使用Jaccard相似度计算相似性
        
        Args:
            text1: 文本1
            text2: 文本2
            **kwargs: 其他参数
            
        Returns:
            相似度分数
        """
        try:
            # 预处理文本
            processed_text1 = self.preprocess_text(text1)
            processed_text2 = self.preprocess_text(text2)
            
            # 生成n-gram集合
            set1 = self._generate_ngrams(processed_text1, self.n_grams)
            set2 = self._generate_ngrams(processed_text2, self.n_grams)
            
            # 计算Jaccard相似度
            intersection = set1.intersection(set2)
            union = set1.union(set2)
            
            if len(union) == 0:
                return 1.0  # 两个空集合完全相似
            
            jaccard_similarity = len(intersection) / len(union)
            
            return jaccard_similarity
            
        except Exception as e:
            self.logger.error(f"Jaccard相似度计算失败: {e}")
            raise DetectionError(f"Jaccard相似度计算失败: {e}", algorithm=self.algorithm_name)
    
    def _generate_ngrams(self, text: str, n: int) -> Set[str]:
        """
        生成n-gram集合
        
        Args:
            text: 文本
            n: n-gram大小
            
        Returns:
            n-gram集合
        """
        words = text.split()
        ngrams = set()
        
        for i in range(len(words) - n + 1):
            ngram = ' '.join(words[i:i + n])
            ngrams.add(ngram)
        
        return ngrams


class CosineSimilarityDetector(BaseSimilarityDetector):
    """余弦相似度检测器（基于TF-IDF）"""
    
    def __init__(self, threshold: float = 0.85, **kwargs):
        """
        初始化余弦相似度检测器
        
        Args:
            threshold: 相似度阈值
            **kwargs: 其他参数
        """
        super().__init__("cosine", threshold, **kwargs)
    
    def calculate_similarity(self, text1: str, text2: str, **kwargs) -> float:
        """
        使用余弦相似度计算相似性
        
        Args:
            text1: 文本1
            text2: 文本2
            **kwargs: 其他参数
            
        Returns:
            相似度分数
        """
        try:
            # 预处理文本
            processed_text1 = self.preprocess_text(text1)
            processed_text2 = self.preprocess_text(text2)
            
            # 分词
            words1 = processed_text1.split()
            words2 = processed_text2.split()
            
            # 计算词频
            vec1 = Counter(words1)
            vec2 = Counter(words2)
            
            # 计算余弦相似度
            intersection = set(vec1.keys()) & set(vec2.keys())
            
            # 计算点积
            dot_product = sum([vec1[word] * vec2[word] for word in intersection])
            
            # 计算向量的模
            magnitude1 = math.sqrt(sum([val ** 2 for val in vec1.values()]))
            magnitude2 = math.sqrt(sum([val ** 2 for val in vec2.values()]))
            
            if magnitude1 == 0 or magnitude2 == 0:
                return 0.0  # 空文本
            
            cosine_similarity = dot_product / (magnitude1 * magnitude2)
            
            return cosine_similarity
            
        except Exception as e:
            self.logger.error(f"余弦相似度计算失败: {e}")
            raise DetectionError(f"余弦相似度计算失败: {e}", algorithm=self.algorithm_name)


class TokenBasedSimilarityDetector(BaseSimilarityDetector):
    """基于分词的相似度检测器（支持中文）"""
    
    def __init__(self, threshold: float = 0.85, language: str = "auto", **kwargs):
        """
        初始化分词相似度检测器
        
        Args:
            threshold: 相似度阈值
            language: 语言（"auto", "chinese", "english"）
            **kwargs: 其他参数
        """
        super().__init__("token_based", threshold, **kwargs)
        self.language = language
    
    def calculate_similarity(self, text1: str, text2: str, **kwargs) -> float:
        """
        基于分词计算相似度
        
        Args:
            text1: 文本1
            text2: 文本2
            **kwargs: 其他参数
            
        Returns:
            相似度分数
        """
        try:
            # 检测语言
            detected_language = self._detect_language(text1 + " " + text2)
            
            # 分词
            tokens1 = self._tokenize(text1, detected_language)
            tokens2 = self._tokenize(text2, detected_language)
            
            # 计算Jaccard相似度
            set1 = set(tokens1)
            set2 = set(tokens2)
            
            intersection = set1.intersection(set2)
            union = set1.union(set2)
            
            if len(union) == 0:
                return 1.0
            
            jaccard_similarity = len(intersection) / len(union)
            
            return jaccard_similarity
            
        except Exception as e:
            self.logger.error(f"分词相似度计算失败: {e}")
            raise DetectionError(f"分词相似度计算失败: {e}", algorithm=self.algorithm_name)
    
    def _detect_language(self, text: str) -> str:
        """
        检测文本语言
        
        Args:
            text: 文本
            
        Returns:
            语言类型
        """
        if self.language != "auto":
            return self.language
        
        # 简单的语言检测：检查中文字符比例
        chinese_chars = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
        total_chars = len(text)
        
        if total_chars == 0:
            return "english"
        
        chinese_ratio = chinese_chars / total_chars
        
        return "chinese" if chinese_ratio > 0.3 else "english"
    
    def _tokenize(self, text: str, language: str) -> List[str]:
        """
        分词
        
        Args:
            text: 文本
            language: 语言
            
        Returns:
            分词结果
        """
        if language == "chinese":
            if JIEBA_AVAILABLE:
                return list(jieba.cut(text))
            else:
                # 备用方案：按字符分割
                return list(text)
        else:
            # 英文：按空格和标点分割
            import re
            return re.findall(r'\b\w+\b', text.lower())


class WeightedSimilarityDetector(BaseSimilarityDetector):
    """加权相似度检测器"""
    
    def __init__(self, threshold: float = 0.85, weights: Optional[Dict[str, float]] = None, **kwargs):
        """
        初始化加权相似度检测器
        
        Args:
            threshold: 相似度阈值
            weights: 各种相似度算法的权重
            **kwargs: 其他参数
        """
        super().__init__("weighted", threshold, **kwargs)
        
        # 默认权重
        self.weights = weights or {
            "sequence_matcher": 0.3,
            "edit_distance": 0.2,
            "jaccard": 0.2,
            "cosine": 0.2,
            "token_based": 0.1
        }
        
        # 创建子检测器
        self.detectors = {
            "sequence_matcher": SequenceMatcherDetector(threshold),
            "edit_distance": EditDistanceDetector(threshold),
            "jaccard": JaccardSimilarityDetector(threshold),
            "cosine": CosineSimilarityDetector(threshold),
            "token_based": TokenBasedSimilarityDetector(threshold)
        }
    
    def calculate_similarity(self, text1: str, text2: str, **kwargs) -> float:
        """
        使用加权方法计算综合相似度
        
        Args:
            text1: 文本1
            text2: 文本2
            **kwargs: 其他参数
            
        Returns:
            综合相似度分数
        """
        try:
            weighted_similarity = 0.0
            total_weight = 0.0
            individual_scores = {}
            
            for algorithm, detector in self.detectors.items():
                if algorithm in self.weights:
                    weight = self.weights[algorithm]
                    
                    try:
                        similarity = detector.calculate_similarity(text1, text2, **kwargs)
                        weighted_similarity += similarity * weight
                        total_weight += weight
                        individual_scores[algorithm] = similarity
                        
                    except Exception as e:
                        self.logger.warning(f"{algorithm} 相似度计算失败: {e}")
                        individual_scores[algorithm] = 0.0
            
            # 计算加权平均
            if total_weight > 0:
                final_similarity = weighted_similarity / total_weight
            else:
                final_similarity = 0.0
            
            # 存储个体分数用于分析
            kwargs["individual_scores"] = individual_scores
            
            return final_similarity
            
        except Exception as e:
            self.logger.error(f"加权相似度计算失败: {e}")
            raise DetectionError(f"加权相似度计算失败: {e}", algorithm=self.algorithm_name)


class AdaptiveSimilarityDetector(BaseSimilarityDetector):
    """自适应相似度检测器"""
    
    def __init__(self, threshold: float = 0.85, **kwargs):
        """
        初始化自适应相似度检测器
        
        Args:
            threshold: 基础相似度阈值
            **kwargs: 其他参数
        """
        super().__init__("adaptive", threshold, **kwargs)
        
        # 子检测器
        self.detectors = {
            "sequence_matcher": SequenceMatcherDetector(threshold),
            "edit_distance": EditDistanceDetector(threshold),
            "jaccard": JaccardSimilarityDetector(threshold, n_grams=2),
            "cosine": CosineSimilarityDetector(threshold)
        }
        
        # 历史统计
        self.history = []
        self.adaptive_threshold = threshold
    
    def calculate_similarity(self, text1: str, text2: str, **kwargs) -> float:
        """
        自适应计算相似度
        
        Args:
            text1: 文本1
            text2: 文本2
            **kwargs: 其他参数
            
        Returns:
            自适应相似度分数
        """
        try:
            # 检测文本特征
            text_features = self._analyze_text_features(text1, text2)
            
            # 根据特征选择合适的算法和权重
            selected_algorithms = self._select_algorithms(text_features)
            
            # 计算加权相似度
            weighted_similarity = 0.0
            total_weight = 0.0
            individual_scores = {}
            
            for algorithm, weight in selected_algorithms.items():
                if algorithm in self.detectors:
                    try:
                        similarity = self.detectors[algorithm].calculate_similarity(text1, text2, **kwargs)
                        weighted_similarity += similarity * weight
                        total_weight += weight
                        individual_scores[algorithm] = similarity
                        
                    except Exception as e:
                        self.logger.warning(f"{algorithm} 相似度计算失败: {e}")
                        individual_scores[algorithm] = 0.0
            
            # 计算最终相似度
            if total_weight > 0:
                final_similarity = weighted_similarity / total_weight
            else:
                final_similarity = 0.0
            
            # 更新历史记录
            self._update_history(text_features, final_similarity, individual_scores)
            
            # 自适应调整阈值
            self._adapt_threshold()
            
            kwargs["text_features"] = text_features
            kwargs["individual_scores"] = individual_scores
            kwargs["adaptive_threshold"] = self.adaptive_threshold
            
            return final_similarity
            
        except Exception as e:
            self.logger.error(f"自适应相似度计算失败: {e}")
            raise DetectionError(f"自适应相似度计算失败: {e}", algorithm=self.algorithm_name)
    
    def _analyze_text_features(self, text1: str, text2: str) -> Dict[str, Any]:
        """
        分析文本特征
        
        Args:
            text1: 文本1
            text2: 文本2
            
        Returns:
            文本特征字典
        """
        features = {}
        
        # 基本统计特征
        features["length1"] = len(text1)
        features["length2"] = len(text2)
        features["length_ratio"] = min(len(text1), len(text2)) / max(len(text1), len(text2)) if max(len(text1), len(text2)) > 0 else 1.0
        
        # 语言特征
        chinese_chars1 = sum(1 for char in text1 if '\u4e00' <= char <= '\u9fff')
        chinese_chars2 = sum(1 for char in text2 if '\u4e00' <= char <= '\u9fff')
        
        features["chinese_ratio1"] = chinese_chars1 / len(text1) if len(text1) > 0 else 0
        features["chinese_ratio2"] = chinese_chars2 / len(text2) if len(text2) > 0 else 0
        
        # 结构特征
        features["has_html"] = '<' in text1 or '<' in text2
        features["has_special_chars"] = any(ord(char) > 127 for char in text1 + text2)
        
        # 复杂度特征
        features["avg_word_length1"] = len(text1) / max(len(text1.split()), 1)
        features["avg_word_length2"] = len(text2) / max(len(text2.split()), 1)
        
        return features
    
    def _select_algorithms(self, text_features: Dict[str, Any]) -> Dict[str, float]:
        """
        根据文本特征选择算法和权重
        
        Args:
            text_features: 文本特征
            
        Returns:
            算法权重字典
        """
        weights = {}
        
        # 基于语言特征选择
        if text_features["chinese_ratio1"] > 0.3 or text_features["chinese_ratio2"] > 0.3:
            # 中文文本：重视字符级和分词相似度
            weights["sequence_matcher"] = 0.4
            weights["jaccard"] = 0.3
            weights["cosine"] = 0.2
            weights["edit_distance"] = 0.1
        else:
            # 英文文本：重视单词级相似度
            weights["cosine"] = 0.4
            weights["jaccard"] = 0.3
            weights["sequence_matcher"] = 0.2
            weights["edit_distance"] = 0.1
        
        # 基于长度特征调整
        if text_features["length_ratio"] < 0.5:
            # 长度差异较大：重视编辑距离
            weights["edit_distance"] += 0.2
            weights["sequence_matcher"] -= 0.1
        
        # 基于复杂度特征调整
        if text_features["has_html"]:
            # HTML内容：重视结构相似度
            weights["sequence_matcher"] += 0.1
        
        return weights
    
    def _update_history(self, text_features: Dict[str, Any], final_similarity: float, 
                       individual_scores: Dict[str, float]):
        """
        更新历史记录
        
        Args:
            text_features: 文本特征
            final_similarity: 最终相似度
            individual_scores: 个体算法分数
        """
        self.history.append({
            "timestamp": datetime.now(),
            "text_features": text_features,
            "final_similarity": final_similarity,
            "individual_scores": individual_scores
        })
        
        # 保持历史记录在合理大小内
        if len(self.history) > 1000:
            self.history = self.history[-500:]  # 保留最近500条
    
    def _adapt_threshold(self):
        """
        自适应调整阈值
        """
        if len(self.history) < 10:
            return  # 历史数据不足，不调整
        
        # 计算近期相似度的统计特征
        recent_similarities = [record["final_similarity"] for record in self.history[-50:]]
        
        if not recent_similarities:
            return
        
        avg_similarity = sum(recent_similarities) / len(recent_similarities)
        std_similarity = self._calculate_std(recent_similarities)
        
        # 基于统计特征调整阈值
        if avg_similarity > 0.9 and std_similarity < 0.1:
            # 高相似度且变化小：提高阈值，减少误报
            self.adaptive_threshold = min(self.adaptive_threshold + 0.02, 0.95)
        elif avg_similarity < 0.7 and std_similarity > 0.2:
            # 低相似度且变化大：降低阈值，提高敏感度
            self.adaptive_threshold = max(self.adaptive_threshold - 0.02, 0.5)
        
        self.logger.debug(f"自适应阈值调整为: {self.adaptive_threshold:.3f}")
    
    def _calculate_std(self, values: List[float]) -> float:
        """
        计算标准差
        
        Args:
            values: 数值列表
            
        Returns:
            标准差
        """
        if len(values) <= 1:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return math.sqrt(variance)
    
    def get_adaptive_info(self) -> Dict[str, Any]:
        """
        获取自适应信息
        
        Returns:
            自适应信息字典
        """
        return {
            "base_threshold": self.threshold,
            "adaptive_threshold": self.adaptive_threshold,
            "history_size": len(self.history),
            "algorithms_available": list(self.detectors.keys())
        }