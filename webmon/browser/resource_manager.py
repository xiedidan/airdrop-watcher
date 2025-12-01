"""
浏览器资源管理器

管理浏览器实例池，控制并发数量，优化资源使用。
"""
import asyncio
import logging
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from .browser_engine import BrowserEngine
from ..exceptions import ResourceError, ConcurrentError
from ..utils.logger import get_logger


class ResourceStatus(Enum):
    """资源状态枚举"""
    IDLE = "idle"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"
    ERROR = "error"
    CLOSED = "closed"


@dataclass
class ResourceMetrics:
    """资源使用指标"""
    created_at: datetime = field(default_factory=datetime.now)
    last_used: Optional[datetime] = None
    use_count: int = 0
    total_usage_time: float = 0.0
    error_count: int = 0
    average_response_time: float = 0.0
    memory_usage: Optional[int] = None
    
    def update_usage(self, usage_time: float, response_time: float):
        """更新使用统计"""
        self.use_count += 1
        self.total_usage_time += usage_time
        self.last_used = datetime.now()
        
        # 更新平均响应时间
        if self.average_response_time == 0:
            self.average_response_time = response_time
        else:
            self.average_response_time = (
                (self.average_response_time * (self.use_count - 1) + response_time) / self.use_count
            )
    
    def record_error(self):
        """记录错误"""
        self.error_count += 1
    
    def get_utilization_rate(self) -> float:
        """获取资源利用率"""
        if self.use_count == 0:
            return 0.0
        
        lifetime = (datetime.now() - self.created_at).total_seconds()
        if lifetime == 0:
            return 0.0
        
        return min(self.total_usage_time / lifetime, 1.0)


class BrowserResource:
    """浏览器资源包装类"""
    
    def __init__(self, browser_engine: BrowserEngine, resource_id: str):
        """
        初始化浏览器资源
        
        Args:
            browser_engine: 浏览器引擎实例
            resource_id: 资源ID
        """
        self.browser_engine = browser_engine
        self.resource_id = resource_id
        self.status = ResourceStatus.IDLE
        self.metrics = ResourceMetrics()
        self.in_use_since: Optional[datetime] = None
        self.current_user: Optional[str] = None
        self.logger = get_logger(__name__)
    
    async def acquire(self, user_id: str) -> bool:
        """
        获取资源使用权
        
        Args:
            user_id: 用户ID
            
        Returns:
            是否成功获取
        """
        if self.status != ResourceStatus.IDLE:
            return False
        
        self.status = ResourceStatus.IN_USE
        self.current_user = user_id
        self.in_use_since = datetime.now()
        
        self.logger.debug(f"资源 {self.resource_id} 被用户 {user_id} 获取")
        return True
    
    async def release(self) -> bool:
        """
        释放资源使用权
        
        Returns:
            是否成功释放
        """
        if self.status != ResourceStatus.IN_USE:
            return False
        
        # 计算使用时间
        if self.in_use_since:
            usage_time = (datetime.now() - self.in_use_since).total_seconds()
            # 假设响应时间为使用时间的一半（简化计算）
            response_time = usage_time / 2
            self.metrics.update_usage(usage_time, response_time)
        
        self.status = ResourceStatus.IDLE
        self.current_user = None
        self.in_use_since = None
        
        self.logger.debug(f"资源 {self.resource_id} 已释放")
        return True
    
    async def mark_error(self, error_message: str):
        """
        标记资源为错误状态
        
        Args:
            error_message: 错误信息
        """
        self.status = ResourceStatus.ERROR
        self.metrics.record_error()
        self.logger.error(f"资源 {self.resource_id} 发生错误: {error_message}")
    
    async def mark_maintenance(self):
        """标记资源为维护状态"""
        self.status = ResourceStatus.MAINTENANCE
        self.logger.info(f"资源 {self.resource_id} 进入维护状态")
    
    async def close(self):
        """关闭资源"""
        self.status = ResourceStatus.CLOSED
        if self.browser_engine:
            await self.browser_engine.cleanup()
        self.logger.info(f"资源 {self.resource_id} 已关闭")
    
    def is_healthy(self) -> bool:
        """
        检查资源是否健康
        
        Returns:
            是否健康
        """
        if self.status in [ResourceStatus.ERROR, ResourceStatus.CLOSED]:
            return False
        
        # 错误率检查
        if self.metrics.use_count > 0 and self.metrics.error_count / self.metrics.use_count > 0.2:
            return False  # 错误率超过20%
        
        return True
    
    def get_info(self) -> Dict[str, Any]:
        """
        获取资源信息
        
        Returns:
            资源信息字典
        """
        return {
            "resource_id": self.resource_id,
            "status": self.status.value,
            "current_user": self.current_user,
            "in_use_since": self.in_use_since.isoformat() if self.in_use_since else None,
            "is_healthy": self.is_healthy(),
            "metrics": {
                "created_at": self.metrics.created_at.isoformat(),
                "last_used": self.metrics.last_used.isoformat() if self.metrics.last_used else None,
                "use_count": self.metrics.use_count,
                "total_usage_time": self.metrics.total_usage_time,
                "error_count": self.metrics.error_count,
                "average_response_time": self.metrics.average_response_time,
                "utilization_rate": self.metrics.get_utilization_rate()
            }
        }


class ResourceManager:
    """浏览器资源管理器"""
    
    def __init__(self, config_manager, max_resources: int = 5, max_concurrent: int = 3):
        """
        初始化资源管理器
        
        Args:
            config_manager: 配置管理器
            max_resources: 最大资源数量
            max_concurrent: 最大并发数
        """
        self.config_manager = config_manager
        self.max_resources = max_resources
        self.max_concurrent = max_concurrent
        
        self.resources: Dict[str, BrowserResource] = {}
        self.resource_semaphore = asyncio.Semaphore(max_concurrent)
        self.resource_counter = 0
        
        # 监控相关
        self.monitoring_enabled = True
        self.cleanup_interval = 300  # 5分钟清理一次
        self.max_idle_time = 1800  # 30分钟空闲后回收
        
        self.logger = get_logger(__name__)

        # 监控任务（延迟启动）
        self._monitoring_task = None

        # 启动监控任务（仅当有运行的事件循环时）
        if self.monitoring_enabled:
            try:
                loop = asyncio.get_running_loop()
                self._monitoring_task = asyncio.create_task(self._monitoring_loop())
            except RuntimeError:
                # 没有运行的事件循环，稍后启动
                self.logger.debug("没有运行的事件循环，监控任务将在首次使用时启动")

    async def _ensure_monitoring_started(self):
        """确保监控任务已启动"""
        if self.monitoring_enabled and self._monitoring_task is None:
            try:
                self._monitoring_task = asyncio.create_task(self._monitoring_loop())
            except Exception as e:
                self.logger.warning(f"启动监控任务失败: {e}")
    
    async def acquire_resource(self, user_id: str, timeout: Optional[float] = None) -> Optional[BrowserResource]:
        """
        获取浏览器资源
        
        Args:
            user_id: 用户ID
            timeout: 超时时间（秒）
            
        Returns:
            浏览器资源，获取失败返回None
            
        Raises:
            ConcurrentError: 并发限制错误
            ResourceError: 资源获取失败
        """
        start_time = time.time()
        
        try:
            # 获取并发信号量
            async with self.resource_semaphore:
                # 查找可用资源
                resource = await self._find_available_resource()
                
                if resource:
                    # 获取资源
                    if await resource.acquire(user_id):
                        self.logger.info(f"用户 {user_id} 成功获取资源 {resource.resource_id}")
                        return resource
                    else:
                        raise ResourceError(f"资源获取失败: {resource.resource_id}")
                
                # 创建新资源
                if len(self.resources) < self.max_resources:
                    resource = await self._create_resource()
                    if resource and await resource.acquire(user_id):
                        self.logger.info(f"用户 {user_id} 成功创建并获取新资源 {resource.resource_id}")
                        return resource
                
                # 等待可用资源
                if timeout is None:
                    timeout = 30.0  # 默认30秒超时
                
                while time.time() - start_time < timeout:
                    resource = await self._find_available_resource()
                    if resource and await resource.acquire(user_id):
                        self.logger.info(f"用户 {user_id} 成功获取资源 {resource.resource_id}")
                        return resource
                    
                    await asyncio.sleep(0.5)
                
                # 超时
                raise ConcurrentError(
                    f"获取资源超时，最大并发数: {self.max_concurrent}, "
                    f"最大资源数: {self.max_resources}"
                )
        
        except ConcurrentError:
            raise
        except Exception as e:
            self.logger.error(f"获取资源失败: {e}")
            raise ResourceError(f"获取资源失败: {e}")
    
    async def release_resource(self, resource: BrowserResource) -> bool:
        """
        释放浏览器资源
        
        Args:
            resource: 要释放的资源
            
        Returns:
            是否成功释放
        """
        try:
            success = await resource.release()
            if success:
                self.logger.info(f"资源 {resource.resource_id} 已释放")
            return success
        except Exception as e:
            self.logger.error(f"释放资源失败: {e}")
            return False
    
    async def _find_available_resource(self) -> Optional[BrowserResource]:
        """
        查找可用资源
        
        Returns:
            可用资源，没有则返回None
        """
        # 优先选择空闲且健康的资源
        for resource in self.resources.values():
            if (resource.status == ResourceStatus.IDLE and 
                resource.is_healthy()):
                return resource
        
        return None
    
    async def _create_resource(self) -> Optional[BrowserResource]:
        """
        创建新资源
        
        Returns:
            新创建的资源，创建失败返回None
        """
        try:
            self.resource_counter += 1
            resource_id = f"browser_resource_{self.resource_counter}"
            
            # 创建浏览器引擎
            browser_engine = BrowserEngine(self.config_manager)
            await browser_engine.initialize()
            
            # 创建资源包装
            resource = BrowserResource(browser_engine, resource_id)
            self.resources[resource_id] = resource
            
            self.logger.info(f"创建新资源: {resource_id}")
            return resource
            
        except Exception as e:
            self.logger.error(f"创建资源失败: {e}")
            return None
    
    async def _monitoring_loop(self):
        """监控循环"""
        while self.monitoring_enabled:
            try:
                await asyncio.sleep(self.cleanup_interval)
                await self._perform_maintenance()
            except Exception as e:
                self.logger.error(f"监控循环错误: {e}")
    
    async def _perform_maintenance(self):
        """执行维护任务"""
        self.logger.info("开始资源维护...")
        
        # 清理空闲过久的资源
        resources_to_remove = []
        
        for resource_id, resource in self.resources.items():
            # 检查是否需要回收
            if (resource.status == ResourceStatus.IDLE and 
                resource.metrics.last_used and
                (datetime.now() - resource.metrics.last_used).total_seconds() > self.max_idle_time):
                resources_to_remove.append(resource_id)
                continue
            
            # 检查不健康资源
            if not resource.is_healthy():
                self.logger.warning(f"资源 {resource_id} 不健康，准备回收")
                resources_to_remove.append(resource_id)
                continue
        
        # 移除需要回收的资源
        for resource_id in resources_to_remove:
            await self._remove_resource(resource_id)
        
        # 报告统计信息
        stats = await self.get_statistics()
        self.logger.info(f"资源维护完成 - 活跃资源: {stats['active_resources']}, "
                        f"空闲资源: {stats['idle_resources']}, 已回收: {len(resources_to_remove)}")
    
    async def _remove_resource(self, resource_id: str):
        """
        移除资源
        
        Args:
            resource_id: 资源ID
        """
        resource = self.resources.get(resource_id)
        if resource:
            try:
                await resource.close()
                del self.resources[resource_id]
                self.logger.info(f"资源 {resource_id} 已移除")
            except Exception as e:
                self.logger.error(f"移除资源失败 {resource_id}: {e}")
    
    async def get_statistics(self) -> Dict[str, Any]:
        """
        获取资源统计信息
        
        Returns:
            统计信息字典
        """
        total_resources = len(self.resources)
        idle_resources = sum(1 for r in self.resources.values() if r.status == ResourceStatus.IDLE)
        active_resources = sum(1 for r in self.resources.values() if r.status == ResourceStatus.IN_USE)
        error_resources = sum(1 for r in self.resources.values() if r.status == ResourceStatus.ERROR)
        
        total_use_count = sum(r.metrics.use_count for r in self.resources.values())
        total_error_count = sum(r.metrics.error_count for r in self.resources.values())
        average_response_time = (
            sum(r.metrics.average_response_time for r in self.resources.values() if r.metrics.use_count > 0) / 
            max(sum(1 for r in self.resources.values() if r.metrics.use_count > 0), 1)
        )
        
        return {
            "total_resources": total_resources,
            "idle_resources": idle_resources,
            "active_resources": active_resources,
            "error_resources": error_resources,
            "max_resources": self.max_resources,
            "max_concurrent": self.max_concurrent,
            "total_use_count": total_use_count,
            "total_error_count": total_error_count,
            "error_rate": total_error_count / max(total_use_count, 1),
            "average_response_time": average_response_time
        }
    
    def get_resource_info(self) -> List[Dict[str, Any]]:
        """
        获取所有资源信息
        
        Returns:
            资源信息列表
        """
        return [resource.get_info() for resource in self.resources.values()]
    
    async def shutdown(self):
        """关闭资源管理器"""
        self.monitoring_enabled = False
        
        # 关闭所有资源
        for resource in self.resources.values():
            try:
                await resource.close()
            except Exception as e:
                self.logger.error(f"关闭资源失败: {e}")
        
        self.resources.clear()
        self.logger.info("资源管理器已关闭")


class ResourcePool:
    """简化的资源池实现"""
    
    def __init__(self, config_manager, max_resources: int = 3):
        """
        初始化资源池
        
        Args:
            config_manager: 配置管理器
            max_resources: 最大资源数
        """
        self.config_manager = config_manager
        self.max_resources = max_resources
        self.resources: List[BrowserResource] = []
        self.semaphore = asyncio.Semaphore(max_resources)
        self.lock = asyncio.Lock()
        self.logger = get_logger(__name__)
        
        # 预创建资源
        asyncio.create_task(self._pre_create_resources())
    
    async def _pre_create_resources(self):
        """预创建资源"""
        try:
            for i in range(min(2, self.max_resources)):  # 预创建2个资源或最大资源数
                resource = await self._create_resource(f"pre_created_{i}")
                if resource:
                    self.resources.append(resource)
        except Exception as e:
            self.logger.error(f"预创建资源失败: {e}")
    
    async def _create_resource(self, resource_id: str) -> Optional[BrowserResource]:
        """创建资源"""
        try:
            browser_engine = BrowserEngine(self.config_manager)
            await browser_engine.initialize()
            return BrowserResource(browser_engine, resource_id)
        except Exception as e:
            self.logger.error(f"创建资源失败: {e}")
            return None
    
    async def acquire(self, user_id: str, timeout: float = 30.0) -> Optional[BrowserResource]:
        """获取资源"""
        async with self.semaphore:
            async with self.lock:
                # 查找空闲资源
                for resource in self.resources:
                    if resource.status == ResourceStatus.IDLE and await resource.acquire(user_id):
                        return resource
                
                # 创建新资源
                if len(self.resources) < self.max_resources:
                    resource_id = f"pool_resource_{len(self.resources)}"
                    resource = await self._create_resource(resource_id)
                    if resource and await resource.acquire(user_id):
                        self.resources.append(resource)
                        return resource
            
            # 等待可用资源
            start_time = time.time()
            while time.time() - start_time < timeout:
                async with self.lock:
                    for resource in self.resources:
                        if resource.status == ResourceStatus.IDLE and await resource.acquire(user_id):
                            return resource
                await asyncio.sleep(0.1)
            
            return None
    
    async def release(self, resource: BrowserResource) -> bool:
        """释放资源"""
        return await resource.release()
    
    async def cleanup(self):
        """清理资源池"""
        for resource in self.resources:
            await resource.close()
        self.resources.clear()