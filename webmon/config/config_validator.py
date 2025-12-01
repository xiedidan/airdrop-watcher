"""
配置验证器 - 验证配置文件的有效性和完整性
"""
import re
import logging
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse
from ..exceptions import ConfigurationError


class ConfigValidator:
    """配置验证器"""
    
    def __init__(self):
        """初始化配置验证器"""
        self.logger = logging.getLogger(__name__)
        
        # 预定义验证规则
        self.validation_rules = {
            'url': self._validate_url,
            'email': self._validate_email,
            'path': self._validate_path,
            'timeout': self._validate_timeout,
            'interval': self._validate_interval,
            'threshold': self._validate_threshold,
            'percentage': self._validate_percentage,
            'positive_int': self._validate_positive_int,
            'non_negative_int': self._validate_non_negative_int,
            'positive_float': self._validate_positive_float,
            'boolean': self._validate_boolean,
            'color': self._validate_color,
            'css_selector': self._validate_css_selector,
            'webhook_url': self._validate_webhook_url,
            'token': self._validate_token
        }
    
    def validate_json_config(self, config: Dict[str, Any]) -> bool:
        """
        验证JSON配置文件
        
        Args:
            config: JSON配置数据
            
        Returns:
            是否有效
        """
        try:
            # 验证基本结构
            if not self._validate_basic_structure(config):
                return False
            
            # 验证版本信息
            if not self._validate_version(config.get('version')):
                return False
            
            # 验证监控配置
            if not self._validate_monitoring_config(config.get('monitoring', {})):
                return False
            
            # 验证检测配置
            if not self._validate_detection_config(config.get('detection', {})):
                return False
            
            # 验证通知配置
            if not self._validate_notification_config(config.get('notification', {})):
                return False
            
            # 验证存储配置
            if not self._validate_storage_config(config.get('storage', {})):
                return False
            
            # 验证调度器配置
            if not self.validate_scheduler_config(config.get('scheduler', {})):
                return False
            
            # 验证日志配置
            if not self.validate_logging_config(config.get('logging', {})):
                return False
            
            # 验证任务配置
            if not self._validate_tasks_config(config.get('tasks', [])):
                return False
            
            self.logger.info("JSON配置验证通过")
            return True
            
        except Exception as e:
            self.logger.error(f"JSON配置验证失败: {e}")
            return False
    
    def validate_env_config(self, env_config: Dict[str, Any]) -> bool:
        """
        验证环境变量配置
        
        Args:
            env_config: 环境变量配置
            
        Returns:
            是否有效
        """
        try:
            # 验证推送平台令牌
            if not self._validate_push_tokens(env_config):
                return False
            
            # 验证监控相关配置
            if not self._validate_monitoring_env(env_config):
                return False
            
            # 验证检测相关配置
            if not self._validate_detection_env(env_config):
                return False
            
            # 验证日志相关配置
            if not self._validate_logging_env(env_config):
                return False
            
            # 验证高级配置
            if not self._validate_advanced_env(env_config):
                return False
            
            self.logger.info("环境变量配置验证通过")
            return True
            
        except Exception as e:
            self.logger.error(f"环境变量配置验证失败: {e}")
            return False
    
    def validate_scheduler_config(self, scheduler_config: Dict[str, Any]) -> bool:
        """
        验证调度器配置
        
        Args:
            scheduler_config: 调度器配置
            
        Returns:
            是否有效
        """
        try:
            if not isinstance(scheduler_config, dict):
                self.logger.error("调度器配置必须是字典类型")
                return False
            
            # 验证性能配置
            if 'performance' in scheduler_config:
                if not self._validate_scheduler_performance_config(scheduler_config['performance']):
                    return False
            
            # 验证超时配置
            if 'timeouts' in scheduler_config:
                if not self._validate_scheduler_timeouts_config(scheduler_config['timeouts']):
                    return False
            
            # 验证重试配置
            if 'retry' in scheduler_config:
                if not self._validate_scheduler_retry_config(scheduler_config['retry']):
                    return False
            
            # 验证队列配置
            if 'queue' in scheduler_config:
                if not self._validate_scheduler_queue_config(scheduler_config['queue']):
                    return False
            
            # 验证监控配置
            if 'monitoring' in scheduler_config:
                if not self._validate_scheduler_monitoring_config(scheduler_config['monitoring']):
                    return False
            
            # 验证优先级配置
            if 'priority' in scheduler_config:
                if not self._validate_scheduler_priority_config(scheduler_config['priority']):
                    return False
            
            # 验证错误处理配置
            if 'error_handling' in scheduler_config:
                if not self._validate_scheduler_error_handling_config(scheduler_config['error_handling']):
                    return False
            
            # 验证日志配置
            if 'logging' in scheduler_config:
                if not self._validate_scheduler_logging_config(scheduler_config['logging']):
                    return False
            
            self.logger.info("调度器配置验证通过")
            return True
            
        except Exception as e:
            self.logger.error(f"调度器配置验证失败: {e}")
            return False
    
    def _validate_scheduler_performance_config(self, performance: Dict[str, Any]) -> bool:
        """验证调度器性能配置"""
        if not isinstance(performance, dict):
            self.logger.error("性能配置必须是字典类型")
            return False
        
        # 验证最大并发任务数
        if 'max_concurrent_tasks' in performance:
            if not self._validate_positive_int(performance['max_concurrent_tasks']):
                return False
            if performance['max_concurrent_tasks'] > 50:
                self.logger.warning(f"最大并发任务数设置过高: {performance['max_concurrent_tasks']}")
        
        # 验证最大浏览器资源数
        if 'max_browser_resources' in performance:
            if not self._validate_positive_int(performance['max_browser_resources']):
                return False
        
        # 验证最大浏览器并发数
        if 'max_browser_concurrent' in performance:
            if not self._validate_positive_int(performance['max_browser_concurrent']):
                return False
        
        # 验证调度循环间隔
        if 'scheduler_loop_interval' in performance:
            if not isinstance(performance['scheduler_loop_interval'], (int, float)):
                self.logger.error("调度循环间隔必须是数字")
                return False
            if performance['scheduler_loop_interval'] <= 0:
                self.logger.error("调度循环间隔必须大于0")
                return False
            if performance['scheduler_loop_interval'] < 0.01:
                self.logger.warning(f"调度循环间隔设置过小: {performance['scheduler_loop_interval']}")
        
        # 验证批量处理大小
        if 'job_batch_size' in performance:
            if not self._validate_positive_int(performance['job_batch_size']):
                return False
            if performance['job_batch_size'] > 100:
                self.logger.warning(f"批量处理大小设置过大: {performance['job_batch_size']}")
        
        return True
    
    def _validate_scheduler_timeouts_config(self, timeouts: Dict[str, Any]) -> bool:
        """验证调度器超时配置"""
        if not isinstance(timeouts, dict):
            self.logger.error("超时配置必须是字典类型")
            return False
        
        # 验证默认超时时间
        if 'default_timeout' in timeouts:
            if not self._validate_timeout(timeouts['default_timeout']):
                return False
        
        # 验证最大执行时间
        if 'max_execution_time' in timeouts:
            if not self._validate_positive_int(timeouts['max_execution_time']):
                return False
            if timeouts['max_execution_time'] > 3600:  # 1小时
                self.logger.warning(f"最大执行时间设置过长: {timeouts['max_execution_time']}秒")
        
        # 验证资源获取超时
        if 'resource_acquisition_timeout' in timeouts:
            if not self._validate_positive_int(timeouts['resource_acquisition_timeout']):
                return False
            if timeouts['resource_acquisition_timeout'] > 300:  # 5分钟
                self.logger.warning(f"资源获取超时设置过长: {timeouts['resource_acquisition_timeout']}秒")
        
        return True
    
    def _validate_scheduler_retry_config(self, retry: Dict[str, Any]) -> bool:
        """验证调度器重试配置"""
        if not isinstance(retry, dict):
            self.logger.error("重试配置必须是字典类型")
            return False
        
        # 验证重试次数
        if 'retry_attempts' in retry:
            if not self._validate_non_negative_int(retry['retry_attempts']):
                return False
            if retry['retry_attempts'] > 10:
                self.logger.warning(f"重试次数设置过多: {retry['retry_attempts']}")
        
        # 验证重试延迟
        if 'retry_delay' in retry:
            if not self._validate_positive_int(retry['retry_delay']):
                return False
            if retry['retry_delay'] < 10:  # 10秒
                self.logger.warning(f"重试延迟设置过短: {retry['retry_delay']}秒")
        
        # 验证退避因子
        if 'retry_backoff_factor' in retry:
            if not isinstance(retry['retry_backoff_factor'], (int, float)):
                self.logger.error("退避因子必须是数字")
                return False
            if retry['retry_backoff_factor'] < 1.0:
                self.logger.error("退避因子必须大于等于1.0")
                return False
            if retry['retry_backoff_factor'] > 10.0:
                self.logger.warning(f"退避因子设置过大: {retry['retry_backoff_factor']}")
        
        return True
    
    def _validate_scheduler_queue_config(self, queue: Dict[str, Any]) -> bool:
        """验证调度器队列配置"""
        if not isinstance(queue, dict):
            self.logger.error("队列配置必须是字典类型")
            return False
        
        # 验证最大队列大小
        if 'max_queue_size' in queue:
            if not self._validate_positive_int(queue['max_queue_size']):
                return False
            if queue['max_queue_size'] > 10000:
                self.logger.warning(f"最大队列大小设置过大: {queue['max_queue_size']}")
        
        # 验证队列清理间隔
        if 'queue_cleanup_interval' in queue:
            if not self._validate_positive_int(queue['queue_cleanup_interval']):
                return False
            if queue['queue_cleanup_interval'] < 60:  # 1分钟
                self.logger.warning(f"队列清理间隔设置过短: {queue['queue_cleanup_interval']}秒")
        
        return True
    
    def _validate_scheduler_monitoring_config(self, monitoring: Dict[str, Any]) -> bool:
        """验证调度器监控配置"""
        if not isinstance(monitoring, dict):
            self.logger.error("监控配置必须是字典类型")
            return False
        
        # 验证性能监控开关
        if 'enable_performance_monitoring' in monitoring:
            if not self._validate_boolean(monitoring['enable_performance_monitoring']):
                return False
        
        # 验证资源监控开关
        if 'enable_resource_monitoring' in monitoring:
            if not self._validate_boolean(monitoring['enable_resource_monitoring']):
                return False
        
        # 验证统计更新间隔
        if 'stats_update_interval' in monitoring:
            if not self._validate_positive_int(monitoring['stats_update_interval']):
                return False
            if monitoring['stats_update_interval'] < 10:  # 10秒
                self.logger.warning(f"统计更新间隔设置过短: {monitoring['stats_update_interval']}秒")
        
        return True
    
    def _validate_scheduler_priority_config(self, priority: Dict[str, Any]) -> bool:
        """验证调度器优先级配置"""
        if not isinstance(priority, dict):
            self.logger.error("优先级配置必须是字典类型")
            return False
        
        # 验证优先级调度开关
        if 'enable_priority_scheduling' in priority:
            if not self._validate_boolean(priority['enable_priority_scheduling']):
                return False
        
        # 验证优先级权重
        if 'priority_weights' in priority:
            weights = priority['priority_weights']
            if not isinstance(weights, dict):
                self.logger.error("优先级权重必须是字典类型")
                return False
            
            valid_weights = ['age_factor', 'change_frequency_factor', 'error_penalty_factor', 'success_bonus_factor']
            for weight_name, weight_value in weights.items():
                if weight_name not in valid_weights:
                    self.logger.warning(f"未知的优先级权重: {weight_name}")
                    continue
                if not isinstance(weight_value, (int, float)):
                    self.logger.error(f"优先级权重值必须是数字: {weight_name}")
                    return False
        
        return True
    
    def _validate_scheduler_error_handling_config(self, error_handling: Dict[str, Any]) -> bool:
        """验证调度器错误处理配置"""
        if not isinstance(error_handling, dict):
            self.logger.error("错误处理配置必须是字典类型")
            return False
        
        # 验证最大连续错误数
        if 'max_consecutive_errors' in error_handling:
            if not self._validate_positive_int(error_handling['max_consecutive_errors']):
                return False
            if error_handling['max_consecutive_errors'] > 20:
                self.logger.warning(f"最大连续错误数设置过大: {error_handling['max_consecutive_errors']}")
        
        # 验证错误冷却期
        if 'error_cooldown_period' in error_handling:
            if not self._validate_positive_int(error_handling['error_cooldown_period']):
                return False
            if error_handling['error_cooldown_period'] > 3600:  # 1小时
                self.logger.warning(f"错误冷却期设置过长: {error_handling['error_cooldown_period']}秒")
        
        # 验证熔断阈值
        if 'circuit_breaker_threshold' in error_handling:
            if not self._validate_positive_int(error_handling['circuit_breaker_threshold']):
                return False
            if error_handling['circuit_breaker_threshold'] > 50:
                self.logger.warning(f"熔断阈值设置过大: {error_handling['circuit_breaker_threshold']}")
        
        # 验证熔断超时
        if 'circuit_breaker_timeout' in error_handling:
            if not self._validate_positive_int(error_handling['circuit_breaker_timeout']):
                return False
            if error_handling['circuit_breaker_timeout'] > 3600:  # 1小时
                self.logger.warning(f"熔断超时设置过长: {error_handling['circuit_breaker_timeout']}秒")
        
        return True
    
    def _validate_scheduler_logging_config(self, logging: Dict[str, Any]) -> bool:
        """验证调度器日志配置"""
        if not isinstance(logging, dict):
            self.logger.error("日志配置必须是字典类型")
            return False
        
        # 验证日志级别
        if 'log_level' in logging:
            valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
            if logging['log_level'] not in valid_levels:
                self.logger.error(f"无效的日志级别: {logging['log_level']}, 可选值: {valid_levels}")
                return False
        
        # 验证执行详情日志开关
        if 'log_execution_details' in logging:
            if not self._validate_boolean(logging['log_execution_details']):
                return False
        
        # 验证性能指标日志开关
        if 'log_performance_metrics' in logging:
            if not self._validate_boolean(logging['log_performance_metrics']):
                return False
        
        return True
    
    def validate_logging_config(self, logging_config: Dict[str, Any]) -> bool:
        """
        验证日志配置
        
        Args:
            logging_config: 日志配置
            
        Returns:
            是否有效
        """
        try:
            if not isinstance(logging_config, dict):
                self.logger.error("日志配置必须是字典类型")
                return False
            
            # 验证日志级别
            if 'level' in logging_config:
                valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
                if logging_config['level'] not in valid_levels:
                    self.logger.error(f"无效的日志级别: {logging_config['level']}, 可选值: {valid_levels}")
                    return False
            
            # 验证日志目录
            if 'log_dir' in logging_config:
                if not self._validate_path(logging_config['log_dir']):
                    return False
            
            # 验证轮转配置
            if 'rotation' in logging_config:
                if not self._validate_rotation_config(logging_config['rotation']):
                    return False
            
            # 验证格式配置
            if 'format' in logging_config:
                if not self._validate_format_config(logging_config['format']):
                    return False
            
            # 验证处理器列表
            if 'handlers' in logging_config:
                if not self._validate_handlers_config(logging_config['handlers']):
                    return False
            
            # 验证压缩开关
            if 'compression' in logging_config:
                if not self._validate_boolean(logging_config['compression']):
                    return False
            
            # 验证异步模式开关
            if 'async_mode' in logging_config:
                if not self._validate_boolean(logging_config['async_mode']):
                    return False
            
            # 验证缓冲区大小
            if 'buffer_size' in logging_config:
                if not self._validate_positive_int(logging_config['buffer_size']):
                    return False
            
            self.logger.info("日志配置验证通过")
            return True
            
        except Exception as e:
            self.logger.error(f"日志配置验证失败: {e}")
            return False
    
    def _validate_rotation_config(self, rotation: Dict[str, Any]) -> bool:
        """验证轮转配置"""
        if not isinstance(rotation, dict):
            self.logger.error("轮转配置必须是字典类型")
            return False
        
        # 验证轮转类型
        if 'type' in rotation:
            if rotation['type'] not in ['time', 'size']:
                self.logger.error(f"无效的轮转类型: {rotation['type']}, 可选值: ['time', 'size']")
                return False
        
        # 验证时间轮转间隔
        if 'interval' in rotation:
            if not self._validate_positive_int(rotation['interval']):
                return False
        
        # 验证最大文件大小
        if 'max_size' in rotation:
            if not self._validate_positive_int(rotation['max_size']):
                return False
        
        # 验证备份数量
        if 'backup_count' in rotation:
            if not self._validate_non_negative_int(rotation['backup_count']):
                return False
        
        # 验证保留天数
        if 'retention_days' in rotation:
            if not self._validate_positive_int(rotation['retention_days']):
                return False
        
        return True
    
    def _validate_format_config(self, format_config: Dict[str, Any]) -> bool:
        """验证格式配置"""
        if not isinstance(format_config, dict):
            self.logger.error("格式配置必须是字典类型")
            return False
        
        # 验证控制台格式
        if 'console' in format_config:
            if not isinstance(format_config['console'], str):
                self.logger.error("控制台格式必须是字符串")
                return False
        
        # 验证文件格式
        if 'file' in format_config:
            if not isinstance(format_config['file'], str):
                self.logger.error("文件格式必须是字符串")
                return False
        
        return True
    
    def _validate_handlers_config(self, handlers: list) -> bool:
        """验证处理器配置"""
        if not isinstance(handlers, list):
            self.logger.error("处理器配置必须是列表类型")
            return False
        
        valid_handlers = ['console', 'file', 'error_file']
        for handler in handlers:
            if handler not in valid_handlers:
                self.logger.error(f"无效的处理器类型: {handler}, 可选值: {valid_handlers}")
                return False
        
        return True
    
    def validate_task_config(self, task_config: Dict[str, Any]) -> bool:
        """
        验证任务配置
        
        Args:
            task_config: 任务配置
            
        Returns:
            是否有效
        """
        try:
            # 验证必需字段
            required_fields = ['id', 'url', 'name']
            for field in required_fields:
                if field not in task_config:
                    self.logger.error(f"任务配置缺少必需字段: {field}")
                    return False
            
            # 验证任务ID
            if not self._validate_task_id(task_config['id']):
                return False
            
            # 验证URL
            if not self._validate_url(task_config['url']):
                return False
            
            # 验证名称
            if not self._validate_task_name(task_config['name']):
                return False
            
            # 验证选择器
            if 'selectors' in task_config:
                if not self._validate_selectors(task_config['selectors']):
                    return False
            
            # 验证间隔时间
            if 'interval' in task_config:
                if not self._validate_interval(task_config['interval']):
                    return False
            
            # 验证超时时间
            if 'timeout' in task_config:
                if not self._validate_timeout(task_config['timeout']):
                    return False
            
            # 验证状态字段
            if 'enabled' in task_config:
                if not self._validate_boolean(task_config['enabled']):
                    return False
            
            # 验证状态值
            if 'status' in task_config:
                if not self._validate_task_status(task_config['status']):
                    return False
            
            # 验证时间戳字段
            timestamp_fields = ['created_at', 'updated_at', 'last_check', 'last_change']
            for field in timestamp_fields:
                if field in task_config and task_config[field]:
                    if not self._validate_timestamp(task_config[field]):
                        return False
            
            # 验证变化次数
            if 'change_count' in task_config:
                if not self._validate_non_negative_int(task_config['change_count']):
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"任务配置验证失败: {e}")
            return False
    
    def validate_url(self, url: str) -> bool:
        """
        验证URL格式
        
        Args:
            url: URL字符串
            
        Returns:
            是否有效
        """
        return self._validate_url(url)
    
    def validate_css_selector(self, selector: str) -> bool:
        """
        验证CSS选择器格式
        
        Args:
            selector: CSS选择器
            
        Returns:
            是否有效
        """
        return self._validate_css_selector(selector)
    
    def _validate_basic_structure(self, config: Dict[str, Any]) -> bool:
        """验证基本结构"""
        if not isinstance(config, dict):
            self.logger.error("配置必须是字典类型")
            return False
        
        # 检查顶级字段
        required_top_level = ['version', 'monitoring', 'detection', 'notification', 'storage']
        for field in required_top_level:
            if field not in config:
                self.logger.error(f"缺少必需字段: {field}")
                return False
        
        return True
    
    def _validate_version(self, version: Any) -> bool:
        """验证版本号"""
        if not isinstance(version, str):
            self.logger.error("版本号必须是字符串")
            return False
        
        # 验证版本号格式 (例如: "1.0.0")
        version_pattern = r'^\d+\.\d+\.\d+$'
        if not re.match(version_pattern, version):
            self.logger.error(f"版本号格式无效: {version}")
            return False
        
        return True
    
    def _validate_monitoring_config(self, monitoring: Dict[str, Any]) -> bool:
        """验证监控配置"""
        if not isinstance(monitoring, dict):
            self.logger.error("监控配置必须是字典类型")
            return False
        
        # 验证默认间隔时间
        if 'default_interval' in monitoring:
            if not self._validate_interval(monitoring['default_interval']):
                return False
        
        # 验证默认超时时间
        if 'default_timeout' in monitoring:
            if not self._validate_timeout(monitoring['default_timeout']):
                return False
        
        # 验证最大重试次数
        if 'max_retries' in monitoring:
            if not self._validate_non_negative_int(monitoring['max_retries']):
                return False
        
        # 验证并发任务数
        if 'concurrent_tasks' in monitoring:
            if not self._validate_positive_int(monitoring['concurrent_tasks']):
                return False
        
        # 验证浏览器无头模式
        if 'browser_headless' in monitoring:
            if not self._validate_boolean(monitoring['browser_headless']):
                return False
        
        # 验证速率限制配置
        if 'rate_limit' in monitoring:
            rate_limit = monitoring['rate_limit']
            if isinstance(rate_limit, dict):
                if 'requests_per_minute' in rate_limit:
                    if not self._validate_positive_int(rate_limit['requests_per_minute']):
                        return False
                if 'retry_delay' in rate_limit:
                    if not self._validate_positive_int(rate_limit['retry_delay']):
                        return False
        
        return True
    
    def _validate_detection_config(self, detection: Dict[str, Any]) -> bool:
        """验证检测配置"""
        if not isinstance(detection, dict):
            self.logger.error("检测配置必须是字典类型")
            return False
        
        # 验证智能检测开关
        if 'enable_smart_detection' in detection:
            if not self._validate_boolean(detection['enable_smart_detection']):
                return False
        
        # 验证相似度阈值
        if 'similarity_threshold' in detection:
            if not self._validate_threshold(detection['similarity_threshold']):
                return False
        
        # 验证最小变化长度
        if 'min_change_length' in detection:
            if not self._validate_positive_int(detection['min_change_length']):
                return False
        
        # 验证忽略选择器
        if 'ignore_selectors' in detection:
            ignore_selectors = detection['ignore_selectors']
            if isinstance(ignore_selectors, list):
                for selector in ignore_selectors:
                    if not self._validate_css_selector(selector):
                        return False
        
        # 验证提取字段配置
        if 'extract_fields' in detection:
            extract_fields = detection['extract_fields']
            if isinstance(extract_fields, dict):
                for field_name, selector in extract_fields.items():
                    if not isinstance(field_name, str) or not field_name.strip():
                        self.logger.error(f"提取字段名无效: {field_name}")
                        return False
                    if not self._validate_css_selector(selector):
                        return False
        
        return True
    
    def _validate_notification_config(self, notification: Dict[str, Any]) -> bool:
        """验证通知配置"""
        if not isinstance(notification, dict):
            self.logger.error("通知配置必须是字典类型")
            return False
        
        # 验证平台列表
        if 'platforms' in notification:
            platforms = notification['platforms']
            if isinstance(platforms, list):
                valid_platforms = ['pushplus', 'telegram', 'discord', 'feishu']
                for platform in platforms:
                    if not isinstance(platform, str) or platform not in valid_platforms:
                        self.logger.error(f"无效的通知平台: {platform}")
                        return False
        
        # 验证消息模板
        if 'template' in notification:
            template = notification['template']
            if isinstance(template, dict):
                if 'title' in template and not isinstance(template['title'], str):
                    self.logger.error("消息标题必须是字符串")
                    return False
                if 'content' in template and not isinstance(template['content'], str):
                    self.logger.error("消息内容必须是字符串")
                    return False
                if 'rate_limit' in template and not self._validate_positive_int(template['rate_limit']):
                    return False
        
        # 验证平台配置
        if 'platform_configs' in notification:
            platform_configs = notification['platform_configs']
            if isinstance(platform_configs, dict):
                for platform, config in platform_configs.items():
                    if isinstance(config, dict):
                        if 'enabled' in config and not self._validate_boolean(config['enabled']):
                            return False
                        # 验证平台特定配置
                        if platform == 'pushplus' and 'token' in config:
                            if not self._validate_token(config['token']):
                                return False
                        elif platform == 'telegram':
                            if 'bot_token' in config and not self._validate_token(config['bot_token']):
                                return False
                            if 'chat_id' in config and not isinstance(config['chat_id'], str):
                                return False
                        elif platform in ['discord', 'feishu'] and 'webhook_url' in config:
                            if not self._validate_webhook_url(config['webhook_url']):
                                return False
        
        return True
    
    def _validate_storage_config(self, storage: Dict[str, Any]) -> bool:
        """验证存储配置"""
        if not isinstance(storage, dict):
            self.logger.error("存储配置必须是字典类型")
            return False
        
        # 验证历史文件路径
        if 'history_file' in storage:
            if not self._validate_path(storage['history_file']):
                return False
        
        # 验证最大历史条目数
        if 'max_history_entries' in storage:
            if not self._validate_positive_int(storage['max_history_entries']):
                return False
        
        # 验证自动清理天数
        if 'auto_cleanup_days' in storage:
            if not self._validate_positive_int(storage['auto_cleanup_days']):
                return False
        
        return True
    
    def _validate_tasks_config(self, tasks: List[Dict[str, Any]]) -> bool:
        """验证任务配置列表"""
        if not isinstance(tasks, list):
            self.logger.error("任务配置必须是列表类型")
            return False
        
        # 验证任务ID唯一性
        task_ids = set()
        for i, task in enumerate(tasks):
            if not isinstance(task, dict):
                self.logger.error(f"任务 {i} 必须是字典类型")
                return False
            
            task_id = task.get('id')
            if task_id:
                if task_id in task_ids:
                    self.logger.error(f"任务ID重复: {task_id}")
                    return False
                task_ids.add(task_id)
            
            # 验证单个任务配置
            if not self.validate_task_config(task):
                return False
        
        return True
    
    def _validate_push_tokens(self, env_config: Dict[str, Any]) -> bool:
        """验证推送平台令牌"""
        token_fields = ['PUSHPLUS_TOKEN', 'TELEGRAM_BOT_TOKEN', 'DISCORD_WEBHOOK_URL', 'FEISHU_WEBHOOK_URL']
        
        for field in token_fields:
            if field in env_config and env_config[field]:
                if not self._validate_token(env_config[field]):
                    return False
        
        return True
    
    def _validate_monitoring_env(self, env_config: Dict[str, Any]) -> bool:
        """验证监控相关环境变量"""
        # 验证默认间隔时间
        if 'DEFAULT_INTERVAL' in env_config and env_config['DEFAULT_INTERVAL']:
            if not self._validate_interval(env_config['DEFAULT_INTERVAL']):
                return False
        
        # 验证默认超时时间
        if 'DEFAULT_TIMEOUT' in env_config and env_config['DEFAULT_TIMEOUT']:
            if not self._validate_timeout(env_config['DEFAULT_TIMEOUT']):
                return False
        
        # 验证最大重试次数
        if 'MAX_RETRIES' in env_config and env_config['MAX_RETRIES']:
            if not self._validate_non_negative_int(env_config['MAX_RETRIES']):
                return False
        
        # 验证并发任务数
        if 'CONCURRENT_TASKS' in env_config and env_config['CONCURRENT_TASKS']:
            if not self._validate_positive_int(env_config['CONCURRENT_TASKS']):
                return False
        
        return True
    
    def _validate_detection_env(self, env_config: Dict[str, Any]) -> bool:
        """验证检测相关环境变量"""
        # 验证相似度阈值
        if 'SIMILARITY_THRESHOLD' in env_config and env_config['SIMILARITY_THRESHOLD']:
            if not self._validate_threshold(env_config['SIMILARITY_THRESHOLD']):
                return False
        
        # 验证最小变化长度
        if 'MIN_CHANGE_LENGTH' in env_config and env_config['MIN_CHANGE_LENGTH']:
            if not self._validate_positive_int(env_config['MIN_CHANGE_LENGTH']):
                return False
        
        return True
    
    def _validate_logging_env(self, env_config: Dict[str, Any]) -> bool:
        """验证日志相关环境变量"""
        # 验证日志级别
        if 'LOG_LEVEL' in env_config and env_config['LOG_LEVEL']:
            valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
            if env_config['LOG_LEVEL'] not in valid_levels:
                self.logger.error(f"无效的日志级别: {env_config['LOG_LEVEL']}")
                return False
        
        # 验证日志文件路径
        if 'LOG_FILE' in env_config and env_config['LOG_FILE']:
            if not self._validate_path(env_config['LOG_FILE']):
                return False
        
        # 验证日志备份数量
        if 'LOG_BACKUP_COUNT' in env_config and env_config['LOG_BACKUP_COUNT']:
            if not self._validate_non_negative_int(env_config['LOG_BACKUP_COUNT']):
                return False
        
        return True
    
    def _validate_advanced_env(self, env_config: Dict[str, Any]) -> bool:
        """验证高级环境变量"""
        # 验证代理URL
        if 'PROXY_URL' in env_config and env_config['PROXY_URL']:
            if not self._validate_url(env_config['PROXY_URL']):
                return False
        
        # 验证每分钟请求限制
        if 'RATE_LIMIT_PER_MINUTE' in env_config and env_config['RATE_LIMIT_PER_MINUTE']:
            if not self._validate_positive_int(env_config['RATE_LIMIT_PER_MINUTE']):
                return False
        
        return True
    
    # 基础验证方法
    def _validate_url(self, url: str) -> bool:
        """验证URL格式"""
        if not isinstance(url, str):
            return False
        
        # 检查是否为环境变量占位符
        if url.startswith('${') and url.endswith('}'):
            # 环境变量占位符，暂时认为是有效的
            return True
        
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                self.logger.error(f"URL格式无效: {url}")
                return False
            
            # 检查协议
            if parsed.scheme not in ['http', 'https']:
                self.logger.error(f"不支持的URL协议: {parsed.scheme}")
                return False
            
            # 检查主机名
            if not parsed.hostname:
                self.logger.error(f"URL缺少主机名: {url}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"URL验证失败: {url}, 错误: {e}")
            return False
    
    def _validate_email(self, email: str) -> bool:
        """验证邮箱格式"""
        if not isinstance(email, str):
            return False
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            self.logger.error(f"邮箱格式无效: {email}")
            return False
        
        return True
    
    def _validate_path(self, path: str) -> bool:
        """验证文件路径"""
        if not isinstance(path, str):
            return False
        
        # 基本的路径验证
        if not path.strip():
            self.logger.error("文件路径不能为空")
            return False
        
        # 检查是否包含非法字符
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
        if any(char in path for char in invalid_chars):
            self.logger.error(f"文件路径包含非法字符: {path}")
            return False
        
        return True
    
    def _validate_timeout(self, timeout: int) -> bool:
        """验证超时时间"""
        if not self._validate_positive_int(timeout):
            return False
        
        # 合理的超时时间范围: 1000-60000 毫秒
        if timeout < 1000 or timeout > 60000:
            self.logger.warning(f"超时时间超出推荐范围: {timeout} 毫秒 (推荐: 1000-60000)")
        
        return True
    
    def _validate_interval(self, interval: int) -> bool:
        """验证间隔时间"""
        if not self._validate_positive_int(interval):
            return False
        
        # 合理的间隔时间范围: 60-86400 秒 (1分钟到24小时)
        if interval < 60 or interval > 86400:
            self.logger.warning(f"间隔时间超出推荐范围: {interval} 秒 (推荐: 60-86400)")
        
        return True
    
    def _validate_threshold(self, threshold: float) -> bool:
        """验证相似度阈值"""
        if not isinstance(threshold, (int, float)):
            self.logger.error("相似度阈值必须是数字")
            return False
        
        # 合理的阈值范围: 0.1-1.0
        if threshold < 0.1 or threshold > 1.0:
            self.logger.error(f"相似度阈值超出范围: {threshold} (推荐: 0.1-1.0)")
            return False
        
        return True
    
    def _validate_percentage(self, percentage: Union[int, float]) -> bool:
        """验证百分比"""
        if not isinstance(percentage, (int, float)):
            self.logger.error("百分比必须是数字")
            return False
        
        if percentage < 0 or percentage > 100:
            self.logger.error(f"百分比超出范围: {percentage} (范围: 0-100)")
            return False
        
        return True
    
    def _validate_positive_int(self, value: int) -> bool:
        """验证正整数"""
        if not isinstance(value, int) or value <= 0:
            self.logger.error(f"必须是正整数: {value}")
            return False
        
        return True
    
    def _validate_non_negative_int(self, value: int) -> bool:
        """验证非负整数"""
        if not isinstance(value, int) or value < 0:
            self.logger.error(f"必须是非负整数: {value}")
            return False
        
        return True
    
    def _validate_positive_float(self, value: float) -> bool:
        """验证正浮点数"""
        if not isinstance(value, (int, float)) or value <= 0:
            self.logger.error(f"必须是正数: {value}")
            return False
        
        return True
    
    def _validate_boolean(self, value: Any) -> bool:
        """验证布尔值"""
        if not isinstance(value, bool):
            self.logger.error(f"必须是布尔值: {value}")
            return False
        
        return True
    
    def _validate_color(self, color: str) -> bool:
        """验证颜色格式"""
        if not isinstance(color, str):
            return False
        
        # 支持十六进制颜色 (#RGB 或 #RRGGBB)
        color_pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
        if not re.match(color_pattern, color):
            self.logger.error(f"颜色格式无效: {color}")
            return False
        
        return True
    
    def _validate_css_selector(self, selector: str) -> bool:
        """验证CSS选择器格式"""
        if not isinstance(selector, str):
            return False
        
        if not selector.strip():
            self.logger.error("CSS选择器不能为空")
            return False
        
        # 基本的选择器验证
        if len(selector) > 500:
            self.logger.error(f"CSS选择器过长: {len(selector)} 字符")
            return False
        
        # 检查是否包含明显的语法错误
        if selector.count('(') != selector.count(')'):
            self.logger.error(f"CSS选择器括号不匹配: {selector}")
            return False
        
        if selector.count('[') != selector.count(']'):
            self.logger.error(f"CSS选择器方括号不匹配: {selector}")
            return False
        
        return True
    
    def _validate_webhook_url(self, url: str) -> bool:
        """验证Webhook URL"""
        if not self._validate_url(url):
            return False
        
        # 检查是否包含webhook关键字
        if 'webhook' not in url.lower() and 'bot' not in url.lower():
            self.logger.warning(f"URL可能不是有效的webhook: {url}")
        
        return True
    
    def _validate_token(self, token: str) -> bool:
        """验证令牌格式"""
        if not isinstance(token, str):
            return False
        
        # 检查是否为环境变量占位符
        if token.startswith('${') and token.endswith('}'):
            # 环境变量占位符，暂时认为是有效的
            return True
        
        if not token.strip():
            self.logger.error("令牌不能为空")
            return False
        
        # 基本的令牌长度验证
        if len(token) < 10:
            self.logger.warning(f"令牌长度过短: {len(token)} 字符")
        
        if len(token) > 1000:
            self.logger.error(f"令牌长度过长: {len(token)} 字符")
            return False
        
        return True
    
    def _validate_task_id(self, task_id: str) -> bool:
        """验证任务ID"""
        if not isinstance(task_id, str):
            self.logger.error("任务ID必须是字符串")
            return False
        
        if not task_id.strip():
            self.logger.error("任务ID不能为空")
            return False
        
        # 任务ID格式: 允许字母、数字、连字符和下划线，长度1-50
        task_id_pattern = r'^[a-zA-Z0-9_-]{1,50}$'
        if not re.match(task_id_pattern, task_id):
            self.logger.error(f"任务ID格式无效: {task_id} (只允许字母、数字、连字符和下划线，长度1-50)")
            return False
        
        return True
    
    def _validate_task_name(self, name: str) -> bool:
        """验证任务名称"""
        if not isinstance(name, str):
            self.logger.error("任务名称必须是字符串")
            return False
        
        if not name.strip():
            self.logger.error("任务名称不能为空")
            return False
        
        if len(name) > 100:
            self.logger.error(f"任务名称过长: {len(name)} 字符")
            return False
        
        return True
    
    def _validate_selectors(self, selectors: List[str]) -> bool:
        """验证选择器列表"""
        if not isinstance(selectors, list):
            self.logger.error("选择器必须是列表类型")
            return False
        
        for i, selector in enumerate(selectors):
            if not self._validate_css_selector(selector):
                self.logger.error(f"选择器 {i} 格式无效: {selector}")
                return False
        
        return True
    
    def _validate_task_status(self, status: str) -> bool:
        """验证任务状态"""
        if not isinstance(status, str):
            self.logger.error("任务状态必须是字符串")
            return False
        
        valid_statuses = ['active', 'inactive', 'error', 'paused']
        if status not in valid_statuses:
            self.logger.error(f"无效的任务状态: {status}, 可选值: {valid_statuses}")
            return False
        
        return True
    
    def _validate_timestamp(self, timestamp: str) -> bool:
        """验证时间戳格式"""
        if not isinstance(timestamp, str):
            self.logger.error("时间戳必须是字符串")
            return False
        
        try:
            # 尝试解析ISO格式时间戳
            from datetime import datetime
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return True
        except ValueError:
            self.logger.error(f"时间戳格式无效: {timestamp}")
            return False