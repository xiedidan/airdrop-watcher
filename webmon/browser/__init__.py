"""
浏览器引擎模块

提供基于Playwright的浏览器自动化功能，支持网页内容获取、JavaScript渲染、反检测等特性。
"""

from .browser_engine import BrowserEngine, BrowserPool
from .resource_manager import ResourceManager, ResourcePool, BrowserResource
from .performance_optimizer import PerformanceOptimizer, MemoryManager, ContentCache, ResourceBlocker

__all__ = [
    'BrowserEngine',
    'BrowserPool',
    'ResourceManager',
    'ResourcePool',
    'BrowserResource',
    'PerformanceOptimizer',
    'MemoryManager',
    'ContentCache',
    'ResourceBlocker'
]

# 版本信息
__version__ = '1.0.0'