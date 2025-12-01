#!/usr/bin/env python3
"""
任务调度器主类
负责任务的调度、执行和管理
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Callable, Any
from pathlib import Path
import signal
import sys

from webmon.utils.logger import get_logger
from webmon.models.task import Task
from webmon.storage.task_storage import TaskStorage
from webmon.storage.history_storage import HistoryStorage
from webmon.config import ConfigManager
from webmon.browser.resource_manager import ResourceManager
from webmon.browser.browser_engine import BrowserEngine
from webmon.detection.change_detector import ChangeDetector
from webmon.notification.service import NotificationService
from .job_queue import JobQueue
from .execution_engine import ExecutionEngine
from .priority_manager import PriorityManager
from .scheduler_config import SchedulerConfig


class TaskScheduler:
    """任务调度器主类"""
    
    def __init__(self, config_manager: Optional[ConfigManager] = None):
        """初始化任务调度器"""
        self.logger = get_logger(__name__)
        self.config_manager = config_manager or ConfigManager()
        # 使用与ConfigManager相同的配置文件路径
        config_file_path = str(self.config_manager.json_file)
        self.storage = TaskStorage(config_file_path)
        self.history_storage = HistoryStorage()
        
        # 调度器配置 - 使用 ConfigManager 获取调度器配置
        self.scheduler_config = SchedulerConfig.from_config_manager(self.config_manager)
        self.max_concurrent_tasks = self.scheduler_config.max_concurrent_tasks
        self.default_interval = self.scheduler_config.default_interval
        self.retry_attempts = self.scheduler_config.retry_attempts
        self.retry_delay = self.scheduler_config.retry_delay
        
        # 记录调度器配置信息
        self.logger.info(f"任务调度器初始化完成 - 最大并发任务数: {self.max_concurrent_tasks}, 默认间隔: {self.default_interval}秒")

        # 运行状态
        self.is_running = False
        self.scheduler_task: Optional[asyncio.Task] = None
        self.running_tasks: Dict[str, asyncio.Task] = {}
        self.task_last_run: Dict[str, datetime] = {}
        self.task_next_run: Dict[str, datetime] = {}

        # 并发锁保护 running_tasks 的访问
        self._running_tasks_lock = asyncio.Lock()

        # 控制信号
        self._shutdown_event = asyncio.Event()
        self._pause_event = asyncio.Event()

        # 统计信息
        self.stats = {
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'total_changes': 0,
            'start_time': None,
            'uptime': 0
        }

        # 核心组件
        self.job_queue = JobQueue(max_size=self.scheduler_config.max_queue_size)
        self.execution_engine = ExecutionEngine(self.config_manager)
        self.priority_manager = PriorityManager()

        # 资源管理器
        self.resource_manager = ResourceManager(
            config_manager=self.config_manager,
            max_resources=self.scheduler_config.max_browser_resources,
            max_concurrent=self.scheduler_config.max_browser_concurrent
        )

        # 浏览器引擎
        self.browser_engine = BrowserEngine(self.config_manager)

        # 变化检测器
        self.change_detector = ChangeDetector(self.config_manager)

        # 通知服务
        self.notification_service = NotificationService(self.config_manager)

        # 注册信号处理
        self._setup_signal_handlers()

        self.logger.info("任务调度器初始化完成 - 所有组件已加载")
    
    def update_scheduler_config(self, new_config: Dict[str, Any]) -> bool:
        """
        更新调度器配置
        
        Args:
            new_config: 新的调度器配置
            
        Returns:
            是否成功更新
        """
        try:
            # 通过 ConfigManager 更新配置
            if self.config_manager.update_scheduler_config(new_config):
                # 重新加载调度器配置
                self.scheduler_config = SchedulerConfig.from_config_manager(self.config_manager)
                
                # 更新相关属性
                self.max_concurrent_tasks = self.scheduler_config.max_concurrent_tasks
                self.default_interval = self.scheduler_config.default_interval
                self.retry_attempts = self.scheduler_config.retry_attempts
                self.retry_delay = self.scheduler_config.retry_delay
                
                self.logger.info("调度器配置已更新并重新加载")
                return True
            else:
                self.logger.error("调度器配置更新失败")
                return False
                
        except Exception as e:
            self.logger.error(f"更新调度器配置时发生错误: {e}")
            return False
    
    def get_scheduler_config(self) -> Dict[str, Any]:
        """获取当前调度器配置"""
        return self.scheduler_config.to_dict()
    
    def validate_scheduler_config(self, config: Dict[str, Any]) -> bool:
        """
        验证调度器配置

        Args:
            config: 待验证的配置

        Returns:
            是否有效
        """
        try:
            return self.config_manager.validator.validate_scheduler_config(config)
        except Exception as e:
            self.logger.error(f"验证调度器配置失败: {e}")
            return False

    def _setup_signal_handlers(self):
        """设置信号处理"""
        try:
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
            self.logger.info("信号处理程序设置完成")
        except Exception as e:
            self.logger.warning(f"设置信号处理程序失败: {e}")
    
    def _signal_handler(self, signum, frame):
        """信号处理程序"""
        self.logger.info(f"收到信号 {signum}，准备优雅关闭...")
        asyncio.create_task(self.shutdown())
    
    async def start(self) -> bool:
        """启动任务调度器"""
        try:
            self.logger.info("正在启动任务调度器...")
            
            # 检查是否已经在运行
            if self.is_running:
                self.logger.warning("任务调度器已经在运行")
                return False
            
            # 初始化浏览器引擎
            browser_initialized = await self.browser_engine.initialize()
            if not browser_initialized:
                self.logger.error("浏览器引擎初始化失败")
                return False
            
            # 资源管理器不需要初始化，它在构造函数中已经初始化
            
            # 加载所有任务
            await self._load_all_tasks()
            
            # 重置控制信号
            self._shutdown_event.clear()
            self._pause_event.clear()
            
            # 设置运行状态
            self.is_running = True
            self.stats['start_time'] = datetime.now()
            
            # 启动调度循环
            self.scheduler_task = asyncio.create_task(self._scheduler_loop())
            
            self.logger.info("任务调度器启动成功")
            return True
            
        except Exception as e:
            self.logger.error(f"启动任务调度器失败: {e}")
            await self._cleanup()
            return False
    
    async def stop(self) -> bool:
        """停止任务调度器"""
        try:
            self.logger.info("正在停止任务调度器...")
            
            if not self.is_running:
                self.logger.warning("任务调度器未在运行")
                return False
            
            # 设置关闭信号
            self._shutdown_event.set()
            
            # 等待调度循环结束
            if self.scheduler_task:
                try:
                    await asyncio.wait_for(self.scheduler_task, timeout=30.0)
                except asyncio.TimeoutError:
                    self.logger.warning("调度循环超时，强制取消")
                    self.scheduler_task.cancel()
                    try:
                        await self.scheduler_task
                    except asyncio.CancelledError:
                        pass
            
            # 等待所有运行中的任务完成
            await self._wait_for_running_tasks()
            
            # 清理资源
            await self._cleanup()
            
            # 重置运行状态
            self.is_running = False
            self.scheduler_task = None
            
            self.logger.info("任务调度器已停止")
            return True
            
        except Exception as e:
            self.logger.error(f"停止任务调度器失败: {e}")
            return False
    
    async def shutdown(self):
        """优雅关闭"""
        self.logger.info("正在执行优雅关闭...")
        await self.stop()
        sys.exit(0)
    
    async def pause(self):
        """暂停调度器"""
        if self.is_running:
            self._pause_event.set()
            self.logger.info("任务调度器已暂停")
        else:
            self.logger.warning("任务调度器未在运行，无法暂停")
    
    async def resume(self):
        """恢复调度器"""
        if self.is_running:
            self._pause_event.clear()
            self.logger.info("任务调度器已恢复")
        else:
            self.logger.warning("任务调度器未在运行，无法恢复")
    
    async def _load_all_tasks(self):
        """加载所有任务"""
        try:
            self.logger.info("正在加载所有任务...")
            tasks = self.storage.list_tasks()
            
            for task in tasks:
                if task.enabled:
                    await self._schedule_task(task)
            
            self.logger.info(f"成功加载 {len(tasks)} 个任务，其中 {sum(1 for t in tasks if t.enabled)} 个已启用")
            
        except Exception as e:
            self.logger.error(f"加载任务失败: {e}")
            raise
    
    async def _schedule_task(self, task: Task, immediate: bool = False):
        """调度单个任务"""
        try:
            # 计算下次执行时间
            now = datetime.now()
            if immediate:
                next_run = now
            elif task.last_check:
                # 基于上次检测时间计算
                next_run = task.last_check + timedelta(seconds=task.interval)
            else:
                # 新任务，立即执行
                next_run = now
            
            # 如果下次运行时间已过，立即执行
            if next_run <= now:
                next_run = now
            
            # 添加到调度队列
            job = {
                'task': task,
                'next_run': next_run,
                'priority': self.priority_manager.calculate_priority(task),
                'retry_count': 0
            }
            
            await self.job_queue.put(job)
            
            self.task_next_run[task.id] = next_run
            self.logger.debug(f"任务 {task.name} (ID: {task.id}) 已调度，下次运行: {next_run}")
            
        except Exception as e:
            self.logger.error(f"调度任务 {task.name} 失败: {e}")
    
    async def _scheduler_loop(self):
        """主调度循环"""
        self.logger.info("调度循环已启动")
        
        try:
            while not self._shutdown_event.is_set():
                try:
                    # 检查暂停状态
                    if self._pause_event.is_set():
                        await asyncio.sleep(1)
                        continue
                    
                    # 获取当前时间
                    now = datetime.now()
                    
                    # 处理到期的任务
                    ready_jobs = await self.job_queue.get_ready_jobs(now)
                    
                    for job in ready_jobs:
                        task = job['task']

                        # 使用锁保护 running_tasks 的访问
                        async with self._running_tasks_lock:
                            # 检查是否已在运行
                            if task.id in self.running_tasks:
                                self.logger.debug(f"任务 {task.name} 已在运行中，跳过")
                                continue

                            # 检查并发限制
                            if len(self.running_tasks) >= self.max_concurrent_tasks:
                                self.logger.debug(f"并发任务数已达上限 ({self.max_concurrent_tasks})，任务 {task.name} 将等待")
                                # 重新放入队列，稍后重试
                                await self.job_queue.put(job)
                                continue

                            # 启动任务执行
                            task_coro = self._execute_task(task)
                            task_future = asyncio.create_task(task_coro)

                            self.running_tasks[task.id] = task_future
                            self.task_last_run[task.id] = now

                            self.logger.debug(f"任务 {task.name} (ID: {task.id}) 开始执行")
                    
                    # 清理已完成的任务
                    await self._cleanup_completed_tasks()
                    
                    # 更新统计信息
                    self._update_stats()
                    
                    # 短暂休眠，避免CPU占用过高
                    await asyncio.sleep(0.1)
                    
                except Exception as e:
                    self.logger.error(f"调度循环异常: {e}")
                    await asyncio.sleep(1)  # 异常后等待更长时间
                    
        except asyncio.CancelledError:
            self.logger.info("调度循环被取消")
            raise
        except Exception as e:
            self.logger.error(f"调度循环严重异常: {e}")
            raise
        finally:
            self.logger.info("调度循环已停止")
    
    async def _execute_task(self, task: Task):
        """执行单个任务"""
        try:
            self.stats['total_executions'] += 1
            self.logger.info(f"开始执行任务: {task.name} (ID: {task.id})")
            
            # 获取浏览器资源
            resource = await self.resource_manager.acquire_resource(
                user_id=f"task_{task.id}",
                timeout=task.timeout / 1000  # 转换为秒
            )
            
            if not resource:
                raise Exception("无法获取浏览器资源")
            
            try:
                # 执行监控任务
                start_time = datetime.now()
                
                # 获取网页内容
                page_content = await self.browser_engine.get_page_content(
                    url=task.url,
                    selector=task.selectors[0] if task.selectors else None,
                    timeout=task.timeout,
                    resource=resource
                )
                
                if not page_content:
                    raise Exception("无法获取网页内容")
                
                # 检测变化
                check_result = await self.change_detector.detect_changes(
                    task=task,
                    current_content=page_content
                )
                
                # 保存检测结果
                await self.history_storage.add_check_result(task.id, check_result)
                
                # 如果有变化，发送通知
                if check_result.changed:
                    self.stats['total_changes'] += 1
                    
                    # 获取变化详情
                    change_details = await self.change_detector.get_change_details(
                        task=task,
                        old_content=check_result.previous_content,
                        new_content=page_content
                    )
                    
                    # 保存变化详情
                    await self.history_storage.add_change_details(task.id, change_details)
                    
                    # 发送通知
                    await self.notification_service.send_webpage_change_notification(
                        task=task,
                        check_result=check_result,
                        change_details=change_details
                    )
                    
                    self.logger.info(f"任务 {task.name} 检测到变化，已发送通知")
                
                # 更新任务状态
                task.mark_as_checked()
                if check_result.changed:
                    task.mark_as_changed()
                
                # 保存任务更新
                self.storage.update_task(task)
                
                # 记录执行时间
                execution_time = (datetime.now() - start_time).total_seconds()
                self.logger.info(f"任务 {task.name} 执行完成，耗时: {execution_time:.2f}秒")
                
                # 更新统计
                self.stats['successful_executions'] += 1
                
            finally:
                # 释放资源
                await self.resource_manager.release_resource(resource)
                
        except Exception as e:
            self.stats['failed_executions'] += 1
            self.logger.error(f"任务 {task.name} 执行失败: {e}")
            
            # 失败处理
            await self._handle_task_failure(task, e)
            
        finally:
            # 从运行中任务列表移除（使用锁保护）
            async with self._running_tasks_lock:
                if task.id in self.running_tasks:
                    del self.running_tasks[task.id]

            # 重新调度任务（如果还在运行）
            if self.is_running and not self._shutdown_event.is_set():
                try:
                    await self._schedule_task(task)
                except Exception as e:
                    self.logger.error(f"重新调度任务 {task.name} 失败: {e}")
    
    async def _handle_task_failure(self, task: Task, error: Exception):
        """处理任务失败"""
        try:
            # 获取失败次数
            retry_count = getattr(task, 'retry_count', 0)
            
            if retry_count < self.retry_attempts:
                # 重试任务
                retry_count += 1
                task.retry_count = retry_count
                
                # 计算重试延迟（指数退避）
                retry_delay = self.retry_delay * (2 ** (retry_count - 1))
                
                self.logger.warning(f"任务 {task.name} 将在 {retry_delay} 秒后重试 (第 {retry_count} 次)")
                
                # 创建重试任务
                retry_job = {
                    'task': task,
                    'next_run': datetime.now() + timedelta(seconds=retry_delay),
                    'priority': self.priority_manager.calculate_priority(task) + 10,  # 降低优先级
                    'retry_count': retry_count
                }
                
                await self.job_queue.put(retry_job)
                
            else:
                # 达到最大重试次数，标记为失败
                task.set_status('error')
                self.storage.update_task(task)
                
                # 发送错误通知
                await self.notification_service.send_error_notification(
                    task=task,
                    error_message=str(error)
                )
                
                self.logger.error(f"任务 {task.name} 达到最大重试次数，标记为失败状态")
                
        except Exception as e:
            self.logger.error(f"处理任务失败时出错: {e}")
    
    async def _cleanup_completed_tasks(self):
        """清理已完成的任务"""
        # 使用锁保护 running_tasks 的访问
        async with self._running_tasks_lock:
            completed_tasks = []

            for task_id, task_future in self.running_tasks.items():
                if task_future.done():
                    completed_tasks.append(task_id)

                    # 检查是否有异常
                    try:
                        task_future.result()
                    except Exception as e:
                        self.logger.error(f"任务 {task_id} 异常完成: {e}")

            # 移除已完成的任务
            for task_id in completed_tasks:
                del self.running_tasks[task_id]
    
    async def _wait_for_running_tasks(self, timeout: float = 30.0):
        """等待所有运行中的任务完成"""
        # 使用锁保护对 running_tasks 的访问
        async with self._running_tasks_lock:
            if not self.running_tasks:
                return

            self.logger.info(f"等待 {len(self.running_tasks)} 个运行中的任务完成...")

            # 创建任务列表的副本
            tasks_to_wait = list(self.running_tasks.values())

        # 在锁外等待任务（避免长时间持有锁）
        try:
            # 等待所有任务完成
            await asyncio.wait(
                tasks_to_wait,
                timeout=timeout,
                return_when=asyncio.ALL_COMPLETED
            )

            # 取消仍在运行的任务
            async with self._running_tasks_lock:
                for task_future in self.running_tasks.values():
                    if not task_future.done():
                        task_future.cancel()

            self.logger.info("所有运行中的任务已处理完成")

        except Exception as e:
            self.logger.error(f"等待任务完成时出错: {e}")
    
    async def _cleanup(self):
        """清理资源"""
        try:
            self.logger.info("正在清理调度器资源...")
            
            # 清理浏览器引擎
            await self.browser_engine.cleanup()
            
            # 资源管理器不需要清理，它在析构函数中自动清理
            
            # 清理任务队列
            await self.job_queue.clear()
            
            self.logger.info("调度器资源清理完成")
            
        except Exception as e:
            self.logger.error(f"清理资源失败: {e}")
    
    def _update_stats(self):
        """更新统计信息"""
        if self.stats['start_time']:
            self.stats['uptime'] = (datetime.now() - self.stats['start_time']).total_seconds()
    
    # 公共API方法
    
    def get_status(self) -> Dict[str, Any]:
        """获取调度器状态"""
        # 创建 running_tasks 的快照以避免并发问题
        try:
            running_tasks_count = len(self.running_tasks)
        except RuntimeError:
            # 字典在迭代过程中被修改
            running_tasks_count = 0

        return {
            'is_running': self.is_running,
            'total_tasks': len(self.storage.list_tasks()),
            'enabled_tasks': len([t for t in self.storage.list_tasks() if t.enabled]),
            'running_tasks': running_tasks_count,
            'queued_tasks': self.job_queue.size(),
            'stats': self.stats.copy(),
            'uptime': self.stats['uptime']
        }

    def get_running_tasks(self) -> List[Dict[str, Any]]:
        """获取正在运行的任务"""
        running_tasks_info = []

        # 创建 running_tasks 的副本以避免并发修改问题
        try:
            running_tasks_snapshot = list(self.running_tasks.items())
        except RuntimeError:
            # 字典在迭代过程中被修改，返回空列表
            return running_tasks_info

        for task_id, task_future in running_tasks_snapshot:
            task = self.storage.get_task(task_id)
            if task:
                running_tasks_info.append({
                    'id': task.id,
                    'name': task.name,
                    'url': task.url,
                    'start_time': self.task_last_run.get(task_id),
                    'status': 'running' if not task_future.done() else 'completed'
                })

        return running_tasks_info
    
    async def add_task(self, task: Task) -> bool:
        """动态添加任务"""
        try:
            # 保存任务到存储
            success = self.storage.add_task(task)
            if success and self.is_running:
                # 如果调度器在运行，立即调度新任务
                await self._schedule_task(task, immediate=True)
                self.logger.info(f"动态添加任务成功: {task.name}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"动态添加任务失败: {e}")
            return False
    
    async def remove_task(self, task_id: str) -> bool:
        """动态移除任务"""
        try:
            # 获取任务信息
            task = self.storage.get_task(task_id)
            if not task:
                return False

            # 如果任务正在运行，取消执行（使用锁保护）
            async with self._running_tasks_lock:
                if task_id in self.running_tasks:
                    task_future = self.running_tasks[task_id]
                    if not task_future.done():
                        task_future.cancel()
                    del self.running_tasks[task_id]

            # 从队列中移除
            await self.job_queue.remove_task(task_id)

            # 从存储中删除
            success = self.storage.remove_task(task_id)
            
            # 清理相关数据
            if task_id in self.task_last_run:
                del self.task_last_run[task_id]
            if task_id in self.task_next_run:
                del self.task_next_run[task_id]
            
            if success:
                self.logger.info(f"动态移除任务成功: {task.name}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"动态移除任务失败: {e}")
            return False