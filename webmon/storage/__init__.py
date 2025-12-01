"""
存储模块

提供WebMon项目中使用的数据存储管理功能。
"""

from .task_storage import TaskStorage
from .history_storage import HistoryStorage

__all__ = [
    'TaskStorage',
    'HistoryStorage'
]

# 版本信息
__version__ = '1.0.0'