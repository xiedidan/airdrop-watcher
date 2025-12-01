"""
变化检测模块

提供各种变化检测算法和内容提取功能。
"""

# 基础检测器
from .base_detector import (
    BaseChangeDetector,
    HashChangeDetector,
    LengthChangeDetector,
    ThresholdChangeDetector,
    CompositeChangeDetector
)

# 内容提取器
from .content_extractor import (
    BaseContentExtractor,
    TextContentExtractor,
    StructuredDataExtractor,
    LinkExtractor,
    ImageExtractor,
    MetaDataExtractor,
    CompositeExtractor
)

# 相似度检测器
from .similarity_detector import (
    BaseSimilarityDetector,
    SequenceMatcherDetector,
    EditDistanceDetector,
    JaccardSimilarityDetector,
    CosineSimilarityDetector,
    TokenBasedSimilarityDetector,
    WeightedSimilarityDetector,
    AdaptiveSimilarityDetector
)

# 结构化检测器
from .structured_detector import (
    BaseStructuredDetector,
    FieldLevelDetector,
    ValueChangeDetector,
    SchemaBasedDetector,
    CompositeStructuredDetector
)

# 综合变化检测器
from .change_detector import ChangeDetector

__all__ = [
    # 基础检测器
    'BaseChangeDetector',
    'HashChangeDetector',
    'LengthChangeDetector',
    'ThresholdChangeDetector',
    'CompositeChangeDetector',
    
    # 内容提取器
    'BaseContentExtractor',
    'TextContentExtractor',
    'StructuredDataExtractor',
    'LinkExtractor',
    'ImageExtractor',
    'MetaDataExtractor',
    'CompositeExtractor',
    
    # 相似度检测器
    'BaseSimilarityDetector',
    'SequenceMatcherDetector',
    'EditDistanceDetector',
    'JaccardSimilarityDetector',
    'CosineSimilarityDetector',
    'TokenBasedSimilarityDetector',
    'WeightedSimilarityDetector',
    'AdaptiveSimilarityDetector',
    
    # 结构化检测器
    'BaseStructuredDetector',
    'FieldLevelDetector',
    'ValueChangeDetector',
    'SchemaBasedDetector',
    'CompositeStructuredDetector',
    
    # 综合变化检测器
    'ChangeDetector'
]

# 版本信息
__version__ = '1.0.0'