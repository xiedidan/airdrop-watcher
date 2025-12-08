#!/usr/bin/env python3
"""
查看系统状态命令
"""

import json
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from webmon.cli.command import Command
from webmon.utils.logger import get_logger
from webmon.storage.task_storage import TaskStorage
from webmon.storage.history_storage import HistoryStorage
from webmon.config import ConfigManager


class StatusCommand(Command):
    """查看系统状态命令"""
    
    def __init__(self, app=None):
        super().__init__(app)
        self.logger = get_logger(__name__)
        # 获取配置路径，默认为config/config.json
        config_path = getattr(self.args, 'config', 'config/config.json') if hasattr(self, 'args') else 'config/config.json'
        self.task_storage = TaskStorage(config_path)
        self.history_storage = HistoryStorage()
        self.config_manager = ConfigManager()
    
    def execute(self) -> bool:
        """执行状态查看命令"""
        try:
            self.logger.info("执行系统状态查看命令")
            
            # 收集各项状态信息
            status_info = self._collect_status_info()
            
            # 根据输出格式显示结果
            if getattr(self.args, 'json', False):
                output = self._format_json_output(status_info)
                print(output)
            else:
                self._format_text_output(status_info)
            
            return True
            
        except Exception as e:
            self.logger.error(f"查看系统状态时发生错误: {e}")
            print(f"❌ 查看系统状态时发生错误: {e}")
            return False
    
    def _collect_status_info(self) -> Dict[str, Any]:
        """收集系统状态信息"""
        status_info = {}
        
        # 基本信息
        status_info['system'] = self._get_system_info()
        status_info['tasks'] = self._get_tasks_info()
        status_info['history'] = self._get_history_info()
        status_info['config'] = self._get_config_info()
        status_info['service'] = self._get_service_info()
        
        return status_info
    
    def _get_system_info(self) -> Dict[str, Any]:
        """获取系统信息"""
        try:
            # 尝试导入psutil，如果不可用则提供基础信息
            try:
                import psutil
                # 系统资源使用情况
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                return {
                    'platform': sys.platform,
                    'memory_usage': {
                        'total': memory.total,
                        'available': memory.available,
                        'percent': memory.percent,
                        'used': memory.used
                    },
                    'disk_usage': {
                        'total': disk.total,
                        'free': disk.free,
                        'used': disk.used,
                        'percent': (disk.used / disk.total) * 100
                    },
                    'cpu_count': psutil.cpu_count(),
                    'cpu_percent': psutil.cpu_percent(interval=1),
                    'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat(),
                    'current_time': datetime.now().isoformat()
                }
            except ImportError:
                # psutil不可用，提供基础信息
                return {
                    'platform': sys.platform,
                    'current_time': datetime.now().isoformat(),
                    'note': '系统资源信息需要安装psutil库: pip install psutil'
                }
        except Exception as e:
            self.logger.warning(f"获取系统信息失败: {e}")
            return {
                'platform': sys.platform,
                'current_time': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def _get_tasks_info(self) -> Dict[str, Any]:
        """获取任务信息"""
        try:
            tasks = self.task_storage.list_tasks()
            
            # 统计各种状态的任务数量
            status_counts = {}
            enabled_count = 0
            total_interval = 0
            
            for task in tasks:
                status = task.status or 'unknown'
                status_counts[status] = status_counts.get(status, 0) + 1
                
                if task.enabled:
                    enabled_count += 1
                    total_interval += task.interval
            
            # 计算平均检测间隔
            avg_interval = total_interval / enabled_count if enabled_count > 0 else 0
            
            return {
                'total': len(tasks),
                'enabled': enabled_count,
                'disabled': len(tasks) - enabled_count,
                'status_breakdown': status_counts,
                'average_interval': round(avg_interval, 1),
                'by_status': self._get_tasks_by_status(tasks)
            }
        except Exception as e:
            self.logger.warning(f"获取任务信息失败: {e}")
            return {
                'total': 0,
                'enabled': 0,
                'disabled': 0,
                'status_breakdown': {},
                'average_interval': 0,
                'error': str(e)
            }
    
    def _get_tasks_by_status(self, tasks) -> Dict[str, list]:
        """按状态分组任务"""
        tasks_by_status = {}
        
        for task in tasks[:10]:  # 限制显示数量
            status = task.status or 'unknown'
            if status not in tasks_by_status:
                tasks_by_status[status] = []
            
            tasks_by_status[status].append({
                'id': task.id,
                'name': task.name,
                'url': task.url,
                'interval': task.interval,
                'last_check': task.last_check.isoformat() if task.last_check else None,
                'last_change': task.last_change.isoformat() if task.last_change else None,
                'change_count': task.change_count
            })
        
        return tasks_by_status
    
    def _get_history_info(self) -> Dict[str, Any]:
        """获取历史记录信息"""
        try:
            # 获取最近24小时的统计
            last_24h = datetime.now() - timedelta(hours=24)
            
            # 获取总体统计
            stats = self.history_storage.get_history_statistics()
            
            # 获取最近记录
            recent_checks = self.history_storage.list_check_results(limit=10)
            recent_changes = self.history_storage.list_change_details(limit=10)
            
            return {
                'total_checks': stats.get('total_checks', 0),
                'total_changes': stats.get('total_changes', 0),
                'success_rate': stats.get('success_rate', 0),
                'change_rate': stats.get('change_rate', 0),
                'last_24h_checks': len([c for c in recent_checks if c.timestamp > last_24h]),
                'last_24h_changes': len([c for c in recent_changes if c.timestamp > last_24h]),
                'recent_checks': [
                    {
                        'task_id': c.task_id,
                        'success': c.success,
                        'changed': c.changed,
                        'timestamp': c.timestamp.isoformat(),
                        'content_size': c.content_size,
                        'load_time': c.load_time
                    }
                    for c in recent_checks[:5]
                ],
                'recent_changes': [
                    {
                        'task_id': c.task_id,
                        'similarity': c.similarity,
                        'change_count': c.change_count,
                        'timestamp': c.timestamp.isoformat(),
                        'change_summary': c.get('change_summary', '')
                    }
                    for c in recent_changes[:5]
                ]
            }
        except Exception as e:
            self.logger.warning(f"获取历史信息失败: {e}")
            return {
                'total_checks': 0,
                'total_changes': 0,
                'success_rate': 0,
                'change_rate': 0,
                'error': str(e)
            }
    
    def _get_config_info(self) -> Dict[str, Any]:
        """获取配置信息"""
        try:
            # 获取通知配置
            notification_config = self.config_manager.get_notification_config()
            
            # 首先尝试新的配置结构 (platforms + platform_configs)
            platforms = notification_config.get('platforms', [])
            enabled_platforms = []
            
            # 检查每个平台是否启用
            platform_configs = notification_config.get('platform_configs', {})
            for platform_name in platforms:
                config = platform_configs.get(platform_name, {})
                if config.get('enabled', False):
                    enabled_platforms.append(platform_name)
            
            # 如果没有找到启用的平台，尝试旧的配置结构 (enabled_platforms)
            if not enabled_platforms:
                config = self.config_manager.json_config.get_all()
                notification_config_old = config.get('notification', {})
                enabled_platforms = notification_config_old.get('enabled_platforms', [])
            
            # 监控设置
            config = self.config_manager.json_config.get_all()
            settings = config.get('settings', {})
            
            return {
                'version': config.get('version', 'unknown'),
                'config_file': str(self.config_manager.json_file),
                'notification_platforms': {
                    'enabled': enabled_platforms,
                    'count': len(enabled_platforms),
                    'available': ['pushplus', 'telegram', 'discord', 'feishu']
                },
                'monitor_settings': {
                    'default_interval': settings.get('default_check_interval', 60),
                    'max_concurrent': settings.get('max_concurrent_tasks', 5),
                    'timeout': settings.get('browser_timeout', 30),
                    'similarity_threshold': settings.get('similarity_threshold', 0.95),
                    'history_retention_days': settings.get('history_retention_days', 30)
                }
            }
        except Exception as e:
            self.logger.warning(f"获取配置信息失败: {e}")
            return {
                'version': 'unknown',
                'error': str(e)
            }
    
    def _get_service_info(self) -> Dict[str, Any]:
        """获取服务状态信息"""
        try:
            # 检查是否有WebMon进程在运行
            webmon_processes = []
            try:
                import psutil
                for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
                    try:
                        cmdline = proc.info.get('cmdline', [])
                        if cmdline and any('webmon' in str(arg).lower() for arg in cmdline):
                            webmon_processes.append({
                                'pid': proc.info['pid'],
                                'name': proc.info['name'],
                                'create_time': datetime.fromtimestamp(proc.info['create_time']).isoformat(),
                                'cmdline': ' '.join(cmdline)
                            })
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
            except ImportError:
                # psutil不可用，跳过进程检查
                pass
            
            # 检查日志文件
            import os
            from pathlib import Path
            log_file = Path('logs/webmon.log')
            log_info = {
                'exists': log_file.exists(),
                'size': log_file.stat().st_size if log_file.exists() else 0,
                'modified': datetime.fromtimestamp(log_file.stat().st_mtime).isoformat() if log_file.exists() else None
            }
            
            return {
                'running_processes': webmon_processes,
                'process_count': len(webmon_processes),
                'is_running': len(webmon_processes) > 0,
                'log_file': log_info,
                'uptime': self._get_uptime_info()
            }
        except Exception as e:
            self.logger.warning(f"获取服务信息失败: {e}")
            return {
                'running_processes': [],
                'process_count': 0,
                'is_running': False,
                'error': str(e)
            }
    
    def _get_uptime_info(self) -> Optional[str]:
        """获取运行时间信息"""
        try:
            # 简单估算：基于最近的历史记录时间
            latest_check = self.history_storage.get_latest_check_result()
            if latest_check and latest_check.timestamp:
                uptime = datetime.now() - latest_check.timestamp
                hours = uptime.total_seconds() / 3600
                if hours < 1:
                    return f"{int(uptime.total_seconds() / 60)} 分钟"
                elif hours < 24:
                    return f"{int(hours)} 小时"
                else:
                    return f"{int(hours / 24)} 天 {int(hours % 24)} 小时"
            return None
        except Exception:
            return None
    
    def _format_text_output(self, status_info: Dict[str, Any]):
        """格式化文本输出"""
        print("📊 WebMon 系统状态")
        print("=" * 50)
        
        # 任务概览
        tasks_info = status_info['tasks']
        print(f"📝 任务概览:")
        print(f"   总任务数: {tasks_info['total']}")
        print(f"   启用任务: {tasks_info['enabled']} | 禁用任务: {tasks_info['disabled']}")
        if tasks_info['enabled'] > 0:
            print(f"   平均检测间隔: {tasks_info['average_interval']} 分钟")

        # 显示任务状态统计
        status_breakdown = tasks_info.get('status_breakdown', {})
        if status_breakdown:
            print(f"\n   任务状态统计:")
            for status, count in status_breakdown.items():
                print(f"      {status}: {count}")
        print()
        
        # 历史统计
        history_info = status_info['history']
        print(f"📈 历史统计:")
        print(f"   总检测次数: {history_info['total_checks']}")
        print(f"   总变化次数: {history_info['total_changes']}")
        print(f"   成功率: {history_info['success_rate']:.1f}%")
        print(f"   变化率: {history_info['change_rate']:.1f}%")
        
        if history_info.get('last_24h_checks', 0) > 0:
            print(f"   最近24小时: {history_info['last_24h_checks']} 次检测, {history_info['last_24h_changes']} 次变化")
        print()
        
        # 服务状态
        service_info = status_info['service']
        print(f"🔄 服务状态:")
        if service_info['is_running']:
            print(f"   ✅ 运行中 (进程数: {service_info['process_count']})")
            if service_info['uptime']:
                print(f"   运行时间: {service_info['uptime']}")
        else:
            print(f"   ❌ 未运行")
        
        # 日志文件
        log_info = service_info['log_file']
        if log_info['exists']:
            size_mb = log_info['size'] / (1024 * 1024)
            print(f"   日志文件: {size_mb:.1f} MB (最后更新: {log_info['modified']})")
        print()
        
        # 配置信息
        config_info = status_info['config']
        print(f"⚙️  配置信息:")
        print(f"   版本: {config_info['version']}")
        print(f"   配置文件: {config_info['config_file']}")
        
        # 通知平台
        notification_info = config_info['notification_platforms']
        if notification_info['count'] > 0:
            print(f"   通知平台: {', '.join(notification_info['enabled'])}")
        else:
            print(f"   通知平台: 未配置")
        
        # 监控设置
        settings = config_info['monitor_settings']
        print(f"   默认间隔: {settings['default_interval']} 分钟")
        print(f"   最大并发: {settings['max_concurrent']} 任务")
        print(f"   相似度阈值: {settings['similarity_threshold']}")
        print()
        
        # 系统资源
        system_info = status_info['system']
        if 'memory_usage' in system_info:
            memory = system_info['memory_usage']
            print(f"💻 系统资源:")
            print(f"   内存使用: {memory['percent']:.1f}% ({memory['used'] / (1024**3):.1f}GB / {memory['total'] / (1024**3):.1f}GB)")
            
            if 'disk_usage' in system_info:
                disk = system_info['disk_usage']
                print(f"   磁盘使用: {disk['percent']:.1f}%")
        elif 'note' in system_info:
            print(f"💻 系统资源: {system_info['note']}")
        
        # 最近活动
        if history_info.get('recent_checks'):
            print(f"\n📋 最近检测:")
            for check in history_info['recent_checks'][:3]:
                status = "✅" if check['success'] else "❌"
                changed = "🔄" if check['changed'] else "⏸️"
                print(f"   {status} {changed} {check['timestamp'][:19]} - {check['load_time']:.1f}s")
        
        if history_info.get('recent_changes'):
            print(f"\n🔄 最近变化:")
            for change in history_info['recent_changes'][:3]:
                print(f"   📝 {change['timestamp'][:19]} - 相似度: {change['similarity']:.2f}, 变化数: {change['change_count']}")

        # 显示每个任务的详细状态
        print(f"\n📋 任务详细状态:")
        print("=" * 100)
        tasks = self.task_storage.list_tasks()
        if tasks:
            for task in tasks:
                # 任务状态图标
                enabled_icon = "✅" if task.enabled else "❌"
                status_icon = {
                    'active': '🟢',
                    'error': '🔴',
                    'idle': '🟡',
                    'unknown': '⚪'
                }.get(task.status or 'unknown', '⚪')

                print(f"\n{enabled_icon} {status_icon} [{task.id[:8]}] {task.name}")
                print(f"   URL: {task.url}")
                print(f"   状态: {task.status or 'unknown'} | 启用: {'是' if task.enabled else '否'}")
                print(f"   间隔: {task.interval}分钟 | 超时: {task.timeout}ms")
                if task.last_check:
                    print(f"   最后检测: {task.last_check.isoformat()[:19]}")
                if task.last_change:
                    print(f"   最后变化: {task.last_change.isoformat()[:19]}")
                print(f"   变化次数: {task.change_count}")
        else:
            print("   暂无任务")
        print("=" * 100)
    
    def _format_json_output(self, status_info: Dict[str, Any]) -> str:
        """格式化JSON输出"""
        return json.dumps(status_info, ensure_ascii=False, indent=2)
    
    def validate_args(self) -> bool:
        """验证参数"""
        # status命令不需要特殊参数验证
        return True