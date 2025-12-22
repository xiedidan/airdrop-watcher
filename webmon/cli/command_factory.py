"""
命令工厂类
用于创建和管理各种命令实例
"""

from typing import Dict, Type, Optional
from argparse import Namespace

from webmon.cli.commands.init_command import InitCommand
from webmon.cli.commands.add_command import AddCommand
from webmon.cli.commands.edit_command import EditCommand
from webmon.cli.commands.list_command import ListCommand
from webmon.cli.commands.remove_command import RemoveCommand
from webmon.cli.commands.start_command import StartCommand
from webmon.cli.commands.stop_command import StopCommand
from webmon.cli.commands.status_command import StatusCommand
from webmon.cli.commands.history_command import HistoryCommand
from webmon.cli.commands.test_command import TestCommand
from webmon.cli.commands.config_command import ConfigCommand
from webmon.cli.commands.web_command import WebCommand
from webmon.cli.command import Command


class CommandFactory:
    """
    命令工厂类，负责创建各种命令实例
    """
    
    def __init__(self):
        """初始化命令工厂"""
        self._commands: Dict[str, Type[Command]] = {
            'init': InitCommand,
            'add': AddCommand,
            'edit': EditCommand,
            'list': ListCommand,
            'remove': RemoveCommand,
            'start': StartCommand,
            'stop': StopCommand,
            'status': StatusCommand,
            'history': HistoryCommand,
            'test': TestCommand,
            'config': ConfigCommand,
            'web': WebCommand,
        }
    
    def create_command(self, command_name: str, args: Namespace) -> Optional[Command]:
        """
        创建命令实例
        
        Args:
            command_name: 命令名称
            args: 命令行参数
        
        Returns:
            Command: 命令实例，如果命令不存在返回None
        """
        command_class = self._commands.get(command_name.lower())
        if command_class:
            return command_class(args)
        return None
    
    def get_available_commands(self) -> list:
        """
        获取所有可用的命令名称
        
        Returns:
            list: 命令名称列表
        """
        return list(self._commands.keys())
    
    def register_command(self, name: str, command_class: Type[Command]) -> None:
        """
        注册新的命令类型
        
        Args:
            name: 命令名称
            command_class: 命令类
        """
        self._commands[name.lower()] = command_class
    
    def unregister_command(self, name: str) -> None:
        """
        注销命令类型
        
        Args:
            name: 命令名称
        """
        if name.lower() in self._commands:
            del self._commands[name.lower()]