# Claude Code 使用规范

> **版本**: 1.1
> **更新日期**: 2025-12-02
> **维护者**: WebMon 开发团队

---

## Token 使用报告规则

**规则：** 每个任务完成之后，必须显示当前Token使用情况，格式如下：

```
📊 Token使用情况：已用 X / 总计 Y (占比 aa.bb%)
```

---

## 任务管理规范

**规则：** 执行任务之前，阅读TASKS.md，并遵循其中任务管理规则。

### 任务操作流程

1. **认领任务**：在TASKS.md中更新任务状态和负责人
2. **开始任务**：使用TodoWrite工具追踪进度
3. **提交变更**：按照Git规范提交代码
4. **完成任务**：更新TASKS.md并推送到远程仓库

---

## 项目目录结构规范

### 1. 根目录结构

```
airdrop-watcher/
├── .claude/                    # Claude Code 配置目录
│   ├── guide.md               # 项目规范文档（本文件）
│   └── settings.local.json    # 本地设置
├── archive/                   # 归档目录（调试文件、临时测试）
│   ├── debug_files/          # 调试文件
│   ├── demo_logs/            # 演示日志
│   └── test_files/           # 临时测试文件
├── backup/                    # 配置备份目录
├── config/                    # 配置文件目录（生产配置）
│   ├── backup/               # 配置文件备份
│   └── config.json           # 主配置文件
├── data/                      # 数据存储目录
│   ├── backup/               # 数据备份
│   └── history.json          # 历史记录
├── docs/                      # 项目文档
│   ├── design.md             # 设计文档
│   ├── requirements.md       # 需求文档
│   ├── tasks.md              # 任务详细文档
│   └── stage*_summary.md     # 阶段总结文档
├── examples/                  # 示例代码
├── logs/                      # 日志文件目录
├── tests/                     # 测试目录（项目级测试）
│   ├── test_browser_engine.py
│   ├── test_cli_commands.py
│   └── test_task_scheduler.py
├── venv/                      # Python虚拟环境
├── webmon/                    # 主包目录（见下文）
├── .env                       # 环境变量配置（本地，不提交）
├── .env.example               # 环境变量示例
├── .gitignore                 # Git忽略规则
├── config.json                # 配置文件（旧版，待清理）
├── README.md                  # 项目说明
├── requirements.txt           # Python依赖
├── TASKS.md                   # 任务看板
└── webmon.py                  # CLI入口脚本
```

**重要规则：**

- ✅ **archive/** - 所有调试、临时、测试文件必须放在此目录
- ✅ **config/** - 生产环境配置文件目录，不要在根目录创建配置
- ✅ **data/** - 所有运行时数据存储在此目录
- ✅ **docs/** - 所有项目文档集中管理
- ✅ **tests/** - 项目级集成测试和端到端测试
- ❌ **禁止** 在根目录创建临时测试文件
- ❌ **禁止** 在根目录创建调试脚本

---

### 2. webmon 包结构

```
webmon/
├── browser/                   # 浏览器引擎模块
│   ├── browser_engine.py     # 浏览器引擎主类
│   ├── network_config.py     # 网络配置管理
│   ├── performance_optimizer.py  # 性能优化
│   ├── resource_manager.py   # 资源管理
│   └── __init__.py
├── cli/                       # 命令行接口模块
│   ├── commands/             # CLI命令实现
│   │   ├── add_command.py
│   │   ├── init_command.py
│   │   ├── list_command.py
│   │   ├── start_command.py
│   │   ├── status_command.py
│   │   ├── stop_command.py
│   │   ├── test_command.py
│   │   └── history_command.py
│   ├── argument_parser.py    # 参数解析器
│   ├── command_factory.py    # 命令工厂
│   ├── command.py            # 命令基类
│   └── __init__.py
├── config/                    # 配置管理模块
│   ├── config_manager.py     # 配置管理器主类
│   ├── env_config.py         # 环境变量配置
│   ├── json_config.py        # JSON配置
│   ├── config_validator.py   # 配置验证
│   ├── constants.py          # 常量定义
│   └── __init__.py
├── core/                      # 核心模块（预留）
│   └── __init__.py
├── detection/                 # 变化检测模块
│   ├── base_detector.py      # 检测器基类
│   ├── change_detector.py    # 主变化检测器
│   ├── similarity_detector.py # 相似度检测
│   ├── structured_detector.py # 结构化检测
│   ├── content_extractor.py  # 内容提取
│   └── __init__.py
├── exceptions/                # 异常定义模块
│   └── __init__.py           # 所有自定义异常
├── models/                    # 数据模型模块
│   ├── task.py               # 任务模型
│   ├── check_result.py       # 检测结果模型
│   ├── change_details.py     # 变化详情模型
│   └── __init__.py
├── notification/              # 通知服务模块
│   ├── platforms/            # 各推送平台实现
│   │   ├── pushplus_platform.py
│   │   ├── telegram_platform.py
│   │   ├── discord_platform.py
│   │   └── feishu_platform.py
│   ├── base_platform.py      # 平台基类
│   ├── factory.py            # 平台工厂
│   ├── service.py            # 通知服务
│   ├── template_engine.py    # 模板引擎
│   └── __init__.py
├── scheduler/                 # 任务调度模块
│   ├── task_scheduler.py     # 任务调度器
│   ├── execution_engine.py   # 执行引擎
│   ├── job_queue.py          # 任务队列
│   ├── priority_manager.py   # 优先级管理
│   ├── scheduler_config.py   # 调度器配置
│   └── __init__.py
├── storage/                   # 存储管理模块
│   ├── task_storage.py       # 任务存储
│   ├── history_storage.py    # 历史记录存储
│   └── __init__.py
├── tests/                     # 单元测试模块
│   ├── unit/                 # 单元测试
│   ├── integration/          # 集成测试
│   └── __init__.py
├── utils/                     # 工具函数模块
│   ├── logger.py             # 日志管理
│   ├── enhanced_logger.py    # 增强日志
│   ├── log_config.py         # 日志配置
│   ├── formatters.py         # 格式化工具
│   ├── validators.py         # 验证工具
│   └── __init__.py
└── __init__.py
```

---

## 模块职责说明

### browser - 浏览器引擎

**职责**: 封装Playwright浏览器操作，提供网页内容获取能力

**核心类**:
- `BrowserEngine`: 浏览器引擎主类
- `NetworkConfig`: 网络配置（代理、SSL、User-Agent）
- `ResourceManager`: 浏览器资源管理
- `PerformanceOptimizer`: 性能优化器

**依赖**: Playwright, config

### cli - 命令行接口

**职责**: 提供用户交互的CLI命令

**核心类**:
- `ArgumentParser`: 命令行参数解析
- `CommandFactory`: 命令工厂模式
- `*Command`: 各种具体命令实现

**依赖**: config, storage, scheduler, notification

### config - 配置管理

**职责**: 统一管理配置文件和环境变量

**核心类**:
- `ConfigManager`: 配置管理器主类
- `EnvConfig`: 环境变量配置
- `JsonConfig`: JSON配置文件

**依赖**: 无（基础模块）

### detection - 变化检测

**职责**: 检测网页内容变化

**核心类**:
- `ChangeDetector`: 主变化检测器
- `SimilarityDetector`: 相似度算法
- `StructuredDetector`: 结构化检测

**依赖**: models

### models - 数据模型

**职责**: 定义核心数据结构

**核心类**:
- `Task`: 监控任务模型
- `CheckResult`: 检测结果模型
- `ChangeDetails`: 变化详情模型

**依赖**: 无（基础模块）

### notification - 通知服务

**职责**: 多平台消息推送

**核心类**:
- `NotificationService`: 通知服务主类
- `*Platform`: 各平台具体实现
- `TemplateEngine`: 消息模板引擎

**依赖**: config

### scheduler - 任务调度

**职责**: 管理任务调度和并发执行

**核心类**:
- `TaskScheduler`: 任务调度器
- `ExecutionEngine`: 执行引擎
- `JobQueue`: 任务队列
- `PriorityManager`: 优先级管理

**依赖**: browser, detection, notification, storage

### storage - 数据存储

**职责**: 管理任务和历史记录的持久化

**核心类**:
- `TaskStorage`: 任务存储
- `HistoryStorage`: 历史记录存储

**依赖**: models

### utils - 工具函数

**职责**: 提供通用工具函数

**核心模块**:
- `logger`: 日志管理
- `validators`: 数据验证
- `formatters`: 格式化工具

**依赖**: 无（基础模块）

---

## 代码组织规范

### 1. 文件命名规范

- **Python模块**: 小写字母 + 下划线，如 `browser_engine.py`
- **Python类**: 驼峰命名，如 `BrowserEngine`
- **配置文件**: 小写字母，如 `config.json`
- **文档文件**: 小写字母 + 下划线，如 `stage3_summary.md`
- **测试文件**: `test_` 前缀，如 `test_browser_engine.py`

### 2. 包导入规范

```python
# 标准库导入
import os
import sys
import asyncio

# 第三方库导入
from playwright.async_api import async_playwright

# 本地包导入（相对导入）
from ..config import ConfigManager
from ..exceptions import BrowserError
from .network_config import NetworkConfig
```

**规则：**
- 使用相对导入（`..` 或 `.`）引用本项目模块
- 按照：标准库 → 第三方库 → 本地包的顺序
- 每组之间空一行

### 3. 类设计规范

```python
class ExampleClass:
    """类的简要说明

    详细说明...

    Attributes:
        attr1: 属性1说明
        attr2: 属性2说明
    """

    def __init__(self, param1, param2):
        """初始化方法

        Args:
            param1: 参数1说明
            param2: 参数2说明
        """
        self.attr1 = param1
        self.attr2 = param2

    def public_method(self):
        """公共方法说明"""
        pass

    def _private_method(self):
        """私有方法说明（单下划线）"""
        pass
```

**规则：**
- 所有类必须有docstring
- 所有公共方法必须有docstring
- 私有方法使用单下划线前缀
- 类内方法顺序：`__init__` → 公共方法 → 私有方法

### 4. 错误处理规范

```python
try:
    # 尝试执行的代码
    result = some_operation()
except SpecificError as e:
    self.logger.error(f"具体错误描述: {e}")
    raise CustomError(f"转换为项目异常: {e}")
except Exception as e:
    self.logger.error(f"未预期的错误: {e}")
    raise
```

**规则：**
- 优先捕获具体异常类型
- 记录错误日志
- 转换为项目自定义异常
- 避免空except语句

### 5. 日志使用规范

```python
from ..utils.logger import get_logger

class ExampleClass:
    def __init__(self):
        self.logger = get_logger(__name__)

    def some_method(self):
        self.logger.debug("调试信息")
        self.logger.info("一般信息")
        self.logger.warning("警告信息")
        self.logger.error("错误信息")
```

**日志级别使用：**
- `DEBUG`: 详细的调试信息
- `INFO`: 关键操作的确认信息
- `WARNING`: 警告但不影响运行
- `ERROR`: 错误但可以继续运行
- `CRITICAL`: 严重错误，程序可能无法继续

---

## 新功能开发规范

### 1. 添加新模块

当需要添加新功能模块时：

1. **确定模块位置**: 在 `webmon/` 下选择合适的子包，或创建新子包
2. **创建模块文件**: 使用小写字母+下划线命名
3. **实现核心类**: 遵循类设计规范
4. **更新__init__.py**: 在对应的`__init__.py`中导出新类
5. **编写单元测试**: 在`webmon/tests/unit/`或`tests/`中添加测试
6. **更新文档**: 在`docs/`中更新相关文档

### 2. 修改现有模块

修改现有功能时：

1. **阅读现有代码**: 理解当前实现
2. **保持接口兼容**: 不要破坏已有API
3. **更新测试**: 确保所有测试通过
4. **更新文档**: 同步更新文档

### 3. 添加配置项

添加新配置时：

1. **环境变量**: 在`.env.example`中添加示例
2. **JSON配置**: 在`config/config.json`中添加默认值
3. **常量定义**: 在`webmon/config/constants.py`中定义常量
4. **配置文档**: 在`docs/`中说明配置用途

---

## 测试规范

### 1. 测试文件位置

- **单元测试**: `webmon/tests/unit/` 或 `tests/`
- **集成测试**: `webmon/tests/integration/` 或 `tests/`
- **临时测试**: `archive/test_files/`（不提交到git）

### 2. 测试命名

```python
class TestBrowserEngine:
    """测试类名: Test + 被测试类名"""

    def test_initialize(self):
        """测试方法名: test_ + 功能描述"""
        pass

    def test_get_page_content_success(self):
        """详细描述测试场景"""
        pass

    def test_get_page_content_timeout(self):
        """测试异常情况"""
        pass
```

### 3. 运行测试

```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行特定文件
python -m pytest tests/test_browser_engine.py -v

# 查看覆盖率
python -m pytest tests/ --cov=webmon --cov-report=html
```

---

## Git 提交规范

### 1. 提交消息格式

```
<类型>: <简短描述> (#任务编号)

<详细描述>
- 具体变更1
- 具体变更2

验收标准：
✅ 标准1
✅ 标准2

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### 2. 提交类型

- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具链相关
- `task`: 任务管理相关

### 3. 示例

```bash
git commit -m "feat: 实现网络安全功能 (#048)

- 创建NetworkConfig类
- 支持HTTP/HTTPS/SOCKS5代理
- 集成到BrowserEngine

验收标准：
✅ 代理配置正常工作
✅ 所有测试通过

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## 文档维护规范

### 1. 必须更新的文档

添加新功能时，必须同步更新：

- `README.md`: 如果影响用户使用
- `docs/design.md`: 如果影响系统设计
- `docs/tasks.md`: 如果是新任务
- `TASKS.md`: 任务状态更新
- 本文件（guide.md）: 如果影响目录结构或规范

### 2. 文档编写规范

- 使用Markdown格式
- 使用中文编写（代码注释可用英文）
- 包含代码示例
- 包含使用场景说明

---

## 禁止事项

### ❌ 绝对禁止

1. **在根目录创建临时文件** - 必须放在`archive/`
2. **提交调试代码** - 清理后再提交
3. **硬编码配置** - 使用配置文件或环境变量
4. **跳过测试** - 所有功能必须有测试
5. **不写文档** - 新功能必须有文档
6. **破坏现有API** - 保持向后兼容
7. **使用中文命名变量** - 代码中使用英文

### ⚠️ 谨慎操作

1. **修改核心模块** - 充分测试
2. **变更数据模型** - 考虑数据迁移
3. **调整目录结构** - 更新文档
4. **删除功能** - 确认无依赖

---

## 检查清单

### 提交前检查

- [ ] 代码符合命名规范
- [ ] 添加了必要的docstring
- [ ] 编写了单元测试
- [ ] 所有测试通过
- [ ] 更新了相关文档
- [ ] 清理了临时文件
- [ ] Git提交消息规范
- [ ] 代码已经格式化

### 任务完成检查

- [ ] TASKS.md已更新
- [ ] TodoWrite已标记完成
- [ ] 代码已提交并推送
- [ ] 文档已同步更新
- [ ] Token使用已报告

---

## 附录：常用命令

### 项目运行

```bash
# 初始化配置
python webmon.py init

# 添加任务
python webmon.py add https://example.com --name "示例"

# 启动监控
python webmon.py start

# 查看状态
python webmon.py status

# 测试通知
python webmon.py test --platform discord
```

### 开发命令

```bash
# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行测试
python -m pytest tests/ -v

# 代码格式化
black webmon/

# 代码检查
flake8 webmon/
```

---

**最后更新**: 2025-12-02
**维护者**: WebMon 开发团队
