"""
网络配置模块

提供代理、SSL验证、User-Agent等网络安全相关的配置管理。
"""
import logging
from typing import Optional, Dict, Any
from urllib.parse import urlparse

from ..config import ConfigManager
from ..utils.logger import get_logger


class NetworkConfig:
    """网络配置管理器"""

    def __init__(self, config_manager: Optional[ConfigManager] = None):
        """
        初始化网络配置

        Args:
            config_manager: 配置管理器实例
        """
        self.config_manager = config_manager or ConfigManager()
        self.logger = get_logger(__name__)

        # 加载配置
        self._load_config()

    def _load_config(self):
        """加载网络配置"""
        try:
            # 代理配置
            self.http_proxy = self.config_manager.get('HTTP_PROXY')
            self.https_proxy = self.config_manager.get('HTTPS_PROXY')
            self.socks_proxy = self.config_manager.get('SOCKS_PROXY')
            self.no_proxy = self.config_manager.get('NO_PROXY', 'localhost,127.0.0.1')

            # SSL配置
            self.verify_ssl = self.config_manager.get('VERIFY_SSL', 'true').lower() == 'true'
            self.client_cert_path = self.config_manager.get('CLIENT_CERT_PATH')
            self.client_key_path = self.config_manager.get('CLIENT_KEY_PATH')

            # User-Agent配置
            self.custom_user_agent = self.config_manager.get('CUSTOM_USER_AGENT')
            self.browser_user_agent = self.config_manager.get('BROWSER_USER_AGENT')

            # 代理认证
            self.proxy_username = self.config_manager.get('PROXY_USERNAME')
            self.proxy_password = self.config_manager.get('PROXY_PASSWORD')

            self.logger.info("网络配置加载完成")

        except Exception as e:
            self.logger.error(f"加载网络配置失败: {e}")
            # 使用默认值
            self.http_proxy = None
            self.https_proxy = None
            self.socks_proxy = None
            self.no_proxy = 'localhost,127.0.0.1'
            self.verify_ssl = True
            self.custom_user_agent = None

    def get_proxy_config(self, url: Optional[str] = None) -> Optional[Dict[str, str]]:
        """
        获取代理配置

        Args:
            url: 目标URL，用于判断是否跳过代理

        Returns:
            代理配置字典，如果不需要代理则返回None
        """
        # 检查是否应跳过代理
        if url and self._should_bypass_proxy(url):
            self.logger.debug(f"URL在NO_PROXY列表中，跳过代理: {url}")
            return None

        # 优先使用SOCKS代理
        if self.socks_proxy:
            return self._parse_socks_proxy(self.socks_proxy)

        # 使用HTTP/HTTPS代理
        if self.http_proxy or self.https_proxy:
            return {
                'server': self.https_proxy or self.http_proxy,
                'username': self.proxy_username,
                'password': self.proxy_password
            }

        return None

    def _parse_socks_proxy(self, socks_proxy: str) -> Dict[str, str]:
        """
        解析SOCKS代理配置

        Args:
            socks_proxy: SOCKS代理地址

        Returns:
            Playwright格式的代理配置
        """
        # SOCKS代理格式: socks5://host:port 或 socks4://host:port
        proxy_config = {
            'server': socks_proxy,
            'username': self.proxy_username,
            'password': self.proxy_password
        }

        self.logger.debug(f"使用SOCKS代理: {socks_proxy}")
        return proxy_config

    def _should_bypass_proxy(self, url: str) -> bool:
        """
        判断URL是否应该跳过代理

        Args:
            url: 目标URL

        Returns:
            是否跳过代理
        """
        if not self.no_proxy:
            return False

        try:
            parsed = urlparse(url)
            hostname = parsed.hostname or parsed.netloc

            # 解析NO_PROXY列表
            no_proxy_list = [item.strip() for item in self.no_proxy.split(',')]

            for no_proxy_item in no_proxy_list:
                # 完全匹配
                if hostname == no_proxy_item:
                    return True

                # 域名匹配（*.example.com）
                if no_proxy_item.startswith('.') and hostname.endswith(no_proxy_item):
                    return True

                # 后缀匹配
                if hostname.endswith('.' + no_proxy_item):
                    return True

            return False

        except Exception as e:
            self.logger.warning(f"判断NO_PROXY失败: {e}")
            return False

    def get_ssl_config(self) -> Dict[str, Any]:
        """
        获取SSL配置

        Returns:
            SSL配置字典
        """
        ssl_config = {
            'ignore_https_errors': not self.verify_ssl
        }

        # 客户端证书（如果有）
        if self.client_cert_path and self.client_key_path:
            ssl_config['client_certificates'] = [{
                'origin': '*',
                'certPath': self.client_cert_path,
                'keyPath': self.client_key_path
            }]
            self.logger.info("已配置客户端证书")

        if not self.verify_ssl:
            self.logger.warning("SSL验证已禁用，这可能存在安全风险")

        return ssl_config

    def get_user_agent(self) -> Optional[str]:
        """
        获取User-Agent配置

        Returns:
            User-Agent字符串，如果未配置则返回None
        """
        # 优先使用自定义User-Agent
        if self.custom_user_agent:
            return self.custom_user_agent

        # 使用浏览器User-Agent
        if self.browser_user_agent:
            return self.browser_user_agent

        # 默认User-Agent（模拟常见浏览器）
        return self._get_default_user_agent()

    def _get_default_user_agent(self) -> str:
        """
        获取默认User-Agent

        Returns:
            默认User-Agent字符串
        """
        # 模拟Windows Chrome浏览器
        return (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        )

    def get_browser_context_options(self, url: Optional[str] = None) -> Dict[str, Any]:
        """
        获取浏览器上下文选项（整合所有网络配置）

        Args:
            url: 目标URL（用于代理判断）

        Returns:
            浏览器上下文选项字典
        """
        options = {}

        # 代理配置
        proxy_config = self.get_proxy_config(url)
        if proxy_config:
            options['proxy'] = proxy_config
            self.logger.info(f"已配置代理: {proxy_config.get('server')}")

        # SSL配置
        ssl_config = self.get_ssl_config()
        options.update(ssl_config)

        # User-Agent
        user_agent = self.get_user_agent()
        if user_agent:
            options['user_agent'] = user_agent
            self.logger.debug(f"已配置User-Agent: {user_agent[:50]}...")

        return options

    def get_config_summary(self) -> Dict[str, Any]:
        """
        获取配置摘要（用于调试和日志）

        Returns:
            配置摘要字典
        """
        return {
            'proxy': {
                'http_proxy': self.http_proxy,
                'https_proxy': self.https_proxy,
                'socks_proxy': self.socks_proxy,
                'no_proxy': self.no_proxy,
                'has_auth': bool(self.proxy_username and self.proxy_password)
            },
            'ssl': {
                'verify_ssl': self.verify_ssl,
                'has_client_cert': bool(self.client_cert_path and self.client_key_path)
            },
            'user_agent': {
                'custom': bool(self.custom_user_agent),
                'browser': bool(self.browser_user_agent)
            }
        }

    def validate_config(self) -> tuple[bool, list[str]]:
        """
        验证网络配置

        Returns:
            (是否有效, 错误消息列表)
        """
        errors = []

        # 验证代理配置
        if self.socks_proxy and not self._is_valid_proxy_url(self.socks_proxy):
            errors.append(f"无效的SOCKS代理地址: {self.socks_proxy}")

        if self.http_proxy and not self._is_valid_proxy_url(self.http_proxy):
            errors.append(f"无效的HTTP代理地址: {self.http_proxy}")

        if self.https_proxy and not self._is_valid_proxy_url(self.https_proxy):
            errors.append(f"无效的HTTPS代理地址: {self.https_proxy}")

        # 验证SSL证书文件
        if self.client_cert_path and self.client_key_path:
            from pathlib import Path
            cert_path = Path(self.client_cert_path)
            key_path = Path(self.client_key_path)

            if not cert_path.exists():
                errors.append(f"客户端证书文件不存在: {self.client_cert_path}")

            if not key_path.exists():
                errors.append(f"客户端私钥文件不存在: {self.client_key_path}")

        # 验证代理认证
        if (self.proxy_username and not self.proxy_password) or \
           (self.proxy_password and not self.proxy_username):
            errors.append("代理认证配置不完整，需要同时设置用户名和密码")

        is_valid = len(errors) == 0

        if not is_valid:
            self.logger.warning(f"网络配置验证失败: {errors}")
        else:
            self.logger.info("网络配置验证通过")

        return is_valid, errors

    def _is_valid_proxy_url(self, proxy_url: str) -> bool:
        """
        验证代理URL格式

        Args:
            proxy_url: 代理URL

        Returns:
            是否有效
        """
        try:
            parsed = urlparse(proxy_url)
            # 检查协议和主机
            valid_schemes = ['http', 'https', 'socks4', 'socks5']
            return (
                parsed.scheme in valid_schemes and
                bool(parsed.hostname) and
                bool(parsed.port or parsed.scheme in ['http', 'https'])
            )
        except Exception:
            return False


class ProxyRotator:
    """代理轮换器（扩展功能）"""

    def __init__(self, proxy_list: list[str]):
        """
        初始化代理轮换器

        Args:
            proxy_list: 代理地址列表
        """
        self.proxy_list = proxy_list
        self.current_index = 0
        self.logger = get_logger(__name__)

    def get_next_proxy(self) -> Optional[str]:
        """
        获取下一个代理

        Returns:
            代理地址，如果列表为空则返回None
        """
        if not self.proxy_list:
            return None

        proxy = self.proxy_list[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxy_list)

        self.logger.debug(f"轮换到代理: {proxy}")
        return proxy

    def mark_proxy_failed(self, proxy: str):
        """
        标记代理失败（可扩展为从列表中移除）

        Args:
            proxy: 失败的代理地址
        """
        self.logger.warning(f"代理失败: {proxy}")
        # 可以实现从列表中移除失败的代理
        # if proxy in self.proxy_list:
        #     self.proxy_list.remove(proxy)
