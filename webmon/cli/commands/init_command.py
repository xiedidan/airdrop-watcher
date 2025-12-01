"""
初始化命令实现
"""

import os
import shutil
from pathlib import Path
from argparse import Namespace

from webmon.cli.command import Command
from webmon.utils.logger import get_logger


class InitCommand(Command):
    """初始化命令"""
    
    def __init__(self, args: Namespace):
        super().__init__(args)
        self.logger = get_logger(__name__)
    
    def execute(self) -> bool:
        """执行初始化命令"""
        try:
            self.logger.info("开始初始化WebMon...")
            
            # 创建必要的目录
            self._create_directories()
            
            # 创建配置文件
            self._create_config_files()
            
            # 创建环境变量文件
            self._create_env_file()
            
            self.logger.info("WebMon初始化完成！")
            print("✅ WebMon初始化成功！")
            print("请编辑 .env 文件配置推送平台参数")
            print("使用 'webmon add <URL>' 添加监控任务")
            
            return True
            
        except Exception as e:
            self.logger.error(f"初始化失败: {e}")
            print(f"❌ 初始化失败: {e}")
            return False
    
    def _create_directories(self):
        """创建必要的目录"""
        directories = [
            'config',
            'data', 
            'logs',
            'data/backup'
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"创建目录: {directory}")
    
    def _create_config_files(self):
        """创建配置文件"""
        config_file = Path('config/config.json')
        
        if config_file.exists() and not self.args.force:
            self.logger.warning(f"配置文件已存在: {config_file}")
            return
        
        default_config = {
            "version": "1.0.0",
            "tasks": [],
            "settings": {
                "default_check_interval": 60,
                "max_concurrent_tasks": 5,
                "browser_timeout": 30,
                "page_load_timeout": 30,
                "similarity_threshold": 0.95,
                "max_retry_times": 3,
                "retry_interval": 5,
                "history_retention_days": 30,
                "auto_backup": True,
                "backup_interval_days": 7
            },
            "notification": {
                "enabled_platforms": [],
                "templates": {
                    "default": "🌐 网页变化检测\n\n任务: {task_name}\nURL: {url}\n变化时间: {change_time}\n变化类型: {change_type}\n\n{change_summary}"
                }
            }
        }
        
        import json
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"创建配置文件: {config_file}")
    
    def _create_env_file(self):
        """创建环境变量文件"""
        env_file = Path('.env')
        env_example = Path('.env.example')
        
        if env_file.exists() and not self.args.force:
            self.logger.warning(f"环境变量文件已存在: {env_file}")
            return
        
        if env_example.exists():
            shutil.copy(env_example, env_file)
            self.logger.info(f"从模板创建环境变量文件: {env_file}")
        else:
            # 创建基本的.env文件
            basic_env = """# WebMon 环境变量配置
LOG_LEVEL=INFO
DATA_DIR=./data
CONFIG_DIR=./config
LOGS_DIR=./logs

# PushPlus 微信推送配置
PUSHPLUS_TOKEN=

# Telegram Bot 推送配置
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# Discord Webhook 推送配置
DISCORD_WEBHOOK_URL=

# 飞书 Webhook 推送配置
FEISHU_WEBHOOK_URL=
"""
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(basic_env)
            self.logger.info(f"创建基本环境变量文件: {env_file}")
    
    def validate_args(self) -> bool:
        """验证参数"""
        return True