"""
任务存储管理器

负责任务的CRUD操作，管理config.json中的任务数据
"""
import json
import os
import shutil
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path

from ..models.task import Task
from ..exceptions import StorageError, ConfigurationError
from ..config.constants import DEFAULT_CONFIG_FILE


class TaskStorage:
    """任务存储管理器"""
    
    def __init__(self, config_file: str = None):
        """
        初始化任务存储管理器
        
        Args:
            config_file: 配置文件路径，默认为None使用标准路径
        """
        if config_file:
            self.config_file = Path(config_file)
        else:
            self.config_file = DEFAULT_CONFIG_FILE
        self.backup_dir = self.config_file.parent / "backup"
        
        # 确保备份目录存在
        self.backup_dir.mkdir(exist_ok=True)
        
        # 初始化配置文件（如果不存在）
        if not self.config_file.exists():
            self._init_config_file()
    
    def _init_config_file(self):
        """初始化配置文件"""
        default_config = {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
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
                    "content": "📍 URL: {url}\n⏰ 时间: {timestamp}\n📝 变化: {summary}\n🔗 查看: {url}",
                    "rate_limit": 60
                },
                "platform_configs": {
                    "pushplus": {
                        "enabled": True,
                        "token": ""
                    },
                    "telegram": {
                        "enabled": False,
                        "bot_token": "",
                        "chat_id": ""
                    },
                    "discord": {
                        "enabled": False,
                        "webhook_url": ""
                    },
                    "feishu": {
                        "enabled": False,
                        "webhook_url": ""
                    }
                }
            },
            "tasks": [],
            "storage": {
                "history_file": "data/history.json",
                "max_history_entries": 1000,
                "auto_cleanup_days": 30
            }
        }
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise StorageError(f"创建配置文件失败: {e}")
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise StorageError(f"配置文件不存在: {self.config_file}")
        except json.JSONDecodeError as e:
            raise StorageError(f"配置文件格式错误: {e}")
        except Exception as e:
            raise StorageError(f"加载配置文件失败: {e}")
    
    def _save_config(self, config: Dict[str, Any]):
        """保存配置文件"""
        try:
            # 更新修改时间
            config["updated_at"] = datetime.now().isoformat()
            
            # 创建备份
            self._create_backup()
            
            # 保存配置
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            raise StorageError(f"保存配置文件失败: {e}")
    
    def _create_backup(self):
        """创建配置备份"""
        try:
            if self.config_file.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = self.backup_dir / f"config_{timestamp}.json"
                shutil.copy2(self.config_file, backup_file)
                
                # 清理旧备份（保留最近10个）
                self._cleanup_old_backups()
                
        except Exception as e:
            # 备份失败不中断主流程，只记录警告
            print(f"警告: 创建备份失败: {e}")
    
    def _cleanup_old_backups(self, keep_count: int = 10):
        """清理旧备份文件"""
        try:
            backup_files = sorted(self.backup_dir.glob("config_*.json"))
            if len(backup_files) > keep_count:
                for backup_file in backup_files[:-keep_count]:
                    backup_file.unlink()
        except Exception as e:
            print(f"警告: 清理备份文件失败: {e}")
    
    def add_task(self, task: Task) -> str:
        """
        添加任务
        
        Args:
            task: 任务对象
            
        Returns:
            任务ID
            
        Raises:
            StorageError: 存储错误
            ConfigurationError: 配置错误
        """
        # 验证任务
        errors = task.validate()
        if errors:
            raise ConfigurationError(f"任务验证失败: {'; '.join(errors)}")
        
        # 加载配置
        config = self._load_config()
        tasks = config.get("tasks", [])
        
        # 检查任务是否已存在（通过URL）
        for existing_task in tasks:
            if existing_task.get("url") == task.url:
                raise ConfigurationError(f"任务已存在: {task.url}")
        
        # 添加任务
        task_data = task.to_dict()
        tasks.append(task_data)
        config["tasks"] = tasks
        
        # 保存配置
        self._save_config(config)
        
        return task.id
    
    def remove_task(self, task_id: str) -> bool:
        """
        删除任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            是否成功删除
            
        Raises:
            StorageError: 存储错误
        """
        # 加载配置
        config = self._load_config()
        tasks = config.get("tasks", [])
        
        # 查找并删除任务
        original_count = len(tasks)
        tasks = [task for task in tasks if task.get("id") != task_id]
        
        if len(tasks) == original_count:
            return False  # 任务未找到
        
        # 保存配置
        config["tasks"] = tasks
        self._save_config(config)
        
        return True
    
    def update_task(self, task_id: str, updates: Dict[str, Any]) -> bool:
        """
        更新任务
        
        Args:
            task_id: 任务ID
            updates: 更新字段
            
        Returns:
            是否成功更新
            
        Raises:
            StorageError: 存储错误
            ConfigurationError: 配置错误
        """
        # 加载配置
        config = self._load_config()
        tasks = config.get("tasks", [])
        
        # 查找任务
        task_index = None
        for i, task in enumerate(tasks):
            if task.get("id") == task_id:
                task_index = i
                break
        
        if task_index is None:
            return False
        
        # 创建任务对象进行验证
        task_data = tasks[task_index].copy()
        task_data.update(updates)
        task_data["updated_at"] = datetime.now().isoformat()
        
        try:
            task = Task.from_dict(task_data)
            errors = task.validate()
            if errors:
                raise ConfigurationError(f"任务验证失败: {'; '.join(errors)}")
            
            # 更新任务
            tasks[task_index] = task.to_dict()
            config["tasks"] = tasks
            
            # 保存配置
            self._save_config(config)
            
            return True
            
        except Exception as e:
            raise ConfigurationError(f"更新任务失败: {e}")
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """
        获取任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务对象，不存在则返回None
            
        Raises:
            StorageError: 存储错误
        """
        # 加载配置
        config = self._load_config()
        tasks = config.get("tasks", [])
        
        # 查找任务
        for task_data in tasks:
            if task_data.get("id") == task_id:
                try:
                    return Task.from_dict(task_data)
                except Exception as e:
                    raise StorageError(f"解析任务数据失败: {e}")
        
        return None
    
    def get_task_by_url(self, url: str) -> Optional[Task]:
        """
        通过URL获取任务
        
        Args:
            url: 任务URL
            
        Returns:
            任务对象，不存在则返回None
            
        Raises:
            StorageError: 存储错误
        """
        # 加载配置
        config = self._load_config()
        tasks = config.get("tasks", [])
        
        # 查找任务
        for task_data in tasks:
            if task_data.get("url") == url:
                try:
                    return Task.from_dict(task_data)
                except Exception as e:
                    raise StorageError(f"解析任务数据失败: {e}")
        
        return None
    
    def list_tasks(self, enabled_only: bool = False, status: str = None) -> List[Task]:
        """
        列出任务
        
        Args:
            enabled_only: 只返回启用的任务
            status: 筛选特定状态的任务
            
        Returns:
            任务列表
            
        Raises:
            StorageError: 存储错误
        """
        # 加载配置
        config = self._load_config()
        tasks = config.get("tasks", [])
        
        result = []
        for task_data in tasks:
            try:
                task = Task.from_dict(task_data)
                
                # 应用筛选条件
                if enabled_only and not task.enabled:
                    continue
                if status and task.status != status:
                    continue
                
                result.append(task)
                
            except Exception as e:
                # 跳过无效的任务数据
                print(f"警告: 跳过无效的任务数据: {e}")
                continue
        
        return result
    
    def count_tasks(self, enabled_only: bool = False, status: str = None) -> int:
        """
        统计任务数量
        
        Args:
            enabled_only: 只统计启用的任务
            status: 统计特定状态的任务
            
        Returns:
            任务数量
            
        Raises:
            StorageError: 存储错误
        """
        tasks = self.list_tasks(enabled_only=enabled_only, status=status)
        return len(tasks)
    
    def task_exists(self, task_id: str) -> bool:
        """
        检查任务是否存在
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务是否存在
        """
        return self.get_task(task_id) is not None
    
    def export_tasks(self, file_path: str, format: str = "json") -> str:
        """
        导出任务
        
        Args:
            file_path: 导出文件路径
            format: 导出格式 (json/csv)
            
        Returns:
            导出文件路径
            
        Raises:
            StorageError: 存储错误
        """
        tasks = self.list_tasks()
        
        if format.lower() == "json":
            export_data = {
                "version": "1.0.0",
                "exported_at": datetime.now().isoformat(),
                "tasks": [task.to_dict() for task in tasks]
            }
            
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
            except Exception as e:
                raise StorageError(f"导出任务失败: {e}")
        
        else:
            raise ConfigurationError(f"不支持的导出格式: {format}")
        
        return file_path
    
    def import_tasks(self, file_path: str, overwrite: bool = False) -> int:
        """
        导入任务
        
        Args:
            file_path: 导入文件路径
            overwrite: 是否覆盖现有任务
            
        Returns:
            导入的任务数量
            
        Raises:
            StorageError: 存储错误
            ConfigurationError: 配置错误
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            imported_tasks = import_data.get("tasks", [])
            count = 0
            
            for task_data in imported_tasks:
                try:
                    task = Task.from_dict(task_data)
                    
                    # 检查任务是否已存在
                    existing_task = self.get_task_by_url(task.url)
                    if existing_task and not overwrite:
                        continue
                    
                    # 添加或更新任务
                    if existing_task and overwrite:
                        self.update_task(task.id, task_data)
                    else:
                        self.add_task(task)
                    
                    count += 1
                    
                except Exception as e:
                    print(f"警告: 跳过无效的任务数据: {e}")
                    continue
            
            return count
            
        except Exception as e:
            raise StorageError(f"导入任务失败: {e}")
    
    def get_config(self) -> Dict[str, Any]:
        """
        获取完整配置
        
        Returns:
            配置字典
            
        Raises:
            StorageError: 存储错误
        """
        return self._load_config()
    
    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        更新配置
        
        Args:
            updates: 配置更新
            
        Returns:
            是否成功更新
            
        Raises:
            StorageError: 存储错误
        """
        try:
            config = self._load_config()
            config.update(updates)
            self._save_config(config)
            return True
        except Exception as e:
            raise StorageError(f"更新配置失败: {e}")
    
    def restore_backup(self, backup_file: str = None) -> bool:
        """
        恢复备份
        
        Args:
            backup_file: 备份文件路径，如果为None则使用最新备份
            
        Returns:
            是否成功恢复
            
        Raises:
            StorageError: 存储错误
        """
        try:
            if backup_file is None:
                # 使用最新备份
                backup_files = sorted(self.backup_dir.glob("config_*.json"))
                if not backup_files:
                    raise StorageError("没有找到备份文件")
                backup_file = backup_files[-1]
            else:
                backup_file = Path(backup_file)
            
            if not backup_file.exists():
                raise StorageError(f"备份文件不存在: {backup_file}")
            
            # 创建当前配置的备份
            current_backup = self.backup_dir / f"config_before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            shutil.copy2(self.config_file, current_backup)
            
            # 恢复备份
            shutil.copy2(backup_file, self.config_file)
            
            return True
            
        except Exception as e:
            raise StorageError(f"恢复备份失败: {e}")
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """
        列出备份文件
        
        Returns:
            备份文件信息列表
        """
        try:
            backup_files = sorted(self.backup_dir.glob("config_*.json"))
            backups = []
            
            for backup_file in backup_files:
                stat = backup_file.stat()
                backups.append({
                    "file": str(backup_file),
                    "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "size": stat.st_size
                })
            
            return backups
            
        except Exception as e:
            raise StorageError(f"列出备份文件失败: {e}")