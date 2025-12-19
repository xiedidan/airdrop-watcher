"""
添加监控任务命令实现
"""

import re
from pathlib import Path
from argparse import Namespace
from urllib.parse import urlparse

from webmon.cli.command import Command
from webmon.utils.logger import get_logger


class AddCommand(Command):
    """添加监控任务命令"""
    
    def __init__(self, args: Namespace):
        super().__init__(args)
        self.logger = get_logger(__name__)
    
    def execute(self) -> bool:
        """执行添加任务命令"""
        try:
            url = self.args.url
            name = self.args.name
            selector = self.args.selector
            interval = self.args.interval
            timeout = self.args.timeout
            description = getattr(self.args, 'description', '') or ''
            ai_prompt = getattr(self.args, 'ai_prompt', '') or ''

            self.logger.info(f"添加监控任务: {url}")

            # 验证URL格式
            if not self._validate_url(url):
                print(f"❌ 无效的URL: {url}")
                return False

            # 生成任务名称
            if not name:
                name = self._generate_task_name(url)

            # 创建任务配置
            task_config = {
                "id": self._generate_task_id(),
                "name": name,
                "description": description,
                "url": url,
                "selector": selector,
                "interval": interval,
                "timeout": timeout,
                "enabled": True,
                "ai_prompt": ai_prompt,
                "created_at": self._get_current_timestamp()
            }

            # 保存任务到配置文件
            if not self._save_task(task_config):
                return False

            self.logger.info(f"任务添加成功: {name}")
            print(f"✅ 任务添加成功！")
            print(f"任务名称: {name}")
            print(f"监控URL: {url}")
            print(f"检测间隔: {interval}秒")
            if selector:
                print(f"CSS选择器: {selector}")
            if description:
                print(f"任务描述: {description}")
            if ai_prompt:
                print(f"AI提示词: {ai_prompt[:50]}..." if len(ai_prompt) > 50 else f"AI提示词: {ai_prompt}")

            return True
            
        except Exception as e:
            self.logger.error(f"添加任务失败: {e}")
            print(f"❌ 添加任务失败: {e}")
            return False
    
    def _validate_url(self, url: str) -> bool:
        """验证URL格式"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def _generate_task_name(self, url: str) -> str:
        """根据URL生成任务名称"""
        parsed = urlparse(url)
        domain = parsed.netloc
        
        # 移除www.前缀
        if domain.startswith('www.'):
            domain = domain[4:]
        
        # 替换特殊字符
        name = re.sub(r'[^a-zA-Z0-9.-]', '_', domain)
        
        return name
    
    def _generate_task_id(self) -> str:
        """生成任务ID"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def _get_current_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _save_task(self, task_config: dict) -> bool:
        """保存任务到配置文件"""
        try:
            config_file = Path('config/config.json')
            
            # 读取现有配置
            if config_file.exists():
                import json
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {"tasks": [], "settings": {}}
            
            # 检查任务名称是否已存在
            for task in config.get("tasks", []):
                if task["name"] == task_config["name"]:
                    print(f"❌ 任务名称已存在: {task_config['name']}")
                    return False
            
            # 添加新任务
            if "tasks" not in config:
                config["tasks"] = []
            
            config["tasks"].append(task_config)
            
            # 保存配置
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            self.logger.error(f"保存任务配置失败: {e}")
            return False
    
    def validate_args(self) -> bool:
        """验证参数"""
        if not self.args.url:
            print("❌ 必须提供URL参数")
            return False
        
        if self.args.interval <= 0:
            print("❌ 检测间隔必须大于0")
            return False
        
        if self.args.timeout <= 0:
            print("❌ 超时时间必须大于0")
            return False
        
        return True