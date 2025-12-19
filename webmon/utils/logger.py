"""
日志管理模块
提供统一的日志配置和管理功能
支持按大小和日期轮转，结构化日志
"""

import os
import sys
import logging
import logging.handlers
from pathlib import Path
from typing import Optional, Dict, Any, Union
import threading
from datetime import datetime

# 尝试导入增强日志系统
try:
    from webmon.utils.enhanced_logger import EnhancedLogger, get_logger as get_enhanced_logger
    from webmon.utils.enhanced_logger import _loguru_initialized as _enhanced_loguru_initialized
    from webmon.utils.enhanced_logger import _loguru_init_lock as _enhanced_loguru_init_lock
    ENHANCED_LOGGER_AVAILABLE = True
except ImportError:
    ENHANCED_LOGGER_AVAILABLE = False
    _enhanced_loguru_initialized = False
    _enhanced_loguru_init_lock = threading.Lock()

# 尝试导入loguru，如果失败则使用标准库logging
try:
    from loguru import logger as loguru_logger
    LOGURU_AVAILABLE = True
except ImportError:
    LOGURU_AVAILABLE = False
    import logging as loguru_logger


def get_logger(
    name: str,
    level: str = None,
    log_dir: str = None,
    log_file: str = None,
    max_bytes: int = None,
    backup_count: int = None,
    rotation_type: str = "time",
    config_manager: Optional['ConfigManager'] = None
):
    """
    获取配置好的logger实例 - 增强版，支持按大小轮转
    
    Args:
        name: logger名称，通常使用__name__
        level: 日志级别 (DEBUG, INFO, WARNING, ERROR)
        log_dir: 日志文件目录
        log_file: 日志文件名
        max_bytes: 最大文件大小(字节)，用于大小轮转
        backup_count: 备份文件数量
        rotation_type: 轮转类型("time"或"size")
        config_manager: 配置管理器实例
    
    Returns:
        配置好的logger实例
    """
    # 优先使用增强版日志系统
    if ENHANCED_LOGGER_AVAILABLE:
        try:
            # 尝试从配置管理器获取配置
            if config_manager and hasattr(config_manager, 'get_logging_config'):
                log_config = config_manager.get_logging_config()
                # 使用增强版日志系统
                from webmon.utils.enhanced_logger import get_logger as get_enhanced_logger
                return get_enhanced_logger(name, config_manager)
        except Exception:
            pass
    
    # 回退到传统日志系统
    # 从环境变量获取配置
    if level is None:
        level = os.getenv('LOG_LEVEL', 'INFO')
    
    if log_dir is None:
        log_dir = os.getenv('LOGS_DIR', './logs')
    
    if max_bytes is None:
        max_bytes = int(os.getenv('LOG_MAX_BYTES', str(10*1024*1024)))  # 10MB
    
    if backup_count is None:
        backup_count = int(os.getenv('LOG_BACKUP_COUNT', '5'))
    
    # 确保日志目录存在
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    if LOGURU_AVAILABLE:
        # 检查是否已经被增强版日志系统初始化过
        # 如果是，直接返回已配置的 loguru_logger，避免重复添加 handler
        if ENHANCED_LOGGER_AVAILABLE:
            from webmon.utils.enhanced_logger import _loguru_initialized, _loguru_init_lock
            with _loguru_init_lock:
                if _loguru_initialized:
                    # 增强版已初始化，直接返回绑定了名称的 logger
                    return loguru_logger.bind(name=name)

        # 使用loguru
        logger = loguru_logger.bind(name=name)

        # 移除默认的handler
        logger.remove()

        # 添加控制台输出
        logger.add(
            sys.stdout,
            level=level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            colorize=True
        )
        
        # 添加文件输出 - 支持按大小轮转
        if log_file is None:
            if rotation_type == "size":
                log_file = "webmon.log"
            else:
                log_file = f"webmon_{datetime.now().strftime('%Y-%m-%d')}.log"
        
        if LOGURU_AVAILABLE:
            # loguru格式
            if rotation_type == "size":
                # 按大小轮转
                logger.add(
                    os.path.join(log_dir, log_file),
                    level=level,
                    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
                    rotation=max_bytes,
                    retention=backup_count,
                    compression="zip"
                )
            else:
                # 按时间轮转（原有逻辑）
                logger.add(
                    os.path.join(log_dir, log_file),
                    level=level,
                    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
                    rotation="1 day",
                    retention="30 days",
                    compression="zip"
                )
        else:
            # 标准库logging格式
            if rotation_type == "size":
                # 按大小轮转
                file_handler = logging.handlers.RotatingFileHandler(
                    os.path.join(log_dir, log_file),
                    maxBytes=max_bytes,
                    backupCount=backup_count,
                    encoding='utf-8'
                )
            else:
                # 按时间轮转
                file_handler = logging.handlers.TimedRotatingFileHandler(
                    os.path.join(log_dir, log_file),
                    when='midnight',
                    interval=1,
                    backupCount=30,
                    encoding='utf-8'
                )
            
            file_handler.setLevel(getattr(logging, level.upper()))
            file_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        
        return logger
    else:
        # 使用标准库logging - 增强版，支持按大小轮转
        logger = loguru_logger.getLogger(name)
        logger.setLevel(getattr(loguru_logger, level.upper()))
        
        # 移除现有的handler
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # 添加控制台handler
        console_handler = loguru_logger.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(loguru_logger, level.upper()))
        
        formatter = loguru_logger.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s'
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # 添加文件handler - 支持按大小轮转
        if rotation_type == "size":
            # 按大小轮转
            file_handler = logging.handlers.RotatingFileHandler(
                os.path.join(log_dir, log_file or "webmon.log"),
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
        else:
            # 按时间轮转
            file_handler = logging.handlers.TimedRotatingFileHandler(
                os.path.join(log_dir, log_file or f"webmon_{datetime.now().strftime('%Y-%m-%d')}.log"),
                when='midnight',
                interval=1,
                backupCount=30,
                encoding='utf-8'
            )
        
        file_handler.setLevel(getattr(loguru_logger, level.upper()))
        file_formatter = loguru_logger.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        return logger


def setup_global_logger(
    level: str = None,
    log_dir: str = None,
    max_bytes: int = None,
    backup_count: int = None,
    rotation_type: str = "time"
) -> None:
    """
    设置全局logger配置 - 增强版，支持按大小轮转

    Args:
        level: 日志级别，默认从环境变量LOG_LEVEL读取
        log_dir: 日志文件目录，默认从环境变量LOGS_DIR读取
        max_bytes: 最大文件大小(字节)，用于大小轮转
        backup_count: 备份文件数量
        rotation_type: 轮转类型("time"或"size")
    """
    # 从环境变量读取默认值
    if level is None:
        level = os.getenv('LOG_LEVEL', 'INFO')

    if log_dir is None:
        log_dir = os.getenv('LOGS_DIR', './logs')

    # 确保日志目录存在
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    # 设置默认参数
    if max_bytes is None:
        max_bytes = int(os.getenv('LOG_MAX_BYTES', str(10*1024*1024)))  # 10MB

    if backup_count is None:
        backup_count = int(os.getenv('LOG_BACKUP_COUNT', '5'))

    if LOGURU_AVAILABLE:
        # 检查是否已经初始化，避免重复配置
        if ENHANCED_LOGGER_AVAILABLE:
            from webmon.utils.enhanced_logger import _loguru_initialized, _loguru_init_lock
            import webmon.utils.enhanced_logger as enhanced_logger_module
            with _loguru_init_lock:
                if _loguru_initialized:
                    # 已经初始化，跳过
                    return

                # 使用loguru
                loguru_logger.remove()

                # 添加控制台输出
                loguru_logger.add(
                    sys.stdout,
                    level=level,
                    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                    colorize=True
                )

                # 添加文件输出 - 支持按大小轮转
                if rotation_type == "size":
                    # 按大小轮转
                    loguru_logger.add(
                        os.path.join(log_dir, "webmon.log"),
                        level=level,
                        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
                        rotation=max_bytes,
                        retention=backup_count,
                        compression="zip"
                    )
                else:
                    # 按时间轮转（原有逻辑）
                    loguru_logger.add(
                        os.path.join(log_dir, f"webmon_{{time:YYYY-MM-DD}}.log"),
                        level=level,
                        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
                        rotation="1 day",
                        retention="30 days",
                        compression="zip"
                    )

                # 设置全局初始化标记，防止后续 get_logger 再次添加 handlers
                enhanced_logger_module._loguru_initialized = True
        else:
            # 没有增强版日志模块，使用原有逻辑
            loguru_logger.remove()

            # 添加控制台输出
            loguru_logger.add(
                sys.stdout,
                level=level,
                format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                colorize=True
            )

            # 添加文件输出 - 支持按大小轮转
            if rotation_type == "size":
                # 按大小轮转
                loguru_logger.add(
                    os.path.join(log_dir, "webmon.log"),
                    level=level,
                    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
                    rotation=max_bytes,
                    retention=backup_count,
                    compression="zip"
                )
            else:
                # 按时间轮转（原有逻辑）
                loguru_logger.add(
                    os.path.join(log_dir, f"webmon_{{time:YYYY-MM-DD}}.log"),
                    level=level,
                    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
                    rotation="1 day",
                    retention="30 days",
                    compression="zip"
                )
    else:
        # 使用标准库logging - 增强版，支持按大小轮转
        # 配置根logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, level.upper()))
        
        # 移除现有的handler
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # 添加控制台handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper()))
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        root_logger.addHandler(console_handler)
        
        # 添加文件handler - 支持按大小轮转
        if rotation_type == "size":
            # 按大小轮转
            file_handler = logging.handlers.RotatingFileHandler(
                os.path.join(log_dir, "webmon.log"),
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
        else:
            # 按时间轮转
            file_handler = logging.handlers.TimedRotatingFileHandler(
                os.path.join(log_dir, "webmon.log"),
                when='midnight',
                interval=1,
                backupCount=30,
                encoding='utf-8'
            )
        
        file_handler.setLevel(getattr(logging, level.upper()))
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)