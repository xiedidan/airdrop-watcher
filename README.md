# WebMon - 网页监控工具

WebMon 是一个功能强大的网页监控工具，基于 Playwright 浏览器引擎，支持自动检测网页变化并通过多个平台发送通知。

## 特性

- 基于 Playwright 的无头浏览器，支持 JavaScript 渲染
- 智能变化检测算法（哈希对比、相似度分析）
- 多平台通知支持（Discord、Telegram、飞书、PushPlus）
- 灵活的任务调度系统，支持自定义检测间隔
- CSS选择器支持，精准监控页面特定区域
- 完整的历史记录和变化追踪
- 代理支持，适应各种网络环境
- 详细的日志系统
- 命令行界面，易于使用和自动化

## 快速开始

### 1. 安装依赖

```bash
# 安装 Python 依赖
pip3 install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium
```

### 2. 初始化配置

```bash
python3 webmon.py init
```

这将创建必要的配置文件和目录：
- `config/config.json` - 主配置文件
- `.env` - 环境变量配置
- `data/` - 数据存储目录
- `logs/` - 日志文件目录

### 3. 配置通知平台

编辑 `.env` 文件，添加你的通知平台凭据：

```bash
# Discord Webhook
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_URL

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# 飞书 Webhook
FEISHU_WEBHOOK_URL=your_webhook_url
FEISHU_SECRET=your_secret

# PushPlus
PUSHPLUS_TOKEN=your_token

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

### 4. 添加监控任务

```bash
# 基本用法
python3 webmon.py add https://www.example.com

# 指定名称和检测间隔（秒）
python3 webmon.py add https://github.com --name "GitHub主页" --interval 300

# 使用 CSS 选择器精准监控
python3 webmon.py add https://news.ycombinator.com \
  --name "Hacker News" \
  --selector ".titleline" \
  --interval 600

# 设置超时时间
python3 webmon.py add https://slow-site.com \
  --timeout 30000
```

### 5. 启动监控服务

```bash
# 前台运行
python3 webmon.py start

# 查看服务状态
python3 webmon.py status
```

### 6. 管理任务

```bash
# 列出所有任务
python3 webmon.py list

# 查看详细信息（JSON 格式）
python3 webmon.py list --format json

# 删除任务
python3 webmon.py remove <task_id>

# 查看变化历史
python3 webmon.py history <task_id>
```

### 7. 测试通知

```bash
# 测试所有配置的平台
python3 webmon.py test

# 测试特定平台
python3 webmon.py test --platform discord
```

## 命令详解

### init - 初始化配置

```bash
python3 webmon.py init [--force]
```

创建配置文件和目录结构。使用 `--force` 覆盖现有配置。

### add - 添加监控任务

```bash
python3 webmon.py add <url> [选项]
```

选项：
- `--name, -n`: 任务名称（默认使用域名）
- `--selector, -s`: CSS 选择器，监控页面特定区域
- `--interval, -i`: 检测间隔（秒，默认 60）
- `--timeout, -t`: 超时时间（毫秒，默认 30000）

### remove - 删除任务

```bash
python3 webmon.py remove <task_id>
```

### list - 列出任务

```bash
python3 webmon.py list [--format FORMAT] [--filter STATUS]
```

选项：
- `--format`: 输出格式（table/json/csv，默认 table）
- `--filter`: 按状态过滤（all/enabled/disabled/error）

### start - 启动服务

```bash
python3 webmon.py start [--daemon]
```

选项：
- `--daemon, -d`: 后台运行模式

### stop - 停止服务

```bash
python3 webmon.py stop
```

### status - 查看状态

```bash
python3 webmon.py status [--verbose]
```

显示服务运行状态、任务统计和资源使用情况。

### test - 测试通知

```bash
python3 webmon.py test [--platform PLATFORM]
```

测试通知平台配置是否正确。

### history - 查看历史

```bash
python3 webmon.py history <task_id> [--limit N] [--changes-only]
```

选项：
- `--limit, -l`: 显示最近 N 条记录（默认 10）
- `--changes-only`: 只显示有变化的记录

## 配置说明

### 环境变量 (.env)

| 变量 | 说明 | 示例 |
|------|------|------|
| LOG_LEVEL | 日志级别 | INFO |
| DISCORD_WEBHOOK_URL | Discord Webhook URL | https://discord.com/api/webhooks/... |
| TELEGRAM_BOT_TOKEN | Telegram Bot Token | 123456:ABC-DEF... |
| TELEGRAM_CHAT_ID | Telegram Chat ID | 123456789 |
| FEISHU_WEBHOOK_URL | 飞书 Webhook URL | https://open.feishu.cn/... |
| PUSHPLUS_TOKEN | PushPlus Token | xxx |
| HTTP_PROXY | HTTP 代理 | http://127.0.0.1:10808 |
| HTTPS_PROXY | HTTPS 代理 | http://127.0.0.1:10808 |

### 主配置文件 (config/config.json)

```json
{
  "version": "1.0.0",
  "tasks": [],
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
  "scheduler": {
    "performance": {
      "max_concurrent_tasks": 15,
      "max_browser_resources": 8,
      "scheduler_loop_interval": 0.2
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

### 调度器配置

调度器支持高级配置，可以优化性能和资源使用：

```json
{
  "scheduler": {
    "performance": {
      "max_concurrent_tasks": 15,        // 最大并发任务数
      "max_browser_resources": 8,        // 最大浏览器资源数
      "scheduler_loop_interval": 0.2     // 调度循环间隔（秒）
    },
    "retry": {
      "retry_attempts": 5,                // 重试次数
      "retry_delay": 120                  // 重试延迟（秒）
    }
  }
}
```

详细文档：[docs/scheduler_config.md](docs/scheduler_config.md)

### 日志配置

日志系统支持灵活配置：

```json
{
  "logging": {
    "level": "INFO",                      // 日志级别
    "log_dir": "logs",                    // 日志目录
    "rotation": {
      "type": "size",                     // 轮转类型: size/time
      "interval": 7,                      // 时间轮转间隔（天）
      "max_size": 5242880,                // 大小轮转阈值（字节，5MB）
      "backup_count": 3                   // 保留备份数量
    },
    "format": {
      "console": "{time:HH:mm:ss} | {level} | {message}",
      "file": "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name} | {message}"
    },
    "compression": false,                 // 是否压缩旧日志
    "async_mode": false                   // 是否异步写入
  }
}
```

详细文档：[docs/logging_config_guide.md](docs/logging_config_guide.md)

## 项目结构

```
airdrop-watcher/
├── webmon.py                  # 主程序入口
├── requirements.txt           # Python 依赖
├── .env                       # 环境变量配置
├── config/
│   └── config.json            # 主配置文件
├── data/
│   ├── history.json           # 变化历史
│   └── tasks.db               # 任务数据库
├── logs/                      # 日志文件
├── docs/                      # 文档
└── webmon/                    # 核心代码
    ├── cli/                   # CLI 模块
    │   ├── argument_parser.py # 参数解析
    │   └── commands/          # 命令实现
    ├── config/                # 配置管理
    │   ├── config_manager.py  # 配置管理器
    │   ├── env_config.py      # 环境变量
    │   └── json_config.py     # JSON 配置
    ├── models/                # 数据模型
    │   ├── task.py            # 任务模型
    │   ├── check_result.py    # 检测结果
    │   └── change_details.py  # 变化详情
    ├── storage/               # 存储管理
    │   ├── task_storage.py    # 任务存储
    │   └── history_storage.py # 历史存储
    ├── browser/               # 浏览器引擎
    │   ├── browser_engine.py  # 浏览器管理
    │   ├── resource_manager.py# 资源管理
    │   └── network_config.py  # 网络配置
    ├── detection/             # 变化检测
    │   ├── change_detector.py # 检测器
    │   ├── hash_detector.py   # 哈希检测
    │   └── similarity_detector.py # 相似度检测
    ├── notification/          # 通知推送
    │   ├── service.py         # 通知服务
    │   ├── base_platform.py   # 平台基类
    │   └── platforms/         # 各平台实现
    │       ├── discord_platform.py
    │       ├── telegram_platform.py
    │       ├── feishu_platform.py
    │       └── pushplus_platform.py
    ├── scheduler/             # 任务调度
    │   ├── task_scheduler.py  # 调度器
    │   ├── execution_engine.py# 执行引擎
    │   ├── job_queue.py       # 任务队列
    │   └── priority_manager.py# 优先级管理
    └── utils/                 # 工具类
        ├── logger.py          # 日志工具
        └── validators.py      # 验证工具
```

## 使用示例

### 监控新闻网站

```bash
# 监控 Hacker News 首页标题
python3 webmon.py add https://news.ycombinator.com \
  --name "HN首页" \
  --selector ".titleline" \
  --interval 300

# 监控 Reddit 热门
python3 webmon.py add https://www.reddit.com/r/programming \
  --name "Reddit编程" \
  --selector "div[data-testid='post-container']" \
  --interval 600
```

### 监控价格变化

```bash
# 监控产品价格
python3 webmon.py add https://www.amazon.com/dp/PRODUCT_ID \
  --name "iPhone价格" \
  --selector ".a-price-whole" \
  --interval 1800
```

### 监控 GitHub 仓库

```bash
# 监控 Star 数
python3 webmon.py add https://github.com/user/repo \
  --name "项目Star数" \
  --selector "#repo-stars-counter-star" \
  --interval 3600
```

### 本地测试

项目包含测试脚本，可以快速验证功能：

```bash
# 启动测试服务器（监听 8001 端口）
python3 test_server.py &

# 添加本地测试任务
python3 webmon.py add http://localhost:8001 \
  --name "本地测试" \
  --interval 60

# 启动监控
python3 webmon.py start

# 触发变化（访问测试页面，计数器会增加）
curl http://localhost:8001

# 查看 Discord 频道，应该收到变化通知
```

## 已实现功能

### CLI 命令系统
- [x] init - 初始化配置
- [x] add - 添加监控任务
- [x] remove - 删除任务
- [x] list - 列出任务
- [x] start - 启动服务
- [x] stop - 停止服务
- [x] status - 查看状态
- [x] test - 测试通知
- [x] history - 查看历史

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

### 测试状态
- [x] Discord 通知 - 已测试通过 ✅
- [x] 本地测试服务器 - 正常运行 ✅
- [x] 变化检测 - 功能正常 ✅
- [x] 任务调度 - 稳定运行 ✅
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
python3 webmon.py test --platform discord

# 检查环境变量
cat .env | grep DISCORD

# 查看日志
tail -f logs/webmon.log
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

### 任务不执行

```bash
# 查看任务状态
python3 webmon.py list

# 检查服务状态
python3 webmon.py status

# 查看日志
tail -f logs/webmon.log
```

## 性能优化

### 调整并发数

编辑 `config/config.json`：

```json
{
  "scheduler": {
    "performance": {
      "max_concurrent_tasks": 20,
      "max_browser_resources": 10
    }
  }
}
```

### 优化检测间隔

```bash
# 对于不常变化的页面，增加检测间隔
python3 webmon.py add https://stable-site.com --interval 3600

# 对于快速变化的页面，减少检测间隔
python3 webmon.py add https://live-site.com --interval 30
```

### 使用选择器

使用 CSS 选择器只监控页面特定部分，减少误报：

```bash
python3 webmon.py add https://example.com \
  --selector "#main-content"
```

## 开发文档

- [设计文档](docs/design.md)
- [调度器配置](docs/scheduler_config.md)
- [日志配置指南](docs/logging_config_guide.md)
- [任务清单](docs/tasks.md)

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
- [Loguru](https://github.com/Delgan/loguru) - 日志系统
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) - HTML 解析

## 联系方式

如有问题或建议，请提交 Issue 或 Pull Request。
