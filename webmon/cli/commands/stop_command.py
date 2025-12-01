#!/usr/bin/env python3
"""
停止监控服务命令
"""

import asyncio
import signal
import os
import time
from pathlib import Path
from argparse import Namespace
from typing import Optional, List, Dict, Any

from webmon.cli.command import Command
from webmon.utils.logger import get_logger
from webmon.scheduler import TaskScheduler
from webmon.config import ConfigManager


class StopCommand(Command):
    """停止监控服务命令"""
    
    def __init__(self, args: Namespace):
        super().__init__(args)
        self.logger = get_logger(__name__)
    
    def execute(self) -> bool:
        """执行停止命令"""
        try:
            self.logger.info("执行停止监控服务命令")
            
            # 参数验证
            if not self.validate_args():
                return False
            
            # 检查服务是否正在运行
            if not self._is_service_running():
                print("⚠️  监控服务未在运行")
                return True
            
            # 获取停止参数
            force_mode = getattr(self.args, 'force', False)
            timeout = getattr(self.args, 'timeout', 30)
            
            # 停止服务
            return self._stop_service(force_mode, timeout)
            
        except KeyboardInterrupt:
            self.logger.info("用户中断停止操作")
            print("\n⏹️  停止操作已取消")
            return False
        except Exception as e:
            self.logger.error(f"停止监控服务失败: {e}")
            print(f"❌ 停止监控服务失败: {e}")
            return False
    
    def _stop_service(self, force_mode: bool, timeout: int) -> bool:
        """停止监控服务"""
        try:
            self.logger.info(f"正在停止监控服务 (force={force_mode}, timeout={timeout})")
            
            if force_mode:
                print("🛑 正在强制停止监控服务...")
                return self._force_stop_service()
            else:
                print("⏹️  正在优雅停止监控服务...")
                return self._graceful_stop_service(timeout)
                
        except Exception as e:
            self.logger.error(f"停止服务失败: {e}")
            return False
    
    def _graceful_stop_service(self, timeout: int) -> bool:
        """优雅停止服务"""
        try:
            # 获取PID
            pid = self._get_service_pid()
            if not pid:
                print("❌ 无法获取服务PID")
                return False
            
            print(f"📋 找到服务进程 (PID: {pid})")
            
            # 发送终止信号
            self.logger.info(f"向进程 {pid} 发送终止信号")
            
            try:
                import psutil
                process = psutil.Process(pid)
                
                # 发送SIGTERM信号
                process.terminate()
                
                # 等待进程结束
                print(f"⏳ 等待服务优雅关闭 (最长 {timeout} 秒)...")
                
                try:
                    process.wait(timeout=timeout)
                    print("✅ 服务已优雅停止")
                    
                    # 清理PID文件
                    self._cleanup_pid_file()
                    
                    # 显示停止信息
                    self._show_stop_info(pid, graceful=True)
                    
                    return True
                    
                except psutil.TimeoutExpired:
                    print(f"⚠️  服务在 {timeout} 秒内未正常停止")
                    
                    # 询问是否强制停止
                    if self._confirm_force_stop():
                        return self._force_stop_service()
                    else:
                        return False
                        
            except ImportError:
                # 没有psutil，使用简化方式
                return self._simple_stop_service(pid, timeout)
                
        except Exception as e:
            self.logger.error(f"优雅停止服务失败: {e}")
            return False
    
    def _force_stop_service(self) -> bool:
        """强制停止服务"""
        try:
            # 获取PID
            pid = self._get_service_pid()
            if not pid:
                print("❌ 无法获取服务PID")
                return False
            
            print(f"🛑 强制停止服务进程 (PID: {pid})")
            self.logger.info(f"强制停止服务进程 {pid}")
            
            try:
                import psutil
                process = psutil.Process(pid)
                
                # 发送SIGKILL信号
                process.kill()
                
                # 等待进程结束
                try:
                    process.wait(timeout=5)
                    print("✅ 服务已强制停止")
                    
                    # 清理PID文件
                    self._cleanup_pid_file()
                    
                    # 显示停止信息
                    self._show_stop_info(pid, graceful=False)
                    
                    return True
                    
                except psutil.TimeoutExpired:
                    print("⚠️  强制停止可能需要系统权限")
                    return False
                    
            except ImportError:
                # 没有psutil，使用kill命令
                return self._kill_process(pid)
                
        except Exception as e:
            self.logger.error(f"强制停止服务失败: {e}")
            return False
    
    def _simple_stop_service(self, pid: int, timeout: int) -> bool:
        """简化停止服务（无psutil）"""
        try:
            # 发送SIGTERM信号
            import signal
            os.kill(pid, signal.SIGTERM)
            
            print(f"⏳ 等待服务优雅关闭 (最长 {timeout} 秒)...")
            
            # 等待进程结束
            for i in range(timeout):
                if not self._is_process_running(pid):
                    print("✅ 服务已优雅停止")
                    
                    # 清理PID文件
                    self._cleanup_pid_file()
                    
                    # 显示停止信息
                    self._show_stop_info(pid, graceful=True)
                    
                    return True
                
                time.sleep(1)
            
            print(f"⚠️  服务在 {timeout} 秒内未正常停止")
            
            # 询问是否强制停止
            if self._confirm_force_stop():
                return self._kill_process(pid)
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"简化停止服务失败: {e}")
            return False
    
    def _kill_process(self, pid: int) -> bool:
        """强制杀死进程"""
        try:
            import signal
            os.kill(pid, signal.SIGKILL)
            
            # 等待进程结束
            time.sleep(2)
            
            if not self._is_process_running(pid):
                print("✅ 服务已强制停止")
                
                # 清理PID文件
                self._cleanup_pid_file()
                
                # 显示停止信息
                self._show_stop_info(pid, graceful=False)
                
                return True
            else:
                print("⚠️  强制停止可能需要系统权限")
                return False
                
        except Exception as e:
            self.logger.error(f"强制杀死进程失败: {e}")
            return False
    
    def _get_service_pid(self) -> Optional[int]:
        """获取服务PID"""
        try:
            pid_file = Path("webmon.pid")
            if not pid_file.exists():
                return None
            
            with open(pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # 验证PID是否有效
            if pid <= 0:
                self.logger.warning(f"无效的PID: {pid}")
                return None
            
            return pid
            
        except (ValueError, FileNotFoundError) as e:
            self.logger.warning(f"读取PID文件失败: {e}")
            return None
        except Exception as e:
            self.logger.error(f"获取服务PID失败: {e}")
            return None
    
    def _is_service_running(self) -> bool:
        """检查服务是否正在运行"""
        try:
            pid = self._get_service_pid()
            if not pid:
                return False
            
            return self._is_process_running(pid)
            
        except Exception as e:
            self.logger.warning(f"检查服务状态失败: {e}")
            return False
    
    def _is_process_running(self, pid: int) -> bool:
        """检查进程是否正在运行"""
        try:
            # 方法1: 使用psutil（如果可用）
            try:
                import psutil
                return psutil.pid_exists(pid) and psutil.Process(pid).is_running()
            except ImportError:
                pass
            
            # 方法2: 向进程发送信号0
            import signal
            try:
                os.kill(pid, 0)
                return True
            except OSError:
                return False
                
        except Exception as e:
            self.logger.warning(f"检查进程状态失败 (PID: {pid}): {e}")
            return False
    
    def _cleanup_pid_file(self):
        """清理PID文件"""
        try:
            pid_file = Path("webmon.pid")
            if pid_file.exists():
                pid_file.unlink()
                self.logger.info("PID文件已清理")
                
        except Exception as e:
            self.logger.warning(f"清理PID文件失败: {e}")
    
    def _confirm_force_stop(self) -> bool:
        """确认是否强制停止"""
        try:
            response = input("是否强制停止服务？此操作可能导致数据丢失 [y/N]: ").strip().lower()
            return response in ['y', 'yes']
            
        except (KeyboardInterrupt, EOFError):
            return False
    
    def _show_stop_info(self, pid: int, graceful: bool):
        """显示停止信息"""
        try:
            stop_time = "优雅" if graceful else "强制"
            
            print(f"\n📊 服务停止信息")
            print("=" * 40)
            print(f"⏹️  停止方式: {stop_time}")
            print(f"📝 进程PID: {pid}")
            print(f"⏰ 停止时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 显示额外的统计信息（如果可用）
            stats = self._get_service_stats(pid)
            if stats:
                print(f"📈 总执行次数: {stats.get('total_executions', 0)}")
                print(f"✅ 成功次数: {stats.get('successful_executions', 0)}")
                print(f"🔄 变化次数: {stats.get('total_changes', 0)}")
            
            print("=" * 40)
            print("✅ 监控服务已停止")
            
        except Exception as e:
            self.logger.warning(f"显示停止信息失败: {e}")
    
    def _get_service_stats(self, pid: int) -> Optional[Dict[str, Any]]:
        """获取服务统计信息"""
        try:
            # 这里可以从日志文件或其他存储中获取统计信息
            # 简化实现，返回空统计
            return {
                'total_executions': 0,
                'successful_executions': 0,
                'total_changes': 0
            }
            
        except Exception as e:
            self.logger.warning(f"获取服务统计信息失败: {e}")
            return None
    
    def _get_config_manager(self):
        """获取配置管理器"""
        config_path = getattr(self.args, 'config', 'config/config.json')
        env_path = getattr(self.args, 'env', '.env')
        
        config_manager = ConfigManager()
        
        # 设置配置文件路径
        if hasattr(config_manager, 'json_config'):
            config_manager.json_config.file_path = Path(config_path)
        
        if hasattr(config_manager, 'env_config'):
            config_manager.env_config.env_file = Path(env_path)
        
        return config_manager
    
    def validate_args(self) -> bool:
        """验证参数"""
        # 验证超时参数
        timeout = getattr(self.args, 'timeout', 30)
        if not isinstance(timeout, int) or timeout <= 0:
            print("❌ 错误: 超时参数必须是正整数")
            return False
        
        if timeout > 300:  # 5分钟
            print("⚠️  警告: 超时时间设置过长，可能影响用户体验")
        
        return True
    
    def format_output(self, result: bool, format_type: str = 'text') -> str:
        """格式化输出"""
        import json
        
        if format_type == 'json':
            return json.dumps({
                "success": result,
                "message": "监控服务已停止" if result else "监控服务停止失败",
                "force_mode": getattr(self.args, 'force', False),
                "timeout": getattr(self.args, 'timeout', 30)
            }, ensure_ascii=False, indent=2)
        else:
            return ""