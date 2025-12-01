"""
数据模型模块

提供WebMon项目中使用的所有数据模型类。
"""

from .task import Task
from .check_result import CheckResult
from .change_details import ChangeDetails

__all__ = [
    'Task',
    'CheckResult', 
    'ChangeDetails'
]

# 版本信息
__version__ = '1.0.0'