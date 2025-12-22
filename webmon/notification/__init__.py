"""
通知推送模块

提供多平台消息推送功能和消息模板系统。
"""

from .base_platform import Notification, NotificationPlatform, NotificationManager
from .template_engine import TemplateEngine, MessageTemplate, SimpleTemplateEngine, AdvancedTemplateEngine
from .service import NotificationService

__all__ = [
    'Notification',
    'NotificationPlatform',
    'NotificationManager',
    'TemplateEngine',
    'MessageTemplate',
    'SimpleTemplateEngine',
    'AdvancedTemplateEngine',
    'NotificationService',
]

# 版本信息
__version__ = '1.0.0'