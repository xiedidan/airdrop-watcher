# 日志配置管理指南

本文档介绍webmon项目中新增的日志配置管理功能。

## 概述

webmon项目现在通过ConfigManager类提供了完整的日志配置管理功能。所有日志配置都可以通过配置管理器统一管理，支持动态修改和验证。

## 新增功能

### 1. ConfigManager类新增方法

#### 获取日志配置
```python
# 获取日志配置字典
logging_config = config_manager.get_logging_config()

# 获取日志配置对象
log_config = config_manager.get_log_config()
```

#### 修改日志配置
```python
# 设置日志级别
config_manager.set_log_level("DEBUG")  # 支持: DEBUG, INFO, WARNING, ERROR, CRITICAL

# 设置日志目录
config_manager.set_log_directory("./logs")

# 配置日志轮转
config_manager.configure_log_rotation("size", max_size=10*1024*1024, backup_count=5)
config_manager.configure_log_rotation("time", interval=1, retention_days=30)

# 添加/移除日志处理器
config_manager.add_log_handler("error_file")
config_manager.remove_log_handler("console")

# 启用/禁用功能
config_manager.enable_log_compression(True)
config_manager.enable_async_logging(True)

# 设置缓冲区大小
config_manager.set_buffer_size(1000)
```

#### 查询和验证
```python
# 获取特定配置值（支持点号分隔）
level = config_manager.get_logging_config_value("level")
rotation_type = config_manager.get_logging_config_value("rotation.type")

# 获取日志文件路径
log_paths = config_manager.get_log_file_paths()

# 估计日志大小
size_info = config_manager.estimate_log_size(tasks_per_day=100, avg_log_size=200)

# 验证日志配置
is_valid = config_manager.validator.validate_logging_config(logging_config)

# 重置为默认配置
config_manager.reset_logging_config()
```

### 2. 配置文件结构

在`config.json`中新增了`logging`配置段：

```json
{
  "logging": {
    "level": "INFO",
    "log_dir": "./logs",
    "rotation": {
      "type": "time",           // "time" 或 "size"
      "interval": 1,            // 时间轮转间隔(天)
      "max_size": 10485760,     // 最大文件大小(字节)
      "backup_count": 5,        // 备份文件数量
      "retention_days": 30      // 保留天数
    },
    "format": {
      "console": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>",
      "file": "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    },
    "handlers": ["console", "file", "error_file"],
    "compression": true,
    "async_mode": true,
    "buffer_size": 1000
  }
}
```

### 3. 配置验证器增强

ConfigValidator类新增了日志配置验证方法：

```python
# 验证完整的日志配置
is_valid = validator.validate_logging_config(logging_config)

# 验证特定部分
is_valid = validator._validate_rotation_config(rotation_config)
is_valid = validator._validate_format_config(format_config)
is_valid = validator._validate_handlers_config(handlers_list)
```

## 使用示例

### 基本使用
```python
from webmon.config.config_manager import ConfigManager

# 创建配置管理器
config_manager = ConfigManager()

# 获取当前日志配置
logging_config = config_manager.get_logging_config()
print(f"当前日志级别: {logging_config['level']}")

# 修改日志级别
config_manager.set_log_level("DEBUG")

# 设置日志目录
config_manager.set_log_directory("./my_logs")

# 配置日志轮转
config_manager.configure_log_rotation("size", max_size=5*1024*1024, backup_count=3)
```

### 高级配置
```python
# 创建自定义日志配置
custom_config = {
    "level": "WARNING",
    "log_dir": "./custom_logs",
    "rotation": {
        "type": "time",
        "interval": 7,  # 每周轮转
        "retention_days": 30
    },
    "format": {
        "console": "{time:HH:mm:ss} | {level} | {message}",
        "file": "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name} | {message}"
    },
    "handlers": ["console", "file"],
    "compression": False,
    "async_mode": False,
    "buffer_size": 500
}

# 更新配置
config_manager.update_logging_config(custom_config)
```

### 查询和监控
```python
# 获取日志文件路径
log_paths = config_manager.get_log_file_paths()
print(f"主日志文件: {log_paths.get('main')}")
print(f"错误日志文件: {log_paths.get('error')}")

# 估计日志大小
size_info = config_manager.estimate_log_size(
    tasks_per_day=100,
    avg_log_size=200
)
print(f"预计每日日志量: {size_info['daily_logs_bytes']} 字节")
print(f"预计保留天数: {size_info['estimated_retention_days']}")

# 验证配置
is_valid = config_manager.validator.validate_logging_config(
    config_manager.get_logging_config()
)
print(f"配置有效性: {is_valid}")
```

## 配置参数说明

### 日志级别
- `DEBUG`: 最详细的日志信息
- `INFO`: 一般信息（默认）
- `WARNING`: 警告信息
- `ERROR`: 错误信息
- `CRITICAL`: 严重错误信息

### 轮转类型
- `time`: 基于时间的轮转
  - `interval`: 轮转间隔（天）
  - `retention_days`: 保留天数
- `size`: 基于文件大小的轮转
  - `max_size`: 最大文件大小（字节）
  - `backup_count`: 备份文件数量

### 处理器类型
- `console`: 控制台输出
- `file`: 普通日志文件
- `error_file`: 错误日志文件（仅记录ERROR及以上级别）

### 其他选项
- `compression`: 是否压缩旧的日志文件
- `async_mode`: 是否使用异步日志记录
- `buffer_size`: 日志缓冲区大小

## 集成说明

日志配置管理器与现有的配置系统完全集成：

1. **统一配置管理**: 所有配置都通过ConfigManager统一管理
2. **自动保存**: 修改配置后自动保存到配置文件
3. **配置验证**: 提供完整的配置验证功能
4. **向后兼容**: 不影响现有的配置功能
5. **动态更新**: 支持运行时动态更新配置

## 最佳实践

1. **日志级别**: 开发环境使用DEBUG，生产环境使用INFO或WARNING
2. **日志目录**: 使用专用的日志目录，定期清理
3. **轮转策略**: 根据日志量选择合适的轮转策略
4. **备份数量**: 平衡存储空间和历史记录需求
5. **缓冲区大小**: 根据系统性能调整缓冲区大小
6. **异步模式**: 高性能场景建议启用异步模式

## 故障排除

### 常见问题

1. **配置验证失败**
   - 检查配置参数格式是否正确
   - 确保日志目录存在且可写
   - 验证日志级别和轮转参数

2. **日志文件未生成**
   - 确认日志处理器配置正确
   - 检查日志目录权限
   - 验证日志级别设置

3. **轮转不工作**
   - 检查轮转类型和参数
   - 确认文件大小或时间条件
   - 验证备份数量设置

### 调试方法
```python
# 获取详细配置信息
config_manager = ConfigManager()
logging_config = config_manager.get_logging_config()
print(f"完整配置: {logging_config}")

# 验证配置
is_valid = config_manager.validator.validate_logging_config(logging_config)
print(f"配置有效性: {is_valid}")

# 获取日志配置对象
log_config = config_manager.get_log_config()
print(f"日志级别: {log_config.get_level()}")
print(f"日志目录: {log_config.get_log_dir()}")
print(f"文件路径: {log_config.get_log_file_paths()}")
```

## 总结

新的日志配置管理功能提供了：

- ✅ 完整的日志配置管理
- ✅ 动态配置更新
- ✅ 配置验证功能
- ✅ 多种日志处理器
- ✅ 灵活的轮转策略
- ✅ 性能优化选项
- ✅ 易于使用的API

这些功能使得webmon项目的日志管理更加灵活和强大，满足不同场景下的日志需求。