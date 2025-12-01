#!/usr/bin/env python3
"""
增强版日志系统
支持按大小和日期轮转，结构化日志，动态配置
"""

import os
import sys
import json
import logging
import logging.handlers
from pathlib import Path
from typing import Optional, Dict, Any, Union
from datetime import datetime
import threading
import functools

# 尝试导入loguru
try:
    from loguru import logger as loguru_logger
    LOGURU_AVAILABLE = True
except ImportError:
    LOGURU_AVAILABLE = False

# 导入配置管理器
try:
    from webmon.config import ConfigManager
    from webmon.utils.log_config import LogConfig, get_log_config
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False

# 日志配置常量
DEFAULT_LOG_DIR = "logs"
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_MAX_BYTES = 10 * 1024 * 1024  # 10MB
DEFAULT_BACKUP_COUNT = 5
DEFAULT_RETENTION_DAYS = 30

# 日志格式模板
CONSOLE_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)

FILE_FORMAT = (
    "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
    "{name}:{function}:{line} | {message}"
)

# 线程安全的日志级别缓存
_log_level_cache = {}
_log_level_lock = threading.Lock()


class EnhancedLogger:
    """增强版日志管理器"""
    
    def __init__(self, name: str, config_manager: Optional['ConfigManager'] = None):
        """初始化增强版日志管理器"""
        self.name = name
        self.config_manager = config_manager
        self._logger = None
        self._config = None
        self._handlers = []
        self._lock = threading.Lock()
        
        # 初始化日志配置
        self._initialize_config()
        
    def _initialize_config(self):
        """初始化日志配置"""
        # 尝试从配置管理器获取配置
        if self.config_manager and CONFIG_AVAILABLE:
            try:
                self._config = self.config_manager.get_logging_config()
                return
            except Exception:
                pass
        
        # 尝试使用全局日志配置
        if CONFIG_AVAILABLE:
            try:
                global_config = get_log_config()
                self._config = global_config.to_dict()
                return
            except Exception:
                pass
        
        # 使用默认配置
        self._config = self._get_default_config()
            
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认日志配置"""
        return {
            "level": DEFAULT_LOG_LEVEL,
            "log_dir": DEFAULT_LOG_DIR,
            "rotation": {
                "type": "time",  # "time" 或 "size"
                "interval": 1,   # 天
                "max_size": DEFAULT_MAX_BYTES,
                "backup_count": DEFAULT_BACKUP_COUNT,
                "retention_days": DEFAULT_RETENTION_DAYS
            },
            "format": {
                "console": CONSOLE_FORMAT,
                "file": FILE_FORMAT
            },
            "handlers": ["console", "file", "error_file"],
            "compression": True
        }
    
    def _setup_log_directory(self) -> Path:
        """设置日志目录"""
        log_dir = Path(self._config.get("log_dir", DEFAULT_LOG_DIR))
        
        try:
            log_dir.mkdir(parents=True, exist_ok=True)
            return log_dir
        except Exception as e:
            print(f"创建日志目录失败: {e}")
            # 回退到当前目录
            return Path(".")
    
    def _setup_loguru_logger(self) -> bool:
        """设置loguru日志系统"""
        if not LOGURU_AVAILABLE:
            return False
            
        try:
            log_dir = self._setup_log_directory()
            level = self._config.get("level", DEFAULT_LOG_LEVEL)
            rotation_config = self._config.get("rotation", {})
            format_config = self._config.get("format", {})
            
            # 配置日志级别
            loguru_logger.remove()  # 移除默认handler
            
            # 控制台handler
            if "console" in self._config.get("handlers", []):
                console_format = format_config.get("console", CONSOLE_FORMAT)
                loguru_logger.add(
                    sys.stderr,
                    level=level,
                    format=console_format,
                    backtrace=True,
                    diagnose=True
                )
            
            # 文件handler
            if "file" in self._config.get("handlers", []):
                file_format = format_config.get("file", FILE_FORMAT)
                log_file = log_dir / f"webmon_{{time:YYYY-MM-DD}}.log"
                
                # 根据轮转类型设置参数
                rotation_type = rotation_config.get("type", "time")
                
                if rotation_type == "size":
                    max_size = rotation_config.get("max_size", DEFAULT_MAX_BYTES)
                    backup_count = rotation_config.get("backup_count", DEFAULT_BACKUP_COUNT)
                    
                    loguru_logger.add(
                        str(log_dir / "webmon.log"),
                        level=level,
                        format=file_format,
                        rotation=max_size,
                        retention=backup_count,
                        compression="zip" if self._config.get("compression") else None,
                        enqueue=True  # 线程安全
                    )
                else:  # time based
                    loguru_logger.add(
                        str(log_file),
                        level=level,
                        format=file_format,
                        rotation="1 day",
                        retention=f"{rotation_config.get('retention_days', DEFAULT_RETENTION_DAYS)} days",
                        compression="zip" if self._config.get("compression") else None,
                        enqueue=True
                    )
            
            # 错误文件handler
            if "error_file" in self._config.get("handlers", []):
                error_format = format_config.get("file", FILE_FORMAT)
                
                if rotation_type == "size":
                    max_size = rotation_config.get("max_size", DEFAULT_MAX_BYTES)
                    
                    loguru_logger.add(
                        str(log_dir / "webmon_error.log"),
                        level="ERROR",
                        format=error_format,
                        rotation=max_size,
                        retention=backup_count,
                        compression="zip" if self._config.get("compression") else None,
                        enqueue=True
                    )
                else:
                    loguru_logger.add(
                        str(log_dir / f"webmon_error_{{time:YYYY-MM-DD}}.log"),
                        level="ERROR",
                        format=error_format,
                        rotation="1 day",
                        retention=f"{rotation_config.get('retention_days', DEFAULT_RETENTION_DAYS)} days",
                        compression="zip" if self._config.get("compression") else None,
                        enqueue=True
                    )
            
            return True
            
        except Exception as e:
            print(f"设置loguru日志系统失败: {e}")
            return False
    
    def _setup_standard_logger(self) -> bool:
        """设置标准库日志系统"""
        try:
            log_dir = self._setup_log_directory()
            level = self._config.get("level", DEFAULT_LOG_LEVEL)
            rotation_config = self._config.get("rotation", {})
            
            # 创建logger
            logger = logging.getLogger(self.name)
            logger.setLevel(getattr(logging, level.upper(), logging.INFO))
            
            # 清除现有handlers
            logger.handlers.clear()
            
            # 控制台handler
            if "console" in self._config.get("handlers", []):
                console_handler = logging.StreamHandler(sys.stderr)
                console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
                
                console_formatter = logging.Formatter(
                    '%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                console_handler.setFormatter(console_formatter)
                logger.addHandler(console_handler)
            
            # 文件handler
            if "file" in self._config.get("handlers", []):
                rotation_type = rotation_config.get("type", "time")
                
                if rotation_type == "size":
                    max_bytes = rotation_config.get("max_size", DEFAULT_MAX_BYTES)
                    backup_count = rotation_config.get("backup_count", DEFAULT_BACKUP_COUNT)
                    
                    file_handler = logging.handlers.RotatingFileHandler(
                        log_dir / "webmon.log",
                        maxBytes=max_bytes,
                        backupCount=backup_count,
                        encoding='utf-8'
                    )
                else:  # time based
                    file_handler = logging.handlers.TimedRotatingFileHandler(
                        log_dir / "webmon.log",
                        when='midnight',
                        interval=1,
                        backupCount=rotation_config.get('retention_days', DEFAULT_RETENTION_DAYS),
                        encoding='utf-8'
                    )
                
                file_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
                
                file_formatter = logging.Formatter(
                    '%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                file_handler.setFormatter(file_formatter)
                logger.addHandler(file_handler)
            
            # 错误文件handler
            if "error_file" in self._config.get("handlers", []):
                if rotation_type == "size":
                    max_bytes = rotation_config.get("max_size", DEFAULT_MAX_BYTES)
                    
                    error_handler = logging.handlers.RotatingFileHandler(
                        log_dir / "webmon_error.log",
                        maxBytes=max_bytes,
                        backupCount=rotation_config.get("backup_count", DEFAULT_BACKUP_COUNT),
                        encoding='utf-8'
                    )
                else:
                    error_handler = logging.handlers.TimedRotatingFileHandler(
                        log_dir / "webmon_error.log",
                        when='midnight',
                        interval=1,
                        backupCount=rotation_config.get('retention_days', DEFAULT_RETENTION_DAYS),
                        encoding='utf-8'
                    )
                
                error_handler.setLevel(logging.ERROR)
                
                error_formatter = logging.Formatter(
                    '%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                error_handler.setFormatter(error_formatter)
                logger.addHandler(error_handler)
            
            return True
            
        except Exception as e:
            print(f"设置标准库日志系统失败: {e}")
            return False
    
    def setup_logger(self) -> bool:
        """设置日志系统"""
        with self._lock:
            try:
                # 优先使用loguru
                if LOGURU_AVAILABLE:
                    success = self._setup_loguru_logger()
                    if success:
                        self._logger = loguru_logger
                        return True
                
                # 回退到标准库
                success = self._setup_standard_logger()
                if success:
                    self._logger = logging.getLogger(self.name)
                    return True
                
                return False
                
            except Exception as e:
                print(f"设置日志系统失败: {e}")
                return False
    
    def get_logger(self):
        """获取logger实例"""
        if self._logger is None:
            if not self.setup_logger():
                # 最后回退到基本logging
                self._logger = logging.getLogger(self.name)
                self._logger.setLevel(logging.INFO)
        
        return self._logger
    
    def update_config(self, new_config: Dict[str, Any]) -> bool:
        """更新日志配置"""
        try:
            with self._lock:
                self._config.update(new_config)
                
                # 重新设置logger
                if self._logger:
                    # 清除现有配置
                    if LOGURU_AVAILABLE and hasattr(self._logger, 'remove'):
                        self._logger.remove()
                    elif hasattr(self._logger, 'handlers'):
                        self._logger.handlers.clear()
                
                # 重新设置
                return self.setup_logger()
                
        except Exception as e:
            print(f"更新日志配置失败: {e}")
            return False
    
    def get_log_stats(self) -> Dict[str, Any]:
        """获取日志统计信息"""
        try:
            log_dir = Path(self._config.get("log_dir", DEFAULT_LOG_DIR))
            
            if not log_dir.exists():
                return {"error": "日志目录不存在"}
            
            stats = {
                "log_dir": str(log_dir),
                "total_size": 0,
                "file_count": 0,
                "files": []
            }
            
            for log_file in log_dir.glob("*.log*"):
                try:
                    file_size = log_file.stat().st_size
                    stats["total_size"] += file_size
                    stats["file_count"] += 1
                    
                    stats["files"].append({
                        "name": log_file.name,
                        "size": file_size,
                        "modified": datetime.fromtimestamp(log_file.stat().st_mtime).isoformat()
                    })
                except Exception:
                    continue
            
            # 按大小排序
            stats["files"].sort(key=lambda x: x["size"], reverse=True)
            
            return stats
            
        except Exception as e:
            return {"error": str(e)}
    
    def cleanup_old_logs(self, retention_days: int = None) -> int:
        """清理旧日志文件"""
        try:
            if retention_days is None:
                retention_days = self._config.get("rotation", {}).get("retention_days", DEFAULT_RETENTION_DAYS)
            
            log_dir = Path(self._config.get("log_dir", DEFAULT_LOG_DIR))
            
            if not log_dir.exists():
                return 0
            
            cutoff_date = datetime.now().timestamp() - (retention_days * 24 * 3600)
            cleaned_count = 0
            
            for log_file in log_dir.glob("*.log*"):
                try:
                    if log_file.stat().st_mtime < cutoff_date:
                        log_file.unlink()
                        cleaned_count += 1
                except Exception:
                    continue
            
            return cleaned_count
            
        except Exception as e:
            print(f"清理旧日志失败: {e}")
            return 0


# 向后兼容的函数接口
def get_logger(name: str = None, config_manager: Optional['ConfigManager'] = None):
    """获取增强版logger - 兼容接口"""
    if name is None:
        name = __name__
    
    logger = EnhancedLogger(name, config_manager)
    if logger.setup_logger():
        return logger.get_logger()
    else:
        # 最后回退
        import logging
        return logging.getLogger(name)


def setup_global_logger(config_manager: Optional['ConfigManager'] = None):
    """设置全局日志系统 - 兼容接口"""
    global _global_logger
    _global_logger = EnhancedLogger("webmon", config_manager)
    return _global_logger.setup_logger()


# 全局logger实例
_global_logger = None