# WebMon - 网页监控工具

WebMon 是一个功能强大的网页监控工具，基于 Playwright 浏览器引擎，支持自动检测网页变化并通过多个平台发送通知。支持 AI 智能分析变化内容，提供 WebUI 管理界面。

## 特性

### 核心功能
- 基于 Playwright 的无头浏览器，支持 JavaScript 渲染
- 智能变化检测算法（哈希对比、相似度分析）
- 多平台通知支持（Discord、Telegram、飞书、PushPlus）
- 灵活的任务调度系统，支持自定义检测间隔
- CSS 选择器支持，精准监控页面特定区域
- 完整的历史记录和变化追踪
- 代理支持，适应各种网络环境

### AI 智能分析
- 支持 OpenAI 兼容 API（OpenAI、DeepSeek、通义千问等）
- 自动分析网页变化，生成自然语言摘要
- 可自定义分析提示词模板
- AI 分析结果集成到通知推送

### WebUI 管理界面
- 现代化 Web 界面（Vue 3 + Naive UI）
- 实时监控状态仪表盘
- 任务管理（增删改查）
- 历史记录查看和 Diff 对比
- 系统配置管理
- SSE 实时事件推送

### 安全特性
- 敏感信息自动屏蔽（Token、API Key、密码等）
- 日志中不泄露敏感数据
- 支持环境变量配置敏感信息

## 系统要求

- Python 3.10+
- Node.js 18+（仅 WebUI 开发需要）
- 现代浏览器（Chromium，由 Playwright 自动安装）

## 快速开始

### 方式一：使用 venv 部署（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/xiedidan/airdrop-watcher.git
cd airdrop-watcher

# 2. 创建虚拟环境
python3 -m venv venv

# 3. 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 4. 安装依赖
pip install -r requirements.txt

# 5. 安装 Playwright 浏览器
playwright install chromium

# 6. 初始化配置
python webmon.py init

# 7. 启动服务
python webmon.py start
```

### 方式二：使用 Docker 部署

```bash
# 1. 克隆项目
git clone https://github.com/xiedidan/airdrop-watcher.git
cd airdrop-watcher

# 2. 复制环境变量配置
cp .env.docker.example .env

# 3. 编辑 .env 配置通知平台凭据
vim .env

# 4. 构建并启动
docker-compose up -d

# 5. 查看日志
docker-compose logs -f
```

### 方式三：使用 WebUI

```bash
# 启动 WebUI 服务（包含后端 API）
python webmon.py web

# 指定端口
python webmon.py web --port 8080

# 不自动打开浏览器
python webmon.py web --no-browser

# 开发模式（自动重载）
python webmon.py web --reload
```

访问 http://localhost:8020 即可使用 WebUI 管理界面。

**端口配置**：默认端口为 8020，可通过以下方式配置：
- 命令行参数：`--port 8080`
- 环境变量：`WEB_PORT=8080`
- .env 文件：添加 `WEB_PORT=8080`

## 配置通知平台

编辑 `.env` 文件，添加通知平台凭据：

```bash
# Discord Webhook
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_URL

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# 飞书 Webhook
FEISHU_WEBHOOK_URL=your_webhook_url

# PushPlus
PUSHPLUS_TOKEN=your_token

# AI 分析配置（可选）
AI_API_KEY=your_api_key
AI_API_URL=https://api.openai.com/v1
AI_MODEL=gpt-4o-mini

# 代理设置（可选）
HTTP_PROXY=http://127.0.0.1:10808
HTTPS_PROXY=http://127.0.0.1:10808
```

在 `config/config.json` 中启用平台：

```json
{
  "notification": {
    "platforms": ["discord"],
    "platform_configs": {
      "discord": {
        "enabled": true,
        "webhook_url": "${DISCORD_WEBHOOK_URL}"
      }
    }
  }
}
```

## CLI 命令

### 基础命令

```bash
# 初始化配置
python webmon.py init [--force]

# 添加监控任务
python webmon.py add <url> [--name NAME] [--interval SECONDS] [--selector CSS] [--timeout MS]

# 列出所有任务
python webmon.py list [--format table|json|csv] [--filter all|enabled|disabled|error]

# 删除任务
python webmon.py remove <task_id>

# 编辑任务
python webmon.py edit <task_id> [--name NAME] [--interval SECONDS] [--enabled true|false]

# 启动监控服务
python webmon.py start

# 停止监控服务
python webmon.py stop

# 查看服务状态
python webmon.py status [--verbose]

# 测试通知
python webmon.py test [--platform discord|telegram|feishu|pushplus]

# 查看历史记录
python webmon.py history <task_id> [--limit N] [--changes-only]

# 启动 WebUI
python webmon.py web [--port PORT] [--no-browser] [--reload]

# 管理配置
python webmon.py config [show|ai|set]
```

### 使用示例

```bash
# 监控 Hacker News 首页标题
python webmon.py add https://news.ycombinator.com \
  --name "HN首页" \
  --selector ".titleline" \
  --interval 300

# 监控 GitHub 仓库
python webmon.py add https://github.com/user/repo \
  --name "项目主页" \
  --interval 3600

# 添加带描述的任务（用于 AI 分析）
python webmon.py add https://example.com \
  --name "示例网站" \
  --description "监控首页公告信息，关注价格和活动变化" \
  --interval 600
```

## 项目结构

```
airdrop-watcher/
├── webmon.py                  # CLI 入口
├── requirements.txt           # Python 依赖
├── Dockerfile                 # Docker 镜像构建
├── docker-compose.yml         # Docker 编排
├── .env.example              # 环境变量示例
├── .env.docker.example       # Docker 环境变量示例
├── config/
│   └── config.json           # 主配置文件
├── data/
│   └── history.json          # 变化历史
├── logs/                     # 日志文件
├── frontend/                 # Vue 3 前端
│   ├── src/
│   │   ├── views/           # 页面组件
│   │   ├── stores/          # Pinia 状态管理
│   │   ├── api/             # API 服务
│   │   └── components/      # 通用组件
│   └── package.json
├── docs/                     # 文档
└── webmon/                   # 核心代码
    ├── cli/                  # CLI 模块
    │   ├── argument_parser.py
    │   ├── command_factory.py
    │   └── commands/        # 命令实现
    ├── config/              # 配置管理
    │   ├── config_manager.py
    │   ├── env_config.py
    │   └── json_config.py
    ├── models/              # 数据模型
    │   ├── task.py
    │   ├── check_result.py
    │   └── change_details.py
    ├── storage/             # 存储管理
    │   ├── task_storage.py
    │   └── history_storage.py
    ├── browser/             # 浏览器引擎
    │   ├── browser_engine.py
    │   ├── resource_manager.py
    │   └── network_config.py
    ├── detection/           # 变化检测
    │   ├── change_detector.py
    │   └── similarity_detector.py
    ├── notification/        # 通知推送
    │   ├── service.py
    │   ├── base_platform.py
    │   └── platforms/
    │       ├── discord_platform.py
    │       ├── telegram_platform.py
    │       ├── feishu_platform.py
    │       └── pushplus_platform.py
    ├── scheduler/           # 任务调度
    │   ├── task_scheduler.py
    │   ├── execution_engine.py
    │   └── job_queue.py
    ├── ai/                  # AI 分析
    │   ├── service.py
    │   └── models.py
    ├── web/                 # WebUI 后端
    │   ├── app.py
    │   ├── api/            # API 路由
    │   ├── schemas/        # 数据模型
    │   └── services/       # 服务层
    └── utils/              # 工具类
        ├── logger.py
        ├── security_manager.py  # 敏感信息保护
        └── validators.py
```

## 配置说明

### 环境变量 (.env)

| 变量 | 说明 | 默认值 |
|------|------|--------|
| WEB_PORT | WebUI 服务端口 | 8020 |
| WEB_HOST | WebUI 监听地址 | 0.0.0.0 |
| LOG_LEVEL | 日志级别 | INFO |
| DISCORD_WEBHOOK_URL | Discord Webhook URL | - |
| TELEGRAM_BOT_TOKEN | Telegram Bot Token | - |
| TELEGRAM_CHAT_ID | Telegram Chat ID | - |
| FEISHU_WEBHOOK_URL | 飞书 Webhook URL | - |
| PUSHPLUS_TOKEN | PushPlus Token | - |
| AI_API_KEY | AI API 密钥 | - |
| AI_API_URL | AI API 地址 | https://api.deepseek.com/v1 |
| AI_MODEL | AI 模型名称 | deepseek-reasoner |
| HTTP_PROXY | HTTP 代理 | - |
| HTTPS_PROXY | HTTPS 代理 | - |

### 主配置文件 (config/config.json)

```json
{
  "version": "1.0.0",
  "settings": {
    "default_check_interval": 60,
    "max_concurrent_tasks": 5,
    "browser_timeout": 30,
    "similarity_threshold": 0.95,
    "max_retry_times": 3
  },
  "notification": {
    "platforms": ["discord"],
    "platform_configs": {
      "discord": {
        "enabled": true,
        "webhook_url": "${DISCORD_WEBHOOK_URL}"
      }
    }
  },
  "ai": {
    "enabled": true,
    "api_url": "${AI_API_URL}",
    "api_key": "${AI_API_KEY}",
    "model": "gpt-4o-mini",
    "max_tokens": 2048,
    "temperature": 0.7
  },
  "scheduler": {
    "performance": {
      "max_concurrent_tasks": 15,
      "max_browser_resources": 8
    },
    "retry": {
      "retry_attempts": 5,
      "retry_delay": 120
    }
  },
  "logging": {
    "level": "INFO",
    "log_dir": "logs",
    "rotation": {
      "type": "size",
      "max_size": 5242880,
      "backup_count": 3
    }
  }
}
```

## 已实现功能

### CLI 命令系统
- [x] init - 初始化配置
- [x] add - 添加监控任务
- [x] remove - 删除任务
- [x] edit - 编辑任务
- [x] list - 列出任务
- [x] start - 启动服务
- [x] stop - 停止服务
- [x] status - 查看状态
- [x] test - 测试通知
- [x] history - 查看历史
- [x] config - 管理配置
- [x] web - 启动 WebUI

### 核心功能
- [x] Playwright 浏览器引擎集成
- [x] 智能变化检测算法
- [x] 多平台通知支持（Discord、Telegram、飞书、PushPlus）
- [x] 任务调度和并发管理
- [x] 配置管理系统
- [x] 历史记录和变化追踪
- [x] 代理支持
- [x] 日志系统
- [x] 资源管理和优化
- [x] 敏感信息自动保护

### AI 分析
- [x] OpenAI 兼容 API 支持
- [x] 提示词模板系统
- [x] 集成到通知流程

### WebUI
- [x] FastAPI 后端框架
- [x] Vue 3 前端框架
- [x] Dashboard 仪表盘
- [x] 任务管理页面
- [x] 历史记录页面
- [x] 系统设置页面
- [x] SSE 实时事件推送
- [x] Docker 部署支持

### 测试状态
- [x] Discord 通知 - 已测试通过 ✅
- [x] 变化检测 - 功能正常 ✅
- [x] 任务调度 - 稳定运行 ✅
- [x] WebUI - 功能正常 ✅
- [ ] Telegram 通知 - 待测试
- [ ] 飞书通知 - 待测试
- [ ] PushPlus 通知 - 待测试

## 故障排查

### 浏览器启动失败

```bash
# 重新安装 Playwright 浏览器
playwright install chromium

# 检查系统依赖
playwright install-deps
```

### 通知发送失败

```bash
# 测试通知配置
python webmon.py test --platform discord

# 检查环境变量
cat .env | grep DISCORD

# 查看日志
tail -f logs/webmon.log
```

### WebUI 无法访问

```bash
# 检查端口是否被占用
lsof -i :8000

# 查看 WebUI 日志
python webmon.py web --reload

# 检查前端构建
cd frontend && npm run build
```

### 代理问题

```bash
# 设置代理环境变量
export HTTP_PROXY=http://127.0.0.1:10808
export HTTPS_PROXY=http://127.0.0.1:10808

# 或在 .env 文件中配置
echo "HTTP_PROXY=http://127.0.0.1:10808" >> .env
echo "HTTPS_PROXY=http://127.0.0.1:10808" >> .env
```

## 开发指南

### 本地开发环境

```bash
# 安装开发依赖
pip install -r requirements.txt

# 安装前端依赖
cd frontend && npm install

# 启动前端开发服务器
npm run dev

# 启动后端开发服务器（另一个终端）
python webmon.py web --reload
```

### 运行测试

```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试
python -m pytest webmon/tests/unit/test_security_manager.py -v

# 生成覆盖率报告
python -m pytest tests/ --cov=webmon --cov-report=html
```

### 代码格式化

```bash
# 格式化代码
black webmon/

# 检查代码风格
flake8 webmon/

# 类型检查
mypy webmon/
```

## 开发文档

- [设计文档](docs/design.md)
- [WebUI 设计文档](docs/webui_design.md)
- [API 文档](docs/api.md)
- [任务清单](TASKS.md)

## 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

此项目采用 MIT 许可证。

## 致谢

- [Playwright](https://playwright.dev/) - 浏览器自动化
- [FastAPI](https://fastapi.tiangolo.com/) - Web 框架
- [Vue.js](https://vuejs.org/) - 前端框架
- [Naive UI](https://www.naiveui.com/) - UI 组件库
- [Loguru](https://github.com/Delgan/loguru) - 日志系统
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) - HTML 解析

## 联系方式

如有问题或建议，请提交 Issue 或 Pull Request。
