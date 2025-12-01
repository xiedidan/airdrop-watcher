"""
内容提取算法

提供各种内容提取功能，包括文本提取、结构化数据提取、链接提取等。
"""
import re
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Union
from urllib.parse import urljoin, urlparse
from datetime import datetime

try:
    from bs4 import BeautifulSoup, Tag, NavigableString
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

from ..exceptions import DetectionError


class BaseContentExtractor(ABC):
    """内容提取算法基类"""
    
    def __init__(self, extractor_name: str = "base", **kwargs):
        """
        初始化内容提取器
        
        Args:
            extractor_name: 提取器名称
            **kwargs: 其他参数
        """
        self.extractor_name = extractor_name
        self.config = kwargs
        self.logger = logging.getLogger(__name__)
        
        # 检查BeautifulSoup是否可用
        if not BS4_AVAILABLE:
            self.logger.warning("BeautifulSoup4未安装，某些功能可能受限")
    
    @abstractmethod
    def extract(self, content: str, **kwargs) -> Dict[str, Any]:
        """
        提取内容
        
        Args:
            content: 要提取的内容
            **kwargs: 其他参数
            
        Returns:
            提取结果字典
        """
        pass
    
    def validate_html(self, html_content: str) -> bool:
        """
        验证HTML内容有效性
        
        Args:
            html_content: HTML内容
            
        Returns:
            是否有效
        """
        if not html_content or not isinstance(html_content, str):
            return False
        
        # 基本HTML格式检查
        if "<html" not in html_content.lower() and "<body" not in html_content.lower():
            # 尝试包装成完整的HTML
            return len(html_content.strip()) > 10
        
        return len(html_content.strip()) > 0
    
    def clean_text(self, text: str) -> str:
        """
        清理文本内容
        
        Args:
            text: 原始文本
            
        Returns:
            清理后的文本
        """
        if not text or not isinstance(text, str):
            return ""
        
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        
        # 移除特殊字符（保留基本标点）
        text = re.sub(r'[^\w\s\u4e00-\u9fff.,!?;:\-\'"()\[\]{}]', '', text)
        
        # 去除首尾空白
        text = text.strip()
        
        return text
    
    def get_extractor_info(self) -> Dict[str, Any]:
        """
        获取提取器信息
        
        Returns:
            提取器信息字典
        """
        return {
            "extractor_name": self.extractor_name,
            "config": self.config,
            "bs4_available": BS4_AVAILABLE
        }


class TextContentExtractor(BaseContentExtractor):
    """文本内容提取器"""
    
    def __init__(self, max_length: int = 5000, remove_scripts: bool = True, 
                 remove_styles: bool = True, **kwargs):
        """
        初始化文本内容提取器
        
        Args:
            max_length: 最大文本长度
            remove_scripts: 是否移除脚本
            remove_styles: 是否移除样式
            **kwargs: 其他参数
        """
        super().__init__("text", **kwargs)
        self.max_length = max_length
        self.remove_scripts = remove_scripts
        self.remove_styles = remove_styles
    
    def extract(self, content: str, **kwargs) -> Dict[str, Any]:
        """
        提取文本内容
        
        Args:
            content: HTML内容
            **kwargs: 其他参数
            
        Returns:
            提取结果字典
            
        Raises:
            DetectionError: 提取失败
        """
        try:
            if not self.validate_html(content):
                return {
                    "success": False,
                    "error": "无效的HTML内容",
                    "extracted_text": "",
                    "text_length": 0
                }
            
            if not BS4_AVAILABLE:
                # 备用方案：使用正则表达式
                return self._extract_with_regex(content)
            
            # 使用BeautifulSoup提取
            return self._extract_with_bs4(content)
            
        except Exception as e:
            self.logger.error(f"文本提取失败: {e}")
            raise DetectionError(f"文本提取失败: {e}", extractor=self.extractor_name)
    
    def _extract_with_bs4(self, html_content: str) -> Dict[str, Any]:
        """
        使用BeautifulSoup提取文本
        
        Args:
            html_content: HTML内容
            
        Returns:
            提取结果
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 移除不需要的元素
            elements_to_remove = []
            
            if self.remove_scripts:
                elements_to_remove.extend(['script', 'noscript'])
            
            if self.remove_styles:
                elements_to_remove.append('style')
            
            # 移除导航、页脚、侧边栏等通常不包含主要内容的部分
            elements_to_remove.extend(['nav', 'footer', 'aside', 'header', 'menu'])
            
            for element_name in elements_to_remove:
                for element in soup.find_all(element_name):
                    element.decompose()
            
            # 提取文本
            text = soup.get_text(separator=' ', strip=True)
            
            # 清理文本
            text = self.clean_text(text)
            
            # 限制长度
            if len(text) > self.max_length:
                text = text[:self.max_length] + "..."
            
            return {
                "success": True,
                "extracted_text": text,
                "text_length": len(text),
                "original_length": len(html_content),
                "compression_ratio": len(text) / len(html_content) if html_content else 0
            }
            
        except Exception as e:
            self.logger.error(f"BeautifulSoup提取失败: {e}")
            return self._extract_with_regex(html_content)
    
    def _extract_with_regex(self, html_content: str) -> Dict[str, Any]:
        """
        使用正则表达式提取文本（备用方案）
        
        Args:
            html_content: HTML内容
            
        Returns:
            提取结果
        """
        try:
            # 移除脚本和样式
            if self.remove_scripts:
                html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
                html_content = re.sub(r'<noscript[^>]*>.*?</noscript>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
            
            if self.remove_styles:
                html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
            
            # 移除HTML标签
            text = re.sub(r'<[^>]+>', '', html_content)
            
            # 解码HTML实体
            text = self._decode_html_entities(text)
            
            # 清理文本
            text = self.clean_text(text)
            
            # 限制长度
            if len(text) > self.max_length:
                text = text[:self.max_length] + "..."
            
            return {
                "success": True,
                "extracted_text": text,
                "text_length": len(text),
                "original_length": len(html_content),
                "compression_ratio": len(text) / len(html_content) if html_content else 0,
                "method": "regex"
            }
            
        except Exception as e:
            self.logger.error(f"正则表达式提取失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "extracted_text": "",
                "text_length": 0
            }
    
    def _decode_html_entities(self, text: str) -> str:
        """
        解码HTML实体
        
        Args:
            text: 包含HTML实体的文本
            
        Returns:
            解码后的文本
        """
        # 基本的HTML实体解码
        html_entities = {
            '&amp;': '&',
            '&lt;': '<',
            '&gt;': '>',
            '&quot;': '"',
            '&apos;': "'",
            '&nbsp;': ' ',
            '&#39;': "'",
            '&#34;': '"'
        }
        
        for entity, char in html_entities.items():
            text = text.replace(entity, char)
        
        # 处理数字实体
        text = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), text)
        
        return text


class StructuredDataExtractor(BaseContentExtractor):
    """结构化数据提取器"""
    
    def __init__(self, default_selectors: Optional[Dict[str, str]] = None, **kwargs):
        """
        初始化结构化数据提取器
        
        Args:
            default_selectors: 默认选择器配置
            **kwargs: 其他参数
        """
        super().__init__("structured", **kwargs)
        self.default_selectors = default_selectors or {
            "title": "title",
            "description": "meta[name='description']",
            "keywords": "meta[name='keywords']",
            "h1": "h1",
            "h2": "h2",
            "h3": "h3",
            "links": "a[href]",
            "images": "img[src]",
            "text_blocks": "p"
        }
    
    def extract(self, content: str, selectors: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """
        提取结构化数据
        
        Args:
            content: HTML内容
            selectors: 自定义选择器（可选）
            **kwargs: 其他参数
            
        Returns:
            提取结果字典
        """
        try:
            if not self.validate_html(content):
                return {
                    "success": False,
                    "error": "无效的HTML内容",
                    "extracted_data": {}
                }
            
            # 使用提供的选择器或默认选择器
            extract_selectors = selectors or self.default_selectors
            
            if not BS4_AVAILABLE:
                return {
                    "success": False,
                    "error": "BeautifulSoup4不可用，无法提取结构化数据",
                    "extracted_data": {},
                    "fields_extracted": 0,
                    "total_fields": len(extract_selectors),
                    "extraction_rate": 0.0
                }
            
            # 使用BeautifulSoup提取
            return self._extract_structured_data(content, extract_selectors)
            
        except Exception as e:
            self.logger.error(f"结构化数据提取失败: {e}")
            raise DetectionError(f"结构化数据提取失败: {e}", extractor=self.extractor_name)
    
    def _extract_structured_data(self, html_content: str, selectors: Dict[str, str]) -> Dict[str, Any]:
        """
        使用BeautifulSoup提取结构化数据
        
        Args:
            html_content: HTML内容
            selectors: 选择器配置
            
        Returns:
            提取结果
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            extracted_data = {}
            
            for field_name, selector in selectors.items():
                try:
                    elements = soup.select(selector)
                    
                    if not elements:
                        extracted_data[field_name] = None
                        continue
                    
                    # 根据元素类型和内容进行处理
                    if field_name in ["title", "description", "keywords"]:
                        # 元数据字段
                        if len(elements) == 1:
                            content = elements[0].get("content", "") or elements[0].get_text(strip=True)
                            extracted_data[field_name] = content
                        else:
                            extracted_data[field_name] = [elem.get("content", "") or elem.get_text(strip=True) 
                                                        for elem in elements]
                    
                    elif field_name in ["links"]:
                        # 链接字段
                        links = []
                        for element in elements:
                            href = element.get("href", "")
                            text = element.get_text(strip=True)
                            title = element.get("title", "")
                            
                            if href:  # 只提取有href的链接
                                links.append({
                                    "href": href,
                                    "text": text,
                                    "title": title
                                })
                        extracted_data[field_name] = links
                    
                    elif field_name in ["images"]:
                        # 图片字段
                        images = []
                        for element in elements:
                            src = element.get("src", "")
                            alt = element.get("alt", "")
                            title = element.get("title", "")
                            
                            if src:  # 只提取有src的图片
                                images.append({
                                    "src": src,
                                    "alt": alt,
                                    "title": title
                                })
                        extracted_data[field_name] = images
                    
                    else:
                        # 普通字段
                        if len(elements) == 1:
                            extracted_data[field_name] = elements[0].get_text(strip=True)
                        else:
                            extracted_data[field_name] = [elem.get_text(strip=True) for elem in elements]
                    
                    self.logger.debug(f"字段 {field_name} 提取成功: {selector}, 找到 {len(elements)} 个元素")
                    
                except Exception as e:
                    self.logger.warning(f"字段 {field_name} 提取失败: {e}")
                    extracted_data[field_name] = None
            
            # 添加统计信息
            extracted_count = sum(1 for v in extracted_data.values() if v is not None and v != [])
            
            return {
                "success": True,
                "extracted_data": extracted_data,
                "fields_extracted": extracted_count,
                "total_fields": len(selectors),
                "extraction_rate": extracted_count / len(selectors) if selectors else 0
            }
            
        except Exception as e:
            self.logger.error(f"结构化提取失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "extracted_data": {}
            }
    
    def extract_specific_fields(self, html_content: str, fields: List[str]) -> Dict[str, Any]:
        """
        提取特定字段
        
        Args:
            html_content: HTML内容
            fields: 要提取的字段列表
            
        Returns:
            特定字段提取结果
        """
        # 从默认选择器中选择需要的字段
        selectors = {field: self.default_selectors.get(field) for field in fields 
                    if field in self.default_selectors}
        
        return self.extract(html_content, selectors=selectors)


class LinkExtractor(BaseContentExtractor):
    """链接提取器"""
    
    def __init__(self, base_url: Optional[str] = None, extract_internal: bool = True, 
                 extract_external: bool = True, **kwargs):
        """
        初始化链接提取器
        
        Args:
            base_url: 基础URL，用于转换相对链接
            extract_internal: 是否提取内部链接
            extract_external: 是否提取外部链接
            **kwargs: 其他参数
        """
        super().__init__("links", **kwargs)
        self.base_url = base_url
        self.extract_internal = extract_internal
        self.extract_external = extract_external
    
    def extract(self, content: str, **kwargs) -> Dict[str, Any]:
        """
        提取链接
        
        Args:
            content: HTML内容
            **kwargs: 其他参数
            
        Returns:
            提取结果字典
        """
        try:
            if not self.validate_html(content):
                return {
                    "success": False,
                    "error": "无效的HTML内容",
                    "links": []
                }
            
            if not BS4_AVAILABLE:
                return {
                    "success": False,
                    "error": "BeautifulSoup4不可用，无法提取链接",
                    "links": []
                }
            
            return self._extract_links(content)
            
        except Exception as e:
            self.logger.error(f"链接提取失败: {e}")
            raise DetectionError(f"链接提取失败: {e}", extractor=self.extractor_name)
    
    def _extract_links(self, html_content: str) -> Dict[str, Any]:
        """
        提取链接
        
        Args:
            html_content: HTML内容
            
        Returns:
            提取结果
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            base_domain = None
            if self.base_url:
                base_domain = urlparse(self.base_url).netloc
            
            links = []
            link_elements = soup.find_all('a', href=True)
            
            for element in link_elements:
                href = element.get('href', '').strip()
                text = element.get_text(strip=True)
                title = element.get('title', '')
                
                if not href:  # 跳过空链接
                    continue
                
                # 转换相对链接
                if self.base_url and not href.startswith(('http://', 'https://', '//')):
                    href = urljoin(self.base_url, href)
                
                # 分类链接
                link_type = "unknown"
                if base_domain:
                    link_domain = urlparse(href).netloc
                    if link_domain == base_domain:
                        link_type = "internal"
                    elif link_domain:
                        link_type = "external"
                
                # 根据配置决定是否包含
                if link_type == "internal" and not self.extract_internal:
                    continue
                if link_type == "external" and not self.extract_external:
                    continue
                
                links.append({
                    "href": href,
                    "text": text,
                    "title": title,
                    "type": link_type
                })
            
            # 分类统计
            internal_links = [link for link in links if link["type"] == "internal"]
            external_links = [link for link in links if link["type"] == "external"]
            
            return {
                "success": True,
                "links": links,
                "total_links": len(links),
                "internal_links": len(internal_links),
                "external_links": len(external_links),
                "base_url": self.base_url
            }
            
        except Exception as e:
            self.logger.error(f"链接提取过程失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "links": []
            }
    
    def extract_by_type(self, html_content: str, link_type: str) -> List[Dict[str, Any]]:
        """
        按类型提取链接
        
        Args:
            html_content: HTML内容
            link_type: 链接类型（internal/external）
            
        Returns:
            指定类型的链接列表
        """
        result = self.extract(html_content)
        if result["success"]:
            return [link for link in result["links"] if link["type"] == link_type]
        return []


class ImageExtractor(BaseContentExtractor):
    """图片提取器"""
    
    def __init__(self, base_url: Optional[str] = None, **kwargs):
        """
        初始化图片提取器
        
        Args:
            base_url: 基础URL，用于转换相对URL
            **kwargs: 其他参数
        """
        super().__init__("images", **kwargs)
        self.base_url = base_url
    
    def extract(self, content: str, **kwargs) -> Dict[str, Any]:
        """
        提取图片
        
        Args:
            content: HTML内容
            **kwargs: 其他参数
            
        Returns:
            提取结果字典
        """
        try:
            if not self.validate_html(content):
                return {
                    "success": False,
                    "error": "无效的HTML内容",
                    "images": []
                }
            
            if not BS4_AVAILABLE:
                return {
                    "success": False,
                    "error": "BeautifulSoup4不可用，无法提取图片",
                    "images": []
                }
            
            return self._extract_images(content)
            
        except Exception as e:
            self.logger.error(f"图片提取失败: {e}")
            raise DetectionError(f"图片提取失败: {e}", extractor=self.extractor_name)
    
    def _extract_images(self, html_content: str) -> Dict[str, Any]:
        """
        提取图片
        
        Args:
            html_content: HTML内容
            
        Returns:
            提取结果
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            images = []
            img_elements = soup.find_all('img')
            
            for element in img_elements:
                src = element.get('src', '').strip()
                alt = element.get('alt', '')
                title = element.get('title', '')
                width = element.get('width')
                height = element.get('height')
                
                if not src:  # 跳过没有src的图片
                    continue
                
                # 转换相对URL
                if self.base_url and not src.startswith(('http://', 'https://', '//')):
                    src = urljoin(self.base_url, src)
                
                images.append({
                    "src": src,
                    "alt": alt,
                    "title": title,
                    "width": width,
                    "height": height
                })
            
            return {
                "success": True,
                "images": images,
                "total_images": len(images),
                "base_url": self.base_url
            }
            
        except Exception as e:
            self.logger.error(f"图片提取过程失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "images": []
            }


class MetaDataExtractor(BaseContentExtractor):
    """元数据提取器"""
    
    def __init__(self, **kwargs):
        """
        初始化元数据提取器
        
        Args:
            **kwargs: 其他参数
        """
        super().__init__("metadata", **kwargs)
    
    def extract(self, content: str, **kwargs) -> Dict[str, Any]:
        """
        提取元数据
        
        Args:
            content: HTML内容
            **kwargs: 其他参数
            
        Returns:
            提取结果字典
        """
        try:
            if not self.validate_html(content):
                return {
                    "success": False,
                    "error": "无效的HTML内容",
                    "metadata": {}
                }
            
            if not BS4_AVAILABLE:
                return {
                    "success": False,
                    "error": "BeautifulSoup4不可用，无法提取元数据",
                    "metadata": {}
                }
            
            return self._extract_metadata(content)
            
        except Exception as e:
            self.logger.error(f"元数据提取失败: {e}")
            raise DetectionError(f"元数据提取失败: {e}", extractor=self.extractor_name)
    
    def _extract_metadata(self, html_content: str) -> Dict[str, Any]:
        """
        提取元数据
        
        Args:
            html_content: HTML内容
            
        Returns:
            提取结果
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            metadata = {}
            
            # 基本元数据
            title = soup.find('title')
            if title:
                metadata['title'] = title.get_text(strip=True)
            
            # Meta标签
            meta_tags = soup.find_all('meta')
            for meta in meta_tags:
                name = meta.get('name', '').lower()
                property_name = meta.get('property', '').lower()
                content = meta.get('content', '')
                
                if name:
                    metadata[f'meta_{name}'] = content
                elif property_name:
                    metadata[f'meta_{property_name}'] = content
                elif meta.get('charset'):
                    metadata['charset'] = meta.get('charset')
            
            # Open Graph标签
            og_tags = soup.find_all('meta', property=re.compile(r'^og:'))
            for og_tag in og_tags:
                property_name = og_tag.get('property', '')
                content = og_tag.get('content', '')
                if property_name and content:
                    metadata[property_name] = content
            
            # Twitter Card标签
            twitter_tags = soup.find_all('meta', attrs={'name': re.compile(r'^twitter:')})
            for twitter_tag in twitter_tags:
                name = twitter_tag.get('name', '')
                content = twitter_tag.get('content', '')
                if name and content:
                    metadata[name] = content
            
            # 语言信息
            html_tag = soup.find('html')
            if html_tag and html_tag.get('lang'):
                metadata['language'] = html_tag.get('lang')
            
            # 规范化元数据键名
            normalized_metadata = self._normalize_metadata(metadata)
            
            return {
                "success": True,
                "metadata": normalized_metadata,
                "total_meta_tags": len(meta_tags),
                "og_tags": len(og_tags),
                "twitter_tags": len(twitter_tags)
            }
            
        except Exception as e:
            self.logger.error(f"元数据提取过程失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "metadata": {}
            }
    
    def _normalize_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        规范化元数据
        
        Args:
            metadata: 原始元数据
            
        Returns:
            规范化的元数据
        """
        normalized = {}
        
        # 常见元数据映射
        key_mappings = {
            'meta_description': 'description',
            'meta_keywords': 'keywords',
            'meta_author': 'author',
            'meta_viewport': 'viewport',
            'meta_robots': 'robots',
            'meta_charset': 'charset'
        }
        
        for old_key, new_key in key_mappings.items():
            if old_key in metadata:
                normalized[new_key] = metadata[old_key]
        
        # 保留其他元数据
        for key, value in metadata.items():
            if key not in key_mappings:
                normalized[key] = value
        
        return normalized


class CompositeExtractor(BaseContentExtractor):
    """组合提取器"""
    
    def __init__(self, extractors: Optional[List[BaseContentExtractor]] = None, **kwargs):
        """
        初始化组合提取器
        
        Args:
            extractors: 提取器列表
            **kwargs: 其他参数
        """
        super().__init__("composite", **kwargs)
        self.extractors = extractors or []
    
    def add_extractor(self, extractor: BaseContentExtractor):
        """
        添加提取器
        
        Args:
            extractor: 提取器实例
        """
        self.extractors.append(extractor)
    
    def extract(self, content: str, **kwargs) -> Dict[str, Any]:
        """
        使用多个提取器进行综合提取
        
        Args:
            content: HTML内容
            **kwargs: 其他参数
            
        Returns:
            综合提取结果
        """
        try:
            if not self.extractors:
                return {
                    "success": False,
                    "error": "没有可用的提取器",
                    "extracted_data": {}
                }
            
            all_results = {}
            errors = []
            
            for extractor in self.extractors:
                try:
                    result = extractor.extract(content, **kwargs)
                    
                    # 根据提取器类型组织结果
                    if isinstance(extractor, TextContentExtractor):
                        all_results["text"] = result
                    elif isinstance(extractor, StructuredDataExtractor):
                        all_results["structured"] = result
                    elif isinstance(extractor, LinkExtractor):
                        all_results["links"] = result
                    elif isinstance(extractor, ImageExtractor):
                        all_results["images"] = result
                    elif isinstance(extractor, MetaDataExtractor):
                        all_results["metadata"] = result
                    else:
                        all_results[extractor.extractor_name] = result
                        
                except Exception as e:
                    errors.append({
                        "extractor": extractor.extractor_name,
                        "error": str(e)
                    })
            
            # 统计信息
            successful_extractions = sum(1 for result in all_results.values() 
                                       if result.get("success", False))
            
            return {
                "success": len(errors) < len(self.extractors),  # 至少有一个成功就算成功
                "extracted_data": all_results,
                "successful_extractions": successful_extractions,
                "total_extractors": len(self.extractors),
                "errors": errors,
                "extraction_rate": successful_extractions / len(self.extractors) if self.extractors else 0
            }
            
        except Exception as e:
            self.logger.error(f"组合提取失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "extracted_data": {}
            }