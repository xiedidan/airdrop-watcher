"""
监控服务封装

封装与核心监控模块的交互逻辑，管理调度器的启动和停止。
"""

import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, List

from webmon.config.config_manager import ConfigManager
from webmon.scheduler.task_scheduler import TaskScheduler


class MonitorService:
    """监控控制服务"""

    _instance: Optional['MonitorService'] = None
    _scheduler: Optional[TaskScheduler] = None
    _config_manager: Optional[ConfigManager] = None
    _lock: asyncio.Lock = asyncio.Lock()

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
    def get_scheduler(cls) -> TaskScheduler:
        """获取调度器实例"""
        if cls._scheduler is None:
            cls._scheduler = TaskScheduler(cls.get_config_manager())
        return cls._scheduler

    @classmethod
    def set_scheduler(cls, scheduler: TaskScheduler):
        """设置调度器实例（用于测试）"""
        cls._scheduler = scheduler

    async def get_status(self) -> Dict[str, Any]:
        """
        获取监控器状态

        Returns:
            监控状态信息
        """
        config_manager = self.get_config_manager()
        scheduler = self.get_scheduler()

        # 获取任务统计
        tasks = config_manager.list_tasks()
        total_tasks = len(tasks)
        active_tasks = sum(1 for t in tasks if t.get('enabled', True))

        # 获取调度器状态
        is_running = scheduler.is_running
        stats = scheduler.stats

        # 计算运行时间
        uptime = 0.0
        start_time = None
        if stats.get('start_time'):
            start_time = stats['start_time']
            if isinstance(start_time, datetime):
                uptime = (datetime.now() - start_time).total_seconds()
                start_time = start_time.isoformat()

        # 获取正在运行的任务数
        running_tasks = len(scheduler.running_tasks) if hasattr(scheduler, 'running_tasks') else 0

        # 获取下次检测时间
        next_check = None
        if hasattr(scheduler, 'task_next_run') and scheduler.task_next_run:
            next_times = [t for t in scheduler.task_next_run.values() if t]
            if next_times:
                next_check_time = min(next_times)
                next_check = next_check_time.isoformat() if isinstance(next_check_time, datetime) else str(next_check_time)

        return {
            'status': 'running' if is_running else 'stopped',
            'is_running': is_running,
            'start_time': start_time,
            'uptime': uptime,
            'total_tasks': total_tasks,
            'active_tasks': active_tasks,
            'running_tasks': running_tasks,
            'total_executions': stats.get('total_executions', 0),
            'successful_executions': stats.get('successful_executions', 0),
            'failed_executions': stats.get('failed_executions', 0),
            'total_changes': stats.get('total_changes', 0),
            'next_check': next_check,
        }

    async def start(self, task_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        启动监控器

        Args:
            task_ids: 指定启动的任务ID列表，为空则启动所有

        Returns:
            操作结果
        """
        async with self._lock:
            scheduler = self.get_scheduler()

            if scheduler.is_running:
                return {
                    'success': False,
                    'message': '监控器已在运行中',
                }

            try:
                # 启动调度器
                success = await scheduler.start()

                if success:
                    status = await self.get_status()
                    return {
                        'success': True,
                        'message': '监控器启动成功',
                        'status': status,
                    }
                else:
                    return {
                        'success': False,
                        'message': '监控器启动失败',
                    }

            except Exception as e:
                return {
                    'success': False,
                    'message': f'启动监控器时发生错误: {str(e)}',
                }

    async def stop(self, force: bool = False, wait_timeout: int = 30) -> Dict[str, Any]:
        """
        停止监控器

        Args:
            force: 是否强制停止
            wait_timeout: 等待超时时间（秒）

        Returns:
            操作结果
        """
        async with self._lock:
            scheduler = self.get_scheduler()

            if not scheduler.is_running:
                return {
                    'success': False,
                    'message': '监控器未在运行',
                }

            try:
                # 停止调度器
                success = await scheduler.stop()

                if success:
                    status = await self.get_status()
                    return {
                        'success': True,
                        'message': '监控器已停止',
                        'status': status,
                    }
                else:
                    return {
                        'success': False,
                        'message': '监控器停止失败',
                    }

            except Exception as e:
                return {
                    'success': False,
                    'message': f'停止监控器时发生错误: {str(e)}',
                }

    async def get_scheduler_stats(self) -> Dict[str, Any]:
        """
        获取调度器统计信息

        Returns:
            调度器统计
        """
        scheduler = self.get_scheduler()
        stats = scheduler.stats
        config = scheduler.get_scheduler_config() if hasattr(scheduler, 'get_scheduler_config') else {}

        start_time = stats.get('start_time')
        uptime = 0.0
        if start_time and isinstance(start_time, datetime):
            uptime = (datetime.now() - start_time).total_seconds()
            start_time = start_time.isoformat()

        return {
            'total_executions': stats.get('total_executions', 0),
            'successful_executions': stats.get('successful_executions', 0),
            'failed_executions': stats.get('failed_executions', 0),
            'total_changes': stats.get('total_changes', 0),
            'start_time': start_time,
            'uptime': uptime,
            'max_concurrent_tasks': config.get('max_concurrent_tasks', 5),
            'default_interval': config.get('default_interval', 300),
        }


# 全局服务实例
monitor_service = MonitorService()


def get_monitor_service() -> MonitorService:
    """获取监控服务实例"""
    return monitor_service


# 保持向后兼容的函数接口
async def get_monitor_status() -> Dict[str, Any]:
    """获取监控器状态（兼容旧接口）"""
    return await monitor_service.get_status()


async def start_monitor() -> Dict[str, Any]:
    """启动监控器（兼容旧接口）"""
    return await monitor_service.start()


async def stop_monitor() -> Dict[str, Any]:
    """停止监控器（兼容旧接口）"""
    return await monitor_service.stop()
