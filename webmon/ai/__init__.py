"""
AI分析服务模块

提供基于大语言模型的网页变化内容智能分析功能。
支持DeepSeek R1及OpenAI兼容API。
"""

from webmon.ai.service import AIAnalysisService
from webmon.ai.models import AIConfig, AIAnalysisResult

__all__ = [
    'AIAnalysisService',
    'AIConfig',
    'AIAnalysisResult',
]
