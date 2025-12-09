"""
Discord Webhook推送平台集成

实现Discord Webhook消息推送服务的集成。
"""
import asyncio
import aiohttp
import logging
import os
from typing import Dict, Any, Optional, List
from datetime import datetime

from ..base_platform import NotificationPlatform, Notification
from ...exceptions import NotificationError


class DiscordPlatform(NotificationPlatform):
    """Discord Webhook推送平台"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化Discord平台
        
        Args:
            config: 平台配置
        """
        super().__init__("discord", config)
        
        # Webhook配置
        self.webhook_url = None
        self.username = "WebMon Bot"
        self.avatar_url = None
        
        # 可选配置
        self.embed_color = 0x00ff00  # 绿色
        self.include_timestamp = True
        self.include_footer = True
        self.footer_text = "WebMon - 网页监控工具"
        self.footer_icon = "https://cdn.discordapp.com/embed/avatars/0.png"
        
        # 更新配置
        self._load_config()
    
    def _load_config(self):
        """加载配置"""
        try:
            # 获取基本配置
            self.webhook_url = self.config.get("webhook_url", "")
            self.username = self.config.get("username", "WebMon Bot")
            self.avatar_url = self.config.get("avatar_url")
            
            # 获取可选配置
            self.embed_color = self.config.get("embed_color", 0x00ff00)
            self.include_timestamp = self.config.get("include_timestamp", True)
            self.include_footer = self.config.get("include_footer", True)
            self.footer_text = self.config.get("footer_text", "WebMon - 网页监控工具")
            self.footer_icon = self.config.get("footer_icon", "https://cdn.discordapp.com/embed/avatars/0.png")
            
            # 检查是否配置
            self.is_configured = self.validate_config()
            
            if self.is_configured:
                self.logger.info("Discord平台配置加载完成")
            else:
                self.logger.warning("Discord平台未配置webhook_url")
                
        except Exception as e:
            self.logger.error(f"Discord配置加载失败: {e}")
            self.is_configured = False
    
    def update_config(self, config: Dict[str, Any]):
        """
        更新平台配置

        Args:
            config: 新配置
        """
        self.config.update(config)
        # 重新加载配置以更新实例变量
        self._load_config()

    def validate_config(self) -> bool:
        """
        验证平台配置

        Returns:
            配置是否有效
        """
        if not self.webhook_url:
            return False

        if not isinstance(self.webhook_url, str):
            return False

        # Discord webhook URL格式验证
        if not self.webhook_url.startswith("https://discord.com/api/webhooks/"):
            return False

        # 基本URL长度检查
        if len(self.webhook_url.strip()) < 60:  # Discord webhook URL通常较长
            return False

        return True
    
    def get_platform_info(self) -> Dict[str, Any]:
        """
        获取平台信息
        
        Returns:
            平台信息字典
        """
        return {
            "platform_name": self.platform_name,
            "description": "Discord Webhook消息推送平台",
            "features": [
                "富文本消息支持",
                "嵌入式消息（Embed）",
                "自定义用户名和头像",
                "支持多字段展示",
                "时间戳显示",
                "颜色自定义"
            ],
            "limits": {
                "max_embeds": 10,  # 每条消息最多10个embed
                "max_title_length": 256,
                "max_description_length": 4096,
                "max_fields": 25,
                "max_field_name_length": 256,
                "max_field_value_length": 1024
            },
            "website": "https://discord.com",
            "docs": "https://discord.com/developers/docs/resources/webhook",
            "is_configured": self.is_configured,
            "config": self.get_config()
        }
    
    async def send_notification(self, notification: Notification) -> bool:
        """
        发送通知到Discord
        
        Args:
            notification: 通知消息
            
        Returns:
            是否发送成功
            
        Raises:
            NotificationError: 发送失败
        """
        if not self.is_configured:
            raise NotificationError("Discord平台未配置", platform=self.platform_name)
        
        if not self.is_enabled():
            self.logger.debug(f"Discord平台已禁用，跳过发送")
            return False
        
        try:
            self.logger.info(f"开始发送Discord通知 - 标题: {notification.title}")
            
            # 准备请求数据
            payload = self._prepare_payload(notification)
            
            # 发送请求
            success = await self._send_webhook(payload)
            
            # 记录结果
            if success:
                self.record_success()
                self.logger.info(f"Discord通知发送成功 - 标题: {notification.title}")
            else:
                self.record_failure()
                self.logger.warning(f"Discord通知发送失败 - 标题: {notification.title}")
            
            return success
            
        except NotificationError:
            raise
        except Exception as e:
            self.record_failure()
            self.logger.error(f"Discord通知发送异常: {e}")
            raise NotificationError(f"Discord通知发送失败: {e}", platform=self.platform_name)
    
    def _prepare_payload(self, notification: Notification) -> Dict[str, Any]:
        """
        准备Discord webhook负载
        
        Args:
            notification: 通知消息
            
        Returns:
            Discord webhook负载
        """
        # 基础负载
        payload = {
            "username": self.username,
            "content": "",  # 主内容，使用embed代替
            "embeds": [self._create_embed(notification)]
        }
        
        # 添加头像
        if self.avatar_url:
            payload["avatar_url"] = self.avatar_url
        
        return payload
    
    def _create_embed(self, notification: Notification) -> Dict[str, Any]:
        """
        创建Discord embed
        
        Args:
            notification: 通知消息
            
        Returns:
            Embed配置
        """
        # 根据紧急程度选择颜色
        color = self._get_color_by_urgency(notification.urgency)
        
        # 基础embed
        embed = {
            "title": notification.title,
            "description": notification.content,
            "color": color,
            "timestamp": notification.timestamp.isoformat() if self.include_timestamp else None,
            "url": notification.url if notification.url else None
        }
        
        # 添加作者信息
        embed["author"] = {
            "name": self.username,
            "icon_url": self.avatar_url if self.avatar_url else None
        }
        
        # 添加footer
        if self.include_footer:
            embed["footer"] = {
                "text": self.footer_text,
                "icon_url": self.footer_icon
            }
        
        # 添加额外数据作为字段
        if notification.extra_data:
            fields = []
            for key, value in notification.extra_data.items():
                if isinstance(value, (str, int, float, bool)):
                    fields.append({
                        "name": str(key),
                        "value": str(value),
                        "inline": True  # 紧凑显示
                    })
            
            if fields:
                embed["fields"] = fields[:25]  # Discord限制最多25个字段
        
        return embed
    
    def _get_color_by_urgency(self, urgency: str) -> int:
        """
        根据紧急程度获取颜色
        
        Args:
            urgency: 紧急程度
            
        Returns:
            颜色值（十进制）
        """
        color_map = {
            "critical": 0xff0000,  # 红色
            "high": 0xff8800,      # 橙色
            "normal": 0x00ff00,    # 绿色
            "low": 0x0088ff        # 蓝色
        }
        
        return color_map.get(urgency, self.embed_color)
    
    async def _send_webhook(self, payload: Dict[str, Any]) -> bool:
        """
        发送webhook请求

        Args:
            payload: 请求负载

        Returns:
            是否发送成功

        Raises:
            NotificationError: 请求失败
        """
        try:
            timeout = aiohttp.ClientTimeout(total=30)  # 30秒超时

            # 获取代理配置（从环境变量或配置中获取）
            proxy = None
            if os.environ.get('HTTP_PROXY') or os.environ.get('HTTPS_PROXY'):
                proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('HTTP_PROXY')
                self.logger.debug(f"使用代理: {proxy}")

            # trust_env=True 让 aiohttp 自动使用系统代理环境变量
            async with aiohttp.ClientSession(timeout=timeout, trust_env=True) as session:
                async with session.post(self.webhook_url, json=payload, proxy=proxy) as response:
                    response_text = await response.text()
                    
                    # Discord webhook通常返回204 No Content表示成功
                    if response.status == 204:
                        self.logger.debug("Discord webhook发送成功 (204 No Content)")
                        return True
                    elif response.status == 200:
                        # 有时可能返回200和响应数据
                        try:
                            response_data = await response.json()
                            if response_data.get("id"):
                                self.logger.debug(f"Discord消息发送成功，ID: {response_data['id']}")
                                return True
                            else:
                                self.logger.warning(f"Discord返回200但没有消息ID: {response_data}")
                                return False
                        except:
                            # 如果无法解析JSON，只要状态码是200就算成功
                            self.logger.debug("Discord webhook返回200，视为成功")
                            return True
                    else:
                        # 处理错误响应
                        error_msg = f"Discord webhook返回错误状态码: {response.status}"
                        if response_text:
                            error_msg += f", 响应: {response_text[:200]}"
                        
                        self.logger.error(error_msg)
                        raise NotificationError(error_msg, platform=self.platform_name)
                        
        except aiohttp.ClientError as e:
            raise NotificationError(f"网络请求失败: {e}", platform=self.platform_name)
        except asyncio.TimeoutError:
            raise NotificationError("请求超时", platform=self.platform_name)
        except Exception as e:
            raise NotificationError(f"请求异常: {e}", platform=self.platform_name)
    
    def format_message(self, notification: Notification) -> str:
        """
        格式化消息内容（Discord专用）
        
        Args:
            notification: 通知消息
            
        Returns:
            格式化后的消息
        """
        # Discord使用embed格式，这里返回备用文本格式
        return super().format_message(notification)
    
    async def test_connection(self) -> Dict[str, Any]:
        """
        测试Discord连接
        
        Returns:
            测试结果
        """
        try:
            # 创建测试通知
            test_notification = Notification(
                title="WebMon连接测试",
                content="这是一条来自WebMon的连接测试消息，如果您收到此消息，说明Discord Webhook配置正确。",
                urgency="low"
            )
            
            # 发送测试消息
            success = await self.send_notification(test_notification)
            
            return {
                "success": success,
                "platform": self.platform_name,
                "message": "连接测试成功" if success else "连接测试失败",
                "timestamp": datetime.now().isoformat(),
                "platform_info": self.get_platform_info()
            }
            
        except Exception as e:
            return {
                "success": False,
                "platform": self.platform_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_rate_limit_info(self) -> Dict[str, Any]:
        """
        获取速率限制信息
        
        Returns:
            速率限制信息
        """
        return {
            "rate_limit": "5次/2秒",
            "global_limit": "每个webhook全局限制",
            "retry_after": "如果超过限制，会返回429状态码和retry_after头",
            "platform": self.platform_name
        }
    
    def get_message_limits(self) -> Dict[str, Any]:
        """
        获取消息限制信息
        
        Returns:
            消息限制信息
        """
        return {
            "max_embeds": 10,
            "max_title_length": 256,
            "max_description_length": 4096,
            "max_fields": 25,
            "max_field_name_length": 256,
            "max_field_value_length": 1024,
            "max_total_characters": 6000,
            "supports_embeds": True,
            "supports_files": True,
            "supports_images": True,
            "platform": self.platform_name
        }