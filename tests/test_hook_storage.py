"""
Hook 执行结果存储测试

测试 HookResultStorage 的存储、查询和清理功能。
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytest

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from webmon.hooks.storage import HookResultStorage
from webmon.hooks.result import HookResult


class TestHookResultStorage:
    """测试 HookResultStorage"""

    @pytest.fixture
    def storage(self, tmp_path):
        """创建临时存储实例"""
        db_path = tmp_path / "test_hooks.db"
        return HookResultStorage(
            db_path=str(db_path),
            max_entries=100,
            auto_cleanup_days=30,
        )

    @pytest.fixture
    def sample_result(self):
        """创建示例执行结果"""
        result = HookResult(
            hook_name="test_hook",
            trigger="on_change_detected",
            task_id="task-001",
        )
        result.mark_success(exit_code=0, stdout="Hello World", stderr="")
        return result

    def test_add_and_get(self, storage, sample_result):
        """测试添加和获取执行结果"""
        # 添加结果
        result_id = storage.add(sample_result)
        assert result_id == sample_result.id

        # 获取结果
        retrieved = storage.get(result_id)
        assert retrieved is not None
        assert retrieved.id == sample_result.id
        assert retrieved.hook_name == "test_hook"
        assert retrieved.trigger == "on_change_detected"
        assert retrieved.task_id == "task-001"
        assert retrieved.success is True
        assert retrieved.exit_code == 0
        assert "Hello World" in retrieved.stdout

    def test_get_nonexistent(self, storage):
        """测试获取不存在的记录"""
        result = storage.get("nonexistent-id")
        assert result is None

    def test_list_results(self, storage):
        """测试列出执行结果"""
        # 添加多条记录
        for i in range(5):
            result = HookResult(
                hook_name=f"hook_{i}",
                trigger="on_change_detected",
                task_id=f"task-{i:03d}",
            )
            result.mark_success()
            storage.add(result)

        # 列出所有记录
        results = storage.list(limit=10)
        assert len(results) == 5

    def test_list_with_filters(self, storage):
        """测试带筛选条件的列表查询"""
        # 添加不同类型的记录
        for i in range(3):
            result = HookResult(
                hook_name="hook_a",
                trigger="on_change_detected",
                task_id="task-001",
            )
            result.mark_success()
            storage.add(result)

        for i in range(2):
            result = HookResult(
                hook_name="hook_b",
                trigger="on_before_notify",
                task_id="task-002",
            )
            result.mark_failure("Error occurred", error_type="non_zero_exit")
            storage.add(result)

        # 按 hook_name 筛选
        results = storage.list(hook_name="hook_a")
        assert len(results) == 3

        # 按 trigger 筛选
        results = storage.list(trigger="on_before_notify")
        assert len(results) == 2

        # 按 task_id 筛选
        results = storage.list(task_id="task-001")
        assert len(results) == 3

        # 按 success 筛选
        results = storage.list(success=True)
        assert len(results) == 3

        results = storage.list(success=False)
        assert len(results) == 2

    def test_count(self, storage):
        """测试统计记录数量"""
        # 添加记录
        for i in range(10):
            result = HookResult(
                hook_name="test_hook",
                trigger="on_change_detected",
                task_id=f"task-{i:03d}",
            )
            if i < 7:
                result.mark_success()
            else:
                result.mark_failure("Error")
            storage.add(result)

        # 统计总数
        total = storage.count()
        assert total == 10

        # 按条件统计
        success_count = storage.count(success=True)
        assert success_count == 7

        fail_count = storage.count(success=False)
        assert fail_count == 3

    def test_get_latest(self, storage):
        """测试获取最新记录"""
        # 添加记录
        for i in range(3):
            result = HookResult(
                hook_name="test_hook",
                trigger="on_change_detected",
                task_id="task-001",
            )
            result.mark_success(stdout=f"Output {i}")
            storage.add(result)

        # 获取最新记录
        latest = storage.get_latest(hook_name="test_hook")
        assert latest is not None
        assert "Output 2" in latest.stdout

    def test_get_statistics(self, storage):
        """测试获取统计信息"""
        # 添加成功和失败的记录
        for i in range(8):
            result = HookResult(
                hook_name="test_hook",
                trigger="on_change_detected",
                task_id="task-001",
            )
            result.mark_success()
            storage.add(result)

        for i in range(2):
            result = HookResult(
                hook_name="test_hook",
                trigger="on_before_notify",
                task_id="task-001",
            )
            result.mark_failure("Error", error_type="timeout")
            storage.add(result)

        # 获取统计
        stats = storage.get_statistics(days=7)
        assert stats["total_executions"] == 10
        assert stats["successful"] == 8
        assert stats["failed"] == 2
        assert stats["success_rate"] == 0.8
        assert "on_change_detected" in stats["by_trigger"]
        assert stats["by_trigger"]["on_change_detected"] == 8
        assert "timeout" in stats["by_error_type"]

    def test_cleanup_old_entries(self, storage):
        """测试清理过期记录"""
        # 添加记录
        for i in range(5):
            result = HookResult(
                hook_name="test_hook",
                trigger="on_change_detected",
                task_id="task-001",
            )
            # 模拟旧记录：设置为 60 天前
            result.started_at = datetime.now() - timedelta(days=60)
            result.mark_success()
            storage.add(result)

        # 添加新记录
        for i in range(3):
            result = HookResult(
                hook_name="test_hook",
                trigger="on_change_detected",
                task_id="task-001",
            )
            result.mark_success()
            storage.add(result)

        # 清理 30 天前的记录
        cleaned = storage.cleanup_old_entries(days=30)
        assert cleaned == 5

        # 验证剩余记录
        remaining = storage.count()
        assert remaining == 3

    def test_max_entries_limit(self, storage):
        """测试最大记录数限制"""
        # 创建一个小限制的存储
        from tempfile import mkdtemp
        small_storage = HookResultStorage(
            db_path=f"{mkdtemp()}/small.db",
            max_entries=10,
        )

        # 添加超过限制的记录
        for i in range(15):
            result = HookResult(
                hook_name="test_hook",
                trigger="on_change_detected",
                task_id=f"task-{i:03d}",
            )
            result.mark_success()
            small_storage.add(result)

        # 验证记录数不超过限制
        count = small_storage.count()
        assert count <= 10

    def test_delete_by_task(self, storage):
        """测试按任务删除记录"""
        # 添加不同任务的记录
        for i in range(3):
            result = HookResult(
                hook_name="test_hook",
                trigger="on_change_detected",
                task_id="task-001",
            )
            result.mark_success()
            storage.add(result)

        for i in range(2):
            result = HookResult(
                hook_name="test_hook",
                trigger="on_change_detected",
                task_id="task-002",
            )
            result.mark_success()
            storage.add(result)

        # 删除 task-001 的记录
        deleted = storage.delete_by_task("task-001")
        assert deleted == 3

        # 验证剩余记录
        remaining = storage.count()
        assert remaining == 2

    def test_delete_by_hook(self, storage):
        """测试按 Hook 名称删除记录"""
        # 添加不同 Hook 的记录
        for i in range(4):
            result = HookResult(
                hook_name="hook_a",
                trigger="on_change_detected",
                task_id="task-001",
            )
            result.mark_success()
            storage.add(result)

        for i in range(2):
            result = HookResult(
                hook_name="hook_b",
                trigger="on_change_detected",
                task_id="task-001",
            )
            result.mark_success()
            storage.add(result)

        # 删除 hook_a 的记录
        deleted = storage.delete_by_hook("hook_a")
        assert deleted == 4

        # 验证剩余记录
        remaining = storage.count()
        assert remaining == 2

    def test_get_storage_info(self, storage, sample_result):
        """测试获取存储信息"""
        # 添加一些记录
        storage.add(sample_result)

        # 获取存储信息
        info = storage.get_storage_info()
        assert "file_path" in info
        assert "file_size" in info
        assert info["total_entries"] == 1
        assert info["max_entries"] == 100
        assert info["auto_cleanup_days"] == 30

    def test_failed_result_storage(self, storage):
        """测试失败结果的存储"""
        result = HookResult(
            hook_name="failing_hook",
            trigger="on_change_detected",
            task_id="task-001",
        )
        result.mark_failure(
            error_message="Script crashed",
            exit_code=1,
            stdout="",
            stderr="Error: Division by zero",
            error_type="crash",
        )
        result.retry_count = 2

        # 存储
        storage.add(result)

        # 获取并验证
        retrieved = storage.get(result.id)
        assert retrieved is not None
        assert retrieved.success is False
        assert retrieved.exit_code == 1
        assert retrieved.error_message == "Script crashed"
        assert retrieved.error_type == "crash"
        assert retrieved.retry_count == 2
        assert "Division by zero" in retrieved.stderr

    def test_timeout_result_storage(self, storage):
        """测试超时结果的存储"""
        result = HookResult(
            hook_name="slow_hook",
            trigger="on_change_detected",
            task_id="task-001",
        )
        result.mark_timeout(30)

        # 存储
        storage.add(result)

        # 获取并验证
        retrieved = storage.get(result.id)
        assert retrieved is not None
        assert retrieved.success is False
        assert retrieved.is_timeout is True
        assert "超时" in retrieved.error_message


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
