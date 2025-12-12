# WebMon - 网页监控工具设计文档

## 1. 总体架构设计

### 1.1 架构概览
```
┌─────────────────────────────────────────────────────────────┐
│                         CLI Layer                           │
├─────────────────────────────────────────────────────────────┤
│  Commands: init, add, remove, list, start, stop, status    │
├─────────────────────────────────────────────────────────────┤
│                    Core Logic Layer                         │
│  ┌─────────────┐ ┌──────────────┐ ┌────────────────────┐   │
│  │ Task Manager│ │ChangeDetector│ │NotificationService │   │
│  └─────────────┘ └──────────────┘ └────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              AIAnalysisService (新增)                │   │
│  │  - 调用AI模型分析变化内容                             │   │
│  │  - 提示词模板渲染                                    │   │
│  │  - 生成自然语言摘要                                  │   │
│  └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                    Browser Engine                           │
│                    (Playwright)                            │
├─────────────────────────────────────────────────────────────┤
│                  Data Storage Layer                         │
│  ┌─────────────┐ ┌──────────────┐ ┌────────────────────┐   │
│  │config.json  │ │history.json  │ │   webmon.log       │   │
│  └─────────────┘ └──────────────┘ └────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 核心组件

#### 1.2.1 CLI组件 (webmon.py)
- **职责**: 用户交互接口
- **输入**: 命令行参数
- **输出**: 控制台输出、日志文件
- **依赖**: Core Logic Layer

#### 1.2.2 任务管理器 (TaskManager)
- **职责**: 管理监控任务生命周期
- **功能**: 任务CRUD、任务调度、状态管理
- **存储**: config.json

#### 1.2.3 变化检测器 (ChangeDetector)
- **职责**: 检测网页内容变化
- **算法**: 哈希比对 + 相似度计算
- **配置**: 阈值、选择器、过滤器

#### 1.2.4 通知服务 (NotificationService)
- **职责**: 多平台消息推送
- **平台**: PushPlus, Telegram, Discord, 飞书
- **模板**: 可自定义消息格式

#### 1.2.5 浏览器引擎 (Playwright)
- **职责**: 网页内容获取
- **功能**: JS渲染、动态等待、反检测
- **配置**: 无头模式、超时、重试

#### 1.2.6 AI分析服务 (AIAnalysisService) - 新增
- **职责**: 智能分析网页变化内容
- **功能**:
  - 调用AI模型（DeepSeek R1 / OpenAI兼容API）
  - 提示词模板渲染（占位符替换）
  - 生成自然语言变化摘要
- **配置**:
  - API URL、API Key、模型名称
  - 最大token数、温度参数、超时时间
  - 系统提示词、用户提示词模板
- **降级策略**: AI调用失败时使用原始变化内容

## 2. 详细设计

### 2.1 类结构设计

```python
# 主应用类
class WebMon:
    """主应用类，协调各组件工作"""
    def __init__(self):
        self.config_manager = ConfigManager()
        self.task_manager = TaskManager()
        self.change_detector = ChangeDetector()
        self.notification_service = NotificationService()
        self.browser_engine = BrowserEngine()
    
    def run_command(self, command, args):
        """执行CLI命令"""
        pass

# 配置管理器
class ConfigManager:
    """配置管理，处理.env和config.json"""
    def __init__(self):
        self.env_config = EnvConfig()
        self.json_config = JsonConfig()
    
    def get(self, key, default=None):
        """获取配置值"""
        pass
    
    def set(self, key, value):
        """设置配置值"""
        pass

# 任务管理器
class TaskManager:
    """监控任务管理"""
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.tasks = []
    
    def add_task(self, task):
        """添加任务"""
        pass
    
    def remove_task(self, task_id):
        """删除任务"""
        pass
    
    def list_tasks(self):
        """列出任务"""
        pass
    
    def get_task(self, task_id):
        """获取任务"""
        pass

# 变化检测器
class ChangeDetector:
    """内容变化检测"""
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.history = {}
    
    def detect_changes(self, url, new_content):
        """检测变化"""
        pass
    
    def extract_meaningful_content(self, content):
        """提取有意义内容"""
        pass
    
    def calculate_similarity(self, old_content, new_content):
        """计算相似度"""
        pass

# 通知服务
class NotificationService:
    """多平台通知服务"""
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.platforms = {}
    
    def send_notification(self, message, platforms=None):
        """发送通知"""
        pass
    
    def register_platform(self, name, platform):
        """注册推送平台"""
        pass

# 浏览器引擎
class BrowserEngine:
    """Playwright浏览器引擎"""
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.playwright = None
        self.browser = None

    async def get_page_content(self, url, selectors=None):
        """获取页面内容"""
        pass

    async def setup_browser(self):
        """设置浏览器"""
        pass

    async def close_browser(self):
        """关闭浏览器"""
        pass

# AI分析服务 - 新增
class AIAnalysisService:
    """AI智能分析服务"""
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.ai_config = None
        self.http_client = None

    def load_config(self):
        """加载AI配置"""
        pass

    def render_prompt(self, template: str, context: dict) -> str:
        """渲染提示词模板，替换占位符

        支持的占位符:
        - {task_name}: 任务名称
        - {url}: 监控URL
        - {description}: 任务描述
        - {changes}: 变动内容
        - {old_content}: 旧内容摘要
        - {new_content}: 新内容摘要
        """
        pass

    async def analyze_changes(self, task: Task, changes: dict) -> AIAnalysisResult:
        """分析变化内容

        Args:
            task: 监控任务
            changes: 变化详情字典

        Returns:
            AIAnalysisResult: 分析结果
        """
        pass

    async def call_ai_api(self, system_prompt: str, user_prompt: str) -> str:
        """调用AI API

        支持OpenAI兼容API (DeepSeek, OpenAI, Claude等)
        """
        pass

    def get_fallback_summary(self, changes: dict) -> str:
        """获取降级摘要（AI调用失败时使用）"""
        pass
```

### 2.2 数据模型设计

#### 2.2.1 任务模型 (Task)
```python
@dataclass
class Task:
    id: str                    # 任务唯一ID
    url: str                   # 监控URL
    name: str                  # 任务名称
    description: str           # 任务描述（用于AI分析上下文）- 新增
    selectors: List[str]       # CSS选择器列表
    interval: int              # 检测间隔（秒）
    timeout: int               # 超时时间（毫秒）
    enabled: bool              # 是否启用
    created_at: datetime       # 创建时间
    updated_at: datetime       # 更新时间
    last_check: datetime       # 最后检测时间
    last_change: datetime      # 最后变化时间
    change_count: int          # 变化次数
    status: str                # 任务状态
```

#### 2.2.2 检测结果模型 (CheckResult)
```python
@dataclass
class CheckResult:
    task_id: str               # 任务ID
    url: str                   # 检测URL
    timestamp: datetime        # 检测时间
    success: bool              # 是否成功
    content_hash: str          # 内容哈希
    content_size: int          # 内容大小
    load_time: float           # 加载时间（秒）
    changed: bool              # 是否变化
    change_type: str           # 变化类型
    error_message: str         # 错误信息（如果有）
    extracted_data: dict       # 提取的数据
```

#### 2.2.3 变化详情模型 (ChangeDetails)
```python
@dataclass
class ChangeDetails:
    task_id: str               # 任务ID
    url: str                   # URL
    timestamp: datetime        # 检测时间
    similarity: float          # 相似度
    changes: dict              # 变化详情
    old_content: str           # 旧内容摘要
    new_content: str           # 新内容摘要
    change_summary: str        # 变化总结
```

#### 2.2.4 通知消息模型 (Notification)
```python
@dataclass
class Notification:
    title: str                 # 消息标题
    content: str               # 消息内容
    url: str                   # 相关URL
    timestamp: datetime        # 时间戳
    urgency: str               # 紧急程度
    platforms: List[str]       # 目标平台
    ai_summary: str            # AI分析摘要（新增）
```

#### 2.2.5 AI分析结果模型 (AIAnalysisResult) - 新增
```python
@dataclass
class AIAnalysisResult:
    task_id: str               # 任务ID
    success: bool              # 分析是否成功
    summary: str               # AI生成的摘要
    model: str                 # 使用的模型
    tokens_used: int           # 消耗的token数
    latency: float             # 响应延迟（秒）
    timestamp: datetime        # 分析时间
    error_message: str         # 错误信息（如果失败）
```

#### 2.2.6 AI配置模型 (AIConfig) - 新增
```python
@dataclass
class AIConfig:
    enabled: bool              # 是否启用AI分析
    api_url: str               # API端点URL
    api_key: str               # API密钥
    model: str                 # 模型名称（如 deepseek-reasoner）
    max_tokens: int            # 最大生成token数
    temperature: float         # 温度参数（0.0-1.0）
    timeout: int               # 请求超时时间（秒）
    system_prompt: str         # 系统提示词
    user_prompt_template: str  # 用户提示词模板
```

### 2.3 配置设计

#### 2.3.1 环境变量配置 (.env)
```bash
# ==============================================
# WebMon - 网页监控工具环境变量配置
# ==============================================

# 推送平台配置
PUSHPLUS_TOKEN=                    # PushPlus令牌
TELEGRAM_BOT_TOKEN=                # Telegram Bot令牌
TELEGRAM_CHAT_ID=                  # Telegram聊天ID
DISCORD_WEBHOOK_URL=               # Discord Webhook URL
FEISHU_WEBHOOK_URL=                # 飞书Webhook URL

# AI分析配置（新增）
AI_API_URL=https://api.deepseek.com/v1    # AI API端点URL
AI_API_KEY=                               # AI API密钥
AI_MODEL=deepseek-reasoner                # 模型名称
AI_MAX_TOKENS=2048                        # 最大生成token数
AI_TEMPERATURE=0.7                        # 温度参数
AI_TIMEOUT=60                             # 请求超时时间（秒）
AI_ENABLED=true                           # 是否启用AI分析

# 监控配置
DEFAULT_INTERVAL=300               # 默认检测间隔（秒）
DEFAULT_TIMEOUT=30000              # 默认超时时间（毫秒）
MAX_RETRIES=3                      # 最大重试次数
BROWSER_HEADLESS=true              # 浏览器无头模式

# 检测配置
SIMILARITY_THRESHOLD=0.85          # 相似度阈值
ENABLE_SMART_DETECTION=true        # 启用智能检测
MIN_CHANGE_LENGTH=10               # 最小变化长度

# 日志配置
LOG_LEVEL=INFO                     # 日志级别
LOG_FILE=logs/webmon.log           # 日志文件路径
LOG_MAX_SIZE=10MB                  # 日志文件最大大小
LOG_BACKUP_COUNT=5                 # 日志备份数量

# 高级配置
CONCURRENT_TASKS=5                 # 并发任务数
RATE_LIMIT_PER_MINUTE=30           # 每分钟请求限制
PROXY_URL=                         # 代理服务器URL
CUSTOM_USER_AGENT=                 # 自定义User-Agent
```

#### 2.3.2 JSON配置文件 (config.json)
```json
{
  "version": "1.0.0",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",

  "monitoring": {
    "default_interval": 300,
    "default_timeout": 30000,
    "max_retries": 3,
    "concurrent_tasks": 5,
    "browser_headless": true,
    "rate_limit": {
      "requests_per_minute": 30,
      "retry_delay": 60
    }
  },

  "detection": {
    "enable_smart_detection": true,
    "similarity_threshold": 0.85,
    "min_change_length": 10,
    "ignore_selectors": [
      ".advertisement",
      ".cookie-banner",
      ".timestamp",
      ".view-count"
    ],
    "extract_fields": {
      "title": "title",
      "description": "meta[name='description']",
      "headlines": "h1, h2, h3",
      "links": "a[href]",
      "images": "img[src]"
    }
  },

  "ai": {
    "enabled": true,
    "api_url": "${AI_API_URL}",
    "api_key": "${AI_API_KEY}",
    "model": "deepseek-reasoner",
    "max_tokens": 2048,
    "temperature": 0.7,
    "timeout": 60,
    "system_prompt": "你是一个专业的网页内容变化分析助手。你的任务是：\n1. 分析网页内容的变化\n2. 提取用户可能关注的关键信息\n3. 用简洁的自然语言总结变化要点\n4. 如果变化涉及价格、时间、状态等重要信息，请特别指出\n\n请用中文回复，保持简洁（不超过200字），重点突出关键变化。",
    "user_prompt_template": "## 监控任务信息\n- 任务名称：{task_name}\n- 监控URL：{url}\n- 任务描述：{description}\n\n## 检测到的变化内容\n{changes}\n\n请分析以上变化，提取关键信息并生成简洁的摘要。"
  },

  "notification": {
    "platforms": ["pushplus"],
    "template": {
      "title": "🎯 网页变化检测通知",
      "content": "📍 URL: {url}\n⏰ 时间: {timestamp}\n📝 变化: {summary}\n\n🤖 AI分析：\n{ai_summary}\n\n🔗 查看: {url}",
      "rate_limit": 60
    },
    "platform_configs": {
      "pushplus": {
        "enabled": true,
        "token": "${PUSHPLUS_TOKEN}"
      },
      "telegram": {
        "enabled": false,
        "bot_token": "${TELEGRAM_BOT_TOKEN}",
        "chat_id": "${TELEGRAM_CHAT_ID}"
      },
      "discord": {
        "enabled": false,
        "webhook_url": "${DISCORD_WEBHOOK_URL}"
      },
      "feishu": {
        "enabled": false,
        "webhook_url": "${FEISHU_WEBHOOK_URL}"
      }
    }
  },

  "tasks": [
    {
      "id": "example_task",
      "url": "https://example.com",
      "name": "示例任务",
      "description": "监控示例网站，关注价格变化和重要公告",
      "selectors": [".content"],
      "interval": 300,
      "enabled": true
    }
  ],

  "storage": {
    "history_file": "data/history.json",
    "max_history_entries": 1000,
    "auto_cleanup_days": 30
  }
}
```

### 2.4 算法设计

#### 2.4.1 变化检测算法
```python
class ChangeDetectionAlgorithm:
    """变化检测算法"""
    
    def basic_hash_detection(self, old_content, new_content):
        """基础哈希检测"""
        old_hash = hashlib.md5(old_content.encode()).hexdigest()
        new_hash = hashlib.md5(new_content.encode()).hexdigest()
        
        return {
            'changed': old_hash != new_hash,
            'old_hash': old_hash,
            'new_hash': new_hash,
            'algorithm': 'basic_hash'
        }
    
    def similarity_detection(self, old_content, new_content, threshold=0.85):
        """相似度检测"""
        from difflib import SequenceMatcher
        
        similarity = SequenceMatcher(None, old_content, new_content).ratio()
        
        return {
            'changed': similarity < threshold,
            'similarity': similarity,
            'threshold': threshold,
            'algorithm': 'similarity'
        }
    
    def structured_detection(self, old_data, new_data):
        """结构化数据检测"""
        changes = {}
        
        # 比较各个字段
        for field in new_data.keys():
            if field in old_data and old_data[field] != new_data[field]:
                changes[field] = {
                    'old': old_data[field],
                    'new': new_data[field]
                }
        
        return {
            'changed': len(changes) > 0,
            'changes': changes,
            'algorithm': 'structured'
        }
```

#### 2.4.2 内容提取算法
```python
class ContentExtractionAlgorithm:
    """内容提取算法"""
    
    def extract_text_content(self, html_content):
        """提取文本内容"""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 移除脚本和样式
        for element in soup(['script', 'style', 'nav', 'footer', 'aside']):
            element.decompose()
        
        # 提取文本
        text = soup.get_text(separator=' ', strip=True)
        
        # 清理空白字符
        text = re.sub(r'\s+', ' ', text)
        
        return text[:5000]  # 限制长度
    
    def extract_structured_data(self, html_content, selectors):
        """提取结构化数据"""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html_content, 'html.parser')
        data = {}
        
        for name, selector in selectors.items():
            elements = soup.select(selector)
            if elements:
                if len(elements) == 1:
                    data[name] = elements[0].get_text(strip=True)
                else:
                    data[name] = [elem.get_text(strip=True) for elem in elements]
        
        return data
    
    def extract_links(self, html_content):
        """提取链接"""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html_content, 'html.parser')
        links = []
        
        for link in soup.find_all('a', href=True):
            links.append({
                'text': link.get_text(strip=True),
                'href': link['href'],
                'title': link.get('title', '')
            })
        
        return links
```

#### 2.4.3 AI分析算法 - 新增
```python
class AIAnalysisAlgorithm:
    """AI智能分析算法"""

    def __init__(self, config: AIConfig):
        self.config = config
        self.http_client = httpx.AsyncClient(timeout=config.timeout)

    def render_user_prompt(self, task: Task, changes: dict) -> str:
        """渲染用户提示词模板

        支持的占位符:
        - {task_name}: 任务名称
        - {url}: 监控URL
        - {description}: 任务描述
        - {changes}: 变动内容（格式化后的字符串）
        - {old_content}: 旧内容摘要
        - {new_content}: 新内容摘要
        """
        # 格式化变化内容
        changes_text = self._format_changes(changes)

        # 替换占位符
        prompt = self.config.user_prompt_template
        prompt = prompt.replace('{task_name}', task.name)
        prompt = prompt.replace('{url}', task.url)
        prompt = prompt.replace('{description}', task.description or '无')
        prompt = prompt.replace('{changes}', changes_text)
        prompt = prompt.replace('{old_content}', changes.get('old_content', ''))
        prompt = prompt.replace('{new_content}', changes.get('new_content', ''))

        return prompt

    def _format_changes(self, changes: dict) -> str:
        """格式化变化内容为可读文本"""
        if not changes:
            return "无明显变化"

        lines = []
        for key, value in changes.items():
            if isinstance(value, dict) and 'old' in value and 'new' in value:
                lines.append(f"- {key}: {value['old']} → {value['new']}")
            else:
                lines.append(f"- {key}: {value}")

        return '\n'.join(lines)

    async def call_openai_compatible_api(
        self,
        system_prompt: str,
        user_prompt: str
    ) -> AIAnalysisResult:
        """调用OpenAI兼容API

        支持: DeepSeek, OpenAI, Azure OpenAI, 通义千问等
        """
        start_time = time.time()

        try:
            response = await self.http_client.post(
                f"{self.config.api_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.config.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.config.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "max_tokens": self.config.max_tokens,
                    "temperature": self.config.temperature
                }
            )

            response.raise_for_status()
            data = response.json()

            return AIAnalysisResult(
                success=True,
                summary=data['choices'][0]['message']['content'],
                model=self.config.model,
                tokens_used=data.get('usage', {}).get('total_tokens', 0),
                latency=time.time() - start_time,
                timestamp=datetime.now(),
                error_message=None
            )

        except Exception as e:
            return AIAnalysisResult(
                success=False,
                summary=self.get_fallback_summary(changes),
                model=self.config.model,
                tokens_used=0,
                latency=time.time() - start_time,
                timestamp=datetime.now(),
                error_message=str(e)
            )

    def get_fallback_summary(self, changes: dict) -> str:
        """获取降级摘要（AI调用失败时使用）"""
        if not changes:
            return "检测到页面变化，但无法获取详细信息。"

        change_count = len(changes)
        return f"检测到 {change_count} 处变化。（AI分析暂时不可用）"
```

### 2.5 异常处理设计

#### 2.5.1 异常分类
```python
class WebMonException(Exception):
    """基础异常类"""
    pass

class ConfigurationError(WebMonException):
    """配置错误"""
    pass

class NetworkError(WebMonException):
    """网络错误"""
    pass

class BrowserError(WebMonException):
    """浏览器错误"""
    pass

class DetectionError(WebMonException):
    """检测错误"""
    pass

class NotificationError(WebMonException):
    """通知错误"""
    pass

class StorageError(WebMonException):
    """存储错误"""
    pass

class AIAnalysisError(WebMonException):
    """AI分析错误 - 新增"""
    pass

class AIConfigError(AIAnalysisError):
    """AI配置错误 - 新增"""
    pass

class AIAPIError(AIAnalysisError):
    """AI API调用错误 - 新增"""
    pass

class AITimeoutError(AIAnalysisError):
    """AI请求超时错误 - 新增"""
    pass
```

#### 2.5.2 异常处理策略
```python
class ExceptionHandler:
    """异常处理器"""
    
    def handle_browser_error(self, error, context):
        """处理浏览器异常"""
        if "Timeout" in str(error):
            return {
                'error_type': 'timeout',
                'message': '页面加载超时，请检查网络连接或增加超时时间',
                'suggestion': '尝试增加DEFAULT_TIMEOUT配置'
            }
        elif "Navigation" in str(error):
            return {
                'error_type': 'navigation_failed',
                'message': '页面导航失败，请检查URL是否正确',
                'suggestion': '验证URL是否可访问'
            }
        else:
            return {
                'error_type': 'browser_error',
                'message': f'浏览器错误: {str(error)}',
                'suggestion': '检查浏览器配置或目标网站状态'
            }
    
    def handle_network_error(self, error, context):
        """处理网络异常"""
        if "Connection" in str(error):
            return {
                'error_type': 'connection_error',
                'message': '网络连接失败',
                'suggestion': '检查网络连接状态'
            }
        elif "SSL" in str(error):
            return {
                'error_type': 'ssl_error',
                'message': 'SSL证书验证失败',
                'suggestion': '检查目标网站的SSL配置'
            }
        else:
            return {
                'error_type': 'network_error',
                'message': f'网络错误: {str(error)}',
                'suggestion': '检查网络配置或稍后重试'
            }
```

## 3. 接口设计

### 3.1 CLI接口

#### 3.1.1 命令接口
```python
# 命令基类
class Command:
    """命令基类"""
    
    def __init__(self, app):
        self.app = app
    
    def execute(self, args):
        """执行命令"""
        raise NotImplementedError
    
    def validate_args(self, args):
        """验证参数"""
        pass
    
    def format_output(self, result, format_type='table'):
        """格式化输出"""
        pass

# 具体命令实现
class InitCommand(Command):
    """初始化命令"""
    
    def execute(self, args):
        # 创建配置文件
        # 创建.env文件
        # 初始化目录结构
        pass

class AddCommand(Command):
    """添加任务命令"""
    
    def execute(self, args):
        # 验证URL格式
        # 检查任务是否已存在
        # 创建新任务
        # 保存配置
        pass

class StartCommand(Command):
    """启动监控命令"""
    
    def execute(self, args):
        # 加载任务列表
        # 初始化浏览器
        # 启动监控循环
        # 处理中断信号
        pass
```

#### 3.1.2 参数解析
```python
class ArgumentParser:
    """参数解析器"""
    
    def __init__(self):
        self.commands = {
            'init': InitCommand,
            'add': AddCommand,
            'remove': RemoveCommand,
            'list': ListCommand,
            'start': StartCommand,
            'stop': StopCommand,
            'status': StatusCommand,
            'test': TestCommand,
            'history': HistoryCommand
        }
    
    def parse(self, argv):
        """解析命令行参数"""
        if len(argv) < 2:
            return self.show_help()
        
        command_name = argv[1]
        if command_name not in self.commands:
            return self.show_error(f"未知命令: {command_name}")
        
        command_class = self.commands[command_name]
        command_args = argv[2:]
        
        return command_name, command_class, command_args
```

### 3.2 内部接口

#### 3.2.1 任务管理接口
```python
class ITaskManager(ABC):
    """任务管理器接口"""
    
    @abstractmethod
    def add_task(self, task: Task) -> str:
        """添加任务"""
        pass
    
    @abstractmethod
    def remove_task(self, task_id: str) -> bool:
        """删除任务"""
        pass
    
    @abstractmethod
    def update_task(self, task_id: str, updates: dict) -> bool:
        """更新任务"""
        pass
    
    @abstractmethod
    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务"""
        pass
    
    @abstractmethod
    def list_tasks(self) -> List[Task]:
        """列出任务"""
        pass
```

#### 3.2.2 变化检测接口
```python
class IChangeDetector(ABC):
    """变化检测器接口"""
    
    @abstractmethod
    def detect_changes(self, url: str, new_content: str) -> dict:
        """检测变化"""
        pass
    
    @abstractmethod
    def extract_content(self, html_content: str, selectors: List[str]) -> dict:
        """提取内容"""
        pass
    
    @abstractmethod
    def compare_content(self, old_data: dict, new_data: dict) -> dict:
        """比较内容"""
        pass
```

#### 3.2.3 通知服务接口
```python
class INotificationService(ABC):
    """通知服务接口"""
    
    @abstractmethod
    def send(self, notification: Notification) -> bool:
        """发送通知"""
        pass
    
    @abstractmethod
    def register_platform(self, name: str, platform) -> bool:
        """注册平台"""
        pass
    
    @abstractmethod
    def get_supported_platforms(self) -> List[str]:
        """获取支持的平台列表"""
        pass
```

## 4. 存储设计

### 4.1 项目目录结构

#### 4.1.1 完整目录树
```
airdrop-watcher/
├── archive/                    # 归档目录
│   ├── debug_files/           # 调试文件归档
│   ├── demo_logs/             # 演示日志归档
│   ├── my_logs/               # 个人��志归档
│   └── test_files/            # 测试文件归档
├── backup/                     # 配置备份目录
│   └── config_*.json          # 按时间戳命名的配置备份
├── config/                     # 配置文件目录
│   ├── backup/                # 配置备份子目录
│   └── config.json            # 主配置文件
├── data/                       # 运行时数据目录
│   ├── backup/                # 数据备份
│   └── history.json           # 历史检测记录
├── docs/                       # 项目文档目录
│   ├── design.md              # 设计文档
│   ├── requirements.md        # 需求文档
│   ├── tasks.md               # 任务跟踪
│   ├── logging_config_guide.md      # 日志配置指南
│   ├── scheduler_config.md          # 调度器配置文档
│   ├── project_progress_analysis.md # 项目进度分析
│   └── stage*_summary.md            # 各阶段总结文档
├── examples/                   # 示例代码目录
│   ├── logging_config_demo.py       # 日志配���示例
│   └── scheduler_config_example.py  # 调度器配置示例
├── logs/                       # 日志文件目录
│   ├── webmon.log             # 当前日志文件（软链接）
│   └── webmon_YYYY-MM-DD.log  # 按日期轮转的日志文件
├── tests/                      # 单元测试目录
│   ├── test_browser_engine.py      # 浏览器引擎测试
│   ├── test_cli_commands.py        # CLI命令测试
│   └── test_task_scheduler.py      # 任务调度器测试
├── webmon/                     # 主程序包目录
│   ├── browser/               # 浏览器引擎模块
│   │   ├── __init__.py
│   │   └── browser_engine.py       # Playwright浏览器封装
│   ├── cli/                   # 命令行接口模块
│   │   ├── __init__.py
│   │   ├── app.py                  # CLI应用主类
│   │   └── commands/               # 各种CLI命令实现
│   ├── config/                # 配置管理模块
│   │   ├── __init__.py
│   │   ├── config_manager.py       # 配置管理器
│   │   ├── env_config.py           # 环境变量配置
│   │   └── json_config.py          # JSON配置处理
│   ├── core/                  # 核心业务逻辑
│   │   ├── __init__.py
│   │   └── monitor.py              # 监控核心逻辑
│   ├── detection/             # 变化检测模块
│   │   ├── __init__.py
│   │   ├── change_detector.py      # 变化检测器
│   │   └── content_extractor.py    # 内容提取器
│   ├── exceptions/            # 异常定义模块
│   │   ├── __init__.py
│   │   └── exceptions.py           # 自定义异常类
│   ├── models/                # 数据模型模块
│   │   ├── __init__.py
│   │   ├── task.py                 # 任务模型
│   │   ├── check_result.py         # 检测结果模型
│   │   └── notification.py         # 通知消息模型
│   ├── notification/          # 通知服务模块
│   │   ├── __init__.py
│   │   ├── factory.py              # 通知平台工厂
│   │   ├── base.py                 # 通知基类
│   │   └── platforms/              # 各平台实现
│   ├── scheduler/             # 任务调度模块
│   │   ├── __init__.py
│   │   └── task_scheduler.py       # 任务调度器
│   ├── storage/               # 数据存储模块
│   │   ├── __init__.py
│   │   ├── task_storage.py         # 任务存储
│   │   └── history_storage.py      # 历史记录存储
│   ├── utils/                 # 工具函数模块
│   │   ├── __init__.py
│   │   ├── logger.py               # 日志工具
│   │   └── helpers.py              # 辅助函数
│   └── __init__.py            # 包初始化文件
├── .claude/                    # Claude Code配置目录
│   └── settings.local.json    # Claude本地设置
├── .env                        # 环境变量配置（敏感信息）
├── .env.example                # 环境变量配置模板
├── .gitignore                  # Git忽略规则
├── claude.md                   # Claude Code使用规范
├── config.json                 # 主配置文件（根目录）
├── project_progress_report.md  # 项目进度报告
├── README.md                   # 项目说明文档
├── requirements.txt            # Python依赖列表
└── webmon.py                   # 程序入口文件
```

#### 4.1.2 目录说明

**顶级目录**
- `archive/`: 归档临时文件和调试文件，避免污染主目录
- `backup/`: 存放配置文件的备份，按时间戳命名
- `config/`: 配置文件专用目录（备用，主要使用根目录的config.json）
- `data/`: 运行时生成的数据文件（历史记录、缓存等）
- `docs/`: 所有项目文档，包括设计文档、需求文档、阶段总结等
- `examples/`: 示例代码和配置示例，帮助用户快速上手
- `logs/`: 日志文件目录，支持日志轮转
- `tests/`: 单元测试和集成测试
- `webmon/`: 主程序包，包含所有业务逻辑代码

**webmon包结构**
- `browser/`: 浏览器引擎封装，基于Playwright实现
- `cli/`: 命令行接口，包含所有CLI命令的实现
- `config/`: 配置管理，处理.env和config.json
- `core/`: 核心业务逻辑，监控主流程
- `detection/`: 内容变化检测算法
- `exceptions/`: 自定义异常类定义
- `models/`: 数据模型定义（Task、CheckResult等）
- `notification/`: 多平台通知服务
- `scheduler/`: 任务调度器，处理并发和定时执行
- `storage/`: 数据持久化层
- `utils/`: 通用工具函数

**配置文件**
- `.env`: 环境变量配置，包含敏感信息（API密钥等），不提交到Git
- `.env.example`: 环境变量模板，可以提交到Git
- `config.json`: 主配置文件，存储任务列表和系统设置
- `.gitignore`: Git忽略规则
- `claude.md`: Claude Code使用规范和Token报告规则

**文档文件**
- `README.md`: 项目说明和快速开始指南
- `requirements.txt`: Python依赖包列表
- `project_progress_report.md`: 项目进度跟踪报告

#### 4.1.3 文件组织原则

1. **关注点分离**: 不同功能模块放在独立的目录中
2. **清晰命名**: 目录和文件名能清楚表达其用途
3. **避免污染**: 临时文件、调试文件统一放入archive/
4. **可测试性**: tests/目录镜像webmon/包结构
5. **文档完整**: docs/集中管理所有文档
6. **配置分离**: 敏感配置(.env)与公开配置(config.json)分离

### 4.2 数据存储格式

#### 4.2.1 任务存储 (config.json)
```json
{
  "version": "1.0.0",
  "tasks": [
    {
      "id": "task_123456",
      "url": "https://example.com/news",
      "name": "示例新闻网站",
      "selectors": [".news-item", "h1"],
      "interval": 300,
      "timeout": 30000,
      "enabled": true,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z",
      "last_check": "2024-01-01T00:00:00Z",
      "last_change": "2024-01-01T00:00:00Z",
      "change_count": 5,
      "status": "active"
    }
  ]
}
```

#### 4.2.2 历史记录存储 (data/history.json)
```json
{
  "version": "1.0.0",
  "entries": [
    {
      "id": "history_123456",
      "task_id": "task_123456",
      "url": "https://example.com/news",
      "timestamp": "2024-01-01T00:00:00Z",
      "success": true,
      "changed": true,
      "change_type": "content_change",
      "content_hash": "abc123...",
      "content_size": 1024,
      "load_time": 2.5,
      "changes": {
        "title": {
          "old": "旧标题",
          "new": "新标题"
        }
      },
      "extracted_data": {
        "title": "页面标题",
        "links": []
      }
    }
  ]
}
```

## 5. 并发设计

### 5.1 任务调度设计
```python
import asyncio
from asyncio import Semaphore

class TaskScheduler:
    """任务调度器"""
    
    def __init__(self, max_concurrent=5):
        self.max_concurrent = max_concurrent
        self.semaphore = Semaphore(max_concurrent)
        self.running_tasks = {}
    
    async def schedule_tasks(self, tasks):
        """调度多个任务"""
        async with asyncio.TaskGroup() as tg:
            for task in tasks:
                tg.create_task(self.execute_task(task))
    
    async def execute_task(self, task):
        """执行单个任务"""
        async with self.semaphore:
            try:
                # 获取浏览器实例
                browser = await self.get_browser()
                
                # 获取页面内容
                content = await browser.get_page_content(task.url, task.selectors)
                
                # 检测变化
                result = await self.change_detector.detect_changes(task.url, content)
                
                # 发送通知（如果有变化）
                if result['changed']:
                    await self.send_notification(task, result)
                
                # 更新任务状态
                await self.update_task_status(task, result)
                
            except Exception as e:
                await self.handle_task_error(task, e)
            finally:
                await self.release_browser(browser)
```

### 5.2 资源管理
```python
class ResourceManager:
    """资源管理器"""
    
    def __init__(self, max_browsers=3):
        self.max_browsers = max_browsers
        self.browser_pool = []
        self.semaphore = Semaphore(max_browsers)
    
    async def get_browser(self):
        """获取浏览器实例"""
        async with self.semaphore:
            if self.browser_pool:
                return self.browser_pool.pop()
            else:
                return await self.create_browser()
    
    async def release_browser(self, browser):
        """释放浏览器实例"""
        if len(self.browser_pool) < self.max_browsers:
            self.browser_pool.append(browser)
        else:
            await browser.close()
    
    async def create_browser(self):
        """创建新的浏览器实例"""
        # 创建Playwright浏览器实例
        pass
    
    async def cleanup(self):
        """清理资源"""
        for browser in self.browser_pool:
            await browser.close()
```

## 6. 安全设计

### 6.1 敏感信息保护
```python
class SecurityManager:
    """安全管理器"""
    
    def __init__(self):
        self.sensitive_keys = [
            'PUSHPLUS_TOKEN',
            'TELEGRAM_BOT_TOKEN',
            'DISCORD_WEBHOOK_URL',
            'FEISHU_WEBHOOK_URL'
        ]
    
    def mask_sensitive_data(self, data):
        """屏蔽敏感数据"""
        if isinstance(data, dict):
            masked_data = {}
            for key, value in data.items():
                if key in self.sensitive_keys and value:
                    masked_data[key] = self.mask_string(value)
                else:
                    masked_data[key] = value
            return masked_data
        return data
    
    def mask_string(self, text, visible_chars=4):
        """屏蔽字符串"""
        if len(text) <= visible_chars * 2:
            return '*' * len(text)
        
        start = text[:visible_chars]
        end = text[-visible_chars:]
        middle = '*' * (len(text) - visible_chars * 2)
        
        return f"{start}{middle}{end}"
```

### 6.2 网络安全
```python
class NetworkSecurity:
    """网络安全"""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
    
    def setup_secure_headers(self):
        """设置安全请求头"""
        return {
            'User-Agent': self.get_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
    
    def get_user_agent(self):
        """获取User-Agent"""
        custom_ua = self.config_manager.get('CUSTOM_USER_AGENT')
        if custom_ua:
            return custom_ua
        
        return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    
    def validate_url(self, url):
        """验证URL安全性"""
        parsed = urlparse(url)
        
        # 检查协议
        if parsed.scheme not in ['http', 'https']:
            raise ValueError(f"不支持的协议: {parsed.scheme}")
        
        # 检查主机名
        if not parsed.hostname:
            raise ValueError("无效的主机名")
        
        # 检查私有IP
        if self.is_private_ip(parsed.hostname):
            raise ValueError("不允许监控私有IP地址")
        
        return True
```

## 7. 性能设计

### 7.1 性能优化策略
```python
class PerformanceOptimizer:
    """性能优化器"""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
    
    def optimize_browser_settings(self, browser_context):
        """优化浏览器设置"""
        # 禁用图片加载
        browser_context.route("**/*.{png,jpg,jpeg,gif,svg}", lambda route: route.abort())
        
        # 禁用字体加载
        browser_context.route("**/*.{woff,woff2,ttf}", lambda route: route.abort())
        
        # 禁用CSS（可选）
        if not self.config_manager.get('LOAD_CSS', True):
            browser_context.route("**/*.css", lambda route: route.abort())
        
        # 禁用视频和音频
        browser_context.route("**/*.{mp4,mp3,avi}", lambda route: route.abort())
    
    def optimize_page_loading(self, page):
        """优化页面加载"""
        # 设置合理的超时
        timeout = self.config_manager.get('DEFAULT_TIMEOUT', 30000)
        page.set_default_timeout(timeout)
        
        # 设置网络拦截
        page.route("**/*.{png,jpg,jpeg,gif,svg,css,woff,woff2}", lambda route: route.abort())
    
    def implement_caching(self, url):
        """实现缓存机制"""
        # 实现简单的内存缓存
        cache_key = f"content_{hash(url)}"
        cache_timeout = 60  # 60秒缓存
        
        # 检查缓存
        if hasattr(self, '_cache') and cache_key in self._cache:
            cached_data = self._cache[cache_key]
            if time.time() - cached_data['timestamp'] < cache_timeout:
                return cached_data['content']
        
        return None
```

### 7.2 内存管理
```python
class MemoryManager:
    """内存管理器"""
    
    def __init__(self, max_memory_mb=500):
        self.max_memory_mb = max_memory_mb
        self.memory_monitor = MemoryMonitor()
    
    def check_memory_usage(self):
        """检查内存使用"""
        current_memory = self.memory_monitor.get_current_memory_mb()
        
        if current_memory > self.max_memory_mb:
            self.perform_memory_cleanup()
            
            # 如果仍然超过限制，发出警告
            new_memory = self.memory_monitor.get_current_memory_mb()
            if new_memory > self.max_memory_mb:
                logger.warning(f"内存使用超过限制: {new_memory}MB > {self.max_memory_mb}MB")
    
    def perform_memory_cleanup(self):
        """执行内存清理"""
        # 清理浏览器缓存
        gc.collect()
        
        # 清理大对象
        if hasattr(self, '_large_objects'):
            self._large_objects.clear()
        
        # 强制垃圾回收
        gc.collect()
```

---

**设计文档版本**: v1.0
**最后更新**: 2024年
**架构师**: WebMon开发团队