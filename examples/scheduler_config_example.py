#!/usr/bin/env python3
"""
调度器配置使用示例

这个示例展示了如何使用 ConfigManager 来管理调度器配置，包括：
1. 获取和更新调度器配置
2. 使用配置验证功能
3. 动态更新调度器配置
4. 获取性能优化建议
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from webmon.config import ConfigManager
from webmon.scheduler.scheduler_config import SchedulerConfig
from webmon.scheduler.task_scheduler import TaskScheduler


def demonstrate_basic_usage():
    """演示基本用法"""
    print("=== 调度器配置基本用法演示 ===")
    
    # 创建配置管理器
    config_manager = ConfigManager()
    
    # 获取调度器配置
    scheduler_config = config_manager.get_scheduler_config()
    print(f"当前调度器配置包含 {len(scheduler_config)} 个主要配置块")
    
    # 获取特定的配置值
    max_tasks = config_manager.get_scheduler_config_value('performance.max_concurrent_tasks')
    retry_attempts = config_manager.get_scheduler_config_value('retry.retry_attempts')
    print(f"最大并发任务数: {max_tasks}, 重试次数: {retry_attempts}")
    
    # 获取不存在的配置值（返回默认值）
    non_existent = config_manager.get_scheduler_config_value('non_existent.key', 'default_value')
    print(f"不存在的配置值: {non_existent}")


def demonstrate_config_validation():
    """演示配置验证功能"""
    print("\n=== 配置验证功能演示 ===")
    
    config_manager = ConfigManager()
    
    # 有效的配置
    valid_config = {
        "performance": {
            "max_concurrent_tasks": 8,
            "max_browser_resources": 4,
            "scheduler_loop_interval": 0.1
        },
        "retry": {
            "retry_attempts": 3,
            "retry_delay": 60
        }
    }
    
    is_valid = config_manager.validator.validate_scheduler_config(valid_config)
    print(f"有效配置验证: {'✅ 通过' if is_valid else '❌ 失败'}")
    
    # 无效的配置
    invalid_config = {
        "performance": {
            "max_concurrent_tasks": -1,  # 无效：负数
            "scheduler_loop_interval": 0  # 无效：零值
        }
    }
    
    is_valid = config_manager.validator.validate_scheduler_config(invalid_config)
    print(f"无效配置验证: {'❌ 失败' if not is_valid else '✅ 通过'}")


def demonstrate_config_update():
    """演示配置更新功能"""
    print("\n=== 配置更新功能演示 ===")
    
    config_manager = ConfigManager()
    
    # 显示更新前的配置
    old_interval = config_manager.get_scheduler_config_value('performance.scheduler_loop_interval')
    print(f"更新前的调度循环间隔: {old_interval}秒")
    
    # 更新配置
    new_config = {
        "performance": {
            "scheduler_loop_interval": 0.5,  # 减慢调度循环
            "job_batch_size": 5  # 减小批处理大小
        },
        "monitoring": {
            "stats_update_interval": 120  # 降低统计更新频率
        }
    }
    
    success = config_manager.update_scheduler_config(new_config)
    print(f"配置更新: {'✅ 成功' if success else '❌ 失败'}")
    
    # 显示更新后的配置
    new_interval = config_manager.get_scheduler_config_value('performance.scheduler_loop_interval')
    print(f"更新后的调度循环间隔: {new_interval}秒")


def demonstrate_scheduler_integration():
    """演示与任务调度器的集成"""
    print("\n=== 任务调度器集成演示 ===")
    
    # 创建配置管理器和任务调度器
    config_manager = ConfigManager()
    scheduler = TaskScheduler(config_manager)
    
    print(f"调度器初始化完成")
    
    # 获取当前配置
    current_config = scheduler.get_scheduler_config()
    print(f"当前最大并发任务数: {current_config['max_concurrent_tasks']}")
    print(f"当前重试次数: {current_config['retry_attempts']}")
    
    # 动态更新配置
    print("\n动态更新调度器配置...")
    new_settings = {
        "performance": {
            "max_concurrent_tasks": 12,
            "job_batch_size": 8
        },
        "retry": {
            "retry_attempts": 4
        }
    }
    
    success = scheduler.update_scheduler_config(new_settings)
    print(f"动态更新: {'✅ 成功' if success else '❌ 失败'}")
    
    # 验证更新后的配置
    updated_config = scheduler.get_scheduler_config()
    print(f"更新后的最大并发任务数: {updated_config['max_concurrent_tasks']}")
    print(f"更新后的重试次数: {updated_config['retry_attempts']}")


def demonstrate_performance_optimization():
    """演示性能优化建议功能"""
    print("\n=== 性能优化建议演示 ===")
    
    config_manager = ConfigManager()
    scheduler_config = SchedulerConfig.from_config_manager(config_manager)
    
    # 获取性能优化建议
    recommendations = scheduler_config.get_performance_recommendations()
    
    if recommendations:
        print("性能优化建议:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
    else:
        print("✅ 当前配置没有明显的性能问题")
    
    # 验证性能配置
    validation_result = scheduler_config.validate_performance()
    print(f"\n性能配置验证:")
    print(f"  有效性: {'✅ 有效' if validation_result['valid'] else '❌ 无效'}")
    if validation_result['issues']:
        print("  问题:")
        for issue in validation_result['issues']:
            print(f"    - {issue}")
    if validation_result['warnings']:
        print("  警告:")
        for warning in validation_result['warnings']:
            print(f"    - {warning}")
    print(f"  估计内存使用: {validation_result['estimated_memory_mb']}MB")
    print(f"  总超时时间: {validation_result['total_timeout_seconds']:.0f}秒")


def demonstrate_best_practices():
    """演示最佳实践"""
    print("\n=== 配置最佳实践演示 ===")
    
    config_manager = ConfigManager()
    
    # 推荐的生产环境配置
    production_config = {
        "performance": {
            "max_concurrent_tasks": 8,  # 适中的并发数
            "max_browser_resources": 4,  # 根据服务器资源调整
            "max_browser_concurrent": 2,  # 避免浏览器过载
            "scheduler_loop_interval": 0.1,  # 保持响应性
            "job_batch_size": 5  # 适中的批处理大小
        },
        "timeouts": {
            "default_timeout": 20000,  # 20秒超时
            "max_execution_time": 180,  # 3分钟最大执行时间
            "resource_acquisition_timeout": 20  # 20秒资源获取超时
        },
        "retry": {
            "retry_attempts": 2,  # 较少的重试次数
            "retry_delay": 120,  # 较长的重试延迟
            "retry_backoff_factor": 2.0  # 指数退避
        },
        "monitoring": {
            "enable_performance_monitoring": True,  # 启用性能监控
            "enable_resource_monitoring": True,  # 启用资源监控
            "stats_update_interval": 60  # 每分钟更新统计
        },
        "priority": {
            "enable_priority_scheduling": True,  # 启用智能优先级调度
            "priority_weights": {
                "age_factor": 1.0,
                "change_frequency_factor": 2.0,
                "error_penalty_factor": 3.0,  # 降低错误惩罚
                "success_bonus_factor": -0.5  # 降低成功奖励
            }
        },
        "error_handling": {
            "max_consecutive_errors": 3,  # 较低的连续错误阈值
            "error_cooldown_period": 600,  # 10分钟冷却期
            "circuit_breaker_threshold": 5,  # 较低的熔断阈值
            "circuit_breaker_timeout": 1800  # 30分钟熔断超时
        },
        "logging": {
            "log_level": "INFO",  # 适当的日志级别
            "log_execution_details": True,  # 记录执行详情
            "log_performance_metrics": True  # 记录性能指标
        }
    }
    
    print("生产环境推荐配置:")
    print(f"  最大并发任务数: {production_config['performance']['max_concurrent_tasks']}")
    print(f"  最大浏览器资源数: {production_config['performance']['max_browser_resources']}")
    print(f"  重试次数: {production_config['retry']['retry_attempts']}")
    print(f"  错误冷却期: {production_config['error_handling']['error_cooldown_period']}秒")
    
    # 验证推荐配置
    is_valid = config_manager.validator.validate_scheduler_config(production_config)
    print(f"推荐配置验证: {'✅ 有效' if is_valid else '❌ 无效'}")
    
    if is_valid:
        # 测试性能
        temp_config = SchedulerConfig.from_dict(production_config)
        validation = temp_config.validate_performance()
        if validation['valid'] and not validation['warnings']:
            print("✅ 推荐配置通过性能和资源使用验证")
        else:
            print("⚠️  推荐配置存在性能或资源使用问题")


def main():
    """主函数 - 运行所有演示"""
    print("调度器配置管理功能演示")
    print("=" * 50)
    
    try:
        demonstrate_basic_usage()
        demonstrate_config_validation()
        demonstrate_config_update()
        demonstrate_scheduler_integration()
        demonstrate_performance_optimization()
        demonstrate_best_practices()
        
        print("\n" + "=" * 50)
        print("✅ 所有演示完成！")
        print("\n总结:")
        print("- ConfigManager 现在支持完整的调度器配置管理")
        print("- 提供了配置验证功能确保配置有效性")
        print("- 支持动态更新调度器配置")
        print("- 集成了性能优化建议和验证功能")
        print("- 向后兼容旧的配置格式")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ 演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())