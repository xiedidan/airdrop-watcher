"""
Hook 执行结果存储管理器

使用 SQLite 数据库存储 Hook 执行记录，提供查询和自动清理功能。
"""

import json
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from webmon.utils.logger import get_logger
from .result import HookResult


class HookResultStorage:
    """
    Hook 执行结果存储管理器

    使用 SQLite 数据库存储 Hook 执行记录，支持：
    - 存储 HookResult 数据
    - 按条件查询执行历史
    - 30 天自动清理过期记录
    - 统计信息查询
    """

    # 数据库版本，用于未来迁移
    DB_VERSION = 1

    def __init__(
        self,
        db_path: str = "data/hooks.db",
        max_entries: int = 10000,
        auto_cleanup_days: int = 30,
    ):
        """
        初始化 Hook 结果存储管理器

        Args:
            db_path: 数据库文件路径
            max_entries: 最大记录条目数
            auto_cleanup_days: 自动清理天数（默认 30 天）
        """
        self.logger = get_logger(__name__)
        self.db_path = Path(db_path)
        self.max_entries = max_entries
        self.auto_cleanup_days = auto_cleanup_days

        # 线程本地存储，每个线程使用独立连接
        self._local = threading.local()

        # 确保数据目录存在
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # 初始化数据库
        self._init_database()

    def _get_connection(self) -> sqlite3.Connection:
        """获取当前线程的数据库连接"""
        if not hasattr(self._local, "connection") or self._local.connection is None:
            self._local.connection = sqlite3.connect(
                str(self.db_path),
                check_same_thread=False,
                timeout=30.0,
            )
            self._local.connection.row_factory = sqlite3.Row
            # 启用外键约束
            self._local.connection.execute("PRAGMA foreign_keys = ON")
            # 使用 WAL 模式提高并发性能
            self._local.connection.execute("PRAGMA journal_mode = WAL")
        return self._local.connection

    @contextmanager
    def _get_cursor(self):
        """获取数据库游标的上下文管理器"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            self.logger.error(f"数据库操作失败: {e}")
            raise
        finally:
            cursor.close()

    def _init_database(self):
        """初始化数据库表结构"""
        with self._get_cursor() as cursor:
            # 创建 hook_results 表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS hook_results (
                    id TEXT PRIMARY KEY,
                    hook_name TEXT NOT NULL,
                    trigger TEXT NOT NULL,
                    task_id TEXT NOT NULL,
                    success INTEGER DEFAULT 0,
                    exit_code INTEGER,
                    stdout TEXT,
                    stderr TEXT,
                    execution_time REAL DEFAULT 0.0,
                    started_at TEXT NOT NULL,
                    finished_at TEXT,
                    error_message TEXT,
                    error_type TEXT DEFAULT 'none',
                    retry_count INTEGER DEFAULT 0,
                    metadata TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 创建索引以加速常见查询
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_hook_results_hook_name
                ON hook_results(hook_name)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_hook_results_trigger
                ON hook_results(trigger)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_hook_results_task_id
                ON hook_results(task_id)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_hook_results_started_at
                ON hook_results(started_at DESC)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_hook_results_success
                ON hook_results(success)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_hook_results_error_type
                ON hook_results(error_type)
            """)

            # 创建元数据表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)

            # 设置数据库版本
            cursor.execute(
                "INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)",
                ("db_version", str(self.DB_VERSION)),
            )

        self.logger.debug(f"Hook 结果存储数据库已初始化: {self.db_path}")

    def add(self, result: HookResult) -> str:
        """
        添加 Hook 执行结果

        Args:
            result: HookResult 对象

        Returns:
            记录 ID
        """
        metadata_json = json.dumps(result.metadata, ensure_ascii=False, default=str)

        with self._get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO hook_results
                (id, hook_name, trigger, task_id, success, exit_code,
                 stdout, stderr, execution_time, started_at, finished_at,
                 error_message, error_type, retry_count, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    result.id,
                    result.hook_name,
                    result.trigger,
                    result.task_id,
                    1 if result.success else 0,
                    result.exit_code,
                    result.stdout,
                    result.stderr,
                    result.execution_time,
                    result.started_at.isoformat() if result.started_at else None,
                    result.finished_at.isoformat() if result.finished_at else None,
                    result.error_message,
                    result.error_type,
                    result.retry_count,
                    metadata_json,
                ),
            )

            # 检查是否需要清理旧记录
            self._check_and_cleanup(cursor)

        self.logger.debug(f"已保存 Hook 执行结果: {result.id}")
        return result.id

    def _check_and_cleanup(self, cursor):
        """检查并清理超出限制的旧记录"""
        cursor.execute("SELECT COUNT(*) FROM hook_results")
        count = cursor.fetchone()[0]

        if count > self.max_entries:
            # 删除最旧的记录，保留 max_entries 条
            delete_count = count - self.max_entries
            cursor.execute(
                """
                DELETE FROM hook_results
                WHERE id IN (
                    SELECT id FROM hook_results
                    ORDER BY started_at ASC
                    LIMIT ?
                )
            """,
                (delete_count,),
            )
            self.logger.info(f"已清理 {delete_count} 条过期 Hook 执行记录")

    def get(self, result_id: str) -> Optional[HookResult]:
        """
        获取单条执行结果

        Args:
            result_id: 结果 ID

        Returns:
            HookResult 对象，不存在则返回 None
        """
        with self._get_cursor() as cursor:
            cursor.execute(
                "SELECT * FROM hook_results WHERE id = ?",
                (result_id,),
            )
            row = cursor.fetchone()

            if row:
                return self._row_to_result(row)

        return None

    def _row_to_result(self, row: sqlite3.Row) -> HookResult:
        """将数据库行转换为 HookResult 对象"""
        metadata = {}
        if row["metadata"]:
            try:
                metadata = json.loads(row["metadata"])
            except json.JSONDecodeError:
                pass

        return HookResult.from_dict({
            "id": row["id"],
            "hook_name": row["hook_name"],
            "trigger": row["trigger"],
            "task_id": row["task_id"],
            "success": bool(row["success"]),
            "exit_code": row["exit_code"],
            "stdout": row["stdout"] or "",
            "stderr": row["stderr"] or "",
            "execution_time": row["execution_time"] or 0.0,
            "started_at": row["started_at"],
            "finished_at": row["finished_at"],
            "error_message": row["error_message"],
            "error_type": row["error_type"] or "none",
            "retry_count": row["retry_count"] or 0,
            "metadata": metadata,
        })

    def list(
        self,
        hook_name: str = None,
        trigger: str = None,
        task_id: str = None,
        success: bool = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[HookResult]:
        """
        列出执行结果

        Args:
            hook_name: 按 Hook 名称筛选
            trigger: 按触发点筛选
            task_id: 按任务 ID 筛选
            success: 按成功/失败筛选
            limit: 返回结果数量限制
            offset: 偏移量

        Returns:
            HookResult 列表
        """
        conditions = []
        params = []

        if hook_name:
            conditions.append("hook_name = ?")
            params.append(hook_name)

        if trigger:
            conditions.append("trigger = ?")
            params.append(trigger)

        if task_id:
            conditions.append("task_id = ?")
            params.append(task_id)

        if success is not None:
            conditions.append("success = ?")
            params.append(1 if success else 0)

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        with self._get_cursor() as cursor:
            query = f"""
                SELECT * FROM hook_results
                WHERE {where_clause}
                ORDER BY started_at DESC
                LIMIT ? OFFSET ?
            """
            params.extend([limit, offset])
            cursor.execute(query, params)

            results = []
            for row in cursor.fetchall():
                try:
                    results.append(self._row_to_result(row))
                except Exception as e:
                    self.logger.warning(f"跳过无效的 Hook 结果记录: {e}")

            return results

    def count(
        self,
        hook_name: str = None,
        trigger: str = None,
        task_id: str = None,
        success: bool = None,
    ) -> int:
        """
        统计执行结果数量

        Args:
            hook_name: 按 Hook 名称筛选
            trigger: 按触发点筛选
            task_id: 按任务 ID 筛选
            success: 按成功/失败筛选

        Returns:
            记录数量
        """
        conditions = []
        params = []

        if hook_name:
            conditions.append("hook_name = ?")
            params.append(hook_name)

        if trigger:
            conditions.append("trigger = ?")
            params.append(trigger)

        if task_id:
            conditions.append("task_id = ?")
            params.append(task_id)

        if success is not None:
            conditions.append("success = ?")
            params.append(1 if success else 0)

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        with self._get_cursor() as cursor:
            cursor.execute(
                f"SELECT COUNT(*) FROM hook_results WHERE {where_clause}",
                params,
            )
            return cursor.fetchone()[0]

    def get_latest(
        self,
        hook_name: str = None,
        task_id: str = None,
    ) -> Optional[HookResult]:
        """
        获取最新的执行结果

        Args:
            hook_name: 按 Hook 名称筛选
            task_id: 按任务 ID 筛选

        Returns:
            最新的 HookResult 对象
        """
        results = self.list(hook_name=hook_name, task_id=task_id, limit=1)
        return results[0] if results else None

    def get_statistics(
        self,
        hook_name: str = None,
        task_id: str = None,
        days: int = 7,
    ) -> Dict[str, Any]:
        """
        获取执行统计信息

        Args:
            hook_name: 按 Hook 名称筛选
            task_id: 按任务 ID 筛选
            days: 统计最近多少天的数据

        Returns:
            统计信息字典
        """
        cutoff_date = datetime.now() - timedelta(days=days)

        conditions = ["started_at >= ?"]
        params = [cutoff_date.isoformat()]

        if hook_name:
            conditions.append("hook_name = ?")
            params.append(hook_name)

        if task_id:
            conditions.append("task_id = ?")
            params.append(task_id)

        where_clause = " AND ".join(conditions)

        with self._get_cursor() as cursor:
            # 总执行次数
            cursor.execute(
                f"SELECT COUNT(*) FROM hook_results WHERE {where_clause}",
                params,
            )
            total_executions = cursor.fetchone()[0]

            if total_executions == 0:
                return {
                    "total_executions": 0,
                    "successful": 0,
                    "failed": 0,
                    "success_rate": 0.0,
                    "avg_execution_time": 0.0,
                    "total_retries": 0,
                    "by_trigger": {},
                    "by_error_type": {},
                }

            # 成功次数
            cursor.execute(
                f"SELECT COUNT(*) FROM hook_results WHERE success = 1 AND {where_clause}",
                params,
            )
            successful = cursor.fetchone()[0]

            # 失败次数
            failed = total_executions - successful

            # 平均执行时间
            cursor.execute(
                f"SELECT AVG(execution_time) FROM hook_results WHERE {where_clause}",
                params,
            )
            avg_time = cursor.fetchone()[0] or 0.0

            # 总重试次数
            cursor.execute(
                f"SELECT SUM(retry_count) FROM hook_results WHERE {where_clause}",
                params,
            )
            total_retries = cursor.fetchone()[0] or 0

            # 按触发点统计
            cursor.execute(
                f"""
                SELECT trigger, COUNT(*) as count
                FROM hook_results
                WHERE {where_clause}
                GROUP BY trigger
            """,
                params,
            )
            by_trigger = {row["trigger"]: row["count"] for row in cursor.fetchall()}

            # 按错误类型统计
            cursor.execute(
                f"""
                SELECT error_type, COUNT(*) as count
                FROM hook_results
                WHERE success = 0 AND {where_clause}
                GROUP BY error_type
            """,
                params,
            )
            by_error_type = {row["error_type"]: row["count"] for row in cursor.fetchall()}

            return {
                "total_executions": total_executions,
                "successful": successful,
                "failed": failed,
                "success_rate": round(successful / total_executions, 4),
                "avg_execution_time": round(avg_time, 3),
                "total_retries": total_retries,
                "by_trigger": by_trigger,
                "by_error_type": by_error_type,
            }

    def cleanup_old_entries(self, days: int = None) -> int:
        """
        清理旧的执行记录

        Args:
            days: 清理多少天前的记录（默认使用 auto_cleanup_days）

        Returns:
            清理的记录数量
        """
        cleanup_days = days or self.auto_cleanup_days
        cutoff_date = datetime.now() - timedelta(days=cleanup_days)

        with self._get_cursor() as cursor:
            cursor.execute(
                "DELETE FROM hook_results WHERE started_at < ?",
                (cutoff_date.isoformat(),),
            )
            removed_count = cursor.rowcount

        if removed_count > 0:
            self.logger.info(f"已清理 {removed_count} 条过期 Hook 执行记录（{cleanup_days} 天前）")

        return removed_count

    def delete_by_task(self, task_id: str) -> int:
        """
        删除指定任务的所有执行记录

        Args:
            task_id: 任务 ID

        Returns:
            删除的记录数量
        """
        with self._get_cursor() as cursor:
            cursor.execute(
                "DELETE FROM hook_results WHERE task_id = ?",
                (task_id,),
            )
            return cursor.rowcount

    def delete_by_hook(self, hook_name: str) -> int:
        """
        删除指定 Hook 的所有执行记录

        Args:
            hook_name: Hook 名称

        Returns:
            删除的记录数量
        """
        with self._get_cursor() as cursor:
            cursor.execute(
                "DELETE FROM hook_results WHERE hook_name = ?",
                (hook_name,),
            )
            return cursor.rowcount

    def get_storage_info(self) -> Dict[str, Any]:
        """获取存储信息"""
        try:
            stat = self.db_path.stat()

            with self._get_cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM hook_results")
                total_entries = cursor.fetchone()[0]

                cursor.execute(
                    "SELECT MIN(started_at), MAX(started_at) FROM hook_results"
                )
                row = cursor.fetchone()
                first_entry_date = row[0]
                last_entry_date = row[1]

            return {
                "file_path": str(self.db_path),
                "file_size": stat.st_size,
                "total_entries": total_entries,
                "first_entry_date": first_entry_date,
                "last_entry_date": last_entry_date,
                "max_entries": self.max_entries,
                "auto_cleanup_days": self.auto_cleanup_days,
            }
        except Exception as e:
            self.logger.error(f"获取存储信息失败: {e}")
            return {}

    def close(self):
        """关闭数据库连接"""
        if hasattr(self._local, "connection") and self._local.connection:
            self._local.connection.close()
            self._local.connection = None

    def vacuum(self):
        """整理数据库，回收空间"""
        conn = self._get_connection()
        conn.execute("VACUUM")
        conn.commit()
        self.logger.debug("数据库已整理")
