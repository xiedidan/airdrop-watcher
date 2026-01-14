"""
SQLite 历史记录存储管理器

使用 SQLite 数据库存储历史记录，替代 JSON 文件存储，
提供更好的查询性能和可扩展性。
"""
import json
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..exceptions import StorageError
from ..models.change_details import ChangeDetails
from ..models.check_result import CheckResult


class SQLiteHistoryStorage:
    """SQLite 历史记录存储管理器"""

    # 数据库版本，用于迁移
    DB_VERSION = 1

    def __init__(
        self,
        db_path: str = "data/history.db",
        max_entries: int = 10000,
        auto_cleanup_days: int = 30,
    ):
        """
        初始化 SQLite 历史记录存储管理器

        Args:
            db_path: 数据库文件路径
            max_entries: 最大历史记录条目数
            auto_cleanup_days: 自动清理天数
        """
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
            raise StorageError(f"数据库操作失败: {e}")
        finally:
            cursor.close()

    def _init_database(self):
        """初始化数据库表结构"""
        with self._get_cursor() as cursor:
            # 创建历史记录主表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS history_entries (
                    id TEXT PRIMARY KEY,
                    type TEXT NOT NULL,
                    task_id TEXT NOT NULL,
                    url TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    success INTEGER DEFAULT 1,
                    changed INTEGER DEFAULT 0,
                    data TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 创建索引
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_history_task_id
                ON history_entries(task_id)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_history_timestamp
                ON history_entries(timestamp DESC)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_history_type
                ON history_entries(type)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_history_changed
                ON history_entries(changed)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_history_task_timestamp
                ON history_entries(task_id, timestamp DESC)
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
                """
                INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)
            """,
                ("db_version", str(self.DB_VERSION)),
            )

    def add_check_result(self, check_result: CheckResult) -> str:
        """
        添加检测结果

        Args:
            check_result: 检测结果对象

        Returns:
            记录ID

        Raises:
            StorageError: 存储错误
        """
        data = check_result.to_dict()
        data_json = json.dumps(data, ensure_ascii=False, default=str)

        with self._get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO history_entries
                (id, type, task_id, url, timestamp, success, changed, data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    check_result.id,
                    "check_result",
                    check_result.task_id,
                    check_result.url,
                    check_result.timestamp.isoformat(),
                    1 if check_result.success else 0,
                    1 if check_result.changed else 0,
                    data_json,
                ),
            )

            # 检查是否需要清理旧记录
            self._check_and_cleanup(cursor)

        return check_result.id

    def add_change_details(self, change_details: ChangeDetails) -> str:
        """
        添加变化详情

        Args:
            change_details: 变化详情对象

        Returns:
            记录ID

        Raises:
            StorageError: 存储错误
        """
        data = change_details.to_dict()
        data_json = json.dumps(data, ensure_ascii=False, default=str)

        with self._get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO history_entries
                (id, type, task_id, url, timestamp, success, changed, data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    change_details.id,
                    "change_details",
                    change_details.task_id,
                    change_details.url,
                    change_details.timestamp.isoformat(),
                    1,  # 变化详情默认成功
                    1,  # 变化详情默认有变化
                    data_json,
                ),
            )

            # 检查是否需要清理旧记录
            self._check_and_cleanup(cursor)

        return change_details.id

    def _check_and_cleanup(self, cursor):
        """检查并清理超出限制的旧记录"""
        cursor.execute("SELECT COUNT(*) FROM history_entries")
        count = cursor.fetchone()[0]

        if count > self.max_entries:
            # 删除最旧的记录，保留 max_entries 条
            delete_count = count - self.max_entries
            cursor.execute(
                """
                DELETE FROM history_entries
                WHERE id IN (
                    SELECT id FROM history_entries
                    ORDER BY timestamp ASC
                    LIMIT ?
                )
            """,
                (delete_count,),
            )

    def get_check_result(self, result_id: str) -> Optional[CheckResult]:
        """
        获取检测结果

        Args:
            result_id: 结果ID

        Returns:
            检测结果对象，不存在则返回None
        """
        with self._get_cursor() as cursor:
            cursor.execute(
                """
                SELECT data FROM history_entries
                WHERE id = ? AND type = 'check_result'
            """,
                (result_id,),
            )
            row = cursor.fetchone()

            if row:
                data = json.loads(row["data"])
                return CheckResult.from_dict(data)

        return None

    def get_change_details(self, details_id: str) -> Optional[ChangeDetails]:
        """
        获取变化详情

        Args:
            details_id: 详情ID

        Returns:
            变化详情对象，不存在则返回None
        """
        with self._get_cursor() as cursor:
            cursor.execute(
                """
                SELECT data FROM history_entries
                WHERE id = ? AND type = 'change_details'
            """,
                (details_id,),
            )
            row = cursor.fetchone()

            if row:
                data = json.loads(row["data"])
                return ChangeDetails.from_dict(data)

        return None

    def list_check_results(
        self, task_id: str = None, limit: int = 100, offset: int = 0
    ) -> List[CheckResult]:
        """
        列出检测结果

        Args:
            task_id: 任务ID（可选）
            limit: 返回结果数量限制
            offset: 偏移量

        Returns:
            检测结果列表
        """
        with self._get_cursor() as cursor:
            if task_id:
                cursor.execute(
                    """
                    SELECT data FROM history_entries
                    WHERE type = 'check_result' AND task_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ? OFFSET ?
                """,
                    (task_id, limit, offset),
                )
            else:
                cursor.execute(
                    """
                    SELECT data FROM history_entries
                    WHERE type = 'check_result'
                    ORDER BY timestamp DESC
                    LIMIT ? OFFSET ?
                """,
                    (limit, offset),
                )

            results = []
            for row in cursor.fetchall():
                try:
                    data = json.loads(row["data"])
                    results.append(CheckResult.from_dict(data))
                except Exception as e:
                    print(f"警告: 跳过无效的检测结果: {e}")

            return results

    def list_change_details(
        self, task_id: str = None, limit: int = 100, offset: int = 0
    ) -> List[ChangeDetails]:
        """
        列出变化详情

        Args:
            task_id: 任务ID（可选）
            limit: 返回结果数量限制
            offset: 偏移量

        Returns:
            变化详情列表
        """
        with self._get_cursor() as cursor:
            if task_id:
                cursor.execute(
                    """
                    SELECT data FROM history_entries
                    WHERE type = 'change_details' AND task_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ? OFFSET ?
                """,
                    (task_id, limit, offset),
                )
            else:
                cursor.execute(
                    """
                    SELECT data FROM history_entries
                    WHERE type = 'change_details'
                    ORDER BY timestamp DESC
                    LIMIT ? OFFSET ?
                """,
                    (limit, offset),
                )

            results = []
            for row in cursor.fetchall():
                try:
                    data = json.loads(row["data"])
                    results.append(ChangeDetails.from_dict(data))
                except Exception as e:
                    print(f"警告: 跳过无效的变化详情: {e}")

            return results

    def get_latest_check_result(self, task_id: str) -> Optional[CheckResult]:
        """获取最新的检测结果"""
        results = self.list_check_results(task_id=task_id, limit=1)
        return results[0] if results else None

    def get_latest_change_details(self, task_id: str) -> Optional[ChangeDetails]:
        """获取最新的变化详情"""
        details = self.list_change_details(task_id=task_id, limit=1)
        return details[0] if details else None

    def search_history(
        self,
        task_id: str = None,
        keyword: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        success_only: bool = False,
        changed_only: bool = False,
        entry_type: str = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        搜索历史记录

        Args:
            task_id: 任务ID（可选）
            keyword: 关键词搜索（可选）
            start_date: 开始日期（可选）
            end_date: 结束日期（可选）
            success_only: 只搜索成功的记录
            changed_only: 只搜索有变化的记录
            entry_type: 记录类型 (check_result/change_details)
            limit: 返回结果数量限制
            offset: 偏移量

        Returns:
            搜索结果列表
        """
        conditions = []
        params = []

        if task_id:
            conditions.append("task_id = ?")
            params.append(task_id)

        if entry_type:
            conditions.append("type = ?")
            params.append(entry_type)

        if start_date:
            conditions.append("timestamp >= ?")
            params.append(start_date.isoformat())

        if end_date:
            conditions.append("timestamp <= ?")
            params.append(end_date.isoformat())

        if success_only:
            conditions.append("success = 1")

        if changed_only:
            conditions.append("changed = 1")

        if keyword:
            # 在 URL 和 data 中搜索关键词
            conditions.append("(url LIKE ? OR data LIKE ?)")
            keyword_pattern = f"%{keyword}%"
            params.extend([keyword_pattern, keyword_pattern])

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        with self._get_cursor() as cursor:
            # 优化：只提取列表显示所需的字段，不加载完整的 data 列
            # 使用 JSON 提取函数获取摘要信息
            query = f"""
                SELECT
                    id, type, task_id, url, timestamp, success, changed,
                    json_extract(data, '$.changes_summary') as changes_summary,
                    json_extract(data, '$.change_summary') as change_summary,
                    json_extract(data, '$.ai_summary') as ai_summary,
                    json_extract(data, '$.error_message') as error_message,
                    json_extract(data, '$.change_type') as change_type
                FROM history_entries
                WHERE {where_clause}
                ORDER BY timestamp DESC
                LIMIT ? OFFSET ?
            """
            params.extend([limit, offset])
            cursor.execute(query, params)

            results = []
            for row in cursor.fetchall():
                try:
                    # 构建精简的 data 对象，只包含列表显示需要的字段
                    data = {
                        "changes_summary": row["changes_summary"],
                        "change_summary": row["change_summary"],
                        "ai_summary": row["ai_summary"],
                        "error_message": row["error_message"],
                        "change_type": row["change_type"],
                    }
                    results.append(
                        {
                            "id": row["id"],
                            "type": row["type"],
                            "task_id": row["task_id"],
                            "url": row["url"],
                            "timestamp": row["timestamp"],
                            "data": data,
                        }
                    )
                except Exception as e:
                    print(f"警告: 跳过无效的记录: {e}")

            return results

    def count_history(
        self,
        task_id: str = None,
        keyword: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        success_only: bool = False,
        changed_only: bool = False,
        entry_type: str = None,
    ) -> int:
        """
        统计历史记录数量

        Args:
            与 search_history 相同的筛选条件

        Returns:
            记录数量
        """
        conditions = []
        params = []

        if task_id:
            conditions.append("task_id = ?")
            params.append(task_id)

        if entry_type:
            conditions.append("type = ?")
            params.append(entry_type)

        if start_date:
            conditions.append("timestamp >= ?")
            params.append(start_date.isoformat())

        if end_date:
            conditions.append("timestamp <= ?")
            params.append(end_date.isoformat())

        if success_only:
            conditions.append("success = 1")

        if changed_only:
            conditions.append("changed = 1")

        if keyword:
            conditions.append("(url LIKE ? OR data LIKE ?)")
            keyword_pattern = f"%{keyword}%"
            params.extend([keyword_pattern, keyword_pattern])

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        with self._get_cursor() as cursor:
            query = f"SELECT COUNT(*) FROM history_entries WHERE {where_clause}"
            cursor.execute(query, params)
            return cursor.fetchone()[0]

    def get_history_statistics(self, task_id: str = None) -> Dict[str, Any]:
        """
        获取历史统计信息

        Args:
            task_id: 任务ID（可选）

        Returns:
            统计信息
        """
        with self._get_cursor() as cursor:
            task_condition = "task_id = ?" if task_id else "1=1"
            params = [task_id] if task_id else []

            # 总记录数
            cursor.execute(
                f"SELECT COUNT(*) FROM history_entries WHERE {task_condition}", params
            )
            total_entries = cursor.fetchone()[0]

            if total_entries == 0:
                return {
                    "total_entries": 0,
                    "check_results": 0,
                    "change_details": 0,
                    "success_rate": 0.0,
                    "change_rate": 0.0,
                    "first_date": None,
                    "last_date": None,
                }

            # 检测结果数
            cursor.execute(
                f"""
                SELECT COUNT(*) FROM history_entries
                WHERE type = 'check_result' AND {task_condition}
            """,
                params,
            )
            check_results = cursor.fetchone()[0]

            # 变化详情数
            cursor.execute(
                f"""
                SELECT COUNT(*) FROM history_entries
                WHERE type = 'change_details' AND {task_condition}
            """,
                params,
            )
            change_details = cursor.fetchone()[0]

            # 成功的检测数
            cursor.execute(
                f"""
                SELECT COUNT(*) FROM history_entries
                WHERE type = 'check_result' AND success = 1 AND {task_condition}
            """,
                params,
            )
            successful_checks = cursor.fetchone()[0]

            # 有变化的检测数
            cursor.execute(
                f"""
                SELECT COUNT(*) FROM history_entries
                WHERE type = 'check_result' AND changed = 1 AND {task_condition}
            """,
                params,
            )
            changed_checks = cursor.fetchone()[0]

            # 日期范围
            cursor.execute(
                f"""
                SELECT MIN(timestamp), MAX(timestamp) FROM history_entries
                WHERE {task_condition}
            """,
                params,
            )
            row = cursor.fetchone()
            first_date = row[0]
            last_date = row[1]

            # 计算比率
            success_rate = successful_checks / check_results if check_results > 0 else 0.0
            change_rate = changed_checks / check_results if check_results > 0 else 0.0

            return {
                "total_entries": total_entries,
                "check_results": check_results,
                "change_details": change_details,
                "success_rate": round(success_rate, 2),
                "change_rate": round(change_rate, 2),
                "first_date": first_date,
                "last_date": last_date,
            }

    def cleanup_old_entries(self, days: int = None) -> int:
        """
        清理旧的历史记录

        Args:
            days: 清理天数（可选）

        Returns:
            清理的条目数量
        """
        cleanup_days = days or self.auto_cleanup_days
        cutoff_date = datetime.now() - timedelta(days=cleanup_days)

        with self._get_cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM history_entries
                WHERE timestamp < ?
            """,
                (cutoff_date.isoformat(),),
            )
            removed_count = cursor.rowcount

        return removed_count

    def get_storage_info(self) -> Dict[str, Any]:
        """获取存储信息"""
        try:
            stat = self.db_path.stat()

            with self._get_cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM history_entries")
                total_entries = cursor.fetchone()[0]

                cursor.execute(
                    """
                    SELECT MIN(timestamp), MAX(timestamp) FROM history_entries
                """
                )
                row = cursor.fetchone()
                first_entry_date = row[0]
                last_entry_date = row[1]

            return {
                "file_path": str(self.db_path),
                "file_size": stat.st_size,
                "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "total_entries": total_entries,
                "first_entry_date": first_entry_date,
                "last_entry_date": last_entry_date,
                "max_entries": self.max_entries,
                "auto_cleanup_days": self.auto_cleanup_days,
                "storage_type": "sqlite",
            }
        except Exception as e:
            raise StorageError(f"获取存储信息失败: {e}")

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
