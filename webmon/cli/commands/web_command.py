#!/usr/bin/env python3
"""
启动 WebUI 服务命令
"""

import os
import sys
import signal
import webbrowser
from argparse import Namespace
from pathlib import Path

from webmon.cli.command import Command
from webmon.utils.logger import get_logger


class WebCommand(Command):
    """启动 WebUI 服务命令"""

    def __init__(self, args: Namespace):
        super().__init__(args)
        self.logger = get_logger(__name__)

    def execute(self) -> bool:
        """执行 web 命令"""
        try:
            self.logger.info("执行启动 WebUI 服务命令")

            # 获取参数（优先使用命令行参数，其次是环境变量，最后是默认值）
            default_port = int(os.getenv('WEB_PORT', '8020'))
            default_host = os.getenv('WEB_HOST', '0.0.0.0')

            port = getattr(self.args, 'port', default_port)
            host = getattr(self.args, 'host', default_host)
            no_browser = getattr(self.args, 'no_browser', False)
            reload_mode = getattr(self.args, 'reload', False)

            # 参数验证
            if not self._validate_port(port):
                return False

            print(f"🌐 正在启动 WebMon WebUI 服务...")
            print(f"   地址: http://{host}:{port}")

            # 打开浏览器
            if not no_browser:
                self._open_browser(host, port)

            # 启动 uvicorn 服务器
            return self._start_server(host, port, reload_mode)

        except KeyboardInterrupt:
            self.logger.info("用户中断操作")
            print("\n⏹️  WebUI 服务已停止")
            return True
        except Exception as e:
            self.logger.error(f"启动 WebUI 服务失败: {e}")
            print(f"❌ 启动 WebUI 服务失败: {e}")
            return False

    def _validate_port(self, port: int) -> bool:
        """验证端口号"""
        if port < 1 or port > 65535:
            print(f"❌ 无效的端口号: {port} (应在 1-65535 范围内)")
            return False

        if port < 1024 and os.geteuid() != 0:
            print(f"⚠️  端口 {port} 需要 root 权限")

        return True

    def _open_browser(self, host: str, port: int):
        """打开浏览器"""
        import threading
        import time

        def open_browser_delayed():
            # 延迟 1.5 秒等待服务器启动
            time.sleep(1.5)
            url = f"http://127.0.0.1:{port}"
            try:
                webbrowser.open(url)
                self.logger.info(f"已在浏览器中打开: {url}")
            except Exception as e:
                self.logger.warning(f"无法打开浏览器: {e}")

        # 在后台线程中打开浏览器
        thread = threading.Thread(target=open_browser_delayed, daemon=True)
        thread.start()

    def _start_server(self, host: str, port: int, reload: bool) -> bool:
        """启动 uvicorn 服务器"""
        try:
            import uvicorn

            print(f"\n✅ WebMon WebUI 服务已启动!")
            print(f"   访问地址: http://127.0.0.1:{port}")
            print(f"   API 文档: http://127.0.0.1:{port}/docs")
            print(f"\n   按 Ctrl+C 停止服务\n")

            # 运行 uvicorn
            uvicorn.run(
                "webmon.web.app:app",
                host=host,
                port=port,
                reload=reload,
                log_level="info",
                access_log=True,
            )

            return True

        except ImportError:
            print("❌ 缺少依赖: uvicorn")
            print("   请运行: pip install uvicorn")
            return False
        except Exception as e:
            self.logger.error(f"启动服务器失败: {e}")
            print(f"❌ 启动服务器失败: {e}")
            return False

    def validate_args(self) -> bool:
        """验证参数"""
        default_port = int(os.getenv('WEB_PORT', '8020'))
        port = getattr(self.args, 'port', default_port)
        return self._validate_port(port)
