"""
通知服务模块

提供统一的通知服务接口，管理多个推送平台。
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from .base_platform import NotificationManager, Notification
from .template_engine import TemplateEngine
from ..config import ConfigManager
from ..exceptions import NotificationError


class NotificationService:
    """通知服务类"""
    
    def __init__(self, config_manager: Optional[ConfigManager] = None):
        """
        初始化通知服务
        
        Args:
            config_manager: 配置管理器
        """
        self.config_manager = config_manager or ConfigManager()
        self.notification_manager = NotificationManager(self.config_manager)
        self.template_engine = TemplateEngine()
        self.logger = logging.getLogger(__name__)
        
        # 从配置中加载平台设置
        self._load_platform_configs()
    
    def _load_platform_configs(self):
        """从配置文件中加载平台配置"""
        try:
            notification_config = self.config_manager.get_notification_config()
            
            # 获取启用的平台
            enabled_platforms = notification_config.get('platforms', [])
            platform_configs = notification_config.get('platform_configs', {})
            
            # 为每个启用的平台加载配置
            for platform_name in enabled_platforms:
                platform_config = platform_configs.get(platform_name, {})
                if platform_config.get('enabled', False):
                    # 获取平台实例
                    platform = self.notification_manager.get_platform(platform_name)
                    if platform:
                        # 加载平台特定配置
                        self._configure_platform(platform, platform_config)
                        self.logger.info(f"已加载平台配置: {platform_name}")
                    else:
                        self.logger.warning(f"平台未找到: {platform_name}")
            
            self.logger.info(f"通知服务初始化完成，已启用平台: {enabled_platforms}")
            
        except Exception as e:
            self.logger.error(f"加载平台配置失败: {e}")
    
    def _configure_platform(self, platform, config: Dict[str, Any]):
        """配置单个平台"""
        try:
            # 提取平台特定配置（移除enabled字段）
            platform_config = {k: v for k, v in config.items() if k != 'enabled'}

            # 解析环境变量引用
            resolved_config = {}
            for key, value in platform_config.items():
                if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
                    # 从环境变量获取值
                    env_key = value[2:-1]  # 移除 ${ 和 }
                    env_value = self.config_manager.env_config.get(env_key, '')
                    resolved_config[key] = env_value
                    if env_value:
                        self.logger.debug(f"解析环境变量: {key} = {env_key}")
                    else:
                        self.logger.warning(f"环境变量 {env_key} 未设置或为空")
                else:
                    resolved_config[key] = value

            # 更新平台配置
            platform.update_config(resolved_config)

            # 启用平台
            platform.set_enabled(True)

        except Exception as e:
            self.logger.error(f"配置平台 {platform.platform_name} 失败: {e}")
            platform.set_enabled(False)
    
    async def send_notification(self, title: str, content: str, 
                              platforms: Optional[List[str]] = None,
                              urgency: str = "normal",
                              url: str = "",
                              extra_data: Optional[Dict[str, Any]] = None) -> Dict[str, bool]:
        """
        发送通知
        
        Args:
            title: 通知标题
            content: 通知内容
            platforms: 目标平台列表，如果为None则发送到所有可用平台
            urgency: 紧急程度 (low, normal, high, critical)
            url: 相关URL
            extra_data: 额外数据
            
        Returns:
            各平台发送结果
        """
        try:
            # 创建通知对象
            notification = Notification(
                title=title,
                content=content,
                url=url,
                urgency=urgency,
                extra_data=extra_data or {}
            )
            
            # 发送通知
            results = await self.notification_manager.send_notification(notification, platforms)
            
            # 记录发送结果
            success_count = sum(1 for success in results.values() if success)
            total_count = len(results)
            
            self.logger.info(f"通知发送完成 - 成功: {success_count}/{total_count}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"发送通知失败: {e}")
            raise NotificationError(f"发送通知失败: {e}")
    
    async def send_change_notification(self, task_name: str, url: str, 
                                     change_summary: str, similarity: Optional[float] = None,
                                     detection_time: Optional[float] = None,
                                     platforms: Optional[List[str]] = None) -> Dict[str, bool]:
        """
        发送变化检测通知
        
        Args:
            task_name: 任务名称
            url: 监控URL
            change_summary: 变化摘要
            similarity: 相似度（可选）
            detection_time: 检测耗时（可选）
            platforms: 目标平台列表
            
        Returns:
            各平台发送结果
        """
        try:
            # 使用模板创建消息
            message_content = self.template_engine.create_change_notification_template(
                task_name=task_name,
                url=url,
                change_summary=change_summary,
                similarity=similarity,
                detection_time=detection_time
            )
            
            # 发送通知
            results = await self.send_notification(
                title="🎯 网页变化检测通知",
                content=message_content,
                platforms=platforms,
                urgency="high",
                url=url,
                extra_data={
                    "task_name": task_name,
                    "similarity": similarity,
                    "detection_time": detection_time
                }
            )
            
            return results
            
        except Exception as e:
            self.logger.error(f"发送变化通知失败: {e}")
            raise NotificationError(f"发送变化通知失败: {e}")
    
    async def send_system_notification(self, title: str, content: str,
                                     notification_type: str = "info",
                                     platforms: Optional[List[str]] = None,
                                     details: Optional[str] = None) -> Dict[str, bool]:
        """
        发送系统通知
        
        Args:
            title: 通知标题
            content: 通知内容
            notification_type: 通知类型 (info, warning, error, success)
            platforms: 目标平台列表
            details: 详细信息（可选）
            
        Returns:
            各平台发送结果
        """
        try:
            # 使用模板创建消息
            message_content = self.template_engine.create_system_notification_template(
                title=title,
                content=content,
                notification_type=notification_type,
                details=details
            )
            
            # 确定紧急程度
            urgency_map = {
                "info": "low",
                "warning": "normal", 
                "error": "high",
                "success": "low"
            }
            urgency = urgency_map.get(notification_type, "normal")
            
            # 发送通知
            results = await self.send_notification(
                title=f"🔔 {title}",
                content=message_content,
                platforms=platforms,
                urgency=urgency,
                extra_data={
                    "type": notification_type,
                    "details": details
                }
            )
            
            return results
            
        except Exception as e:
            self.logger.error(f"发送系统通知失败: {e}")
            raise NotificationError(f"发送系统通知失败: {e}")
    
    async def test_platforms(self, platforms: Optional[List[str]] = None) -> Dict[str, Dict[str, Any]]:
        """
        测试所有平台或指定平台
        
        Args:
            platforms: 要测试的平台列表，如果为None则测试所有平台
            
        Returns:
            测试结果
        """
        try:
            self.logger.info("开始测试通知平台...")
            
            # 测试所有平台
            results = await self.notification_manager.test_all_platforms()
            
            # 过滤结果（如果只测试特定平台）
            if platforms:
                results = {name: result for name, result in results.items() if name in platforms}
            
            # 记录测试结果
            success_count = sum(1 for result in results.values() if result.get('success', False))
            total_count = len(results)
            
            self.logger.info(f"平台测试完成 - 成功: {success_count}/{total_count}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"测试平台失败: {e}")
            raise NotificationError(f"测试平台失败: {e}")
    
    def get_platform_status(self) -> Dict[str, Any]:
        """
        获取平台状态
        
        Returns:
            平台状态信息
        """
        try:
            return self.notification_manager.get_summary()
        except Exception as e:
            self.logger.error(f"获取平台状态失败: {e}")
            return {}
    
    def get_enabled_platforms(self) -> List[str]:
        """
        获取启用的平台列表
        
        Returns:
            启用的平台名称列表
        """
        return self.notification_manager.get_enabled_platforms()
    
    def get_configured_platforms(self) -> List[str]:
        """
        获取已配置的平台列表
        
        Returns:
            已配置的平台名称列表
        """
        return self.notification_manager.get_configured_platforms()
    
    def get_platform_info(self, platform_name: str) -> Optional[Dict[str, Any]]:
        """
        获取平台信息
        
        Args:
            platform_name: 平台名称
            
        Returns:
            平台信息，不存在返回None
        """
        platform = self.notification_manager.get_platform(platform_name)
        if platform:
            return platform.get_platform_info()
        return None