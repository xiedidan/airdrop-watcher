#!/usr/bin/env python3
"""
查看变化历史命令
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from webmon.cli.command import Command
from webmon.utils.logger import get_logger
from webmon.storage.task_storage import TaskStorage
from webmon.storage.history_storage import HistoryStorage
from webmon.utils.formatters import format_file_size, format_duration


class HistoryCommand(Command):
    """查看变化历史命令"""
    
    def __init__(self, app=None):
        super().__init__(app)
        self.logger = get_logger(__name__)
        # 获取配置路径，默认为config/config.json
        config_path = getattr(self.args, 'config', 'config/config.json') if hasattr(self, 'args') else 'config/config.json'
        self.task_storage = TaskStorage(config_path)
        self.history_storage = HistoryStorage()
    
    def execute(self) -> bool:
        """执行历史查看命令"""
        try:
            task_id = getattr(self.args, 'task_id', None)
            limit = getattr(self.args, 'limit', 20)
            format_type = getattr(self.args, 'format', 'table')
            show_all = getattr(self.args, 'show_all', False)

            self.logger.info(f"执行历史查看命令，任务ID: {task_id}, 限制: {limit}, 格式: {format_type}, 显示全部: {show_all}")

            # 获取历史记录
            if task_id:
                records = self._get_task_history(task_id, limit, show_all)
            else:
                records = self._get_all_history(limit, show_all)

            if not records:
                if show_all:
                    print("📭 没有找到历史记录")
                else:
                    print("📭 没有找到变化记录（使用 --all 查看所有记录）")
                return True

            # 格式化输出
            if format_type == 'json':
                output = self._format_json_output(records)
                print(output)
            elif format_type == 'csv':
                output = self._format_csv_output(records)
                print(output)
            else:  # table
                self._format_table_output(records, task_id, show_all)

            return True

        except Exception as e:
            self.logger.error(f"查看历史记录时发生错误: {e}")
            print(f"❌ 查看历史记录时发生错误: {e}")
            return False
    
    def _get_task_history(self, task_identifier: str, limit: int, show_all: bool = False) -> List[Dict[str, Any]]:
        """获取指定任务的历史记录"""
        # 查找任务
        task = self._find_task(task_identifier)
        if not task:
            print(f"❌ 未找到任务: {task_identifier}")
            return []

        # 获取检测历史和变化历史（获取更多记录用于过滤）
        fetch_limit = limit * 5 if not show_all else limit
        check_results = self.history_storage.list_check_results(
            task_id=task.id,
            limit=fetch_limit
        )

        change_details = self.history_storage.list_change_details(
            task_id=task.id,
            limit=fetch_limit
        )

        # 合并和排序记录
        all_records = []

        # 添加检测记录
        for check in check_results:
            # 如果不是显示全部，只添加有变化的记录
            if not show_all and not check.changed:
                continue

            all_records.append({
                'type': 'check',
                'task_id': check.task_id,
                'task_name': task.name,
                'timestamp': check.timestamp,
                'success': check.success,
                'changed': check.changed,
                'content_size': check.content_size,
                'load_time': check.load_time,
                'content_hash': check.content_hash,
                'status_code': check.status_code,
                'error_message': check.error_message,
                'extracted_data': check.extracted_data,
                # 添加diff信息
                'content_diff': check.content_diff if hasattr(check, 'content_diff') else None,
                'added_lines': check.added_lines if hasattr(check, 'added_lines') else 0,
                'removed_lines': check.removed_lines if hasattr(check, 'removed_lines') else 0,
                'modified_lines': check.modified_lines if hasattr(check, 'modified_lines') else 0,
                'changes_summary': check.changes_summary if hasattr(check, 'changes_summary') else None,
                'change_details': check.change_details if hasattr(check, 'change_details') else []
            })
        
        # 添加变化记录
        for change in change_details:
            all_records.append({
                'type': 'change',
                'task_id': change.task_id,
                'task_name': task.name,
                'timestamp': change.timestamp,
                'similarity': change.similarity,
                'change_count': change.change_count,
                'change_summary': change.changes.get('summary', ''),
                'old_hash': change.old_hash,
                'new_hash': change.new_hash
            })
        
        # 按时间倒序排序
        all_records.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return all_records[:limit]
    
    def _get_all_history(self, limit: int, show_all: bool = False) -> List[Dict[str, Any]]:
        """获取所有任务的历史记录"""
        # 获取所有任务
        tasks = self.task_storage.list_tasks()
        task_map = {task.id: task for task in tasks}

        # 获取最近的历史记录（获取更多记录用于过滤）
        fetch_limit = limit * 5 if not show_all else limit
        recent_checks = self.history_storage.list_check_results(limit=fetch_limit)
        recent_changes = self.history_storage.list_change_details(limit=fetch_limit)

        all_records = []

        # 添加检测记录
        for check in recent_checks:
            task = task_map.get(check.task_id)
            if task:
                # 如果不是显示全部，只添加有变化的记录
                if not show_all and not check.changed:
                    continue

                all_records.append({
                    'type': 'check',
                    'task_id': check.task_id,
                    'task_name': task.name,
                    'timestamp': check.timestamp,
                    'success': check.success,
                    'changed': check.changed,
                    'content_size': check.content_size,
                    'load_time': check.load_time,
                    'content_hash': check.content_hash,
                    'status_code': check.status_code,
                    'error_message': check.error_message,
                    'extracted_data': check.extracted_data,
                    # 添加diff信息
                    'content_diff': check.content_diff if hasattr(check, 'content_diff') else None,
                    'added_lines': check.added_lines if hasattr(check, 'added_lines') else 0,
                    'removed_lines': check.removed_lines if hasattr(check, 'removed_lines') else 0,
                    'modified_lines': check.modified_lines if hasattr(check, 'modified_lines') else 0,
                    'changes_summary': check.changes_summary if hasattr(check, 'changes_summary') else None,
                    'change_details': check.change_details if hasattr(check, 'change_details') else []
                })
        
        # 添加变化记录
        for change in recent_changes:
            task = task_map.get(change.task_id)
            if task:
                all_records.append({
                    'type': 'change',
                    'task_id': change.task_id,
                    'task_name': task.name,
                    'timestamp': change.timestamp,
                    'similarity': change.similarity,
                    'change_count': change.change_count,
                    'change_summary': change.changes.get('summary', ''),
                    'old_hash': change.old_hash,
                    'new_hash': change.new_hash
                })
        
        # 按时间倒序排序
        all_records.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return all_records[:limit]
    
    def _find_task(self, identifier: str) -> Optional[object]:
        """查找任务（支持ID和名称）"""
        from webmon.utils.validators import validate_task_id
        
        # 首先尝试作为ID查找
        if validate_task_id(identifier):
            task = self.task_storage.get_task(identifier)
            if task:
                return task
        
        # 尝试作为名称查找
        tasks = self.task_storage.list_tasks()
        for task in tasks:
            if task.name == identifier:
                return task
        
        return None
    
    def _format_table_output(self, records: List[Dict[str, Any]], task_id: Optional[str], show_all: bool = False):
        """格式化为表格输出"""
        if not records:
            print("📭 没有找到历史记录")
            return

        title = "📋 历史记录" if show_all else "📋 变化记录"
        print(f"\n{title} ({len(records)} 条)")
        print("=" * 80)
        
        # 按时间分组显示
        current_date = None
        
        for record in records:
            record_date = record['timestamp'].strftime('%Y-%m-%d')
            
            # 显示日期分组
            if record_date != current_date:
                current_date = record_date
                print(f"\n📅 {current_date}")
                print("-" * 60)
            
            # 显示记录详情
            if record['type'] == 'check':
                self._format_check_record(record)
            else:
                self._format_change_record(record)
        
        # 显示统计信息
        self._show_history_summary(records)
    
    def _format_check_record(self, record: Dict[str, Any]):
        """格式化检测记录"""
        time_str = record['timestamp'].strftime('%H:%M:%S')
        task_name = record['task_name']

        # 状态图标
        status_icon = "✅" if record['success'] else "❌"
        change_icon = "🔄" if record['changed'] else "⏸️"

        # 基本信息
        print(f"   {time_str} {status_icon} {change_icon} {task_name}")

        # 详细信息
        if record['success']:
            size_str = format_file_size(record['content_size'])
            duration_str = format_duration(record['load_time'])
            print(f"      📄 大小: {size_str}, 加载: {duration_str}, 状态码: {record['status_code']}")

            if record['changed']:
                print(f"      🔄 内容发生变化")

                # 显示变化摘要
                if record.get('changes_summary'):
                    print(f"      📝 {record['changes_summary']}")

                # 显示变化统计
                added = record.get('added_lines', 0)
                removed = record.get('removed_lines', 0)
                modified = record.get('modified_lines', 0)
                if added > 0 or removed > 0 or modified > 0:
                    stats = []
                    if modified > 0:
                        stats.append(f"修改{modified}行")
                    if added - modified > 0:
                        stats.append(f"新增{added - modified}行")
                    if removed - modified > 0:
                        stats.append(f"删除{removed - modified}行")
                    if stats:
                        print(f"      📊 {', '.join(stats)}")

                # 显示关键变化（最多3条）
                change_details = record.get('change_details', [])
                if change_details:
                    print(f"      🔍 关键变化:")
                    for detail in change_details[:3]:
                        change_type = detail.get('type')
                        content = detail.get('content', '').strip()
                        if content and len(content) > 10:
                            if change_type == 'add':
                                print(f"         + {content[:60]}{'...' if len(content) > 60 else ''}")
                            elif change_type == 'remove':
                                print(f"         - {content[:60]}{'...' if len(content) > 60 else ''}")
        else:
            error_msg = record['error_message'] or '未知错误'
            print(f"      ❌ 错误: {error_msg[:50]}{'...' if len(error_msg) > 50 else ''}")
        print()  # 记录之间加空行
    
    def _format_change_record(self, record: Dict[str, Any]):
        """格式化变化记录"""
        time_str = record['timestamp'].strftime('%H:%M:%S')
        task_name = record['task_name']
        similarity = record['similarity']
        change_count = record['change_count']
        
        print(f"   {time_str} 📝 {task_name}")
        print(f"      📊 相似度: {similarity:.2f}, 变化数: {change_count}")
        
        if record.get('change_summary'):
            summary = record['change_summary']
            print(f"      📝 摘要: {summary[:60]}{'...' if len(summary) > 60 else ''}")
        print()  # 记录之间加空行
    
    def _show_history_summary(self, records: List[Dict[str, Any]]):
        """显示历史记录统计"""
        if not records:
            return
        
        # 统计信息
        total_checks = len([r for r in records if r['type'] == 'check'])
        total_changes = len([r for r in records if r['type'] == 'change'])
        successful_checks = len([r for r in records if r['type'] == 'check' and r['success']])
        
        print(f"\n📊 统计摘要:")
        print(f"   总记录: {len(records)} 条")
        print(f"   检测记录: {total_checks} 条 (成功: {successful_checks})")
        print(f"   变化记录: {total_changes} 条")
        
        if total_checks > 0:
            success_rate = (successful_checks / total_checks) * 100
            print(f"   检测成功率: {success_rate:.1f}%")
        
        if total_checks > 0 and total_changes > 0:
            change_rate = (total_changes / total_checks) * 100
            print(f"   内容变化率: {change_rate:.1f}%")
        
        # 时间范围
        oldest_record = min(records, key=lambda r: r['timestamp'])
        newest_record = max(records, key=lambda r: r['timestamp'])
        
        print(f"   时间范围: {oldest_record['timestamp'].strftime('%Y-%m-%d %H:%M')} - {newest_record['timestamp'].strftime('%Y-%m-%d %H:%M')}")
    
    def _format_json_output(self, records: List[Dict[str, Any]]) -> str:
        """格式化为JSON输出"""
        # 转换datetime对象为字符串
        json_records = []
        for record in records:
            json_record = record.copy()
            json_record['timestamp'] = record['timestamp'].isoformat()
            json_records.append(json_record)
        
        return json.dumps({
            "records": json_records,
            "count": len(json_records),
            "summary": {
                "total_checks": len([r for r in records if r['type'] == 'check']),
                "total_changes": len([r for r in records if r['type'] == 'change']),
                "successful_checks": len([r for r in records if r['type'] == 'check' and r['success']])
            }
        }, ensure_ascii=False, indent=2)
    
    def _format_csv_output(self, records: List[Dict[str, Any]]) -> str:
        """格式化为CSV输出"""
        import csv
        import io
        
        output = io.StringIO()
        
        # CSV标题
        fieldnames = [
            'timestamp', 'type', 'task_id', 'task_name', 
            'success', 'changed', 'content_size', 'load_time',
            'similarity', 'change_count', 'status_code', 'error_message'
        ]
        
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        # 写入数据
        for record in records:
            row = {
                'timestamp': record['timestamp'].isoformat(),
                'type': record['type'],
                'task_id': record['task_id'],
                'task_name': record['task_name']
            }
            
            # 根据记录类型添加相应字段
            if record['type'] == 'check':
                row.update({
                    'success': record['success'],
                    'changed': record['changed'],
                    'content_size': record['content_size'],
                    'load_time': record['load_time'],
                    'status_code': record['status_code'],
                    'error_message': record['error_message']
                })
            else:  # change
                row.update({
                    'similarity': record['similarity'],
                    'change_count': record['change_count']
                })
            
            writer.writerow(row)
        
        return output.getvalue()
    
    def validate_args(self, args) -> bool:
        """验证参数"""
        # 验证limit参数
        limit = getattr(args, 'limit', 20)
        if limit <= 0:
            self.logger.error("limit参数必须大于0")
            print("❌ 错误: limit参数必须大于0")
            return False
        
        if limit > 1000:
            self.logger.error("limit参数不能超过1000")
            print("❌ 错误: limit参数不能超过1000")
            return False
        
        # 验证format参数
        format_type = getattr(args, 'format', 'table')
        valid_formats = ['table', 'json', 'csv']
        if format_type not in valid_formats:
            self.logger.error(f"无效的格式类型: {format_type}")
            print(f"❌ 错误: 无效的格式类型 '{format_type}'，支持: {', '.join(valid_formats)}")
            return False
        
        return True