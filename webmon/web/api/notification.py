"""
通知管理 API 路由

提供通知测试等接口。
"""

import logging
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from ..schemas.common import SuccessResponse
from ...notification import NotificationService
from ...config import ConfigManager

router = APIRouter(prefix="/api/notification", tags=["通知管理"])
logger = logging.getLogger(__name__)

# 全局服务实例
_notification_service: Optional[NotificationService] = None


def get_notification_service() -> NotificationService:
    """获取通知服务实例"""
    global _notification_service
    if _notification_service is None:
        config_manager = ConfigManager()
        _notification_service = NotificationService(config_manager)
    return _notification_service


class TestNotificationRequest(BaseModel):
    """测试通知请求"""
    platform: Optional[str] = Field(None, description="要测试的平台名称，为空则测试所有启用的平台")
    title: Optional[str] = Field("WebMon 通知测试", description="测试通知标题")
    message: Optional[str] = Field(None, description="测试通知内容，为空则使用默认内容")


class PlatformTestResult(BaseModel):
    """平台测试结果"""
    platform: str = Field(..., description="平台名称")
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="结果消息")
    error: Optional[str] = Field(None, description="错误信息（如果失败）")


class TestNotificationResponse(BaseModel):
    """测试通知响应"""
    success: bool = Field(..., description="整体是否成功")
    message: str = Field(..., description="响应消息")
    results: List[PlatformTestResult] = Field(default_factory=list, description="各平台测试结果")
    total_platforms: int = Field(0, description="测试的平台总数")
    success_count: int = Field(0, description="成功的平台数")


@router.post(
    "/test",
    response_model=TestNotificationResponse,
    summary="测试通知",
    description="向指定平台或所有启用的平台发送测试通知",
)
async def test_notification(request: TestNotificationRequest):
    """发送测试通知"""
    try:
        service = get_notification_service()

        # 确定要测试的平台
        platforms_to_test = None
        if request.platform:
            platforms_to_test = [request.platform]

        # 构建测试消息
        title = request.title or "WebMon 通知测试"
        message = request.message or (
            "这是一条来自 WebMon 的测试通知。\n\n"
            "如果您收到此消息，说明通知服务配置正确。\n\n"
            "---\n"
            "WebMon 网页监控工具"
        )

        # 发送测试通知
        results = await service.send_notification(
            title=title,
            content=message,
            platforms=platforms_to_test,
            urgency="normal"
        )

        # 构建响应
        platform_results = []
        for platform_name, success in results.items():
            platform_results.append(PlatformTestResult(
                platform=platform_name,
                success=success,
                message="发送成功" if success else "发送失败",
                error=None if success else "平台返回错误或配置无效"
            ))

        total = len(platform_results)
        success_count = sum(1 for r in platform_results if r.success)

        return TestNotificationResponse(
            success=success_count > 0,
            message=f"测试完成，{success_count}/{total} 个平台发送成功",
            results=platform_results,
            total_platforms=total,
            success_count=success_count
        )

    except Exception as e:
        logger.error(f"测试通知失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/platforms",
    response_model=SuccessResponse,
    summary="获取可用平台",
    description="获取所有已启用的通知平台列表",
)
async def get_available_platforms():
    """获取可用的通知平台"""
    try:
        service = get_notification_service()

        # 获取启用的平台
        enabled_platforms = service.get_enabled_platforms()

        # 获取已配置的平台
        configured_platforms = service.get_configured_platforms()

        # 获取平台状态
        platform_status = service.get_platform_status()

        return SuccessResponse(
            success=True,
            message="获取成功",
            data={
                "enabled_platforms": enabled_platforms,
                "configured_platforms": configured_platforms,
                "platform_status": platform_status
            }
        )

    except Exception as e:
        logger.error(f"获取平台列表失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/platforms/{platform}/info",
    response_model=SuccessResponse,
    summary="获取平台信息",
    description="获取指定通知平台的详细信息",
)
async def get_platform_info(platform: str):
    """获取平台详细信息"""
    try:
        service = get_notification_service()

        # 获取平台信息
        info = service.get_platform_info(platform)

        if info is None:
            raise HTTPException(status_code=404, detail=f"平台 {platform} 不存在")

        return SuccessResponse(
            success=True,
            message="获取成功",
            data=info
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取平台信息失败 [{platform}]: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/test-all",
    response_model=TestNotificationResponse,
    summary="测试所有平台",
    description="测试所有已配置的通知平台（使用平台内置测试方法）",
)
async def test_all_platforms():
    """测试所有平台（使用内置测试方法）"""
    try:
        service = get_notification_service()

        # 调用平台测试方法
        results = await service.test_platforms()

        # 构建响应
        platform_results = []
        for platform_name, result in results.items():
            success = result.get('success', False)
            message = result.get('message', '')
            error = result.get('error') if not success else None

            platform_results.append(PlatformTestResult(
                platform=platform_name,
                success=success,
                message=message,
                error=error
            ))

        total = len(platform_results)
        success_count = sum(1 for r in platform_results if r.success)

        return TestNotificationResponse(
            success=success_count > 0 or total == 0,
            message=f"测试完成，{success_count}/{total} 个平台测试通过" if total > 0 else "没有已配置的平台",
            results=platform_results,
            total_platforms=total,
            success_count=success_count
        )

    except Exception as e:
        logger.error(f"测试所有平台失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
