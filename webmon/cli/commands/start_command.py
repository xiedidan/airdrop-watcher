#!/usr/bin/env python3
"""
启动监控服务命令
"""

import asyncio
import signal
import sys
import os
from pathlib import Path
from argparse import Namespace
from typing import Optional

from webmon.cli.command import Command
from webmon.utils.logger import get_logger, setup_global_logger
from webmon.scheduler import TaskScheduler
from webmon.config import ConfigManager
from webmon.utils.validators import validate_interval


class StartCommand(Command):
    """启动监控服务命令"""
    
    def __init__(self, args: Namespace):
        super().__init__(args)
        self.logger = get_logger(__name__)
        self.scheduler: Optional[TaskScheduler] = None
        self._shutdown_event = asyncio.Event()
    
    def execute(self) -> bool:
        """执行启动命令"""
        try:
            self.logger.info("执行启动监控服务命令")
            
            # 参数验证
            if not self.validate_args():
                return False
            
            # 检查是否已在运行
            if self._is_service_running():
                print("⚠️  监控服务已经在运行中")
                return False
            
            # 获取配置
            config_manager = self._get_config_manager()
            
            # 检查守护进程模式
            daemon_mode = getattr(self.args, 'daemon', False)
            specific_task = getattr(self.args, 'task', None)
            
            if daemon_mode:
                return self._start_daemon_mode(config_manager, specific_task)
            else:
                return self._start_foreground_mode(config_manager, specific_task)
                
        except KeyboardInterrupt:
            self.logger.info("用户中断启动操作")
            print("\n⏹️  启动操作已取消")
            return False
        except Exception as e:
            self.logger.error(f"启动监控服务失败: {e}")
            print(f"❌ 启动监控服务失败: {e}")
            return False
    
    def _start_daemon_mode(self, config_manager: ConfigManager, specific_task: Optional[str]) -> bool:
        """启动守护进程模式"""
        try:
            self.logger.info("启动守护进程模式...")
            print("🚀 正在启动监控服务（守护进程模式）...")

            # 先检查PID文件是否已存在（不创建）
            pid_file = Path("webmon.pid")
            if pid_file.exists():
                self.logger.warning("PID文件已存在，守护进程可能已在运行")
                print("⚠️  守护进程可能已在运行，请先执行 stop 命令")
                return False

            # 守护进程化（fork之后才创建PID文件）
            self._daemonize()

            # 在守护进程化后创建PID文件（此时已是最终的子进程）
            if not self._create_pid_file():
                return False

            # 设置信号处理
            self._setup_signal_handlers()

            # 运行事件循环
            return asyncio.run(self._run_scheduler(config_manager, specific_task))

        except Exception as e:
            self.logger.error(f"守护进程模式启动失败: {e}")
            return False
    
    def _start_foreground_mode(self, config_manager: ConfigManager, specific_task: Optional[str]) -> bool:
        """启动前台模式"""
        try:
            self.logger.info("启动前台模式...")
            print("🚀 正在启动监控服务（前台模式）...")
            
            # 设置信号处理
            self._setup_signal_handlers()
            
            # 运行事件循环
            return asyncio.run(self._run_scheduler(config_manager, specific_task))
            
        except Exception as e:
            self.logger.error(f"前台模式启动失败: {e}")
            return False
    
    async def _run_scheduler(self, config_manager: ConfigManager, specific_task: Optional[str]) -> bool:
        """运行调度器"""
        try:
            # 创建任务调度器
            self.scheduler = TaskScheduler(config_manager)
            
            # 如果指定了特定任务，只运行该任务
            if specific_task:
                await self._run_specific_task(specific_task)
            else:
                # 启动完整调度服务
                success = await self.scheduler.start()
                
                if success:
                    self.logger.info("监控服务启动成功")
                    print("✅ 监控服务启动成功！")
                    
                    # 显示状态信息
                    await self._show_status()
                    
                    # 等待关闭信号
                    await self._wait_for_shutdown()
                    
                    return True
                else:
                    print("❌ 监控服务启动失败")
                    return False
                    
        except asyncio.CancelledError:
            self.logger.info("调度器任务被取消")
            return False
        except Exception as e:
            self.logger.error(f"运行调度器失败: {e}")
            return False
        finally:
            # 清理资源
            if self.scheduler and self.scheduler.is_running:
                await self.scheduler.stop()
    
    async def _run_specific_task(self, task_identifier: str):
        """运行特定任务"""
        try:
            # 查找任务
            task = self._find_task(task_identifier)
            if not task:
                print(f"❌ 未找到任务: {task_identifier}")
                return

            # 如果任务被禁用，自动启用它
            if not task.enabled:
                print(f"⚠️  任务 {task.name} 当前已禁用，正在自动启用...")
                self._enable_task(task.id)
                task.enabled = True  # 更新本地对象
                print(f"✅ 任务已启用")

            print(f"🎯 正在运行特定任务: {task.name} (ID: {task.id})")
            print(f"   URL: {task.url}")

            # 实际执行任务
            try:
                await self.scheduler._execute_task(task)
                print(f"✅ 任务 {task.name} 执行完成")

                # 显示执行结果
                from webmon.storage.task_storage import TaskStorage
                storage = TaskStorage()
                updated_task = storage.get_task(task.id)
                if updated_task:
                    print(f"\n📊 执行结果:")
                    print(f"   状态: {updated_task.status}")
                    print(f"   最后检测: {updated_task.last_check}")
                    if updated_task.error_count > 0:
                        print(f"   ⚠️  错误次数: {updated_task.error_count}")
                        print(f"   错误信息: {updated_task.last_error_message}")

            except Exception as e:
                self.logger.error(f"执行任务失败: {e}", exc_info=True)
                print(f"❌ 任务执行失败: {e}")
                print(f"   请查看日志文件了解详细信息: logs/webmon.log")

        except Exception as e:
            self.logger.error(f"运行特定任务失败: {e}")
            print(f"❌ 运行特定任务失败: {e}")
    
    def _find_task(self, identifier: str):
        """查找任务"""
        from webmon.utils.validators import validate_task_id
        from webmon.storage.task_storage import TaskStorage
        
        storage = TaskStorage()
        
        # 首先尝试作为ID查找
        if validate_task_id(identifier):
            task = storage.get_task(identifier)
            if task:
                return task
        
        # 尝试作为名称查找
        tasks = storage.list_tasks()
        for task in tasks:
            if task.name == identifier:
                return task
        
        return None

    def _enable_task(self, task_id: str) -> bool:
        """启用指定任务"""
        try:
            import json
            from pathlib import Path

            config_file = Path('config/config.json')

            # 读取配置
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # 找到任务并启用
            for task in config.get('tasks', []):
                if task['id'] == task_id:
                    task['enabled'] = True
                    task['updated_at'] = self._get_current_timestamp()
                    break

            # 保存配置
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            self.logger.info(f"任务已启用: {task_id}")
            return True

        except Exception as e:
            self.logger.error(f"启用任务失败: {e}")
            return False

    def _get_current_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()

    def _is_service_running(self) -> bool:
        """检查服务是否已在运行"""
        try:
            pid_file = Path("webmon.pid")
            if pid_file.exists():
                # 检查PID是否有效
                try:
                    with open(pid_file, 'r') as f:
                        pid = int(f.read().strip())
                    
                    # 检查进程是否存在
                    import psutil
                    if psutil.pid_exists(pid):
                        return True
                    else:
                        # PID文件存在但进程不存在，删除PID文件
                        pid_file.unlink()
                        return False
                        
                except (ValueError, FileNotFoundError):
                    # PID文件格式错误，删除它
                    pid_file.unlink()
                    return False
            
            return False
            
        except ImportError:
            # 没有psutil，简化检查
            return Path("webmon.pid").exists()
        except Exception as e:
            self.logger.warning(f"检查服务状态失败: {e}")
            return False
    
    def _create_pid_file(self) -> bool:
        """创建PID文件"""
        try:
            pid_file = Path("webmon.pid")
            
            # 检查是否已存在
            if pid_file.exists():
                self.logger.warning("PID文件已存在")
                return False
            
            # 写入当前进程PID
            with open(pid_file, 'w') as f:
                f.write(str(os.getpid()))
            
            self.logger.info(f"创建PID文件: {pid_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"创建PID文件失败: {e}")
            return False
    
    def _daemonize(self):
        """守护进程化"""
        try:
            self.logger.info("正在守护进程化...")

            # 保存当前工作目录
            original_cwd = os.getcwd()

            # 第一次fork
            try:
                pid = os.fork()
                if pid > 0:
                    # 父进程退出
                    sys.exit(0)
            except OSError as e:
                self.logger.error(f"第一次fork失败: {e}")
                raise

            # 脱离父进程环境
            os.setsid()
            os.umask(0)
            
            # 第二次fork
            try:
                pid = os.fork()
                if pid > 0:
                    # 父进程退出
                    sys.exit(0)
            except OSError as e:
                self.logger.error(f"第二次fork失败: {e}")
                raise

            # 恢复到原始工作目录（而不是切换到根目录）
            # 这样可以正确访问相对路径的配置文件和日志
            try:
                os.chdir(original_cwd)
                self.logger.info(f"恢复工作目录: {original_cwd}")
            except Exception as e:
                self.logger.error(f"恢复工作目录失败: {e}")
                raise

            # 重定向标准文件描述符
            sys.stdout.flush()
            sys.stderr.flush()

            # 关闭文件描述符
            try:
                with open('/dev/null', 'r') as si:
                    os.dup2(si.fileno(), sys.stdin.fileno())
                with open('/dev/null', 'w') as so:
                    os.dup2(so.fileno(), sys.stdout.fileno())
                with open('/dev/null', 'w') as se:
                    os.dup2(se.fileno(), sys.stderr.fileno())
            except Exception as e:
                self.logger.warning(f"重定向文件描述符失败: {e}")

            self.logger.info("守护进程化完成")
            
        except Exception as e:
            self.logger.error(f"守护进程化失败: {e}")
            raise
    
    def _setup_signal_handlers(self):
        """设置信号处理"""
        try:
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
            
            self.logger.info("信号处理程序设置完成")
            
        except Exception as e:
            self.logger.warning(f"设置信号处理程序失败: {e}")
    
    def _signal_handler(self, signum, frame):
        """信号处理程序"""
        self.logger.info(f"收到信号 {signum}，准备停止服务...")
        self._shutdown_event.set()
    
    async def _wait_for_shutdown(self):
        """等待关闭信号"""
        try:
            self.logger.info("服务正在运行，按 Ctrl+C 停止...")
            
            while not self._shutdown_event.is_set():
                await asyncio.sleep(1)
            
            self.logger.info("收到关闭信号，正在停止服务...")
            print("\n⏹️  正在停止监控服务...")
            
        except Exception as e:
            self.logger.error(f"等待关闭信号时出错: {e}")
    
    async def _show_status(self):
        """显示状态信息"""
        try:
            if not self.scheduler:
                return
            
            status = self.scheduler.get_status()
            
            print("\n📊 监控服务状态")
            print("=" * 40)
            print(f"🔄 运行状态: {'运行中' if status['is_running'] else '已停止'}")
            print(f"📝 总任务数: {status['total_tasks']}")
            print(f"✅ 启用任务: {status['enabled_tasks']}")
            print(f"🎯 运行中任务: {status['running_tasks']}")
            print(f"⏳ 队列任务: {status['queued_tasks']}")
            print(f"⏱️  运行时间: {self._format_uptime(status['uptime'])}")
            print(f"📈 总执行次数: {status['stats']['total_executions']}")
            print(f"✨ 成功次数: {status['stats']['successful_executions']}")
            print(f"🔄 变化次数: {status['stats']['total_changes']}")
            print("=" * 40)
            
        except Exception as e:
            self.logger.warning(f"显示状态信息失败: {e}")
    
    def _format_uptime(self, seconds: float) -> str:
        """格式化运行时间"""
        if seconds < 60:
            return f"{int(seconds)}秒"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}分{secs}秒"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}小时{minutes}分钟"
    
    def _get_config_manager(self):
        """获取配置管理器"""
        config_path = getattr(self.args, 'config', 'config/config.json')
        env_path = getattr(self.args, 'env', '.env')
        
        # 创建配置管理器并指定配置目录
        config_dir = Path(config_path).parent
        config_manager = ConfigManager(config_dir)
        
        # 设置JSON配置文件路径
        config_manager.json_file = Path(config_path)
        config_manager.json_config.file_path = Path(config_path)
        
        # 设置环境变量文件路径
        if hasattr(config_manager, 'env_config'):
            config_manager.env_config.env_file = Path(env_path)
        
        # 重新加载配置
        config_manager._load_configs()
        
        return config_manager
    
    def validate_args(self) -> bool:
        """验证参数"""
        # 验证守护进程模式
        daemon_mode = getattr(self.args, 'daemon', False)
        if daemon_mode and not hasattr(os, 'fork'):
            print("❌ 错误: 当前系统不支持守护进程模式")
            return False
        
        # 验证特定任务
        specific_task = getattr(self.args, 'task', None)
        if specific_task and not specific_task.strip():
            print("❌ 错误: 任务ID或名称不能为空")
            return False
        
        return True
    
    def format_output(self, result: bool, format_type: str = 'text') -> str:
        """格式化输出"""
        import json
        
        if format_type == 'json':
            return json.dumps({
                "success": result,
                "message": "监控服务启动成功" if result else "监控服务启动失败",
                "daemon_mode": getattr(self.args, 'daemon', False),
                "specific_task": getattr(self.args, 'task', None)
            }, ensure_ascii=False, indent=2)
        else:
            return ""