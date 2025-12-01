# 调度器配置管理

从版本 1.1.0 开始，webmon 项目引入了专门的调度器配置管理功能，通过 ConfigManager 提供对调度器各项参数的集中管理和配置。

## 概述

新的调度器配置系统提供以下功能：

1. **集中配置管理** - 所有调度器相关配置集中在 `config.json` 的 `scheduler` 部分
2. **配置验证** - 内置的配置验证器确保配置参数的有效性
3. **动态更新** - 支持运行时动态更新调度器配置
4. **性能优化建议** - 提供配置性能分析和优化建议
5. **向后兼容** - 完全兼容旧的配置格式

## 配置文件结构

调度器配置位于 `config.json` 文件的 `scheduler` 部分，包含以下主要配置块：

```json
{
  "scheduler": {
    "performance": {
      "max_concurrent_tasks": 10,           // 最大并发任务数
      "max_browser_resources": 5,           // 最大浏览器资源数
      "max_browser_concurrent": 3,          // 最大浏览器并发数
      "scheduler_loop_interval": 0.1,       // 调度循环间隔（秒）
      "job_batch_size": 10                  // 批量处理大小
    },
    "timeouts": {
      "default_timeout": 30000,             // 默认超时时间（毫秒）
      "max_execution_time": 300,            // 最大执行时间（秒）
      "resource_acquisition_timeout": 30    // 资源获取超时（秒）
    },
    "retry": {
      "retry_attempts": 3,                  // 最大重试次数
      "retry_delay": 60,                    // 重试延迟（秒）
      "retry_backoff_factor": 2.0           // 退避因子
    },
    "queue": {
      "max_queue_size": 1000,               // 最大队列大小
      "queue_cleanup_interval": 300         // 队列清理间隔（秒）
    },
    "monitoring": {
      "enable_performance_monitoring": true,    // 启用性能监控
      "enable_resource_monitoring": true,       // 启用资源监控
      "stats_update_interval": 60               // 统计更新间隔（秒）
    },
    "priority": {
      "enable_priority_scheduling": true,       // 启用优先级调度
      "priority_weights": {
        "age_factor": 1.0,                      // 时间权重因子
        "change_frequency_factor": 2.0,         // 变化频率权重因子
        "error_penalty_factor": 5.0,            // 错误惩罚因子
        "success_bonus_factor": -1.0            // 成功奖励因子
      }
    },
    "error_handling": {
      "max_consecutive_errors": 5,          // 最大连续错误数
      "error_cooldown_period": 300,         // 错误冷却期（秒）
      "circuit_breaker_threshold": 10,      // 熔断阈值
      "circuit_breaker_timeout": 600        // 熔断超时（秒）
    },
    "logging": {
      "log_level": "INFO",                  // 日志级别
      "log_execution_details": true,        // 记录执行详情
      "log_performance_metrics": true       // 记录性能指标
    }
  }
}
```

## 基本用法

### 获取调度器配置

```python
from webmon.config import ConfigManager

# 创建配置管理器
config_manager = ConfigManager()

# 获取完整的调度器配置
scheduler_config = config_manager.get_scheduler_config()

# 获取特定的配置值（支持点号分隔）
max_tasks = config_manager.get_scheduler_config_value('performance.max_concurrent_tasks')
timeout = config_manager.get_scheduler_config_value('timeouts.default_timeout')
```

### 更新调度器配置

```python
# 定义新的配置
new_config = {
    "performance": {
        "max_concurrent_tasks": 15,
        "scheduler_loop_interval": 0.2
    },
    "retry": {
        "retry_attempts": 5,
        "retry_delay": 120
    }
}

# 更新配置
success = config_manager.update_scheduler_config(new_config)
print(f"配置更新{'成功' if success else '失败'}")
```

### 与任务调度器集成

```python
from webmon.scheduler.task_scheduler import TaskScheduler

# 创建任务调度器（自动使用最新的调度器配置）
scheduler = TaskScheduler(config_manager)

# 获取当前调度器配置
current_config = scheduler.get_scheduler_config()

# 动态更新调度器配置
new_settings = {
    "performance": {
        "max_concurrent_tasks": 20,
        "job_batch_size": 15
    }
}
success = scheduler.update_scheduler_config(new_settings)
```

## 配置验证

### 基本验证

```python
# 验证调度器配置
is_valid = config_manager.validator.validate_scheduler_config(scheduler_config)
print(f"配置验证{'通过' if is_valid else '失败'}")
```

### 详细验证

调度器配置验证器会检查以下方面：

1. **性能配置验证**
   - 确保所有数值参数为正数
   - 检查合理的参数范围
   - 验证参数间的逻辑关系

2. **超时配置验证**
   - 验证超时时间的合理性
   - 检查超时参数的范围

3. **重试配置验证**
   - 验证重试次数和延迟
   - 检查退避因子的合理性

4. **队列配置验证**
   - 验证队列大小的合理性
   - 检查清理间隔

5. **监控配置验证**
   - 验证监控开关参数
   - 检查统计更新间隔

6. **优先级配置验证**
   - 验证优先级权重
   - 检查权重参数的合理性

7. **错误处理配置验证**
   - 验证错误处理参数
   - 检查熔断参数

8. **日志配置验证**
   - 验证日志级别
   - 检查日志开关参数

## 性能优化

### 获取性能优化建议

```python
from webmon.scheduler.scheduler_config import SchedulerConfig

# 从配置管理器创建调度器配置
scheduler_config = SchedulerConfig.from_config_manager(config_manager)

# 获取性能优化建议
recommendations = scheduler_config.get_performance_recommendations()
for rec in recommendations:
    print(f"优化建议: {rec}")
```

### 性能验证

```python
# 验证性能配置
validation_result = scheduler_config.validate_performance()
print(f"配置有效性: {validation_result['valid']}")
print(f"估计内存使用: {validation_result['estimated_memory_mb']}MB")
print(f"总超时时间: {validation_result['total_timeout_seconds']}秒")

if validation_result['issues']:
    print("发现的问题:")
    for issue in validation_result['issues']:
        print(f"  - {issue}")

if validation_result['warnings']:
    print("警告信息:")
    for warning in validation_result['warnings']:
        print(f"  - {warning}")
```

## 最佳实践

### 生产环境推荐配置

```python
production_config = {
    "performance": {
        "max_concurrent_tasks": 8,          // 适中的并发数，避免资源竞争
        "max_browser_resources": 4,         // 根据服务器内存调整
        "max_browser_concurrent": 2,        // 避免浏览器过载
        "scheduler_loop_interval": 0.1,     // 保持响应性
        "job_batch_size": 5                 // 适中的批处理大小
    },
    "timeouts": {
        "default_timeout": 20000,           // 20秒超时，平衡速度和稳定性
        "max_execution_time": 180,          // 3分钟最大执行时间
        "resource_acquisition_timeout": 20  // 20秒资源获取超时
    },
    "retry": {
        "retry_attempts": 2,                // 较少的重试次数，避免资源浪费
        "retry_delay": 120,                 // 较长的重试延迟，避免频繁重试
        "retry_backoff_factor": 2.0         // 指数退避
    },
    "monitoring": {
        "enable_performance_monitoring": True,    // 启用性能监控
        "enable_resource_monitoring": True,       // 启用资源监控
        "stats_update_interval": 60               // 每分钟更新统计
    },
    "priority": {
        "enable_priority_scheduling": True,       // 启用智能优先级调度
        "priority_weights": {
            "age_factor": 1.0,
            "change_frequency_factor": 2.0,
            "error_penalty_factor": 3.0,        // 降低错误惩罚
            "success_bonus_factor": -0.5        // 降低成功奖励
        }
    },
    "error_handling": {
        "max_consecutive_errors": 3,        // 较低的连续错误阈值
        "error_cooldown_period": 600,       // 10分钟冷却期
        "circuit_breaker_threshold": 5,     // 较低的熔断阈值
        "circuit_breaker_timeout": 1800     // 30分钟熔断超时
    },
    "logging": {
        "log_level": "INFO",                // 适当的日志级别
        "log_execution_details": True,      // 记录执行详情
        "log_performance_metrics": True     // 记录性能指标
    }
}
```

### 配置调优建议

1. **并发任务数调优**
   - 从较低的数值开始（如 5-8 个）
   - 根据服务器 CPU 和内存使用情况逐步增加
   - 监控任务执行时间和系统资源使用率

2. **浏览器资源调优**
   - 每个浏览器实例大约需要 200-300MB 内存
   - 根据服务器总内存计算合理的浏览器资源数
   - 确保 `max_browser_concurrent` ≤ `max_browser_resources`

3. **重试策略调优**
   - 生产环境中使用较少的重试次数（2-3 次）
   - 使用指数退避策略避免频繁重试
   - 设置合理的重试延迟（60-300 秒）

4. **监控配置建议**
   - 始终启用性能和资源监控
   - 根据实际需求调整统计更新间隔
   - 定期检查性能指标和日志

## 向后兼容性

新的调度器配置系统完全向后兼容旧的配置格式。如果 `config.json` 中没有 `scheduler` 部分，系统会自动从旧的配置格式中提取相关参数：

- 从 `monitoring` 部分获取基本的性能参数
- 从 `storage` 部分获取队列相关参数
- 使用默认值补充缺失的配置项

## 故障排除

### 常见配置问题

1. **配置更新失败**
   - 检查配置格式是否正确
   - 验证配置参数的有效性
   - 查看日志文件获取详细错误信息

2. **性能问题**
   - 使用性能验证功能检查配置
   - 参考性能优化建议调整参数
   - 监控系统资源使用情况

3. **调度器异常**
   - 检查日志级别是否适当
   - 验证错误处理配置
   - 监控任务执行状态

### 调试技巧

```python
import logging

# 启用调试日志
logging.getLogger('webmon.config').setLevel(logging.DEBUG)
logging.getLogger('webmon.scheduler').setLevel(logging.DEBUG)

# 详细配置验证
config_manager = ConfigManager()
is_valid = config_manager.validate_config()
print(f"完整配置验证: {'通过' if is_valid else '失败'}")
```

## API 参考

### ConfigManager 新增方法

- `get_scheduler_config()` - 获取完整的调度器配置
- `get_scheduler_config_value(key, default=None)` - 获取特定的配置值
- `update_scheduler_config(scheduler_config)` - 更新调度器配置

### ConfigValidator 新增方法

- `validate_scheduler_config(scheduler_config)` - 验证调度器配置

### TaskScheduler 新增方法

- `get_scheduler_config()` - 获取当前调度器配置
- `update_scheduler_config(new_config)` - 动态更新调度器配置
- `validate_scheduler_config(config)` - 验证调度器配置

### SchedulerConfig 新增功能

- `from_config_manager(config_manager)` - 从配置管理器创建配置
- `to_dict()` - 将配置转换为字典
- `from_dict(config_dict)` - 从字典创建配置
- `get_performance_recommendations()` - 获取性能优化建议
- `validate_performance()` - 验证性能配置

## 更新日志

### v1.1.0
- 新增调度器配置管理功能
- 添加配置验证器
- 支持动态配置更新
- 集成性能优化建议
- 保持向后兼容性