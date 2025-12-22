"""
配置管理 API 路由

提供系统配置的读写接口。
"""

import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Query

from ..schemas.settings import (
    SettingsResponse,
    SettingsSectionResponse,
    MonitoringConfigUpdate,
    DetectionConfigUpdate,
    NotificationConfigUpdate,
    AIConfigUpdate,
    StorageConfigUpdate,
    LoggingConfigUpdate,
    SchedulerConfigUpdate,
)
from ..schemas.common import SuccessResponse, ErrorResponse
from ..services.settings_service import get_settings_service

router = APIRouter(prefix="/api/settings", tags=["配置管理"])
logger = logging.getLogger(__name__)


@router.get(
    "",
    response_model=SettingsResponse,
    summary="获取所有配置",
    description="获取系统所有配置段的当前值",
)
async def get_all_settings(
    mask_secrets: bool = Query(True, description="是否掩码敏感信息")
):
    """获取所有配置"""
    try:
        service = get_settings_service()
        settings = service.get_all_settings(mask_secrets=mask_secrets)

        return SettingsResponse(
            success=True,
            message="获取成功",
            data=settings
        )

    except Exception as e:
        logger.error(f"获取配置失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{section}",
    response_model=SettingsSectionResponse,
    summary="获取指定配置段",
    description="获取指定配置段的当前值。支持的配置段：monitoring, detection, notification, ai, storage, logging, scheduler",
)
async def get_section(
    section: str,
    mask_secrets: bool = Query(True, description="是否掩码敏感信息")
):
    """获取指定配置段"""
    try:
        service = get_settings_service()
        config = service.get_section(section, mask_secrets=mask_secrets)

        return SettingsSectionResponse(
            success=True,
            message="获取成功",
            section=section,
            data=config
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"获取配置段失败 [{section}]: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/monitoring",
    response_model=SuccessResponse,
    summary="更新监控配置",
    description="更新监控相关配置，如默认检测间隔、超时时间、并发数等",
)
async def update_monitoring(config: MonitoringConfigUpdate):
    """更新监控配置"""
    try:
        service = get_settings_service()

        # 过滤掉 None 值
        updates = {k: v for k, v in config.model_dump().items() if v is not None}

        if not updates:
            return SuccessResponse(
                success=True,
                message="无更新内容"
            )

        success = service.update_section("monitoring", updates)

        if success:
            return SuccessResponse(
                success=True,
                message="监控配置已更新",
                data=service.get_section("monitoring")
            )
        else:
            raise HTTPException(status_code=500, detail="更新失败")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新监控配置失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/detection",
    response_model=SuccessResponse,
    summary="更新检测配置",
    description="更新变化检测相关配置，如相似度阈值、忽略选择器等",
)
async def update_detection(config: DetectionConfigUpdate):
    """更新检测配置"""
    try:
        service = get_settings_service()
        updates = {k: v for k, v in config.model_dump().items() if v is not None}

        if not updates:
            return SuccessResponse(success=True, message="无更新内容")

        success = service.update_section("detection", updates)

        if success:
            return SuccessResponse(
                success=True,
                message="检测配置已更新",
                data=service.get_section("detection")
            )
        else:
            raise HTTPException(status_code=500, detail="更新失败")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新检测配置失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/notification",
    response_model=SuccessResponse,
    summary="更新通知配置",
    description="更新通知相关配置，如启用的平台、模板等",
)
async def update_notification(config: NotificationConfigUpdate):
    """更新通知配置"""
    try:
        service = get_settings_service()
        updates = {k: v for k, v in config.model_dump().items() if v is not None}

        if not updates:
            return SuccessResponse(success=True, message="无更新内容")

        success = service.update_section("notification", updates)

        if success:
            return SuccessResponse(
                success=True,
                message="通知配置已更新",
                data=service.get_section("notification")
            )
        else:
            raise HTTPException(status_code=500, detail="更新失败")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新通知配置失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/notification/platforms",
    response_model=SuccessResponse,
    summary="获取通知平台列表",
    description="获取所有通知平台及其配置状态",
)
async def get_notification_platforms():
    """获取通知平台列表"""
    try:
        service = get_settings_service()
        platforms = service.get_notification_platforms()

        return SuccessResponse(
            success=True,
            message="获取成功",
            data={"platforms": platforms}
        )

    except Exception as e:
        logger.error(f"获取通知平台失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/notification/platforms/{platform}",
    response_model=SuccessResponse,
    summary="更新单个平台配置",
    description="更新指定通知平台的配置",
)
async def update_platform_config(
    platform: str,
    config: dict,
    enable: Optional[bool] = Query(None, description="是否启用该平台")
):
    """更新单个平台配置"""
    try:
        service = get_settings_service()
        success = service.update_platform_config(platform, config, enable)

        if success:
            return SuccessResponse(
                success=True,
                message=f"平台 {platform} 配置已更新"
            )
        else:
            raise HTTPException(status_code=500, detail="更新失败")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新平台配置失败 [{platform}]: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/ai",
    response_model=SuccessResponse,
    summary="更新 AI 配置",
    description="更新 AI 分析相关配置，如 API 地址、模型、提示词等",
)
async def update_ai(config: AIConfigUpdate):
    """更新 AI 配置"""
    try:
        service = get_settings_service()
        updates = {k: v for k, v in config.model_dump().items() if v is not None}

        if not updates:
            return SuccessResponse(success=True, message="无更新内容")

        success = service.update_section("ai", updates)

        if success:
            return SuccessResponse(
                success=True,
                message="AI 配置已更新",
                data=service.get_section("ai")
            )
        else:
            raise HTTPException(status_code=500, detail="更新失败")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新 AI 配置失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/storage",
    response_model=SuccessResponse,
    summary="更新存储配置",
    description="更新存储相关配置，如历史记录文件路径、保留天数等",
)
async def update_storage(config: StorageConfigUpdate):
    """更新存储配置"""
    try:
        service = get_settings_service()
        updates = {k: v for k, v in config.model_dump().items() if v is not None}

        if not updates:
            return SuccessResponse(success=True, message="无更新内容")

        success = service.update_section("storage", updates)

        if success:
            return SuccessResponse(
                success=True,
                message="存储配置已更新",
                data=service.get_section("storage")
            )
        else:
            raise HTTPException(status_code=500, detail="更新失败")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新存储配置失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/logging",
    response_model=SuccessResponse,
    summary="更新日志配置",
    description="更新日志相关配置，如日志级别、轮转策略等",
)
async def update_logging(config: LoggingConfigUpdate):
    """更新日志配置"""
    try:
        service = get_settings_service()
        updates = {k: v for k, v in config.model_dump().items() if v is not None}

        if not updates:
            return SuccessResponse(success=True, message="无更新内容")

        success = service.update_section("logging", updates)

        if success:
            return SuccessResponse(
                success=True,
                message="日志配置已更新",
                data=service.get_section("logging")
            )
        else:
            raise HTTPException(status_code=500, detail="更新失败")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新日志配置失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/scheduler",
    response_model=SuccessResponse,
    summary="更新调度器配置",
    description="更新调度器相关配置，如并发数、重试策略等",
)
async def update_scheduler(config: SchedulerConfigUpdate):
    """更新调度器配置"""
    try:
        service = get_settings_service()
        updates = {k: v for k, v in config.model_dump().items() if v is not None}

        if not updates:
            return SuccessResponse(success=True, message="无更新内容")

        success = service.update_section("scheduler", updates)

        if success:
            return SuccessResponse(
                success=True,
                message="调度器配置已更新",
                data=service.get_section("scheduler")
            )
        else:
            raise HTTPException(status_code=500, detail="更新失败")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新调度器配置失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/{section}/reset",
    response_model=SuccessResponse,
    summary="重置配置段",
    description="将指定配置段重置为默认值",
)
async def reset_section(section: str):
    """重置配置段为默认值"""
    try:
        service = get_settings_service()
        success = service.reset_section(section)

        if success:
            return SuccessResponse(
                success=True,
                message=f"配置段 {section} 已重置为默认值",
                data=service.get_section(section)
            )
        else:
            raise HTTPException(status_code=500, detail="重置失败")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"重置配置失败 [{section}]: {e}")
        raise HTTPException(status_code=500, detail=str(e))
