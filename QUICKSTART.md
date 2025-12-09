# WebMon 快速开始指南

本指南将帮助你在 5 分钟内完成 WebMon 的安装和配置，并开始监控你的第一个网页。

## 前置要求

- Python 3.8 或更高版本
- pip3
- 稳定的网络连接

## 步骤 1: 克隆项目

```bash
cd /path/to/your/projects
git clone <your-repo-url>
cd airdrop-watcher
```

## 步骤 2: 安装依赖

```bash
# 安装 Python 依赖
pip3 install -r requirements.txt

# 安装 Playwright 浏览器（约 300MB）
playwright install chromium
```

## 步骤 3: 初始化配置

```bash
python3 webmon.py init
```

这将创建：
- `config/config.json` - 主配置文件
- `.env` - 环境变量配置文件
- `data/` - 数据存储目录
- `logs/` - 日志目录

## 步骤 4: 配置 Discord 通知（推荐）

### 4.1 创建 Discord Webhook

1. 打开你的 Discord 服务器
2. 右键点击要接收通知的频道
3. 选择 "编辑频道" → "整合"
4. 点击 "创建 Webhook"
5. 复制 Webhook URL

### 4.2 配置环境变量

编辑 `.env` 文件：

```bash
# Discord Webhook
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_TOKEN

# 代理设置（如果需要）
HTTP_PROXY=http://127.0.0.1:10808
HTTPS_PROXY=http://127.0.0.1:10808
```

### 4.3 启用 Discord 平台

编辑 `config/config.json`，确保以下配置存在：

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

## 步骤 5: 测试通知

```bash
python3 webmon.py test --platform discord
```

如果配置正确，你会在 Discord 频道收到测试消息。

## 步骤 6: 添加第一个监控任务

```bash
# 监控一个简单的网站
python3 webmon.py add https://www.example.com \
  --name "示例网站" \
  --interval 300
```

参数说明：
- `--name`: 任务名称
- `--interval`: 检测间隔（秒）

## 步骤 7: 启动监控服务

```bash
python3 webmon.py start
```

服务将在前台运行，你会看到实时日志输出。

## 步骤 8: 查看监控状态

打开新终端窗口：

```bash
# 查看任务列表
python3 webmon.py list

# 查看服务状态
python3 webmon.py status
```

## 步骤 9: 触发测试通知（可选）

如果你想快速测试通知功能，可以使用项目提供的测试服务器：

```bash
# 启动测试服务器
python3 test_server.py &

# 添加本地测试任务
python3 webmon.py add http://localhost:8001 \
  --name "本地测试" \
  --interval 60

# 触发网页变化
curl http://localhost:8001

# 等待约 60 秒，应该收到 Discord 通知
```

## 常见问题

### Q: 浏览器启动失败

```bash
# 重新安装浏览器
playwright install chromium

# 安装系统依赖（Linux）
playwright install-deps
```

### Q: Discord 通知未收到

检查配置：

```bash
# 验证环境变量
cat .env | grep DISCORD

# 测试通知
python3 webmon.py test --platform discord

# 查看日志
tail -f logs/webmon.log
```

### Q: 代理问题

如果你在中国大陆，可能需要配置代理：

```bash
# 在 .env 文件中添加
HTTP_PROXY=http://127.0.0.1:你的代理端口
HTTPS_PROXY=http://127.0.0.1:你的代理端口
```

### Q: 如何停止服务

在运行 `python3 webmon.py start` 的终端按 `Ctrl+C`

或者：

```bash
python3 webmon.py stop
```

## 下一步

恭喜！你已经成功配置了 WebMon。接下来你可以：

1. **添加更多监控任务**
   ```bash
   python3 webmon.py add https://news.ycombinator.com \
     --name "Hacker News" \
     --selector ".titleline" \
     --interval 600
   ```

2. **配置其他通知平台**
   - Telegram
   - 飞书
   - PushPlus

3. **优化配置**
   - 调整检测间隔
   - 使用 CSS 选择器精准监控
   - 优化并发数和资源使用

4. **查看完整文档**
   - [README.md](README.md) - 完整功能文档
   - [docs/scheduler_config.md](docs/scheduler_config.md) - 调度器配置
   - [docs/logging_config_guide.md](docs/logging_config_guide.md) - 日志配置

## 使用技巧

### 使用 CSS 选择器

CSS 选择器可以让你只监控页面的特定部分，减少误报：

```bash
# 只监控标题
python3 webmon.py add https://example.com \
  --selector "h1.title"

# 只监控价格
python3 webmon.py add https://shop.com/product \
  --selector ".price-value"
```

### 调整检测间隔

根据网页更新频率调整间隔：

```bash
# 新闻网站 - 5 分钟
python3 webmon.py add https://news.site.com --interval 300

# 价格监控 - 30 分钟
python3 webmon.py add https://price.site.com --interval 1800

# 慢更新网站 - 1 小时
python3 webmon.py add https://slow.site.com --interval 3600
```

### 查看变化历史

```bash
# 查看最近 20 条记录
python3 webmon.py history <task_id> --limit 20

# 只显示有变化的记录
python3 webmon.py history <task_id> --changes-only
```

## 获得帮助

- 查看命令帮助：`python3 webmon.py <command> --help`
- 查看日志：`tail -f logs/webmon.log`
- 提交问题：[GitHub Issues](your-repo-url/issues)

---

现在开始享受自动化的网页监控吧！
