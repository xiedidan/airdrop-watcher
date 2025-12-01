"""
通知工厂模块

提供创建通知客户端的工厂方法，支持多种推送平台。
"""

import logging
from typing import Dict, Any, Optional

from .base_platform import NotificationPlatform
from .platforms.pushplus_platform import PushPlusPlatform
from .platforms.telegram_platform import TelegramPlatform
from .platforms.discord_platform import DiscordPlatform
from .platforms.feishu_platform import FeishuPlatform
from ..exceptions import NotificationError


class NotificationFactory:
    """通知工厂类"""
    
    # 支持的平台类型
    SUPPORTED_PLATFORMS = {
        'pushplus': PushPlusPlatform,
        'telegram': TelegramPlatform,
        'discord': DiscordPlatform,
        'feishu': FeishuPlatform
    }
    
    @staticmethod
    def create_client(platform_name: str, config: Optional[Dict[str, Any]] = None) -> Optional[NotificationPlatform]:
        """
        创建通知客户端
        
        Args:
            platform_name: 平台名称
            config: 平台配置
            
        Returns:
            通知平台客户端，创建失败返回None
            
        Raises:
            NotificationError: 平台不支持或配置无效
        """
        logger = logging.getLogger(__name__)
        
        try:
            # 标准化平台名称
            platform_name = platform_name.lower().strip()
            
            # 检查平台是否支持
            if platform_name not in NotificationFactory.SUPPORTED_PLATFORMS:
                raise NotificationError(f"不支持的平台: {platform_name}")
            
            # 获取平台类
            platform_class = NotificationFactory.SUPPORTED_PLATFORMS[platform_name]
            
            # 创建平台实例
            platform = platform_class(config or {})
            
            # 验证配置
            if not platform.validate_config():
                logger.warning(f"平台 {platform_name} 配置无效")
                return None
            
            logger.info(f"成功创建通知客户端: {platform_name}")
            return platform
            
        except NotificationError:
            raise
        except Exception as e:
            logger.error(f"创建通知客户端失败: {e}")
            raise NotificationError(f"创建通知客户端失败: {e}")
    
    @staticmethod
    def create_platform(platform_name: str, config: Optional[Dict[str, Any]] = None) -> NotificationPlatform:
        """
        创建通知平台实例
        
        Args:
            platform_name: 平台名称
            config: 平台配置
            
        Returns:
            通知平台实例
            
        Raises:
            NotificationError: 平台不支持
        """
        logger = logging.getLogger(__name__)
        
        try:
            # 标准化平台名称
            platform_name = platform_name.lower().strip()
            
            # 检查平台是否支持
            if platform_name not in NotificationFactory.SUPPORTED_PLATFORMS:
                raise NotificationError(f"不支持的平台: {platform_name}")
            
            # 获取平台类
            platform_class = NotificationFactory.SUPPORTED_PLATFORMS[platform_name]
            
            # 创建平台实例
            platform = platform_class(config or {})
            
            logger.info(f"成功创建通知平台: {platform_name}")
            return platform
            
        except NotificationError:
            raise
        except Exception as e:
            logger.error(f"创建通知平台失败: {e}")
            raise NotificationError(f"创建通知平台失败: {e}")
    
    @staticmethod
    def get_supported_platforms() -> Dict[str, str]:
        """
        获取支持的平台列表
        
        Returns:
            平台名称和描述的映射
        """
        return {
            'pushplus': 'PushPlus微信推送平台',
            'telegram': 'Telegram Bot消息推送平台',
            'discord': 'Discord Webhook消息推送平台',
            'feishu': '飞书Webhook消息推送平台'
        }
    
    @staticmethod
    def get_platform_info(platform_name: str) -> Optional[Dict[str, Any]]:
        """
        获取平台信息
        
        Args:
            platform_name: 平台名称
            
        Returns:
            平台信息，不支持的平台返回None
        """
        try:
            # 创建临时实例来获取信息
            platform = NotificationFactory.create_platform(platform_name)
            if platform:
                return platform.get_platform_info()
            return None
        except Exception as e:
            logging.getLogger(__name__).error(f"获取平台信息失败: {e}")
            return None
    
    @staticmethod
    def validate_config(platform_name: str, config: Dict[str, Any]) -> bool:
        """
        验证平台配置
        
        Args:
            platform_name: 平台名称
            config: 平台配置
            
        Returns:
            配置是否有效
        """
        try:
            platform = NotificationFactory.create_platform(platform_name, config)
            return platform.validate_config() if platform else False
        except Exception:
            return False
    
    @staticmethod
    def test_platform(platform_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        测试平台配置
        
        Args:
            platform_name: 平台名称
            config: 平台配置
            
        Returns:
            测试结果
        """
        logger = logging.getLogger(__name__)
        
        try:
            # 创建平台实例
            platform = NotificationFactory.create_platform(platform_name, config)
            if not platform:
                return {
                    'success': False,
                    'error': '无法创建平台实例',
                    'platform': platform_name
                }
            
            # 测试连接
            import asyncio
            if asyncio.iscoroutinefunction(platform.test_connection):
                result = asyncio.run(platform.test_connection())
            else:
                result = platform.test_connection()
            
            return result
            
        except Exception as e:
            logger.error(f"测试平台失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'platform': platform_name
            }