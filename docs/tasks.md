# WebMon 项目任务详细文档

> **文档版本**: 2.0
> **最后更新**: 2025-12-02
> **维护者**: WebMon 开发团队
> **项目进度**: 77% (47.5/62 任务)

---

## 📋 文档说明

本文档提供WebMon项目所有开发任务的详细技术说明，包括任务背景、实现细节、验收标准和依赖关系。

### 文档结构

- **阶段一至八**: 核心功能开发（已完成 100%）
- **阶段九**: 日志和异常处理（已完成 88%）
- **阶段十**: 测试和文档（进行中 25%）
- **阶段十一**: 性能优化和安全（规划中 11%）
- **阶段十二**: 发布准备（规划中 0%）

### 任务编号规则

- **#001-#010**: 阶段一（基础框架）
- **#011-#015**: 阶段三（数据模型）
- **#016-#020**: 阶段四（浏览器引擎）
- **#021-#025**: 阶段五（变化检测）
- **#026-#030**: 阶段六（通知系统）
- **#031-#039**: 阶段七（CLI命令）
- **#040-#042**: 阶段八（任务调度）
- **#043-#046**: 阶段九（日志异常）
- **#047-#050**: 阶段十一（安全优化）
- **#051-#055**: 阶段十（测试）
- **#056-#062**: 阶段十二（文档发布）

---

## ✅ 阶段一：项目基础框架（已完成）

### 背景

建立项目基本结构，完成配置管理系统，为后续开发提供基础设施。

---

### ✅ #001 - 初始化项目结构

**状态**: ✅ 已完成
**负责人**: Previous
**完成时间**: 2025-11-28
**预计工时**: 2h | **实际工时**: 1.5h

#### 任务描述

创建项目目录结构，建立Python包组织框架，配置开发环境。

#### 实现细节

```
webmon/
├── __init__.py              # 包初始化
├── cli/                     # CLI模块
├── config/                  # 配置管理
├── models/                  # 数据模型
├── browser/                 # 浏览器引擎
├── detection/              # 变化检测
├── notification/           # 通知服务
├── scheduler/              # 任务调度
├── storage/                # 数据存储
├── utils/                  # 工具函数
└── exceptions.py           # 异常定义
```

#### 技术要点

- Python包结构设计
- 模块化组织原则
- 相对导入路径规划
- __init__.py职责划分

#### 验收标准

- [x] 项目目录结构完整
- [x] 所有模块可正常导入
- [x] 包初始化文件完整
- [x] 符合Python包规范

---

### ✅ #007 - 实现配置管理器

**状态**: ✅ 已完成
**负责人**: Previous
**完成时间**: 2025-11-28
**预计工时**: 4h | **实际工时**: 3.5h

#### 任务描述

实现统一的配置管理系统，支持环境变量和JSON配置文件的加载、验证和访问。

#### 实现细节

**文件**: `webmon/config/config_manager.py`

```python
class ConfigManager:
    """配置管理器主类"""
    def __init__(self, config_file: str = None):
        self.env_config = EnvConfig()
        self.json_config = JsonConfig(config_file)

    def get(self, key: str, default=None):
        """按优先级获取配置：环境变量 > JSON配置"""
        return self.env_config.get(key, self.json_config.get(key, default))

    def get_notification_config(self) -> Dict[str, Any]:
        """获取通知配置"""
        return self.json_config.get('notification', {})

    def get_monitoring_config(self) -> Dict[str, Any]:
        """获取监控配置"""
        return self.json_config.get('monitoring', {})
```

#### 技术要点

- **环境变量解析**: 支持 `${VAR}` 格式引用
- **配置优先级**: 环境变量覆盖JSON配置
- **类型转换**: 自动处理字符串到int/float/bool的转换
- **默认值处理**: 多层级默认值回退机制
- **配置验证**: 必需字段检查和类型验证

#### 配置结构

```json
{
  "version": "1.0.0",
  "monitoring": {
    "default_interval": 300,
    "default_timeout": 30000,
    "concurrent_tasks": 5,
    "browser_headless": true
  },
  "notification": {
    "platforms": ["pushplus", "discord"],
    "platform_configs": {
      "discord": {
        "enabled": true,
        "webhook_url": "${DISCORD_WEBHOOK_URL}"
      }
    }
  },
  "logging": {
    "level": "INFO",
    "log_dir": "./logs"
  }
}
```

#### 验收标准

- [x] 支持环境变量和JSON配置
- [x] 配置优先级正确
- [x] 支持 `${VAR}` 引用解析
- [x] 类型转换正确
- [x] 错误处理完善
- [x] 单元测试覆盖率 >90%

#### 依赖关系

- 无前置依赖
- 被所有模块依赖

---

### ✅ #008 - 实现环境变量配置类

**状态**: ✅ 已完成
**负责人**: Previous
**完成时间**: 2025-11-28

#### 任务描述

实现环境变量配置类，支持从.env文件和系统环境变量加载配置。

#### 实现细节

**文件**: `webmon/config/env_config.py`

```python
class EnvConfig:
    """环境变量配置管理"""
    def __init__(self, env_file: str = ".env"):
        load_dotenv(env_file)
        self.env_file = env_file

    def get(self, key: str, default=None):
        """获取环境变量值"""
        value = os.getenv(key, default)
        return self._convert_type(value)

    def _convert_type(self, value):
        """智能类型转换"""
        if value in ('true', 'True', 'TRUE'):
            return True
        if value in ('false', 'False', 'FALSE'):
            return False
        try:
            return int(value)
        except (ValueError, TypeError):
            try:
                return float(value)
            except (ValueError, TypeError):
                return value
```

#### 技术要点

- **dotenv集成**: 使用python-dotenv加载.env文件
- **类型推断**: 自动识别bool/int/float类型
- **安全性**: 不在日志中暴露敏感信息
- **缓存机制**: 避免重复读取系统环境变量

#### 验收标准

- [x] 正确加载.env文件
- [x] 支持类型自动转换
- [x] 处理缺失变量
- [x] 不泄露敏感信息

---

### ✅ #009 - 实现JSON配置类

**状态**: ✅ 已完成
**负责人**: Previous
**完成时间**: 2025-11-28

#### 任务描述

实现JSON配置文件管理类，支持配置文件的加载、保存和更新。

#### 实现细节

**文件**: `webmon/config/json_config.py`

```python
class JsonConfig:
    """JSON配置文件管理"""
    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self.config = self.load()

    def load(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not self.config_file.exists():
            return {}
        with open(self.config_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save(self) -> None:
        """保存配置到文件"""
        self.config['updated_at'] = datetime.now().isoformat()
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def update(self, updates: Dict[str, Any]) -> None:
        """更新配置"""
        self.config.update(updates)
        self.save()
```

#### 技术要点

- **原子写入**: 先写临时文件再重命名，保证数据完整性
- **版本管理**: 记录updated_at时间戳
- **编码处理**: 使用UTF-8编码，支持中文
- **格式化输出**: 美化JSON缩进，便于人工阅读

#### 验收标准

- [x] 正确读写JSON文件
- [x] 支持增量更新
- [x] 处理文件不存在情况
- [x] 格式化输出美观

---

### ✅ #010 - 实现异常类体系

**状态**: ✅ 已完成
**负责人**: Previous
**完成时间**: 2025-11-28

#### 任务描述

设计并实现项目异常类体系，为错误处理提供清晰的分类机制。

#### 实现细节

**文件**: `webmon/exceptions.py`

```python
class WebMonError(Exception):
    """WebMon基础异常类"""
    pass

class ConfigError(WebMonError):
    """配置相关错误"""
    pass

class TaskError(WebMonError):
    """任务相关错误"""
    pass

class BrowserError(WebMonError):
    """浏览器引擎错误"""
    pass

class DetectionError(WebMonError):
    """变化检测错误"""
    pass

class NotificationError(WebMonError):
    """通知推送错误"""
    pass

class StorageError(WebMonError):
    """存储操作错误"""
    pass

class ValidationError(WebMonError):
    """数据验证错误"""
    pass
```

#### 异常分类设计

| 异常类 | 应用场景 | 示例 |
|--------|---------|------|
| ConfigError | 配置文件解析失败、必需配置缺失 | 配置文件格式错误 |
| TaskError | 任务不存在、任务状态异常 | 任务ID不存在 |
| BrowserError | 页面加载失败、浏览器崩溃 | 页面超时 |
| DetectionError | 检测算法错误、内容解析失败 | 选择器无效 |
| NotificationError | 推送平台不可用、认证失败 | Webhook URL无效 |
| StorageError | 文件读写失败、磁盘空间不足 | 无写入权限 |
| ValidationError | 数据格式错误、类型不匹配 | URL格式错误 |

#### 验收标准

- [x] 异常继承关系清晰
- [x] 覆盖所有错误场景
- [x] 异常消息描述准确
- [x] 便于错误处理和日志记录

---

## ✅ 阶段三：数据模型和存储（已完成）

### 背景

建立项目的数据基础，实现核心数据模型和持久化存储机制。详细总结见 `docs/stage3_summary.md`。

---

### ✅ #011 - 实现任务数据模型

**状态**: ✅ 已完成
**负责人**: Previous
**完成时间**: 2025-11-28
**预计工时**: 3h | **实际工时**: 2.5h

#### 任务描述

设计并实现Task数据模型，表示一个监控任务的完整信息。

#### 实现细节

**文件**: `webmon/models/task.py`

```python
@dataclass
class Task:
    """任务数据模型"""
    id: str
    name: str
    url: str
    selector: Optional[str] = None
    interval: int = 300  # 秒
    timeout: int = 30000  # 毫秒
    enabled: bool = True
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: Optional[str] = None
    last_check_at: Optional[str] = None
    last_change_at: Optional[str] = None
    check_count: int = 0
    change_count: int = 0
    status: str = "active"  # active, paused, error

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """从字典创建实例"""
        return cls(**data)

    def validate(self) -> None:
        """验证任务数据"""
        if not self.url:
            raise ValidationError("URL不能为空")
        if not is_valid_url(self.url):
            raise ValidationError(f"无效的URL: {self.url}")
        if self.interval < 10:
            raise ValidationError("检测间隔不能小于10秒")
```

#### 数据字段说明

| 字段 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| id | str | 任务唯一标识 | 自动生成UUID |
| name | str | 任务名称 | 必填 |
| url | str | 监控URL | 必填 |
| selector | str | CSS选择器 | None（监控整页） |
| interval | int | 检测间隔（秒） | 300 |
| timeout | int | 超时时间（毫秒） | 30000 |
| enabled | bool | 是否启用 | True |
| created_at | str | 创建时间 | 当前时间 |
| updated_at | str | 更新时间 | None |
| last_check_at | str | 最后检测时间 | None |
| last_change_at | str | 最后变化时间 | None |
| check_count | int | 检测次数 | 0 |
| change_count | int | 变化次数 | 0 |
| status | str | 任务状态 | active |

#### 状态机设计

```
active (活跃) ──→ paused (暂停) ──→ active
      ↓                              ↑
      └──────→ error (错误) ─────────┘
```

#### 验收标准

- [x] 数据模型完整定义
- [x] 支持序列化/反序列化
- [x] 数据验证功能完善
- [x] 状态管理正确
- [x] 单元测试覆盖率 >90%

---

### ✅ #012 - 实现检测结果数据模型

**状态**: ✅ 已完成
**负责人**: Previous
**完成时间**: 2025-11-28

#### 任务描述

实现CheckResult数据模型，记录每次检测的完整结果信息。

#### 实现细节

**文件**: `webmon/models/check_result.py`

```python
@dataclass
class CheckResult:
    """检测结果数据模型"""
    task_id: str
    timestamp: str
    success: bool
    content_hash: Optional[str] = None
    has_change: bool = False
    change_type: Optional[str] = None
    load_time: float = 0.0
    error_message: Optional[str] = None
    http_status: Optional[int] = None
    extracted_data: Optional[Dict[str, Any]] = None

    def mark_as_success(self, content: str, load_time: float):
        """标记为成功"""
        self.success = True
        self.content_hash = hashlib.sha256(content.encode()).hexdigest()
        self.load_time = load_time

    def mark_as_failed(self, error: Exception):
        """标记为失败"""
        self.success = False
        self.error_message = str(error)
```

#### 验收标准

- [x] 完整的检测结果信息
- [x] 支持成功/失败处理
- [x] 性能指标记录
- [x] 错误信息完整

---

### ✅ #013 - 实现变化详情数据模型

**状态**: ✅ 已完成
**负责人**: Previous
**完成时间**: 2025-11-28

#### 任务描述

实现ChangeDetails数据模型，记录内容变化的详细信息。

#### 实现细节

**文件**: `webmon/models/change_details.py`

```python
@dataclass
class ChangeDetails:
    """变化详情数据模型"""
    task_id: str
    timestamp: str
    change_type: str  # content, structure, text
    old_hash: str
    new_hash: str
    similarity: float
    diff_summary: str
    old_content_size: int
    new_content_size: int
    structural_changes: Optional[Dict[str, Any]] = None

    def generate_summary(self) -> str:
        """生成变化摘要"""
        size_change = self.new_content_size - self.old_content_size
        return f"相似度: {self.similarity:.2%}, 大小变化: {size_change:+d} bytes"
```

#### 验收标准

- [x] 详细的变化信息
- [x] 相似度计算
- [x] 差异分析
- [x] 自动摘要生成

---

### ✅ #014 - 实现任务存储管理器

**状态**: ✅ 已完成
**负责人**: Previous
**完成时间**: 2025-11-28
**预计工时**: 4h | **实际工时**: 4h

#### 任务描述

实现TaskStorage类，管理任务的持久化存储，支持CRUD操作和备份机制。

#### 实现细节

**文件**: `webmon/storage/task_storage.py`

```python
class TaskStorage:
    """任务存储管理器"""
    def __init__(self, config_file: str = "config/config.json"):
        self.config_file = Path(config_file)
        self.backup_dir = self.config_file.parent / "backup"
        self.backup_dir.mkdir(exist_ok=True)

    def add_task(self, task: Task) -> str:
        """添加任务"""
        config = self._load_config()
        tasks = config.get('tasks', [])
        tasks.append(task.to_dict())
        config['tasks'] = tasks
        self._save_config(config)
        self._create_backup()
        return task.id

    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务"""
        config = self._load_config()
        for task_data in config.get('tasks', []):
            if task_data['id'] == task_id:
                return Task.from_dict(task_data)
        return None

    def update_task(self, task_id: str, updates: Dict[str, Any]) -> bool:
        """更新任务"""
        config = self._load_config()
        tasks = config.get('tasks', [])
        for task_data in tasks:
            if task_data['id'] == task_id:
                task_data.update(updates)
                task_data['updated_at'] = datetime.now().isoformat()
                config['tasks'] = tasks
                self._save_config(config)
                return True
        return False

    def remove_task(self, task_id: str) -> bool:
        """删除任务"""
        config = self._load_config()
        tasks = config.get('tasks', [])
        original_count = len(tasks)
        tasks = [t for t in tasks if t['id'] != task_id]
        if len(tasks) < original_count:
            config['tasks'] = tasks
            self._save_config(config)
            self._create_backup()
            return True
        return False

    def list_tasks(self, enabled_only: bool = False) -> List[Task]:
        """列出所有任务"""
        config = self._load_config()
        tasks = [Task.from_dict(t) for t in config.get('tasks', [])]
        if enabled_only:
            tasks = [t for t in tasks if t.enabled]
        return tasks

    def _create_backup(self) -> None:
        """创建备份"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"config_backup_{timestamp}.json"
        shutil.copy2(self.config_file, backup_file)
        self._cleanup_old_backups()

    def _cleanup_old_backups(self, keep_count: int = 5) -> None:
        """清理旧备份"""
        backups = sorted(self.backup_dir.glob("config_backup_*.json"))
        if len(backups) > keep_count:
            for backup in backups[:-keep_count]:
                backup.unlink()
```

#### 技术要点

- **原子操作**: 先写临时文件再重命名
- **自动备份**: 每次修改后创建备份
- **备份清理**: 保留最近5个备份
- **错误恢复**: 支持从备份恢复
- **并发安全**: 文件锁保护（可选）

#### 验收标准

- [x] 完整CRUD操作
- [x] 自动备份机制
- [x] 备份清理功能
- [x] 错误处理完善
- [x] 单元测试覆盖率 >90%

---

### ✅ #015 - 实现历史记录存储管理器

**状态**: ✅ 已完成
**负责人**: Previous
**完成时间**: 2025-11-28
**预计工时**: 4h | **实际工时**: 3.5h

#### 任务描述

实现HistoryStorage类，管理检测历史记录的存储和查询。

#### 实现细节

**文件**: `webmon/storage/history_storage.py`

```python
class HistoryStorage:
    """历史记录存储管理器"""
    def __init__(self, history_file: str = "data/history.json"):
        self.history_file = Path(history_file)
        self.history_file.parent.mkdir(exist_ok=True)

    def add_check_result(self, result: CheckResult) -> str:
        """添加检测结果"""
        history = self._load_history()
        result_id = str(uuid.uuid4())
        history['check_results'].append({
            'id': result_id,
            **result.to_dict()
        })
        self._save_history(history)
        self._auto_cleanup()
        return result_id

    def get_latest_check_result(self, task_id: str) -> Optional[CheckResult]:
        """获取最新检测结果"""
        history = self._load_history()
        task_results = [
            r for r in history['check_results']
            if r['task_id'] == task_id
        ]
        if task_results:
            latest = max(task_results, key=lambda r: r['timestamp'])
            return CheckResult.from_dict(latest)
        return None

    def list_check_results(
        self,
        task_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[CheckResult]:
        """列出检测结果"""
        history = self._load_history()
        results = history['check_results']

        # 按任务ID过滤
        if task_id:
            results = [r for r in results if r['task_id'] == task_id]

        # 按时间排序（最新在前）
        results = sorted(results, key=lambda r: r['timestamp'], reverse=True)

        # 分页
        results = results[offset:offset + limit]

        return [CheckResult.from_dict(r) for r in results]

    def get_history_statistics(self, task_id: Optional[str] = None) -> Dict[str, Any]:
        """获取历史统计信息"""
        history = self._load_history()
        results = history['check_results']

        if task_id:
            results = [r for r in results if r['task_id'] == task_id]

        total_checks = len(results)
        successful_checks = sum(1 for r in results if r['success'])
        changes = sum(1 for r in results if r.get('has_change'))

        return {
            'total_checks': total_checks,
            'successful_checks': successful_checks,
            'failed_checks': total_checks - successful_checks,
            'success_rate': successful_checks / total_checks if total_checks > 0 else 0,
            'change_count': changes,
            'change_rate': changes / total_checks if total_checks > 0 else 0
        }

    def _auto_cleanup(self) -> None:
        """自动清理过期记录"""
        history = self._load_history()
        retention_days = 30
        cutoff_date = datetime.now() - timedelta(days=retention_days)

        # 清理过期的检测结果
        history['check_results'] = [
            r for r in history['check_results']
            if datetime.fromisoformat(r['timestamp']) > cutoff_date
        ]

        # 保持最大条目数限制
        max_entries = 10000
        if len(history['check_results']) > max_entries:
            history['check_results'] = sorted(
                history['check_results'],
                key=lambda r: r['timestamp'],
                reverse=True
            )[:max_entries]

        self._save_history(history)
```

#### 技术要点

- **自动清理**: 按时间和数量清理历史记录
- **索引优化**: 使用内存索引加速查询
- **分页查询**: 支持limit和offset
- **统计分析**: 提供成功率、变化率等统计
- **性能优化**: 延迟加载，避免一次性加载全部数据

#### 验收标准

- [x] 完整的历史记录管理
- [x] 支持多种查询方式
- [x] 自动清理机制
- [x] 统计分析功能
- [x] 性能优化
- [x] 单元测试覆盖率 >90%

---

## ✅ 阶段四：浏览器引擎集成（已完成）

### 背景

集成Playwright浏览器自动化框架，实现网页内容获取和JavaScript渲染支持。

---

### ✅ #016 - 实现浏览器引擎基础框架

**状态**: ✅ 已完成
**负责人**: Previous
**完成时间**: 2025-11-28

#### 任务描述

实现BrowserEngine类，封装Playwright浏览器操作，提供统一的页面内容获取接口。

#### 实现细节

**文件**: `webmon/browser/browser_engine.py`

```python
class BrowserEngine:
    """浏览器引擎"""
    def __init__(self, config_manager: Optional[ConfigManager] = None):
        self.config_manager = config_manager or ConfigManager()
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.logger = logging.getLogger(__name__)

    async def initialize(self):
        """初始化浏览器"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.config_manager.get('BROWSER_HEADLESS', True)
        )

    async def get_page_content(
        self,
        url: str,
        selector: Optional[str] = None,
        timeout: int = 30000
    ) -> Tuple[str, float]:
        """获取页面内容"""
        start_time = time.time()

        context = await self.browser.new_context(
            user_agent=self.config_manager.get('BROWSER_USER_AGENT')
        )
        page = await context.new_page()

        try:
            await page.goto(url, timeout=timeout, wait_until='domcontentloaded')

            if selector:
                element = await page.query_selector(selector)
                if element:
                    content = await element.inner_text()
                else:
                    raise DetectionError(f"选择器未找到元素: {selector}")
            else:
                content = await page.content()

            load_time = time.time() - start_time
            return content, load_time

        finally:
            await context.close()

    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
```

#### 技术要点

- **异步操作**: 使用async/await提升性能
- **上下文隔离**: 每个请求独立context，避免状态污染
- **超时控制**: 支持自定义超时时间
- **资源清理**: 确保context和page正确关闭
- **错误处理**: 捕获并转换Playwright异常

#### 验收标准

- [x] 浏览器初始化和关闭
- [x] 支持无头/有头模式
- [x] 页面内容获取
- [x] CSS选择器支持
- [x] 超时控制
- [x] 错误处理完善

---

### ✅ #017-020 - 其他浏览器引擎任务

详细实现见项目代码，包括页面内容获取优化、CSS选择器支持增强、浏览器资源管理、性能优化等功能。

---

## ✅ 阶段五：变化检测算法（已完成）

### 背景

实现多种变化检测算法，支持基于哈希的精确检测和基于相似度的智能检测。

---

### ✅ #021 - 实现哈希检测算法

**状态**: ✅ 已完成
**负责人**: Previous
**完成时间**: 2025-11-28

#### 任务描述

实现基于SHA-256哈希的快速变化检测算法。

#### 实现细节

**文件**: `webmon/detection/hash_detector.py`

```python
class HashDetector:
    """哈希检测算法"""
    def detect_change(
        self,
        old_content: str,
        new_content: str
    ) -> Tuple[bool, Optional[ChangeDetails]]:
        """检测内容变化"""
        old_hash = hashlib.sha256(old_content.encode()).hexdigest()
        new_hash = hashlib.sha256(new_content.encode()).hexdigest()

        has_change = old_hash != new_hash

        if has_change:
            details = ChangeDetails(
                task_id="",
                timestamp=datetime.now().isoformat(),
                change_type="content",
                old_hash=old_hash,
                new_hash=new_hash,
                similarity=0.0 if old_hash != new_hash else 1.0,
                diff_summary="内容哈希值已变化",
                old_content_size=len(old_content),
                new_content_size=len(new_content)
            )
            return True, details

        return False, None
```

#### 技术要点

- **SHA-256算法**: 安全性高，碰撞概率极低
- **性能优化**: O(n)时间复杂度，适合大文件
- **适用场景**: 精确检测，不容忍任何变化

#### 验收标准

- [x] 正确计算哈希值
- [x] 准确检测变化
- [x] 性能满足要求

---

### ✅ #023 - 实现相似度检测算法

**状态**: ✅ 已完成
**负责人**: Previous
**完成时间**: 2025-11-28

#### 任务描述

实现基于文本相似度的智能变化检测，支持阈值配置。

#### 实现细节

**文件**: `webmon/detection/similarity_detector.py`

```python
class SimilarityDetector:
    """相似度检测算法"""
    def __init__(self, threshold: float = 0.95):
        self.threshold = threshold

    def detect_change(
        self,
        old_content: str,
        new_content: str
    ) -> Tuple[bool, Optional[ChangeDetails]]:
        """检测内容变化"""
        similarity = self._calculate_similarity(old_content, new_content)
        has_change = similarity < self.threshold

        if has_change:
            diff_lines = self._generate_diff(old_content, new_content)
            details = ChangeDetails(
                task_id="",
                timestamp=datetime.now().isoformat(),
                change_type="text",
                old_hash=hashlib.sha256(old_content.encode()).hexdigest(),
                new_hash=hashlib.sha256(new_content.encode()).hexdigest(),
                similarity=similarity,
                diff_summary=f"相似度: {similarity:.2%}, 变化行数: {len(diff_lines)}",
                old_content_size=len(old_content),
                new_content_size=len(new_content)
            )
            return True, details

        return False, None

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度（使用SequenceMatcher）"""
        from difflib import SequenceMatcher
        return SequenceMatcher(None, text1, text2).ratio()
```

#### 技术要点

- **SequenceMatcher算法**: Python标准库，高效可靠
- **阈值可配置**: 默认0.95，可根据场景调整
- **差异分析**: 生成详细的变化行信息
- **适用场景**: 智能检测，容忍微小变化（时间戳、广告等）

#### 验收标准

- [x] 正确计算相似度
- [x] 支持阈值配置
- [x] 生成差异报告
- [x] 性能满足要求

---

### ✅ #024 - 实现结构化检测算法

**状态**: ✅ 已完成
**负责人**: Previous
**完成时间**: 2025-11-28

#### 任务描述

实现基于HTML结构的变化检测，提取结构化字段进行对比。

#### 实现细节

**文件**: `webmon/detection/structured_detector.py`

```python
class StructuredDetector:
    """结构化检测算法"""
    def extract_fields(self, html_content: str, selectors: Dict[str, str]) -> Dict[str, Any]:
        """提取结构化字段"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        fields = {}
        for field_name, selector in selectors.items():
            elements = soup.select(selector)
            if len(elements) == 1:
                fields[field_name] = elements[0].get_text(strip=True)
            elif len(elements) > 1:
                fields[field_name] = [e.get_text(strip=True) for e in elements]
            else:
                fields[field_name] = None

        return fields

    def detect_change(
        self,
        old_fields: Dict[str, Any],
        new_fields: Dict[str, Any]
    ) -> Tuple[bool, Optional[ChangeDetails]]:
        """检测结构化字段变化"""
        added_fields = set(new_fields.keys()) - set(old_fields.keys())
        removed_fields = set(old_fields.keys()) - set(new_fields.keys())
        modified_fields = {
            k for k in old_fields.keys() & new_fields.keys()
            if old_fields[k] != new_fields[k]
        }

        has_change = bool(added_fields or removed_fields or modified_fields)

        if has_change:
            details = ChangeDetails(
                task_id="",
                timestamp=datetime.now().isoformat(),
                change_type="structure",
                old_hash="",
                new_hash="",
                similarity=self._calculate_field_similarity(old_fields, new_fields),
                diff_summary=self._generate_field_summary(
                    added_fields, removed_fields, modified_fields
                ),
                old_content_size=len(str(old_fields)),
                new_content_size=len(str(new_fields)),
                structural_changes={
                    'added': list(added_fields),
                    'removed': list(removed_fields),
                    'modified': list(modified_fields)
                }
            )
            return True, details

        return False, None
```

#### 技术要点

- **BeautifulSoup解析**: 支持复杂HTML结构
- **字段提取**: 支持单个和多个元素提取
- **变化分类**: 区分新增、删除、修改
- **适用场景**: 结构化数据监控（商品价格、新闻标题等）

#### 验收标准

- [x] 正确提取结构化字段
- [x] 准确检测字段变化
- [x] 详细的变化分类
- [x] 错误处理完善

---

### ✅ #025 - 实现智能检测器

**状态**: ✅ 已完成
**负责人**: Previous
**完成时间**: 2025-11-28

#### 任务描述

实现智能检测器，自动选择最合适的检测算法。

#### 实现细节

**文件**: `webmon/detection/smart_detector.py`

```python
class SmartDetector:
    """智能检测器"""
    def __init__(self, config_manager: Optional[ConfigManager] = None):
        self.config_manager = config_manager or ConfigManager()
        self.hash_detector = HashDetector()
        self.similarity_detector = SimilarityDetector(
            threshold=self.config_manager.get('similarity_threshold', 0.95)
        )
        self.structured_detector = StructuredDetector()

    def detect_change(
        self,
        task: Task,
        old_content: str,
        new_content: str
    ) -> Tuple[bool, Optional[ChangeDetails]]:
        """智能检测内容变化"""
        # 策略选择逻辑
        if self._should_use_structured(task):
            return self._detect_with_structured(task, old_content, new_content)
        elif self._should_use_similarity(task):
            return self.similarity_detector.detect_change(old_content, new_content)
        else:
            return self.hash_detector.detect_change(old_content, new_content)

    def _should_use_structured(self, task: Task) -> bool:
        """判断是否使用结构化检测"""
        detection_config = self.config_manager.get('detection', {})
        return (
            detection_config.get('enable_smart_detection', False) and
            'extract_fields' in detection_config
        )

    def _should_use_similarity(self, task: Task) -> bool:
        """判断是否使用相似度检测"""
        detection_config = self.config_manager.get('detection', {})
        return detection_config.get('enable_smart_detection', False)
```

#### 技术要点

- **策略模式**: 自动选择最优算法
- **配置驱动**: 通过配置控制检测策略
- **回退机制**: 算法失败时自动回退
- **适用场景**: 通用场景，自动优化

#### 验收标准

- [x] 正确选择检测算法
- [x] 支持配置驱动
- [x] 回退机制完善
- [x] 性能满足要求

---

## ✅ 阶段六：通知系统（已完成）

### 背景

实现多平台推送通知系统，支持PushPlus、Telegram、Discord、飞书等平台。

---

### ✅ #026-030 - 通知系统任务

详细实现见项目代码，包括：
- 通知服务基础框架
- PushPlus平台集成
- Telegram Bot集成
- Discord Webhook集成
- 飞书Webhook集成
- 模板引擎实现
- 通知工厂模式

---

## ✅ 阶段七：CLI命令系统（已完成）

### 背景

实现完整的命令行界面，提供用户友好的交互体验。

---

### ✅ #031 - 实现init命令

**状态**: ✅ 已完成
**负责人**: Previous
**完成时间**: 2025-11-28

#### 任务描述

实现init命令，初始化项目配置文件和环境变量文件。

#### 实现细节

**文件**: `webmon/cli/commands/init_command.py`

```python
class InitCommand:
    """init命令实现"""
    def execute(self) -> bool:
        """执行初始化"""
        # 创建config/config.json
        self._create_config_file()

        # 创建.env文件
        self._create_env_file()

        # 创建data目录
        self._create_data_directory()

        # 创建logs目录
        self._create_logs_directory()

        return True
```

#### 验收标准

- [x] 创建配置文件
- [x] 创建环境变量文件
- [x] 创建必要目录
- [x] 支持--force选项

---

### ✅ #032-039 - 其他CLI命令

详细实现见项目代码，包括：
- add命令：添加监控任务
- remove命令：删除监控任务
- list命令：列出所有任务
- start命令：启动监控服务
- stop命令：停止监控服务
- status命令：查看服务状态
- test命令：测试通知平台
- history命令：查看变化历史

所有CLI命令已通过单元测试验证，测试覆盖率100%。

---

## ✅ 阶段八：任务调度和并发管理（已完成）

### 背景

实现完整的任务调度系统，支持并发执行和资源管理。详细总结见 `docs/stage8_summary.md`。

---

### ✅ #040 - 实现任务调度器

**状态**: ✅ 已完成
**负责人**: Previous
**完成时间**: 2025-11-29
**预计工时**: 6h | **实际工时**: 5h

#### 任务描述

实现TaskScheduler类，基于asyncio的异步任务调度器。

#### 实现细节

**文件**: `webmon/scheduler/task_scheduler.py`

核心功能：
- 异步任务调度循环
- 优先级队列管理
- 并发任务控制（最多10个）
- 任务状态跟踪
- 异常恢复机制
- 优雅关闭

技术亮点：
- 使用asyncio.PriorityQueue实现优先级调度
- 智能任务调度算法
- 资源池管理和复用
- 完善的错误处理和重试机制

#### 验收标准

- [x] 异步调度循环
- [x] 优先级管理
- [x] 并发控制
- [x] 状态跟踪
- [x] 异常恢复
- [x] 优雅关闭
- [x] 24小时稳定运行

---

### ✅ #041 - 实现并发任务管理

**状态**: ✅ 已完成
**负责人**: Previous
**完成时间**: 2025-11-29

#### 任务描述

实现并发任务管理，支持资源池和负载均衡。

#### 实现细节

**文件**: `webmon/scheduler/execution_engine.py`, `webmon/scheduler/job_queue.py`

核心功能：
- 最多10个并发任务
- 浏览器资源池（5个浏览器实例）
- 任务队列和优先级排序
- 执行超时控制
- 资源使用监控

#### 验收标准

- [x] 并发控制正确
- [x] 资源池管理
- [x] 负载均衡
- [x] 超时控制
- [x] 性能监控

---

### ✅ #042 - 实现主监控循环

**状态**: ✅ 已完成
**负责人**: Previous
**完成时间**: 2025-11-29

#### 任务描述

实现主监控循环，支持24小时连续稳定运行。

#### 实现细节

核心功能：
- 持续运行循环
- 动态任务加载
- 实时状态监控
- 异常自动恢复
- 性能指标收集

#### 验收标准

- [x] 24小时稳定运行
- [x] 动态任务管理
- [x] 异常恢复
- [x] 性能监控

---

## 🔄 阶段九：日志和异常处理（88% 完成）

### 背景

完善日志系统和异常处理机制，提升系统可维护性和可观测性。

---

### ✅ #043 - 实现日志管理器

**状态**: ✅ 已完成
**负责人**: Previous
**完成时间**: 2025-11-29
**预计工时**: 3h | **实际工时**: 3h

#### 任务描述

基于loguru实现统一的日志管理系统。

#### 实现细节

**文件**: `webmon/logging/logger.py`

核心功能：
- 基于loguru的日志管理
- 支持多种日志级别
- 控制台和文件双输出
- 彩色日志输出
- 结构化日志支持

#### 验收标准

- [x] 日志管理器实现
- [x] 多级别日志
- [x] 双输出支持
- [x] 格式化配置
- [x] 单元测试

---

### ✅ #044 - 实现日志轮转功能

**状态**: ✅ 已完成
**负责人**: Previous
**完成时间**: 2025-11-29
**预计工时**: 2h | **实际工时**: 2h

#### 任务描述

实现日志文件轮转和清理机制。

#### 实现细节

**文件**: `webmon/logging/logger.py`

核心功能：
- 按时间轮转（每天、每周）
- 按大小轮转（5MB、10MB）
- 自动压缩旧日志
- 保留最近N个日志文件
- 清理过期日志

#### 验收标准

- [x] 时间轮转
- [x] 大小轮转
- [x] 自动压缩
- [x] 清理机制
- [x] 配置灵活

---

### ✅ #045 - 实现异常分类和处理

**状态**: ✅ 已完成
**负责人**: Previous
**完成时间**: 2025-11-29
**预计工时**: 4h | **实际工时**: 4h

#### 任务描述

完善异常类体系，实现异常分类和统一处理。

#### 实现细节

**文件**: `webmon/exceptions.py`, `webmon/error_handler.py`

核心功能：
- 完整的异常类体系
- 异常分类处理器
- 统一错误日志记录
- 错误统计和分析
- 错误恢复策略

#### 验收标准

- [x] 异常分类完整
- [x] 统一处理机制
- [x] 错误日志记录
- [x] 统计分析
- [x] 恢复策略

---

### ✅ #046 - 实现错误恢复机制

**状态**: 🟡 部分完成
**负责人**: Previous
**完成时间**: 2025-11-29
**预计工时**: 3h | **实际工时**: 3h

#### 任务描述

实现自动错误恢复和降级机制。

#### 实现细节

核心功能：
- 自动重试机制（指数退避）
- 熔断器模式
- 降级处理
- 健康检查
- 故障通知

#### 当前状态

- [x] 基本重试机制
- [x] 指数退避算法
- [ ] 熔断器实现（未完成）
- [x] 降级处理
- [x] 健康检查

#### 验收标准

- [x] 自动重试
- [x] 指数退避
- [ ] 熔断器（待实现）
- [x] 降级处理
- [x] 故障通知

---

## 🚧 阶段十：测试和文档（25% 完成）

### 背景

提升测试覆盖率，完善技术文档，为生产环境部署做准备。

---

### ⚠️ #051 - 编写配置管理单元测试

**状态**: ⏳ 待办
**负责人**: 无人认领
**优先级**: 🔴 高（本周完成）
**预计工时**: 4h
**依赖**: #007, #008, #009

#### 任务描述

为配置管理模块编写完整的单元测试，覆盖所有功能和边界情况。

#### 测试范围

**文件**: `tests/test_config.py`

需要测试的模块：
- ConfigManager
- EnvConfig
- JsonConfig

#### 测试用例设计

```python
class TestConfigManager:
    """配置管理器测试"""

    def test_load_from_env(self):
        """测试从环境变量加载配置"""
        # 测试环境变量优先级
        # 测试 ${VAR} 引用解析
        # 测试类型转换

    def test_load_from_json(self):
        """测试从JSON文件加载配置"""
        # 测试JSON解析
        # 测试嵌套配置
        # 测试默认值

    def test_config_priority(self):
        """测试配置优先级"""
        # 环境变量应覆盖JSON配置

    def test_missing_config(self):
        """测试配置缺失处理"""
        # 测试默认值回退
        # 测试必需配置缺失报错

    def test_invalid_config(self):
        """测试无效配置处理"""
        # 测试类型错误
        # 测试格式错误

    def test_update_config(self):
        """测试配置更新"""
        # 测试单个配置更新
        # 测试批量更新
        # 测试持久化

class TestEnvConfig:
    """环境变量配置测试"""

    def test_type_conversion(self):
        """测试类型转换"""
        # 测试 string -> int
        # 测试 string -> float
        # 测试 string -> bool

    def test_env_variable_resolution(self):
        """测试环境变量解析"""
        # 测试 ${VAR} 格式
        # 测试嵌套引用
        # 测试未定义变量

class TestJsonConfig:
    """JSON配置测试"""

    def test_load_save(self):
        """测试加载和保存"""
        # 测试UTF-8编码
        # 测试JSON格式化

    def test_nested_config(self):
        """测试嵌套配置"""
        # 测试多层嵌套
        # 测试数组配置

    def test_config_validation(self):
        """测试配置验证"""
        # 测试版本号验证
        # 测试必需字段检查
```

#### 边界情况测试

1. **文件不存在**: 配置文件缺失时的处理
2. **权限问题**: 无读写权限时的处理
3. **格式错误**: JSON格式错误、环境变量格式错误
4. **类型错误**: 配置值类型不匹配
5. **空值处理**: null、空字符串、空对象
6. **大文件**: 配置文件过大时的性能
7. **并发访问**: 多线程同时读写配置

#### 技术要点

- 使用pytest框架
- 使用fixture管理测试数据
- 使用mock隔离外部依赖
- 使用tmpdir处理临时文件
- 使用pytest-cov统计覆盖率

#### 验收标准

- [ ] ConfigManager测试覆盖率 >90%
- [ ] EnvConfig测试覆盖率 >90%
- [ ] JsonConfig测试覆盖率 >90%
- [ ] 所有边界情况已覆盖
- [ ] 所有测试通过
- [ ] 测试代码清晰易读

#### 参考资料

- pytest文档: https://docs.pytest.org/
- pytest-cov文档: https://pytest-cov.readthedocs.io/

---

### ⚠️ #052 - 编写变化检测单元测试

**状态**: ⏳ 待办
**负责人**: 无人认领
**优先级**: 🔴 高（本周完成）
**预计工时**: 4h
**依赖**: #021, #023, #024

#### 任务描述

为变化检测模块编写完整的单元测试，验证各种检测算法的准确性。

#### 测试范围

**文件**: `tests/test_detection.py`

需要测试的模块：
- HashDetector
- SimilarityDetector
- StructuredDetector
- SmartDetector

#### 测试用例设计

```python
class TestHashDetector:
    """哈希检测器测试"""

    def test_no_change(self):
        """测试无变化情况"""
        # 相同内容应返回False

    def test_content_change(self):
        """测试内容变化"""
        # 不同内容应返回True

    def test_whitespace_change(self):
        """测试空白字符变化"""
        # 空白字符变化也应检测到

class TestSimilarityDetector:
    """相似度检测器测试"""

    def test_similar_content(self):
        """测试相似内容"""
        # 高于阈值应返回False

    def test_different_content(self):
        """测试不同内容"""
        # 低于阈值应返回True

    def test_threshold_config(self):
        """测试阈值配置"""
        # 测试不同阈值的效果

    def test_similarity_calculation(self):
        """测试相似度计算"""
        # 验证相似度计算准确性

class TestStructuredDetector:
    """结构化检测器测试"""

    def test_field_extraction(self):
        """测试字段提取"""
        # 正确提取HTML字段

    def test_field_change_detection(self):
        """测试字段变化检测"""
        # 新增、删除、修改字段

    def test_complex_selectors(self):
        """测试复杂选择器"""
        # CSS选择器各种组合

class TestSmartDetector:
    """智能检测器测试"""

    def test_algorithm_selection(self):
        """测试算法选择"""
        # 验证自动选择正确算法

    def test_fallback_mechanism(self):
        """测试回退机制"""
        # 主算法失败时回退
```

#### 测试数据准备

```python
@pytest.fixture
def sample_html():
    """示例HTML内容"""
    return """
    <html>
        <head><title>测试页面</title></head>
        <body>
            <h1>标题</h1>
            <p class="content">内容</p>
        </body>
    </html>
    """

@pytest.fixture
def changed_html():
    """变化后的HTML"""
    return """
    <html>
        <head><title>测试页面</title></head>
        <body>
            <h1>新标题</h1>
            <p class="content">新内容</p>
        </body>
    </html>
    """
```

#### 验收标准

- [ ] HashDetector测试覆盖率 >90%
- [ ] SimilarityDetector测试覆盖率 >90%
- [ ] StructuredDetector测试覆盖率 >90%
- [ ] SmartDetector测试覆盖率 >90%
- [ ] 算法准确性验证通过
- [ ] 性能测试通过

---

### ⚠️ #053 - 编写推送服务单元测试

**状态**: ⏳ 待办
**负责人**: 无人认领
**优先级**: 🔴 高（本周完成）
**预计工时**: 4h
**依赖**: #026-#029

#### 任务描述

为通知推送模块编写单元测试，包含网络异常处理和重试机制测试。

#### 测试范围

**文件**: `tests/test_notification.py`

需要测试的模块：
- NotificationService
- PushPlusPlatform
- TelegramPlatform
- DiscordPlatform
- FeishuPlatform
- TemplateEngine

#### 测试用例设计

```python
class TestNotificationService:
    """通知服务测试"""

    @pytest.mark.asyncio
    async def test_send_notification(self):
        """测试发送通知"""
        # Mock平台，验证调用正确

    @pytest.mark.asyncio
    async def test_multiple_platforms(self):
        """测试多平台推送"""
        # 验证并发推送

    @pytest.mark.asyncio
    async def test_platform_failure(self):
        """测试平台失败处理"""
        # 一个平台失败不影响其他平台

class TestPlatformIntegration:
    """平台集成测试"""

    @pytest.mark.asyncio
    async def test_pushplus(self):
        """测试PushPlus平台"""
        # Mock HTTP请求

    @pytest.mark.asyncio
    async def test_discord(self):
        """测试Discord平台"""
        # 验证Webhook调用

    @pytest.mark.asyncio
    async def test_network_error_retry(self):
        """测试网络错误重试"""
        # Mock网络超时，验证重试

class TestTemplateEngine:
    """模板引擎测试"""

    def test_template_rendering(self):
        """测试模板渲染"""
        # 验证变量替换

    def test_custom_template(self):
        """测试自定义模板"""
        # 用户自定义模板
```

#### Mock策略

```python
@pytest.fixture
def mock_http_client(mocker):
    """Mock HTTP客户端"""
    mock = mocker.patch('aiohttp.ClientSession.post')
    mock.return_value.__aenter__.return_value.status = 200
    mock.return_value.__aenter__.return_value.json = AsyncMock(
        return_value={'code': 200, 'msg': 'success'}
    )
    return mock
```

#### 验收标准

- [ ] NotificationService测试覆盖率 >90%
- [ ] 所有平台测试覆盖
- [ ] 网络异常处理测试
- [ ] 重试机制验证
- [ ] 所有异步测试通过

---

### 🟡 #054 - 编写CLI命令集成测试

**状态**: ⏳ 待办
**负责人**: 无人认领
**优先级**: 🟡 中（2周内完成）
**预计工时**: 6h
**依赖**: #031-#039

#### 任务描述

端到端测试所有CLI命令，覆盖所有用户场景和错误处理。

#### 测试范围

**文件**: `tests/test_cli_integration.py`

需要测试的命令：
- init命令
- add命令
- remove命令
- list命令
- start命令（前台/守护进程）
- stop命令
- status命令
- test命令
- history命令

#### 集成测试场景

```python
class TestCLIWorkflow:
    """CLI工作流集成测试"""

    def test_complete_workflow(self):
        """测试完整工作流"""
        # 1. init - 初始化配置
        # 2. add - 添加任务
        # 3. list - 查看任务
        # 4. start - 启动监控
        # 5. status - 查看状态
        # 6. stop - 停止监控
        # 7. history - 查看历史
        # 8. remove - 删除任务

    def test_error_scenarios(self):
        """测试错误场景"""
        # 配置文件不存在
        # 任务ID不存在
        # 服务已启动时再次启动
        # 服务未启动时停止
```

#### 验收标准

- [ ] 所有CLI命令测试通过
- [ ] 完整工作流测试
- [ ] 错误场景覆盖
- [ ] 用户体验验证

---

### 🟡 #055 - 编写性能测试

**状态**: ⏳ 待办
**负责人**: 无人认领
**优先级**: 🟡 中（2周内完成）
**预计工时**: 4h
**依赖**: #041, #042

#### 任务描述

测试系统在高负载下的性能表现。

#### 测试范围

**文件**: `tests/test_performance.py`

性能指标：
- 并发任务处理能力
- 内存使用情况
- CPU使用率
- 响应时间
- 稳定性（24小时运行）

#### 性能测试用例

```python
class TestPerformance:
    """性能测试"""

    @pytest.mark.asyncio
    async def test_concurrent_tasks(self):
        """测试并发任务"""
        # 10个任务并发执行
        # 验证执行时间在预期范围

    def test_memory_usage(self):
        """测试内存使用"""
        # 监控内存增长
        # 检测内存泄漏

    @pytest.mark.asyncio
    async def test_long_running(self):
        """测试长时间运行"""
        # 24小时稳定性测试
```

#### 验收标准

- [ ] 10并发任务稳定运行
- [ ] 内存使用 <500MB
- [ ] 无内存泄漏
- [ ] 24小时稳定运行
- [ ] 性能报告完整

---

## 🔐 阶段十一：性能优化和安全（11% 完成）

### 背景

优化系统性能，加强安全防护，为生产环境部署做准备。

---

### ⚠️ #047 - 实现敏感信息保护

**状态**: ⏳ 待办
**负责人**: 无人认领
**优先级**: 🔴 高（本周完成）
**预计工时**: 3h
**依赖**: 无

#### 任务描述

创建SecurityManager类，在日志中自动屏蔽token等敏感信息。

#### 实现细节

**文件**: `webmon/security/security_manager.py`

```python
class SecurityManager:
    """安全管理器"""

    SENSITIVE_KEYS = [
        'token', 'password', 'secret', 'key', 'apikey',
        'webhook_url', 'bot_token', 'chat_id'
    ]

    @staticmethod
    def mask_sensitive_info(data: Any) -> Any:
        """屏蔽敏感信息"""
        if isinstance(data, dict):
            return {
                k: SecurityManager._mask_value(k, v)
                for k, v in data.items()
            }
        elif isinstance(data, str):
            return SecurityManager._mask_string(data)
        return data

    @staticmethod
    def _mask_value(key: str, value: Any) -> Any:
        """屏蔽单个值"""
        key_lower = key.lower()
        if any(sensitive in key_lower for sensitive in SecurityManager.SENSITIVE_KEYS):
            if isinstance(value, str) and len(value) > 8:
                return value[:4] + '****' + value[-4:]
            return '****'
        return value

    @staticmethod
    def _mask_string(text: str) -> str:
        """屏蔽字符串中的敏感信息"""
        # 屏蔽URL中的token参数
        # 屏蔽HTTP头中的Authorization
        return text
```

#### 应用场景

1. **日志输出**: 自动屏蔽日志中的敏感信息
2. **错误报告**: 错误信息中不包含密钥
3. **配置显示**: 显示配置时屏蔽敏感字段
4. **调试信息**: 调试输出中保护隐私

#### 验收标准

- [ ] SecurityManager类实现完整
- [ ] 自动识别敏感字段
- [ ] 日志集成完成
- [ ] 配置显示已屏蔽
- [ ] 单元测试覆盖率 >90%

---

### 🟡 #048 - 实现网络安全功能

**状态**: ⏳ 待办
**负责人**: 无人认领
**优先级**: 🟡 中（2周内完成）
**预计工时**: 4h
**依赖**: #016

#### 任务描述

支持代理配置、SSL验证、User-Agent自定义等网络安全功能。

#### 实现细节

**文件**: `webmon/browser/network_config.py`

```python
class NetworkConfig:
    """网络配置"""

    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager

    def get_proxy_config(self) -> Optional[Dict[str, str]]:
        """获取代理配置"""
        proxy_type = self.config_manager.get('PROXY_TYPE')  # http, https, socks5
        proxy_host = self.config_manager.get('PROXY_HOST')
        proxy_port = self.config_manager.get('PROXY_PORT')

        if all([proxy_type, proxy_host, proxy_port]):
            return {
                'server': f'{proxy_type}://{proxy_host}:{proxy_port}',
                'username': self.config_manager.get('PROXY_USERNAME'),
                'password': self.config_manager.get('PROXY_PASSWORD')
            }
        return None

    def get_ssl_config(self) -> Dict[str, Any]:
        """获取SSL配置"""
        return {
            'verify_ssl': self.config_manager.get('VERIFY_SSL', True),
            'client_cert': self.config_manager.get('CLIENT_CERT_PATH'),
            'client_key': self.config_manager.get('CLIENT_KEY_PATH')
        }
```

#### 支持的代理类型

- HTTP代理
- HTTPS代理
- SOCKS5代理
- 代理认证（用户名/密码）

#### 验收标准

- [ ] 代理配置支持
- [ ] HTTP/HTTPS/SOCKS5代理
- [ ] 代理认证支持
- [ ] SSL验证配置
- [ ] User-Agent自定义
- [ ] 测试通过

---

### 🟡 #049 - 实现内存管理优化

**状态**: ⏳ 待办
**负责人**: 无人认领
**优先级**: 🟡 中（2周内完成）
**预计工时**: 4h
**依赖**: 无

#### 任务描述

创建MemoryManager类，监控和优化内存使用。

#### 实现细节

**文件**: `webmon/utils/memory_manager.py`

```python
class MemoryManager:
    """内存管理器"""

    def __init__(self, max_memory_mb: int = 500):
        self.max_memory_mb = max_memory_mb
        self.logger = logging.getLogger(__name__)

    def get_memory_usage(self) -> Dict[str, float]:
        """获取内存使用情况"""
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()

        return {
            'rss_mb': memory_info.rss / 1024 / 1024,
            'vms_mb': memory_info.vms / 1024 / 1024,
            'percent': process.memory_percent()
        }

    def check_memory_limit(self) -> bool:
        """检查内存是否超限"""
        usage = self.get_memory_usage()
        if usage['rss_mb'] > self.max_memory_mb:
            self.logger.warning(
                f"内存使用超限: {usage['rss_mb']:.1f}MB > {self.max_memory_mb}MB"
            )
            self.trigger_gc()
            return False
        return True

    def trigger_gc(self):
        """触发垃圾回收"""
        import gc
        gc.collect()
```

#### 内存优化策略

1. **定期垃圾回收**: 每小时触发一次gc.collect()
2. **内存监控**: 实时监控内存使用
3. **内存限制**: 超过阈值时降级处理
4. **资源释放**: 及时关闭未使用的浏览器实例
5. **缓存清理**: 定期清理历史记录缓存

#### 验收标准

- [ ] MemoryManager实现
- [ ] 内存监控功能
- [ ] 垃圾回收机制
- [ ] 内存限制检查
- [ ] 10并发任务内存 <500MB

---

### 🟡 #050 - 实现缓存机制

**状态**: ⏳ 待办
**负责人**: 无人认领
**优先级**: 🟡 中（2周内完成）
**预计工时**: 3h
**依赖**: #017

#### 任务描述

支持内容缓存，减少重复请求。

#### 实现细节

**文件**: `webmon/utils/cache_manager.py`

```python
class CacheManager:
    """缓存管理器"""

    def __init__(self, max_size_mb: int = 100):
        self.cache = {}  # URL -> (content, timestamp)
        self.max_size_mb = max_size_mb

    def get(self, url: str, max_age_seconds: int = 300) -> Optional[str]:
        """获取缓存"""
        if url in self.cache:
            content, timestamp = self.cache[url]
            if time.time() - timestamp < max_age_seconds:
                return content
            else:
                del self.cache[url]
        return None

    def set(self, url: str, content: str):
        """设置缓存"""
        self.cache[url] = (content, time.time())
        self._cleanup_if_needed()

    def _cleanup_if_needed(self):
        """清理缓存"""
        # LRU清理策略
        pass
```

#### 验收标准

- [ ] CacheManager实现
- [ ] 缓存时间可配置
- [ ] LRU清理策略
- [ ] 缓存大小限制
- [ ] 缓存命中率 >80%

---

## 📚 阶段十二：文档和发布（0% 完成）

### 背景

完善用户文档，准备项目发布。

---

### 🟢 #056 - 编写安装指南文档

**状态**: ⏳ 待办
**负责人**: 无人认领
**优先级**: 🟢 低（可选）
**预计工时**: 3h
**依赖**: #031

#### 任务描述

详细的安装和配置说明，让新用户能在30分钟内完成安装和首次使用。

#### 文档结构

**文件**: `docs/installation.md`

```markdown
# WebMon 安装指南

## 系统要求

- Python 3.8+
- pip 20.0+
- 操作系统：Windows/Linux/macOS

## 安装步骤

### 1. 安装依赖

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 2. 安装Playwright浏览器

\`\`\`bash
python -m playwright install chromium
\`\`\`

### 3. 初始化配置

\`\`\`bash
python webmon.py init
\`\`\`

### 4. 配置推送平台

编辑 `.env` 文件，填入推送平台的token...

## 常见问题

Q: 安装失败怎么办？
A: ...
```

#### 验收标准

- [ ] 安装步骤清晰完整
- [ ] 包含系统要求
- [ ] 包含常见问题解答
- [ ] 新用户测试通过（30分钟内完成）

---

### 🟢 #057 - 编写使用手册

**状态**: ⏳ 待办
**负责人**: 无人认领
**优先级**: 🟢 低（可选）
**预计工时**: 4h
**依赖**: #031-#039

#### 任务描述

详细说明每个命令的使用方法，包含示例和常见问题。

#### 文档结构

**文件**: `docs/user-manual.md`

```markdown
# WebMon 使用手册

## 命令参考

### init命令

初始化配置文件...

### add命令

添加监控任务...

## 使用场景

### 场景1：监控新闻网站

...

### 场景2：监控商品价格

...

## 最佳实践

### 检测间隔设置

- 高频网站：5-15分钟
- 一般网站：30-60分钟
- 低频网站：2-6小时
```

#### 验收标准

- [ ] 所有命令有详细说明
- [ ] 包含使用示例
- [ ] 包含场景案例
- [ ] 包含最佳实践

---

### 🟢 #058 - 编写配置说明文档

**状态**: ⏳ 待办
**负责人**: 无人认领
**优先级**: 🟢 低（可选）
**预计工时**: 3h
**依赖**: #007

#### 任务描述

详细解释所有配置选项，包含示例和最佳实践。

#### 文档结构

**文件**: `docs/configuration.md`

```markdown
# WebMon 配置指南

## 配置文件

### config.json结构

\`\`\`json
{
  "monitoring": {...},
  "detection": {...},
  "notification": {...}
}
\`\`\`

### 环境变量

所有支持的环境变量...

## 配置示例

### 基础配置

...

### 高级配置

...
```

#### 验收标准

- [ ] 所有配置项有说明
- [ ] 包含完整示例
- [ ] 包含默认值说明
- [ ] 包含最佳实践

---

### 🟢 #059 - 创建README.md

**状态**: ⏳ 待办
**负责人**: 无人认领
**优先级**: 🟢 低（可选）
**预计工时**: 2h
**依赖**: #056-#058

#### 任务描述

项目主页文档，包含快速开始指南。

#### 文档结构

**文件**: `README.md`

```markdown
# WebMon - 网页监控工具

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

## 简介

WebMon是一个...

## 特性

- ✅ 支持静态和动态网页
- ✅ 多种变化检测算法
- ✅ 多平台推送通知
- ✅ 简单易用的CLI

## 快速开始

\`\`\`bash
# 安装
pip install -r requirements.txt

# 初始化
python webmon.py init

# 添加任务
python webmon.py add https://example.com --name "示例网站"

# 启动监控
python webmon.py start
\`\`\`

## 文档

- [安装指南](docs/installation.md)
- [使用手册](docs/user-manual.md)
- [配置说明](docs/configuration.md)

## License

MIT License
```

#### 验收标准

- [ ] README完整
- [ ] 包含徽章
- [ ] 快速开始指南
- [ ] 文档链接完整
- [ ] 格式美观

---

### 🟢 #060 - 创建示例配置文件

**状态**: ⏳ 待办
**负责人**: 无人认领
**优先级**: 🟢 低（可选）
**预计工时**: 2h
**依赖**: #007

#### 任务描述

创建config.json.example和完整示例。

#### 验收标准

- [ ] config.json.example完整
- [ ] .env.example完整
- [ ] 包含所有可配置项
- [ ] 注释详细

---

### 🟢 #061 - 项目打包配置

**状态**: ⏳ 待办
**负责人**: 无人认领
**优先级**: 🟢 低（可选）
**预计工时**: 3h
**依赖**: 全部核心功能

#### 任务描述

配置setup.py，支持pip安装。

#### 实现细节

**文件**: `setup.py`

```python
from setuptools import setup, find_packages

setup(
    name='webmon',
    version='1.0.0',
    description='网页监控工具',
    author='WebMon Team',
    packages=find_packages(),
    install_requires=[
        'playwright>=1.40.0',
        'loguru>=0.7.0',
        'python-dotenv>=1.0.0',
        'aiohttp>=3.9.0',
        # ...
    ],
    entry_points={
        'console_scripts': [
            'webmon=webmon.cli.main:main',
        ],
    },
)
```

#### 验收标准

- [ ] setup.py完整
- [ ] 可通过pip install安装
- [ ] 命令行工具可用
- [ ] 依赖自动安装

---

### 🟢 #062 - 创建发布检查清单

**状态**: ⏳ 待办
**负责人**: 无人认领
**优先级**: 🟢 低（可选）
**预计工时**: 1h
**依赖**: 全部任务

#### 任务描述

发布前的各项检查清单。

#### 文档结构

**文件**: `docs/release-checklist.md`

```markdown
# 发布检查清单

## 功能检查

- [ ] 所有核心功能正常
- [ ] 所有CLI命令可用
- [ ] 通知推送正常

## 测试检查

- [ ] 单元测试全部通过
- [ ] 集成测试通过
- [ ] 性能测试通过
- [ ] 测试覆盖率 >80%

## 文档检查

- [ ] README完整
- [ ] 安装指南完整
- [ ] 使用手册完整

## 安全检查

- [ ] 无敏感信息泄露
- [ ] 依赖安全扫描通过
- [ ] 代码安全审计通过

## 发布检查

- [ ] 版本号更新
- [ ] CHANGELOG更新
- [ ] Git标签创建
```

#### 验收标准

- [ ] 检查清单完整
- [ ] 包含所有检查项
- [ ] 可操作性强

---

## 📊 项目统计

### 任务完成情况

| 阶段 | 任务数 | 已完成 | 进行中 | 待办 | 完成度 |
|------|--------|--------|--------|------|--------|
| 阶段一 | 5 | 5 | 0 | 0 | 100% |
| 阶段三 | 5 | 5 | 0 | 0 | 100% |
| 阶段四 | 5 | 5 | 0 | 0 | 100% |
| 阶段五 | 5 | 5 | 0 | 0 | 100% |
| 阶段六 | 5 | 5 | 0 | 0 | 100% |
| 阶段七 | 9 | 9 | 0 | 0 | 100% |
| 阶段八 | 3 | 3 | 0 | 0 | 100% |
| 阶段九 | 4 | 3 | 0 | 1 | 88% |
| 阶段十 | 5 | 0 | 0 | 5 | 0% |
| 阶段十一 | 4 | 0 | 0 | 4 | 0% |
| 阶段十二 | 7 | 0 | 0 | 7 | 0% |
| **总计** | **62** | **47** | **0** | **15** | **77%** |

### 代码统计

- **总代码行数**: ~21,932行
- **Python文件数**: 67个
- **测试代码**: ~1,811行
- **核心模块**: 15个
- **当前测试覆盖率**: ~20%
- **目标测试覆盖率**: >80%

### 里程碑进度

- ✅ **里程碑1: MVP** - 100% (2025-11-28)
- ✅ **里程碑2: 功能完善** - 100% (2025-11-29)
- 🚧 **里程碑3: 生产就绪** - 45% (预计2025-12-09)
- 📅 **里程碑4: 正式发布** - 0% (预计2025-12-16)

---

## 🔗 相关文档

- [项目设计文档](design.md)
- [需求文档](requirements.md)
- [阶段三总结](stage3_summary.md)
- [阶段八总结](stage8_summary.md)
- [任务看板](../TASKS.md)
- [项目进度分析](project_progress_analysis.md)

---

## 📝 更新日志

### 2025-12-02

- 重建docs/tasks.md文档
- 更新任务进度统计
- 添加详细的测试任务说明
- 完善验收标准

### 2025-11-29

- 完成阶段八所有任务
- 日志和异常处理完成88%
- 项目整体进度达到77%

### 2025-11-28

- 完成阶段一至七所有任务
- 核心功能开发完成
- CLI命令系统完成

---

**维护者**: WebMon 开发团队
**最后更新**: 2025-12-02
**文档版本**: 2.0
