#!/usr/bin/env python3
"""
验证工具模块
提供各种数据验证功能
"""

import re
import uuid
from typing import Optional, Union, Any
from urllib.parse import urlparse


def validate_url(url: str) -> bool:
    """
    验证URL格式是否有效
    
    Args:
        url: 要验证的URL字符串
        
    Returns:
        bool: URL格式是否有效
    """
    if not url or not isinstance(url, str):
        return False
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def validate_task_id(task_id: str) -> bool:
    """
    验证任务ID格式是否有效
    
    任务ID应该是8个字符的16进制字符串
    
    Args:
        task_id: 要验证的任务ID
        
    Returns:
        bool: 任务ID格式是否有效
    """
    if not task_id or not isinstance(task_id, str):
        return False
    
    # 检查长度是否为8个字符
    if len(task_id) != 8:
        return False
    
    # 检查是否只包含16进制字符
    try:
        int(task_id, 16)
        return True
    except ValueError:
        return False


def validate_css_selector(selector: str) -> bool:
    """
    验证CSS选择器格式是否基本有效
    
    Args:
        selector: CSS选择器字符串
        
    Returns:
        bool: 选择器格式是否基本有效
    """
    if not selector or not isinstance(selector, str):
        return False
    
    # 基本验证：不能为空，不能包含某些危险字符
    if len(selector.strip()) == 0:
        return False
    
    # 检查是否包含明显的非法字符
    dangerous_chars = ['<', '>', '"', "'", '`']
    if any(char in selector for char in dangerous_chars):
        return False
    
    # 基本格式验证
    # 可以使用更复杂的正则表达式，但这里只做基本检查
    basic_pattern = r'^[a-zA-Z0-9\s\#\.\[\]\(\)\:\+\~\>\-\_]+$'
    return bool(re.match(basic_pattern, selector))


def validate_interval(interval: Union[int, str]) -> bool:
    """
    验证检测间隔是否有效
    
    Args:
        interval: 检测间隔（秒或分钟）
        
    Returns:
        bool: 间隔是否有效
    """
    try:
        if isinstance(interval, str):
            interval = int(interval.strip())
        
        # 间隔应该在合理的范围内：30秒到30天
        return 30 <= interval <= 30 * 24 * 60 * 60  # 30秒到30天
    except (ValueError, TypeError):
        return False


def validate_timeout(timeout: Union[int, str]) -> bool:
    """
    验证超时时间是否有效
    
    Args:
        timeout: 超时时间（秒）
        
    Returns:
        bool: 超时时间是否有效
    """
    try:
        if isinstance(timeout, str):
            timeout = int(timeout.strip())
        
        # 超时时间应该在合理的范围内：5秒到5分钟
        return 5 <= timeout <= 300
    except (ValueError, TypeError):
        return False


def validate_email(email: str) -> bool:
    """
    验证邮箱地址格式是否有效
    
    Args:
        email: 邮箱地址
        
    Returns:
        bool: 邮箱格式是否有效
    """
    if not email or not isinstance(email, str):
        return False
    
    # 简化的邮箱验证正则表达式
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))


def validate_phone(phone: str) -> bool:
    """
    验证手机号码格式是否有效（中国大陆）
    
    Args:
        phone: 手机号码
        
    Returns:
        bool: 手机号码格式是否有效
    """
    if not phone or not isinstance(phone, str):
        return False
    
    # 中国大陆手机号码正则表达式
    phone_pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(phone_pattern, phone))


def validate_platform_name(platform: str) -> bool:
    """
    验证通知平台名称是否有效
    
    Args:
        platform: 平台名称
        
    Returns:
        bool: 平台名称是否有效
    """
    if not platform or not isinstance(platform, str):
        return False
    
    valid_platforms = ['pushplus', 'telegram', 'discord', 'feishu']
    return platform.lower() in valid_platforms


def validate_similarity_threshold(threshold: Union[float, str]) -> bool:
    """
    验证相似度阈值是否有效
    
    Args:
        threshold: 相似度阈值（0-1之间）
        
    Returns:
        bool: 阈值是否有效
    """
    try:
        if isinstance(threshold, str):
            threshold = float(threshold.strip())
        
        return 0.0 <= threshold <= 1.0
    except (ValueError, TypeError):
        return False


def validate_retry_times(retry_times: Union[int, str]) -> bool:
    """
    验证重试次数是否有效
    
    Args:
        retry_times: 重试次数
        
    Returns:
        bool: 重试次数是否有效
    """
    try:
        if isinstance(retry_times, str):
            retry_times = int(retry_times.strip())
        
        return 0 <= retry_times <= 10
    except (ValueError, TypeError):
        return False


def validate_config_name(name: str) -> bool:
    """
    验证配置名称是否有效
    
    Args:
        name: 配置名称
        
    Returns:
        bool: 配置名称是否有效
    """
    if not name or not isinstance(name, str):
        return False
    
    # 配置名称应该只包含字母、数字、下划线和连字符
    name_pattern = r'^[a-zA-Z0-9_-]+$'
    return bool(re.match(name_pattern, name))


def is_valid_uuid(uuid_string: str) -> bool:
    """
    验证字符串是否为有效的UUID
    
    Args:
        uuid_string: UUID字符串
        
    Returns:
        bool: 是否为有效的UUID
    """
    if not uuid_string or not isinstance(uuid_string, str):
        return False
    
    try:
        uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False


def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除不安全的字符
    
    Args:
        filename: 原始文件名
        
    Returns:
        str: 清理后的文件名
    """
    if not filename or not isinstance(filename, str):
        return 'unnamed'
    
    # 移除不安全的字符
    unsafe_chars = r'[<>:"/\|?*]'
    sanitized = re.sub(unsafe_chars, '_', filename)
    
    # 移除连续的下划线
    sanitized = re.sub(r'_+', '_', sanitized)
    
    # 移除开头和结尾的下划点和空格
    sanitized = sanitized.strip(' _.')
    
    # 如果文件名为空，返回默认值
    if not sanitized:
        return 'unnamed'
    
    # 限制长度
    return sanitized[:255]


# 验证器映射表，用于根据类型获取相应的验证函数
VALIDATORS = {
    'url': validate_url,
    'task_id': validate_task_id,
    'css_selector': validate_css_selector,
    'interval': validate_interval,
    'timeout': validate_timeout,
    'email': validate_email,
    'phone': validate_phone,
    'platform': validate_platform_name,
    'similarity_threshold': validate_similarity_threshold,
    'retry_times': validate_retry_times,
    'config_name': validate_config_name,
    'uuid': is_valid_uuid,
}


def validate_value(value: Any, validator_name: str) -> bool:
    """
    使用指定的验证器验证值
    
    Args:
        value: 要验证的值
        validator_name: 验证器名称
        
    Returns:
        bool: 验证结果
    """
    validator_func = VALIDATORS.get(validator_name)
    if not validator_func:
        raise ValueError(f"未知的验证器: {validator_name}")
    
    return validator_func(value)