"""
AI分析服务

提供基于大语言模型的网页变化内容智能分析功能。
支持DeepSeek R1及OpenAI兼容API。
"""

import os
import time
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime

from webmon.ai.models import AIConfig, AIAnalysisResult
from webmon.utils.logger import get_logger


class AIAnalysisService:
    """AI分析服务类"""

    def __init__(self, config: Optional[AIConfig] = None):
        """
        初始化AI分析服务

        Args:
            config: AI配置，如果为None则从环境变量加载
        """
        self.logger = get_logger(__name__)
        self._config = config
        self._http_client = None

    @property
    def config(self) -> AIConfig:
        """获取配置，延迟加载"""
        if self._config is None:
            self._config = self._load_config_from_env()
        return self._config

    def update_config(self, config: AIConfig):
        """更新配置"""
        self._config = config
        self.logger.info(f"AI配置已更新: model={config.model}, enabled={config.enabled}")

    def _load_config_from_env(self) -> AIConfig:
        """从环境变量加载配置"""
        return AIConfig(
            enabled=os.getenv('AI_ENABLED', 'false').lower() in ('true', '1', 'yes'),
            api_url=os.getenv('AI_API_URL', 'https://api.deepseek.com/v1'),
            api_key=os.getenv('AI_API_KEY', ''),
            model=os.getenv('AI_MODEL', 'deepseek-reasoner'),
            max_tokens=int(os.getenv('AI_MAX_TOKENS', '2048')),
            temperature=float(os.getenv('AI_TEMPERATURE', '0.7')),
            timeout=int(os.getenv('AI_TIMEOUT', '60')),
        )

    def is_enabled(self) -> bool:
        """检查AI分析是否启用"""
        return self.config.is_valid()

    def render_prompt(
        self,
        template: str,
        task_name: str = "",
        url: str = "",
        description: str = "",
        changes: str = "",
        old_content: str = "",
        new_content: str = ""
    ) -> str:
        """
        渲染提示词模板

        支持的占位符:
        - {task_name}: 任务名称
        - {url}: 监控URL
        - {description}: 任务描述
        - {changes}: 变动内容
        - {old_content}: 旧内容摘要
        - {new_content}: 新内容摘要
        """
        prompt = template
        prompt = prompt.replace('{task_name}', task_name or '未命名任务')
        prompt = prompt.replace('{url}', url or '')
        prompt = prompt.replace('{description}', description or '无')
        prompt = prompt.replace('{changes}', changes or '无变化信息')
        prompt = prompt.replace('{old_content}', old_content or '')
        prompt = prompt.replace('{new_content}', new_content or '')
        return prompt

    def format_changes(self, changes: Dict[str, Any]) -> str:
        """
        格式化变化内容为可读文本

        Args:
            changes: 变化详情字典

        Returns:
            格式化后的文本
        """
        if not changes:
            return "无明显变化"

        lines = []

        # 处理diff内容
        if 'diff' in changes:
            diff = changes['diff']
            if isinstance(diff, str):
                lines.append(f"内容差异:\n{diff[:2000]}")  # 限制长度
            elif isinstance(diff, dict):
                for key, value in diff.items():
                    lines.append(f"- {key}: {value}")

        # 处理added/removed内容
        if 'added' in changes:
            added = changes['added']
            if added:
                lines.append(f"新增内容:\n{added[:1000]}")

        if 'removed' in changes:
            removed = changes['removed']
            if removed:
                lines.append(f"删除内容:\n{removed[:1000]}")

        # 处理similarity
        if 'similarity' in changes:
            lines.append(f"相似度: {changes['similarity']:.2%}")

        # 处理其他字段
        for key, value in changes.items():
            if key in ('diff', 'added', 'removed', 'similarity', 'old_content', 'new_content'):
                continue
            if isinstance(value, dict) and 'old' in value and 'new' in value:
                lines.append(f"- {key}: {value['old']} → {value['new']}")
            elif value:
                lines.append(f"- {key}: {value}")

        return '\n'.join(lines) if lines else "检测到变化但无详细信息"

    async def analyze_changes(
        self,
        task_id: str,
        task_name: str,
        url: str,
        description: str,
        changes: Dict[str, Any]
    ) -> AIAnalysisResult:
        """
        分析变化内容

        Args:
            task_id: 任务ID
            task_name: 任务名称
            url: 监控URL
            description: 任务描述
            changes: 变化详情字典

        Returns:
            AIAnalysisResult: 分析结果
        """
        # 检查是否启用
        if not self.is_enabled():
            self.logger.debug("AI分析未启用或配置无效")
            return AIAnalysisResult.create_error(
                task_id=task_id,
                error_message="AI分析未启用或配置无效"
            )

        start_time = time.time()

        try:
            # 格式化变化内容
            changes_text = self.format_changes(changes)

            # 渲染用户提示词
            user_prompt = self.render_prompt(
                template=self.config.user_prompt_template,
                task_name=task_name,
                url=url,
                description=description,
                changes=changes_text,
                old_content=changes.get('old_content', ''),
                new_content=changes.get('new_content', '')
            )

            # 调用AI API
            result = await self._call_api(
                system_prompt=self.config.system_prompt,
                user_prompt=user_prompt
            )

            latency = time.time() - start_time

            if result['success']:
                self.logger.info(
                    f"AI分析成功: task={task_id}, "
                    f"tokens={result.get('tokens_used', 0)}, "
                    f"latency={latency:.2f}s"
                )
                return AIAnalysisResult.create_success(
                    task_id=task_id,
                    summary=result['content'],
                    model=self.config.model,
                    tokens_used=result.get('tokens_used', 0),
                    latency=latency
                )
            else:
                self.logger.warning(f"AI分析失败: task={task_id}, error={result.get('error')}")
                return AIAnalysisResult.create_error(
                    task_id=task_id,
                    error_message=result.get('error', '未知错误'),
                    model=self.config.model
                )

        except asyncio.TimeoutError:
            latency = time.time() - start_time
            self.logger.error(f"AI分析超时: task={task_id}, timeout={self.config.timeout}s")
            return AIAnalysisResult.create_error(
                task_id=task_id,
                error_message=f"请求超时 ({self.config.timeout}秒)",
                model=self.config.model
            )

        except Exception as e:
            latency = time.time() - start_time
            self.logger.error(f"AI分析异常: task={task_id}, error={e}")
            return AIAnalysisResult.create_error(
                task_id=task_id,
                error_message=str(e),
                model=self.config.model
            )

    async def _call_api(
        self,
        system_prompt: str,
        user_prompt: str
    ) -> Dict[str, Any]:
        """
        调用OpenAI兼容API

        支持: DeepSeek, OpenAI, Azure OpenAI, 通义千问等

        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词

        Returns:
            包含success, content, tokens_used, error的字典
        """
        try:
            import httpx
        except ImportError:
            return {
                'success': False,
                'error': '缺少httpx库，请运行: pip install httpx'
            }

        api_url = self.config.api_url.rstrip('/')
        endpoint = f"{api_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature
        }

        try:
            async with httpx.AsyncClient(timeout=self.config.timeout) as client:
                response = await client.post(
                    endpoint,
                    headers=headers,
                    json=payload
                )

                if response.status_code == 200:
                    data = response.json()
                    content = data['choices'][0]['message']['content']
                    tokens_used = data.get('usage', {}).get('total_tokens', 0)

                    return {
                        'success': True,
                        'content': content,
                        'tokens_used': tokens_used
                    }
                else:
                    error_msg = f"API返回错误: {response.status_code}"
                    try:
                        error_data = response.json()
                        if 'error' in error_data:
                            error_msg = error_data['error'].get('message', error_msg)
                    except Exception:
                        pass

                    return {
                        'success': False,
                        'error': error_msg
                    }

        except httpx.TimeoutException:
            return {
                'success': False,
                'error': f'请求超时 ({self.config.timeout}秒)'
            }
        except httpx.ConnectError as e:
            return {
                'success': False,
                'error': f'连接失败: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'请求异常: {str(e)}'
            }

    def get_fallback_summary(self, changes: Dict[str, Any]) -> str:
        """
        获取降级摘要（AI调用失败时使用）

        Args:
            changes: 变化详情字典

        Returns:
            简单的变化摘要
        """
        if not changes:
            return "检测到页面变化，但无法获取详细信息。"

        # 尝试提取一些基本信息
        parts = []

        if 'similarity' in changes:
            similarity = changes['similarity']
            parts.append(f"相似度: {similarity:.1%}")

        if 'added' in changes and changes['added']:
            added_len = len(changes['added']) if isinstance(changes['added'], str) else 0
            if added_len > 0:
                parts.append(f"新增约{added_len}字符")

        if 'removed' in changes and changes['removed']:
            removed_len = len(changes['removed']) if isinstance(changes['removed'], str) else 0
            if removed_len > 0:
                parts.append(f"删除约{removed_len}字符")

        if parts:
            return "检测到变化: " + ", ".join(parts) + "。（AI分析暂时不可用）"

        change_count = len(changes)
        return f"检测到 {change_count} 处变化。（AI分析暂时不可用）"

    async def test_connection(self) -> Dict[str, Any]:
        """
        测试API连接

        Returns:
            包含success, message, latency的字典
        """
        if not self.config.api_key:
            return {
                'success': False,
                'message': 'API Key未配置',
                'latency': 0
            }

        start_time = time.time()

        result = await self._call_api(
            system_prompt="你是一个测试助手。",
            user_prompt="请回复'连接成功'四个字。"
        )

        latency = time.time() - start_time

        if result['success']:
            return {
                'success': True,
                'message': f"连接成功，模型: {self.config.model}",
                'response': result.get('content', ''),
                'tokens_used': result.get('tokens_used', 0),
                'latency': latency
            }
        else:
            return {
                'success': False,
                'message': result.get('error', '连接失败'),
                'latency': latency
            }
