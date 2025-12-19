"""
推送平台基础模块

定义推送平台的抽象接口和基础实现。
"""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime

from ..exceptions import NotificationError


class Notification:
    """通知消息数据模型"""
    
    def __init__(self, title: str = "", content: str = "", url: str = "", 
                 timestamp: Optional[datetime] = None, urgency: str = "normal",
                 extra_data: Optional[Dict[str, Any]] = None):
        """
        初始化通知消息
        
        Args:
            title: 消息标题
            content: 消息内容
            url: 相关URL
            timestamp: 时间戳
            urgency: 紧急程度（low, normal, high, critical）
            extra_data: 额外数据
        """
        self.title = title
        self.content = content
        self.url = url
        self.timestamp = timestamp or datetime.now()
        self.urgency = urgency
        self.extra_data = extra_data or {}
        
        # 验证紧急程度
        valid_urgencies = ["low", "normal", "high", "critical"]
        if urgency not in valid_urgencies:
            self.urgency = "normal"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "title": self.title,
            "content": self.content,
            "url": self.url,
            "timestamp": self.timestamp.isoformat(),
            "urgency": self.urgency,
            "extra_data": self.extra_data
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Notification':
        """从字典创建通知对象"""
        if "timestamp" in data and isinstance(data["timestamp"], str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        
        return cls(**data)
    
    def get_summary(self, max_length: int = 100) -> str:
        """
        获取消息摘要
        
        Args:
            max_length: 最大长度
            
        Returns:
            消息摘要
        """
        content = self.content.strip()
        if len(content) > max_length:
            content = content[:max_length] + "..."
        
        summary = f"{self.title}\n{content}"
        if self.url:
            summary += f"\n{self.url}"
        
        return summary


class NotificationPlatform(ABC):
    """推送平台抽象基类"""
    
    def __init__(self, platform_name: str, config: Optional[Dict[str, Any]] = None):
        """
        初始化推送平台
        
        Args:
            platform_name: 平台名称
            config: 平台配置
        """
        self.platform_name = platform_name
        self.config = config or {}
        self.enabled = True
        self.logger = logging.getLogger(__name__)
        
        # 平台状态
        self.is_configured = False
        self.last_used = None
        self.success_count = 0
        self.failure_count = 0
    
    @abstractmethod
    async def send_notification(self, notification: Notification) -> bool:
        """
        发送通知
        
        Args:
            notification: 通知消息
            
        Returns:
            是否发送成功
            
        Raises:
            NotificationError: 发送失败
        """
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """
        验证平台配置
        
        Returns:
            配置是否有效
        """
        pass
    
    @abstractmethod
    def get_platform_info(self) -> Dict[str, Any]:
        """
        获取平台信息
        
        Returns:
            平台信息字典
        """
        pass
    
    def is_enabled(self) -> bool:
        """
        检查平台是否启用
        
        Returns:
            是否启用
        """
        return self.enabled
    
    def set_enabled(self, enabled: bool):
        """
        设置平台启用状态
        
        Args:
            enabled: 是否启用
        """
        self.enabled = enabled
    
    def update_config(self, config: Dict[str, Any]):
        """
        更新平台配置
        
        Args:
            config: 新配置
        """
        self.config.update(config)
        self.is_configured = self.validate_config()
    
    def get_config(self) -> Dict[str, Any]:
        """
        获取平台配置
        
        Returns:
            当前配置（去除敏感信息）
        """
        # 移除敏感信息
        safe_config = self.config.copy()
        sensitive_keys = ["token", "api_key", "secret", "password", "webhook_url"]
        
        for key in sensitive_keys:
            if key in safe_config:
                value = safe_config[key]
                if value and len(str(value)) > 8:
                    # 只显示前后4个字符
                    safe_config[key] = f"{str(value)[:4]}...{str(value)[-4:]}"
                else:
                    safe_config[key] = "***"
        
        return safe_config
    
    def record_success(self):
        """记录发送成功"""
        self.success_count += 1
        self.last_used = datetime.now()
    
    def record_failure(self):
        """记录发送失败"""
        self.failure_count += 1
        self.last_used = datetime.now()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        获取平台统计信息
        
        Returns:
            统计信息字典
        """
        total_attempts = self.success_count + self.failure_count
        success_rate = self.success_count / total_attempts if total_attempts > 0 else 0.0
        
        return {
            "platform_name": self.platform_name,
            "enabled": self.enabled,
            "is_configured": self.is_configured,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "success_rate": round(success_rate, 4),
            "total_attempts": total_attempts,
            "last_used": self.last_used.isoformat() if self.last_used else None
        }
    
    def reset_stats(self):
        """重置统计信息"""
        self.success_count = 0
        self.failure_count = 0
        self.last_used = None
    
    def format_message(self, notification: Notification) -> str:
        """
        格式化消息内容
        
        Args:
            notification: 通知消息
            
        Returns:
            格式化后的消息
        """
        # 基础格式化
        message = f"🎯 {notification.title}\n\n"
        
        if notification.content:
            message += f"{notification.content}\n\n"
        
        if notification.url:
            message += f"🔗 查看: {notification.url}\n"
        
        # 添加时间戳
        message += f"⏰ 时间: {notification.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        
        # 添加紧急程度标识
        if notification.urgency == "high":
            message = "🚨 重要通知\n\n" + message
        elif notification.urgency == "critical":
            message = "🔥 紧急通知\n\n" + message
        elif notification.urgency == "low":
            message = "📌 通知\n\n" + message
        
        return message
    
    def create_api_payload(self, notification: Notification) -> Dict[str, Any]:
        """
        创建API请求负载
        
        Args:
            notification: 通知消息
            
        Returns:
            API请求负载
        """
        # 基础负载结构
        payload = {
            "title": notification.title,
            "content": notification.content,
            "url": notification.url,
            "timestamp": notification.timestamp.isoformat(),
            "urgency": notification.urgency
        }
        
        # 添加额外数据
        if notification.extra_data:
            payload.update(notification.extra_data)
        
        return payload
    
    def handle_api_error(self, response_data: Dict[str, Any], status_code: int) -> str:
        """
        处理API错误响应
        
        Args:
            response_data: 响应数据
            status_code: HTTP状态码
            
        Returns:
            错误信息
        """
        error_msg = f"API请求失败 (状态码: {status_code})"
        
        if response_data:
            # 尝试从响应中提取错误信息
            if "error" in response_data:
                error_msg += f": {response_data['error']}"
            elif "message" in response_data:
                error_msg += f": {response_data['message']}"
            elif "msg" in response_data:
                error_msg += f": {response_data['msg']}"
        
        return error_msg
    
    def test_connection(self) -> Dict[str, Any]:
        """
        测试平台连接
        
        Returns:
            测试结果
        """
        try:
            # 创建测试通知
            test_notification = Notification(
                title="连接测试",
                content="这是来自WebMon的连接测试消息",
                urgency="low"
            )
            
            # 尝试发送测试消息
            success = self.send_notification(test_notification)
            
            return {
                "success": success,
                "platform": self.platform_name,
                "message": "连接测试成功" if success else "连接测试失败",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "platform": self.platform_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


class NotificationManager:
    """通知管理器"""
    
    def __init__(self, config_manager):
        """
        初始化通知管理器
        
        Args:
            config_manager: 配置管理器
        """
        self.config_manager = config_manager
        self.platforms: Dict[str, NotificationPlatform] = {}
        self.logger = logging.getLogger(__name__)
        
        # 初始化内置平台
        self._initialize_builtin_platforms()
    
    def _initialize_builtin_platforms(self):
        """初始化内置推送平台"""
        try:
            from .platforms.pushplus_platform import PushPlusPlatform
            from .platforms.telegram_platform import TelegramPlatform
            from .platforms.discord_platform import DiscordPlatform
            from .platforms.feishu_platform import FeishuPlatform
            
            # 注册内置平台
            self.register_platform("pushplus", PushPlusPlatform())
            self.register_platform("telegram", TelegramPlatform())
            self.register_platform("discord", DiscordPlatform())
            self.register_platform("feishu", FeishuPlatform())
            
            self.logger.info("内置推送平台初始化完成")
            
        except ImportError as e:
            self.logger.warning(f"部分推送平台导入失败: {e}")
        except Exception as e:
            self.logger.error(f"初始化内置平台失败: {e}")
    
    def register_platform(self, name: str, platform: NotificationPlatform):
        """
        注册推送平台
        
        Args:
            name: 平台名称
            platform: 平台实例
        """
        self.platforms[name] = platform
        self.logger.info(f"推送平台已注册: {name}")
    
    def unregister_platform(self, name: str):
        """
        注销推送平台
        
        Args:
            name: 平台名称
        """
        if name in self.platforms:
            del self.platforms[name]
            self.logger.info(f"推送平台已注销: {name}")
    
    async def send_notification(self, notification: Notification, 
                              platforms: Optional[List[str]] = None) -> Dict[str, bool]:
        """
        发送通知到指定平台
        
        Args:
            notification: 通知消息
            platforms: 目标平台列表，如果为None则发送到所有可用平台
            
        Returns:
            各平台发送结果
        """
        if not platforms:
            platforms = list(self.platforms.keys())
        
        results = {}
        
        for platform_name in platforms:
            platform = self.platforms.get(platform_name)
            if not platform:
                results[platform_name] = False
                self.logger.warning(f"推送平台不存在: {platform_name}")
                continue
            
            if not platform.is_enabled():
                results[platform_name] = False
                self.logger.debug(f"推送平台已禁用: {platform_name}")
                continue

            if not platform.is_configured:
                results[platform_name] = False
                self.logger.info(f"推送平台未配置: {platform_name}")
                continue

            try:
                success = await platform.send_notification(notification)
                results[platform_name] = success
                
                if success:
                    self.logger.info(f"通知发送成功 - 平台: {platform_name}")
                else:
                    self.logger.warning(f"通知发送失败 - 平台: {platform_name}")
                    
            except Exception as e:
                results[platform_name] = False
                self.logger.error(f"通知发送异常 - 平台: {platform_name}: {e}")
        
        return results
    
    def get_platform(self, name: str) -> Optional[NotificationPlatform]:
        """
        获取推送平台
        
        Args:
            name: 平台名称
            
        Returns:
            平台实例，不存在返回None
        """
        return self.platforms.get(name)
    
    def get_enabled_platforms(self) -> List[str]:
        """
        获取启用的平台列表
        
        Returns:
            启用的平台名称列表
        """
        return [name for name, platform in self.platforms.items() 
                if platform.is_enabled()]
    
    def get_configured_platforms(self) -> List[str]:
        """
        获取已配置的平台列表
        
        Returns:
            已配置的平台名称列表
        """
        return [name for name, platform in self.platforms.items() 
                if platform.is_configured and platform.is_enabled()]
    
    def get_all_platforms(self) -> Dict[str, NotificationPlatform]:
        """
        获取所有平台
        
        Returns:
            所有平台字典
        """
        return self.platforms.copy()
    
    def get_platform_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        获取所有平台的统计信息
        
        Returns:
            平台统计信息字典
        """
        stats = {}
        for name, platform in self.platforms.items():
            stats[name] = platform.get_stats()
        return stats
    
    def create_notification_from_change(self, change_result: Dict[str, Any], 
                                      task_info: Dict[str, Any]) -> Notification:
        """
        根据变化检测结果创建通知
        
        Args:
            change_result: 变化检测结果
            task_info: 任务信息
            
        Returns:
            通知消息
        """
        try:
            # 构建通知标题
            title = f"🎯 网页变化检测通知"
            
            # 构建通知内容
            content_parts = []
            
            # 基本信息
            task_name = task_info.get("name", "未知任务")
            url = task_info.get("url", "")
            content_parts.append(f"📍 任务: {task_name}")
            if url:
                content_parts.append(f"🔗 URL: {url}")
            
            # 变化信息
            if change_result.get("changed", False):
                content_parts.append(f"📝 检测到内容变化")
                
                # 相似度信息
                if "similarity" in change_result:
                    similarity = change_result["similarity"]
                    content_parts.append(f"📊 相似度: {similarity:.1%}")
                
                # 变化摘要
                if "change_summary" in change_result:
                    content_parts.append(f"📋 变化: {change_result['change_summary']}")
                
                # 字段变化
                if "field_changes" in change_result:
                    field_changes = change_result["field_changes"]
                    if field_changes:
                        content_parts.append(f"🔍 字段变化: {len(field_changes)} 个")
            else:
                content_parts.append(f"✅ 未检测到显著变化")
            
            # 检测时间
            if "detection_time" in change_result:
                detection_time = change_result["detection_time"]
                content_parts.append(f"⏱️ 检测耗时: {detection_time:.3f}秒")
            
            content = "\n".join(content_parts)
            
            # 确定紧急程度
            urgency = "normal"
            if change_result.get("changed", False):
                urgency = "high"
            
            # 创建通知
            notification = Notification(
                title=title,
                content=content,
                url=url,
                urgency=urgency,
                extra_data={
                    "task_id": task_info.get("id"),
                    "change_type": change_result.get("change_type"),
                    "similarity": change_result.get("similarity"),
                    "algorithm": change_result.get("algorithm")
                }
            )
            
            return notification
            
        except Exception as e:
            self.logger.error(f"创建通知失败: {e}")
            # 创建错误通知
            return Notification(
                title="❌ 变化检测通知创建失败",
                content=f"无法创建变化检测通知: {e}",
                urgency="high"
            )
    
    async def test_all_platforms(self) -> Dict[str, Dict[str, Any]]:
        """
        测试所有平台
        
        Returns:
            各平台测试结果
        """
        results = {}
        
        for name, platform in self.platforms.items():
            try:
                result = await platform.test_connection()
                results[name] = result
            except Exception as e:
                results[name] = {
                    "success": False,
                    "platform": name,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
        
        return results
    
    def reset_all_stats(self):
        """重置所有平台的统计信息"""
        for platform in self.platforms.values():
            platform.reset_stats()
        self.logger.info("所有平台统计信息已重置")
    
    def get_summary(self) -> Dict[str, Any]:
        """
        获取通知管理器摘要
        
        Returns:
            摘要信息
        """
        total_platforms = len(self.platforms)
        enabled_platforms = len(self.get_enabled_platforms())
        configured_platforms = len(self.get_configured_platforms())
        
        total_success = sum(p.success_count for p in self.platforms.values())
        total_failure = sum(p.failure_count for p in self.platforms.values())
        total_attempts = total_success + total_failure
        
        overall_success_rate = total_success / total_attempts if total_attempts > 0 else 0.0
        
        return {
            "total_platforms": total_platforms,
            "enabled_platforms": enabled_platforms,
            "configured_platforms": configured_platforms,
            "total_success": total_success,
            "total_failure": total_failure,
            "total_attempts": total_attempts,
            "overall_success_rate": round(overall_success_rate, 4),
            "platforms_summary": self.get_platform_stats()
        }