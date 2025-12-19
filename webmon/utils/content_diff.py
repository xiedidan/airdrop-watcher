"""
内容差异对比工具

提供内容差异计算和格式化功能。
"""

import difflib
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime


class ContentDiff:
    """内容差异对比类"""

    def __init__(self, max_diff_lines: int = 50, context_lines: int = 3):
        """
        初始化内容差异对比器

        Args:
            max_diff_lines: 最大差异行数（超过则截断）
            context_lines: 上下文行数
        """
        self.max_diff_lines = max_diff_lines
        self.context_lines = context_lines

    def compute_diff(self, old_content: str, new_content: str) -> Dict[str, Any]:
        """
        计算两个内容之间的差异

        Args:
            old_content: 旧内容
            new_content: 新内容

        Returns:
            差异信息字典，包含:
            - unified_diff: 统一差异格式文本
            - added_lines: 新增行数
            - removed_lines: 删除行数
            - modified_lines: 修改行数
            - changes_summary: 变化摘要
            - change_details: 变化详情列表
        """
        # 分割为行
        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)

        # 生成统一差异格式
        unified_diff = list(difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile='旧版本',
            tofile='新版本',
            n=self.context_lines
        ))

        # 限制差异行数
        if len(unified_diff) > self.max_diff_lines:
            unified_diff = unified_diff[:self.max_diff_lines]
            unified_diff.append(f"\n... (差异过长，已截断至 {self.max_diff_lines} 行)\n")

        # 统计变化
        added_lines = 0
        removed_lines = 0
        modified_lines = 0
        change_details = []

        for line in unified_diff[2:]:  # 跳过文件名行
            if line.startswith('+') and not line.startswith('+++'):
                added_lines += 1
                change_details.append({
                    'type': 'add',
                    'content': line[1:].strip()
                })
            elif line.startswith('-') and not line.startswith('---'):
                removed_lines += 1
                change_details.append({
                    'type': 'remove',
                    'content': line[1:].strip()
                })

        # 修改行 = min(新增, 删除)，其余为纯新增或纯删除
        modified_lines = min(added_lines, removed_lines)

        # 生成变化摘要
        changes_summary = self._generate_summary(added_lines, removed_lines, modified_lines)

        return {
            'unified_diff': ''.join(unified_diff),
            'added_lines': added_lines,
            'removed_lines': removed_lines,
            'modified_lines': modified_lines,
            'changes_summary': changes_summary,
            'change_details': change_details[:20],  # 限制详情数量
            'total_changes': added_lines + removed_lines
        }

    def compute_text_diff(self, old_text: str, new_text: str) -> Dict[str, Any]:
        """
        计算纯文本差异（不分行）

        Args:
            old_text: 旧文本
            new_text: 新文本

        Returns:
            差异信息字典
        """
        # 使用序列匹配器
        matcher = difflib.SequenceMatcher(None, old_text, new_text)

        changes = []
        added_chars = 0
        removed_chars = 0

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'replace':
                removed_chars += (i2 - i1)
                added_chars += (j2 - j1)
                changes.append({
                    'type': 'replace',
                    'old': old_text[i1:i2],
                    'new': new_text[j1:j2]
                })
            elif tag == 'delete':
                removed_chars += (i2 - i1)
                changes.append({
                    'type': 'delete',
                    'content': old_text[i1:i2]
                })
            elif tag == 'insert':
                added_chars += (j2 - j1)
                changes.append({
                    'type': 'insert',
                    'content': new_text[j1:j2]
                })

        return {
            'added_chars': added_chars,
            'removed_chars': removed_chars,
            'total_changes': added_chars + removed_chars,
            'changes': changes[:10],  # 限制变化数量
            'similarity': matcher.ratio()
        }

    def generate_html_diff(self, old_content: str, new_content: str) -> str:
        """
        生成HTML格式的差异对比

        Args:
            old_content: 旧内容
            new_content: 新内容

        Returns:
            HTML格式的差异对比
        """
        old_lines = old_content.splitlines()
        new_lines = new_content.splitlines()

        # 使用HtmlDiff生成HTML
        differ = difflib.HtmlDiff()
        html_diff = differ.make_table(
            old_lines,
            new_lines,
            fromdesc='旧版本',
            todesc='新版本',
            context=True,
            numlines=self.context_lines
        )

        return html_diff

    def extract_key_changes(self, diff_result: Dict[str, Any], max_items: int = 5) -> List[str]:
        """
        提取关键变化信息

        Args:
            diff_result: compute_diff()的返回结果
            max_items: 最大提取数量

        Returns:
            关键变化列表
        """
        key_changes = []
        change_details = diff_result.get('change_details', [])

        # 提取有意义的变化（过滤空行和短内容）
        for detail in change_details[:max_items * 2]:
            content = detail.get('content', '').strip()
            if len(content) > 10:  # 忽略太短的内容
                change_type = detail.get('type')
                if change_type == 'add':
                    key_changes.append(f"+ {content[:80]}")
                elif change_type == 'remove':
                    key_changes.append(f"- {content[:80]}")

                if len(key_changes) >= max_items:
                    break

        return key_changes

    def format_diff_for_notification(self, diff_result: Dict[str, Any]) -> str:
        """
        格式化差异信息用于通知

        Args:
            diff_result: compute_diff()的返回结果

        Returns:
            格式化的差异文本
        """
        summary = diff_result.get('changes_summary', '')
        key_changes = self.extract_key_changes(diff_result, max_items=3)

        message_parts = [summary]

        if key_changes:
            message_parts.append("\n\n主要变化:")
            for change in key_changes:
                message_parts.append(f"  {change}")

        return '\n'.join(message_parts)

    def _generate_summary(self, added: int, removed: int, modified: int) -> str:
        """
        生成变化摘要

        Args:
            added: 新增行数
            removed: 删除行数
            modified: 修改行数

        Returns:
            摘要文本
        """
        parts = []

        if modified > 0:
            parts.append(f"修改 {modified} 行")

        pure_added = added - modified
        if pure_added > 0:
            parts.append(f"新增 {pure_added} 行")

        pure_removed = removed - modified
        if pure_removed > 0:
            parts.append(f"删除 {pure_removed} 行")

        if not parts:
            return "内容无变化"

        return "、".join(parts)

    def compare_html_elements(self, old_html: str, new_html: str,
                             selector: Optional[str] = None) -> Dict[str, Any]:
        """
        比较HTML元素

        Args:
            old_html: 旧HTML
            new_html: 新HTML
            selector: CSS选择器（可选）

        Returns:
            比较结果
        """
        try:
            from bs4 import BeautifulSoup

            old_soup = BeautifulSoup(old_html, 'html.parser')
            new_soup = BeautifulSoup(new_html, 'html.parser')

            if selector:
                old_elements = old_soup.select(selector)
                new_elements = new_soup.select(selector)
            else:
                old_elements = [old_soup]
                new_elements = [new_soup]

            # 提取文本进行比较
            old_text = '\n'.join([elem.get_text(strip=True) for elem in old_elements])
            new_text = '\n'.join([elem.get_text(strip=True) for elem in new_elements])

            return self.compute_diff(old_text, new_text)

        except ImportError:
            # 如果没有BeautifulSoup，使用普通文本比较
            return self.compute_diff(old_html, new_html)
        except Exception as e:
            return {
                'error': str(e),
                'unified_diff': '',
                'added_lines': 0,
                'removed_lines': 0,
                'modified_lines': 0,
                'changes_summary': f'比较失败: {e}',
                'change_details': []
            }


def create_diff_report(old_content: str, new_content: str,
                      task_name: str = "", url: str = "") -> str:
    """
    创建完整的差异报告

    Args:
        old_content: 旧内容
        new_content: 新内容
        task_name: 任务名称
        url: URL

    Returns:
        差异报告文本
    """
    differ = ContentDiff()
    diff_result = differ.compute_diff(old_content, new_content)

    report_parts = [
        "=" * 60,
        "内容变化报告",
        "=" * 60,
    ]

    if task_name:
        report_parts.append(f"任务: {task_name}")
    if url:
        report_parts.append(f"URL: {url}")

    report_parts.extend([
        f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "变化摘要:",
        f"  {diff_result['changes_summary']}",
        f"  总变化: {diff_result['total_changes']} 处",
        "",
        "详细差异:",
        "-" * 60,
    ])

    if diff_result['unified_diff']:
        report_parts.append(diff_result['unified_diff'])
    else:
        report_parts.append("(无差异)")

    report_parts.append("=" * 60)

    return '\n'.join(report_parts)
