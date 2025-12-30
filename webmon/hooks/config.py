"""
Hook 配置数据模型

定义单个 Hook 的配置结构。
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import json


@dataclass
class HookConfig:
    """
    Hook 配置数据模型

    用于表示单个 Hook 的完整配置信息。

    Attributes:
        name: Hook 名称，用于日志和识别
        type: 脚本类型，支持 'shell' 或 'python'
        script: 脚本路径，支持绝对路径或相对于项目根目录
        enabled: 是否启用此 Hook
        timeout: 执行超时时间（秒）
        async_exec: 是否异步执行（不阻塞后续流程）
        args: 额外的命令行参数列表
        env: 额外的环境变量
        condition: 执行条件表达式
        working_dir: 工作目录
        max_retries: 失败时最大重试次数
    """

    # 必需字段
    name: str
    type: str  # 'shell' 或 'python'
    script: str

    # 可选字段（带默认值）
    enabled: bool = True
    timeout: int = 30  # 秒
    async_exec: bool = True  # 默认异步执行
    args: List[str] = field(default_factory=list)
    env: Dict[str, str] = field(default_factory=dict)
    condition: Optional[str] = None
    working_dir: Optional[str] = None
    max_retries: int = 0

    # 内部标识
    _is_global: bool = field(default=False, repr=False)

    def __post_init__(self):
        """初始化后验证"""
        self._validate()

    def _validate(self):
        """验证配置有效性"""
        # 验证名称
        if not self.name or not self.name.strip():
            raise ValueError("Hook 名称不能为空")

        # 验证类型
        valid_types = ('shell', 'python')
        if self.type not in valid_types:
            raise ValueError(f"Hook 类型必须是 {valid_types} 之一，当前: {self.type}")

        # 验证脚本路径
        if not self.script or not self.script.strip():
            raise ValueError("脚本路径不能为空")

        # 验证超时时间范围
        if self.timeout < 1:
            raise ValueError("超时时间必须大于 0 秒")
        if self.timeout > 300:
            raise ValueError("超时时间不能超过 300 秒（5分钟）")

        # 验证重试次数
        if self.max_retries < 0:
            raise ValueError("重试次数不能为负数")
        if self.max_retries > 5:
            raise ValueError("重试次数不能超过 5 次")

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'type': self.type,
            'script': self.script,
            'enabled': self.enabled,
            'timeout': self.timeout,
            'async': self.async_exec,
            'args': self.args.copy(),
            'env': self.env.copy(),
            'condition': self.condition,
            'working_dir': self.working_dir,
            'max_retries': self.max_retries,
        }

    def to_json(self) -> str:
        """转换为 JSON 字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], is_global: bool = False) -> 'HookConfig':
        """
        从字典创建 HookConfig 实例

        Args:
            data: 配置字典
            is_global: 是否为全局 Hook

        Returns:
            HookConfig 实例
        """
        return cls(
            name=data.get('name', ''),
            type=data.get('type', 'shell'),
            script=data.get('script', ''),
            enabled=data.get('enabled', True),
            timeout=data.get('timeout', 30),
            async_exec=data.get('async', True),
            args=data.get('args', []),
            env=data.get('env', {}),
            condition=data.get('condition'),
            working_dir=data.get('working_dir'),
            max_retries=data.get('max_retries', 0),
            _is_global=is_global,
        )

    @classmethod
    def from_json(cls, json_str: str, is_global: bool = False) -> 'HookConfig':
        """从 JSON 字符串创建实例"""
        data = json.loads(json_str)
        return cls.from_dict(data, is_global)

    @property
    def is_global(self) -> bool:
        """是否为全局 Hook"""
        return self._is_global

    @property
    def is_sync(self) -> bool:
        """是否同步执行"""
        return not self.async_exec

    def __str__(self) -> str:
        """字符串表示"""
        status = "启用" if self.enabled else "禁用"
        exec_mode = "异步" if self.async_exec else "同步"
        scope = "全局" if self._is_global else "任务级"
        return f"Hook[{self.name}] ({self.type}, {exec_mode}, {scope}, {status})"
