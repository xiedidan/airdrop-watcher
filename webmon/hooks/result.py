"""
Hook 执行结果数据模型

记录 Hook 脚本的执行结果。
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, Any
import json
import uuid


@dataclass
class HookResult:
    """
    Hook 执行结果数据模型

    用于记录单次 Hook 执行的完整结果信息。

    Attributes:
        id: 执行记录唯一标识
        hook_name: Hook 名称
        trigger: 触发点
        task_id: 关联的任务 ID
        success: 是否执行成功
        exit_code: 脚本退出码
        stdout: 标准输出内容
        stderr: 标准错误输出
        execution_time: 执行耗时（秒）
        started_at: 执行开始时间
        finished_at: 执行结束时间
        error_message: 错误信息（如果有）
        retry_count: 重试次数
        metadata: 额外元数据
    """

    # 必需字段
    hook_name: str
    trigger: str
    task_id: str

    # 执行结果字段
    success: bool = False
    exit_code: Optional[int] = None
    stdout: str = ""
    stderr: str = ""
    execution_time: float = 0.0  # 秒

    # 时间戳
    started_at: datetime = field(default_factory=datetime.now)
    finished_at: Optional[datetime] = None

    # 错误处理
    error_message: Optional[str] = None
    retry_count: int = 0

    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)

    # 唯一标识
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def mark_success(self, exit_code: int = 0, stdout: str = "", stderr: str = ""):
        """标记执行成功"""
        self.success = True
        self.exit_code = exit_code
        self.stdout = self._truncate_output(stdout)
        self.stderr = self._truncate_output(stderr)
        self.finished_at = datetime.now()
        self.execution_time = (self.finished_at - self.started_at).total_seconds()

    def mark_failure(
        self,
        error_message: str,
        exit_code: Optional[int] = None,
        stdout: str = "",
        stderr: str = ""
    ):
        """标记执行失败"""
        self.success = False
        self.exit_code = exit_code
        self.error_message = error_message
        self.stdout = self._truncate_output(stdout)
        self.stderr = self._truncate_output(stderr)
        self.finished_at = datetime.now()
        self.execution_time = (self.finished_at - self.started_at).total_seconds()

    def mark_timeout(self, timeout_seconds: int):
        """标记执行超时"""
        self.mark_failure(
            error_message=f"执行超时（超过 {timeout_seconds} 秒）",
            exit_code=-1
        )

    def increment_retry(self):
        """增加重试次数"""
        self.retry_count += 1
        # 重置开始时间
        self.started_at = datetime.now()
        self.finished_at = None
        self.execution_time = 0.0

    @staticmethod
    def _truncate_output(output: str, max_length: int = 10000) -> str:
        """截断输出内容，避免过长"""
        if len(output) > max_length:
            return output[:max_length] + f"\n... [已截断，总长度: {len(output)}]"
        return output

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'hook_name': self.hook_name,
            'trigger': self.trigger,
            'task_id': self.task_id,
            'success': self.success,
            'exit_code': self.exit_code,
            'stdout': self.stdout,
            'stderr': self.stderr,
            'execution_time': self.execution_time,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'finished_at': self.finished_at.isoformat() if self.finished_at else None,
            'error_message': self.error_message,
            'retry_count': self.retry_count,
            'metadata': self.metadata.copy(),
        }

    def to_json(self) -> str:
        """转换为 JSON 字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HookResult':
        """从字典创建实例"""
        # 解析时间字段
        started_at = data.get('started_at')
        if isinstance(started_at, str):
            started_at = datetime.fromisoformat(started_at)
        elif started_at is None:
            started_at = datetime.now()

        finished_at = data.get('finished_at')
        if isinstance(finished_at, str):
            finished_at = datetime.fromisoformat(finished_at)

        return cls(
            id=data.get('id', str(uuid.uuid4())[:8]),
            hook_name=data.get('hook_name', ''),
            trigger=data.get('trigger', ''),
            task_id=data.get('task_id', ''),
            success=data.get('success', False),
            exit_code=data.get('exit_code'),
            stdout=data.get('stdout', ''),
            stderr=data.get('stderr', ''),
            execution_time=data.get('execution_time', 0.0),
            started_at=started_at,
            finished_at=finished_at,
            error_message=data.get('error_message'),
            retry_count=data.get('retry_count', 0),
            metadata=data.get('metadata', {}),
        )

    @classmethod
    def from_json(cls, json_str: str) -> 'HookResult':
        """从 JSON 字符串创建实例"""
        data = json.loads(json_str)
        return cls.from_dict(data)

    @property
    def is_timeout(self) -> bool:
        """是否超时"""
        return self.error_message is not None and "超时" in self.error_message

    @property
    def has_output(self) -> bool:
        """是否有输出"""
        return bool(self.stdout.strip() or self.stderr.strip())

    @property
    def duration_str(self) -> str:
        """执行时间的可读字符串"""
        if self.execution_time < 1:
            return f"{self.execution_time * 1000:.0f}ms"
        return f"{self.execution_time:.2f}s"

    def __str__(self) -> str:
        """字符串表示"""
        status = "成功" if self.success else "失败"
        return (
            f"HookResult[{self.hook_name}@{self.trigger}] "
            f"({status}, {self.duration_str}, task={self.task_id})"
        )
