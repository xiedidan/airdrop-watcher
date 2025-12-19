"""
历史记录服务层

封装历史记录管理的业务逻辑，与 HistoryStorage 交互。
"""

import math
from datetime import datetime
from typing import List, Optional, Dict, Any

from webmon.storage.history_storage import HistoryStorage
from webmon.models.check_result import CheckResult
from webmon.models.change_details import ChangeDetails


class HistoryService:
    """历史记录管理服务"""

    _instance: Optional['HistoryService'] = None
    _storage: Optional[HistoryStorage] = None

    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_storage(cls) -> HistoryStorage:
        """获取存储实例"""
        if cls._storage is None:
            cls._storage = HistoryStorage()
        return cls._storage

    @classmethod
    def set_storage(cls, storage: HistoryStorage):
        """设置存储实例（用于测试）"""
        cls._storage = storage

    def list_entries(
        self,
        task_id: Optional[str] = None,
        entry_type: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """
        获取历史记录列表

        Args:
            task_id: 按任务ID筛选
            entry_type: 按记录类型筛选 (check_result/change_details)
            page: 页码
            page_size: 每页数量

        Returns:
            包含分页信息的历史记录列表
        """
        storage = self.get_storage()

        # 使用 search_history 获取所有相关记录
        all_entries = storage.search_history(
            task_id=task_id,
            limit=10000  # 获取足够多的记录用于分页
        )

        # 按类型筛选
        if entry_type:
            all_entries = [e for e in all_entries if e.get('type') == entry_type]

        # 计算分页
        total = len(all_entries)
        total_pages = math.ceil(total / page_size) if total > 0 else 1

        # 计算偏移量
        offset = (page - 1) * page_size
        items = all_entries[offset:offset + page_size]

        return {
            'items': items,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages
        }

    def search_entries(
        self,
        task_id: Optional[str] = None,
        keyword: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        success_only: bool = False,
        changed_only: bool = False,
        entry_type: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """
        搜索历史记录

        Args:
            task_id: 按任务ID筛选
            keyword: 关键词搜索
            start_date: 开始日期 (ISO格式)
            end_date: 结束日期 (ISO格式)
            success_only: 只显示成功的记录
            changed_only: 只显示有变化的记录
            entry_type: 记录类型筛选
            page: 页码
            page_size: 每页数量

        Returns:
            包含分页信息的搜索结果
        """
        storage = self.get_storage()

        # 解析日期
        start_dt = None
        end_dt = None
        if start_date:
            try:
                start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                pass
        if end_date:
            try:
                end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                pass

        # 搜索记录
        all_entries = storage.search_history(
            task_id=task_id,
            keyword=keyword,
            start_date=start_dt,
            end_date=end_dt,
            success_only=success_only,
            changed_only=changed_only,
            limit=10000
        )

        # 按类型筛选
        if entry_type:
            all_entries = [e for e in all_entries if e.get('type') == entry_type]

        # 计算分页
        total = len(all_entries)
        total_pages = math.ceil(total / page_size) if total > 0 else 1

        # 计算偏移量
        offset = (page - 1) * page_size
        items = all_entries[offset:offset + page_size]

        return {
            'items': items,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages
        }

    def get_check_result(self, result_id: str) -> Optional[Dict[str, Any]]:
        """
        获取检测结果详情

        Args:
            result_id: 结果ID

        Returns:
            检测结果数据，不存在返回None
        """
        storage = self.get_storage()
        result = storage.get_check_result(result_id)
        if result:
            return result.to_dict()
        return None

    def get_change_details(self, details_id: str) -> Optional[Dict[str, Any]]:
        """
        获取变化详情

        Args:
            details_id: 详情ID

        Returns:
            变化详情数据，不存在返回None
        """
        storage = self.get_storage()
        details = storage.get_change_details(details_id)
        if details:
            return details.to_dict()
        return None

    def get_entry(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """
        获取历史记录条目（自动判断类型）

        Args:
            entry_id: 条目ID

        Returns:
            条目数据，不存在返回None
        """
        # 先尝试作为检测结果获取
        result = self.get_check_result(entry_id)
        if result:
            return {
                'id': entry_id,
                'type': 'check_result',
                'task_id': result.get('task_id', ''),
                'url': result.get('url', ''),
                'timestamp': result.get('timestamp', ''),
                'data': result
            }

        # 再尝试作为变化详情获取
        details = self.get_change_details(entry_id)
        if details:
            return {
                'id': entry_id,
                'type': 'change_details',
                'task_id': details.get('task_id', ''),
                'url': details.get('url', ''),
                'timestamp': details.get('timestamp', ''),
                'data': details
            }

        return None

    def get_statistics(self, task_id: Optional[str] = None) -> Dict[str, Any]:
        """
        获取历史统计信息

        Args:
            task_id: 按任务ID筛选

        Returns:
            统计信息
        """
        storage = self.get_storage()
        return storage.get_history_statistics(task_id=task_id)

    def get_storage_info(self) -> Dict[str, Any]:
        """
        获取存储信息

        Returns:
            存储信息
        """
        storage = self.get_storage()
        return storage.get_storage_info()

    def list_check_results(
        self,
        task_id: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """
        获取检测结果列表

        Args:
            task_id: 按任务ID筛选
            page: 页码
            page_size: 每页数量

        Returns:
            包含分页信息的检测结果列表
        """
        storage = self.get_storage()

        # 获取所有检测结果
        offset = (page - 1) * page_size
        results = storage.list_check_results(
            task_id=task_id,
            limit=page_size,
            offset=offset
        )

        # 获取总数（需要额外查询）
        all_results = storage.list_check_results(task_id=task_id, limit=10000)
        total = len(all_results)
        total_pages = math.ceil(total / page_size) if total > 0 else 1

        # 转换为字典格式
        items = [r.to_dict() for r in results]

        return {
            'items': items,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages
        }

    def list_change_details(
        self,
        task_id: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """
        获取变化详情列表

        Args:
            task_id: 按任务ID筛选
            page: 页码
            page_size: 每页数量

        Returns:
            包含分页信息的变化详情列表
        """
        storage = self.get_storage()

        # 获取所有变化详情
        offset = (page - 1) * page_size
        details = storage.list_change_details(
            task_id=task_id,
            limit=page_size,
            offset=offset
        )

        # 获取总数
        all_details = storage.list_change_details(task_id=task_id, limit=10000)
        total = len(all_details)
        total_pages = math.ceil(total / page_size) if total > 0 else 1

        # 转换为字典格式
        items = [d.to_dict() for d in details]

        return {
            'items': items,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages
        }

    def get_recent_changes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取最近的变化记录

        Args:
            limit: 返回数量限制

        Returns:
            最近的变化记录列表
        """
        storage = self.get_storage()

        # 搜索有变化的记录
        entries = storage.search_history(
            changed_only=True,
            limit=limit
        )

        return entries

    def cleanup_old_entries(self, days: Optional[int] = None) -> int:
        """
        清理旧的历史记录

        Args:
            days: 清理天数（可选）

        Returns:
            清理的条目数量
        """
        storage = self.get_storage()
        return storage.cleanup_old_entries(days=days)


# 全局服务实例
history_service = HistoryService()


def get_history_service() -> HistoryService:
    """获取历史记录服务实例"""
    return history_service
