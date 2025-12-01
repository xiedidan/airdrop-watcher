#!/usr/bin/env python3
"""
日志配置管理
管理日志相关的配置参数和设置
"""

from typing import Dict, Any, Optional
from pathlib import Path


class LogConfig:
    """日志配置管理器"""
    
    # 默认配置常量
    DEFAULT_CONFIG = {
        "level": "INFO",
        "log_dir": "./logs",
        "rotation": {
            "type": "time",  # "time" 或 "size"
            "interval": 1,   # 时间轮转间隔(天)
            "max_size": 10 * 1024 * 1024,  # 10MB
            "backup_count": 5,
            "retention_days": 30
        },
        "format": {
            "console": (
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                "<level>{message}</level>"
            ),
            "file": (
                "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
                "{name}:{function}:{line} - {message}"
            )
        },
        "handlers": ["console", "file", "error_file"],
        "compression": True,
        "async_mode": True,
        "buffer_size": 1000
    }
    
    def __init__(self, config_data: Optional[Dict[str, Any]] = None):
        """初始化日志配置"""
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_data:
            self.update_config(config_data)
    
    def update_config(self, new_config: Dict[str, Any]):
        """更新日志配置"""
        def deep_update(base_dict: Dict, update_dict: Dict):
            """深度更新字典"""
            for key, value in update_dict.items():
                if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                    deep_update(base_dict[key], value)
                else:
                    base_dict[key] = value
        
        deep_update(self.config, new_config)
    
    def get_level(self) -> str:
        """获取日志级别"""
        return self.config.get("level", "INFO")
    
    def get_log_dir(self) -> str:
        """获取日志目录"""
        return self.config.get("log_dir", "./logs")
    
    def get_rotation_config(self) -> Dict[str, Any]:
        """获取轮转配置"""
        return self.config.get("rotation", {})
    
    def get_rotation_type(self) -> str:
        """获取轮转类型"""
        return self.get_rotation_config().get("type", "time")
    
    def get_max_size(self) -> int:
        """获取最大文件大小"""
        return self.get_rotation_config().get("max_size", 10 * 1024 * 1024)
    
    def get_backup_count(self) -> int:
        """获取备份文件数量"""
        return self.get_rotation_config().get("backup_count", 5)
    
    def get_retention_days(self) -> int:
        """获取保留天数"""
        return self.get_rotation_config().get("retention_days", 30)
    
    def get_format_config(self) -> Dict[str, str]:
        """获取格式配置"""
        return self.config.get("format", {})
    
    def get_console_format(self) -> str:
        """获取控制台格式"""
        return self.get_format_config().get("console", self.DEFAULT_CONFIG["format"]["console"])
    
    def get_file_format(self) -> str:
        """获取文件格式"""
        return self.get_format_config().get("file", self.DEFAULT_CONFIG["format"]["file"])
    
    def get_handlers(self) -> list:
        """获取处理器列表"""
        return self.config.get("handlers", ["console", "file"])
    
    def is_compression_enabled(self) -> bool:
        """是否启用压缩"""
        return self.config.get("compression", True)
    
    def is_async_mode(self) -> bool:
        """是否异步模式"""
        return self.config.get("async_mode", True)
    
    def get_buffer_size(self) -> int:
        """获取缓冲区大小"""
        return self.config.get("buffer_size", 1000)
    
    def validate_config(self) -> bool:
        """验证配置有效性"""
        try:
            # 验证日志级别
            level = self.get_level()
            valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            if level.upper() not in valid_levels:
                raise ValueError(f"无效的日志级别: {level}")
            
            # 验证轮转类型
            rotation_type = self.get_rotation_type()
            if rotation_type not in ["time", "size"]:
                raise ValueError(f"无效的轮转类型: {rotation_type}")
            
            # 验证最大文件大小
            max_size = self.get_max_size()
            if max_size <= 0:
                raise ValueError("最大文件大小必须大于0")
            
            # 验证备份数量
            backup_count = self.get_backup_count()
            if backup_count < 0:
                raise ValueError("备份数量不能为负数")
            
            # 验证保留天数
            retention_days = self.get_retention_days()
            if retention_days <= 0:
                raise ValueError("保留天数必须大于0")
            
            return True
            
        except Exception as e:
            raise ValueError(f"日志配置验证失败: {e}")
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self.config.copy()
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'LogConfig':
        """从字典创建配置"""
        return cls(config_dict)
    
    def get_log_file_paths(self, log_dir: Optional[str] = None) -> Dict[str, str]:
        """获取日志文件路径"""
        if log_dir is None:
            log_dir = self.get_log_dir()
        
        handlers = self.get_handlers()
        paths = {}
        
        if "file" in handlers:
            if self.get_rotation_type() == "size":
                paths["main"] = str(Path(log_dir) / "webmon.log")
            else:
                paths["main"] = str(Path(log_dir) / "webmon.log")  # 时间轮转的文件名会动态生成
        
        if "error_file" in handlers:
            if self.get_rotation_type() == "size":
                paths["error"] = str(Path(log_dir) / "webmon_error.log")
            else:
                paths["error"] = str(Path(log_dir) / "webmon_error.log")
        
        return paths
    
    def create_log_rotation_config(self) -> Dict[str, Any]:
        """创建日志轮转配置"""
        rotation_config = self.get_rotation_config()
        rotation_type = self.get_rotation_type()
        
        if rotation_type == "size":
            return {
                "type": "size",
                "max_size": self.get_max_size(),
                "backup_count": self.get_backup_count()
            }
        else:  # time
            return {
                "type": "time",
                "interval": rotation_config.get("interval", 1),
                "retention_days": self.get_retention_days()
            }
    
    def estimate_log_size(self, tasks_per_day: int = 100, avg_log_size: int = 200) -> Dict[str, Any]:
        """估计日志大小"""
        try:
            daily_logs = tasks_per_day * avg_log_size  # 字节
            retention_days = self.get_retention_days()
            max_size = self.get_max_size()
            backup_count = self.get_backup_count()
            
            if self.get_rotation_type() == "size":
                # 按大小轮转
                max_daily_size = max_size * backup_count
                estimated_retention = max_daily_size // daily_logs if daily_logs > 0 else retention_days
            else:
                # 按时间轮转
                estimated_retention = retention_days
                max_daily_size = daily_logs
            
            return {
                "daily_logs_bytes": daily_logs,
                "estimated_retention_days": estimated_retention,
                "max_daily_size_bytes": max_daily_size,
                "total_size_bytes": daily_logs * estimated_retention,
                "rotation_type": self.get_rotation_type()
            }
            
        except Exception as e:
            return {"error": str(e)}


# 全局日志配置实例
_global_log_config = None


def get_log_config() -> LogConfig:
    """获取全局日志配置"""
    global _global_log_config
    if _global_log_config is None:
        _global_log_config = LogConfig()
    return _global_log_config


def set_log_config(config: LogConfig):
    """设置全局日志配置"""
    global _global_log_config
    _global_log_config = config