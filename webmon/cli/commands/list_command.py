"""
列出监控任务命令实现
"""

import json
import unicodedata
from pathlib import Path
from argparse import Namespace
from typing import List, Dict, Optional

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

    def _load_default_ai_prompt(self) -> str:
        """加载全局默认AI提示词"""
        config_file = Path('config/config.json')

        if not config_file.exists():
            return ""

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            return config.get("ai", {}).get("user_prompt_template", "")
        except Exception:
            return ""

    def _filter_by_status(self, tasks: List[Dict], status: str) -> List[Dict]:
        """按状态过滤任务"""
        if status == 'active':
            return [task for task in tasks if task.get('enabled', True)]
        elif status == 'inactive':
            return [task for task in tasks if not task.get('enabled', True)]
        return tasks

    def _get_display_width(self, text: str) -> int:
        """
        计算字符串的显示宽度（考虑中文字符占2个宽度）

        Args:
            text: 要计算宽度的字符串

        Returns:
            显示宽度
        """
        width = 0
        for char in text:
            # 使用 unicodedata 判断字符宽度
            if unicodedata.east_asian_width(char) in ('F', 'W', 'A'):
                width += 2  # 全角字符
            else:
                width += 1  # 半角字符
        return width

    def _pad_to_width(self, text: str, target_width: int) -> str:
        """
        将字符串填充到指定显示宽度

        Args:
            text: 要填充的字符串
            target_width: 目标显示宽度

        Returns:
            填充后的字符串
        """
        current_width = self._get_display_width(text)
        padding = target_width - current_width
        if padding > 0:
            return text + ' ' * padding
        return text

    def _output_table(self, tasks: List[Dict]):
        """以表格格式输出"""
        if not tasks:
            print("暂无任务")
            return

        # 计算列宽
        headers = ['ID', '名称', '描述', 'URL', '选择器', '间隔', '状态', '启用']
        rows = []

        for task in tasks:
            task_id = task.get('id', '')[:8]
            name = task.get('name', '')
            description = self._truncate_text(task.get('description', '') or '', 15)
            url = self._truncate_url(task.get('url', ''), 35)

            # 获取选择器列表
            selectors = task.get('selectors', [])
            if selectors:
                selector_str = ', '.join(selectors)
                selector_str = self._truncate_text(selector_str, 25)
            else:
                selector_str = '-'

            interval = f"{task.get('interval', 0)}秒"

            # 显示真实的 status 字段
            status = task.get('status', 'unknown') or 'unknown'
            enabled = "是" if task.get('enabled', True) else "否"

            rows.append([task_id, name, description, url, selector_str, interval, status, enabled])

        # 使用tabulate输出表格
        try:
            from tabulate import tabulate
            print(tabulate(rows, headers=headers, tablefmt='grid'))
        except ImportError:
            # 如果没有tabulate，使用简单格式
            self._output_simple_table(headers, rows)

        # 输出 AI 提示词信息
        self._output_ai_prompts(tasks)

    def _output_simple_table(self, headers: List[str], rows: List[List[str]]):
        """使用简单格式输出表格（支持中文对齐）"""
        # 计算每列的最大显示宽度
        col_widths = []
        for i in range(len(headers)):
            header_width = self._get_display_width(headers[i])
            max_row_width = max(self._get_display_width(row[i]) for row in rows) if rows else 0
            col_widths.append(max(header_width, max_row_width) + 2)

        # 输出表头
        header_parts = []
        for i, header in enumerate(headers):
            header_parts.append(self._pad_to_width(header, col_widths[i]))
        print(''.join(header_parts))

        # 输出分隔线
        separator_parts = []
        for width in col_widths:
            separator_parts.append('-' * width)
        print(''.join(separator_parts))

        # 输出行
        for row in rows:
            row_parts = []
            for i, cell in enumerate(row):
                row_parts.append(self._pad_to_width(cell, col_widths[i]))
            print(''.join(row_parts))

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

    def _output_ai_prompts(self, tasks: List[Dict]):
        """输出 AI 提示词信息"""
        default_prompt = self._load_default_ai_prompt()

        print("\n📝 AI提示词配置:")
        print("-" * 60)

        # 先显示全局默认提示词
        if default_prompt:
            # 将换行符替换为可见形式，并截断显示
            display_prompt = default_prompt.replace('\n', '\\n')
            if len(display_prompt) > 80:
                display_prompt = display_prompt[:77] + "..."
            print(f"[全局默认] {display_prompt}")
        else:
            print("[全局默认] (未配置)")

        print("-" * 60)

        # 显示每个任务的提示词配置
        for task in tasks:
            task_id = task.get('id', '')[:8]
            name = task.get('name', '')
            ai_prompt = task.get('ai_prompt', '')

            if ai_prompt and ai_prompt.strip():
                # 有自定义提示词
                display_prompt = ai_prompt.replace('\n', '\\n')
                if len(display_prompt) > 60:
                    display_prompt = display_prompt[:57] + "..."
                print(f"[{task_id}] {name}: {display_prompt}")
            else:
                # 使用默认提示词
                print(f"[{task_id}] {name}: (使用全局默认)")

    def validate_args(self) -> bool:
        """验证参数"""
        if self.args.format not in ['table', 'json', 'csv']:
            print(f"❌ 无效的输出格式: {self.args.format}")
            return False

        if self.args.status not in ['all', 'active', 'inactive']:
            print(f"❌ 无效的状态过滤: {self.args.status}")
            return False

        return True