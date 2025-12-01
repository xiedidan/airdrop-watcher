#!/usr/bin/env python3
"""
删除监控任务命令
"""

import sys
from typing import Optional
from webmon.cli.command import Command
from webmon.utils.logger import get_logger
from webmon.storage.task_storage import TaskStorage
from webmon.utils.validators import validate_task_id


class RemoveCommand(Command):
    """删除监控任务命令"""
    
    def __init__(self, app=None):
        super().__init__(app)
        self.logger = get_logger(__name__)
        # 获取配置路径，默认为config/config.json
        config_path = getattr(self.args, 'config', 'config/config.json') if hasattr(self, 'args') else 'config/config.json'
        self.storage = TaskStorage(config_path)
    
    def execute(self) -> bool:
        """执行删除任务命令"""
        try:
            task_identifier = self.args.task_id
            force = getattr(self.args, 'force', False)
            
            self.logger.info(f"执行删除任务命令，任务标识: {task_identifier}")
            
            # 查找任务
            task = self._find_task(task_identifier)
            if not task:
                self.logger.error(f"未找到任务: {task_identifier}")
                print(f"❌ 错误: 未找到任务 '{task_identifier}'")
                return False
            
            # 确认删除（非强制模式）
            if not force:
                if not self._confirm_delete(task):
                    print("❌ 操作已取消")
                    return False
            
            # 执行删除
            success = self.storage.remove_task(task.id)
            if success:
                self.logger.info(f"成功删除任务: {task.name} (ID: {task.id})")
                print(f"✅ 成功删除任务: {task.name} (ID: {task.id})")
                return True
            else:
                self.logger.error(f"删除任务失败: {task.name} (ID: {task.id})")
                print(f"❌ 删除任务失败: {task.name} (ID: {task.id})")
                return False
                
        except Exception as e:
            self.logger.error(f"删除任务时发生错误: {e}")
            print(f"❌ 删除任务时发生错误: {e}")
            return False
    
    def _find_task(self, identifier: str) -> Optional[object]:
        """查找任务（支持ID和名称）"""
        # 首先尝试作为ID查找
        if validate_task_id(identifier):
            task = self.storage.get_task(identifier)
            if task:
                return task
        
        # 尝试作为名称查找
        tasks = self.storage.list_tasks()
        for task in tasks:
            if task.name == identifier:
                return task
        
        return None
    
    def _confirm_delete(self, task) -> bool:
        """确认删除操作"""
        print(f"\n🗑️  即将删除任务:")
        print(f"   名称: {task.name}")
        print(f"   URL: {task.url}")
        print(f"   ID: {task.id}")
        print(f"   创建时间: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 显示相关历史记录数量
        from webmon.storage.history_storage import HistoryStorage
        history_storage = HistoryStorage()
        check_count = len(history_storage.list_check_results(task_id=task.id, limit=1000))
        change_count = len(history_storage.list_change_details(task_id=task.id, limit=1000))
        
        if check_count > 0:
            print(f"   检测记录: {check_count} 条")
        if change_count > 0:
            print(f"   变化记录: {change_count} 条")
        
        try:
            response = input(f"\n❓ 确定要删除此任务吗? [y/N]: ").strip().lower()
            return response in ['y', 'yes']
        except (KeyboardInterrupt, EOFError):
            print()  # 换行
            return False
    
    def validate_args(self, args) -> bool:
        """验证参数"""
        if not args.task_id:
            self.logger.error("缺少任务ID或名称参数")
            print("❌ 错误: 请指定要删除的任务ID或名称")
            return False
        
        return True
    
    def format_output(self, result: bool, format_type: str = 'text') -> str:
        """格式化输出"""
        if format_type == 'json':
            import json
            return json.dumps({
                "success": result,
                "message": "任务删除成功" if result else "任务删除失败"
            }, ensure_ascii=False, indent=2)
        else:
            # 文本格式在execute方法中已经处理
            return ""