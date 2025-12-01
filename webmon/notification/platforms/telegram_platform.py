"""
Telegram Bot推送平台集成

实现Telegram Bot消息推送服务的集成。
"""
import asyncio
import aiohttp
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from ..base_platform import NotificationPlatform, Notification
from ...exceptions import NotificationError


class TelegramPlatform(NotificationPlatform):
    """Telegram Bot推送平台"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化Telegram平台
        
        Args:
            config: 平台配置
        """
        super().__init__("telegram", config)
        
        # API配置
        self.api_base_url = "https://api.telegram.org"
        self.bot_token = None
        self.chat_id = None
        
        # 可选配置
        self.parse_mode = "HTML"  # 或 "MarkdownV2"
        self.disable_web_page_preview = False
        self.disable_notification = False
        
        # 更新配置
        self._load_config()
    
    def _load_config(self):
        """加载配置"""
        try:
            # 获取基本配置
            self.bot_token = self.config.get("bot_token", "")
            self.chat_id = self.config.get("chat_id", "")
            
            # 获取可选配置
            self.parse_mode = self.config.get("parse_mode", "HTML")
            self.disable_web_page_preview = self.config.get("disable_web_page_preview", False)
            self.disable_notification = self.config.get("disable_notification", False)
            
            # 检查是否配置
            self.is_configured = self.validate_config()
            
            if self.is_configured:
                self.logger.info("Telegram平台配置加载完成")
            else:
                self.logger.warning("Telegram平台未配置token或chat_id")
                
        except Exception as e:
            self.logger.error(f"Telegram配置加载失败: {e}")
            self.is_configured = False
    
    def validate_config(self) -> bool:
        """
        验证平台配置
        
        Returns:
            配置是否有效
        """
        if not self.bot_token:
            return False
        
        if not self.chat_id:
            return False
        
        if not isinstance(self.bot_token, str):
            return False
        
        if not isinstance(self.chat_id, str):
            return False
        
        # Telegram bot token格式验证
        if len(self.bot_token.strip()) < 40:  # Bot token通常较长
            return False
        
        # Chat ID格式验证（可以是数字ID或@username）
        chat_id = self.chat_id.strip()
        if not (chat_id.isdigit() or chat_id.startswith("@")):
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
            "description": "Telegram Bot消息推送平台",
            "features": [
                "即时消息推送",
                "支持富文本格式",
                "支持Markdown和HTML",
                "支持群组和频道",
                "支持消息格式化",
                "支持链接预览控制"
            ],
            "limits": {
                "max_message_length": 4096,  # Telegram消息长度限制
                "rate_limit": "30条/秒",
                "supports_files": True,
                "supports_images": True
            },
            "website": "https://telegram.org",
            "docs": "https://core.telegram.org/bots/api",
            "is_configured": self.is_configured,
            "config": self.get_config()
        }
    
    async def send_notification(self, notification: Notification) -> bool:
        """
        发送通知到Telegram
        
        Args:
            notification: 通知消息
            
        Returns:
            是否发送成功
            
        Raises:
            NotificationError: 发送失败
        """
        if not self.is_configured:
            raise NotificationError("Telegram平台未配置", platform=self.platform_name)
        
        if not self.is_enabled():
            self.logger.debug(f"Telegram平台已禁用，跳过发送")
            return False
        
        try:
            self.logger.info(f"开始发送Telegram通知 - 标题: {notification.title}")
            
            # 准备请求数据
            payload = self._prepare_payload(notification)
            
            # 发送请求
            success = await self._send_message(payload)
            
            # 记录结果
            if success:
                self.record_success()
                self.logger.info(f"Telegram通知发送成功 - 标题: {notification.title}")
            else:
                self.record_failure()
                self.logger.warning(f"Telegram通知发送失败 - 标题: {notification.title}")
            
            return success
            
        except NotificationError:
            raise
        except Exception as e:
            self.record_failure()
            self.logger.error(f"Telegram通知发送异常: {e}")
            raise NotificationError(f"Telegram通知发送失败: {e}", platform=self.platform_name)
    
    def _prepare_payload(self, notification: Notification) -> Dict[str, Any]:
        """
        准备API请求负载
        
        Args:
            notification: 通知消息
            
        Returns:
            API请求负载
        """
        # 格式化消息内容
        content = self.format_message(notification)
        
        # 检查消息长度
        if len(content) > 4096:  # Telegram消息长度限制
            content = content[:4090] + "..."
            self.logger.warning(f"消息内容被截断以适应Telegram长度限制")
        
        # 基础负载
        payload = {
            "chat_id": self.chat_id,
            "text": content,
            "parse_mode": self.parse_mode,
            "disable_web_page_preview": self.disable_web_page_preview,
            "disable_notification": self.disable_notification
        }
        
        return payload
    
    async def _send_message(self, payload: Dict[str, Any]) -> bool:
        """
        发送消息到Telegram API
        
        Args:
            payload: 请求负载
            
        Returns:
            是否发送成功
            
        Raises:
            NotificationError: 请求失败
        """
        url = f"{self.api_base_url}/bot{self.bot_token}/sendMessage"
        
        try:
            timeout = aiohttp.ClientTimeout(total=30)  # 30秒超时
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, json=payload) as response:
                    response_data = await response.json()
                    
                    # 检查HTTP状态码
                    if response.status != 200:
                        error_msg = self.handle_api_error(response_data, response.status)
                        raise NotificationError(error_msg, platform=self.platform_name)
                    
                    # 检查Telegram返回结果
                    if not response_data.get("ok", False):
                        error_code = response_data.get("error_code", -1)
                        description = response_data.get("description", "未知错误")
                        error_msg = f"Telegram API错误 (code: {error_code}): {description}"
                        raise NotificationError(error_msg, platform=self.platform_name)
                    
                    # 获取消息信息
                    result = response_data.get("result", {})
                    message_id = result.get("message_id")
                    
                    if message_id:
                        self.logger.debug(f"Telegram消息发送成功，消息ID: {message_id}")
                        return True
                    else:
                        self.logger.warning("Telegram API返回成功但没有消息ID")
                        return False
                        
        except aiohttp.ClientError as e:
            raise NotificationError(f"网络请求失败: {e}", platform=self.platform_name)
        except asyncio.TimeoutError:
            raise NotificationError("请求超时", platform=self.platform_name)
        except Exception as e:
            raise NotificationError(f"请求异常: {e}", platform=self.platform_name)
    
    def format_message(self, notification: Notification) -> str:
        """
        格式化消息内容（Telegram专用）
        
        Args:
            notification: 通知消息
            
        Returns:
            格式化后的消息
        """
        # 根据parse_mode选择格式化方式
        if self.parse_mode == "MarkdownV2":
            return self._format_markdown_v2(notification)
        elif self.parse_mode == "Markdown":
            return self._format_markdown(notification)
        else:  # HTML
            return self._format_html(notification)
    
    def _format_html(self, notification: Notification) -> str:
        """HTML格式消息"""
        # 基础格式化
        message = f"<b>{self._escape_html(notification.title)}</b>\n\n"
        
        if notification.content:
            content = self._escape_html(notification.content)
            # 替换换行为HTML换行
            content = content.replace("\n", "\n")
            message += f"{content}\n\n"
        
        if notification.url:
            message += f"🔗 <a href=\"{notification.url}\">查看详情</a>\n"
        
        # 添加时间戳
        time_str = notification.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        message += f"⏰ <i>{time_str}</i>"
        
        # 添加紧急程度标识
        if notification.urgency == "critical":
            message = "🔥 <b>紧急通知</b>\n\n" + message
        elif notification.urgency == "high":
            message = "🚨 <b>重要通知</b>\n\n" + message
        elif notification.urgency == "low":
            message = "📌 通知\n\n" + message
        
        return message.strip()
    
    def _format_markdown(self, notification: Notification) -> str:
        """Markdown格式消息"""
        # 基础格式化
        message = f"*{notification.title}*\n\n"
        
        if notification.content:
            message += f"{notification.content}\n\n"
        
        if notification.url:
            message += f"🔗 [查看详情]({notification.url})\n"
        
        # 添加时间戳
        time_str = notification.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        message += f"⏰ _{time_str}_"
        
        # 添加紧急程度标识
        if notification.urgency == "critical":
            message = "🔥 *紧急通知*\n\n" + message
        elif notification.urgency == "high":
            message = "🚨 *重要通知*\n\n" + message
        elif notification.urgency == "low":
            message = "📌 通知\n\n" + message
        
        return message.strip()
    
    def _format_markdown_v2(self, notification: Notification) -> str:
        """MarkdownV2格式消息（需要特殊转义）"""
        # 转义特殊字符
        title = self._escape_markdown_v2(notification.title)
        content = self._escape_markdown_v2(notification.content) if notification.content else ""
        
        # 基础格式化
        message = f"\\*{title}\\*\n\n"
        
        if content:
            message += f"{content}\n\n"
        
        if notification.url:
            url = self._escape_markdown_v2(notification.url)
            message += f"🔗 [查看详情]({url})\n"
        
        # 添加时间戳
        time_str = notification.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        message += f"⏰ _{time_str}_"
        
        # 添加紧急程度标识
        if notification.urgency == "critical":
            message = "🔥 \\*紧急通知\\*\n\n" + message
        elif notification.urgency == "high":
            message = "🚨 \\*重要通知\\*\n\n" + message
        elif notification.urgency == "low":
            message = "📌 通知\n\n" + message
        
        return message.strip()
    
    def _escape_html(self, text: str) -> str:
        """转义HTML特殊字符"""
        if not text:
            return ""
        
        return (text.replace("&", "&amp;")
                   .replace("<", "&lt;")
                   .replace(">", "&gt;")
                   .replace('"', "&quot;")
                   .replace("'", "&#39;"))
    
    def _escape_markdown_v2(self, text: str) -> str:
        """转义MarkdownV2特殊字符"""
        if not text:
            return ""
        
        # MarkdownV2需要转义的字符
        special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        
        for char in special_chars:
            text = text.replace(char, f"\\{char}")
        
        return text
    
    async def get_bot_info(self) -> Optional[Dict[str, Any]]:
        """
        获取Bot信息
        
        Returns:
            Bot信息，失败返回None
        """
        if not self.is_configured:
            return None
        
        try:
            url = f"{self.api_base_url}/bot{self.bot_token}/getMe"
            
            timeout = aiohttp.ClientTimeout(total=10)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    response_data = await response.json()
                    
                    if response_data.get("ok", False):
                        result = response_data.get("result", {})
                        return {
                            "id": result.get("id"),
                            "is_bot": result.get("is_bot"),
                            "first_name": result.get("first_name"),
                            "username": result.get("username"),
                            "can_join_groups": result.get("can_join_groups"),
                            "can_read_all_group_messages": result.get("can_read_all_group_messages"),
                            "supports_inline_queries": result.get("supports_inline_queries")
                        }
                    else:
                        return None
                        
        except Exception as e:
            self.logger.error(f"获取Bot信息失败: {e}")
            return None
    
    async def get_chat_info(self) -> Optional[Dict[str, Any]]:
        """
        获取聊天信息
        
        Returns:
            聊天信息，失败返回None
        """
        if not self.is_configured:
            return None
        
        try:
            url = f"{self.api_base_url}/bot{self.bot_token}/getChat"
            payload = {"chat_id": self.chat_id}
            
            timeout = aiohttp.ClientTimeout(total=10)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, json=payload) as response:
                    response_data = await response.json()
                    
                    if response_data.get("ok", False):
                        result = response_data.get("result", {})
                        return {
                            "id": result.get("id"),
                            "type": result.get("type"),
                            "title": result.get("title"),
                            "username": result.get("username"),
                            "first_name": result.get("first_name"),
                            "last_name": result.get("last_name"),
                            "description": result.get("description")
                        }
                    else:
                        return None
                        
        except Exception as e:
            self.logger.error(f"获取聊天信息失败: {e}")
            return None
    
    async def test_connection(self) -> Dict[str, Any]:
        """
        测试Telegram连接
        
        Returns:
            测试结果
        """
        try:
            # 首先测试Bot Token
            bot_info = await self.get_bot_info()
            if not bot_info:
                return {
                    "success": False,
                    "platform": self.platform_name,
                    "error": "Bot Token无效或网络连接失败",
                    "timestamp": datetime.now().isoformat()
                }
            
            # 然后测试Chat ID
            chat_info = await self.get_chat_info()
            if not chat_info:
                return {
                    "success": False,
                    "platform": self.platform_name,
                    "error": "Chat ID无效或Bot没有访问权限",
                    "timestamp": datetime.now().isoformat(),
                    "bot_info": bot_info
                }
            
            # 最后发送测试消息
            test_result = await super().test_connection()
            test_result["bot_info"] = bot_info
            test_result["chat_info"] = chat_info
            
            return test_result
            
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
            "message_limit": "30条/秒",
            "api_limits": {
                "sendMessage": "30次/秒",
                "getUpdates": "1次/秒"
            },
            "global_limit": "每分钟最多处理30条消息",
            "platform": self.platform_name
        }
    
    def get_message_limits(self) -> Dict[str, Any]:
        """
        获取消息限制信息
        
        Returns:
            消息限制信息
        """
        return {
            "max_message_length": 4096,
            "supports_formatting": True,
            "supports_html": self.parse_mode == "HTML",
            "supports_markdown": "Markdown" in self.parse_mode,
            "supports_attachments": True,
            "supports_images": True,
            "platform": self.platform_name
        }