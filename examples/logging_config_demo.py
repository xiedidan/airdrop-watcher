#!/usr/bin/env python3
"""
日志配置管理演示
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from webmon.config.config_manager import ConfigManager


def main():
    """主函数演示"""
    print("🚀 日志配置管理演示")
    print("=" * 40)
    
    # 创建配置管理器
    config_manager = ConfigManager()
    
    # 显示当前配置
    print("📋 当前日志配置:")
    logging_config = config_manager.get_logging_config()
    print(f"  级别: {logging_config['level']}")
    print(f"  目录: {logging_config['log_dir']}")
    print(f"  轮转类型: {logging_config['rotation']['type']}")
    print(f"  处理器: {', '.join(logging_config['handlers'])}")
    
    # 修改配置示例
    print("\n🔧 修改配置示例:")
    
    # 1. 设置日志级别为DEBUG
    config_manager.set_log_level("DEBUG")
    print("  ✅ 设置日志级别为DEBUG")
    
    # 2. 设置日志目录
    config_manager.set_log_directory("./demo_logs")
    print("  ✅ 设置日志目录为./demo_logs")
    
    # 3. 配置日志轮转
    config_manager.configure_log_rotation("size", max_size=5*1024*1024, backup_count=3)
    print("  ✅ 配置大小轮转(5MB, 3个备份)")
    
    # 4. 获取日志文件路径
    log_paths = config_manager.get_log_file_paths()
    print(f"  📁 日志文件路径:")
    for name, path in log_paths.items():
        print(f"    {name}: {path}")
    
    # 5. 估计日志大小
    size_info = config_manager.estimate_log_size(tasks_per_day=50, avg_log_size=150)
    print(f"  📊 日志大小估计:")
    print(f"    每日日志量: {size_info['daily_logs_bytes']} 字节")
    print(f"    预计保留天数: {size_info['estimated_retention_days']}")
    
    # 6. 验证配置
    is_valid = config_manager.validate_config()
    print(f"  ✅ 配置验证: {'通过' if is_valid else '失败'}")
    
    print("\n🎉 演示完成！")
    print("💡 查看生成的配置文件了解更改")


if __name__ == "__main__":
    main()