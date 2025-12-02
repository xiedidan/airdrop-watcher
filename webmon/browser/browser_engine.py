"""
浏览器引擎 - Playwright集成

提供网页内容获取功能，支持JavaScript渲染、动态等待、反检测等特性。
"""
import asyncio
import logging
import time
from typing import Optional, Dict, Any, List, Union
from urllib.parse import urlparse
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import Error as PlaywrightError

from ..exceptions import BrowserError, NetworkError, ConfigurationError
from ..utils.logger import get_logger
from .network_config import NetworkConfig


class BrowserEngine:
    """Playwright浏览器引擎"""
    
    def __init__(self, config_manager):
        """
        初始化浏览器引擎

        Args:
            config_manager: 配置管理器
        """
        self.config_manager = config_manager
        self.logger = get_logger(__name__)

        # Playwright实例
        self.playwright = None
        self.browser = None
        self.context = None

        # 配置参数
        self.browser_type = "chromium"  # 默认使用Chromium
        self.headless = True
        self.timeout = 30000  # 默认超时时间30秒
        self.user_agent = None
        self.viewport = {"width": 1920, "height": 1080}

        # 性能优化配置
        self.block_resources = True  # 是否拦截不必要的资源
        self.blocked_resource_types = ["image", "stylesheet", "font", "media"]

        # 反检测配置
        self.enable_stealth = True  # 是否启用反检测

        # 状态管理
        self.is_initialized = False
        self.page_count = 0
        self.start_time = None

        # 网络配置管理器
        self.network_config = NetworkConfig(config_manager)

        # 加载配置
        self._load_browser_config()
    
    def _load_browser_config(self):
        """加载浏览器配置"""
        try:
            # 获取监控配置
            monitoring_config = self.config_manager.get_monitoring_config()
            
            # 基础配置
            self.headless = monitoring_config.get("browser_headless", True)
            self.timeout = monitoring_config.get("default_timeout", 30000)
            
            # 获取环境变量配置
            custom_user_agent = self.config_manager.get("CUSTOM_USER_AGENT")
            if custom_user_agent:
                self.user_agent = custom_user_agent
            
            # 获取高级配置
            self.block_resources = self.config_manager.get("BLOCK_RESOURCES", True)
            self.enable_stealth = self.config_manager.get("ENABLE_STEALTH", True)
            
            self.logger.info(f"浏览器配置加载完成 - 无头模式: {self.headless}, 超时: {self.timeout}ms")
            
        except Exception as e:
            self.logger.error(f"加载浏览器配置失败: {e}")
            raise ConfigurationError(f"加载浏览器配置失败: {e}")
    
    async def initialize(self) -> bool:
        """
        初始化浏览器引擎
        
        Returns:
            是否成功初始化
            
        Raises:
            BrowserError: 浏览器初始化失败
        """
        try:
            self.logger.info("开始初始化浏览器引擎...")
            start_time = time.time()
            
            # 初始化Playwright
            self.playwright = await async_playwright().start()
            self.logger.info("Playwright已启动")
            
            # 启动浏览器
            await self._launch_browser()
            
            # 创建浏览器上下文
            await self._create_context()
            
            self.is_initialized = True
            self.start_time = time.time()
            
            init_time = time.time() - start_time
            self.logger.info(f"浏览器引擎初始化完成，耗时: {init_time:.2f}秒")
            
            return True
            
        except Exception as e:
            self.logger.error(f"浏览器引擎初始化失败: {e}")
            await self.cleanup()
            raise BrowserError(f"浏览器引擎初始化失败: {e}")
    
    async def _launch_browser(self):
        """启动浏览器实例"""
        try:
            launch_options = {
                "headless": self.headless,
                "args": [
                    "--disable-blink-features=AutomationControlled",
                    "--disable-features=IsolateOrigins,site-per-process",
                    "--disable-site-isolation-trials",
                    "--disable-web-security",
                    "--disable-features=BlockInsecurePrivateNetworkRequests",
                    "--disable-features=OutOfBlinkCors",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-accelerated-2d-canvas",
                    "--no-first-run",
                    "--no-zygote",
                    "--single-process",  # 单进程模式，适用于容器环境
                    "--disable-gpu"
                ]
            }
            
            # 启动浏览器
            if self.browser_type == "chromium":
                self.browser = await self.playwright.chromium.launch(**launch_options)
            elif self.browser_type == "firefox":
                self.browser = await self.playwright.firefox.launch(**launch_options)
            elif self.browser_type == "webkit":
                self.browser = await self.playwright.webkit.launch(**launch_options)
            else:
                raise BrowserError(f"不支持的浏览器类型: {self.browser_type}")
            
            self.logger.info(f"浏览器已启动: {self.browser_type}")
            
        except Exception as e:
            raise BrowserError(f"浏览器启动失败: {e}")
    
    async def _create_context(self, url: Optional[str] = None):
        """
        创建浏览器上下文

        Args:
            url: 目标URL（用于代理判断）
        """
        try:
            context_options = {
                "viewport": self.viewport,
                "locale": "zh-CN",
                "timezone_id": "Asia/Shanghai",
                "permissions": ["geolocation"],
                "extra_http_headers": {
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                    "DNT": "1",
                    "Upgrade-Insecure-Requests": "1"
                }
            }

            # 使用NetworkConfig获取网络相关配置
            network_options = self.network_config.get_browser_context_options(url)
            context_options.update(network_options)

            # User-Agent优先使用NetworkConfig中的配置
            user_agent = self.network_config.get_user_agent()
            if user_agent:
                context_options['user_agent'] = user_agent

            # 启用反检测功能
            if self.enable_stealth:
                context_options.update({
                    "bypass_csp": True,
                })
                # 如果NetworkConfig没有配置ignore_https_errors，则默认启用
                if 'ignore_https_errors' not in context_options:
                    context_options['ignore_https_errors'] = True

            self.context = await self.browser.new_context(**context_options)

            # 设置默认超时
            self.context.set_default_timeout(self.timeout)
            self.context.set_default_navigation_timeout(self.timeout)

            # 设置资源拦截
            if self.block_resources:
                await self._setup_resource_blocking()

            self.logger.info("浏览器上下文已创建")

        except Exception as e:
            raise BrowserError(f"创建浏览器上下文失败: {e}")
    
    async def _setup_resource_blocking(self):
        """设置资源拦截"""
        try:
            async def route_handler(route):
                """路由处理函数"""
                resource_type = route.request.resource_type
                
                # 拦截不必要的资源
                if resource_type in self.blocked_resource_types:
                    await route.abort("aborted")
                    return
                
                # 继续请求
                await route.continue_()
            
            # 设置路由拦截
            await self.context.route("**/*", route_handler)
            self.logger.info("资源拦截已设置")
            
        except Exception as e:
            self.logger.warning(f"设置资源拦截失败: {e}")
    
    async def get_page_content(self, url: str, selectors: Optional[List[str]] = None, 
                              wait_for_selector: Optional[str] = None,
                              wait_time: Optional[int] = None) -> Dict[str, Any]:
        """
        获取页面内容
        
        Args:
            url: 目标URL
            selectors: CSS选择器列表，用于提取特定内容
            wait_for_selector: 等待的选择器
            wait_time: 额外等待时间（秒）
            
        Returns:
            页面内容信息字典
            
        Raises:
            BrowserError: 浏览器操作失败
            NetworkError: 网络错误
        """
        if not self.is_initialized:
            raise BrowserError("浏览器引擎未初始化")
        
        start_time = time.time()
        page = None
        
        try:
            # 验证URL
            if not self._validate_url(url):
                raise NetworkError(f"无效的URL: {url}")
            
            self.logger.info(f"开始获取页面内容: {url}")
            
            # 创建新页面
            page = await self.context.new_page()
            self.page_count += 1
            
            # 应用反检测脚本
            if self.enable_stealth:
                await self._apply_stealth_scripts(page)
            
            # 导航到页面
            response = await page.goto(url, wait_until="networkidle", timeout=self.timeout)
            
            if not response:
                raise NetworkError(f"页面加载失败: {url}")
            
            # 检查HTTP状态码
            if response.status >= 400:
                raise NetworkError(
                    f"HTTP错误: {response.status}", 
                    url=url, 
                    status_code=response.status
                )
            
            # 等待特定选择器
            if wait_for_selector:
                try:
                    await page.wait_for_selector(wait_for_selector, timeout=10000)
                except PlaywrightTimeoutError:
                    self.logger.warning(f"等待选择器超时: {wait_for_selector}")
            
            # 额外等待时间
            if wait_time and wait_time > 0:
                await asyncio.sleep(wait_time)
            
            # 获取页面内容
            content = await page.content()
            
            # 提取特定内容（如果使用选择器）
            extracted_content = {}
            if selectors:
                extracted_content = await self._extract_by_selectors(page, selectors)
            
            # 获取页面信息
            title = await page.title()
            viewport_size = page.viewport_size
            
            # 计算加载时间
            load_time = time.time() - start_time
            
            result = {
                "url": url,
                "content": content,
                "title": title,
                "status_code": response.status,
                "headers": dict(response.headers),
                "load_time": load_time,
                "viewport": viewport_size,
                "extracted_content": extracted_content,
                "content_size": len(content.encode('utf-8')),
                "success": True
            }
            
            self.logger.info(f"页面内容获取成功: {url}, 大小: {result['content_size']}字节, 耗时: {load_time:.2f}秒")
            
            return result
            
        except PlaywrightTimeoutError as e:
            raise NetworkError(f"页面加载超时: {url}", url=url)
            
        except PlaywrightError as e:
            raise BrowserError(f"浏览器错误: {str(e)}", url=url, browser_error=str(e))
            
        except Exception as e:
            if isinstance(e, (BrowserError, NetworkError)):
                raise
            else:
                raise BrowserError(f"获取页面内容失败: {e}", url=url)
        
        finally:
            # 清理页面
            if page:
                try:
                    await page.close()
                    self.page_count -= 1
                except Exception as e:
                    self.logger.warning(f"关闭页面失败: {e}")
    
    async def _extract_by_selectors(self, page: Page, selectors: List[str]) -> Dict[str, Any]:
        """
        通过CSS选择器提取内容
        
        Args:
            page: 页面实例
            selectors: CSS选择器列表
            
        Returns:
            提取的内容字典
        """
        extracted_content = {}
        
        try:
            for selector in selectors:
                try:
                    # 获取元素文本内容
                    elements = await page.query_selector_all(selector)
                    
                    if not elements:
                        extracted_content[selector] = None
                        continue
                    
                    # 提取文本内容
                    texts = []
                    for element in elements:
                        text = await element.text_content()
                        if text:
                            texts.append(text.strip())
                    
                    # 如果只有一个元素，返回字符串；否则返回列表
                    if len(texts) == 1:
                        extracted_content[selector] = texts[0]
                    else:
                        extracted_content[selector] = texts
                    
                    self.logger.debug(f"选择器提取成功: {selector}, 找到 {len(elements)} 个元素")
                    
                except Exception as e:
                    self.logger.warning(f"选择器提取失败: {selector}, 错误: {e}")
                    extracted_content[selector] = None
            
            return extracted_content
            
        except Exception as e:
            self.logger.error(f"选择器提取过程失败: {e}")
            return {}
    
    async def _apply_stealth_scripts(self, page: Page):
        """应用反检测脚本"""
        try:
            # 隐藏WebDriver属性
            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)
            
            # 修改插件信息
            await page.add_init_script("""
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
            """)
            
            # 修改语言信息
            await page.add_init_script("""
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['zh-CN', 'zh', 'en-US', 'en']
                });
            """)
            
            # 修改权限信息
            await page.add_init_script("""
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
            """)
            
            self.logger.debug("反检测脚本已应用")
            
        except Exception as e:
            self.logger.warning(f"应用反检测脚本失败: {e}")
    
    def _validate_url(self, url: str) -> bool:
        """
        验证URL有效性
        
        Args:
            url: 要验证的URL
            
        Returns:
            是否有效
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc]) and result.scheme in ["http", "https"]
        except Exception:
            return False
    
    async def get_browser_info(self) -> Dict[str, Any]:
        """
        获取浏览器信息
        
        Returns:
            浏览器信息字典
        """
        if not self.is_initialized:
            return {"initialized": False}
        
        return {
            "initialized": self.is_initialized,
            "browser_type": self.browser_type,
            "headless": self.headless,
            "timeout": self.timeout,
            "page_count": self.page_count,
            "start_time": self.start_time,
            "runtime": time.time() - self.start_time if self.start_time else 0
        }
    
    async def cleanup(self):
        """清理浏览器资源"""
        try:
            self.logger.info("开始清理浏览器资源...")
            
            # 关闭所有页面
            if self.context:
                try:
                    pages = self.context.pages
                    for page in pages:
                        await page.close()
                    self.page_count = 0
                except Exception as e:
                    self.logger.warning(f"关闭页面失败: {e}")
            
            # 关闭浏览器上下文
            if self.context:
                try:
                    await self.context.close()
                    self.context = None
                except Exception as e:
                    self.logger.warning(f"关闭浏览器上下文失败: {e}")
            
            # 关闭浏览器
            if self.browser:
                try:
                    await self.browser.close()
                    self.browser = None
                except Exception as e:
                    self.logger.warning(f"关闭浏览器失败: {e}")
            
            # 停止Playwright
            if self.playwright:
                try:
                    await self.playwright.stop()
                    self.playwright = None
                except Exception as e:
                    self.logger.warning(f"停止Playwright失败: {e}")
            
            self.is_initialized = False
            self.logger.info("浏览器资源清理完成")
            
        except Exception as e:
            self.logger.error(f"清理浏览器资源失败: {e}")
    
    def __del__(self):
        """析构函数"""
        if self.is_initialized:
            try:
                # 尝试异步清理（如果事件循环可用）
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(self.cleanup())
                else:
                    loop.run_until_complete(self.cleanup())
            except Exception:
                # 如果无法异步清理，记录日志
                self.logger.warning("无法在析构函数中清理浏览器资源")


class BrowserPool:
    """浏览器池管理器"""
    
    def __init__(self, config_manager, max_browsers: int = 3):
        """
        初始化浏览器池
        
        Args:
            config_manager: 配置管理器
            max_browsers: 最大浏览器实例数
        """
        self.config_manager = config_manager
        self.max_browsers = max_browsers
        self.browsers = []
        self.semaphore = asyncio.Semaphore(max_browsers)
        self.logger = get_logger(__name__)
    
    async def get_browser(self) -> BrowserEngine:
        """
        获取浏览器实例
        
        Returns:
            浏览器引擎实例
        """
        async with self.semaphore:
            # 查找可用的浏览器
            for browser in self.browsers:
                if not browser.in_use:
                    browser.in_use = True
                    return browser
            
            # 创建新浏览器
            if len(self.browsers) < self.max_browsers:
                browser = BrowserEngine(self.config_manager)
                await browser.initialize()
                browser.in_use = True
                self.browsers.append(browser)
                return browser
            
            # 等待可用浏览器
            while True:
                for browser in self.browsers:
                    if not browser.in_use:
                        browser.in_use = True
                        return browser
                await asyncio.sleep(0.1)
    
    async def release_browser(self, browser: BrowserEngine):
        """
        释放浏览器实例
        
        Args:
            browser: 浏览器引擎实例
        """
        browser.in_use = False
    
    async def cleanup(self):
        """清理所有浏览器实例"""
        for browser in self.browsers:
            await browser.cleanup()
        self.browsers.clear()