#!/usr/bin/env python3
"""
WebMon - 网页监控工具
基于Playwright的轻量级网页内容变化检测和通知推送工具
"""

import sys
import os
from pathlib import Path

# 添加webmon模块路径到Python路径
sys.path.insert(0, str(Path(__file__).parent / 'webmon'))

from dotenv import load_dotenv
from webmon.cli.argument_parser import ArgumentParser
from webmon.cli.command_factory import CommandFactory
from webmon.utils.logger import setup_global_logger, get_logger


def main():
    """主程序入口"""
    # 先加载环境变量，再设置日志
    load_dotenv()
    setup_global_logger()
    logger = get_logger(__name__)
    
    try:
        # 解析命令行参数
        parser = ArgumentParser()
        args = parser.parse_args()
        
        # 创建并执行命令
        command_factory = CommandFactory()
        command = command_factory.create_command(args.command, args)
        
        # 执行命令
        result = command.execute()
        
        # 根据执行结果退出
        sys.exit(0 if result else 1)
        
    except KeyboardInterrupt:
        logger.info("用户中断操作")
        sys.exit(130)
    except Exception as e:
        logger.error(f"程序执行错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()