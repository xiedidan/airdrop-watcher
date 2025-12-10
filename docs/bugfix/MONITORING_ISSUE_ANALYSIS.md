# 监控未触发通知问题分析报告

> **报告日期**: 2025-12-10
> **问题描述**: 用户观察到页面变化，但未收到通知，History也没有记录

---

## 测试结果总结

### 1. 本地测试结果

#### 测试场景 1: 动态内容页面（每次访问计数变化）
- **服务器**: http://localhost:8001
- **第一次检测**: ✅ 正确检测到变化，发送Discord通知，保存历史记录
- **第二次检测**: ✅ 正确检测到变化（计数器从2变为3），发送通知，保存记录

#### 测试场景 2: 稳定内容页面（内容不变）
- **服务器**: http://localhost:8002
- **CSS选择器**: `.monitored-content`
- **第一次检测**: ✅ 首次检测报告变化（content_missing），发送通知，保存历史
- **第二次检测**: ✅ 正确识别内容未变化，**没有**发送通知，保存历史

#### 测试场景 3: 用户实际任务
- **URL**: https://bian.sqdxw.top/
- **CSS选择器**: `.table-responsive`
- **检测结果**: ✅ 正常执行，变化: False（内容未变化），未发送通知

**结论**: 系统核心功能完全正常！

---

## 问题原因分析

### 用户问题可能的原因

#### 原因 1: 监控服务未运行 ⭐⭐⭐⭐⭐ (最可能)
**现象**:
- 用户看到页面变化
- 但没有收到通知
- History没有新记录

**解释**:
查看用户任务配置：
```json
{
  "id": "1b77c6d2",
  "name": "币安Alpha活动",
  "last_check": "2025-12-08T17:15:43",  // 最后检查时间是2天前！
  "interval": 10  // 10分钟间隔
}
```

如果监控服务没有运行，任务不会自动执行，自然不会发送通知和保存历史。

**验证方法**:
```bash
# 检查监控服务是否在运行
python3 webmon.py status

# 如果服务未运行，启动它
python3 webmon.py start
```

#### 原因 2: CSS选择器选中的内容没有变化 ⭐⭐⭐⭐
**现象**:
- 页面其他部分变化了
- 但`.table-responsive`选择器选中的表格内容没有变化
- 系统正确判断"未变化"，不发送通知

**解释**:
用户可能看到页面的广告、时间戳、计数器等变化了，但实际监控的表格数据没有变化。

**验证方法**:
```bash
# 移除选择器，监控整个页面
python3 webmon.py edit 1b77c6d2 --selector "" --force

# 或者使用开发者工具检查.table-responsive的实际内容
```

#### 原因 3: 检测间隔设置问题 ⭐⭐⭐
**现象**:
- 页面在两次检测之间变化后又变回去了
- 或者间隔太长，错过了短暂的变化

**当前配置**:
- 间隔: 10分钟

**建议**:
```bash
# 缩短检测间隔到1分钟进行测试
python3 webmon.py edit 1b77c6d2 --interval 1 --force
```

#### 原因 4: Discord配置问题 ⭐⭐
**现象**:
- 检测到变化
- 但Discord通知发送失败

**检查日志**:
```bash
tail -100 logs/webmon.log | grep "discord"
```

查找是否有：
- `Discord平台未配置webhook_url`
- `Discord通知发送失败`
- 网络代理问题

#### 原因 5: 浏览器引擎问题 ⭐
**现象**:
- 页面加载失败
- 或者加载超时

**检查方法**:
```bash
# 手动执行任务查看详细日志
python3 webmon.py start --task 1b77c6d2
```

---

## 诊断步骤

### 第一步: 检查服务状态
```bash
python3 webmon.py status
```

**预期输出**:
```
监控服务状态: 运行中
运行时间: XXX
正在运行的任务: X/15
```

如果显示"未运行"，执行：
```bash
python3 webmon.py start
```

### 第二步: 检查任务状态
```bash
python3 webmon.py list
```

**检查项**:
- 任务是否启用 (启用列应该是"是")
- 最后检查时间是否最近更新

### 第三步: 手动执行任务
```bash
python3 webmon.py start --task 1b77c6d2
```

**观察**:
- 是否成功获取页面内容
- 是否检测到变化
- 是否发送通知
- 是否有错误信息

### 第四步: 检查历史记录
```bash
python3 webmon.py history 1b77c6d2 --limit 10
```

**检查项**:
- 是否有新的检测记录
- 最近一次检测的时间
- 是否有变化标记

### 第五步: 检查日志
```bash
# 查看最近的日志
tail -100 logs/webmon.log

# 查看Discord通知相关日志
grep "discord" logs/webmon.log | tail -20

# 查看变化检测相关日志
grep "检测" logs/webmon.log | tail -20
```

---

## 解决方案

### 方案 1: 确保监控服务运行
```bash
# 启动服务（前台模式，可以看到实时日志）
python3 webmon.py start

# 或者以守护进程模式运行（后台）
python3 webmon.py start --daemon
```

### 方案 2: 调整监控配置
```bash
# 移除CSS选择器，监控整个页面
python3 webmon.py edit 1b77c6d2 --selector "" --force

# 缩短检测间隔
python3 webmon.py edit 1b77c6d2 --interval 1 --force

# 增加超时时间
python3 webmon.py edit 1b77c6d2 --timeout 60 --force
```

### 方案 3: 测试通知配置
```bash
# 测试Discord通知
python3 webmon.py test --platform discord
```

如果失败，检查`.env`文件：
```bash
cat .env | grep DISCORD
```

确保有：
```
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_TOKEN
```

### 方案 4: 清理并重新测试
```bash
# 1. 停止服务
python3 webmon.py stop

# 2. 清理错误状态
python3 webmon.py edit 1b77c6d2 --enable true --force

# 3. 手动执行一次
python3 webmon.py start --task 1b77c6d2

# 4. 启动自动监控
python3 webmon.py start
```

---

## 测试数据

### 历史记录详情

#### 任务: 1317d8ea (本地测试)
```
第1次: 10:56:01 - 内容: "访问计数: 2" - 变化: True (content_missing)
第2次: 13:27:21 - 内容: "访问计数: 3" - 变化: True (similarity_change)
```

✅ **正常**: 计数器确实变化了，系统正确检测并发送通知

#### 任务: c64d3067 (稳定内容测试)
```
第1次: 14:15:03 - 大小: 441B - 变化: True (content_missing)
第2次: 14:15:25 - 大小: 441B - 变化: False
```

✅ **正常**: 内容未变化，系统正确判断不发送通知

#### 任务: 1b77c6d2 (用户实际任务)
```
最后检查: 2025-12-08T17:15:43 (两天前!)
```

⚠️ **异常**: 最后检查时间是2天前，说明监控服务很可能没有在运行

---

## 建议

### 立即行动
1. 检查监控服务是否在运行
2. 如果没运行，启动服务
3. 观察是否能收到新的通知

### 后续优化
1. 使用`systemd`或`supervisor`管理监控服务，确保自动启动
2. 添加健康检查脚本，定期检查服务状态
3. 配置告警，当服务停止时发送通知

### 调试命令
```bash
# 完整的诊断流程
python3 webmon.py status
python3 webmon.py list
python3 webmon.py history 1b77c6d2 --limit 5
python3 webmon.py start --task 1b77c6d2
tail -50 logs/webmon.log
```

---

## 结论

经过完整测试，系统的变化检测、通知发送、历史记录功能**完全正常**。

用户问题最可能的原因是：
1. **监控服务没有在运行**（最后检查时间是2天前）
2. CSS选择器选中的内容实际上没有变化

**建议用户**:
1. 确认监控服务正在运行: `python3 webmon.py status`
2. 如果没运行，启动服务: `python3 webmon.py start`
3. 观察是否能收到新的通知

如果服务正在运行但仍未收到通知，考虑移除CSS选择器或缩短检测间隔进行测试。
