"""
Hook 脚本执行器

负责执行 Shell 和 Python 脚本，处理超时、错误和资源限制。
"""

import asyncio
import json
import os
import signal
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

from webmon.utils.logger import get_logger
from .config import HookConfig
from .result import HookResult
from .triggers import HookTrigger
from .validator import ScriptValidator


# 敏感环境变量名称列表（不传递给脚本）
SENSITIVE_ENV_VARS = {
    'AI_API_KEY',
    'OPENAI_API_KEY',
    'DEEPSEEK_API_KEY',
    'DISCORD_WEBHOOK_URL',
    'TELEGRAM_BOT_TOKEN',
    'PUSHPLUS_TOKEN',
    'FEISHU_WEBHOOK_URL',
    'DATABASE_PASSWORD',
    'SECRET_KEY',
    'API_SECRET',
}

# 资源限制常量（固定值，不可配置）
RESOURCE_LIMITS = {
    'cpu_time': 300,       # CPU 时间限制（秒）
    'memory_mb': 512,      # 内存限制（MB）
    'max_fds': 256,        # 最大文件描述符数
    'max_processes': 16,   # 最大子进程数
}


class HookExecutor:
    """
    Hook 脚本执行器

    负责执行单个 Hook 脚本，包括：
    - 构建执行环境（环境变量、工作目录）
    - 准备 stdin JSON 输入数据
    - 启动子进程执行脚本
    - 处理超时和错误
    - 收集 stdout/stderr 输出
    """

    def __init__(self, project_root: Optional[Path] = None):
        """
        初始化执行器

        Args:
            project_root: 项目根目录路径，默认为当前工作目录
        """
        self.logger = get_logger(__name__)
        self.project_root = project_root or Path.cwd()
        self.data_dir = self.project_root / "data"

        # 脚本路径验证器
        self.validator = ScriptValidator(project_root=self.project_root)

    async def execute(
        self,
        hook_config: HookConfig,
        trigger: str,
        context: Dict[str, Any]
    ) -> HookResult:
        """
        执行 Hook 脚本

        Args:
            hook_config: Hook 配置
            trigger: 触发点名称
            context: 执行上下文（包含任务信息、变化详情等）

        Returns:
            HookResult: 执行结果
        """
        # 创建结果对象
        result = HookResult(
            hook_name=hook_config.name,
            trigger=trigger,
            task_id=context.get('task', {}).get('id', 'unknown')
        )

        try:
            # 验证脚本路径安全性
            validation_result = self.validator.validate(hook_config.script)
            if not validation_result.valid:
                result.mark_failure(f"脚本路径验证失败: {validation_result.error_message}")
                self.logger.warning(
                    f"Hook {hook_config.name} 脚本路径验证失败: "
                    f"{validation_result.error_message}"
                )
                return result

            # 使用验证后的路径
            script_path = validation_result.resolved_path

            # 构建执行环境
            env = self._build_environment(hook_config, trigger, context)

            # 准备 stdin JSON 数据
            stdin_data = self._build_stdin_data(trigger, context)

            # 确定工作目录
            working_dir = self._get_working_dir(hook_config, script_path)

            # 构建执行命令
            cmd = self._build_command(hook_config, script_path)

            self.logger.info(f"执行 Hook: {hook_config.name} ({trigger})")
            self.logger.debug(f"脚本路径: {script_path}")
            self.logger.debug(f"工作目录: {working_dir}")

            # 执行脚本
            stdout, stderr, exit_code = await self._run_process(
                cmd=cmd,
                env=env,
                cwd=working_dir,
                stdin_data=stdin_data,
                timeout=hook_config.timeout
            )

            # 根据退出码判断成功/失败
            if exit_code == 0:
                result.mark_success(exit_code, stdout, stderr)
                self.logger.info(
                    f"Hook {hook_config.name} 执行成功 "
                    f"(耗时: {result.duration_str})"
                )
            else:
                result.mark_failure(
                    f"脚本返回非零退出码: {exit_code}",
                    exit_code, stdout, stderr
                )
                self.logger.warning(
                    f"Hook {hook_config.name} 执行失败: 退出码 {exit_code}"
                )

        except asyncio.TimeoutError:
            result.mark_timeout(hook_config.timeout)
            self.logger.error(
                f"Hook {hook_config.name} 执行超时 "
                f"(超过 {hook_config.timeout} 秒)"
            )

        except Exception as e:
            result.mark_failure(f"执行异常: {str(e)}")
            self.logger.error(f"Hook {hook_config.name} 执行异常: {e}")

        return result

    async def execute_with_retry(
        self,
        hook_config: HookConfig,
        trigger: str,
        context: Dict[str, Any]
    ) -> HookResult:
        """
        带重试机制的执行

        Args:
            hook_config: Hook 配置
            trigger: 触发点名称
            context: 执行上下文

        Returns:
            HookResult: 最终执行结果
        """
        result = await self.execute(hook_config, trigger, context)

        # 如果成功或不需要重试，直接返回
        if result.success or hook_config.max_retries <= 0:
            return result

        # 检查是否为可重试错误
        if not self._is_retryable_error(result):
            self.logger.debug(f"Hook {hook_config.name} 错误不可重试")
            return result

        # 执行重试
        retry_count = 0
        while retry_count < hook_config.max_retries:
            retry_count += 1
            result.increment_retry()

            # 指数退避等待
            wait_time = 2 ** (retry_count - 1)  # 1, 2, 4, 8...
            self.logger.info(
                f"Hook {hook_config.name} 第 {retry_count} 次重试 "
                f"(等待 {wait_time} 秒)"
            )
            await asyncio.sleep(wait_time)

            # 重新执行
            result = await self.execute(hook_config, trigger, context)
            result.retry_count = retry_count

            if result.success:
                self.logger.info(
                    f"Hook {hook_config.name} 重试成功 (第 {retry_count} 次)"
                )
                return result

        self.logger.error(
            f"Hook {hook_config.name} 重试 {retry_count} 次后仍然失败"
        )
        return result

    def _resolve_script_path(self, script: str) -> Path:
        """解析脚本路径"""
        script_path = Path(script)

        # 如果是绝对路径，直接使用
        if script_path.is_absolute():
            return script_path

        # 相对路径：相对于项目根目录
        return self.project_root / script

    def _build_environment(
        self,
        hook_config: HookConfig,
        trigger: str,
        context: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        构建执行环境变量

        Args:
            hook_config: Hook 配置
            trigger: 触发点名称
            context: 执行上下文

        Returns:
            环境变量字典
        """
        # 从当前环境复制（过滤敏感变量）
        env = {}
        for key, value in os.environ.items():
            if key not in SENSITIVE_ENV_VARS:
                env[key] = value

        # 任务相关
        task = context.get('task', {})
        env['WEBMON_TASK_ID'] = str(task.get('id', ''))
        env['WEBMON_TASK_NAME'] = str(task.get('name', ''))
        env['WEBMON_TASK_URL'] = str(task.get('url', ''))
        env['WEBMON_TASK_DESCRIPTION'] = str(task.get('description', ''))

        # 变化相关
        change = context.get('change', {})
        env['WEBMON_CHANGE_DETECTED'] = 'true' if change.get('detected', False) else 'false'
        env['WEBMON_CHANGE_TYPE'] = str(change.get('type', ''))
        env['WEBMON_CHANGE_TIME'] = str(change.get('time', datetime.now().isoformat()))
        env['WEBMON_SIMILARITY'] = str(change.get('similarity', ''))

        # 执行上下文
        env['WEBMON_HOOK_NAME'] = hook_config.name
        env['WEBMON_HOOK_TRIGGER'] = trigger
        env['WEBMON_PROJECT_ROOT'] = str(self.project_root)
        env['WEBMON_DATA_DIR'] = str(self.data_dir)

        # 添加用户自定义环境变量
        for key, value in hook_config.env.items():
            # 确保不覆盖敏感变量
            if key not in SENSITIVE_ENV_VARS:
                env[key] = str(value)

        return env

    def _build_stdin_data(
        self,
        trigger: str,
        context: Dict[str, Any]
    ) -> str:
        """
        构建 stdin JSON 数据

        Args:
            trigger: 触发点名称
            context: 执行上下文

        Returns:
            JSON 字符串
        """
        # 截断内容字段，避免数据量过大
        max_content_length = 2000

        data = {
            'trigger': trigger,
            'timestamp': datetime.now().isoformat(),
            'task': context.get('task', {}),
            'change': self._truncate_change_data(
                context.get('change', {}),
                max_content_length
            ),
            'ai_analysis': context.get('ai_analysis'),
            'notification': context.get('notification', {}),
        }

        return json.dumps(data, ensure_ascii=False, default=str)

    def _truncate_change_data(
        self,
        change: Dict[str, Any],
        max_length: int
    ) -> Dict[str, Any]:
        """截断变化数据中的长文本字段"""
        result = change.copy()

        # 截断内容字段
        for key in ['old_content', 'new_content', 'diff', 'summary']:
            if key in result and isinstance(result[key], str):
                if len(result[key]) > max_length:
                    result[key] = result[key][:max_length] + '...[已截断]'

        return result

    def _get_working_dir(
        self,
        hook_config: HookConfig,
        script_path: Path
    ) -> Path:
        """确定工作目录"""
        if hook_config.working_dir:
            wd = Path(hook_config.working_dir)
            if wd.is_absolute():
                return wd
            return self.project_root / wd

        # 默认使用脚本所在目录
        return script_path.parent

    def _build_command(
        self,
        hook_config: HookConfig,
        script_path: Path
    ) -> List[str]:
        """
        构建执行命令

        Args:
            hook_config: Hook 配置
            script_path: 脚本绝对路径

        Returns:
            命令参数列表
        """
        if hook_config.type == 'python':
            # Python 脚本使用当前 Python 解释器
            cmd = [sys.executable, str(script_path)]
        else:
            # Shell 脚本直接执行
            cmd = [str(script_path)]

        # 添加额外参数
        cmd.extend(hook_config.args)

        return cmd

    async def _run_process(
        self,
        cmd: List[str],
        env: Dict[str, str],
        cwd: Path,
        stdin_data: str,
        timeout: int
    ) -> tuple:
        """
        执行子进程

        Args:
            cmd: 命令参数列表
            env: 环境变量
            cwd: 工作目录
            stdin_data: stdin 输入数据
            timeout: 超时时间（秒）

        Returns:
            (stdout, stderr, exit_code) 元组
        """
        # 设置资源限制的预执行函数（仅 Linux）
        preexec_fn = None
        if sys.platform.startswith('linux'):
            preexec_fn = self._set_resource_limits

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
                cwd=str(cwd),
                preexec_fn=preexec_fn,
            )

            # 带超时的执行
            try:
                stdout_bytes, stderr_bytes = await asyncio.wait_for(
                    process.communicate(input=stdin_data.encode('utf-8')),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                # 超时处理：先 SIGTERM，再 SIGKILL
                await self._terminate_process(process, timeout=5)
                raise

            stdout = stdout_bytes.decode('utf-8', errors='replace')
            stderr = stderr_bytes.decode('utf-8', errors='replace')
            exit_code = process.returncode

            return stdout, stderr, exit_code

        except asyncio.TimeoutError:
            raise
        except Exception as e:
            self.logger.error(f"执行子进程失败: {e}")
            raise

    async def _terminate_process(self, process, timeout: int = 5):
        """
        优雅终止进程

        先发送 SIGTERM，等待指定时间后发送 SIGKILL
        """
        try:
            # 发送 SIGTERM
            process.terminate()

            try:
                await asyncio.wait_for(process.wait(), timeout=timeout)
            except asyncio.TimeoutError:
                # SIGTERM 超时，发送 SIGKILL
                self.logger.warning("进程未响应 SIGTERM，强制终止")
                process.kill()
                await process.wait()

        except ProcessLookupError:
            # 进程已经结束
            pass

    def _set_resource_limits(self):
        """
        设置资源限制（仅 Linux）

        在子进程中调用，设置 CPU 时间、内存等限制
        """
        try:
            import resource

            # CPU 时间限制
            resource.setrlimit(
                resource.RLIMIT_CPU,
                (RESOURCE_LIMITS['cpu_time'], RESOURCE_LIMITS['cpu_time'])
            )

            # 内存限制（软限制和硬限制）
            memory_bytes = RESOURCE_LIMITS['memory_mb'] * 1024 * 1024
            resource.setrlimit(
                resource.RLIMIT_AS,
                (memory_bytes, memory_bytes)
            )

            # 文件描述符限制
            resource.setrlimit(
                resource.RLIMIT_NOFILE,
                (RESOURCE_LIMITS['max_fds'], RESOURCE_LIMITS['max_fds'])
            )

            # 子进程数限制
            resource.setrlimit(
                resource.RLIMIT_NPROC,
                (RESOURCE_LIMITS['max_processes'], RESOURCE_LIMITS['max_processes'])
            )

        except Exception as e:
            # 资源限制设置失败不应阻止脚本执行
            # 但需要记录日志（在主进程中已无法访问 logger）
            print(f"设置资源限制失败: {e}", file=sys.stderr)

    def _is_retryable_error(self, result: HookResult) -> bool:
        """判断错误是否可重试"""
        # 超时可重试
        if result.is_timeout:
            return True

        # 非零退出码可重试（除了特定错误码）
        if result.exit_code is not None and result.exit_code != 0:
            # 权限错误（126、127）不重试
            if result.exit_code in (126, 127):
                return False
            return True

        # 其他错误（如脚本不存在、权限不足）不重试
        return False
