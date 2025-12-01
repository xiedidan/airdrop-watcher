#!/usr/bin/env python3
"""
优先级管理器
负责任务的优先级计算和管理
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum

from webmon.models.task import Task
from webmon.utils.logger import get_logger


class PriorityLevel(Enum):
    """优先级级别"""
    CRITICAL = 0    # 最高优先级
    HIGH = 1
    NORMAL = 2
    LOW = 3
    MINIMAL = 4     # 最低优先级


class PriorityManager:
    """优先级管理器"""
    
    # 优先级权重映射
    PRIORITY_WEIGHTS = {
        PriorityLevel.CRITICAL: 0,
        PriorityLevel.HIGH: 10,
        PriorityLevel.NORMAL: 20,
        PriorityLevel.LOW: 30,
        PriorityLevel.MINIMAL: 40
    }
    
    # 任务类型权重
    TASK_TYPE_WEIGHTS = {
        'monitoring': 0,      # 监控任务
        'notification': 5,    # 通知任务
        'maintenance': 10,    # 维护任务
        'backup': 15,         # 备份任务
        'cleanup': 20         # 清理任务
    }
    
    # 状态权重（状态越差，优先级越高）
    STATUS_WEIGHTS = {
        'error': -15,         # 错误状态，高优先级
        'failed': -10,        # 失败状态，高优先级
        'warning': -5,        # 警告状态，中等优先级
        'active': 0,          # 正常状态，标准优先级
        'paused': 5,          # 暂停状态，低优先级
        'completed': 10       # 完成状态，最低优先级
    }
    
    def __init__(self):
        """初始化优先级管理器"""
        self.logger = get_logger(__name__)
        
        # 动态权重调整参数
        self.age_weight_factor = 1.0      # 任务等待时间权重因子
        self.change_frequency_factor = 2.0  # 变化频率权重因子
        self.error_penalty_factor = 5.0    # 错误惩罚因子
        self.success_bonus_factor = -1.0   # 成功奖励因子
        
        self.logger.info("优先级管理器初始化完成")
    
    def calculate_priority(self, task: Task, 
                          current_time: Optional[datetime] = None) -> int:
        """计算任务的优先级分数"""
        try:
            if current_time is None:
                current_time = datetime.now()
            
            # 基础优先级（来自任务配置）
            base_priority = self._get_base_priority(task)
            
            # 任务类型权重
            type_weight = self._calculate_type_weight(task)
            
            # 状态权重
            status_weight = self._calculate_status_weight(task)
            
            # 时间权重（等待时间）
            time_weight = self._calculate_time_weight(task, current_time)
            
            # 变化频率权重
            change_weight = self._calculate_change_frequency_weight(task)
            
            # 错误历史权重
            error_weight = self._calculate_error_weight(task)
            
            # 成功历史权重
            success_weight = self._calculate_success_weight(task)
            
            # 计算总优先级分数（分数越小，优先级越高）
            total_score = (
                base_priority +
                type_weight +
                status_weight +
                time_weight +
                change_weight +
                error_weight +
                success_weight
            )
            
            # 确保分数在合理范围内
            total_score = max(0, min(total_score, 100))
            
            self.logger.debug(
                f"任务 {task.name} 优先级计算: "
                f"基础={base_priority}, 类型={type_weight}, 状态={status_weight}, "
                f"时间={time_weight}, 变化={change_weight}, 错误={error_weight}, "
                f"成功={success_weight}, 总分={total_score}"
            )
            
            return int(total_score)
            
        except Exception as e:
            self.logger.error(f"计算任务优先级失败: {e}")
            return 50  # 返回默认优先级
    
    def _get_base_priority(self, task: Task) -> int:
        """获取基础优先级"""
        # 如果任务有自定义优先级配置，使用它
        if hasattr(task, 'priority') and task.priority is not None:
            if isinstance(task.priority, (int, float)):
                return int(task.priority)
            elif isinstance(task.priority, str):
                # 处理字符串优先级
                priority_map = {
                    'critical': self.PRIORITY_WEIGHTS[PriorityLevel.CRITICAL],
                    'high': self.PRIORITY_WEIGHTS[PriorityLevel.HIGH],
                    'normal': self.PRIORITY_WEIGHTS[PriorityLevel.NORMAL],
                    'low': self.PRIORITY_WEIGHTS[PriorityLevel.LOW],
                    'minimal': self.PRIORITY_WEIGHTS[PriorityLevel.MINIMAL]
                }
                return priority_map.get(task.priority.lower(), 
                                      self.PRIORITY_WEIGHTS[PriorityLevel.NORMAL])
        
        # 默认使用普通优先级
        return self.PRIORITY_WEIGHTS[PriorityLevel.NORMAL]
    
    def _calculate_type_weight(self, task: Task) -> int:
        """计算任务类型权重"""
        # 根据任务名称或URL判断类型
        task_name = task.name.lower()
        task_url = task.url.lower()
        
        # 检查是否匹配特定类型
        if any(keyword in task_name or keyword in task_url for keyword in 
               ['critical', 'important', 'urgent', 'alert']):
            return self.TASK_TYPE_WEIGHTS['monitoring'] - 10  # 提高优先级
        
        if any(keyword in task_name or keyword in task_url for keyword in 
               ['backup', 'archive']):
            return self.TASK_TYPE_WEIGHTS['backup']
        
        if any(keyword in task_name or keyword in task_url for keyword in 
               ['cleanup', 'maintenance']):
            return self.TASK_TYPE_WEIGHTS['cleanup']
        
        # 默认监控任务
        return self.TASK_TYPE_WEIGHTS['monitoring']
    
    def _calculate_status_weight(self, task: Task) -> int:
        """计算状态权重"""
        status = task.status.lower() if task.status else 'active'
        
        # 返回对应的状态权重
        return self.STATUS_WEIGHTS.get(status, self.STATUS_WEIGHTS['active'])
    
    def _calculate_time_weight(self, task: Task, current_time: datetime) -> int:
        """计算时间权重（等待时间）"""
        try:
            if not task.last_check:
                # 从未执行过的任务，给予较高优先级
                return -10
            
            # 计算距离上次检测的时间（秒）
            time_since_last_check = (current_time - task.last_check).total_seconds()
            
            # 计算应该检测的时间间隔（秒）
            expected_interval = task.interval
            
            # 计算延迟时间
            delay_time = max(0, time_since_last_check - expected_interval)
            
            # 根据延迟时间计算权重（延迟越久，优先级越高）
            time_weight = int(delay_time / 60 * self.age_weight_factor)  # 每分钟增加一定权重
            
            # 限制权重的最大值
            return min(time_weight, 20)
            
        except Exception as e:
            self.logger.warning(f"计算时间权重失败: {e}")
            return 0
    
    def _calculate_change_frequency_weight(self, task: Task) -> int:
        """计算变化频率权重"""
        try:
            # 如果任务经常变化，可能需要更频繁的监控
            change_count = task.change_count
            
            if change_count == 0:
                return 0
            
            # 计算平均变化间隔（假设任务运行了一段时间）
            # 这里使用简化的计算方式
            if hasattr(task, 'created_at') and task.created_at:
                task_age_days = (datetime.now() - task.created_at).days
                if task_age_days > 0:
                    changes_per_day = change_count / task_age_days
                    
                    # 变化频率越高，优先级越高（但需要监控）
                    if changes_per_day > 1:
                        return -int(changes_per_day * self.change_frequency_factor)
                    elif changes_per_day > 0.5:
                        return -5
            
            return 0
            
        except Exception as e:
            self.logger.warning(f"计算变化频率权重失败: {e}")
            return 0
    
    def _calculate_error_weight(self, task: Task) -> int:
        """计算错误历史权重"""
        try:
            # 如果任务最近有错误，提高优先级以便尽快重试
            if task.status.lower() == 'error':
                # 检查是否有重试次数记录
                retry_count = getattr(task, 'retry_count', 0)
                
                # 错误状态的任务应该优先执行
                base_penalty = self.error_penalty_factor
                
                # 重试次数越多，优先级越高（但不要无限增加）
                retry_bonus = min(retry_count * 2, 10)
                
                return -int(base_penalty + retry_bonus)
            
            return 0
            
        except Exception as e:
            self.logger.warning(f"计算错误权重失败: {e}")
            return 0
    
    def _calculate_success_weight(self, task: Task) -> int:
        """计算成功历史权重"""
        try:
            # 连续成功的任务可以适当降低优先级
            # 这里简化处理，实际可以更复杂
            
            if task.status.lower() == 'active' and task.change_count == 0:
                # 长期没有变化的活跃任务，优先级稍低
                if hasattr(task, 'created_at') and task.created_at:
                    task_age_days = (datetime.now() - task.created_at).days
                    if task_age_days > 7:  # 运行超过7天且无变化
                        return int(abs(self.success_bonus_factor) * (task_age_days / 7))
            
            return 0
            
        except Exception as e:
            self.logger.warning(f"计算成功权重失败: {e}")
            return 0
    
    def adjust_priority_for_retry(self, task: Task, retry_count: int) -> int:
        """为重试任务调整优先级"""
        try:
            base_priority = self.calculate_priority(task)
            
            # 重试次数越多，优先级越高（使用指数增长）
            retry_bonus = min(retry_count * retry_count * 2, 20)
            
            adjusted_priority = max(0, base_priority - retry_bonus)
            
            self.logger.debug(
                f"任务 {task.name} 重试优先级调整: "
                f"基础={base_priority}, 重试次数={retry_count}, "
                f"重试奖励={retry_bonus}, 调整后={adjusted_priority}"
            )
            
            return adjusted_priority
            
        except Exception as e:
            self.logger.error(f"调整重试优先级失败: {e}")
            return self.calculate_priority(task)
    
    def get_priority_level(self, priority_score: int) -> PriorityLevel:
        """根据优先级分数获取优先级级别"""
        if priority_score <= self.PRIORITY_WEIGHTS[PriorityLevel.CRITICAL] + 5:
            return PriorityLevel.CRITICAL
        elif priority_score <= self.PRIORITY_WEIGHTS[PriorityLevel.HIGH] + 5:
            return PriorityLevel.HIGH
        elif priority_score <= self.PRIORITY_WEIGHTS[PriorityLevel.NORMAL] + 5:
            return PriorityLevel.NORMAL
        elif priority_score <= self.PRIORITY_WEIGHTS[PriorityLevel.LOW] + 5:
            return PriorityLevel.LOW
        else:
            return PriorityLevel.MINIMAL
    
    def compare_tasks(self, task1: Task, task2: Task, 
                     current_time: Optional[datetime] = None) -> int:
        """比较两个任务的优先级"""
        try:
            if current_time is None:
                current_time = datetime.now()
            
            priority1 = self.calculate_priority(task1, current_time)
            priority2 = self.calculate_priority(task2, current_time)
            
            # 返回比较结果（负数表示task1优先级更高）
            return priority1 - priority2
            
        except Exception as e:
            self.logger.error(f"比较任务优先级失败: {e}")
            return 0
    
    def get_priority_factors(self, task: Task, 
                           current_time: Optional[datetime] = None) -> Dict[str, int]:
        """获取任务优先级的各个因子"""
        try:
            if current_time is None:
                current_time = datetime.now()
            
            return {
                'base_priority': self._get_base_priority(task),
                'type_weight': self._calculate_type_weight(task),
                'status_weight': self._calculate_status_weight(task),
                'time_weight': self._calculate_time_weight(task, current_time),
                'change_weight': self._calculate_change_frequency_weight(task),
                'error_weight': self._calculate_error_weight(task),
                'success_weight': self._calculate_success_weight(task),
                'total_priority': self.calculate_priority(task, current_time)
            }
            
        except Exception as e:
            self.logger.error(f"获取优先级因子失败: {e}")
            return {}
    
    # 批量优先级管理
    
    def batch_calculate_priority(self, tasks: List[Task], 
                               current_time: Optional[datetime] = None) -> Dict[str, int]:
        """批量计算任务优先级"""
        try:
            if current_time is None:
                current_time = datetime.now()
            
            priorities = {}
            for task in tasks:
                priorities[task.id] = self.calculate_priority(task, current_time)
            
            return priorities
            
        except Exception as e:
            self.logger.error(f"批量计算优先级失败: {e}")
            return {}
    
    def sort_tasks_by_priority(self, tasks: List[Task], 
                              reverse: bool = False,
                              current_time: Optional[datetime] = None) -> List[Task]:
        """按优先级排序任务"""
        try:
            if current_time is None:
                current_time = datetime.now()
            
            # 计算所有任务的优先级
            task_priorities = {}
            for task in tasks:
                task_priorities[task.id] = self.calculate_priority(task, current_time)
            
            # 排序（默认优先级高的在前）
            sorted_tasks = sorted(
                tasks,
                key=lambda t: task_priorities[t.id],
                reverse=reverse
            )
            
            return sorted_tasks
            
        except Exception as e:
            self.logger.error(f"按优先级排序任务失败: {e}")
            return tasks
    
    # 配置管理
    
    def update_weights(self, weights_config: Dict[str, Any]):
        """更新权重配置"""
        try:
            # 更新动态权重因子
            if 'age_weight_factor' in weights_config:
                self.age_weight_factor = float(weights_config['age_weight_factor'])
            
            if 'change_frequency_factor' in weights_config:
                self.change_frequency_factor = float(weights_config['change_frequency_factor'])
            
            if 'error_penalty_factor' in weights_config:
                self.error_penalty_factor = float(weights_config['error_penalty_factor'])
            
            if 'success_bonus_factor' in weights_config:
                self.success_bonus_factor = float(weights_config['success_bonus_factor'])
            
            self.logger.info("优先级权重配置已更新")
            
        except Exception as e:
            self.logger.error(f"更新权重配置失败: {e}")
    
    def get_config(self) -> Dict[str, Any]:
        """获取当前配置"""
        return {
            'age_weight_factor': self.age_weight_factor,
            'change_frequency_factor': self.change_frequency_factor,
            'error_penalty_factor': self.error_penalty_factor,
            'success_bonus_factor': self.success_bonus_factor,
            'priority_weights': self.PRIORITY_WEIGHTS,
            'task_type_weights': self.TASK_TYPE_WEIGHTS,
            'status_weights': self.STATUS_WEIGHTS
        }