"""
PushPlus推送平台集成

实现PushPlus微信推送服务的集成。
"""
import asyncio
import aiohttp
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from ..base_platform import NotificationPlatform, Notification
from ...exceptions import NotificationError


class PushPlusPlatform(NotificationPlatform):
    """PushPlus推送平台"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化PushPlus平台
        
        Args:
            config: 平台配置
        """
        super().__init__("pushplus", config)
        
        # API配置
        self.api_base_url = "https://www.pushplus.plus"
        self.send_endpoint = "/send"
        self.token = None
        
        # 更新配置
        self._load_config()
    
    def _load_config(self):
        """加载配置"""
        try:
            # 获取token
            self.token = self.config.get("token", "")
            
            # 检查是否配置
            self.is_configured = self.validate_config()
            
            if self.is_configured:
                self.logger.info("PushPlus平台配置加载完成")
            else:
                self.logger.warning("PushPlus平台未配置token")
                
        except Exception as e:
            self.logger.error(f"PushPlus配置加载失败: {e}")
            self.is_configured = False
    
    def validate_config(self) -> bool:
        """
        验证平台配置
        
        Returns:
            配置是否有效
        """
        if not self.token:
            return False
        
        if not isinstance(self.token, str):
            return False
        
        if len(self.token.strip()) < 10:  # PushPlus token通常较长
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
            "description": "PushPlus微信推送平台",
            "features": [
                "微信消息推送",
                "支持Markdown格式",
                "支持模板消息",
                "支持群发",
                "支持自定义渠道"
            ],
            "limits": {
                "max_content_length": 2000,  # 实际限制可能更大
                "max_title_length": 100,
                "rate_limit": "免费用户200条/天"
            },
            "website": "https://www.pushplus.plus",
            "docs": "https://www.pushplus.plus/doc",
            "is_configured": self.is_configured,
            "config": self.get_config()
        }
    
    async def send_notification(self, notification: Notification) -> bool:
        """
        发送通知到PushPlus
        
        Args:
            notification: 通知消息
            
        Returns:
            是否发送成功
            
        Raises:
            NotificationError: 发送失败
        """
        if not self.is_configured:
            raise NotificationError("PushPlus平台未配置", platform=self.platform_name)
        
        if not self.is_enabled():
            self.logger.debug(f"PushPlus平台已禁用，跳过发送")
            return False
        
        try:
            self.logger.info(f"开始发送PushPlus通知 - 标题: {notification.title}")
            
            # 准备请求数据
            payload = self._prepare_payload(notification)
            
            # 发送请求
            success = await self._send_request(payload)
            
            # 记录结果
            if success:
                self.record_success()
                self.logger.info(f"PushPlus通知发送成功 - 标题: {notification.title}")
            else:
                self.record_failure()
                self.logger.warning(f"PushPlus通知发送失败 - 标题: {notification.title}")
            
            return success
            
        except NotificationError:
            raise
        except Exception as e:
            self.record_failure()
            self.logger.error(f"PushPlus通知发送异常: {e}")
            raise NotificationError(f"PushPlus通知发送失败: {e}", platform=self.platform_name)
    
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
        
        # 基础负载
        payload = {
            "token": self.token,
            "title": notification.title,
            "content": content,
            "template": "html"  # 使用HTML模板支持更好的格式
        }
        
        # 根据紧急程度设置
        if notification.urgency == "critical":
            payload["topic"] = "1"  # 高优先级
        elif notification.urgency == "high":
            payload["topic"] = "1"
        else:
            payload["topic"] = "2"  # 普通优先级
        
        # 添加WebHook（如果提供了URL）
        if notification.url:
            payload["webhook"] = notification.url
        
        # 添加额外数据
        if notification.extra_data:
            # 将额外数据合并到内容中
            extra_content = []
            for key, value in notification.extra_data.items():
                extra_content.append(f"<br><strong>{key}:</strong> {value}")
            
            if extra_content:
                payload["content"] += "".join(extra_content)
        
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
        url = f"{self.api_base_url}{self.send_endpoint}"
        
        try:
            timeout = aiohttp.ClientTimeout(total=30)  # 30秒超时
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, json=payload) as response:
                    response_data = await response.json()
                    
                    # 检查HTTP状态码
                    if response.status != 200:
                        error_msg = self.handle_api_error(response_data, response.status)
                        raise NotificationError(error_msg, platform=self.platform_name)
                    
                    # 检查PushPlus返回码
                    code = response_data.get("code", -1)
                    msg = response_data.get("msg", "未知错误")
                    
                    if code == 200:
                        # 发送成功
                        data = response_data.get("data", {})
                        if data:
                            self.logger.debug(f"PushPlus响应数据: {data}")
                        return True
                    else:
                        # 发送失败
                        error_msg = f"PushPlus返回错误 (code: {code}): {msg}"
                        raise NotificationError(error_msg, platform=self.platform_name)
                        
        except aiohttp.ClientError as e:
            raise NotificationError(f"网络请求失败: {e}", platform=self.platform_name)
        except asyncio.TimeoutError:
            raise NotificationError("请求超时", platform=self.platform_name)
        except json.JSONDecodeError:
            raise NotificationError("响应解析失败", platform=self.platform_name)
        except Exception as e:
            raise NotificationError(f"请求异常: {e}", platform=self.platform_name)
    
    def format_message(self, notification: Notification) -> str:
        """
        格式化消息内容（PushPlus专用）
        
        Args:
            notification: 通知消息
            
        Returns:
            格式化后的HTML消息
        """
        # 使用基础格式化，然后转换为HTML
        base_message = super().format_message(notification)
        
        # 转换为HTML格式
        html_message = base_message.replace("\n", "<br>")
        
        # 添加样式
        styled_message = f"""
        <div style="font-family: Arial, sans-serif; line-height: 1.6;">
            {html_message}
        </div>
        """
        
        return styled_message.strip()
    
    async def test_connection(self) -> Dict[str, Any]:
        """
        测试PushPlus连接
        
        Returns:
            测试结果
        """
        try:
            # 创建测试通知
            test_notification = Notification(
                title="WebMon连接测试",
                content="这是一条来自WebMon的连接测试消息，如果您收到此消息，说明PushPlus配置正确。",
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
                "timestamp": datetime.now().isoformat(),
                "platform_info": self.get_platform_info()
            }
    
    def get_rate_limit_info(self) -> Dict[str, Any]:
        """
        获取速率限制信息
        
        Returns:
            速率限制信息
        """
        return {
            "daily_limit": 200,  # 免费用户每日200条
            "current_usage": self.success_count + self.failure_count,
            "reset_time": "每日0点",
            "platform": self.platform_name
        }
    
    def get_message_limits(self) -> Dict[str, Any]:
        """
        获取消息限制信息
        
        Returns:
            消息限制信息
        """
        return {
            "max_title_length": 100,
            "max_content_length": 2000,
            "supports_html": True,
            "supports_markdown": True,
            "supports_attachments": False,
            "platform": self.platform_name
        }