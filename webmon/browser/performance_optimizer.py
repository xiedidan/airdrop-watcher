"""
浏览器性能优化器

提供浏览器性能优化功能，包括资源拦截、缓存机制、内存管理等。
"""
import asyncio
import logging
import time
import hashlib
import json
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path

from playwright.async_api import BrowserContext, Page, Route, Request
from ..exceptions import ResourceError
from ..utils.logger import get_logger


@dataclass
class CacheEntry:
    """缓存条目"""
    content: str
    headers: Dict[str, Any]
    status_code: int
    timestamp: datetime
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    
    def is_expired(self, max_age: int) -> bool:
        """检查是否过期"""
        age = (datetime.now() - self.timestamp).total_seconds()
        return age > max_age
    
    def get_size(self) -> int:
        """获取缓存大小"""
        return len(self.content.encode('utf-8')) + len(json.dumps(self.headers))


@dataclass
class PerformanceMetrics:
    """性能指标"""
    total_requests: int = 0
    cached_requests: int = 0
    blocked_requests: int = 0
    total_data_saved: int = 0
    average_response_time: float = 0.0
    memory_usage: int = 0
    cache_hit_rate: float = 0.0
    
    def update_request_stats(self, is_cached: bool, is_blocked: bool, 
                           response_time: float, data_size: int):
        """更新请求统计"""
        self.total_requests += 1
        
        if is_cached:
            self.cached_requests += 1
        
        if is_blocked:
            self.blocked_requests += 1
        
        if is_cached:
            self.total_data_saved += data_size
        
        # 更新平均响应时间
        if self.average_response_time == 0:
            self.average_response_time = response_time
        else:
            self.average_response_time = (
                (self.average_response_time * (self.total_requests - 1) + response_time) / 
                self.total_requests
            )
        
        # 更新缓存命中率
        if self.total_requests > 0:
            self.cache_hit_rate = self.cached_requests / self.total_requests
    
    def get_summary(self) -> Dict[str, Any]:
        """获取摘要信息"""
        return {
            "total_requests": self.total_requests,
            "cached_requests": self.cached_requests,
            "blocked_requests": self.blocked_requests,
            "cache_hit_rate": round(self.cache_hit_rate, 2),
            "total_data_saved_mb": round(self.total_data_saved / 1024 / 1024, 2),
            "average_response_time_ms": round(self.average_response_time * 1000, 2),
            "memory_usage_mb": round(self.memory_usage / 1024 / 1024, 2)
        }


class ContentCache:
    """内容缓存管理器"""
    
    def __init__(self, max_size_mb: int = 100, default_ttl: int = 300):
        """
        初始化内容缓存
        
        Args:
            max_size_mb: 最大缓存大小（MB）
            default_ttl: 默认TTL（秒）
        """
        self.cache: Dict[str, CacheEntry] = {}
        self.max_size = max_size_mb * 1024 * 1024  # 转换为字节
        self.default_ttl = default_ttl
        self.current_size = 0
        self.logger = get_logger(__name__)
        
        # 缓存统计
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[CacheEntry]:
        """
        获取缓存内容
        
        Args:
            key: 缓存键
            
        Returns:
            缓存条目，不存在或过期返回None
        """
        entry = self.cache.get(key)
        
        if not entry:
            self.misses += 1
            return None
        
        if entry.is_expired(self.default_ttl):
            self._remove_entry(key)
            self.misses += 1
            return None
        
        self.hits += 1
        return entry
    
    def set(self, key: str, content: str, headers: Dict[str, Any], 
            status_code: int, ttl: Optional[int] = None):
        """
        设置缓存内容
        
        Args:
            key: 缓存键
            content: 内容
            headers: 响应头
            status_code: 状态码
            ttl: TTL（可选）
        """
        # 检查缓存大小
        entry_size = len(content.encode('utf-8')) + len(json.dumps(headers))
        
        if entry_size > self.max_size:
            self.logger.warning(f"内容太大，无法缓存: {entry_size} > {self.max_size}")
            return
        
        # 清理空间
        while self.current_size + entry_size > self.max_size and self.cache:
            self._remove_oldest_entry()
        
        # 创建缓存条目
        etag = headers.get("etag")
        last_modified = headers.get("last-modified")
        
        entry = CacheEntry(
            content=content,
            headers=headers,
            status_code=status_code,
            timestamp=datetime.now(),
            etag=etag,
            last_modified=last_modified
        )
        
        self.cache[key] = entry
        self.current_size += entry_size
        
        self.logger.debug(f"内容已缓存: {key}, 大小: {entry_size}字节")
    
    def _remove_entry(self, key: str):
        """移除缓存条目"""
        entry = self.cache.pop(key, None)
        if entry:
            self.current_size -= entry.get_size()
    
    def _remove_oldest_entry(self):
        """移除最旧的缓存条目"""
        if not self.cache:
            return
        
        oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k].timestamp)
        self._remove_entry(oldest_key)
    
    def clear(self):
        """清空缓存"""
        self.cache.clear()
        self.current_size = 0
        self.hits = 0
        self.misses = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        total_requests = self.hits + self.misses
        hit_rate = self.hits / max(total_requests, 1)
        
        return {
            "cache_size": len(self.cache),
            "current_size_mb": round(self.current_size / 1024 / 1024, 2),
            "max_size_mb": round(self.max_size / 1024 / 1024, 2),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(hit_rate, 2),
            "default_ttl": self.default_ttl
        }


class ResourceBlocker:
    """资源拦截器"""
    
    def __init__(self):
        """初始化资源拦截器"""
        # 默认拦截的资源类型
        self.blocked_types = {
            "image": True,
            "stylesheet": False,  # CSS通常需要加载
            "font": True,
            "media": True,
            "websocket": True,
            "eventsource": True,
            "manifest": True
        }
        
        # 默认拦截的文件扩展名
        self.blocked_extensions = {
            ".jpg", ".jpeg", ".png", ".gif", ".svg", ".ico", ".webp",
            ".mp4", ".avi", ".mov", ".wmv", ".flv", ".webm",
            ".mp3", ".wav", ".flac", ".aac", ".ogg",
            ".woff", ".woff2", ".ttf", ".otf", ".eot"
        }
        
        # 默认拦截的域名模式
        self.blocked_domains = {
            "doubleclick.net", "googleadservices.com", "googlesyndication.com",
            "facebook.com/tr", "google-analytics.com", "googletagmanager.com",
            "adzerk.net", "adsystem.com", "advertising.com"
        }
        
        self.logger = get_logger(__name__)
        self.blocked_count = 0
        self.total_requests = 0
    
    def should_block_request(self, request: Request) -> bool:
        """
        判断是否应该拦截请求
        
        Args:
            request: 请求对象
            
        Returns:
            是否应该拦截
        """
        self.total_requests += 1
        
        url = request.url
        resource_type = request.resource_type
        
        # 检查资源类型
        if self.blocked_types.get(resource_type, False):
            self.blocked_count += 1
            self.logger.debug(f"拦截资源类型: {resource_type}, URL: {url}")
            return True
        
        # 检查文件扩展名
        url_lower = url.lower()
        for extension in self.blocked_extensions:
            if url_lower.endswith(extension):
                self.blocked_count += 1
                self.logger.debug(f"拦截文件扩展名: {extension}, URL: {url}")
                return True
        
        # 检查域名
        domain = self._extract_domain(url)
        for blocked_domain in self.blocked_domains:
            if blocked_domain in domain:
                self.blocked_count += 1
                self.logger.debug(f"拦截域名: {domain}, URL: {url}")
                return True
        
        return False
    
    def _extract_domain(self, url: str) -> str:
        """提取域名"""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc.lower()
        except:
            return ""
    
    def get_stats(self) -> Dict[str, Any]:
        """获取拦截统计"""
        block_rate = self.blocked_count / max(self.total_requests, 1)
        
        return {
            "total_requests": self.total_requests,
            "blocked_requests": self.blocked_count,
            "block_rate": round(block_rate, 2),
            "blocked_types": {k: v for k, v in self.blocked_types.items() if v},
            "blocked_extensions_count": len(self.blocked_extensions),
            "blocked_domains_count": len(self.blocked_domains)
        }


class PerformanceOptimizer:
    """性能优化器"""
    
    def __init__(self, config_manager, cache_enabled: bool = True, 
                 blocking_enabled: bool = True, max_cache_size_mb: int = 50):
        """
        初始化性能优化器
        
        Args:
            config_manager: 配置管理器
            cache_enabled: 是否启用缓存
            blocking_enabled: 是否启用拦截
            max_cache_size_mb: 最大缓存大小
        """
        self.config_manager = config_manager
        self.cache_enabled = cache_enabled
        self.blocking_enabled = blocking_enabled
        
        # 初始化组件
        self.cache = ContentCache(max_cache_size_mb) if cache_enabled else None
        self.blocker = ResourceBlocker() if blocking_enabled else None
        
        # 性能指标
        self.metrics = PerformanceMetrics()
        
        self.logger = get_logger(__name__)
        
        # 加载配置
        self._load_config()
    
    def _load_config(self):
        """加载配置"""
        try:
            # 检查配置是否启用
            self.cache_enabled = self.config_manager.get("ENABLE_CACHE", self.cache_enabled)
            self.blocking_enabled = self.config_manager.get("ENABLE_BLOCKING", self.blocking_enabled)
            
            if self.cache_enabled and not self.cache:
                cache_size = self.config_manager.get("CACHE_SIZE_MB", 50)
                self.cache = ContentCache(cache_size)
            
            if self.blocking_enabled and not self.blocker:
                self.blocker = ResourceBlocker()
            
            self.logger.info(f"性能优化器配置 - 缓存: {self.cache_enabled}, 拦截: {self.blocking_enabled}")
            
        except Exception as e:
            self.logger.error(f"加载性能优化配置失败: {e}")
    
    async def optimize_browser_context(self, context: BrowserContext):
        """
        优化浏览器上下文
        
        Args:
            context: 浏览器上下文
        """
        try:
            # 设置资源拦截
            if self.blocking_enabled and self.blocker:
                await context.route("**/*", self._route_handler)
                self.logger.debug("资源拦截路由已设置")
            
            # 其他优化设置
            await context.set_default_navigation_timeout(30000)
            await context.set_default_timeout(30000)
            
            self.logger.info("浏览器上下文优化完成")
            
        except Exception as e:
            self.logger.error(f"优化浏览器上下文失败: {e}")
    
    async def _route_handler(self, route: Route):
        """路由处理函数"""
        try:
            request = route.request
            url = request.url
            
            # 检查是否应该拦截
            if self.blocker and self.blocker.should_block_request(request):
                await route.abort("aborted")
                return
            
            # 检查缓存
            if self.cache:
                cache_key = self._generate_cache_key(url)
                cached_entry = self.cache.get(cache_key)
                
                if cached_entry:
                    # 使用缓存响应
                    await route.fulfill(
                        status=cached_entry.status_code,
                        content_type=request.headers.get("content-type"),
                        headers=cached_entry.headers,
                        body=cached_entry.content
                    )
                    
                    # 更新统计
                    self.metrics.update_request_stats(
                        is_cached=True,
                        is_blocked=False,
                        response_time=0.1,  # 缓存响应时间
                        data_size=len(cached_entry.content.encode('utf-8'))
                    )
                    
                    self.logger.debug(f"缓存命中: {url}")
                    return
            
            # 继续原始请求
            start_time = time.time()
            response = await route.fetch()
            response_time = time.time() - start_time
            
            # 缓存响应（如果适用）
            if (self.cache and 
                response.status_code == 200 and 
                self._should_cache_response(response)):
                
                content = await response.text()
                cache_key = self._generate_cache_key(url)
                
                self.cache.set(
                    key=cache_key,
                    content=content,
                    headers=dict(response.headers),
                    status_code=response.status_code
                )
                
                self.logger.debug(f"内容已缓存: {url}")
            
            # 更新统计
            content_length = len((await response.body()).decode('utf-8', errors='ignore'))
            self.metrics.update_request_stats(
                is_cached=False,
                is_blocked=False,
                response_time=response_time,
                data_size=content_length
            )
            
            # 返回响应
            await route.fulfill(
                status=response.status_code,
                headers=dict(response.headers),
                body=await response.body()
            )
            
        except Exception as e:
            self.logger.error(f"路由处理失败: {e}")
            try:
                await route.abort("failed")
            except:
                pass
    
    def _generate_cache_key(self, url: str) -> str:
        """生成缓存键"""
        return hashlib.md5(url.encode('utf-8')).hexdigest()
    
    def _should_cache_response(self, response) -> bool:
        """判断是否应该缓存响应"""
        # 检查内容类型
        content_type = response.headers.get("content-type", "").lower()
        
        # 只缓存特定类型的内容
        cacheable_types = [
            "text/html",
            "text/css",
            "text/javascript",
            "application/javascript",
            "application/json",
            "text/plain"
        ]
        
        for cacheable_type in cacheable_types:
            if cacheable_type in content_type:
                return True
        
        return False
    
    def optimize_page_loading(self, page: Page):
        """
        优化页面加载
        
        Args:
            page: 页面实例
        """
        try:
            # 设置合理的超时
            page.set_default_navigation_timeout(30000)
            page.set_default_timeout(30000)
            
            # 添加页面加载优化脚本
            page.add_init_script("""
                // 禁用图片加载（如果配置启用）
                if (window.location.hostname !== 'localhost') {
                    Object.defineProperty(HTMLImageElement.prototype, 'src', {
                        set: function(value) {
                            if (value && value.includes('.jpg') || value.includes('.png') || value.includes('.gif')) {
                                return; // 不加载图片
                            }
                            this.setAttribute('src', value);
                        }
                    });
                }
                
                // 优化CSS加载
                const originalLink = HTMLLinkElement.prototype;
                const originalSetAttribute = originalLink.setAttribute;
                originalLink.setAttribute = function(name, value) {
                    if (name === 'rel' && value === 'stylesheet') {
                        // 延迟非关键CSS加载
                        setTimeout(() => {
                            originalSetAttribute.call(this, name, value);
                        }, 100);
                        return;
                    }
                    originalSetAttribute.call(this, name, value);
                };
            """)
            
            self.logger.debug("页面加载优化脚本已应用")
            
        except Exception as e:
            self.logger.error(f"优化页面加载失败: {e}")
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """获取性能统计"""
        stats = self.metrics.get_summary()
        
        if self.cache:
            cache_stats = self.cache.get_stats()
            stats["cache_stats"] = cache_stats
        
        if self.blocker:
            blocker_stats = self.blocker.get_stats()
            stats["blocker_stats"] = blocker_stats
        
        return stats
    
    def clear_cache(self):
        """清空缓存"""
        if self.cache:
            self.cache.clear()
            self.logger.info("缓存已清空")
    
    def update_config(self, cache_enabled: Optional[bool] = None, 
                     blocking_enabled: Optional[bool] = None,
                     cache_size_mb: Optional[int] = None):
        """
        更新配置
        
        Args:
            cache_enabled: 是否启用缓存
            blocking_enabled: 是否启用拦截
            cache_size_mb: 缓存大小（MB）
        """
        if cache_enabled is not None:
            self.cache_enabled = cache_enabled
            if cache_enabled and not self.cache:
                size = cache_size_mb or 50
                self.cache = ContentCache(size)
            elif not cache_enabled and self.cache:
                self.cache = None
        
        if blocking_enabled is not None:
            self.blocking_enabled = blocking_enabled
            if blocking_enabled and not self.blocker:
                self.blocker = ResourceBlocker()
            elif not blocking_enabled and self.blocker:
                self.blocker = None
        
        if cache_size_mb is not None and self.cache:
            self.cache.max_size = cache_size_mb * 1024 * 1024
        
        self.logger.info(f"性能优化器配置已更新 - 缓存: {self.cache_enabled}, 拦截: {self.blocking_enabled}")


class MemoryManager:
    """内存管理器"""
    
    def __init__(self, max_memory_mb: int = 500):
        """
        初始化内存管理器
        
        Args:
            max_memory_mb: 最大内存使用（MB）
        """
        self.max_memory_mb = max_memory_mb
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.logger = get_logger(__name__)
    
    def get_memory_usage(self) -> int:
        """获取当前内存使用"""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss
        except ImportError:
            self.logger.warning("psutil未安装，无法准确获取内存使用")
            return 0
        except Exception as e:
            self.logger.error(f"获取内存使用失败: {e}")
            return 0
    
    def is_memory_limit_exceeded(self) -> bool:
        """检查是否超过内存限制"""
        current_usage = self.get_memory_usage()
        return current_usage > self.max_memory_bytes
    
    async def perform_gc(self):
        """执行垃圾回收"""
        try:
            import gc
            gc.collect()
            self.logger.debug("垃圾回收已执行")
        except Exception as e:
            self.logger.error(f"垃圾回收失败: {e}")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """获取内存统计"""
        current_usage = self.get_memory_usage()
        usage_percent = (current_usage / self.max_memory_bytes) * 100 if self.max_memory_bytes > 0 else 0
        
        return {
            "current_usage_mb": round(current_usage / 1024 / 1024, 2),
            "max_memory_mb": self.max_memory_mb,
            "usage_percent": round(usage_percent, 2),
            "is_limit_exceeded": self.is_memory_limit_exceeded()
        }