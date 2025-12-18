"""
任务服务层

封装任务管理的业务逻辑，与 ConfigManager 交互。
"""

import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from webmon.config.config_manager import ConfigManager
from webmon.models.task import Task


class TaskService:
    """任务管理服务"""

    _instance: Optional['TaskService'] = None
    _config_manager: Optional[ConfigManager] = None

    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_config_manager(cls) -> ConfigManager:
        """获取配置管理器实例"""
        if cls._config_manager is None:
            cls._config_manager = ConfigManager()
        return cls._config_manager

    @classmethod
    def set_config_manager(cls, config_manager: ConfigManager):
        """设置配置管理器实例（用于测试）"""
        cls._config_manager = config_manager

    def list_tasks(self, enabled_only: bool = False) -> List[Dict[str, Any]]:
        """
        获取任务列表

        Args:
            enabled_only: 是否只返回启用的任务

        Returns:
            任务列表
        """
        config_manager = self.get_config_manager()
        tasks = config_manager.list_tasks()

        if enabled_only:
            tasks = [t for t in tasks if t.get('enabled', True)]

        return tasks

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        获取单个任务

        Args:
            task_id: 任务ID

        Returns:
            任务配置，不存在返回None
        """
        config_manager = self.get_config_manager()
        return config_manager.get_task_config(task_id)

    def create_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建新任务

        Args:
            task_data: 任务数据

        Returns:
            创建的任务配置

        Raises:
            ValueError: 创建失败时抛出
        """
        config_manager = self.get_config_manager()

        # 生成任务ID和时间戳
        task_id = str(uuid.uuid4())
        now = datetime.now().isoformat()

        # 构建完整的任务配置
        task_config = {
            'id': task_id,
            'url': task_data['url'],
            'name': task_data['name'],
            'description': task_data.get('description', ''),
            'selectors': task_data.get('selectors', []),
            'interval': task_data.get('interval', 300),
            'timeout': task_data.get('timeout', 30000),
            'enabled': task_data.get('enabled', True),
            'ai_prompt': task_data.get('ai_prompt', ''),
            'created_at': now,
            'updated_at': now,
            'last_check': None,
            'last_change': None,
            'change_count': 0,
            'status': 'active',
            'error_count': 0,
            'last_error': None,
            'last_error_message': None,
        }

        # 添加任务
        success = config_manager.add_task(task_config)
        if not success:
            raise ValueError("添加任务失败")

        return task_config

    def update_task(self, task_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新任务

        Args:
            task_id: 任务ID
            updates: 更新数据

        Returns:
            更新后的任务配置

        Raises:
            ValueError: 任务不存在或更新失败
        """
        config_manager = self.get_config_manager()

        # 检查任务是否存在
        existing = config_manager.get_task_config(task_id)
        if not existing:
            raise ValueError(f"任务不存在: {task_id}")

        # 过滤None值
        filtered_updates = {k: v for k, v in updates.items() if v is not None}

        # 更新时间戳
        filtered_updates['updated_at'] = datetime.now().isoformat()

        # 执行更新
        success = config_manager.update_task(task_id, filtered_updates)
        if not success:
            raise ValueError("更新任务失败")

        # 返回更新后的任务
        return config_manager.get_task_config(task_id)

    def delete_task(self, task_id: str) -> bool:
        """
        删除任务

        Args:
            task_id: 任务ID

        Returns:
            是否成功

        Raises:
            ValueError: 任务不存在
        """
        config_manager = self.get_config_manager()

        # 检查任务是否存在
        existing = config_manager.get_task_config(task_id)
        if not existing:
            raise ValueError(f"任务不存在: {task_id}")

        return config_manager.remove_task(task_id)

    def enable_task(self, task_id: str) -> Dict[str, Any]:
        """
        启用任务

        Args:
            task_id: 任务ID

        Returns:
            更新后的任务配置
        """
        return self.update_task(task_id, {'enabled': True, 'status': 'active'})

    def disable_task(self, task_id: str) -> Dict[str, Any]:
        """
        禁用任务

        Args:
            task_id: 任务ID

        Returns:
            更新后的任务配置
        """
        return self.update_task(task_id, {'enabled': False})

    async def check_task_now(self, task_id: str) -> Dict[str, Any]:
        """
        立即执行任务检测

        Args:
            task_id: 任务ID

        Returns:
            检测结果
        """
        config_manager = self.get_config_manager()

        # 检查任务是否存在
        task_config = config_manager.get_task_config(task_id)
        if not task_config:
            raise ValueError(f"任务不存在: {task_id}")

        # TODO: 集成实际的检测逻辑
        # 目前返回占位结果
        return {
            'success': True,
            'message': '立即检测功能将在后续实现',
            'task_id': task_id,
            'changed': None,
            'error': None
        }

    def get_task_count(self) -> Dict[str, int]:
        """
        获取任务统计

        Returns:
            任务数量统计
        """
        tasks = self.list_tasks()
        enabled = sum(1 for t in tasks if t.get('enabled', True))
        active = sum(1 for t in tasks if t.get('status') == 'active' and t.get('enabled', True))
        error = sum(1 for t in tasks if t.get('status') == 'error')

        return {
            'total': len(tasks),
            'enabled': enabled,
            'disabled': len(tasks) - enabled,
            'active': active,
            'error': error
        }


# 全局服务实例
task_service = TaskService()


def get_task_service() -> TaskService:
    """获取任务服务实例"""
    return task_service
