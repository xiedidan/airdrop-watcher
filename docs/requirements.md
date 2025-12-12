# WebMon - 网页监控工具需求文档

## 1. 项目概述

WebMon是一个基于Playwright的轻量级网页监控工具，通过命令行界面(CLI)提供网页内容变化检测和通知推送功能。工具采用Python脚本形式，配置通过.env文件管理，支持多种推送平台。

## 2. 目标用户

- **个人用户**: 监控感兴趣网站的更新（新闻、博客、论坛等）
- **技术爱好者**: 监控开源项目、技术文档、API文档等
- **小型企业**: 监控竞品动态、行业资讯、价格变化等
- **开发者**: 作为其他系统的监控组件集成使用

## 3. 功能需求

### 3.1 核心功能

#### 3.1.1 网页监控
- ✅ 支持静态网页内容监控
- ✅ 支持JavaScript动态渲染页面监控
- ✅ 支持指定CSS选择器精准监控
- ✅ 支持多个URL同时监控
- ✅ 支持自定义检测频率
- ✅ 支持页面加载超时设置

#### 3.1.2 变化检测
- ✅ 基于内容哈希的基础变化检测
- ✅ 基于文本相似度的智能变化检测（可选）
- ✅ 支持忽略微小变化（可配置相似度阈值）
- ✅ 支持结构化内容提取（标题、链接、文本等）
- ✅ 支持变化历史记录

#### 3.1.3 AI智能分析（新增）
- ⚠️ 支持AI模型分析变化内容
- ⚠️ 支持DeepSeek R1模型（推荐）
- ⚠️ 支持OpenAI兼容API（如OpenAI、Claude、通义千问等）
- ⚠️ 系统提示词：所有任务通用，定义AI角色和输出格式
- ⚠️ 用户提示词模板：支持占位符替换
  - `{task_name}` - 任务名称
  - `{url}` - 监控URL
  - `{description}` - 任务描述
  - `{changes}` - 变动内容
  - `{old_content}` - 旧内容摘要
  - `{new_content}` - 新内容摘要
- ⚠️ 将AI分析结果加入推送消息
- ⚠️ 支持分析失败降级（失败时使用原始变化内容）

#### 3.1.4 通知推送
- ✅ 支持多平台同时推送
- ✅ 支持PushPlus（微信推送）
- ✅ 支持Telegram Bot推送
- ✅ 支持Discord Webhook推送
- ✅ 支持飞书Webhook推送
- ✅ 支持推送内容模板自定义

### 3.2 CLI功能

#### 3.2.1 命令结构
```bash
webmon [命令] [选项]
```

#### 3.2.2 核心命令
- `init` - 初始化配置文件和.env文件
- `add` - 添加监控任务
- `remove` - 删除监控任务
- `list` - 列出所有监控任务
- `start` - 启动监控服务
- `stop` - 停止监控服务
- `status` - 查看监控状态
- `test` - 测试推送通知
- `history` - 查看变化历史

#### 3.2.3 命令详情

##### init命令
```bash
webmon init [--force]
```
- 创建默认配置文件 `config.json`
- 创建环境变量文件 `.env`
- `--force` 选项强制覆盖已有文件

##### add命令
```bash
webmon add <url> [--name <name>] [--selector <selector>] [--interval <seconds>] [--description <description>]
```
- 添加新的监控任务
- 支持自定义任务名称
- 支持CSS选择器精准监控
- 支持自定义检测间隔
- 支持任务描述（用于AI分析时的上下文）

##### list命令
```bash
webmon list [--format <format>]
```
- 列出所有监控任务
- 支持多种输出格式（table, json, csv）

##### start命令
```bash
webmon start [--daemon] [--log-level <level>]
```
- 启动监控服务
- 支持后台守护进程模式
- 支持日志级别设置

### 3.3 配置管理

#### 3.3.1 环境变量 (.env)
```bash
# 推送平台配置
PUSHPLUS_TOKEN=your_pushplus_token
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
DISCORD_WEBHOOK_URL=your_discord_webhook_url
FEISHU_WEBHOOK_URL=your_feishu_webhook_url

# AI分析配置（新增）
AI_API_URL=https://api.deepseek.com/v1
AI_API_KEY=your_deepseek_api_key
AI_MODEL=deepseek-reasoner
AI_MAX_TOKENS=2048
AI_TEMPERATURE=0.7
AI_TIMEOUT=60
AI_ENABLED=true

# 监控配置
DEFAULT_INTERVAL=300
DEFAULT_TIMEOUT=30000
MAX_RETRIES=3
LOG_LEVEL=INFO

# 高级配置
SIMILARITY_THRESHOLD=0.85
ENABLE_SMART_DETECTION=true
BROWSER_HEADLESS=true
```

#### 3.3.2 配置文件 (config.json)
```json
{
  "monitoring": {
    "default_interval": 300,
    "default_timeout": 30000,
    "max_retries": 3,
    "browser_headless": true
  },
  "detection": {
    "enable_smart_detection": true,
    "similarity_threshold": 0.85,
    "ignore_selectors": [".advertisement", ".cookie-banner"]
  },
  "ai": {
    "enabled": true,
    "api_url": "${AI_API_URL}",
    "api_key": "${AI_API_KEY}",
    "model": "deepseek-reasoner",
    "max_tokens": 2048,
    "temperature": 0.7,
    "timeout": 60,
    "system_prompt": "你是一个专业的网页内容分析助手。你的任务是分析网页变化内容，提取用户关注的关键信息，并用简洁的自然语言总结变化要点。",
    "user_prompt_template": "任务名称：{task_name}\n监控URL：{url}\n任务描述：{description}\n\n变动内容：\n{changes}\n\n请分析以上变动，提取关键更新信息，用简洁的语言总结主要变化。"
  },
  "notification": {
    "platforms": ["pushplus"],
    "template": "🎯 {title}\n📍 {url}\n⏰ {timestamp}\n📝 {changes}\n\n🤖 AI分析：\n{ai_summary}",
    "rate_limit": 60
  },
  "tasks": [
    {
      "id": "task_001",
      "url": "https://example.com",
      "name": "示例任务",
      "description": "监控示例网站的更新，关注价格变化和新公告",
      "selectors": [".content"],
      "interval": 300,
      "enabled": true
    }
  ]
}
```

### 3.4 数据存储

#### 3.4.1 任务配置存储
- 存储位置: `config.json`
- 存储内容: 监控任务列表、配置参数
- 备份机制: 修改前自动备份

#### 3.4.2 变化历史存储
- 存储位置: `data/history.json`
- 存储内容: 每次检测的结果、变化详情、时间戳
- 清理机制: 支持按时间或数量自动清理

#### 3.4.3 日志存储
- 存储位置: `logs/webmon.log`
- 日志级别: DEBUG, INFO, WARNING, ERROR
- 轮转机制: 按日期和大小自动轮转

## 4. 非功能需求

### 4.1 性能要求
- 单个页面检测时间 < 30秒
- 支持并发监控任务 ≥ 10个
- 内存占用 < 500MB（10个任务）
- CPU占用 < 10%（空闲时）

### 4.2 可靠性要求
- 异常恢复时间 < 60秒
- 数据丢失率 = 0%
- 服务可用性 > 99%
- 网络异常自动重试

### 4.3 易用性要求
- 安装步骤 ≤ 5步
- 配置复杂度 ≤ 中等
- 错误提示清晰明确
- 帮助文档完整

### 4.4 兼容性要求
- Python版本: 3.7+
- 操作系统: Windows, macOS, Linux
- 浏览器: Chromium (Playwright自动管理)

## 5. 安全需求

### 5.1 数据安全
- 敏感信息（token等）仅存储在.env文件
- 支持配置文件加密（可选）
- 日志中不记录敏感信息

### 5.2 网络安全
- 支持代理配置
- 支持自定义请求头
- 支持SSL证书验证
- 防止DDoS（请求频率限制）

### 5.3 隐私保护
- 本地存储优先
- 最小数据收集原则
- 用户数据完全可控

## 6. 扩展需求

### 6.1 插件系统
- 支持自定义检测算法
- 支持自定义推送平台
- 支持数据导出格式扩展

### 6.2 API接口
- RESTful API（未来版本）
- WebSocket实时通知（未来版本）
- 第三方集成接口（未来版本）

### 6.3 高级功能
- 机器学习变化检测（未来版本）
- 图像内容监控（未来版本）
- PDF文件监控（未来版本）

## 7. 约束条件

### 7.1 技术约束
- 必须使用Playwright作为浏览器引擎
- 必须使用Python开发
- 必须支持CLI交互
- 必须支持.env配置

### 7.2 资源约束
- 单文件部署优先
- 最小外部依赖
- 内存使用优化
- 网络带宽优化

### 7.3 法律约束
- 遵守目标网站的robots.txt
- 遵守相关法律法规
- 不用于恶意监控
- 尊重网站服务条款

## 8. 验收标准

### 8.1 功能验收
- ✅ 所有CLI命令正常工作
- ✅ 监控任务准确检测变化
- ✅ 通知推送到所有配置平台
- ✅ 配置文件正确读写
- ✅ 历史记录完整存储

### 8.2 性能验收
- ✅ 页面检测时间 < 30秒
- ✅ 并发任务支持 ≥ 10个
- ✅ 资源使用在合理范围
- ✅ 长时间运行稳定

### 8.3 用户体验验收
- ✅ 安装配置简单明了
- ✅ 错误提示友好易懂
- ✅ 帮助文档完整准确
- ✅ 界面输出清晰美观

## 9. 项目交付物

### 9.1 代码交付
- `webmon.py` - 主程序文件
- `requirements.txt` - 依赖列表
- `.env.example` - 环境变量示例
- `config.json.example` - 配置文件示例

### 9.2 文档交付
- `README.md` - 项目说明文档
- `docs/installation.md` - 安装指南
- `docs/usage.md` - 使用手册
- `docs/configuration.md` - 配置说明

### 9.3 测试交付
- `tests/test_monitor.py` - 监控功能测试
- `tests/test_notification.py` - 推送功能测试
- `tests/test_cli.py` - CLI功能测试

## 10. 里程碑计划

### 第一阶段（核心功能）
- [ ] CLI框架搭建
- [ ] 基础监控功能
- [ ] 简单变化检测
- [ ] PushPlus推送集成

### 第二阶段（功能完善）
- [ ] 多平台推送支持
- [ ] 智能变化检测
- [ ] 配置文件管理
- [ ] 历史记录功能

### 第三阶段（体验优化）
- [ ] 守护进程模式
- [ ] 日志系统完善
- [ ] 错误处理优化
- [ ] 性能优化

### 第四阶段（高级功能）
- [ ] 并发监控优化
- [ ] 反检测增强
- [ ] 插件系统
- [ ] API接口

## 11. 风险评估

### 11.1 技术风险
- Playwright浏览器兼容性问题
- 目标网站结构变化影响
- 反爬虫机制升级

### 11.2 项目风险
- 开发时间超出预期
- 功能复杂度增加
- 用户需求变更

### 11.3 缓解措施
- 充分的技术调研
- 模块化开发方式
- 定期用户反馈收集

---

**文档版本**: v1.0
**最后更新**: 2024年
**维护者**: WebMon开发团队