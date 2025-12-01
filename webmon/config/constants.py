"""
配置常量
"""
from pathlib import Path

# 默认配置文件路径
DEFAULT_CONFIG_DIR = Path("config")
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.json"
DEFAULT_ENV_FILE = Path(".env")

# 其他常量
DEFAULT_BACKUP_DIR = DEFAULT_CONFIG_DIR / "backup"
DEFAULT_LOG_DIR = Path("logs")
DEFAULT_DATA_DIR = Path("data")