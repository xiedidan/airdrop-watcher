"""
编辑监控任务命令实现
"""

import json
from pathlib import Path
from argparse import Namespace
from typing import Dict, Any, Optional

from webmon.cli.command import Command
from webmon.utils.logger import get_logger


class EditCommand(Command):
    """编辑监控任务命令"""

    def __init__(self, args: Namespace):
        super().__init__(args)
        self.logger = get_logger(__name__)

    def execute(self) -> bool:
        """执行编辑任务命令"""
        try:
            task_id = self.args.task_id
            self.logger.info(f"编辑监控任务: {task_id}")

            # 加载任务
            task = self._load_task(task_id)
            if not task:
                print(f"❌ 未找到任务: {task_id}")
                return False

            print(f"📝 正在编辑任务: {task['name']} (ID: {task['id'][:8]})")

            # 收集要修改的字段
            updates = self._collect_updates(task)

            if not updates:
                print("⚠️  没有修改任何字段")
                return True

            # 显示修改内容
            print("\n📋 将进行以下修改:")
            for key, (old_val, new_val) in updates.items():
                print(f"   {key}: {old_val} → {new_val}")

            # 确认修改
            if not self.args.force:
                confirm = input("\n确认修改？[y/N]: ").strip().lower()
                if confirm not in ['y', 'yes']:
                    print("❌ 已取消修改")
                    return False

            # 应用修改
            if not self._apply_updates(task, updates):
                return False

            self.logger.info(f"任务修改成功: {task['name']}")
            print(f"✅ 任务修改成功！")

            # 显示修改后的任务
            self._show_task_info(task)

            # 通知调度器立即重启该任务
            self._notify_task_restart(task['id'])

            return True

        except Exception as e:
            self.logger.error(f"编辑任务失败: {e}")
            print(f"❌ 编辑任务失败: {e}")
            return False

    def _load_task(self, task_identifier: str) -> Optional[Dict[str, Any]]:
        """加载任务配置"""
        try:
            config_file = Path('config/config.json')

            if not config_file.exists():
                return None

            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            tasks = config.get("tasks", [])

            # 按ID或名称查找
            for task in tasks:
                if task['id'] == task_identifier or task['id'].startswith(task_identifier):
                    return task
                if task['name'] == task_identifier:
                    return task

            return None

        except Exception as e:
            self.logger.error(f"加载任务配置失败: {e}")
            return None

    def _collect_updates(self, task: Dict[str, Any]) -> Dict[str, tuple]:
        """收集要更新的字段"""
        updates = {}

        # 名称
        if self.args.name:
            updates['name'] = (task['name'], self.args.name)

        # 描述
        if self.args.description is not None:
            old_desc = task.get('description', '')
            updates['description'] = (old_desc, self.args.description)

        # URL
        if self.args.url:
            updates['url'] = (task['url'], self.args.url)

        # 间隔
        if self.args.interval is not None:
            updates['interval'] = (task['interval'], self.args.interval)

        # 超时
        if self.args.timeout is not None:
            updates['timeout'] = (task['timeout'], self.args.timeout)

        # 选择器
        if self.args.selector is not None:
            old_selectors = task.get('selectors', [])
            if self.args.selector:
                new_selectors = [self.args.selector]
            else:
                new_selectors = []
            updates['selectors'] = (old_selectors, new_selectors)

        # 启用/禁用
        if self.args.enable is not None:
            updates['enabled'] = (task.get('enabled', True), self.args.enable)

        # AI提示词
        if getattr(self.args, 'ai_prompt', None) is not None:
            old_prompt = task.get('ai_prompt', '')
            updates['ai_prompt'] = (old_prompt, self.args.ai_prompt)

        return updates

    def _apply_updates(self, task: Dict[str, Any], updates: Dict[str, tuple]) -> bool:
        """应用修改到配置文件"""
        try:
            config_file = Path('config/config.json')

            # 读取配置
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # 找到任务并更新
            tasks = config.get("tasks", [])
            for i, t in enumerate(tasks):
                if t['id'] == task['id']:
                    # 应用所有修改
                    for key, (old_val, new_val) in updates.items():
                        tasks[i][key] = new_val

                    # 更新时间戳
                    from datetime import datetime
                    tasks[i]['updated_at'] = datetime.now().isoformat()
                    break

            # 保存配置
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            # 更新本地task对象
            for key, (old_val, new_val) in updates.items():
                task[key] = new_val

            return True

        except Exception as e:
            self.logger.error(f"保存任务配置失败: {e}")
            print(f"❌ 保存任务配置失败: {e}")
            return False

    def _show_task_info(self, task: Dict[str, Any]):
        """显示任务信息"""
        print(f"\n📊 任务信息:")
        print(f"   ID: {task['id']}")
        print(f"   名称: {task['name']}")
        if task.get('description'):
            print(f"   描述: {task['description']}")
        print(f"   URL: {task['url']}")
        print(f"   间隔: {task['interval']}秒")
        print(f"   超时: {task['timeout']}ms")

        selectors = task.get('selectors', [])
        if selectors:
            print(f"   选择器: {', '.join(selectors)}")
        else:
            print(f"   选择器: 无")

        print(f"   状态: {'启用' if task.get('enabled', True) else '禁用'}")

        ai_prompt = task.get('ai_prompt', '')
        if ai_prompt:
            display_prompt = ai_prompt[:50] + '...' if len(ai_prompt) > 50 else ai_prompt
            print(f"   AI提示词: {display_prompt}")
        else:
            print(f"   AI提示词: (使用全局默认)")

    def validate_args(self) -> bool:
        """验证参数"""
        if not self.args.task_id:
            print("❌ 必须提供任务ID或名称")
            return False

        # 检查是否至少有一个修改项
        has_changes = any([
            self.args.name,
            getattr(self.args, 'description', None) is not None,
            self.args.url,
            self.args.interval is not None,
            self.args.timeout is not None,
            self.args.selector is not None,
            self.args.enable is not None,
            getattr(self.args, 'ai_prompt', None) is not None
        ])

        if not has_changes:
            print("❌ 必须至少指定一个要修改的字段")
            print("   使用 --help 查看可用选项")
            return False

        # 验证间隔
        if self.args.interval is not None and self.args.interval <= 0:
            print("❌ 检测间隔必须大于0")
            return False

        # 验证超时
        if self.args.timeout is not None and self.args.timeout <= 0:
            print("❌ 超时时间必须大于0")
            return False

        return True

    def _notify_task_restart(self, task_id: str):
        """
        通知调度器立即重启指定任务

        通过创建一个信号文件来通知正在运行的调度器，
        调度器会检测到这个文件并立即重新调度该任务。
        """
        try:
            # 检查调度器是否正在运行
            pid_file = Path("webmon.pid")
            if not pid_file.exists():
                self.logger.debug("调度器未运行，跳过重启通知")
                return

            # 创建重启信号目录（如果不存在）
            signal_dir = Path("data/.restart_signals")
            signal_dir.mkdir(parents=True, exist_ok=True)

            # 创建该任务的重启信号文件
            signal_file = signal_dir / f"{task_id}.restart"
            from datetime import datetime
            signal_file.write_text(f"restart_requested_at={datetime.now().isoformat()}")

            self.logger.info(f"已发送任务重启信号: {task_id}")
            print(f"🔄 已通知调度器立即重启任务")

        except Exception as e:
            self.logger.warning(f"发送任务重启信号失败: {e}")
            print(f"⚠️  无法通知调度器重启任务，新配置将在下次调度扫描时生效")

