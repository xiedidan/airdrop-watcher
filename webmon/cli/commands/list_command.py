"""
列出监控任务命令实现
"""

import json
from pathlib import Path
from argparse import Namespace
from typing import List, Dict

from webmon.cli.command import Command
from webmon.utils.logger import get_logger


class ListCommand(Command):
    """列出监控任务命令"""
    
    def __init__(self, args: Namespace):
        super().__init__(args)
        self.logger = get_logger(__name__)
    
    def execute(self) -> bool:
        """执行列出任务命令"""
        try:
            tasks = self._load_tasks()
            
            if not tasks:
                print("暂无监控任务")
                return True
            
            # 根据状态过滤
            if self.args.status != 'all':
                tasks = self._filter_by_status(tasks, self.args.status)
            
            if not tasks:
                print(f"没有找到{self.args.status}状态的任务")
                return True
            
            # 根据格式输出
            if self.args.format == 'table':
                self._output_table(tasks)
            elif self.args.format == 'json':
                self._output_json(tasks)
            elif self.args.format == 'csv':
                self._output_csv(tasks)
            
            return True
            
        except Exception as e:
            self.logger.error(f"列出任务失败: {e}")
            print(f"❌ 列出任务失败: {e}")
            return False
    
    def _load_tasks(self) -> List[Dict]:
        """加载任务配置"""
        config_file = Path('config/config.json')
        
        if not config_file.exists():
            return []
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            return config.get("tasks", [])
        except Exception as e:
            self.logger.error(f"加载任务配置失败: {e}")
            return []
    
    def _filter_by_status(self, tasks: List[Dict], status: str) -> List[Dict]:
        """按状态过滤任务"""
        if status == 'active':
            return [task for task in tasks if task.get('enabled', True)]
        elif status == 'inactive':
            return [task for task in tasks if not task.get('enabled', True)]
        return tasks
    
    def _output_table(self, tasks: List[Dict]):
        """以表格格式输出"""
        if not tasks:
            print("暂无任务")
            return

        # 计算列宽
        headers = ['ID', '名称', '描述', 'URL', '间隔', '状态', '启用']
        rows = []

        for task in tasks:
            task_id = task.get('id', '')[:8]
            name = task.get('name', '')
            description = self._truncate_text(task.get('description', '') or '', 20)
            url = self._truncate_url(task.get('url', ''))
            interval = f"{task.get('interval', 0)}秒"

            # 显示真实的 status 字段
            status = task.get('status', 'unknown') or 'unknown'
            enabled = "是" if task.get('enabled', True) else "否"

            rows.append([task_id, name, description, url, interval, status, enabled])
        
        # 使用tabulate输出表格
        try:
            from tabulate import tabulate
            print(tabulate(rows, headers=headers, tablefmt='grid'))
        except ImportError:
            # 如果没有tabulate，使用简单格式
            self._output_simple_table(headers, rows)
    
    def _output_simple_table(self, headers: List[str], rows: List[List[str]]):
        """使用简单格式输出表格"""
        # 计算列宽
        col_widths = []
        for i in range(len(headers)):
            width = max(len(headers[i]), max(len(row[i]) for row in rows)) if rows else len(headers[i])
            col_widths.append(width + 2)
        
        # 输出表头
        header_line = ""
        for i, header in enumerate(headers):
            header_line += f"{header:<{col_widths[i]}}"
        print(header_line)
        print("-" * len(header_line))
        
        # 输出行
        for row in rows:
            row_line = ""
            for i, cell in enumerate(row):
                row_line += f"{cell:<{col_widths[i]}}"
            print(row_line)
    
    def _output_json(self, tasks: List[Dict]):
        """以JSON格式输出"""
        print(json.dumps(tasks, indent=2, ensure_ascii=False))
    
    def _output_csv(self, tasks: List[Dict]):
        """以CSV格式输出"""
        import csv
        import io

        output = io.StringIO()
        writer = csv.writer(output)

        # 写入表头
        headers = ['ID', '名称', '描述', 'URL', '间隔(秒)', '选择器', '状态', '创建时间']
        writer.writerow(headers)

        # 写入数据
        for task in tasks:
            writer.writerow([
                task.get('id', ''),
                task.get('name', ''),
                task.get('description', ''),
                task.get('url', ''),
                task.get('interval', 0),
                task.get('selector', '') or '',
                '启用' if task.get('enabled', True) else '禁用',
                task.get('created_at', '')
            ])
        
        print(output.getvalue())
    
    def _truncate_url(self, url: str, max_length: int = 50) -> str:
        """截断URL显示"""
        if len(url) <= max_length:
            return url
        return url[:max_length-3] + "..."

    def _truncate_text(self, text: str, max_length: int = 20) -> str:
        """截断文本显示"""
        if not text:
            return "-"
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def validate_args(self) -> bool:
        """验证参数"""
        if self.args.format not in ['table', 'json', 'csv']:
            print(f"❌ 无效的输出格式: {self.args.format}")
            return False
        
        if self.args.status not in ['all', 'active', 'inactive']:
            print(f"❌ 无效的状态过滤: {self.args.status}")
            return False
        
        return True