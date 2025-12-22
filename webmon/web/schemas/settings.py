"""
配置管理数据模型

定义系统配置相关的 Pydantic 数据模型。
"""

from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field


# ==================== 监控配置 ====================

class RateLimitConfig(BaseModel):
    """速率限制配置"""
    requests_per_minute: int = Field(30, ge=1, le=1000, description="每分钟请求数")
    retry_delay: int = Field(60, ge=1, le=3600, description="重试延迟（秒）")


class MonitoringConfig(BaseModel):
    """监控配置"""
    default_interval: int = Field(300, ge=10, le=86400, description="默认检测间隔（秒）")
    default_timeout: int = Field(30000, ge=1000, le=120000, description="默认超时时间（毫秒）")
    max_retries: int = Field(3, ge=0, le=10, description="最大重试次数")
    concurrent_tasks: int = Field(5, ge=1, le=50, description="并发任务数")
    browser_headless: bool = Field(True, description="浏览器无头模式")
    rate_limit: Optional[RateLimitConfig] = Field(None, description="速率限制配置")


class MonitoringConfigUpdate(BaseModel):
    """监控配置更新"""
    default_interval: Optional[int] = Field(None, ge=10, le=86400)
    default_timeout: Optional[int] = Field(None, ge=1000, le=120000)
    max_retries: Optional[int] = Field(None, ge=0, le=10)
    concurrent_tasks: Optional[int] = Field(None, ge=1, le=50)
    browser_headless: Optional[bool] = None
    rate_limit: Optional[RateLimitConfig] = None


# ==================== 检测配置 ====================

class DetectionConfig(BaseModel):
    """变化检测配置"""
    enable_smart_detection: bool = Field(True, description="启用智能检测")
    similarity_threshold: float = Field(0.85, ge=0.0, le=1.0, description="相似度阈值")
    min_change_length: int = Field(10, ge=1, le=1000, description="最小变化长度")
    ignore_selectors: List[str] = Field(default_factory=list, description="忽略的选择器")
    extract_fields: Dict[str, str] = Field(default_factory=dict, description="提取字段映射")


class DetectionConfigUpdate(BaseModel):
    """检测配置更新"""
    enable_smart_detection: Optional[bool] = None
    similarity_threshold: Optional[float] = Field(None, ge=0.0, le=1.0)
    min_change_length: Optional[int] = Field(None, ge=1, le=1000)
    ignore_selectors: Optional[List[str]] = None
    extract_fields: Optional[Dict[str, str]] = None


# ==================== 通知配置 ====================

class NotificationTemplate(BaseModel):
    """通知模板配置"""
    title: str = Field("网页变化检测通知", description="通知标题")
    content: str = Field(..., description="通知内容模板")
    rate_limit: int = Field(60, ge=0, le=3600, description="通知速率限制（秒）")


class PlatformConfig(BaseModel):
    """平台配置基类"""
    enabled: bool = Field(False, description="是否启用")


class PushPlusConfig(PlatformConfig):
    """PushPlus 配置"""
    token: str = Field("", description="PushPlus Token（可使用 ${PUSHPLUS_TOKEN}）")


class TelegramConfig(PlatformConfig):
    """Telegram 配置"""
    bot_token: str = Field("", description="Bot Token（可使用 ${TELEGRAM_BOT_TOKEN}）")
    chat_id: str = Field("", description="Chat ID（可使用 ${TELEGRAM_CHAT_ID}）")


class DiscordConfig(PlatformConfig):
    """Discord 配置"""
    webhook_url: str = Field("", description="Webhook URL（可使用 ${DISCORD_WEBHOOK_URL}）")


class FeishuConfig(PlatformConfig):
    """飞书配置"""
    webhook_url: str = Field("", description="Webhook URL（可使用 ${FEISHU_WEBHOOK_URL}）")


class NotificationConfig(BaseModel):
    """通知配置"""
    enabled_platforms: List[str] = Field(default_factory=list, description="启用的平台列表")
    templates: Dict[str, str] = Field(default_factory=dict, description="通知模板")
    platform_configs: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="各平台配置"
    )


class NotificationConfigUpdate(BaseModel):
    """通知配置更新"""
    enabled_platforms: Optional[List[str]] = None
    templates: Optional[Dict[str, str]] = None
    platform_configs: Optional[Dict[str, Dict[str, Any]]] = None


# ==================== AI 配置 ====================

class AIConfig(BaseModel):
    """AI 分析配置"""
    enabled: bool = Field(False, description="是否启用 AI 分析")
    api_url: str = Field("https://api.deepseek.com/v1", description="API 地址")
    api_key: str = Field("", description="API Key（可使用 ${AI_API_KEY}）")
    model: str = Field("deepseek-reasoner", description="模型名称")
    max_tokens: int = Field(2048, ge=100, le=32000, description="最大 Token 数")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="温度参数")
    timeout: int = Field(60, ge=10, le=600, description="请求超时（秒）")
    retry_attempts: int = Field(3, ge=0, le=10, description="重试次数")
    retry_base_delay: float = Field(5.0, ge=1.0, le=60.0, description="重试基础延迟（秒）")
    retry_max_delay: float = Field(60.0, ge=10.0, le=300.0, description="重试最大延迟（秒）")
    system_prompt: str = Field("", description="系统提示词")
    user_prompt_template: str = Field("", description="用户提示词模板")


class AIConfigUpdate(BaseModel):
    """AI 配置更新"""
    enabled: Optional[bool] = None
    api_url: Optional[str] = None
    api_key: Optional[str] = None
    model: Optional[str] = None
    max_tokens: Optional[int] = Field(None, ge=100, le=32000)
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    timeout: Optional[int] = Field(None, ge=10, le=600)
    retry_attempts: Optional[int] = Field(None, ge=0, le=10)
    retry_base_delay: Optional[float] = Field(None, ge=1.0, le=60.0)
    retry_max_delay: Optional[float] = Field(None, ge=10.0, le=300.0)
    system_prompt: Optional[str] = None
    user_prompt_template: Optional[str] = None


# ==================== 存储配置 ====================

class StorageConfig(BaseModel):
    """存储配置"""
    history_file: str = Field("data/history.json", description="历史记录文件路径")
    max_history_entries: int = Field(1000, ge=100, le=100000, description="最大历史记录数")
    auto_cleanup_days: int = Field(30, ge=1, le=365, description="自动清理天数")


class StorageConfigUpdate(BaseModel):
    """存储配置更新"""
    history_file: Optional[str] = None
    max_history_entries: Optional[int] = Field(None, ge=100, le=100000)
    auto_cleanup_days: Optional[int] = Field(None, ge=1, le=365)


# ==================== 日志配置 ====================

class LogRotationConfig(BaseModel):
    """日志轮转配置"""
    type: str = Field("time", description="轮转类型: time/size")
    interval: int = Field(7, ge=1, le=365, description="轮转间隔（天）")
    retention_days: int = Field(30, ge=1, le=365, description="保留天数")
    max_size: int = Field(10485760, ge=1048576, le=1073741824, description="最大文件大小（字节）")
    backup_count: int = Field(5, ge=1, le=100, description="备份文件数量")


class LogFormatConfig(BaseModel):
    """日志格式配置"""
    console: str = Field(..., description="控制台格式")
    file: str = Field(..., description="文件格式")


class LoggingConfig(BaseModel):
    """日志配置"""
    level: str = Field("INFO", description="日志级别: DEBUG/INFO/WARNING/ERROR/CRITICAL")
    log_dir: str = Field("./logs", description="日志目录")
    rotation: Optional[LogRotationConfig] = Field(None, description="轮转配置")
    format: Optional[LogFormatConfig] = Field(None, description="格式配置")
    handlers: List[str] = Field(default_factory=lambda: ["console", "file"], description="处理器列表")
    compression: bool = Field(False, description="是否压缩")
    async_mode: bool = Field(False, description="异步模式")
    buffer_size: int = Field(1000, ge=100, le=10000, description="缓冲区大小")


class LoggingConfigUpdate(BaseModel):
    """日志配置更新"""
    level: Optional[str] = None
    log_dir: Optional[str] = None
    rotation: Optional[LogRotationConfig] = None
    format: Optional[LogFormatConfig] = None
    handlers: Optional[List[str]] = None
    compression: Optional[bool] = None
    async_mode: Optional[bool] = None
    buffer_size: Optional[int] = Field(None, ge=100, le=10000)


# ==================== 调度器配置 ====================

class SchedulerPerformanceConfig(BaseModel):
    """调度器性能配置"""
    max_concurrent_tasks: int = Field(15, ge=1, le=100, description="最大并发任务数")
    max_browser_resources: int = Field(8, ge=1, le=50, description="最大浏览器资源数")
    scheduler_loop_interval: float = Field(0.2, ge=0.1, le=5.0, description="调度循环间隔（秒）")


class SchedulerRetryConfig(BaseModel):
    """调度器重试配置"""
    retry_attempts: int = Field(5, ge=0, le=20, description="重试次数")
    retry_delay: int = Field(120, ge=10, le=3600, description="重试延迟（秒）")


class SchedulerConfig(BaseModel):
    """调度器配置"""
    performance: Optional[SchedulerPerformanceConfig] = Field(None, description="性能配置")
    retry: Optional[SchedulerRetryConfig] = Field(None, description="重试配置")


class SchedulerConfigUpdate(BaseModel):
    """调度器配置更新"""
    performance: Optional[SchedulerPerformanceConfig] = None
    retry: Optional[SchedulerRetryConfig] = None


# ==================== 完整配置 ====================

class AllSettings(BaseModel):
    """所有配置"""
    monitoring: Optional[MonitoringConfig] = None
    detection: Optional[DetectionConfig] = None
    notification: Optional[NotificationConfig] = None
    ai: Optional[AIConfig] = None
    storage: Optional[StorageConfig] = None
    logging: Optional[LoggingConfig] = None
    scheduler: Optional[SchedulerConfig] = None


class SettingsResponse(BaseModel):
    """配置响应"""
    success: bool = Field(True, description="操作是否成功")
    message: str = Field("获取成功", description="响应消息")
    data: Dict[str, Any] = Field(default_factory=dict, description="配置数据")


class SettingsSectionResponse(BaseModel):
    """配置段响应"""
    success: bool = Field(True, description="操作是否成功")
    message: str = Field("获取成功", description="响应消息")
    section: str = Field(..., description="配置段名称")
    data: Dict[str, Any] = Field(default_factory=dict, description="配置数据")
