"""
配置管理服务

提供配置的读写操作。
"""

import logging
from typing import Dict, Any, Optional, List

from ...config import ConfigManager


class SettingsService:
    """配置管理服务"""

    # 支持的配置段
    SECTIONS = [
        "monitoring",
        "detection",
        "notification",
        "ai",
        "storage",
        "logging",
        "scheduler",
    ]

    def __init__(self):
        self.config_manager = ConfigManager()
        self.logger = logging.getLogger(__name__)

    def get_all_settings(self, mask_secrets: bool = True) -> Dict[str, Any]:
        """
        获取所有配置

        Args:
            mask_secrets: 是否掩码敏感信息

        Returns:
            所有配置字典
        """
        settings = {}
        for section in self.SECTIONS:
            settings[section] = self.get_section(section, mask_secrets)
        return settings

    def get_section(self, section: str, mask_secrets: bool = True) -> Dict[str, Any]:
        """
        获取指定配置段

        Args:
            section: 配置段名称
            mask_secrets: 是否掩码敏感信息

        Returns:
            配置字典
        """
        if section not in self.SECTIONS:
            raise ValueError(f"不支持的配置段: {section}")

        method_map = {
            "monitoring": self.config_manager.get_monitoring_config,
            "detection": self.config_manager.get_detection_config,
            "notification": self.config_manager.get_notification_config,
            "ai": lambda: self.config_manager.get_ai_config(resolve_env=False),
            "storage": self.config_manager.get_storage_config,
            "logging": self.config_manager.get_logging_config,
            "scheduler": self.config_manager.get_scheduler_config,
        }

        config = method_map[section]()

        if mask_secrets:
            config = self._mask_secrets(config, section)

        return config

    def update_section(self, section: str, updates: Dict[str, Any]) -> bool:
        """
        更新指定配置段

        Args:
            section: 配置段名称
            updates: 更新内容

        Returns:
            是否成功
        """
        if section not in self.SECTIONS:
            raise ValueError(f"不支持的配置段: {section}")

        try:
            # 获取当前配置
            current = self.get_section(section, mask_secrets=False)

            # 深度合并更新
            merged = self._deep_merge(current, updates)

            # 根据配置段调用对应的更新方法
            if section == "monitoring":
                return self._update_monitoring(merged)
            elif section == "detection":
                return self._update_detection(merged)
            elif section == "notification":
                return self._update_notification(merged)
            elif section == "ai":
                return self.config_manager.update_ai_config(merged)
            elif section == "storage":
                return self._update_storage(merged)
            elif section == "logging":
                return self.config_manager.update_logging_config(merged)
            elif section == "scheduler":
                return self.config_manager.update_scheduler_config(merged)

            return False

        except Exception as e:
            self.logger.error(f"更新配置失败 [{section}]: {e}")
            return False

    def _update_monitoring(self, config: Dict[str, Any]) -> bool:
        """更新监控配置"""
        try:
            self.config_manager.json_config.set("monitoring", config)
            self.config_manager.json_config.save()
            self.logger.info("监控配置已更新")
            return True
        except Exception as e:
            self.logger.error(f"更新监控配置失败: {e}")
            return False

    def _update_detection(self, config: Dict[str, Any]) -> bool:
        """更新检测配置"""
        try:
            self.config_manager.json_config.set("detection", config)
            self.config_manager.json_config.save()
            self.logger.info("检测配置已更新")
            return True
        except Exception as e:
            self.logger.error(f"更新检测配置失败: {e}")
            return False

    def _update_notification(self, config: Dict[str, Any]) -> bool:
        """更新通知配置"""
        try:
            self.config_manager.json_config.set("notification", config)
            self.config_manager.json_config.save()
            self.logger.info("通知配置已更新")
            return True
        except Exception as e:
            self.logger.error(f"更新通知配置失败: {e}")
            return False

    def _update_storage(self, config: Dict[str, Any]) -> bool:
        """更新存储配置"""
        try:
            self.config_manager.json_config.set("storage", config)
            self.config_manager.json_config.save()
            self.logger.info("存储配置已更新")
            return True
        except Exception as e:
            self.logger.error(f"更新存储配置失败: {e}")
            return False

    def get_notification_platforms(self) -> List[Dict[str, Any]]:
        """
        获取通知平台列表

        Returns:
            平台配置列表
        """
        notification_config = self.config_manager.get_notification_config()
        platform_configs = notification_config.get("platform_configs", {})
        enabled_platforms = notification_config.get("enabled_platforms", [])

        platforms = []
        for name, config in platform_configs.items():
            platforms.append({
                "name": name,
                "enabled": config.get("enabled", False),
                "in_enabled_list": name in enabled_platforms,
                "config": self._mask_secrets(config, "notification"),
            })

        return platforms

    def update_platform_config(
        self, platform: str, config: Dict[str, Any], enable: Optional[bool] = None
    ) -> bool:
        """
        更新单个平台配置

        Args:
            platform: 平台名称
            config: 平台配置
            enable: 是否启用（None 表示不修改）

        Returns:
            是否成功
        """
        try:
            notification_config = self.config_manager.get_notification_config()
            platform_configs = notification_config.get("platform_configs", {})
            enabled_platforms = notification_config.get("enabled_platforms", [])

            # 更新平台配置
            if platform in platform_configs:
                platform_configs[platform].update(config)
            else:
                platform_configs[platform] = config

            # 更新启用状态
            if enable is not None:
                if enable and platform not in enabled_platforms:
                    enabled_platforms.append(platform)
                elif not enable and platform in enabled_platforms:
                    enabled_platforms.remove(platform)
                platform_configs[platform]["enabled"] = enable

            notification_config["platform_configs"] = platform_configs
            notification_config["enabled_platforms"] = enabled_platforms

            return self._update_notification(notification_config)

        except Exception as e:
            self.logger.error(f"更新平台配置失败 [{platform}]: {e}")
            return False

    def reset_section(self, section: str) -> bool:
        """
        重置指定配置段为默认值

        Args:
            section: 配置段名称

        Returns:
            是否成功
        """
        if section not in self.SECTIONS:
            raise ValueError(f"不支持的配置段: {section}")

        try:
            # 获取默认配置
            defaults = self._get_default_config(section)
            if defaults is None:
                return False

            # 应用默认配置
            return self.update_section(section, defaults)

        except Exception as e:
            self.logger.error(f"重置配置失败 [{section}]: {e}")
            return False

    def _get_default_config(self, section: str) -> Optional[Dict[str, Any]]:
        """获取默认配置"""
        defaults = {
            "monitoring": {
                "default_interval": 300,
                "default_timeout": 30000,
                "max_retries": 3,
                "concurrent_tasks": 5,
                "browser_headless": True,
                "rate_limit": {
                    "requests_per_minute": 30,
                    "retry_delay": 60
                }
            },
            "detection": {
                "enable_smart_detection": True,
                "similarity_threshold": 0.85,
                "min_change_length": 10,
                "ignore_selectors": [
                    ".advertisement",
                    ".cookie-banner",
                    ".timestamp",
                    ".view-count"
                ],
                "extract_fields": {}
            },
            "notification": {
                "enabled_platforms": [],
                "templates": {
                    "default": "🌐 网页变化检测\n\n任务: {task_name}\nURL: {url}\n变化时间: {change_time}\n变化类型: {change_type}\n\n{change_summary}"
                },
                "platform_configs": {}
            },
            "ai": {
                "enabled": False,
                "api_url": "https://api.deepseek.com/v1",
                "api_key": "${AI_API_KEY}",
                "model": "deepseek-reasoner",
                "max_tokens": 2048,
                "temperature": 0.7,
                "timeout": 60,
                "retry_attempts": 3,
                "retry_base_delay": 5.0,
                "retry_max_delay": 60.0,
                "system_prompt": "",
                "user_prompt_template": ""
            },
            "storage": {
                "history_file": "data/history.json",
                "max_history_entries": 1000,
                "auto_cleanup_days": 30
            },
            "logging": {
                "level": "INFO",
                "log_dir": "./logs",
                "rotation": {
                    "type": "time",
                    "interval": 7,
                    "retention_days": 30,
                    "max_size": 10485760,
                    "backup_count": 5
                },
                "handlers": ["console", "file"],
                "compression": False,
                "async_mode": False,
                "buffer_size": 1000
            },
            "scheduler": {
                "performance": {
                    "max_concurrent_tasks": 15,
                    "max_browser_resources": 8,
                    "scheduler_loop_interval": 0.2
                },
                "retry": {
                    "retry_attempts": 5,
                    "retry_delay": 120
                }
            }
        }
        return defaults.get(section)

    def _mask_secrets(self, config: Dict[str, Any], section: str) -> Dict[str, Any]:
        """掩码敏感信息"""
        # 需要掩码的字段
        secret_fields = {
            "notification": ["token", "webhook_url", "bot_token", "api_key"],
            "ai": ["api_key"],
        }

        fields_to_mask = secret_fields.get(section, [])
        if not fields_to_mask:
            return config

        return self._mask_dict(config, fields_to_mask)

    def _mask_dict(self, data: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
        """递归掩码字典中的敏感字段"""
        result = {}
        for key, value in data.items():
            if key in fields and isinstance(value, str) and value:
                # 保留开头和结尾部分
                if value.startswith("${"):
                    # 环境变量引用，显示占位符
                    result[key] = value
                elif len(value) > 8:
                    result[key] = value[:4] + "****" + value[-4:]
                else:
                    result[key] = "****"
            elif isinstance(value, dict):
                result[key] = self._mask_dict(value, fields)
            else:
                result[key] = value
        return result

    def _deep_merge(self, base: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
        """深度合并两个字典"""
        result = base.copy()
        for key, value in updates.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result


# 全局服务实例
_settings_service: Optional[SettingsService] = None


def get_settings_service() -> SettingsService:
    """获取配置服务实例"""
    global _settings_service
    if _settings_service is None:
        _settings_service = SettingsService()
    return _settings_service
