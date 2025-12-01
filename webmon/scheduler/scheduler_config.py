#!/usr/bin/env python3
"""
调度器配置管理
管理调度器的各项配置参数
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field

from webmon.utils.logger import get_logger


@dataclass
class SchedulerConfig:
    """调度器配置"""
    
    # 基本配置
    max_concurrent_tasks: int = 10           # 最大并发任务数
    max_browser_resources: int = 5           # 最大浏览器资源数
    max_browser_concurrent: int = 3          # 最大浏览器并发数
    default_interval: int = 300              # 默认检测间隔（秒）
    
    # 超时配置
    default_timeout: int = 30000             # 默认超时时间（毫秒）
    max_execution_time: int = 300            # 最大执行时间（秒）
    resource_acquisition_timeout: int = 30   # 资源获取超时（秒）
    
    # 重试配置
    retry_attempts: int = 3                  # 最大重试次数
    retry_delay: int = 60                    # 重试延迟（秒）
    retry_backoff_factor: float = 2.0        # 退避因子
    
    # 队列配置
    max_queue_size: int = 1000               # 最大队列大小
    queue_cleanup_interval: int = 300        # 队列清理间隔（秒）
    
    # 性能配置
    scheduler_loop_interval: float = 0.1     # 调度循环间隔（秒）
    job_batch_size: int = 10                 # 批量处理大小
    
    # 监控配置
    enable_performance_monitoring: bool = True    # 启用性能监控
    enable_resource_monitoring: bool = True       # 启用资源监控
    stats_update_interval: int = 60               # 统计更新间隔（秒）
    
    # 优先级配置
    enable_priority_scheduling: bool = True       # 启用优先级调度
    priority_weights: Dict[str, float] = field(default_factory=lambda: {
        'age_factor': 1.0,           # 时间权重因子
        'change_frequency_factor': 2.0,  # 变化频率权重因子
        'error_penalty_factor': 5.0,     # 错误惩罚因子
        'success_bonus_factor': -1.0     # 成功奖励因子
    })
    
    # 错误处理配置
    error_handling: Dict[str, Any] = field(default_factory=lambda: {
        'max_consecutive_errors': 5,     # 最大连续错误数
        'error_cooldown_period': 300,    # 错误冷却期（秒）
        'circuit_breaker_threshold': 10, # 熔断阈值
        'circuit_breaker_timeout': 600   # 熔断超时（秒）
    })
    
    # 日志配置
    log_level: str = 'INFO'                  # 日志级别
    log_execution_details: bool = True       # 记录执行详情
    log_performance_metrics: bool = True     # 记录性能指标
    
    def __post_init__(self):
        """初始化后处理"""
        self.logger = get_logger(__name__)
        
        # 验证配置
        self._validate_config()
        
        self.logger.info("调度器配置初始化完成")
    
    def _validate_config(self):
        """验证配置参数"""
        # 验证数值范围
        if self.max_concurrent_tasks <= 0:
            raise ValueError("max_concurrent_tasks 必须大于0")
        
        if self.max_browser_resources <= 0:
            raise ValueError("max_browser_resources 必须大于0")
        
        if self.max_browser_concurrent <= 0:
            raise ValueError("max_browser_concurrent 必须大于0")
        
        if self.max_browser_concurrent > self.max_browser_resources:
            raise ValueError("max_browser_concurrent 不能大于 max_browser_resources")
        
        if self.default_interval <= 0:
            raise ValueError("default_interval 必须大于0")
        
        if self.default_timeout <= 0:
            raise ValueError("default_timeout 必须大于0")
        
        if self.retry_attempts < 0:
            raise ValueError("retry_attempts 不能为负数")
        
        if self.retry_delay < 0:
            raise ValueError("retry_delay 不能为负数")
        
        if self.max_queue_size <= 0:
            raise ValueError("max_queue_size 必须大于0")
        
        if self.scheduler_loop_interval <= 0:
            raise ValueError("scheduler_loop_interval 必须大于0")
        
        if self.job_batch_size <= 0:
            raise ValueError("job_batch_size 必须大于0")
        
        # 验证日志级别
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.log_level not in valid_log_levels:
            raise ValueError(f"log_level 必须是 {valid_log_levels} 之一")
        
        self.logger.debug("调度器配置验证通过")
    
    @classmethod
    def from_config_manager(cls, config_manager) -> 'SchedulerConfig':
        """从配置管理器创建调度器配置"""
        try:
            # 首先尝试从新的调度器配置获取
            scheduler_config = config_manager.get_scheduler_config()
            
            if scheduler_config:
                # 使用新的调度器配置
                return cls._from_new_config_format(scheduler_config, config_manager)
            else:
                # 回退到旧的配置格式
                return cls._from_legacy_config_format(config_manager)
            
        except Exception as e:
            cls.logger.error(f"从配置管理器创建调度器配置失败: {e}")
            raise
    
    @classmethod
    def _from_new_config_format(cls, scheduler_config: Dict[str, Any], config_manager) -> 'SchedulerConfig':
        """从新的调度器配置格式创建"""
        try:
            config = cls()
            
            # 性能配置
            performance = scheduler_config.get('performance', {})
            config.max_concurrent_tasks = performance.get('max_concurrent_tasks', 10)
            config.max_browser_resources = performance.get('max_browser_resources', 5)
            config.max_browser_concurrent = performance.get('max_browser_concurrent', 3)
            config.scheduler_loop_interval = performance.get('scheduler_loop_interval', 0.1)
            config.job_batch_size = performance.get('job_batch_size', 10)
            
            # 超时配置
            timeouts = scheduler_config.get('timeouts', {})
            config.default_timeout = timeouts.get('default_timeout', 30000)
            config.max_execution_time = timeouts.get('max_execution_time', 300)
            config.resource_acquisition_timeout = timeouts.get('resource_acquisition_timeout', 30)
            
            # 重试配置
            retry = scheduler_config.get('retry', {})
            config.retry_attempts = retry.get('retry_attempts', 3)
            config.retry_delay = retry.get('retry_delay', 60)
            config.retry_backoff_factor = retry.get('retry_backoff_factor', 2.0)
            
            # 队列配置
            queue = scheduler_config.get('queue', {})
            config.max_queue_size = queue.get('max_queue_size', 1000)
            config.queue_cleanup_interval = queue.get('queue_cleanup_interval', 300)
            
            # 监控配置
            monitoring = scheduler_config.get('monitoring', {})
            config.enable_performance_monitoring = monitoring.get('enable_performance_monitoring', True)
            config.enable_resource_monitoring = monitoring.get('enable_resource_monitoring', True)
            config.stats_update_interval = monitoring.get('stats_update_interval', 60)
            
            # 优先级配置
            priority = scheduler_config.get('priority', {})
            config.enable_priority_scheduling = priority.get('enable_priority_scheduling', True)
            if 'priority_weights' in priority:
                config.priority_weights.update(priority['priority_weights'])
            
            # 错误处理配置
            error_handling = scheduler_config.get('error_handling', {})
            if error_handling:
                config.error_handling.update(error_handling)
            
            # 日志配置
            logging_config = scheduler_config.get('logging', {})
            config.log_level = logging_config.get('log_level', 'INFO')
            config.log_execution_details = logging_config.get('log_execution_details', True)
            config.log_performance_metrics = logging_config.get('log_performance_metrics', True)
            
            # 从监控配置获取默认间隔时间
            monitoring_config = config_manager.get_monitoring_config()
            config.default_interval = monitoring_config.get('default_interval', 300)
            
            config.logger.info("从新的调度器配置格式创建配置完成")
            return config
            
        except Exception as e:
            config.logger.error(f"从新的调度器配置格式创建失败: {e}")
            raise
    
    @classmethod
    def _from_legacy_config_format(cls, config_manager) -> 'SchedulerConfig':
        """从旧的配置格式创建（向后兼容）"""
        try:
            # 获取调度相关配置
            monitoring_config = config_manager.get_monitoring_config()
            detection_config = config_manager.get_detection_config()
            notification_config = config_manager.get_notification_config()
            storage_config = config_manager.get_storage_config()
            
            # 创建配置实例
            config = cls()
            
            # 基本配置
            config.max_concurrent_tasks = monitoring_config.get('max_concurrent_tasks', 10)
            config.max_browser_resources = monitoring_config.get('max_browser_resources', 5)
            config.max_browser_concurrent = monitoring_config.get('max_browser_concurrent', 3)
            config.default_interval = monitoring_config.get('default_interval', 300)
            config.default_timeout = monitoring_config.get('default_timeout', 30000)
            config.max_execution_time = monitoring_config.get('max_execution_time', 300)
            
            # 重试配置
            config.retry_attempts = monitoring_config.get('max_retries', 3)
            config.retry_delay = monitoring_config.get('retry_delay', 60)
            config.retry_backoff_factor = monitoring_config.get('retry_backoff_factor', 2.0)
            
            # 队列配置
            config.max_queue_size = storage_config.get('max_queue_size', 1000)
            config.queue_cleanup_interval = storage_config.get('queue_cleanup_interval', 300)
            
            # 性能配置
            config.scheduler_loop_interval = monitoring_config.get('scheduler_loop_interval', 0.1)
            config.job_batch_size = monitoring_config.get('job_batch_size', 10)
            
            # 监控配置
            config.enable_performance_monitoring = monitoring_config.get('enable_performance_monitoring', True)
            config.enable_resource_monitoring = monitoring_config.get('enable_resource_monitoring', True)
            config.stats_update_interval = monitoring_config.get('stats_update_interval', 60)
            
            # 优先级配置
            priority_config = monitoring_config.get('priority_weights', {})
            config.priority_weights.update(priority_config)
            
            # 错误处理配置
            error_config = monitoring_config.get('error_handling', {})
            config.error_handling.update(error_config)
            
            # 日志配置
            config.log_level = monitoring_config.get('log_level', 'INFO')
            config.log_execution_details = monitoring_config.get('log_execution_details', True)
            config.log_performance_metrics = monitoring_config.get('log_performance_metrics', True)
            
            config.logger.info("从旧的配置格式创建调度器配置完成")
            return config
            
        except Exception as e:
            config.logger.error(f"从旧的配置格式创建调度器配置失败: {e}")
            raise
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'max_concurrent_tasks': self.max_concurrent_tasks,
            'max_browser_resources': self.max_browser_resources,
            'max_browser_concurrent': self.max_browser_concurrent,
            'default_interval': self.default_interval,
            'default_timeout': self.default_timeout,
            'max_execution_time': self.max_execution_time,
            'resource_acquisition_timeout': self.resource_acquisition_timeout,
            'retry_attempts': self.retry_attempts,
            'retry_delay': self.retry_delay,
            'retry_backoff_factor': self.retry_backoff_factor,
            'max_queue_size': self.max_queue_size,
            'queue_cleanup_interval': self.queue_cleanup_interval,
            'scheduler_loop_interval': self.scheduler_loop_interval,
            'job_batch_size': self.job_batch_size,
            'enable_performance_monitoring': self.enable_performance_monitoring,
            'enable_resource_monitoring': self.enable_resource_monitoring,
            'stats_update_interval': self.stats_update_interval,
            'enable_priority_scheduling': self.enable_priority_scheduling,
            'priority_weights': self.priority_weights,
            'error_handling': self.error_handling,
            'log_level': self.log_level,
            'log_execution_details': self.log_execution_details,
            'log_performance_metrics': self.log_performance_metrics
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'SchedulerConfig':
        """从字典创建配置"""
        try:
            config = cls()
            
            # 基本配置
            if 'max_concurrent_tasks' in config_dict:
                config.max_concurrent_tasks = config_dict['max_concurrent_tasks']
            
            if 'max_browser_resources' in config_dict:
                config.max_browser_resources = config_dict['max_browser_resources']
            
            if 'max_browser_concurrent' in config_dict:
                config.max_browser_concurrent = config_dict['max_browser_concurrent']
            
            if 'default_interval' in config_dict:
                config.default_interval = config_dict['default_interval']
            
            if 'default_timeout' in config_dict:
                config.default_timeout = config_dict['default_timeout']
            
            if 'max_execution_time' in config_dict:
                config.max_execution_time = config_dict['max_execution_time']
            
            if 'resource_acquisition_timeout' in config_dict:
                config.resource_acquisition_timeout = config_dict['resource_acquisition_timeout']
            
            # 重试配置
            if 'retry_attempts' in config_dict:
                config.retry_attempts = config_dict['retry_attempts']
            
            if 'retry_delay' in config_dict:
                config.retry_delay = config_dict['retry_delay']
            
            if 'retry_backoff_factor' in config_dict:
                config.retry_backoff_factor = config_dict['retry_backoff_factor']
            
            # 队列配置
            if 'max_queue_size' in config_dict:
                config.max_queue_size = config_dict['max_queue_size']
            
            if 'queue_cleanup_interval' in config_dict:
                config.queue_cleanup_interval = config_dict['queue_cleanup_interval']
            
            # 性能配置
            if 'scheduler_loop_interval' in config_dict:
                config.scheduler_loop_interval = config_dict['scheduler_loop_interval']
            
            if 'job_batch_size' in config_dict:
                config.job_batch_size = config_dict['job_batch_size']
            
            # 监控配置
            if 'enable_performance_monitoring' in config_dict:
                config.enable_performance_monitoring = config_dict['enable_performance_monitoring']
            
            if 'enable_resource_monitoring' in config_dict:
                config.enable_resource_monitoring = config_dict['enable_resource_monitoring']
            
            if 'stats_update_interval' in config_dict:
                config.stats_update_interval = config_dict['stats_update_interval']
            
            # 优先级配置
            if 'enable_priority_scheduling' in config_dict:
                config.enable_priority_scheduling = config_dict['enable_priority_scheduling']
            
            if 'priority_weights' in config_dict:
                config.priority_weights.update(config_dict['priority_weights'])
            
            # 错误处理配置
            if 'error_handling' in config_dict:
                config.error_handling.update(config_dict['error_handling'])
            
            # 日志配置
            if 'log_level' in config_dict:
                config.log_level = config_dict['log_level']
            
            if 'log_execution_details' in config_dict:
                config.log_execution_details = config_dict['log_execution_details']
            
            if 'log_performance_metrics' in config_dict:
                config.log_performance_metrics = config_dict['log_performance_metrics']
            
            config.logger.info("从字典创建调度器配置完成")
            return config
            
        except Exception as e:
            config.logger.error(f"从字典创建调度器配置失败: {e}")
            raise
    
    def update_config(self, updates: Dict[str, Any]):
        """更新配置"""
        try:
            # 保存当前配置
            old_config = self.to_dict()
            
            # 应用更新
            for key, value in updates.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                elif key in self.priority_weights:
                    self.priority_weights[key] = value
                elif key in self.error_handling:
                    self.error_handling[key] = value
                else:
                    self.logger.warning(f"未知配置项: {key}")
            
            # 重新验证配置
            self._validate_config()
            
            self.logger.info("调度器配置已更新")
            
        except Exception as e:
            self.logger.error(f"更新配置失败: {e}")
            # 回滚配置
            self.__dict__.update(old_config)
            raise
    
    def get_performance_recommendations(self) -> List[str]:
        """获取性能优化建议"""
        recommendations = []
        
        try:
            # 检查并发配置
            if self.max_concurrent_tasks > 20:
                recommendations.append(
                    "max_concurrent_tasks 设置过高 (>20)，可能导致资源竞争，建议降低到10-15"
                )
            
            if self.max_concurrent_tasks < 3:
                recommendations.append(
                    "max_concurrent_tasks 设置过低 (<3)，可能无法充分利用资源，建议增加到5-10"
                )
            
            # 检查浏览器资源配置
            if self.max_browser_concurrent > self.max_browser_resources:
                recommendations.append(
                    "max_browser_concurrent 大于 max_browser_resources，可能导致资源不足"
                )
            
            # 检查重试配置
            if self.retry_attempts > 5:
                recommendations.append(
                    "retry_attempts 设置过高 (>5)，可能导致资源浪费，建议降低到3-5"
                )
            
            if self.retry_delay < 30:
                recommendations.append(
                    "retry_delay 设置过低 (<30秒)，可能导致过于频繁的重试，建议增加到60-120秒"
                )
            
            # 检查队列配置
            if self.max_queue_size > 5000:
                recommendations.append(
                    "max_queue_size 设置过高 (>5000)，可能导致内存占用过大，建议降低到1000-2000"
                )
            
            # 检查性能监控配置
            if not self.enable_performance_monitoring:
                recommendations.append(
                    "建议启用 enable_performance_monitoring 以监控调度器性能"
                )
            
            if not self.enable_resource_monitoring:
                recommendations.append(
                    "建议启用 enable_resource_monitoring 以监控资源使用情况"
                )
            
            # 检查优先级配置
            if not self.enable_priority_scheduling:
                recommendations.append(
                    "建议启用 enable_priority_scheduling 以实现智能任务调度"
                )
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"生成性能优化建议失败: {e}")
            return []
    
    def validate_performance(self) -> Dict[str, Any]:
        """验证性能配置"""
        try:
            issues = []
            warnings = []
            
            # 检查配置冲突
            if self.max_browser_concurrent > self.max_browser_resources:
                issues.append("浏览器并发数超过资源数")
            
            if self.max_concurrent_tasks > self.max_browser_resources * 2:
                warnings.append("任务并发数可能超过浏览器处理能力")
            
            # 检查超时配置
            total_timeout = self.default_timeout / 1000 * self.retry_attempts + self.retry_delay * self.retry_attempts
            if total_timeout > 600:  # 10分钟
                warnings.append(f"总超时时间过长 ({total_timeout:.0f}秒)")
            
            # 检查资源使用
            estimated_memory = (
                self.max_browser_resources * 200 +  # 每个浏览器约200MB
                self.max_concurrent_tasks * 50 +    # 每个任务约50MB
                self.max_queue_size * 10             # 队列项约10MB
            )
            
            if estimated_memory > 2000:  # 2GB
                warnings.append(f"估计内存使用过高 ({estimated_memory}MB)")
            
            return {
                'valid': len(issues) == 0,
                'issues': issues,
                'warnings': warnings,
                'estimated_memory_mb': estimated_memory,
                'total_timeout_seconds': total_timeout
            }
            
        except Exception as e:
            self.logger.error(f"验证性能配置失败: {e}")
            return {'valid': False, 'issues': [str(e)], 'warnings': []}