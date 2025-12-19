"""
历史记录 API 路由

提供历史记录查询的 RESTful API 端点。
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Depends

from webmon.web.schemas.history import (
    HistoryListResponse,
    HistoryEntryResponse,
    HistoryStatisticsResponse,
    StorageInfoResponse,
    CheckResultResponse,
    ChangeDetailsResponse,
)
from webmon.web.services.history_service import HistoryService, get_history_service

router = APIRouter(prefix="/api/history", tags=["history"])


def entry_to_response(entry: dict) -> HistoryEntryResponse:
    """将历史记录条目转换为响应模型"""
    return HistoryEntryResponse(
        id=entry.get('id', ''),
        type=entry.get('type', ''),
        task_id=entry.get('task_id', ''),
        url=entry.get('url', ''),
        timestamp=entry.get('timestamp', ''),
        data=entry.get('data', {})
    )


@router.get(
    "",
    response_model=HistoryListResponse,
    summary="获取历史记录列表",
    description="获取历史记录列表，支持分页和筛选"
)
async def list_history(
    task_id: Optional[str] = Query(None, description="按任务ID筛选"),
    entry_type: Optional[str] = Query(None, description="按记录类型筛选: check_result/change_details"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    service: HistoryService = Depends(get_history_service)
) -> HistoryListResponse:
    """获取历史记录列表"""
    try:
        result = service.list_entries(
            task_id=task_id,
            entry_type=entry_type,
            page=page,
            page_size=page_size
        )

        items = [entry_to_response(e) for e in result['items']]

        return HistoryListResponse(
            items=items,
            total=result['total'],
            page=result['page'],
            page_size=result['page_size'],
            total_pages=result['total_pages']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取历史记录失败: {str(e)}")


@router.get(
    "/search",
    response_model=HistoryListResponse,
    summary="搜索历史记录",
    description="根据条件搜索历史记录，支持关键词、日期范围等筛选"
)
async def search_history(
    task_id: Optional[str] = Query(None, description="按任务ID筛选"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    start_date: Optional[str] = Query(None, description="开始日期 (ISO格式)"),
    end_date: Optional[str] = Query(None, description="结束日期 (ISO格式)"),
    success_only: bool = Query(False, description="只显示成功的记录"),
    changed_only: bool = Query(False, description="只显示有变化的记录"),
    entry_type: Optional[str] = Query(None, description="记录类型筛选: check_result/change_details"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    service: HistoryService = Depends(get_history_service)
) -> HistoryListResponse:
    """搜索历史记录"""
    try:
        result = service.search_entries(
            task_id=task_id,
            keyword=keyword,
            start_date=start_date,
            end_date=end_date,
            success_only=success_only,
            changed_only=changed_only,
            entry_type=entry_type,
            page=page,
            page_size=page_size
        )

        items = [entry_to_response(e) for e in result['items']]

        return HistoryListResponse(
            items=items,
            total=result['total'],
            page=result['page'],
            page_size=result['page_size'],
            total_pages=result['total_pages']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索历史记录失败: {str(e)}")


@router.get(
    "/statistics",
    response_model=HistoryStatisticsResponse,
    summary="获取历史统计信息",
    description="获取历史记录的统计数据，如成功率、变化率等"
)
async def get_statistics(
    task_id: Optional[str] = Query(None, description="按任务ID筛选"),
    service: HistoryService = Depends(get_history_service)
) -> HistoryStatisticsResponse:
    """获取历史统计信息"""
    try:
        stats = service.get_statistics(task_id=task_id)
        return HistoryStatisticsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")


@router.get(
    "/storage",
    response_model=StorageInfoResponse,
    summary="获取存储信息",
    description="获取历史记录存储的详细信息"
)
async def get_storage_info(
    service: HistoryService = Depends(get_history_service)
) -> StorageInfoResponse:
    """获取存储信息"""
    try:
        info = service.get_storage_info()
        return StorageInfoResponse(**info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取存储信息失败: {str(e)}")


@router.get(
    "/recent-changes",
    response_model=HistoryListResponse,
    summary="获取最近的变化记录",
    description="获取最近检测到的变化记录"
)
async def get_recent_changes(
    limit: int = Query(10, ge=1, le=100, description="返回数量限制"),
    service: HistoryService = Depends(get_history_service)
) -> HistoryListResponse:
    """获取最近的变化记录"""
    try:
        entries = service.get_recent_changes(limit=limit)
        items = [entry_to_response(e) for e in entries]

        return HistoryListResponse(
            items=items,
            total=len(items),
            page=1,
            page_size=limit,
            total_pages=1
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取最近变化记录失败: {str(e)}")


@router.get(
    "/check-results",
    summary="获取检测结果列表",
    description="获取检测结果列表，支持分页和任务筛选"
)
async def list_check_results(
    task_id: Optional[str] = Query(None, description="按任务ID筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    service: HistoryService = Depends(get_history_service)
):
    """获取检测结果列表"""
    try:
        result = service.list_check_results(
            task_id=task_id,
            page=page,
            page_size=page_size
        )

        return {
            'items': result['items'],
            'total': result['total'],
            'page': result['page'],
            'page_size': result['page_size'],
            'total_pages': result['total_pages']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取检测结果失败: {str(e)}")


@router.get(
    "/change-details",
    summary="获取变化详情列表",
    description="获取变化详情列表，支持分页和任务筛选"
)
async def list_change_details(
    task_id: Optional[str] = Query(None, description="按任务ID筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    service: HistoryService = Depends(get_history_service)
):
    """获取变化详情列表"""
    try:
        result = service.list_change_details(
            task_id=task_id,
            page=page,
            page_size=page_size
        )

        return {
            'items': result['items'],
            'total': result['total'],
            'page': result['page'],
            'page_size': result['page_size'],
            'total_pages': result['total_pages']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取变化详情失败: {str(e)}")


@router.get(
    "/entry/{entry_id}",
    response_model=HistoryEntryResponse,
    summary="获取历史记录详情",
    description="根据ID获取单条历史记录的详细信息"
)
async def get_entry(
    entry_id: str,
    service: HistoryService = Depends(get_history_service)
) -> HistoryEntryResponse:
    """获取历史记录详情"""
    try:
        entry = service.get_entry(entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail=f"历史记录不存在: {entry_id}")

        return entry_to_response(entry)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取历史记录失败: {str(e)}")


@router.get(
    "/check-results/{result_id}",
    response_model=CheckResultResponse,
    summary="获取检测结果详情",
    description="根据ID获取检测结果的详细信息"
)
async def get_check_result(
    result_id: str,
    service: HistoryService = Depends(get_history_service)
) -> CheckResultResponse:
    """获取检测结果详情"""
    try:
        result = service.get_check_result(result_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"检测结果不存在: {result_id}")

        return CheckResultResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取检测结果失败: {str(e)}")


@router.get(
    "/change-details/{details_id}",
    response_model=ChangeDetailsResponse,
    summary="获取变化详情",
    description="根据ID获取变化详情的详细信息"
)
async def get_change_details_by_id(
    details_id: str,
    service: HistoryService = Depends(get_history_service)
) -> ChangeDetailsResponse:
    """获取变化详情"""
    try:
        details = service.get_change_details(details_id)
        if not details:
            raise HTTPException(status_code=404, detail=f"变化详情不存在: {details_id}")

        return ChangeDetailsResponse(**details)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取变化详情失败: {str(e)}")


@router.delete(
    "/cleanup",
    summary="清理旧的历史记录",
    description="清理指定天数之前的历史记录"
)
async def cleanup_history(
    days: Optional[int] = Query(None, ge=1, description="清理多少天前的记录（默认使用配置值）"),
    service: HistoryService = Depends(get_history_service)
):
    """清理旧的历史记录"""
    try:
        removed_count = service.cleanup_old_entries(days=days)
        return {
            'success': True,
            'message': f"已清理 {removed_count} 条历史记录",
            'removed_count': removed_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清理历史记录失败: {str(e)}")
