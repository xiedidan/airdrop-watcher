#!/usr/bin/env python3
"""
任务执行引擎
负责任务的实际执行，集成浏览器、检测器、通知等组件
"""

import asyncio
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass

from webmon.utils.logger import get_logger
from webmon.models.task import Task
from webmon.models.check_result import CheckResult
from webmon.models.change_details import ChangeDetails


@dataclass
class ExecutionContext:
    """执行上下文"""
    task: Task
    resource: Any  # 浏览器资源
    start_time: datetime
    timeout: float
    retry_count: int = 0
    attempt_count: int = 1


@dataclass 
class ExecutionResult:
    """执行结果"""
    success: bool
    task_id: str
    execution_time: float
    check_result: Optional[CheckResult] = None
    change_details: Optional[ChangeDetails] = None
    error_message: Optional[str] = None
    resource_usage: Dict[str, Any] = None


class ExecutionEngine:
    """任务执行引擎"""
    
    def __init__(self, config_manager):
        """初始化执行引擎"""
        self.logger = get_logger(__name__)
        self.config_manager = config_manager
        
        # 执行统计
        self.stats = {
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'total_changes': 0,
            'average_execution_time': 0.0,
            'resource_acquisition_time': 0.0
        }
        
        # 执行钩子
        self.before_execution_hooks: List[Callable] = []
        self.after_execution_hooks: List[Callable] = []
        self.on_change_hooks: List[Callable] = []
        self.on_error_hooks: List[Callable] = []
        
        # 执行超时配置
        self.default_timeout = 30.0  # 秒
        self.max_execution_time = 300.0  # 最大执行时间 5分钟
        
        self.logger.info("任务执行引擎初始化完成")
    
    async def execute_task(self, task: Task, resource: Any, 
                          browser_engine: Any, change_detector: Any,
                          notification_service: Any, storage: Any,
                          history_storage: Any) -> ExecutionResult:
        """执行单个任务"""
        start_time = time.time()
        execution_start = datetime.now()
        
        try:
            self.stats['total_executions'] += 1
            self.logger.info(f"开始执行任务: {task.name} (ID: {task.id})")
            
            # 创建执行上下文
            context = ExecutionContext(
                task=task,
                resource=resource,
                start_time=execution_start,
                timeout=min(task.timeout / 1000, self.max_execution_time)  # 转换为秒
            )
            
            # 执行前钩子
            await self._run_before_hooks(context)
            
            # 实际执行任务
            result = await self._do_execute(
                context=context,
                browser_engine=browser_engine,
                change_detector=change_detector,
                notification_service=notification_service,
                storage=storage,
                history_storage=history_storage
            )
            
            # 执行后钩子
            await self._run_after_hooks(context, result)
            
            # 更新统计
            execution_time = time.time() - start_time
            result.execution_time = execution_time
            
            self._update_stats(result)
            
            if result.success:
                self.stats['successful_executions'] += 1
                self.logger.info(f"任务 {task.name} 执行成功，耗时: {execution_time:.2f}秒")
            else:
                self.stats['failed_executions'] += 1
                self.logger.error(f"任务 {task.name} 执行失败: {result.error_message}")
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.stats['failed_executions'] += 1
            
            self.logger.error(f"任务 {task.name} 执行异常: {e}")
            
            # 创建失败结果
            result = ExecutionResult(
                success=False,
                task_id=task.id,
                execution_time=execution_time,
                error_message=str(e)
            )
            
            # 错误钩子
            await self._run_error_hooks(context, e)
            
            return result
    
    async def _do_execute(self, context: ExecutionContext,
                         browser_engine: Any, change_detector: Any,
                         notification_service: Any, storage: Any,
                         history_storage: Any) -> ExecutionResult:
        """实际执行任务"""
        task = context.task
        resource = context.resource
        
        try:
            # 1. 获取网页内容
            self.logger.debug(f"正在获取网页内容: {task.url}")
            
            page_content = await self._get_page_content(
                task=task,
                browser_engine=browser_engine,
                resource=resource,
                timeout=context.timeout
            )
            
            if not page_content:
                raise Exception("无法获取网页内容")
            
            # 2. 检测变化
            self.logger.debug(f"正在检测变化: {task.name}")
            
            check_result = await self._detect_changes(
                task=task,
                current_content=page_content,
                change_detector=change_detector
            )
            
            # 3. 保存检测结果
            await self._save_check_result(
                task_id=task.id,
                check_result=check_result,
                history_storage=history_storage
            )
            
            change_details = None
            
            # 4. 处理变化
            if check_result.changed:
                self.stats['total_changes'] += 1
                
                self.logger.info(f"任务 {task.name} 检测到变化")
                
                # 获取变化详情
                change_details = await self._get_change_details(
                    task=task,
                    check_result=check_result,
                    change_detector=change_detector
                )
                
                # 保存变化详情
                await self._save_change_details(
                    task_id=task.id,
                    change_details=change_details,
                    history_storage=history_storage
                )
                
                # 发送通知
                await self._send_notification(
                    task=task,
                    check_result=check_result,
                    change_details=change_details,
                    notification_service=notification_service
                )
                
                # 变化钩子
                await self._run_change_hooks(context, check_result, change_details)
            
            # 5. 更新任务状态
            await self._update_task_status(
                task=task,
                check_result=check_result,
                storage=storage
            )
            
            # 6. 收集资源使用信息
            resource_usage = await self._collect_resource_usage(resource)
            
            # 创建成功结果
            result = ExecutionResult(
                success=True,
                task_id=task.id,
                execution_time=0,  # 将在外层设置
                check_result=check_result,
                change_details=change_details,
                resource_usage=resource_usage
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"任务执行过程中出错: {e}")
            raise
    
    async def _get_page_content(self, task: Task, browser_engine: Any, 
                               resource: Any, timeout: float) -> Optional[str]:
        """获取网页内容"""
        try:
            # 设置超时
            import asyncio
            
            # 使用asyncio.wait_for实现超时控制
            content = await asyncio.wait_for(
                browser_engine.get_page_content(
                    url=task.url,
                    selector=task.selectors[0] if task.selectors else None,
                    timeout=int(timeout * 1000),  # 转换为毫秒
                    resource=resource
                ),
                timeout=timeout
            )
            
            return content
            
        except asyncio.TimeoutError:
            self.logger.error(f"获取网页内容超时: {task.url} (超时: {timeout}秒)")
            raise Exception(f"获取网页内容超时: {timeout}秒")
            
        except Exception as e:
            self.logger.error(f"获取网页内容失败: {task.url} - {e}")
            raise
    
    async def _detect_changes(self, task: Task, current_content: str, 
                            change_detector: Any) -> CheckResult:
        """检测变化"""
        try:
            check_result = await change_detector.detect_changes(
                task=task,
                current_content=current_content
            )
            
            if not check_result:
                raise Exception("变化检测返回空结果")
            
            return check_result
            
        except Exception as e:
            self.logger.error(f"变化检测失败: {task.name} - {e}")
            raise
    
    async def _save_check_result(self, task_id: str, check_result: CheckResult,
                               history_storage: Any):
        """保存检测结果"""
        try:
            success = await history_storage.add_check_result(task_id, check_result)
            if not success:
                self.logger.warning(f"保存检测结果失败: {task_id}")
                
        except Exception as e:
            self.logger.error(f"保存检测结果异常: {e}")
    
    async def _get_change_details(self, task: Task, check_result: CheckResult,
                                change_detector: Any) -> ChangeDetails:
        """获取变化详情"""
        try:
            if not check_result.previous_content:
                # 首次检测，没有历史内容
                return ChangeDetails(
                    task_id=task.id,
                    similarity=0.0,
                    change_count=0,
                    changes={'summary': '首次检测，无历史数据'},
                    old_hash='',
                    new_hash=check_result.content_hash
                )
            
            change_details = await change_detector.get_change_details(
                task=task,
                old_content=check_result.previous_content,
                new_content=check_result.content
            )
            
            if not change_details:
                raise Exception("获取变化详情返回空结果")
            
            return change_details
            
        except Exception as e:
            self.logger.error(f"获取变化详情失败: {task.name} - {e}")
            raise
    
    async def _save_change_details(self, task_id: str, change_details: ChangeDetails,
                                 history_storage: Any):
        """保存变化详情"""
        try:
            success = await history_storage.add_change_details(task_id, change_details)
            if not success:
                self.logger.warning(f"保存变化详情失败: {task_id}")
                
        except Exception as e:
            self.logger.error(f"保存变化详情异常: {e}")
    
    async def _send_notification(self, task: Task, check_result: CheckResult,
                               change_details: ChangeDetails, notification_service: Any):
        """发送通知"""
        try:
            success = await notification_service.send_webpage_change_notification(
                task=task,
                check_result=check_result,
                change_details=change_details
            )
            
            if success:
                self.logger.info(f"变化通知发送成功: {task.name}")
            else:
                self.logger.warning(f"变化通知发送失败: {task.name}")
                
        except Exception as e:
            self.logger.error(f"发送通知异常: {task.name} - {e}")
    
    async def _update_task_status(self, task: Task, check_result: CheckResult, storage: Any):
        """更新任务状态"""
        try:
            # 更新任务状态
            task.mark_as_checked()
            if check_result.changed:
                task.mark_as_changed()
            
            # 保存任务更新
            success = storage.update_task(task)
            if not success:
                self.logger.warning(f"更新任务状态失败: {task.id}")
                
        except Exception as e:
            self.logger.error(f"更新任务状态异常: {e}")
    
    async def _collect_resource_usage(self, resource: Any) -> Dict[str, Any]:
        """收集资源使用信息"""
        try:
            # 这里可以扩展收集更多资源使用信息
            return {
                'resource_id': getattr(resource, 'id', 'unknown'),
                'memory_usage': getattr(resource, 'memory_usage', None),
                'cpu_usage': getattr(resource, 'cpu_usage', None),
                'uptime': getattr(resource, 'uptime', None)
            }
            
        except Exception as e:
            self.logger.warning(f"收集资源使用信息失败: {e}")
            return {}
    
    # 钩子系统
    
    def add_before_execution_hook(self, hook: Callable):
        """添加执行前钩子"""
        self.before_execution_hooks.append(hook)
    
    def add_after_execution_hook(self, hook: Callable):
        """添加执行后钩子"""
        self.after_execution_hooks.append(hook)
    
    def add_on_change_hook(self, hook: Callable):
        """添加变化钩子"""
        self.on_change_hooks.append(hook)
    
    def add_on_error_hook(self, hook: Callable):
        """添加错误钩子"""
        self.on_error_hooks.append(hook)
    
    async def _run_before_hooks(self, context: ExecutionContext):
        """运行执行前钩子"""
        for hook in self.before_execution_hooks:
            try:
                if asyncio.iscoroutinefunction(hook):
                    await hook(context)
                else:
                    hook(context)
            except Exception as e:
                self.logger.warning(f"执行前钩子异常: {e}")
    
    async def _run_after_hooks(self, context: ExecutionContext, result: ExecutionResult):
        """运行执行后钩子"""
        for hook in self.after_execution_hooks:
            try:
                if asyncio.iscoroutinefunction(hook):
                    await hook(context, result)
                else:
                    hook(context, result)
            except Exception as e:
                self.logger.warning(f"执行后钩子异常: {e}")
    
    async def _run_change_hooks(self, context: ExecutionContext, 
                              check_result: CheckResult, change_details: ChangeDetails):
        """运行变化钩子"""
        for hook in self.on_change_hooks:
            try:
                if asyncio.iscoroutinefunction(hook):
                    await hook(context, check_result, change_details)
                else:
                    hook(context, check_result, change_details)
            except Exception as e:
                self.logger.warning(f"变化钩子异常: {e}")
    
    async def _run_error_hooks(self, context: ExecutionContext, error: Exception):
        """运行错误钩子"""
        for hook in self.on_error_hooks:
            try:
                if asyncio.iscoroutinefunction(hook):
                    await hook(context, error)
                else:
                    hook(context, error)
            except Exception as e:
                self.logger.warning(f"错误钩子异常: {e}")
    
    # 统计和监控
    
    def _update_stats(self, result: ExecutionResult):
        """更新统计信息"""
        try:
            # 更新总执行次数
            self.stats['total_executions'] += 1
            
            # 更新成功/失败次数
            if result.success:
                self.stats['successful_executions'] += 1
            else:
                self.stats['failed_executions'] += 1
            
            # 更新变化次数
            if result.check_result and result.check_result.changed:
                self.stats['total_changes'] += 1
            
            # 更新平均执行时间
            if result.execution_time > 0:
                current_avg = self.stats['average_execution_time']
                total_success = self.stats['successful_executions']
                self.stats['average_execution_time'] = (
                    (current_avg * (total_success - 1) + result.execution_time) / total_success
                )
            
        except Exception as e:
            self.logger.error(f"更新统计信息失败: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取执行引擎统计信息"""
        return self.stats.copy()
    
    def reset_stats(self):
        """重置统计信息"""
        self.stats = {
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'total_changes': 0,
            'average_execution_time': 0.0,
            'resource_acquisition_time': 0.0
        }