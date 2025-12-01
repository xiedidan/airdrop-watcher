"""
配置管理器 - 管理.env和config.json配置文件
"""
import os
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union
from dotenv import load_dotenv, set_key
from .env_config import EnvConfig
from .json_config import JsonConfig
from .config_validator import ConfigValidator
from .constants import DEFAULT_CONFIG_FILE, DEFAULT_ENV_FILE
from ..exceptions import ConfigurationError
from ..utils.log_config import LogConfig


class ConfigManager:
    """配置管理器 - 统一管理所有配置"""
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            config_dir: 配置目录路径，默认为config目录
        """
        if config_dir:
            self.config_dir = Path(config_dir)
            self.env_file = self.config_dir / '.env'
            self.json_file = self.config_dir / 'config.json'
        else:
            # 使用默认路径
            self.config_dir = DEFAULT_CONFIG_FILE.parent
            self.env_file = DEFAULT_ENV_FILE
            self.json_file = DEFAULT_CONFIG_FILE
        
        # 初始化子配置管理器
        self.env_config = EnvConfig(self.env_file)
        self.json_config = JsonConfig(self.json_file)
        self.validator = ConfigValidator()
        
        # 初始化日志配置
        self._log_config = None
        
        # 加载配置
        self._load_configs()
        
        self.logger = logging.getLogger(__name__)
    
    def _load_configs(self):
        """加载所有配置文件"""
        try:
            # 加载环境变量
            if self.env_file.exists():
                self.env_config.load()
            
            # 加载JSON配置
            if self.json_file.exists():
                self.json_config.load()
            else:
                # 创建默认配置
                self._create_default_config()
                
        except Exception as e:
            raise ConfigurationError(f"加载配置失败: {e}")
    
    def _create_default_config(self):
        """创建默认配置文件"""
        default_config = {
            "version": "1.0.0",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "monitoring": {
                "default_interval": 300,
                "default_timeout": 30000,
                "max_retries": 3,
                "concurrent_tasks": 5,
                "browser_headless": True,
                "rate_limit": {
                    "requests_per_minute": 30,
                    "retry_delay": 60
                }
            },
            "detection": {
                "enable_smart_detection": True,
                "similarity_threshold": 0.85,
                "min_change_length": 10,
                "ignore_selectors": [
                    ".advertisement",
                    ".cookie-banner",
                    ".timestamp",
                    ".view-count"
                ],
                "extract_fields": {
                    "title": "title",
                    "description": "meta[name='description']",
                    "headlines": "h1, h2, h3",
                    "links": "a[href]",
                    "images": "img[src]"
                }
            },
            "notification": {
                "platforms": ["pushplus"],
                "template": {
                    "title": "🎯 网页变化检测通知",
                    "content": "📍 URL: {url}\\n⏰ 时间: {timestamp}\\n📝 变化: {summary}\\n🔗 查看: {url}",
                    "rate_limit": 60
                },
                "platform_configs": {
                    "pushplus": {
                        "enabled": True,
                        "token": "${PUSHPLUS_TOKEN}"
                    },
                    "telegram": {
                        "enabled": False,
                        "bot_token": "${TELEGRAM_BOT_TOKEN}",
                        "chat_id": "${TELEGRAM_CHAT_ID}"
                    },
                    "discord": {
                        "enabled": False,
                        "webhook_url": "${DISCORD_WEBHOOK_URL}"
                    },
                    "feishu": {
                        "enabled": False,
                        "webhook_url": "${FEISHU_WEBHOOK_URL}"
                    }
                }
            },
            "tasks": [],
            "storage": {
                "history_file": "data/history.json",
                "max_history_entries": 1000,
                "auto_cleanup_days": 30
            },
            "logging": {
                "level": "INFO",
                "log_dir": "./logs",
                "rotation": {
                    "type": "time",
                    "interval": 1,
                    "max_size": 10485760,
                    "backup_count": 5,
                    "retention_days": 30
                },
                "format": {
                    "console": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>",
                    "file": "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
                },
                "handlers": ["console", "file", "error_file"],
                "compression": true,
                "async_mode": true,
                "buffer_size": 1000
            }
        }
        
        self.json_config.data = default_config
        self.json_config.save()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值（优先从环境变量获取）
        
        Args:
            key: 配置键名
            default: 默认值
            
        Returns:
            配置值
        """
        # 优先从环境变量获取
        env_value = self.env_config.get(key)
        if env_value is not None:
            return env_value
        
        # 从JSON配置获取
        return self.json_config.get(key, default)
    
    def set(self, key: str, value: Any, config_type: str = "json") -> bool:
        """
        设置配置值
        
        Args:
            key: 配置键名
            value: 配置值
            config_type: 配置类型 ('env' 或 'json')
            
        Returns:
            是否成功
        """
        try:
            if config_type == "env":
                success = self.env_config.set(key, value)
                return success
            elif config_type == "json":
                success = self.json_config.set(key, value)
                if success:
                    # 自动保存JSON配置
                    self.json_config.save()
                return success
            else:
                raise ValueError(f"不支持的配置类型: {config_type}")
            
        except Exception as e:
            self.logger.error(f"配置更新失败: {key} = {value}, 错误: {e}")
            return False
    
    def get_monitoring_config(self) -> Dict[str, Any]:
        """获取监控配置"""
        return self.json_config.get("monitoring", {})
    
    def get_detection_config(self) -> Dict[str, Any]:
        """获取检测配置"""
        return self.json_config.get("detection", {})
    
    def get_notification_config(self) -> Dict[str, Any]:
        """获取通知配置"""
        return self.json_config.get("notification", {})
    
    def get_storage_config(self) -> Dict[str, Any]:
        """获取存储配置"""
        return self.json_config.get("storage", {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """获取日志配置"""
        return self.json_config.get("logging", {})
    
    def get_log_config(self) -> LogConfig:
        """
        获取日志配置对象
        
        Returns:
            LogConfig实例
        """
        if self._log_config is None:
            logging_config = self.get_logging_config()
            self._log_config = LogConfig(logging_config)
        return self._log_config
    
    def update_logging_config(self, logging_config: Dict[str, Any]) -> bool:
        """
        更新日志配置
        
        Args:
            logging_config: 日志配置
            
        Returns:
            是否成功
        """
        try:
            # 验证日志配置
            if not self.validator.validate_logging_config(logging_config):
                return False
            
            # 更新配置
            self.json_config.set("logging", logging_config)
            self.json_config.save()
            
            # 更新内存中的日志配置对象
            if self._log_config:
                self._log_config.update_config(logging_config)
            
            self.logger.info("日志配置已更新")
            return True
            
        except Exception as e:
            self.logger.error(f"更新日志配置失败: {e}")
            return False
    
    def get_logging_config_value(self, key: str, default: Any = None) -> Any:
        """
        获取日志配置值
        
        Args:
            key: 配置键名，支持点号分隔 (如 "rotation.backup_count")
            default: 默认值
            
        Returns:
            配置值
        """
        logging_config = self.get_logging_config()
        
        # 支持点号分隔的键名
        keys = key.split('.')
        value = logging_config
        
        try:
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            return value
        except (KeyError, TypeError):
            return default
    
    def set_log_level(self, level: str) -> bool:
        """
        设置日志级别
        
        Args:
            level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            
        Returns:
            是否成功
        """
        try:
            valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            if level.upper() not in valid_levels:
                self.logger.error(f"无效的日志级别: {level}")
                return False
            
            # 获取当前日志配置
            logging_config = self.get_logging_config()
            logging_config["level"] = level.upper()
            
            # 更新配置
            return self.update_logging_config(logging_config)
            
        except Exception as e:
            self.logger.error(f"设置日志级别失败: {e}")
            return False
    
    def set_log_directory(self, log_dir: str) -> bool:
        """
        设置日志目录
        
        Args:
            log_dir: 日志目录路径
            
        Returns:
            是否成功
        """
        try:
            # 验证路径
            from pathlib import Path
            log_path = Path(log_dir)
            
            # 创建目录（如果不存在）
            log_path.mkdir(parents=True, exist_ok=True)
            
            # 获取当前日志配置
            logging_config = self.get_logging_config()
            logging_config["log_dir"] = str(log_path.absolute())
            
            # 更新配置
            return self.update_logging_config(logging_config)
            
        except Exception as e:
            self.logger.error(f"设置日志目录失败: {e}")
            return False
    
    def configure_log_rotation(self, rotation_type: str = "time", **kwargs) -> bool:
        """
        配置日志轮转
        
        Args:
            rotation_type: 轮转类型 ("time" 或 "size")
            **kwargs: 其他轮转参数
            
        Returns:
            是否成功
        """
        try:
            if rotation_type not in ["time", "size"]:
                self.logger.error(f"无效的轮转类型: {rotation_type}")
                return False
            
            # 获取当前日志配置
            logging_config = self.get_logging_config()
            
            # 更新轮转配置
            rotation_config = logging_config.get("rotation", {})
            rotation_config["type"] = rotation_type
            
            # 根据轮转类型设置参数
            if rotation_type == "time":
                if "interval" in kwargs:
                    rotation_config["interval"] = kwargs["interval"]
                if "retention_days" in kwargs:
                    rotation_config["retention_days"] = kwargs["retention_days"]
            else:  # size
                if "max_size" in kwargs:
                    rotation_config["max_size"] = kwargs["max_size"]
                if "backup_count" in kwargs:
                    rotation_config["backup_count"] = kwargs["backup_count"]
            
            logging_config["rotation"] = rotation_config
            
            # 更新配置
            return self.update_logging_config(logging_config)
            
        except Exception as e:
            self.logger.error(f"配置日志轮转失败: {e}")
            return False
    
    def add_log_handler(self, handler_type: str) -> bool:
        """
        添加日志处理器
        
        Args:
            handler_type: 处理器类型 ("console", "file", "error_file")
            
        Returns:
            是否成功
        """
        try:
            valid_handlers = ["console", "file", "error_file"]
            if handler_type not in valid_handlers:
                self.logger.error(f"无效的处理器类型: {handler_type}")
                return False
            
            # 获取当前日志配置
            logging_config = self.get_logging_config()
            handlers = logging_config.get("handlers", [])
            
            # 添加处理器（如果不存在）
            if handler_type not in handlers:
                handlers.append(handler_type)
                logging_config["handlers"] = handlers
                
                # 更新配置
                return self.update_logging_config(logging_config)
            
            return True
            
        except Exception as e:
            self.logger.error(f"添加日志处理器失败: {e}")
            return False
    
    def remove_log_handler(self, handler_type: str) -> bool:
        """
        移除日志处理器
        
        Args:
            handler_type: 处理器类型
            
        Returns:
            是否成功
        """
        try:
            # 获取当前日志配置
            logging_config = self.get_logging_config()
            handlers = logging_config.get("handlers", [])
            
            # 移除处理器
            if handler_type in handlers:
                handlers.remove(handler_type)
                logging_config["handlers"] = handlers
                
                # 更新配置
                return self.update_logging_config(logging_config)
            
            return True
            
        except Exception as e:
            self.logger.error(f"移除日志处理器失败: {e}")
            return False
    
    def enable_log_compression(self, enabled: bool = True) -> bool:
        """
        启用/禁用日志压缩
        
        Args:
            enabled: 是否启用压缩
            
        Returns:
            是否成功
        """
        try:
            # 获取当前日志配置
            logging_config = self.get_logging_config()
            logging_config["compression"] = enabled
            
            # 更新配置
            return self.update_logging_config(logging_config)
            
        except Exception as e:
            self.logger.error(f"设置日志压缩失败: {e}")
            return False
    
    def enable_async_logging(self, enabled: bool = True) -> bool:
        """
        启用/禁用异步日志
        
        Args:
            enabled: 是否启用异步模式
            
        Returns:
            是否成功
        """
        try:
            # 获取当前日志配置
            logging_config = self.get_logging_config()
            logging_config["async_mode"] = enabled
            
            # 更新配置
            return self.update_logging_config(logging_config)
            
        except Exception as e:
            self.logger.error(f"设置异步日志失败: {e}")
            return False
    
    def set_buffer_size(self, size: int) -> bool:
        """
        设置日志缓冲区大小
        
        Args:
            size: 缓冲区大小
            
        Returns:
            是否成功
        """
        try:
            if not isinstance(size, int) or size <= 0:
                self.logger.error("缓冲区大小必须是正整数")
                return False
            
            # 获取当前日志配置
            logging_config = self.get_logging_config()
            logging_config["buffer_size"] = size
            
            # 更新配置
            return self.update_logging_config(logging_config)
            
        except Exception as e:
            self.logger.error(f"设置缓冲区大小失败: {e}")
            return False
    
    def get_log_file_paths(self) -> Dict[str, str]:
        """
        获取日志文件路径
        
        Returns:
            日志文件路径字典
        """
        try:
            log_config = self.get_log_config()
            return log_config.get_log_file_paths()
        except Exception as e:
            self.logger.error(f"获取日志文件路径失败: {e}")
            return {}
    
    def estimate_log_size(self, tasks_per_day: int = 100, avg_log_size: int = 200) -> Dict[str, Any]:
        """
        估计日志大小
        
        Args:
            tasks_per_day: 每日任务数
            avg_log_size: 平均日志大小（字节）
            
        Returns:
            日志大小估计信息
        """
        try:
            log_config = self.get_log_config()
            return log_config.estimate_log_size(tasks_per_day, avg_log_size)
        except Exception as e:
            self.logger.error(f"估计日志大小失败: {e}")
            return {"error": str(e)}
    
    def reset_logging_config(self) -> bool:
        """
        重置日志配置为默认值
        
        Returns:
            是否成功
        """
        try:
            # 获取默认日志配置
            from ..utils.log_config import LogConfig
            default_config = LogConfig.DEFAULT_CONFIG.copy()
            
            # 更新配置
            return self.update_logging_config(default_config)
            
        except Exception as e:
            self.logger.error(f"重置日志配置失败: {e}")
            return False
    
    def get_scheduler_config(self) -> Dict[str, Any]:
        """获取调度器配置"""
        return self.json_config.get("scheduler", {})
    
    def update_scheduler_config(self, scheduler_config: Dict[str, Any]) -> bool:
        """
        更新调度器配置
        
        Args:
            scheduler_config: 调度器配置
            
        Returns:
            是否成功
        """
        try:
            # 验证调度器配置
            if not self.validator.validate_scheduler_config(scheduler_config):
                return False
            
            # 更新配置
            self.json_config.set("scheduler", scheduler_config)
            self.json_config.save()
            
            self.logger.info("调度器配置已更新")
            return True
            
        except Exception as e:
            self.logger.error(f"更新调度器配置失败: {e}")
            return False
    
    def get_scheduler_config_value(self, key: str, default: Any = None) -> Any:
        """
        获取调度器配置值
        
        Args:
            key: 配置键名，支持点号分隔 (如 "performance.max_concurrent_tasks")
            default: 默认值
            
        Returns:
            配置值
        """
        scheduler_config = self.get_scheduler_config()
        
        # 支持点号分隔的键名
        keys = key.split('.')
        value = scheduler_config
        
        try:
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            return value
        except (KeyError, TypeError):
            return default
    
    def get_task_config(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取特定任务配置"""
        tasks = self.json_config.get("tasks", [])
        for task in tasks:
            if task.get("id") == task_id:
                return task
        return None
    
    def add_task(self, task_config: Dict[str, Any]) -> bool:
        """
        添加任务配置
        
        Args:
            task_config: 任务配置
            
        Returns:
            是否成功
        """
        try:
            # 验证任务配置
            if not self.validator.validate_task_config(task_config):
                return False
            
            # 获取现有任务
            tasks = self.json_config.get("tasks", [])
            
            # 检查任务是否已存在
            task_id = task_config.get("id")
            if task_id and self.get_task_config(task_id):
                self.logger.warning(f"任务已存在: {task_id}")
                return False
            
            # 添加新任务
            tasks.append(task_config)
            self.json_config.set("tasks", tasks)
            self.json_config.save()  # 保存更改
            
            self.logger.info(f"任务已添加: {task_config.get('name', task_id)}")
            return True
            
        except Exception as e:
            self.logger.error(f"添加任务失败: {e}")
            return False
    
    def remove_task(self, task_id: str) -> bool:
        """
        删除任务配置
        
        Args:
            task_id: 任务ID
            
        Returns:
            是否成功
        """
        try:
            tasks = self.json_config.get("tasks", [])
            
            # 查找并删除任务
            for i, task in enumerate(tasks):
                if task.get("id") == task_id:
                    removed_task = tasks.pop(i)
                    self.json_config.set("tasks", tasks)
                    self.json_config.save()  # 保存更改
                    
                    self.logger.info(f"任务已删除: {removed_task.get('name', task_id)}")
                    return True
            
            self.logger.warning(f"任务未找到: {task_id}")
            return False
            
        except Exception as e:
            self.logger.error(f"删除任务失败: {e}")
            return False
    
    def update_task(self, task_id: str, updates: Dict[str, Any]) -> bool:
        """
        更新任务配置
        
        Args:
            task_id: 任务ID
            updates: 更新内容
            
        Returns:
            是否成功
        """
        try:
            tasks = self.json_config.get("tasks", [])
            
            # 查找并更新任务
            for i, task in enumerate(tasks):
                if task.get("id") == task_id:
                    # 验证更新内容
                    if not self.validator.validate_task_config({**task, **updates}):
                        return False
                    
                    # 更新任务
                    tasks[i].update(updates)
                    tasks[i]["updated_at"] = self._get_current_timestamp()
                    
                    self.json_config.set("tasks", tasks)
                    self.json_config.save()  # 保存更改
                    
                    self.logger.info(f"任务已更新: {task_id}")
                    return True
            
            self.logger.warning(f"任务未找到: {task_id}")
            return False
            
        except Exception as e:
            self.logger.error(f"更新任务失败: {e}")
            return False
    
    def list_tasks(self) -> list:
        """获取所有任务配置"""
        return self.json_config.get("tasks", [])
    
    def validate_config(self) -> bool:
        """
        验证所有配置
        
        Returns:
            是否有效
        """
        try:
            # 验证JSON配置
            if not self.validator.validate_json_config(self.json_config.data):
                return False
            
            # 验证环境变量配置
            if not self.validator.validate_env_config(self.env_config.data):
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"配置验证失败: {e}")
            return False
    
    def backup_config(self, backup_dir: Optional[str] = None) -> bool:
        """
        备份配置文件
        
        Args:
            backup_dir: 备份目录
            
        Returns:
            是否成功
        """
        try:
            if not backup_dir:
                backup_dir = self.config_dir / "backup"
            
            backup_path = Path(backup_dir)
            backup_path.mkdir(exist_ok=True)
            
            # 备份JSON配置
            if self.json_file.exists():
                backup_json = backup_path / f"config_{self._get_timestamp()}.json"
                backup_json.write_text(self.json_file.read_text())
            
            # 备份环境变量配置
            if self.env_file.exists():
                backup_env = backup_path / f"env_{self._get_timestamp()}.env"
                backup_env.write_text(self.env_file.read_text())
            
            self.logger.info(f"配置已备份到: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"备份配置失败: {e}")
            return False
    
    def reset_config(self) -> bool:
        """
        重置为默认配置
        
        Returns:
            是否成功
        """
        try:
            # 先备份当前配置
            self.backup_config()
            
            # 重置JSON配置
            self._create_default_config()
            
            # 重置环境变量配置
            if self.env_file.exists():
                self.env_file.rename(self.env_file.with_suffix('.env.backup'))
            
            self.logger.info("配置已重置为默认值")
            return True
            
        except Exception as e:
            self.logger.error(f"重置配置失败: {e}")
            return False
    
    def _get_current_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _get_timestamp(self) -> str:
        """获取时间戳字符串"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")