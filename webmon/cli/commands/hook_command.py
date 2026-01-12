#!/usr/bin/env python3
"""
Hook 管理命令

提供 Hook 的列表、测试、验证和历史查询功能。
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from argparse import Namespace

from webmon.cli.command import Command
from webmon.utils.logger import get_logger
from webmon.config import ConfigManager
from webmon.hooks import (
    HookManager,
    HookConfig,
    HookResult,
    HookResultStorage,
    HookTrigger,
)


class HookCommand(Command):
    """Hook 管理命令"""

    def __init__(self, args: Namespace):
        super().__init__(args)
        self.logger = get_logger(__name__)
        self.config_manager = ConfigManager()
        self.hook_manager = HookManager(config_manager=self.config_manager)

    def execute(self) -> bool:
        """执行 Hook 命令"""
        subcommand = getattr(self.args, 'hook_subcommand', None)

        if not subcommand:
            print("❌ 请指定子命令: list, test, validate, history")
            print("   使用 'webmon hook -h' 查看帮助")
            return False

        # 分发到子命令
        handlers = {
            'list': self._handle_list,
            'test': self._handle_test,
            'validate': self._handle_validate,
            'history': self._handle_history,
        }

        handler = handlers.get(subcommand)
        if handler:
            return handler()
        else:
            print(f"❌ 未知子命令: {subcommand}")
            return False

    def _handle_list(self) -> bool:
        """列出所有 Hook"""
        try:
            if not self.hook_manager.is_enabled:
                print("⚠️  Hook 功能未启用")
                print("   在 config/config.json 中设置 hooks.enabled = true 启用")
                return True

            all_hooks = self.hook_manager.get_all_hooks()

            if not all_hooks:
                print("📋 没有配置任何 Hook")
                return True

            # 统计
            total_count = sum(len(hooks) for hooks in all_hooks.values())
            print(f"📋 全局 Hook 列表 (共 {total_count} 个)")
            print("=" * 70)

            for trigger, hooks in all_hooks.items():
                if hooks:
                    trigger_name = self._get_trigger_display_name(trigger)
                    print(f"\n🔔 {trigger_name} ({len(hooks)} 个)")
                    print("-" * 50)

                    for hook in hooks:
                        self._print_hook_info(hook)

            # 显示存储信息
            storage_info = self.hook_manager.get_storage_info()
            if storage_info:
                print(f"\n💾 存储信息:")
                print(f"   记录数: {storage_info.get('total_entries', 0)}")
                print(f"   数据库: {storage_info.get('file_path', 'N/A')}")

            return True

        except Exception as e:
            self.logger.error(f"列出 Hook 失败: {e}")
            print(f"❌ 列出 Hook 失败: {e}")
            return False

    def _handle_test(self) -> bool:
        """测试指定的 Hook"""
        hook_name = getattr(self.args, 'hook_name', None)
        trigger = getattr(self.args, 'trigger', 'on_change_detected')

        if not hook_name:
            print("❌ 请指定要测试的 Hook 名称")
            print("   使用 'webmon hook list' 查看可用的 Hook")
            return False

        if not self.hook_manager.is_enabled:
            print("⚠️  Hook 功能未启用")
            return False

        # 查找 Hook
        hook_config = self.hook_manager.get_hook_by_name(hook_name)
        if not hook_config:
            print(f"❌ 找不到 Hook: {hook_name}")
            print("   使用 'webmon hook list' 查看可用的 Hook")
            return False

        print(f"🧪 测试 Hook: {hook_name}")
        print(f"   触发点: {trigger}")
        print(f"   脚本: {hook_config.script}")
        print("-" * 50)

        # 构建测试上下文
        context = self._build_test_context()

        # 执行 Hook
        try:
            result = asyncio.run(
                self.hook_manager.executor.execute_with_retry(
                    hook_config, trigger, context
                )
            )

            # 显示结果
            self._print_test_result(result)

            return result.success

        except Exception as e:
            self.logger.error(f"测试 Hook 失败: {e}")
            print(f"❌ 测试失败: {e}")
            return False

    def _handle_validate(self) -> bool:
        """验证 Hook 配置"""
        try:
            print("🔍 验证 Hook 配置...")
            print("=" * 50)

            hooks_config = self.config_manager.get_hooks_config()

            # 检查全局开关
            enabled = hooks_config.get('enabled', False)
            print(f"   全局开关: {'✅ 启用' if enabled else '❌ 禁用'}")

            if not enabled:
                print("\n⚠️  Hook 功能未启用，跳过详细验证")
                return True

            # 验证默认配置
            defaults = hooks_config.get('defaults', {})
            print(f"\n📋 默认配置:")
            print(f"   超时: {defaults.get('timeout', 30)} 秒")
            print(f"   异步: {'是' if defaults.get('async', True) else '否'}")
            print(f"   最大重试: {defaults.get('max_retries', 0)} 次")

            # 验证全局 Hooks
            global_hooks = hooks_config.get('global_hooks', {})
            total_hooks = 0
            valid_hooks = 0
            errors = []

            print(f"\n🔔 全局 Hook 验证:")

            for trigger, hook_list in global_hooks.items():
                # 验证触发点
                if not HookTrigger.is_valid(trigger):
                    errors.append(f"无效的触发点: {trigger}")
                    continue

                for hook_data in hook_list:
                    total_hooks += 1
                    hook_name = hook_data.get('name', 'unknown')

                    try:
                        # 尝试创建 HookConfig 以验证配置
                        hook_config = HookConfig.from_dict(hook_data)

                        # 验证脚本路径
                        validation = self.hook_manager.executor.validator.validate(
                            hook_config.script
                        )

                        if validation.valid:
                            print(f"   ✅ {hook_name} ({trigger})")
                            valid_hooks += 1
                        else:
                            print(f"   ❌ {hook_name}: {validation.error_message}")
                            errors.append(f"{hook_name}: {validation.error_message}")

                    except Exception as e:
                        print(f"   ❌ {hook_name}: {e}")
                        errors.append(f"{hook_name}: {e}")

            # 总结
            print(f"\n📊 验证结果:")
            print(f"   总计: {total_hooks} 个 Hook")
            print(f"   有效: {valid_hooks} 个")
            print(f"   无效: {total_hooks - valid_hooks} 个")

            if errors:
                print(f"\n⚠️  发现 {len(errors)} 个问题:")
                for error in errors[:5]:
                    print(f"   - {error}")
                if len(errors) > 5:
                    print(f"   ... 还有 {len(errors) - 5} 个问题")

            return len(errors) == 0

        except Exception as e:
            self.logger.error(f"验证 Hook 配置失败: {e}")
            print(f"❌ 验证失败: {e}")
            return False

    def _handle_history(self) -> bool:
        """查看执行历史"""
        try:
            hook_name = getattr(self.args, 'history_hook_name', None)
            limit = getattr(self.args, 'limit', 20)
            success_only = getattr(self.args, 'success', None)
            failed_only = getattr(self.args, 'failed', False)
            output_format = getattr(self.args, 'format', 'table')

            # 确定筛选条件
            success_filter = None
            if success_only:
                success_filter = True
            elif failed_only:
                success_filter = False

            # 获取历史记录
            results = self.hook_manager.get_execution_history(
                hook_name=hook_name,
                success=success_filter,
                limit=limit,
            )

            if output_format == 'json':
                self._print_history_json(results)
            else:
                self._print_history_table(results, hook_name)

            # 显示统计信息
            if not hook_name:
                stats = self.hook_manager.get_execution_statistics(days=7)
                self._print_history_stats(stats)

            return True

        except Exception as e:
            self.logger.error(f"查看 Hook 历史失败: {e}")
            print(f"❌ 查看历史失败: {e}")
            return False

    def _get_trigger_display_name(self, trigger: str) -> str:
        """获取触发点的显示名称"""
        names = {
            'on_change_detected': '变化检测后',
            'on_before_notify': '通知发送前',
            'on_after_notify': '通知发送后',
            'on_notify_failed': '通知失败时',
        }
        return names.get(trigger, trigger)

    def _print_hook_info(self, hook: HookConfig):
        """打印单个 Hook 信息"""
        status = "✅" if hook.enabled else "❌"
        mode = "异步" if hook.async_exec else "同步"
        retry = f", 重试{hook.max_retries}次" if hook.max_retries > 0 else ""

        print(f"   {status} {hook.name}")
        print(f"      类型: {hook.type} | 模式: {mode} | 超时: {hook.timeout}s{retry}")
        print(f"      脚本: {hook.script}")
        if hook.condition:
            print(f"      条件: {hook.condition}")

    def _build_test_context(self) -> Dict[str, Any]:
        """构建测试上下文"""
        return {
            'task': {
                'id': 'test-task-001',
                'name': '测试任务',
                'url': 'https://example.com',
                'description': '这是一个测试任务',
            },
            'change': {
                'detected': True,
                'type': 'content_change',
                'time': datetime.now().isoformat(),
                'similarity': 0.85,
                'old_content': '旧内容示例...',
                'new_content': '新内容示例...',
                'diff': '--- old\n+++ new\n@@ -1 +1 @@\n-旧内容\n+新内容',
            },
            'ai_analysis': '检测到页面内容发生变化，主要变化为：内容更新。',
            'notification': {
                'status': 'pending',
            },
        }

    def _print_test_result(self, result: HookResult):
        """打印测试结果"""
        if result.success:
            print(f"✅ 执行成功")
        else:
            print(f"❌ 执行失败")

        print(f"   退出码: {result.exit_code}")
        print(f"   耗时: {result.duration_str}")

        if result.retry_count > 0:
            print(f"   重试次数: {result.retry_count}")

        if result.stdout.strip():
            print(f"\n📤 标准输出:")
            for line in result.stdout.strip().split('\n')[:10]:
                print(f"   {line}")

        if result.stderr.strip():
            print(f"\n⚠️  标准错误:")
            for line in result.stderr.strip().split('\n')[:10]:
                print(f"   {line}")

        if result.error_message:
            print(f"\n❌ 错误信息: {result.error_message}")

    def _print_history_table(self, results: List[HookResult], hook_name: Optional[str]):
        """打印历史记录表格"""
        if hook_name:
            print(f"📜 Hook [{hook_name}] 执行历史")
        else:
            print(f"📜 Hook 执行历史")

        if not results:
            print("   暂无执行记录")
            return

        print("=" * 90)
        print(f"{'时间':<20} {'Hook名称':<15} {'触发点':<20} {'状态':<6} {'耗时':<10} {'重试':<4}")
        print("-" * 90)

        for result in results:
            status = "✅" if result.success else "❌"
            time_str = result.started_at.strftime('%Y-%m-%d %H:%M:%S') if result.started_at else 'N/A'
            trigger = result.trigger[:18] + '..' if len(result.trigger) > 20 else result.trigger
            hook = result.hook_name[:13] + '..' if len(result.hook_name) > 15 else result.hook_name

            print(f"{time_str:<20} {hook:<15} {trigger:<20} {status:<6} {result.duration_str:<10} {result.retry_count:<4}")

        print("-" * 90)
        print(f"共 {len(results)} 条记录")

    def _print_history_json(self, results: List[HookResult]):
        """打印历史记录 JSON"""
        data = [result.to_dict() for result in results]
        print(json.dumps(data, ensure_ascii=False, indent=2, default=str))

    def _print_history_stats(self, stats: Dict[str, Any]):
        """打印历史统计"""
        print(f"\n📊 最近 7 天统计:")
        print(f"   总执行: {stats.get('total_executions', 0)} 次")
        print(f"   成功: {stats.get('successful', 0)} 次")
        print(f"   失败: {stats.get('failed', 0)} 次")

        success_rate = stats.get('success_rate', 0)
        print(f"   成功率: {success_rate * 100:.1f}%")

        avg_time = stats.get('avg_execution_time', 0)
        print(f"   平均耗时: {avg_time:.3f}s")

        by_trigger = stats.get('by_trigger', {})
        if by_trigger:
            print(f"\n   按触发点:")
            for trigger, count in by_trigger.items():
                print(f"      {trigger}: {count} 次")

        by_error = stats.get('by_error_type', {})
        if by_error:
            print(f"\n   错误分布:")
            for error_type, count in by_error.items():
                print(f"      {error_type}: {count} 次")

    def validate_args(self) -> bool:
        """验证参数"""
        return True
