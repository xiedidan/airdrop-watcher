"""
工具模块
提供项目中常用的工具函数
"""

# 从formatters模块导入格式化函数
from .formatters import (
    format_file_size,
    format_duration,
    format_duration_precise,
    format_bytes_per_second,
    format_percentage,
    format_count
)

# 从validators模块导入验证函数
from .validators import (
    validate_url,
    validate_task_id,
    validate_css_selector,
    validate_interval,
    validate_timeout,
    validate_email,
    validate_phone,
    validate_platform_name,
    validate_similarity_threshold,
    validate_retry_times,
    validate_config_name,
    is_valid_uuid,
    sanitize_filename,
    validate_value,
    VALIDATORS
)

# 从logger模块导入日志函数
from .logger import get_logger, setup_global_logger

# 从simple_logger模块导入简化日志函数（备用）
from .simple_logger import get_logger as get_simple_logger, setup_global_logger as setup_simple_global_logger

# 从security_manager模块导入敏感信息保护
from .security_manager import (
    SecurityManager,
    SecretMaskingFilter,
    LoguruSecretMaskingHandler,
    get_security_manager,
    mask_secrets,
    register_secret,
    security_manager
)

__all__ = [
    # 格式化函数
    'format_file_size',
    'format_duration',
    'format_duration_precise',
    'format_bytes_per_second',
    'format_percentage',
    'format_count',
    # 验证函数
    'validate_url',
    'validate_task_id',
    'validate_css_selector',
    'validate_interval',
    'validate_timeout',
    'validate_email',
    'validate_phone',
    'validate_platform_name',
    'validate_similarity_threshold',
    'validate_retry_times',
    'validate_config_name',
    'is_valid_uuid',
    'sanitize_filename',
    'validate_value',
    'VALIDATORS',
    # 日志函数
    'get_logger',
    'setup_global_logger',
    'get_simple_logger',
    'setup_simple_global_logger',
    # 敏感信息保护
    'SecurityManager',
    'SecretMaskingFilter',
    'LoguruSecretMaskingHandler',
    'get_security_manager',
    'mask_secrets',
    'register_secret',
    'security_manager'
]