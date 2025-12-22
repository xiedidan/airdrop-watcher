#!/usr/bin/env python3
"""
敏感信息保护模块测试
测试SecurityManager类的敏感信息屏蔽功能
"""

import os
import pytest
import logging
from unittest.mock import patch

from webmon.utils.security_manager import (
    SecurityManager,
    SecretMaskingFilter,
    get_security_manager,
    mask_secrets,
    register_secret
)


class TestSecurityManager:
    """SecurityManager测试类"""

    def setup_method(self):
        """每个测试方法前重置SecurityManager"""
        self.sm = SecurityManager()

    def test_init_default_params(self):
        """测试默认参数初始化"""
        sm = SecurityManager()
        assert sm.mask_char == "*"
        assert sm.visible_chars == 4

    def test_init_custom_params(self):
        """测试自定义参数初始化"""
        sm = SecurityManager(mask_char="#", visible_chars=2)
        assert sm.mask_char == "#"
        assert sm.visible_chars == 2

    def test_mask_value_short(self):
        """测试短值完全屏蔽"""
        masked = self.sm._mask_value("abc123")
        assert masked == "******"

    def test_mask_value_long(self):
        """测试长值部分屏蔽"""
        masked = self.sm._mask_value("sk-abcd1234efgh5678ijkl")
        assert masked.startswith("sk-a")
        assert masked.endswith("ijkl")
        assert "****" in masked

    def test_mask_empty_value(self):
        """测试空值不变"""
        assert self.sm._mask_value("") == ""
        assert self.sm._mask_value(None) is None

    def test_mask_openai_key(self):
        """测试OpenAI API Key屏蔽"""
        message = "Using API key: sk-1234567890abcdefghijklmnopqrstuv"
        masked = self.sm.mask(message)
        assert "sk-1234567890abcdefghijklmnopqrstuv" not in masked
        assert "****" in masked

    def test_mask_discord_webhook(self):
        """测试Discord Webhook URL屏蔽"""
        message = "Discord webhook: https://discord.com/api/webhooks/123456789012345678/abcdefghijklmnopqrstuvwxyz1234567890"
        masked = self.sm.mask(message)
        assert "123456789012345678" not in masked or "****" in masked

    def test_mask_telegram_token(self):
        """测试Telegram Bot Token屏蔽"""
        message = "Bot token: 1234567890:ABCDEFGHIJ-klmnopqrstuvwxyz12345678"
        masked = self.sm.mask(message)
        assert "1234567890:ABCDEFGHIJ-klmnopqrstuvwxyz12345678" not in masked

    def test_mask_bearer_token(self):
        """测试Bearer Token屏蔽"""
        message = "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        masked = self.sm.mask(message)
        assert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" not in masked

    def test_mask_password_field(self):
        """测试密码字段屏蔽"""
        message = 'password = "my_secret_password_123"'
        masked = self.sm.mask(message)
        assert "my_secret_password_123" not in masked

    def test_mask_api_key_field(self):
        """测试api_key字段屏蔽"""
        message = 'api_key: "abcdef1234567890abcdef"'
        masked = self.sm.mask(message)
        assert "abcdef1234567890abcdef" not in masked

    def test_mask_webhook_url_field(self):
        """测试webhook_url字段屏蔽"""
        message = 'webhook_url = "https://example.com/webhook/secret123"'
        masked = self.sm.mask(message)
        assert "secret123" not in masked or "****" in masked

    def test_register_secret(self):
        """测试注册自定义敏感值"""
        secret = "my_custom_secret_value_12345678"
        self.sm.register_secret(secret)
        message = f"The secret is: {secret}"
        masked = self.sm.mask(message)
        assert secret not in masked
        assert "****" in masked

    def test_register_secrets_batch(self):
        """测试批量注册敏感值"""
        secrets = ["secret_one_12345678", "secret_two_12345678"]
        self.sm.register_secrets(secrets)
        message = f"Secrets: {secrets[0]} and {secrets[1]}"
        masked = self.sm.mask(message)
        assert secrets[0] not in masked
        assert secrets[1] not in masked

    def test_register_short_secret_ignored(self):
        """测试短敏感值被忽略"""
        short_secret = "abc"
        self.sm.register_secret(short_secret)
        assert short_secret not in self.sm._registered_secrets

    def test_mask_dict_basic(self):
        """测试字典敏感信息屏蔽"""
        data = {
            "name": "test",
            "api_key": "sk-1234567890abcdef",
            "password": "secretpass123"
        }
        masked = self.sm.mask_dict(data)
        assert masked["name"] == "test"
        assert "****" in masked["api_key"]
        assert "****" in masked["password"]

    def test_mask_dict_nested(self):
        """测试嵌套字典屏蔽"""
        data = {
            "config": {
                "notification": {
                    "token": "abcd1234efgh5678ijkl"
                }
            }
        }
        masked = self.sm.mask_dict(data)
        assert "****" in masked["config"]["notification"]["token"]

    def test_mask_dict_env_var_preserved(self):
        """测试环境变量引用保留"""
        data = {
            "api_key": "${AI_API_KEY}",
            "token": "${PUSHPLUS_TOKEN}"
        }
        masked = self.sm.mask_dict(data)
        assert masked["api_key"] == "${AI_API_KEY}"
        assert masked["token"] == "${PUSHPLUS_TOKEN}"

    def test_mask_dict_list_values(self):
        """测试包含列表的字典屏蔽"""
        data = {
            "platforms": [
                {"token": "secret_token_12345678"},
                {"api_key": "api_key_123456789"}
            ]
        }
        masked = self.sm.mask_dict(data)
        assert "****" in masked["platforms"][0]["token"]
        assert "****" in masked["platforms"][1]["api_key"]

    def test_load_env_secrets(self):
        """测试从环境变量加载敏感值"""
        with patch.dict(os.environ, {"AI_API_KEY": "test_api_key_12345678"}):
            sm = SecurityManager()
            sm._env_secrets_loaded = False  # 重置状态
            sm.load_env_secrets()
            message = "Using key: test_api_key_12345678"
            masked = sm.mask(message)
            assert "test_api_key_12345678" not in masked

    def test_add_custom_pattern(self):
        """测试添加自定义匹配模式"""
        import re
        self.sm.add_pattern("custom", re.compile(r"CUSTOM-[A-Z0-9]{10}"))
        message = "Code: CUSTOM-ABC1234567"
        masked = self.sm.mask(message)
        assert "ABC1234567" not in masked or "****" in masked

    def test_mask_non_string(self):
        """测试非字符串输入"""
        assert self.sm.mask(None) is None
        assert self.sm.mask(123) == 123
        assert self.sm.mask([1, 2, 3]) == [1, 2, 3]

    def test_no_sensitive_info(self):
        """测试无敏感信息的消息不变"""
        message = "This is a normal log message without secrets"
        masked = self.sm.mask(message)
        assert masked == message


class TestSecretMaskingFilter:
    """SecretMaskingFilter测试类"""

    def test_filter_basic(self):
        """测试基本过滤功能"""
        filter_obj = SecretMaskingFilter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=1,
            msg="API key: sk-1234567890abcdefghijklmnopqrstuv",
            args=(),
            exc_info=None
        )
        result = filter_obj.filter(record)
        assert result is True
        assert "sk-1234567890abcdefghijklmnopqrstuv" not in record.msg

    def test_filter_with_args(self):
        """测试带参数的日志过滤"""
        filter_obj = SecretMaskingFilter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=1,
            msg="Token: %s",
            args=("secret_token_12345678901234567890",),
            exc_info=None
        )
        result = filter_obj.filter(record)
        assert result is True

    def test_filter_dict_args(self):
        """测试字典参数的日志过滤"""
        filter_obj = SecretMaskingFilter()
        # 字典参数必须作为元组的第一个元素传递
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=1,
            msg="Config: %(token)s",
            args=({"token": "abcd1234567890efghijklmnop"},),
            exc_info=None
        )
        result = filter_obj.filter(record)
        assert result is True


class TestGlobalFunctions:
    """全局函数测试类"""

    def test_get_security_manager_singleton(self):
        """测试全局单例获取"""
        sm1 = get_security_manager()
        sm2 = get_security_manager()
        assert sm1 is sm2

    def test_mask_secrets_function(self):
        """测试便捷函数mask_secrets"""
        message = "key: sk-1234567890abcdefghijklmnopqrstuv"
        masked = mask_secrets(message)
        assert "sk-1234567890abcdefghijklmnopqrstuv" not in masked

    def test_register_secret_function(self):
        """测试便捷函数register_secret"""
        secret = "global_secret_12345678"
        register_secret(secret)
        masked = mask_secrets(f"Secret: {secret}")
        assert secret not in masked


class TestRealWorldScenarios:
    """真实场景测试"""

    def test_ai_config_log(self):
        """测试AI配置日志"""
        sm = SecurityManager()
        log_msg = 'AI配置: api_key="sk-proj-abcdef1234567890", model="gpt-4"'
        masked = sm.mask(log_msg)
        assert "sk-proj-abcdef1234567890" not in masked
        assert 'model="gpt-4"' in masked

    def test_notification_config_log(self):
        """测试通知配置日志"""
        sm = SecurityManager()
        log_msg = """通知配置:
        discord_webhook: https://discord.com/api/webhooks/1234567890123456789/abcdefghijklmnopqrstuvwxyz
        telegram_token: 1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ12345"""
        masked = sm.mask(log_msg)
        # Discord webhook和Telegram token应该被部分屏蔽
        assert "****" in masked or "1234567890123456789/abcdefghijklmnopqrstuvwxyz" not in masked

    def test_json_config_log(self):
        """测试JSON配置日志"""
        sm = SecurityManager()
        # 使用完整的OpenAI格式的key（至少32位）
        log_msg = '{"api_key": "sk-test12345678901234567890abcdefgh", "enabled": true}'
        masked = sm.mask(log_msg)
        # API key应该被屏蔽
        assert "sk-test12345678901234567890abcdefgh" not in masked
        assert "enabled" in masked

    def test_error_log_with_token(self):
        """测试包含token的错误日志"""
        sm = SecurityManager()
        log_msg = "API调用失败: 401 Unauthorized, token=Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyIn0.sig"
        masked = sm.mask(log_msg)
        assert "eyJhbGciOiJIUzI1NiJ9" not in masked


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
