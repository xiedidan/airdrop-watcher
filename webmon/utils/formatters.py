"""
格式化工具模块
提供常用的数据格式化函数
"""

from datetime import timedelta
from typing import Union


def format_file_size(size_bytes: Union[int, float]) -> str:
    """
    格式化文件大小
    
    Args:
        size_bytes: 文件大小（字节）
        
    Returns:
        格式化后的文件大小字符串
        
    Examples:
        >>> format_file_size(1024)
        '1.00 KB'
        >>> format_file_size(1048576)
        '1.00 MB'
    """
    if size_bytes == 0:
        return "0 B"
    
    # 定义单位
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    
    # 计算合适的单位
    size = float(size_bytes)
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    # 格式化输出，保留2位小数
    if unit_index == 0:  # 字节不需要小数
        return f"{int(size)} {units[unit_index]}"
    else:
        return f"{size:.2f} {units[unit_index]}"


def format_duration(seconds: Union[int, float]) -> str:
    """
    格式化持续时间
    
    Args:
        seconds: 持续时间（秒）
        
    Returns:
        格式化后的持续时间字符串
        
    Examples:
        >>> format_duration(1.5)
        '1.5s'
        >>> format_duration(60)
        '1m 0s'
        >>> format_duration(3661)
        '1h 1m 1s'
    """
    if seconds <= 0:
        return "0s"
    
    # 小于1秒，用毫秒表示
    if seconds < 1:
        ms = int(seconds * 1000)
        return f"{ms}ms"
    
    # 转换为整数秒（向下取整）
    total_seconds = int(seconds)
    
    # 计算小时、分钟、秒
    hours = total_seconds // 3600
    remaining = total_seconds % 3600
    minutes = remaining // 60
    secs = remaining % 60
    
    # 构建结果字符串
    parts = []
    
    if hours > 0:
        parts.append(f"{hours}h")
        parts.append(f"{minutes}m")
        parts.append(f"{secs}s")
    elif minutes > 0:
        parts.append(f"{minutes}m")
        parts.append(f"{secs}s")
    else:
        parts.append(f"{secs}s")
    
    return " ".join(parts)


def format_duration_precise(seconds: Union[int, float]) -> str:
    """
    格式化持续时间（精确版本，包含小数秒）
    
    Args:
        seconds: 持续时间（秒）
        
    Returns:
        格式化后的持续时间字符串（包含小数）
        
    Examples:
        >>> format_duration_precise(1.234)
        '1.23s'
        >>> format_duration_precise(61.234)
        '1m 1.23s'
    """
    if seconds <= 0:
        return "0s"
    
    # 小于1秒，用毫秒表示
    if seconds < 1:
        ms = int(seconds * 1000)
        return f"{ms}ms"
    
    # 分离整数和小数部分
    total_seconds = float(seconds)
    integer_part = int(total_seconds)
    decimal_part = total_seconds - integer_part
    
    # 计算小时、分钟、秒
    hours = integer_part // 3600
    remaining = integer_part % 3600
    minutes = remaining // 60
    secs = remaining % 60
    
    # 构建结果字符串
    parts = []
    
    if hours > 0:
        parts.append(f"{hours}h")
        parts.append(f"{minutes}m")
        # 秒数部分，如果有小数则包含小数
        if decimal_part > 0:
            secs_with_decimal = round(total_seconds - hours * 3600 - minutes * 60, 2)
            parts.append(f"{secs_with_decimal}s")
        else:
            parts.append(f"{secs}s")
    elif minutes > 0:
        parts.append(f"{minutes}m")
        # 秒数部分，如果有小数则包含小数
        if decimal_part > 0:
            secs_with_decimal = round(total_seconds - minutes * 60, 2)
            parts.append(f"{secs_with_decimal}s")
        else:
            parts.append(f"{secs}s")
    else:
        if decimal_part > 0:
            parts.append(f"{round(total_seconds, 2)}s")
        else:
            parts.append(f"{secs}s")
    
    return " ".join(parts)


def format_bytes_per_second(bytes_per_sec: Union[int, float]) -> str:
    """
    格式化传输速率
    
    Args:
        bytes_per_sec: 传输速率（字节/秒）
        
    Returns:
        格式化后的传输速率字符串
        
    Examples:
        >>> format_bytes_per_second(1024)
        '1.00 KB/s'
        >>> format_bytes_per_second(1048576)
        '1.00 MB/s'
    """
    if bytes_per_sec == 0:
        return "0 B/s"
    
    # 使用文件大小格式化函数，然后添加"/s"
    size_str = format_file_size(bytes_per_sec)
    return f"{size_str}/s"


def format_percentage(value: Union[int, float], total: Union[int, float]) -> str:
    """
    格式化百分比
    
    Args:
        value: 当前值
        total: 总值
        
    Returns:
        格式化后的百分比字符串
        
    Examples:
        >>> format_percentage(50, 100)
        '50.0%'
        >>> format_percentage(1, 3)
        '33.3%'
    """
    if total == 0:
        return "0.0%"
    
    percentage = (value / total) * 100
    return f"{percentage:.1f}%"


def format_count(count: int, singular: str = "", plural: str = "s") -> str:
    """
    格式化计数（处理单复数）
    
    Args:
        count: 数量
        singular: 单数形式的后缀（默认空字符串）
        plural: 复数形式的后缀（默认"s"）
        
    Returns:
        格式化后的计数字符串
        
    Examples:
        >>> format_count(1, "item")
        '1 item'
        >>> format_count(2, "item")
        '2 items'
        >>> format_count(0, "file", "files")
        '0 files'
    """
    if count == 1:
        suffix = singular
    else:
        suffix = plural
    
    return f"{count} {suffix}"