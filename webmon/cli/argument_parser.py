"""
参数解析器模块
负责解析命令行参数并提供帮助信息
"""

import argparse
import sys
import os
from typing import Optional
from dotenv import load_dotenv


class ArgumentParser:
    """
    参数解析器类，封装argparse功能
    """

    def __init__(self):
        """初始化参数解析器"""
        # 加载环境变量
        load_dotenv()

        # 从环境变量获取默认值（单位：秒）
        self.default_interval = int(os.getenv('DEFAULT_INTERVAL', '300'))  # 秒
        self.default_timeout = int(os.getenv('DEFAULT_TIMEOUT', '30000')) // 1000  # 转换为秒

        self.parser = argparse.ArgumentParser(
            prog='webmon',
            description='WebMon - 基于Playwright的网页监控工具',
            epilog='使用 "webmon <command> -h" 查看具体命令的帮助信息',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        # 添加全局选项
        self._add_global_options()
        
        # 添加子命令
        self.subparsers = self.parser.add_subparsers(
            dest='command',
            title='可用命令',
            description='WebMon支持以下命令：',
            help='命令详情'
        )
        
        # 添加各个子命令
        self._add_init_command()
        self._add_add_command()
        self._add_edit_command()
        self._add_remove_command()
        self._add_list_command()
        self._add_start_command()
        self._add_stop_command()
        self._add_status_command()
        self._add_test_command()
        self._add_history_command()
        self._add_config_command()
    
    def _add_global_options(self):
        """添加全局选项"""
        self.parser.add_argument(
            '--version', 
            action='version', 
            version='%(prog)s 1.0.0'
        )
        
        self.parser.add_argument(
            '--config', 
            '-c',
            type=str,
            default='config/config.json',
            help='配置文件路径 (默认: config/config.json)'
        )
        
        self.parser.add_argument(
            '--env', 
            '-e',
            type=str,
            default='.env',
            help='环境变量文件路径 (默认: .env)'
        )
        
        self.parser.add_argument(
            '--verbose', 
            '-v',
            action='store_true',
            help='显示详细输出'
        )
        
        self.parser.add_argument(
            '--quiet', 
            '-q',
            action='store_true',
            help='静默模式，只显示错误信息'
        )
    
    def _add_init_command(self):
        """添加init命令"""
        parser_init = self.subparsers.add_parser(
            'init',
            help='初始化配置文件和.env文件',
            description='创建默认的配置文件和目录结构'
        )
        
        parser_init.add_argument(
            '--force',
            '-f',
            action='store_true',
            help='强制覆盖已存在的配置文件'
        )
    
    def _add_add_command(self):
        """添加add命令"""
        parser_add = self.subparsers.add_parser(
            'add',
            help='添加监控任务',
            description='添加一个新的网页监控任务'
        )

        parser_add.add_argument(
            'url',
            type=str,
            help='要监控的网页URL'
        )

        parser_add.add_argument(
            '--name',
            '-n',
            type=str,
            help='任务名称 (可选，默认为URL的简化名称)'
        )

        parser_add.add_argument(
            '--description',
            '-d',
            type=str,
            default='',
            help='任务描述，用于AI分析时的上下文 (可选)'
        )

        parser_add.add_argument(
            '--selector',
            '-s',
            type=str,
            help='CSS选择器，用于指定监控的页面元素 (可选)'
        )

        parser_add.add_argument(
            '--interval',
            '-i',
            type=int,
            default=self.default_interval,
            help=f'检测间隔时间 (秒，默认: {self.default_interval})'
        )

        parser_add.add_argument(
            '--timeout',
            '-t',
            type=int,
            default=self.default_timeout,
            help=f'页面加载超时时间 (秒，默认: {self.default_timeout})'
        )

        parser_add.add_argument(
            '--ai-prompt',
            type=str,
            default='',
            help='自定义AI分析提示词，为空则使用全局默认提示词 (可选)'
        )

    def _add_edit_command(self):
        """添加edit命令"""
        parser_edit = self.subparsers.add_parser(
            'edit',
            help='编辑监控任务',
            description='修改已存在的监控任务配置'
        )

        parser_edit.add_argument(
            'task_id',
            type=str,
            help='要编辑的任务ID或名称'
        )

        parser_edit.add_argument(
            '--name',
            '-n',
            type=str,
            help='修改任务名称'
        )

        parser_edit.add_argument(
            '--description',
            '-d',
            type=str,
            help='修改任务描述'
        )

        parser_edit.add_argument(
            '--url',
            '-u',
            type=str,
            help='修改监控URL'
        )

        parser_edit.add_argument(
            '--interval',
            '-i',
            type=int,
            help='修改检测间隔时间 (秒)'
        )

        parser_edit.add_argument(
            '--timeout',
            '-t',
            type=int,
            help='修改页面加载超时时间 (秒)'
        )

        parser_edit.add_argument(
            '--selector',
            '-s',
            type=str,
            help='修改CSS选择器 (使用空字符串清除)'
        )

        parser_edit.add_argument(
            '--enable',
            type=lambda x: x.lower() in ['true', 'yes', '1', 'on'],
            help='启用/禁用任务 (true/false)'
        )

        parser_edit.add_argument(
            '--ai-prompt',
            type=str,
            help='修改AI分析提示词 (使用空字符串清除，恢复使用全局默认)'
        )

        parser_edit.add_argument(
            '--force',
            '-f',
            action='store_true',
            help='跳过确认提示'
        )

    def _add_remove_command(self):
        """添加remove命令"""
        parser_remove = self.subparsers.add_parser(
            'remove',
            help='删除监控任务',
            description='删除指定的网页监控任务'
        )
        
        parser_remove.add_argument(
            'task_id',
            type=str,
            help='要删除的任务ID或名称'
        )
        
        parser_remove.add_argument(
            '--force',
            '-f',
            action='store_true',
            help='强制删除，不提示确认'
        )
    
    def _add_list_command(self):
        """添加list命令"""
        parser_list = self.subparsers.add_parser(
            'list',
            help='列出所有监控任务',
            description='显示当前配置的所有监控任务'
        )
        
        parser_list.add_argument(
            '--format', 
            '-f',
            choices=['table', 'json', 'csv'],
            default='table',
            help='输出格式 (默认: table)'
        )
        
        parser_list.add_argument(
            '--status',
            choices=['all', 'active', 'inactive'],
            default='all',
            help='过滤任务状态 (默认: all)'
        )
    
    def _add_start_command(self):
        """添加start命令"""
        parser_start = self.subparsers.add_parser(
            'start',
            help='启动监控服务',
            description='启动网页监控服务，开始监控所有任务'
        )
        
        parser_start.add_argument(
            '--daemon', 
            '-d',
            action='store_true',
            help='以守护进程模式运行'
        )
        
        parser_start.add_argument(
            '--task',
            type=str,
            help='只监控指定的任务ID或名称'
        )
    
    def _add_stop_command(self):
        """添加stop命令"""
        parser_stop = self.subparsers.add_parser(
            'stop',
            help='停止监控服务',
            description='停止正在运行的网页监控服务'
        )
        
        parser_stop.add_argument(
            '--force',
            '-f',
            action='store_true',
            help='强制停止服务'
        )
        
        parser_stop.add_argument(
            '--timeout',
            '-t',
            type=int,
            default=30,
            help='优雅停止超时时间 (秒，默认: 30)'
        )
    
    def _add_status_command(self):
        """添加status命令"""
        parser_status = self.subparsers.add_parser(
            'status',
            help='查看监控状态',
            description='显示监控服务的当前状态'
        )
        
        parser_status.add_argument(
            '--json',
            action='store_true',
            help='以JSON格式输出状态信息'
        )
    
    def _add_test_command(self):
        """添加test命令"""
        parser_test = self.subparsers.add_parser(
            'test',
            help='测试推送通知',
            description='测试配置的推送平台是否能正常工作'
        )
        
        parser_test.add_argument(
            '--platform',
            choices=['pushplus', 'telegram', 'discord', 'feishu', 'all'],
            default='all',
            help='测试指定的推送平台 (默认: all)'
        )
        
        parser_test.add_argument(
            '--message',
            '-m',
            type=str,
            default='WebMon测试消息',
            help='测试消息内容 (默认: "WebMon测试消息")'
        )
    
    def _add_history_command(self):
        """添加history命令"""
        parser_history = self.subparsers.add_parser(
            'history',
            help='查看变化历史',
            description='查看网页变化检测的历史记录'
        )

        parser_history.add_argument(
            'task_id',
            nargs='?',
            type=str,
            help='查看指定任务的历史记录'
        )

        parser_history.add_argument(
            '--all', '-a',
            action='store_true',
            dest='show_all',
            help='显示所有记录（默认只显示有变化的记录）'
        )

        parser_history.add_argument(
            '--limit',
            '-l',
            type=int,
            default=10,
            help='显示最近N条记录 (默认: 10)'
        )

        parser_history.add_argument(
            '--format',
            '-f',
            choices=['table', 'json'],
            default='table',
            help='输出格式 (默认: table)'
        )

    def _add_config_command(self):
        """添加config命令"""
        parser_config = self.subparsers.add_parser(
            'config',
            help='配置管理',
            description='查看和修改WebMon配置'
        )

        # 添加config子命令
        config_subparsers = parser_config.add_subparsers(
            dest='config_subcommand',
            title='配置子命令',
            help='配置操作'
        )

        # config show 子命令
        config_subparsers.add_parser(
            'show',
            help='显示所有配置'
        )

        # config ai 子命令
        parser_ai = config_subparsers.add_parser(
            'ai',
            help='AI分析配置'
        )

        # AI子命令
        ai_subparsers = parser_ai.add_subparsers(
            dest='ai_action',
            title='AI操作',
            help='AI配置操作'
        )

        # ai enable
        ai_subparsers.add_parser(
            'enable',
            help='启用AI分析'
        )

        # ai disable
        ai_subparsers.add_parser(
            'disable',
            help='禁用AI分析'
        )

        # ai test
        ai_subparsers.add_parser(
            'test',
            help='测试AI连接'
        )

        # ai set
        parser_ai_set = ai_subparsers.add_parser(
            'set',
            help='设置AI配置项'
        )

        parser_ai_set.add_argument(
            '--api-url',
            dest='api_url',
            type=str,
            help='API地址 (如: https://api.deepseek.com/v1)'
        )

        parser_ai_set.add_argument(
            '--api-key',
            dest='api_key',
            type=str,
            help='API Key'
        )

        parser_ai_set.add_argument(
            '--model',
            type=str,
            help='模型名称 (如: deepseek-reasoner, gpt-4)'
        )

        parser_ai_set.add_argument(
            '--max-tokens',
            dest='max_tokens',
            type=int,
            help='最大Token数'
        )

        parser_ai_set.add_argument(
            '--temperature',
            type=float,
            help='温度参数 (0.0-2.0)'
        )

        parser_ai_set.add_argument(
            '--timeout',
            type=int,
            help='超时时间 (秒)'
        )
    
    def parse_args(self, args: Optional[list] = None):
        """
        解析命令行参数
        
        Args:
            args: 命令行参数列表，如果为None则使用sys.argv
        
        Returns:
            解析后的参数对象
        """
        if args is None:
            args = sys.argv[1:]
        
        # 如果没有提供参数，显示帮助
        if not args:
            self.parser.print_help()
            sys.exit(0)
        
        parsed_args = self.parser.parse_args(args)
        
        # 验证命令
        if not parsed_args.command:
            self.parser.print_help()
            sys.exit(1)
        
        return parsed_args
    
    def print_help(self):
        """打印帮助信息"""
        self.parser.print_help()