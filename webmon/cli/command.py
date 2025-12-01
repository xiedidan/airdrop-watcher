"""
命令基类和命令接口定义
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from argparse import Namespace


class Command(ABC):
    """
    命令基类，所有具体命令都需要继承此类
    """
    
    def __init__(self, args: Namespace):
        """
        初始化命令
        
        Args:
            args: 命令行参数
        """
        self.args = args
        self.name = self.__class__.__name__.lower().replace('command', '')
    
    @abstractmethod
    def execute(self) -> bool:
        """
        执行命令
        
        Returns:
            bool: 命令执行成功返回True，失败返回False
        """
        pass
    
    def validate_args(self) -> bool:
        """
        验证命令参数
        
        Returns:
            bool: 参数验证通过返回True，失败返回False
        """
        return True
    
    def get_help(self) -> str:
        """
        获取命令帮助信息
        
        Returns:
            str: 帮助信息
        """
        return f"Help for {self.name} command"


class InitCommand(Command):
    """初始化命令"""
    
    def execute(self) -> bool:
        print("执行初始化命令...")
        return True


class AddCommand(Command):
    """添加监控任务命令"""
    
    def execute(self) -> bool:
        print("执行添加任务命令...")
        return True


class RemoveCommand(Command):
    """删除监控任务命令"""
    
    def execute(self) -> bool:
        print("执行删除任务命令...")
        return True


class ListCommand(Command):
    """列出监控任务命令"""
    
    def execute(self) -> bool:
        print("执行列出任务命令...")
        return True


class StartCommand(Command):
    """启动监控服务命令"""
    
    def execute(self) -> bool:
        print("执行启动服务命令...")
        return True


class StopCommand(Command):
    """停止监控服务命令"""
    
    def execute(self) -> bool:
        print("执行停止服务命令...")
        return True


class StatusCommand(Command):
    """查看监控状态命令"""
    
    def execute(self) -> bool:
        print("执行查看状态命令...")
        return True


class TestCommand(Command):
    """测试推送通知命令"""
    
    def execute(self) -> bool:
        print("执行测试推送命令...")
        return True


class HistoryCommand(Command):
    """查看历史记录命令"""
    
    def execute(self) -> bool:
        print("执行查看历史命令...")
        return True