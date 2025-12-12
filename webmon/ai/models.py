"""
AI分析服务数据模型
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class AIConfig:
    """AI配置模型"""

    # 是否启用AI分析
    enabled: bool = False

    # API配置
    api_url: str = "https://api.deepseek.com/v1"
    api_key: str = ""
    model: str = "deepseek-reasoner"

    # 生成参数
    max_tokens: int = 2048
    temperature: float = 0.7
    timeout: int = 60  # 秒

    # 提示词配置
    system_prompt: str = field(default_factory=lambda: (
        "你是一个专业的网页内容变化分析助手。你的任务是：\n"
        "1. 分析网页内容的变化\n"
        "2. 提取用户可能关注的关键信息\n"
        "3. 用简洁的自然语言总结变化要点\n"
        "4. 如果变化涉及价格、时间、状态等重要信息，请特别指出\n\n"
        "请用中文回复，保持简洁（不超过200字），重点突出关键变化。"
    ))

    user_prompt_template: str = field(default_factory=lambda: (
        "## 监控任务信息\n"
        "- 任务名称：{task_name}\n"
        "- 监控URL：{url}\n"
        "- 任务描述：{description}\n\n"
        "## 检测到的变化内容\n"
        "{changes}\n\n"
        "请分析以上变化，提取关键信息并生成简洁的摘要。"
    ))

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'enabled': self.enabled,
            'api_url': self.api_url,
            'api_key': self.api_key,
            'model': self.model,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature,
            'timeout': self.timeout,
            'system_prompt': self.system_prompt,
            'user_prompt_template': self.user_prompt_template,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AIConfig':
        """从字典创建配置"""
        # 创建默认实例以获取默认提示词
        defaults = cls()
        return cls(
            enabled=data.get('enabled', False),
            api_url=data.get('api_url', 'https://api.deepseek.com/v1'),
            api_key=data.get('api_key', ''),
            model=data.get('model', 'deepseek-reasoner'),
            max_tokens=data.get('max_tokens', 2048),
            temperature=data.get('temperature', 0.7),
            timeout=data.get('timeout', 60),
            system_prompt=data.get('system_prompt', defaults.system_prompt),
            user_prompt_template=data.get('user_prompt_template', defaults.user_prompt_template),
        )

    def is_valid(self) -> bool:
        """检查配置是否有效"""
        return bool(self.enabled and self.api_url and self.api_key)


@dataclass
class AIAnalysisResult:
    """AI分析结果模型"""

    # 分析状态
    success: bool = False
    task_id: str = ""

    # 分析结果
    summary: str = ""

    # 调用信息
    model: str = ""
    tokens_used: int = 0
    latency: float = 0.0  # 秒

    # 时间戳
    timestamp: datetime = field(default_factory=datetime.now)

    # 错误信息
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'success': self.success,
            'task_id': self.task_id,
            'summary': self.summary,
            'model': self.model,
            'tokens_used': self.tokens_used,
            'latency': self.latency,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'error_message': self.error_message,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AIAnalysisResult':
        """从字典创建结果"""
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        return cls(
            success=data.get('success', False),
            task_id=data.get('task_id', ''),
            summary=data.get('summary', ''),
            model=data.get('model', ''),
            tokens_used=data.get('tokens_used', 0),
            latency=data.get('latency', 0.0),
            timestamp=timestamp or datetime.now(),
            error_message=data.get('error_message'),
        )

    @classmethod
    def create_error(cls, task_id: str, error_message: str, model: str = "") -> 'AIAnalysisResult':
        """创建错误结果"""
        return cls(
            success=False,
            task_id=task_id,
            summary="",
            model=model,
            error_message=error_message,
            timestamp=datetime.now(),
        )

    @classmethod
    def create_success(
        cls,
        task_id: str,
        summary: str,
        model: str,
        tokens_used: int = 0,
        latency: float = 0.0
    ) -> 'AIAnalysisResult':
        """创建成功结果"""
        return cls(
            success=True,
            task_id=task_id,
            summary=summary,
            model=model,
            tokens_used=tokens_used,
            latency=latency,
            timestamp=datetime.now(),
        )
