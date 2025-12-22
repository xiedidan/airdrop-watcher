#!/usr/bin/env python3
"""
敏感信息保护模块
自动屏蔽日志和输出中的敏感信息（如token、api_key、password等）
"""

import re
import os
import logging
from typing import Dict, List, Optional, Any, Pattern, Callable
from functools import lru_cache


class SecurityManager:
    """
    敏感信息管理器

    用于在日志输出前自动屏蔽敏感信息，防止token、密码等泄露到日志文件中。

    使用方式：
    1. 直接使用单例：security_manager.mask(message)
    2. 注册自定义敏感信息：security_manager.register_secret("my_secret_value")
    3. 集成到logging：使用SecretMaskingFilter

    示例:
        >>> from webmon.utils.security_manager import security_manager
        >>> security_manager.mask("API key: sk-1234567890abcdef")
        'API key: sk-12****cdef'
    """

    # 敏感信息的正则表达式模式
    DEFAULT_PATTERNS: Dict[str, Pattern] = {
        # API Keys (OpenAI, Anthropic等)
        "openai_key": re.compile(r'sk-[a-zA-Z0-9]{32,}'),
        "anthropic_key": re.compile(r'sk-ant-[a-zA-Z0-9-]{32,}'),

        # Discord Webhook URL
        "discord_webhook": re.compile(
            r'https://discord\.com/api/webhooks/\d+/[a-zA-Z0-9_-]+'
        ),

        # Telegram Bot Token
        "telegram_token": re.compile(r'\d{8,10}:[a-zA-Z0-9_-]{35}'),

        # 飞书 Webhook URL
        "feishu_webhook": re.compile(
            r'https://open\.(?:feishu|larksuite)\.cn/open-apis/bot/v2/hook/[a-zA-Z0-9-]+'
        ),

        # PushPlus Token
        "pushplus_token": re.compile(r'[a-f0-9]{32}'),

        # 通用API Key模式
        "generic_api_key": re.compile(
            r'(?:api[_-]?key|apikey|api_secret|secret[_-]?key)\s*[=:]\s*["\']?([a-zA-Z0-9_-]{16,})["\']?',
            re.IGNORECASE
        ),

        # Bearer Token
        "bearer_token": re.compile(
            r'Bearer\s+[a-zA-Z0-9._-]{20,}',
            re.IGNORECASE
        ),

        # Authorization Header
        "auth_header": re.compile(
            r'Authorization\s*[=:]\s*["\']?[a-zA-Z0-9._-]{20,}["\']?',
            re.IGNORECASE
        ),

        # 密码模式
        "password": re.compile(
            r'(?:password|passwd|pwd)\s*[=:]\s*["\']?([^\s"\']{4,})["\']?',
            re.IGNORECASE
        ),

        # 通用Token模式（32-64位的hex或base64字符串）
        "generic_token": re.compile(
            r'(?:token)\s*[=:]\s*["\']?([a-zA-Z0-9_-]{32,64})["\']?',
            re.IGNORECASE
        ),

        # Webhook URL通用模式
        "webhook_url": re.compile(
            r'(?:webhook[_-]?url)\s*[=:]\s*["\']?(https?://[^\s"\']+)["\']?',
            re.IGNORECASE
        ),
    }

    # 敏感环境变量名称
    SENSITIVE_ENV_VARS = [
        'AI_API_KEY',
        'OPENAI_API_KEY',
        'ANTHROPIC_API_KEY',
        'PUSHPLUS_TOKEN',
        'TELEGRAM_BOT_TOKEN',
        'DISCORD_WEBHOOK_URL',
        'FEISHU_WEBHOOK_URL',
        'PROXY_PASSWORD',
        'DATABASE_PASSWORD',
        'SECRET_KEY',
        'JWT_SECRET',
    ]

    def __init__(self, mask_char: str = "*", visible_chars: int = 4):
        """
        初始化敏感信息管理器

        Args:
            mask_char: 用于屏蔽的字符，默认为 '*'
            visible_chars: 保留可见的字符数（头尾各保留），默认为 4
        """
        self.mask_char = mask_char
        self.visible_chars = visible_chars
        self._registered_secrets: List[str] = []
        self._patterns: Dict[str, Pattern] = self.DEFAULT_PATTERNS.copy()
        self._env_secrets_loaded = False

    def register_secret(self, secret: str) -> None:
        """
        注册一个需要屏蔽的敏感值

        Args:
            secret: 需要屏蔽的敏感值
        """
        if secret and len(secret) >= 8 and secret not in self._registered_secrets:
            self._registered_secrets.append(secret)

    def register_secrets(self, secrets: List[str]) -> None:
        """
        批量注册需要屏蔽的敏感值

        Args:
            secrets: 敏感值列表
        """
        for secret in secrets:
            self.register_secret(secret)

    def add_pattern(self, name: str, pattern: Pattern) -> None:
        """
        添加自定义敏感信息匹配模式

        Args:
            name: 模式名称
            pattern: 正则表达式模式
        """
        self._patterns[name] = pattern

    def load_env_secrets(self) -> None:
        """
        从环境变量加载敏感值
        """
        if self._env_secrets_loaded:
            return

        for var_name in self.SENSITIVE_ENV_VARS:
            value = os.getenv(var_name)
            if value and not value.startswith('${'):
                self.register_secret(value)

        self._env_secrets_loaded = True

    def _mask_value(self, value: str) -> str:
        """
        屏蔽一个敏感值

        Args:
            value: 需要屏蔽的值

        Returns:
            屏蔽后的值
        """
        if not value:
            return value

        length = len(value)

        # 短值完全屏蔽
        if length <= self.visible_chars * 2:
            return self.mask_char * length

        # 保留头尾，中间用掩码替换
        visible = self.visible_chars
        masked_len = length - visible * 2
        return value[:visible] + self.mask_char * min(masked_len, 8) + value[-visible:]

    def mask(self, message: str) -> str:
        """
        屏蔽消息中的敏感信息

        Args:
            message: 原始消息

        Returns:
            屏蔽敏感信息后的消息
        """
        if not message or not isinstance(message, str):
            return message

        # 确保环境变量中的敏感值已加载
        self.load_env_secrets()

        result = message

        # 1. 使用正则表达式模式屏蔽
        for pattern_name, pattern in self._patterns.items():
            result = self._mask_by_pattern(result, pattern, pattern_name)

        # 2. 屏蔽注册的敏感值
        for secret in self._registered_secrets:
            if secret in result:
                masked = self._mask_value(secret)
                result = result.replace(secret, masked)

        return result

    def _mask_by_pattern(self, text: str, pattern: Pattern, pattern_name: str) -> str:
        """
        使用正则表达式模式屏蔽文本

        Args:
            text: 原始文本
            pattern: 正则表达式模式
            pattern_name: 模式名称（用于调试）

        Returns:
            屏蔽后的文本
        """
        def replace_match(match: re.Match) -> str:
            matched_text = match.group(0)

            # 如果有捕获组，屏蔽捕获组内容
            if match.lastindex:
                captured = match.group(1)
                masked = self._mask_value(captured)
                return matched_text.replace(captured, masked)
            else:
                # 没有捕获组，屏蔽整个匹配
                return self._mask_value(matched_text)

        return pattern.sub(replace_match, text)

    def mask_dict(self, data: Dict[str, Any],
                  sensitive_keys: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        屏蔽字典中的敏感值

        Args:
            data: 原始字典
            sensitive_keys: 需要屏蔽的键名列表

        Returns:
            屏蔽后的字典
        """
        if sensitive_keys is None:
            sensitive_keys = [
                'token', 'api_key', 'apikey', 'secret', 'password',
                'passwd', 'pwd', 'webhook_url', 'bot_token', 'authorization'
            ]

        result = {}
        for key, value in data.items():
            key_lower = key.lower()

            if any(sk in key_lower for sk in sensitive_keys):
                if isinstance(value, str) and value:
                    if value.startswith('${'):
                        # 环境变量引用，保留
                        result[key] = value
                    else:
                        result[key] = self._mask_value(value)
                else:
                    result[key] = value
            elif isinstance(value, dict):
                result[key] = self.mask_dict(value, sensitive_keys)
            elif isinstance(value, list):
                result[key] = [
                    self.mask_dict(item, sensitive_keys) if isinstance(item, dict)
                    else item
                    for item in value
                ]
            else:
                result[key] = value

        return result


class SecretMaskingFilter(logging.Filter):
    """
    日志过滤器，自动屏蔽日志消息中的敏感信息

    使用方式:
        import logging
        from webmon.utils.security_manager import SecretMaskingFilter

        logger = logging.getLogger(__name__)
        logger.addFilter(SecretMaskingFilter())
    """

    def __init__(self, security_manager: Optional[SecurityManager] = None):
        """
        初始化日志过滤器

        Args:
            security_manager: SecurityManager实例，如果不提供则使用全局单例
        """
        super().__init__()
        self.security_manager = security_manager or get_security_manager()

    def filter(self, record: logging.LogRecord) -> bool:
        """
        过滤日志记录，屏蔽敏感信息

        Args:
            record: 日志记录

        Returns:
            始终返回True，允许所有日志通过（只是修改内容）
        """
        if hasattr(record, 'msg') and record.msg:
            # 处理消息字符串
            if isinstance(record.msg, str):
                record.msg = self.security_manager.mask(record.msg)
            else:
                # 尝试转换为字符串后处理
                try:
                    record.msg = self.security_manager.mask(str(record.msg))
                except Exception:
                    pass

        # 处理消息参数
        if hasattr(record, 'args') and record.args:
            if isinstance(record.args, dict):
                record.args = {
                    k: self.security_manager.mask(str(v)) if isinstance(v, str) else v
                    for k, v in record.args.items()
                }
            elif isinstance(record.args, tuple):
                record.args = tuple(
                    self.security_manager.mask(str(arg)) if isinstance(arg, str) else arg
                    for arg in record.args
                )

        return True


class LoguruSecretMaskingHandler:
    """
    Loguru日志处理器，自动屏蔽敏感信息

    使用方式:
        from loguru import logger
        from webmon.utils.security_manager import LoguruSecretMaskingHandler

        handler = LoguruSecretMaskingHandler()
        logger.configure(patcher=handler.patch)
    """

    def __init__(self, security_manager: Optional[SecurityManager] = None):
        """
        初始化Loguru处理器

        Args:
            security_manager: SecurityManager实例，如果不提供则使用全局单例
        """
        self.security_manager = security_manager or get_security_manager()

    def patch(self, record: Dict) -> None:
        """
        修补Loguru日志记录

        Args:
            record: Loguru日志记录字典
        """
        if 'message' in record:
            record['message'] = self.security_manager.mask(record['message'])


# 全局单例
_security_manager: Optional[SecurityManager] = None


def get_security_manager() -> SecurityManager:
    """
    获取全局SecurityManager单例

    Returns:
        SecurityManager实例
    """
    global _security_manager
    if _security_manager is None:
        _security_manager = SecurityManager()
    return _security_manager


def mask_secrets(message: str) -> str:
    """
    便捷函数：屏蔽消息中的敏感信息

    Args:
        message: 原始消息

    Returns:
        屏蔽后的消息
    """
    return get_security_manager().mask(message)


def register_secret(secret: str) -> None:
    """
    便捷函数：注册需要屏蔽的敏感值

    Args:
        secret: 敏感值
    """
    get_security_manager().register_secret(secret)


# 模块初始化时创建全局单例
security_manager = get_security_manager()
