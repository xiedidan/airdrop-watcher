"""
配置管理命令实现

支持AI配置的查看、启用、禁用和设置
"""

import os
import asyncio
from argparse import Namespace
from typing import Optional

from webmon.cli.command import Command
from webmon.config import ConfigManager
from webmon.ai import AIAnalysisService, AIConfig
from webmon.utils.logger import get_logger


class ConfigCommand(Command):
    """配置管理命令"""

    def __init__(self, args: Namespace):
        super().__init__(args)
        self.logger = get_logger(__name__)
        self.config_manager = ConfigManager()

    def execute(self) -> bool:
        """执行配置命令"""
        try:
            # 获取子命令
            subcommand = getattr(self.args, 'config_subcommand', None)

            if subcommand == 'ai':
                return self._handle_ai_command()
            elif subcommand == 'show':
                return self._show_all_config()
            else:
                # 默认显示帮助
                self._show_help()
                return True

        except Exception as e:
            self.logger.error(f"配置命令执行失败: {e}")
            print(f"❌ 配置命令执行失败: {e}")
            return False

    def _handle_ai_command(self) -> bool:
        """处理AI相关命令"""
        action = getattr(self.args, 'ai_action', None)

        if action == 'enable':
            return self._enable_ai()
        elif action == 'disable':
            return self._disable_ai()
        elif action == 'set':
            return self._set_ai_config()
        elif action == 'test':
            return self._test_ai()
        else:
            # 默认显示AI配置状态
            return self._show_ai_status()

    def _show_ai_status(self) -> bool:
        """显示AI配置状态"""
        ai_config = self.config_manager.get_ai_config()

        print("\n📊 AI分析配置")
        print("=" * 50)

        enabled = ai_config.get('enabled', False)
        status_icon = "✅" if enabled else "❌"
        print(f"状态: {status_icon} {'已启用' if enabled else '已禁用'}")

        print(f"\n🔧 配置详情:")
        print(f"  API地址: {ai_config.get('api_url', '未设置')}")

        # 显示API Key（部分隐藏）
        api_key = ai_config.get('api_key', '')
        if api_key:
            if api_key.startswith('${'):
                # 环境变量占位符，尝试从环境变量获取
                env_var = api_key[2:-1] if api_key.endswith('}') else api_key[2:]
                actual_key = os.getenv(env_var, '')
                if actual_key:
                    masked = actual_key[:8] + '*' * (len(actual_key) - 12) + actual_key[-4:] if len(actual_key) > 12 else '***'
                    print(f"  API Key: {masked} (从环境变量 {env_var})")
                else:
                    print(f"  API Key: ⚠️ 环境变量 {env_var} 未设置")
            else:
                masked = api_key[:8] + '*' * (len(api_key) - 12) + api_key[-4:] if len(api_key) > 12 else '***'
                print(f"  API Key: {masked}")
        else:
            print(f"  API Key: ⚠️ 未设置")

        print(f"  模型: {ai_config.get('model', '未设置')}")
        print(f"  最大Token: {ai_config.get('max_tokens', 2048)}")
        print(f"  温度: {ai_config.get('temperature', 0.7)}")
        print(f"  超时: {ai_config.get('timeout', 60)}秒")

        # 检查配置是否有效
        print(f"\n📋 配置检查:")
        # 使用resolve_env=True获取解析后的配置进行有效性检查
        resolved_config = self.config_manager.get_ai_config(resolve_env=True)
        config_obj = AIConfig.from_dict(resolved_config)
        if config_obj.is_valid():
            print("  ✅ 配置有效，AI分析可以正常使用")
        else:
            issues = []
            if not config_obj.enabled:
                issues.append("AI分析未启用")
            if not config_obj.api_url:
                issues.append("API地址未设置")
            if not config_obj.api_key:
                issues.append("API Key未设置")
            print(f"  ⚠️ 配置无效: {', '.join(issues)}")
            print(f"\n💡 提示: 使用 'webmon config ai enable' 启用AI分析")

        return True

    def _enable_ai(self) -> bool:
        """启用AI分析"""
        ai_config = self.config_manager.get_ai_config()

        # 检查API Key是否已设置（使用resolve_env获取实际值）
        resolved_config = self.config_manager.get_ai_config(resolve_env=True)
        resolved_key = resolved_config.get('api_key', '')

        if not resolved_key:
            print("⚠️ API Key未设置，请先设置API Key:")
            print("  方法1: webmon config ai set --api-key YOUR_API_KEY")
            print("  方法2: 在.env文件中设置 AI_API_KEY=YOUR_API_KEY")
            return False

        ai_config['enabled'] = True

        if self.config_manager.update_ai_config(ai_config):
            print("✅ AI分析已启用")

            # 显示当前配置摘要
            print(f"\n当前配置:")
            print(f"  模型: {ai_config.get('model', 'deepseek-reasoner')}")
            print(f"  API地址: {ai_config.get('api_url', '')}")
            return True
        else:
            print("❌ 启用AI分析失败")
            return False

    def _disable_ai(self) -> bool:
        """禁用AI分析"""
        ai_config = self.config_manager.get_ai_config()
        ai_config['enabled'] = False

        if self.config_manager.update_ai_config(ai_config):
            print("✅ AI分析已禁用")
            return True
        else:
            print("❌ 禁用AI分析失败")
            return False

    def _set_ai_config(self) -> bool:
        """设置AI配置项"""
        ai_config = self.config_manager.get_ai_config()
        updated = False

        # 处理各个配置项
        if hasattr(self.args, 'api_url') and self.args.api_url:
            ai_config['api_url'] = self.args.api_url
            print(f"✅ API地址已更新: {self.args.api_url}")
            updated = True

        if hasattr(self.args, 'api_key') and self.args.api_key:
            ai_config['api_key'] = self.args.api_key
            print(f"✅ API Key已更新")
            updated = True

        if hasattr(self.args, 'model') and self.args.model:
            ai_config['model'] = self.args.model
            print(f"✅ 模型已更新: {self.args.model}")
            updated = True

        if hasattr(self.args, 'max_tokens') and self.args.max_tokens:
            ai_config['max_tokens'] = self.args.max_tokens
            print(f"✅ 最大Token已更新: {self.args.max_tokens}")
            updated = True

        if hasattr(self.args, 'temperature') and self.args.temperature is not None:
            ai_config['temperature'] = self.args.temperature
            print(f"✅ 温度已更新: {self.args.temperature}")
            updated = True

        if hasattr(self.args, 'timeout') and self.args.timeout:
            ai_config['timeout'] = self.args.timeout
            print(f"✅ 超时时间已更新: {self.args.timeout}秒")
            updated = True

        if not updated:
            print("⚠️ 未指定任何配置项")
            print("\n可用配置项:")
            print("  --api-url URL     设置API地址")
            print("  --api-key KEY     设置API Key")
            print("  --model MODEL     设置模型名称")
            print("  --max-tokens N    设置最大Token数")
            print("  --temperature T   设置温度参数 (0.0-2.0)")
            print("  --timeout N       设置超时时间 (秒)")
            return True

        if self.config_manager.update_ai_config(ai_config):
            print("\n配置已保存")
            return True
        else:
            print("❌ 保存配置失败")
            return False

    def _test_ai(self) -> bool:
        """测试AI连接"""
        print("🔄 正在测试AI连接...")

        # 使用resolve_env=True获取解析后的配置
        ai_config_dict = self.config_manager.get_ai_config(resolve_env=True)
        ai_config = AIConfig.from_dict(ai_config_dict)

        if not ai_config.api_key:
            print("❌ API Key未设置，无法测试")
            return False

        # 临时启用以便测试
        ai_config.enabled = True

        ai_service = AIAnalysisService(config=ai_config)

        # 运行异步测试
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        result = loop.run_until_complete(ai_service.test_connection())

        if result['success']:
            print(f"✅ {result['message']}")
            print(f"  响应: {result.get('response', '')[:100]}")
            print(f"  延迟: {result['latency']:.2f}秒")
            print(f"  Token使用: {result.get('tokens_used', 0)}")
        else:
            print(f"❌ 连接失败: {result['message']}")

        return result['success']

    def _show_all_config(self) -> bool:
        """显示所有配置"""
        print("\n📋 WebMon 配置概览")
        print("=" * 50)

        # 显示AI配置
        self._show_ai_status()

        # 可以扩展显示其他配置...

        return True

    def _show_help(self):
        """显示帮助信息"""
        print("\n📖 配置命令帮助")
        print("=" * 50)
        print("\n用法: webmon config <子命令> [选项]")
        print("\n子命令:")
        print("  ai              查看或管理AI分析配置")
        print("  show            显示所有配置")
        print("\nAI配置操作:")
        print("  ai              显示AI配置状态")
        print("  ai enable       启用AI分析")
        print("  ai disable      禁用AI分析")
        print("  ai set [选项]   设置AI配置项")
        print("  ai test         测试AI连接")
        print("\n示例:")
        print("  webmon config ai")
        print("  webmon config ai enable")
        print("  webmon config ai set --api-key sk-xxx --model deepseek-chat")
        print("  webmon config ai test")

    def validate_args(self) -> bool:
        """验证参数"""
        return True
