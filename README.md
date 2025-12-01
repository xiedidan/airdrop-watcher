# WebMon - 网页监控工具

WebMon是一个基于Playwright的轻量级网页监控工具，通过命令行界面(CLI)提供网页内容变化检测和通知推送功能。

## 🚀 快速开始

### 1. 初始化项目
```bash
python3 webmon.py init
```

### 2. 添加监控任务
```bash
# 基本用法
python3 webmon.py add https://www.example.com

# 指定名称和检测间隔
python3 webmon.py add https://github.com --name "GitHub主页" --interval 30

# 使用CSS选择器精准监控
python3 webmon.py add https://news.ycombinator.com --name "Hacker News" --selector ".titleline"
```

### 3. 查看任务列表
```bash
# 表格格式（默认）
python3 webmon.py list

# JSON格式
python3 webmon.py list --format json

# CSV格式
python3 webmon.py list --format csv
```

## 📋 已实现功能

### ✅ 基础框架
- [x] 项目目录结构
- [x] 依赖管理 (requirements.txt)
- [x] 环境变量配置 (.env.example)
- [x] CLI框架和参数解析
- [x] 命令基类和具体命令实现

### ✅ 核心命令
- [x] `init` - 初始化配置文件和目录结构
- [x] `add` - 添加监控任务
- [x] `list` - 列出所有监控任务

### ✅ 功能特性
- [x] 支持多种输出格式（表格、JSON、CSV）
- [x] 任务配置持久化存储
- [x] 完整的帮助文档
- [x] 日志系统
- [x] 参数验证

## 🛠️ 开发环境设置

### 安装依赖
```bash
pip3 install -r requirements.txt
```

### 安装Playwright浏览器
```bash
playwright install
```

## 📁 项目结构

```
webmon/
├── webmon.py              # 主程序入口
├── requirements.txt       # Python依赖
├── .env.example          # 环境变量模板
├── config/               # 配置文件目录
├── data/                 # 数据存储目录
├── logs/                 # 日志文件目录
└── webmon/               # 核心代码
    ├── cli/               # CLI相关模块
    ├── core/              # 核心逻辑
    ├── config/            # 配置管理
    ├── models/            # 数据模型
    ├── storage/           # 存储管理
    ├── browser/           # 浏览器引擎
    ├── detection/         # 变化检测
    ├── notification/      # 通知推送
    ├── scheduler/         # 任务调度
    ├── utils/             # 工具类
    └── exceptions/        # 异常处理
```

## 🔧 配置说明

### 环境变量 (.env)
- `LOG_LEVEL`: 日志级别 (DEBUG, INFO, WARNING, ERROR)
- `PUSHPLUS_TOKEN`: PushPlus微信推送token
- `TELEGRAM_BOT_TOKEN`: Telegram Bot token
- `DISCORD_WEBHOOK_URL`: Discord Webhook地址
- `FEISHU_WEBHOOK_URL`: 飞书Webhook地址

### 任务配置 (config/config.json)
```json
{
  "tasks": [
    {
      "id": "任务ID",
      "name": "任务名称",
      "url": "监控URL",
      "selector": "CSS选择器",
      "interval": 检测间隔(分钟),
      "timeout": 超时时间(秒),
      "enabled": 是否启用
    }
  ]
}
```

## 🚧 开发计划

### 下一阶段（配置管理系统）
- [ ] 配置管理器基础框架
- [ ] 环境变量配置管理
- [ ] JSON配置文件管理
- [ ] 配置验证和默认值

### 后续阶段
- [ ] 数据模型和存储系统
- [ ] Playwright浏览器引擎集成
- [ ] 变化检测算法
- [ ] 多平台通知推送
- [ ] 完整的CLI命令实现
- [ ] 任务调度和并发管理

## 🤝 贡献指南

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 许可证

此项目采用MIT许可证 - 详情请查看LICENSE文件。