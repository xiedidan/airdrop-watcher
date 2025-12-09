"""
飞书Webhook推送平台集成

实现飞书Webhook消息推送服务的集成。
"""
import asyncio
import aiohttp
import logging
import os
from typing import Dict, Any, Optional
from datetime import datetime

from ..base_platform import NotificationPlatform, Notification
from ...exceptions import NotificationError


class FeishuPlatform(NotificationPlatform):
    """飞书Webhook推送平台"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化飞书平台
        
        Args:
            config: 平台配置
        """
        super().__init__("feishu", config)
        
        # Webhook配置
        self.webhook_url = None
        self.sign_secret = None  # 可选的签名密钥
        
        # 消息类型配置
        self.msg_type = "post"  # 使用富文本消息
        self.title_color = "green"  # 标题颜色
        
        # 更新配置
        self._load_config()
    
    def _load_config(self):
        """加载配置"""
        try:
            # 获取基本配置
            self.webhook_url = self.config.get("webhook_url", "")
            self.sign_secret = self.config.get("sign_secret", "")  # 可选
            
            # 获取可选配置
            self.msg_type = self.config.get("msg_type", "post")
            self.title_color = self.config.get("title_color", "green")
            
            # 检查是否配置
            self.is_configured = self.validate_config()
            
            if self.is_configured:
                self.logger.info("飞书平台配置加载完成")
            else:
                self.logger.warning("飞书平台未配置webhook_url")
                
        except Exception as e:
            self.logger.error(f"飞书配置加载失败: {e}")
            self.is_configured = False
    
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
        
        # 飞书webhook URL格式验证
        if not (self.webhook_url.startswith("https://open.feishu.cn/open-apis/bot/v2/hook/") or
                self.webhook_url.startswith("https://open.larksuite.com/open-apis/bot/v2/hook/")):
            return False
        
        # 基本URL长度检查
        if len(self.webhook_url.strip()) < 60:  # 飞书webhook URL通常较长
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
            "description": "飞书Webhook消息推送平台",
            "features": [
                "富文本消息支持",
                "卡片式消息展示",
                "多语言支持",
                "@提醒功能",
                "图片和文件支持",
                "交互式消息"
            ],
            "limits": {
                "max_message_length": 4096,
                "rate_limit": "100条/分钟",
                "supports_cards": True,
                "supports_interactive": True
            },
            "website": "https://www.feishu.cn",
            "docs": "https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create",
            "is_configured": self.is_configured,
            "config": self.get_config()
        }
    
    async def send_notification(self, notification: Notification) -> bool:
        """
        发送通知到飞书
        
        Args:
            notification: 通知消息
            
        Returns:
            是否发送成功
            
        Raises:
            NotificationError: 发送失败
        """
        if not self.is_configured:
            raise NotificationError("飞书平台未配置", platform=self.platform_name)
        
        if not self.is_enabled():
            self.logger.debug(f"飞书平台已禁用，跳过发送")
            return False
        
        try:
            self.logger.info(f"开始发送飞书通知 - 标题: {notification.title}")
            
            # 准备请求数据
            payload = self._prepare_payload(notification)
            
            # 发送请求
            success = await self._send_request(payload)
            
            # 记录结果
            if success:
                self.record_success()
                self.logger.info(f"飞书通知发送成功 - 标题: {notification.title}")
            else:
                self.record_failure()
                self.logger.warning(f"飞书通知发送失败 - 标题: {notification.title}")
            
            return success
            
        except NotificationError:
            raise
        except Exception as e:
            self.record_failure()
            self.logger.error(f"飞书通知发送异常: {e}")
            raise NotificationError(f"飞书通知发送失败: {e}", platform=self.platform_name)
    
    def _prepare_payload(self, notification: Notification) -> Dict[str, Any]:
        """
        准备API请求负载
        
        Args:
            notification: 通知消息
            
        Returns:
            API请求负载
        """
        # 根据消息类型构建不同的负载
        if self.msg_type == "text":
            return self._prepare_text_payload(notification)
        elif self.msg_type == "post":
            return self._prepare_post_payload(notification)
        elif self.msg_type == "interactive":
            return self._prepare_interactive_payload(notification)
        else:
            # 默认使用富文本消息
            return self._prepare_post_payload(notification)
    
    def _prepare_text_payload(self, notification: Notification) -> Dict[str, Any]:
        """准备文本消息负载"""
        content = self.format_message(notification)
        
        payload = {
            "msg_type": "text",
            "content": {
                "text": content
            }
        }
        
        return payload
    
    def _prepare_post_payload(self, notification: Notification) -> Dict[str, Any]:
        """准备富文本消息负载"""
        # 构建富文本内容
        post_content = {
            "title": notification.title,
            "content": [
                [
                    {
                        "tag": "text",
                        "text": notification.content
                    }
                ]
            ]
        }
        
        # 添加URL
        if notification.url:
            post_content["content"][0].append({
                "tag": "a",
                "text": "查看详情",
                "href": notification.url
            })
        
        # 添加额外数据
        if notification.extra_data:
            for key, value in notification.extra_data.items():
                if isinstance(value, (str, int, float, bool)):
                    post_content["content"].append([
                        {
                            "tag": "text",
                            "text": f"{key}: "
                        },
                        {
                            "tag": "text",
                            "text": str(value)
                        }
                    ])
        
        payload = {
            "msg_type": "post",
            "content": {
                "post": post_content
            }
        }
        
        return payload
    
    def _prepare_interactive_payload(self, notification: Notification) -> Dict[str, Any]:
        """准备交互式消息负载"""
        # 构建卡片消息
        card_content = {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": notification.title
                },
                "template": self.title_color
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": notification.content
                    }
                }
            ]
        }
        
        # 添加时间戳
        if self.include_timestamp:
            time_str = notification.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            card_content["elements"].append({
                "tag": "hr"
            })
            card_content["elements"].append({
                "tag": "note",
                "elements": [
                    {
                        "tag": "plain_text",
                        "content": f"时间: {time_str}"
                    }
                ]
            })
        
        # 添加URL按钮
        if notification.url:
            card_content["elements"].append({
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "查看详情"
                        },
                        "type": "primary",
                        "url": notification.url
                    }
                ]
            })
        
        payload = {
            "msg_type": "interactive",
            "card": card_content
        }
        
        return payload
    
    async def _send_request(self, payload: Dict[str, Any]) -> bool:
        """
        发送HTTP请求
        
        Args:
            payload: 请求负载
            
        Returns:
            是否发送成功
            
        Raises:
            NotificationError: 请求失败
        """
        try:
            timeout = aiohttp.ClientTimeout(total=30)  # 30秒超时
            
            async with aiohttp.ClientSession(timeout=timeout, trust_env=True) as session:
                headers = {
                    "Content-Type": "application/json; charset=utf-8"
                }
                
                # 如果有签名密钥，添加签名
                if self.sign_secret:
                    # 飞书需要添加签名（简化实现）
                    import time
                    import hmac
                    import hashlib
                    import base64
                    
                    timestamp = str(int(time.time()))
                    string_to_sign = f"{timestamp}\n{payload}"
                    
                    hmac_code = hmac.new(
                        self.sign_secret.encode('utf-8'),
                        string_to_sign.encode('utf-8'),
                        digestmod=hashlib.sha256
                    ).digest()
                    
                    sign = base64.b64encode(hmac_code).decode('utf-8')
                    
                    # 添加签名到payload
                    payload["timestamp"] = timestamp
                    payload["sign"] = sign
                
                async with session.post(self.webhook_url, json=payload, headers=headers) as response:
                    response_data = await response.json()
                    
                    # 检查HTTP状态码
                    if response.status != 200:
                        error_msg = self.handle_api_error(response_data, response.status)
                        raise NotificationError(error_msg, platform=self.platform_name)
                    
                    # 检查飞书返回码
                    code = response_data.get("code", -1)
                    msg = response_data.get("msg", "未知错误")
                    
                    if code == 0:
                        # 发送成功
                        data = response_data.get("data", {})
                        if data:
                            self.logger.debug(f"飞书响应数据: {data}")
                        return True
                    else:
                        # 发送失败
                        error_msg = f"飞书返回错误 (code: {code}): {msg}"
                        raise NotificationError(error_msg, platform=self.platform_name)
                        
        except aiohttp.ClientError as e:
            raise NotificationError(f"网络请求失败: {e}", platform=self.platform_name)
        except asyncio.TimeoutError:
            raise NotificationError("请求超时", platform=self.platform_name)
        except Exception as e:
            raise NotificationError(f"请求异常: {e}", platform=self.platform_name)
    
    def format_message(self, notification: Notification) -> str:
        """
        格式化消息内容（飞书专用）
        
        Args:
            notification: 通知消息
            
        Returns:
            格式化后的消息
        """
        # 使用基础格式化，然后根据消息类型进行处理
        base_message = super().format_message(notification)
        
        # 根据紧急程度添加标识
        if notification.urgency == "critical":
            base_message = "🔥 紧急通知\n\n" + base_message
        elif notification.urgency == "high":
            base_message = "🚨 重要通知\n\n" + base_message
        elif notification.urgency == "low":
            base_message = "📌 通知\n\n" + base_message
        
        return base_message.strip()
    
    def _get_color_by_urgency(self, urgency: str) -> str:
        """
        根据紧急程度获取颜色
        
        Args:
            urgency: 紧急程度
            
        Returns:
            颜色名称
        """
        color_map = {
            "critical": "red",
            "high": "orange",
            "normal": "green",
            "low": "blue"
        }
        
        return color_map.get(urgency, self.title_color)
    
    async def test_connection(self) -> Dict[str, Any]:
        """
        测试飞书连接
        
        Returns:
            测试结果
        """
        try:
            # 创建测试通知
            test_notification = Notification(
                title="WebMon连接测试",
                content="这是一条来自WebMon的连接测试消息，如果您收到此消息，说明飞书配置正确。",
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
            "rate_limit": "100条/分钟",
            "burst_limit": "5条/秒",
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
            "supports_rich_text": True,
            "supports_cards": True,
            "supports_interactive": True,
            "supports_at_mentions": True,
            "platform": self.platform_name
        }