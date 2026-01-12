"""
Hook 模块

提供页面变化事件的自定义脚本触发机制。
"""

from .triggers import HookTrigger
from .config import HookConfig
from .result import HookResult
from .executor import HookExecutor
from .manager import HookManager
from .validator import ScriptValidator, ValidationResult
from .storage import HookResultStorage
from .errors import (
    HookErrorType,
    HookExecutionError,
    ScriptNotFoundError,
    PermissionDeniedError,
    TimeoutError,
    NonZeroExitError,
    ScriptCrashError,
    ResourceLimitError,
)

__all__ = [
    'HookTrigger',
    'HookConfig',
    'HookResult',
    'HookExecutor',
    'HookManager',
    'ScriptValidator',
    'ValidationResult',
    'HookResultStorage',
    'HookErrorType',
    'HookExecutionError',
    'ScriptNotFoundError',
    'PermissionDeniedError',
    'TimeoutError',
    'NonZeroExitError',
    'ScriptCrashError',
    'ResourceLimitError',
]
