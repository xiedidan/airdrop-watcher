"""
历史记录存储管理器

负责历史记录的管理，处理data/history.json文件
"""
import json
import os
import shutil
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from pathlib import Path

from ..models.check_result import CheckResult
from ..models.change_details import ChangeDetails
from ..exceptions import StorageError


class HistoryStorage:
    """历史记录存储管理器"""
    
    def __init__(self, history_file: str = "data/history.json", max_entries: int = 1000, 
                 auto_cleanup_days: int = 30):
        """
        初始化历史记录存储管理器
        
        Args:
            history_file: 历史记录文件路径
            max_entries: 最大历史记录条目数
            auto_cleanup_days: 自动清理天数
        """
        self.history_file = Path(history_file)
        self.max_entries = max_entries
        self.auto_cleanup_days = auto_cleanup_days
        
        # 确保数据目录存在
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 初始化历史记录文件（如果不存在）
        if not self.history_file.exists():
            self._init_history_file()
    
    def _init_history_file(self):
        """初始化历史记录文件"""
        default_history = {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "metadata": {
                "total_entries": 0,
                "first_entry_date": None,
                "last_entry_date": None
            },
            "entries": []
        }
        
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(default_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise StorageError(f"创建历史记录文件失败: {e}")
    
    def _load_history(self) -> Dict[str, Any]:
        """加载历史记录"""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise StorageError(f"历史记录文件不存在: {self.history_file}")
        except json.JSONDecodeError as e:
            raise StorageError(f"历史记录文件格式错误: {e}")
        except Exception as e:
            raise StorageError(f"加载历史记录文件失败: {e}")
    
    def _save_history(self, history: Dict[str, Any]):
        """保存历史记录"""
        try:
            # 更新元数据
            entries = history.get("entries", [])
            if entries:
                history["metadata"]["total_entries"] = len(entries)
                history["metadata"]["first_entry_date"] = entries[0].get("timestamp")
                history["metadata"]["last_entry_date"] = entries[-1].get("timestamp")
            else:
                history["metadata"]["total_entries"] = 0
                history["metadata"]["first_entry_date"] = None
                history["metadata"]["last_entry_date"] = None
            
            # 更新修改时间
            history["updated_at"] = datetime.now().isoformat()
            
            # 保存历史记录
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            raise StorageError(f"保存历史记录文件失败: {e}")
    
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
        history = self._load_history()
        entries = history.get("entries", [])
        
        # 添加新记录
        entry = {
            "id": check_result.id,
            "type": "check_result",
            "task_id": check_result.task_id,
            "url": check_result.url,
            "timestamp": check_result.timestamp.isoformat(),
            "data": check_result.to_dict()
        }
        
        entries.append(entry)
        
        # 保持最大条目数限制
        if len(entries) > self.max_entries:
            entries = entries[-self.max_entries:]
        
        history["entries"] = entries
        
        # 保存历史记录
        self._save_history(history)
        
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
        history = self._load_history()
        entries = history.get("entries", [])
        
        # 添加新记录
        entry = {
            "id": change_details.id,
            "type": "change_details",
            "task_id": change_details.task_id,
            "url": change_details.url,
            "timestamp": change_details.timestamp.isoformat(),
            "data": change_details.to_dict()
        }
        
        entries.append(entry)
        
        # 保持最大条目数限制
        if len(entries) > self.max_entries:
            entries = entries[-self.max_entries:]
        
        history["entries"] = entries
        
        # 保存历史记录
        self._save_history(history)
        
        return change_details.id
    
    def get_check_result(self, result_id: str) -> Optional[CheckResult]:
        """
        获取检测结果
        
        Args:
            result_id: 结果ID
            
        Returns:
            检测结果对象，不存在则返回None
            
        Raises:
            StorageError: 存储错误
        """
        history = self._load_history()
        entries = history.get("entries", [])
        
        for entry in entries:
            if (entry.get("id") == result_id and 
                entry.get("type") == "check_result"):
                try:
                    data = entry.get("data", {})
                    return CheckResult.from_dict(data)
                except Exception as e:
                    raise StorageError(f"解析检测结果失败: {e}")
        
        return None
    
    def get_change_details(self, details_id: str) -> Optional[ChangeDetails]:
        """
        获取变化详情
        
        Args:
            details_id: 详情ID
            
        Returns:
            变化详情对象，不存在则返回None
            
        Raises:
            StorageError: 存储错误
        """
        history = self._load_history()
        entries = history.get("entries", [])
        
        for entry in entries:
            if (entry.get("id") == details_id and 
                entry.get("type") == "change_details"):
                try:
                    data = entry.get("data", {})
                    return ChangeDetails.from_dict(data)
                except Exception as e:
                    raise StorageError(f"解析变化详情失败: {e}")
        
        return None
    
    def list_check_results(self, task_id: str = None, limit: int = 100, 
                          offset: int = 0) -> List[CheckResult]:
        """
        列出检测结果
        
        Args:
            task_id: 任务ID（可选，用于筛选特定任务）
            limit: 返回结果数量限制
            offset: 偏移量
            
        Returns:
            检测结果列表
            
        Raises:
            StorageError: 存储错误
        """
        history = self._load_history()
        entries = history.get("entries", [])
        
        # 筛选检测结果
        check_results = []
        for entry in reversed(entries):  # 按时间倒序
            if (entry.get("type") == "check_result" and 
                (task_id is None or entry.get("task_id") == task_id)):
                try:
                    data = entry.get("data", {})
                    check_result = CheckResult.from_dict(data)
                    check_results.append(check_result)
                except Exception as e:
                    print(f"警告: 跳过无效的检测结果: {e}")
                    continue
        
        # 应用分页
        start = offset
        end = offset + limit
        return check_results[start:end]
    
    def list_change_details(self, task_id: str = None, limit: int = 100, 
                           offset: int = 0) -> List[ChangeDetails]:
        """
        列出变化详情
        
        Args:
            task_id: 任务ID（可选，用于筛选特定任务）
            limit: 返回结果数量限制
            offset: 偏移量
            
        Returns:
            变化详情列表
            
        Raises:
            StorageError: 存储错误
        """
        history = self._load_history()
        entries = history.get("entries", [])
        
        # 筛选变化详情
        change_details = []
        for entry in reversed(entries):  # 按时间倒序
            if (entry.get("type") == "change_details" and 
                (task_id is None or entry.get("task_id") == task_id)):
                try:
                    data = entry.get("data", {})
                    details = ChangeDetails.from_dict(data)
                    change_details.append(details)
                except Exception as e:
                    print(f"警告: 跳过无效的变化详情: {e}")
                    continue
        
        # 应用分页
        start = offset
        end = offset + limit
        return change_details[start:end]
    
    def get_latest_check_result(self, task_id: str) -> Optional[CheckResult]:
        """
        获取最新的检测结果
        
        Args:
            task_id: 任务ID
            
        Returns:
            最新的检测结果，不存在则返回None
            
        Raises:
            StorageError: 存储错误
        """
        results = self.list_check_results(task_id=task_id, limit=1)
        return results[0] if results else None
    
    def get_latest_change_details(self, task_id: str) -> Optional[ChangeDetails]:
        """
        获取最新的变化详情
        
        Args:
            task_id: 任务ID
            
        Returns:
            最新的变化详情，不存在则返回None
            
        Raises:
            StorageError: 存储错误
        """
        details = self.list_change_details(task_id=task_id, limit=1)
        return details[0] if details else None
    
    def get_history_statistics(self, task_id: str = None) -> Dict[str, Any]:
        """
        获取历史统计信息
        
        Args:
            task_id: 任务ID（可选，用于统计特定任务）
            
        Returns:
            统计信息
            
        Raises:
            StorageError: 存储错误
        """
        history = self._load_history()
        entries = history.get("entries", [])
        
        # 筛选相关条目
        relevant_entries = []
        for entry in entries:
            if task_id is None or entry.get("task_id") == task_id:
                relevant_entries.append(entry)
        
        if not relevant_entries:
            return {
                "total_entries": 0,
                "check_results": 0,
                "change_details": 0,
                "success_rate": 0.0,
                "change_rate": 0.0,
                "first_date": None,
                "last_date": None
            }
        
        # 计算统计信息
        check_results = [e for e in relevant_entries if e.get("type") == "check_result"]
        change_details = [e for e in relevant_entries if e.get("type") == "change_details"]
        
        # 计算成功率
        successful_checks = [e for e in check_results if e.get("data", {}).get("success", False)]
        success_rate = len(successful_checks) / len(check_results) if check_results else 0.0
        
        # 计算变化率
        changed_checks = [e for e in check_results if e.get("data", {}).get("changed", False)]
        change_rate = len(changed_checks) / len(check_results) if check_results else 0.0
        
        # 获取日期范围
        timestamps = [e.get("timestamp") for e in relevant_entries if e.get("timestamp")]
        first_date = min(timestamps) if timestamps else None
        last_date = max(timestamps) if timestamps else None
        
        return {
            "total_entries": len(relevant_entries),
            "check_results": len(check_results),
            "change_details": len(change_details),
            "success_rate": round(success_rate, 2),
            "change_rate": round(change_rate, 2),
            "first_date": first_date,
            "last_date": last_date
        }
    
    def cleanup_old_entries(self, days: int = None) -> int:
        """
        清理旧的历史记录
        
        Args:
            days: 清理天数（可选，默认使用auto_cleanup_days）
            
        Returns:
            清理的条目数量
            
        Raises:
            StorageError: 存储错误
        """
        cleanup_days = days or self.auto_cleanup_days
        cutoff_date = datetime.now() - timedelta(days=cleanup_days)
        
        history = self._load_history()
        entries = history.get("entries", [])
        
        # 筛选要保留的条目
        remaining_entries = []
        removed_count = 0
        
        for entry in entries:
            entry_date = None
            if entry.get("timestamp"):
                try:
                    entry_date = datetime.fromisoformat(entry.get("timestamp"))
                except:
                    pass
            
            # 保留最近的历史记录
            if entry_date and entry_date >= cutoff_date:
                remaining_entries.append(entry)
            else:
                removed_count += 1
        
        # 保存清理后的历史记录
        history["entries"] = remaining_entries
        self._save_history(history)
        
        return removed_count
    
    def search_history(self, task_id: str = None, keyword: str = None, 
                      start_date: datetime = None, end_date: datetime = None,
                      success_only: bool = False, changed_only: bool = False,
                      limit: int = 100) -> List[Dict[str, Any]]:
        """
        搜索历史记录
        
        Args:
            task_id: 任务ID（可选）
            keyword: 关键词搜索（可选）
            start_date: 开始日期（可选）
            end_date: 结束日期（可选）
            success_only: 只搜索成功的记录
            changed_only: 只搜索有变化的记录
            limit: 返回结果数量限制
            
        Returns:
            搜索结果列表
            
        Raises:
            StorageError: 存储错误
        """
        history = self._load_history()
        entries = history.get("entries", [])
        
        results = []
        for entry in reversed(entries):  # 按时间倒序
            # 应用筛选条件
            if task_id and entry.get("task_id") != task_id:
                continue
            
            # 日期范围筛选
            if entry.get("timestamp"):
                try:
                    entry_date = datetime.fromisoformat(entry.get("timestamp"))
                    if start_date and entry_date < start_date:
                        continue
                    if end_date and entry_date > end_date:
                        continue
                except:
                    pass
            
            # 数据内容筛选
            data = entry.get("data", {})
            
            if success_only and not data.get("success", False):
                continue
            
            if changed_only and not data.get("changed", False):
                continue
            
            # 关键词搜索
            if keyword:
                keyword_lower = keyword.lower()
                search_text = f"{entry.get('url', '')} {entry.get('type', '')}"
                if entry.get("type") == "check_result":
                    search_text += f" {data.get('error_message', '')} {str(data.get('extracted_data', ''))}"
                elif entry.get("type") == "change_details":
                    search_text += f" {data.get('change_summary', '')} {str(data.get('changes', ''))}"
                
                if keyword_lower not in search_text.lower():
                    continue
            
            results.append(entry)
            
            if len(results) >= limit:
                break
        
        return results
    
    def export_history(self, file_path: str, format: str = "json", 
                      task_id: str = None, start_date: datetime = None, 
                      end_date: datetime = None) -> str:
        """
        导出历史记录
        
        Args:
            file_path: 导出文件路径
            format: 导出格式 (json/csv)
            task_id: 任务ID（可选，导出特定任务）
            start_date: 开始日期（可选）
            end_date: 结束日期（可选）
            
        Returns:
            导出文件路径
            
        Raises:
            StorageError: 存储错误
        """
        # 搜索相关历史记录
        entries = self.search_history(
            task_id=task_id,
            start_date=start_date,
            end_date=end_date,
            limit=self.max_entries
        )
        
        export_data = {
            "version": "1.0.0",
            "exported_at": datetime.now().isoformat(),
            "total_entries": len(entries),
            "metadata": {
                "task_id": task_id,
                "start_date": start_date.isoformat() if start_date else None,
                "end_date": end_date.isoformat() if end_date else None
            },
            "entries": entries
        }
        
        if format.lower() == "json":
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
            except Exception as e:
                raise StorageError(f"导出历史记录失败: {e}")
        else:
            raise ValueError(f"不支持的导出格式: {format}")
        
        return file_path
    
    def get_storage_info(self) -> Dict[str, Any]:
        """
        获取存储信息
        
        Returns:
            存储信息
            
        Raises:
            StorageError: 存储错误
        """
        try:
            stat = self.history_file.stat()
            history = self._load_history()
            metadata = history.get("metadata", {})
            
            return {
                "file_path": str(self.history_file),
                "file_size": stat.st_size,
                "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "total_entries": metadata.get("total_entries", 0),
                "first_entry_date": metadata.get("first_entry_date"),
                "last_entry_date": metadata.get("last_entry_date"),
                "max_entries": self.max_entries,
                "auto_cleanup_days": self.auto_cleanup_days
            }
        except Exception as e:
            raise StorageError(f"获取存储信息失败: {e}")