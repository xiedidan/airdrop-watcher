"""
WebMon 异常定义

定义项目中使用的所有自定义异常类，便于错误处理和调试。
"""
from typing import Any


class WebMonException(Exception):
    """WebMon基础异常类"""
    
    def __init__(self, message: str = "", error_code: str = None, details: dict = None):
        """
        初始化异常
        
        Args:
            message: 错误消息
            error_code: 错误代码
            details: 详细错误信息
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "UNKNOWN_ERROR"
        self.details = details or {}
    
    def __str__(self):
        """返回错误字符串表示"""
        if self.details:
            return f"[{self.error_code}] {self.message} - Details: {self.details}"
        return f"[{self.error_code}] {self.message}"


class ConfigurationError(WebMonException):
    """配置错误"""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, "CONFIG_ERROR", details)


class NetworkError(WebMonException):
    """网络错误"""
    
    def __init__(self, message: str, url: str = None, status_code: int = None, details: dict = None):
        error_details = details or {}
        if url:
            error_details['url'] = url
        if status_code:
            error_details['status_code'] = status_code
        super().__init__(message, "NETWORK_ERROR", error_details)


class BrowserError(WebMonException):
    """浏览器错误"""
    
    def __init__(self, message: str, url: str = None, browser_error: str = None, details: dict = None):
        error_details = details or {}
        if url:
            error_details['url'] = url
        if browser_error:
            error_details['browser_error'] = browser_error
        super().__init__(message, "BROWSER_ERROR", error_details)


class DetectionError(WebMonException):
    """检测错误"""
    
    def __init__(self, message: str, algorithm: str = None, content_info: dict = None, details: dict = None):
        error_details = details or {}
        if algorithm:
            error_details['algorithm'] = algorithm
        if content_info:
            error_details.update(content_info)
        super().__init__(message, "DETECTION_ERROR", error_details)


class NotificationError(WebMonException):
    """通知错误"""
    
    def __init__(self, message: str, platform: str = None, notification_data: dict = None, details: dict = None):
        error_details = details or {}
        if platform:
            error_details['platform'] = platform
        if notification_data:
            error_details['notification_data'] = notification_data
        super().__init__(message, "NOTIFICATION_ERROR", error_details)


class StorageError(WebMonException):
    """存储错误"""
    
    def __init__(self, message: str, storage_type: str = None, operation: str = None, details: dict = None):
        error_details = details or {}
        if storage_type:
            error_details['storage_type'] = storage_type
        if operation:
            error_details['operation'] = operation
        super().__init__(message, "STORAGE_ERROR", error_details)


class TaskError(WebMonException):
    """任务错误"""
    
    def __init__(self, message: str, task_id: str = None, task_name: str = None, details: dict = None):
        error_details = details or {}
        if task_id:
            error_details['task_id'] = task_id
        if task_name:
            error_details['task_name'] = task_name
        super().__init__(message, "TASK_ERROR", error_details)


class ValidationError(WebMonException):
    """验证错误"""
    
    def __init__(self, message: str, field: str = None, value: Any = None, expected_type: str = None, details: dict = None):
        error_details = details or {}
        if field:
            error_details['field'] = field
        if value is not None:
            error_details['value'] = value
        if expected_type:
            error_details['expected_type'] = expected_type
        super().__init__(message, "VALIDATION_ERROR", error_details)


class RateLimitError(WebMonException):
    """速率限制错误"""
    
    def __init__(self, message: str, limit: int = None, current: int = None, reset_time: float = None, details: dict = None):
        error_details = details or {}
        if limit:
            error_details['limit'] = limit
        if current:
            error_details['current'] = current
        if reset_time:
            error_details['reset_time'] = reset_time
        super().__init__(message, "RATE_LIMIT_ERROR", error_details)


class AuthenticationError(WebMonException):
    """认证错误"""
    
    def __init__(self, message: str, platform: str = None, auth_type: str = None, details: dict = None):
        error_details = details or {}
        if platform:
            error_details['platform'] = platform
        if auth_type:
            error_details['auth_type'] = auth_type
        super().__init__(message, "AUTH_ERROR", error_details)


class ResourceError(WebMonException):
    """资源错误"""
    
    def __init__(self, message: str, resource_type: str = None, resource_id: str = None, details: dict = None):
        error_details = details or {}
        if resource_type:
            error_details['resource_type'] = resource_type
        if resource_id:
            error_details['resource_id'] = resource_id
        super().__init__(message, "RESOURCE_ERROR", error_details)


class ConcurrentError(WebMonException):
    """并发错误"""

    def __init__(self, message: str, max_concurrent: int = None, current: int = None, details: dict = None):
        error_details = details or {}
        if max_concurrent:
            error_details['max_concurrent'] = max_concurrent
        if current:
            error_details['current'] = current
        super().__init__(message, "CONCURRENT_ERROR", error_details)


class AIAnalysisError(WebMonException):
    """AI分析错误基类"""

    def __init__(self, message: str, model: str = None, task_id: str = None, details: dict = None):
        error_details = details or {}
        if model:
            error_details['model'] = model
        if task_id:
            error_details['task_id'] = task_id
        super().__init__(message, "AI_ERROR", error_details)


class AIConfigError(AIAnalysisError):
    """AI配置错误"""

    def __init__(self, message: str, config_key: str = None, details: dict = None):
        error_details = details or {}
        if config_key:
            error_details['config_key'] = config_key
        super().__init__(message, details=error_details)
        self.error_code = "AI_CONFIG_ERROR"


class AIAPIError(AIAnalysisError):
    """AI API调用错误"""

    def __init__(self, message: str, status_code: int = None, api_url: str = None, details: dict = None):
        error_details = details or {}
        if status_code:
            error_details['status_code'] = status_code
        if api_url:
            error_details['api_url'] = api_url
        super().__init__(message, details=error_details)
        self.error_code = "AI_API_ERROR"


class AITimeoutError(AIAnalysisError):
    """AI请求超时错误"""

    def __init__(self, message: str, timeout: int = None, details: dict = None):
        error_details = details or {}
        if timeout:
            error_details['timeout'] = timeout
        super().__init__(message, details=error_details)
        self.error_code = "AI_TIMEOUT_ERROR"


def handle_exception(exception: Exception, context: str = None) -> dict:
    """
    统一异常处理函数
    
    Args:
        exception: 异常对象
        context: 异常发生的上下文
        
    Returns:
        错误信息字典
    """
    error_info = {
        'error_type': type(exception).__name__,
        'error_message': str(exception),
        'context': context or 'Unknown',
        'suggestion': None
    }
    
    # 根据异常类型提供建议
    if isinstance(exception, ConfigurationError):
        error_info['suggestion'] = "请检查配置文件格式和内容是否正确"
    elif isinstance(exception, NetworkError):
        error_info['suggestion'] = "请检查网络连接和目标网站状态"
    elif isinstance(exception, BrowserError):
        error_info['suggestion'] = "请检查浏览器配置或目标网站是否可访问"
    elif isinstance(exception, DetectionError):
        error_info['suggestion'] = "请检查检测算法配置或内容格式"
    elif isinstance(exception, NotificationError):
        error_info['suggestion'] = "请检查推送平台配置和令牌有效性"
    elif isinstance(exception, StorageError):
        error_info['suggestion'] = "请检查存储权限和磁盘空间"
    elif isinstance(exception, TaskError):
        error_info['suggestion'] = "请检查任务配置和状态"
    elif isinstance(exception, ValidationError):
        error_info['suggestion'] = "请检查输入数据的格式和类型"
    elif isinstance(exception, RateLimitError):
        error_info['suggestion'] = "请等待速率限制重置或调整请求频率"
    elif isinstance(exception, AuthenticationError):
        error_info['suggestion'] = "请检查认证凭据是否正确"
    elif isinstance(exception, ResourceError):
        error_info['suggestion'] = "请检查系统资源是否充足"
    elif isinstance(exception, ConcurrentError):
        error_info['suggestion'] = "请等待其他任务完成或调整并发设置"
    elif isinstance(exception, AIAnalysisError):
        error_info['suggestion'] = "请检查AI配置（API Key、API URL等）是否正确"
    else:
        error_info['suggestion'] = "请查看详细错误信息并尝试解决"
    
    return error_info


__all__ = [
    'WebMonException',
    'ConfigurationError',
    'NetworkError',
    'BrowserError',
    'DetectionError',
    'NotificationError',
    'StorageError',
    'TaskError',
    'ValidationError',
    'RateLimitError',
    'AuthenticationError',
    'ResourceError',
    'ConcurrentError',
    'AIAnalysisError',
    'AIConfigError',
    'AIAPIError',
    'AITimeoutError',
    'handle_exception'
]