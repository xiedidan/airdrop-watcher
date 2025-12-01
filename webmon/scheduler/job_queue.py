#!/usr/bin/env python3
"""
任务队列管理
管理待执行的任务队列，支持优先级和时间调度
"""

import asyncio
import heapq
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field

from webmon.utils.logger import get_logger


@dataclass
class Job:
    """任务作业"""
    task: Any  # Task对象
    next_run: datetime
    priority: int = 0
    retry_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    
    def __lt__(self, other):
        """比较函数，用于优先队列排序"""
        # 先按下次运行时间排序，再按优先级排序
        if self.next_run != other.next_run:
            return self.next_run < other.next_run
        return self.priority < other.priority


class JobQueue:
    """任务队列管理器"""
    
    def __init__(self, max_size: int = 1000):
        """初始化任务队列"""
        self.logger = get_logger(__name__)
        self.max_size = max_size
        
        # 优先队列（最小堆）
        self._queue: List[Job] = []
        
        # 任务索引，用于快速查找
        self._task_index: Dict[str, Job] = {}
        
        # 队列锁
        self._lock = asyncio.Lock()
        
        # 统计信息
        self.stats = {
            'total_added': 0,
            'total_processed': 0,
            'total_removed': 0,
            'current_size': 0
        }
        
        self.logger.info(f"任务队列初始化完成，最大容量: {max_size}")
    
    async def put(self, job_data: Dict[str, Any]) -> bool:
        """添加任务到队列"""
        try:
            async with self._lock:
                # 检查队列是否已满
                if len(self._queue) >= self.max_size:
                    self.logger.warning(f"任务队列已满 ({self.max_size})，无法添加新任务")
                    return False
                
                # 创建作业对象
                job = Job(
                    task=job_data['task'],
                    next_run=job_data['next_run'],
                    priority=job_data.get('priority', 0),
                    retry_count=job_data.get('retry_count', 0)
                )
                
                task_id = job.task.id
                
                # 检查是否已存在相同任务
                if task_id in self._task_index:
                    # 更新现有任务
                    old_job = self._task_index[task_id]
                    if job.next_run < old_job.next_run:
                        # 新任务更早，替换旧任务
                        self._remove_from_queue(old_job)
                        self._add_to_queue(job)
                        self._task_index[task_id] = job
                        self.logger.debug(f"更新任务 {task_id} 的调度时间")
                    else:
                        self.logger.debug(f"忽略任务 {task_id} 的较晚调度")
                else:
                    # 添加新任务
                    self._add_to_queue(job)
                    self._task_index[task_id] = job
                    self.stats['total_added'] += 1
                    self.stats['current_size'] += 1
                    self.logger.debug(f"添加任务 {task_id} 到队列")
                
                return True
                
        except Exception as e:
            self.logger.error(f"添加任务到队列失败: {e}")
            return False
    
    def _add_to_queue(self, job: Job):
        """将作业添加到优先队列"""
        heapq.heappush(self._queue, job)
    
    def _remove_from_queue(self, job: Job):
        """从优先队列中移除作业（标记删除）"""
        # 使用标记删除，避免重新建堆
        job.task = None  # 标记为已删除
        job.next_run = datetime.max
    
    async def get_ready_jobs(self, current_time: datetime) -> List[Job]:
        """获取当前时间可以执行的任务"""
        ready_jobs = []
        
        try:
            async with self._lock:
                # 清理已标记删除的任务
                self._cleanup_deleted_jobs()
                
                # 获取所有到期的任务
                while self._queue and self._queue[0].next_run <= current_time:
                    job = heapq.heappop(self._queue)
                    
                    # 跳过已删除的任务
                    if job.task is None:
                        continue
                    
                    task_id = job.task.id
                    
                    # 从索引中移除
                    if task_id in self._task_index:
                        del self._task_index[task_id]
                    
                    ready_jobs.append(job)
                    self.stats['total_processed'] += 1
                    self.stats['current_size'] -= 1
                
                if ready_jobs:
                    self.logger.debug(f"获取 {len(ready_jobs)} 个就绪任务")
                
                return ready_jobs
                
        except Exception as e:
            self.logger.error(f"获取就绪任务失败: {e}")
            return []
    
    def _cleanup_deleted_jobs(self):
        """清理已标记删除的任务"""
        # 从队列头部开始清理
        while self._queue and self._queue[0].task is None:
            heapq.heappop(self._queue)
    
    async def remove_task(self, task_id: str) -> bool:
        """从队列中移除指定任务"""
        try:
            async with self._lock:
                if task_id not in self._task_index:
                    return False
                
                job = self._task_index[task_id]
                
                # 标记删除
                self._remove_from_queue(job)
                
                # 从索引中移除
                del self._task_index[task_id]
                
                self.stats['total_removed'] += 1
                self.stats['current_size'] -= 1
                
                self.logger.debug(f"从队列中移除任务 {task_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"从队列中移除任务失败: {e}")
            return False
    
    async def update_task_schedule(self, task_id: str, new_next_run: datetime, new_priority: int = None) -> bool:
        """更新任务的调度时间"""
        try:
            async with self._lock:
                if task_id not in self._task_index:
                    return False
                
                old_job = self._task_index[task_id]
                
                # 创建新的作业对象
                new_job = Job(
                    task=old_job.task,
                    next_run=new_next_run,
                    priority=new_priority if new_priority is not None else old_job.priority,
                    retry_count=old_job.retry_count
                )
                
                # 从队列中移除旧作业
                self._remove_from_queue(old_job)
                
                # 添加新作业
                self._add_to_queue(new_job)
                
                # 更新索引
                self._task_index[task_id] = new_job
                
                self.logger.debug(f"更新任务 {task_id} 的调度时间: {new_next_run}")
                return True
                
        except Exception as e:
            self.logger.error(f"更新任务调度时间失败: {e}")
            return False
    
    async def get_next_run_time(self) -> Optional[datetime]:
        """获取下一个任务的执行时间"""
        try:
            async with self._lock:
                self._cleanup_deleted_jobs()
                
                if not self._queue:
                    return None
                
                return self._queue[0].next_run
                
        except Exception as e:
            self.logger.error(f"获取下次运行时间失败: {e}")
            return None
    
    def size(self) -> int:
        """获取队列大小"""
        return len([job for job in self._queue if job.task is not None])
    
    def is_empty(self) -> bool:
        """检查队列是否为空"""
        return self.size() == 0
    
    def is_full(self) -> bool:
        """检查队列是否已满"""
        return self.size() >= self.max_size
    
    async def clear(self):
        """清空队列"""
        try:
            async with self._lock:
                self._queue.clear()
                self._task_index.clear()
                self.stats['current_size'] = 0
                self.logger.info("任务队列已清空")
                
        except Exception as e:
            self.logger.error(f"清空队列失败: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取队列统计信息"""
        return {
            'total_added': self.stats['total_added'],
            'total_processed': self.stats['total_processed'],
            'total_removed': self.stats['total_removed'],
            'current_size': self.size(),
            'max_size': self.max_size,
            'is_empty': self.is_empty(),
            'is_full': self.is_full()
        }
    
    async def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """获取待处理任务列表"""
        try:
            async with self._lock:
                self._cleanup_deleted_jobs()
                
                pending_tasks = []
                for job in self._queue:
                    if job.task is not None:
                        pending_tasks.append({
                            'task_id': job.task.id,
                            'task_name': job.task.name,
                            'next_run': job.next_run.isoformat(),
                            'priority': job.priority,
                            'retry_count': job.retry_count
                        })
                
                return pending_tasks
                
        except Exception as e:
            self.logger.error(f"获取待处理任务列表失败: {e}")
            return []
    
    async def peek_next_job(self) -> Optional[Job]:
        """查看下一个要执行的任务（不移除）"""
        try:
            async with self._lock:
                self._cleanup_deleted_jobs()
                
                if not self._queue:
                    return None
                
                return self._queue[0] if self._queue[0].task is not None else None
                
        except Exception as e:
            self.logger.error(f"查看下一个任务失败: {e}")
            return None


class PriorityJobQueue(JobQueue):
    """带优先级的任务队列"""
    
    def __init__(self, max_size: int = 1000):
        """初始化优先级任务队列"""
        super().__init__(max_size)
        self.priority_weights = {
            'critical': 0,    # 最高优先级
            'high': 10,
            'normal': 20,
            'low': 30,
            'minimal': 40     # 最低优先级
        }
    
    def calculate_priority_score(self, task_priority: str, task_age: float) -> int:
        """计算优先级分数"""
        # 基础优先级权重
        base_priority = self.priority_weights.get(task_priority, 20)
        
        # 任务等待时间加分（等待越久优先级越高）
        age_bonus = min(int(task_age / 60), 10)  # 每分钟加1分，最多10分
        
        return base_priority - age_bonus  # 分数越小优先级越高
    
    async def put_with_priority(self, job_data: Dict[str, Any], priority_level: str = 'normal') -> bool:
        """按优先级添加任务"""
        try:
            # 计算优先级分数
            current_time = datetime.now()
            task_age = (current_time - job_data['next_run']).total_seconds()
            priority_score = self.calculate_priority_score(priority_level, task_age)
            
            # 更新作业数据
            job_data['priority'] = priority_score
            
            return await self.put(job_data)
            
        except Exception as e:
            self.logger.error(f"按优先级添加任务失败: {e}")
            return False