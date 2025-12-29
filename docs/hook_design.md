# 页面差异事件自定义触发机制设计文档

> **版本**: 1.0 (草稿)
> **任务编号**: #097
> **作者**: Claude
> **日期**: 2025-12-29
> **状态**: 待审批

---

## 1. 概述

### 1.1 背景

当前 WebMon 系统在检测到页面变化后，会自动触发通知服务发送消息到配置的推送平台（如 Discord、PushPlus 等）。然而，用户可能有更复杂的自动化需求：

- 检测到特定网页变化后，自动执行交易脚本
- 变化触发后，调用自定义脚本更新数据库
- 在通知前执行数据预处理，丰富通知内容
- 集成第三方系统或服务

### 1.2 目标

设计一套事件钩子（Hook）机制，允许用户配置自定义 Shell 或 Python 脚本，在页面变化检测后自动执行。

### 1.3 核心需求

1. **灵活配置**: 支持全局和任务级别的 Hook 配置
2. **多触发时机**: 支持通知前/后多个触发点
3. **安全可控**: 脚本执行需有超时控制和权限限制
4. **信息传递**: 能将变化信息传递给脚本
5. **执行结果反馈**: 记录脚本执行日志和结果

---

## 2. 系统架构

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                         TaskScheduler                                │
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐   │
│  │ ChangeDetector│ -> │  HookManager │ -> │ NotificationService │   │
│  └──────────────┘    └──────────────┘    └──────────────────────┘   │
│                              │                                       │
│                              v                                       │
│                      ┌──────────────┐                                │
│                      │ HookExecutor │                                │
│                      └──────────────┘                                │
│                              │                                       │
│              ┌───────────────┼───────────────┐                       │
│              v               v               v                       │
│       ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│       │Shell脚本 │    │Python脚本│    │  其他    │                  │
│       └──────────┘    └──────────┘    └──────────┘                  │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 核心组件

| 组件 | 职责 |
|------|------|
| **HookManager** | Hook 配置管理、触发点协调、执行调度 |
| **HookExecutor** | 实际执行脚本，管理超时和错误处理 |
| **HookConfig** | Hook 配置数据模型 |
| **HookResult** | 执行结果数据模型 |

---

## 3. 触发时机设计

### 3.1 触发点定义

定义以下触发时机（按执行顺序）：

| 触发点 | 名称 | 时机 | 典型用途 |
|--------|------|------|----------|
| `on_change_detected` | 变化检测后 | 检测到变化，通知发送前 | 数据预处理、内容过滤 |
| `on_before_notify` | 通知前 | AI分析完成，即将发送通知 | 修改通知内容、条件通知 |
| `on_after_notify` | 通知后 | 通知发送完成后 | 后续操作、日志记录 |
| `on_notify_failed` | 通知失败 | 通知发送失败时 | 备用通知、告警升级 |

### 3.2 执行流程

```
变化检测完成
      │
      v
┌─────────────────────────┐
│  on_change_detected     │ <-- 可中断：返回 skip_notify=true 跳过通知
└─────────────────────────┘
      │
      v
   AI 分析
      │
      v
┌─────────────────────────┐
│  on_before_notify       │ <-- 可修改：可修改通知内容
└─────────────────────────┘
      │
      v
   发送通知
      │
      ├─────── 成功 ──────┐
      │                   v
      │       ┌─────────────────────────┐
      │       │   on_after_notify       │
      │       └─────────────────────────┘
      │
      └─────── 失败 ──────┐
                          v
              ┌─────────────────────────┐
              │   on_notify_failed      │
              └─────────────────────────┘
```

---

## 4. 配置设计

### 4.1 配置层级

支持两个配置层级：

1. **全局配置** (`config.json` 中的 `hooks` 节点)：应用于所有任务
2. **任务级配置** (`task.hooks`)：仅应用于特定任务，优先级高于全局配置

### 4.2 配置格式

#### 4.2.1 全局 Hook 配置

```json
{
  "hooks": {
    "enabled": true,
    "global_hooks": {
      "on_change_detected": [
        {
          "name": "log_all_changes",
          "type": "shell",
          "script": "/path/to/scripts/log_change.sh",
          "enabled": true,
          "timeout": 30,
          "async": true
        }
      ],
      "on_after_notify": [
        {
          "name": "backup_to_db",
          "type": "python",
          "script": "/path/to/scripts/backup.py",
          "enabled": true,
          "timeout": 60,
          "async": true
        }
      ]
    },
    "defaults": {
      "timeout": 30,
      "async": true,
      "max_retries": 0,
      "working_dir": null
    }
  }
}
```

#### 4.2.2 任务级 Hook 配置

```json
{
  "id": "task_123",
  "name": "币安Alpha活动",
  "url": "https://example.com",
  "hooks": {
    "on_change_detected": [
      {
        "name": "binance_analyzer",
        "type": "python",
        "script": "/home/user/scripts/analyze_binance.py",
        "enabled": true,
        "timeout": 60,
        "async": false,
        "args": ["--mode", "detail"]
      }
    ],
    "on_after_notify": [
      {
        "name": "trigger_trade",
        "type": "shell",
        "script": "/home/user/scripts/trade.sh",
        "enabled": true,
        "timeout": 120,
        "async": true,
        "condition": "change_type == 'content_change'"
      }
    ]
  }
}
```

### 4.3 配置字段说明

| 字段 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `name` | string | 是 | - | Hook 名称，用于日志和识别 |
| `type` | string | 是 | - | 脚本类型：`shell` 或 `python` |
| `script` | string | 是 | - | 脚本路径（绝对路径或相对于项目根目录） |
| `enabled` | bool | 否 | true | 是否启用此 Hook |
| `timeout` | int | 否 | 30 | 执行超时时间（秒） |
| `async` | bool | 否 | true | 是否异步执行（不阻塞后续流程） |
| `args` | array | 否 | [] | 额外的命令行参数 |
| `env` | object | 否 | {} | 额外的环境变量 |
| `condition` | string | 否 | null | 执行条件表达式（Python 语法） |
| `working_dir` | string | 否 | 脚本所在目录 | 工作目录 |
| `max_retries` | int | 否 | 0 | 失败时最大重试次数 |

---

## 5. 参数传递设计

### 5.1 传递方式

支持三种参数传递方式（可组合使用）：

| 方式 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **环境变量** | 简单、通用 | 长度限制、特殊字符处理 | 简单信息传递 |
| **命令行参数** | 直观、兼容性好 | 长度限制、需转义 | 简单信息传递 |
| **标准输入 (stdin)** | 无长度限制 | 需脚本支持 | 复杂数据传递 |
| **临时文件** | 无长度限制、可持久化 | 需清理 | 大数据量传递 |

**推荐方案**: 采用**环境变量 + stdin JSON** 组合方式。

### 5.2 环境变量

所有 Hook 脚本执行时都会注入以下环境变量：

#### 5.2.1 任务相关

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `WEBMON_TASK_ID` | 任务 ID | `1b77c6d2` |
| `WEBMON_TASK_NAME` | 任务名称 | `币安Alpha活动` |
| `WEBMON_TASK_URL` | 监控 URL | `https://example.com` |
| `WEBMON_TASK_DESCRIPTION` | 任务描述 | `监控币安Alpha活动...` |

#### 5.2.2 变化相关

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `WEBMON_CHANGE_DETECTED` | 是否检测到变化 | `true` / `false` |
| `WEBMON_CHANGE_TYPE` | 变化类型 | `content_change` |
| `WEBMON_CHANGE_TIME` | 变化检测时间 (ISO 格式) | `2025-12-29T10:30:00` |
| `WEBMON_SIMILARITY` | 相似度百分比 | `85.5` |

#### 5.2.3 执行上下文

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `WEBMON_HOOK_NAME` | 当前 Hook 名称 | `binance_analyzer` |
| `WEBMON_HOOK_TRIGGER` | 触发点 | `on_change_detected` |
| `WEBMON_PROJECT_ROOT` | 项目根目录 | `/home/xd/project/airdrop-watcher` |
| `WEBMON_DATA_DIR` | 数据目录 | `/home/xd/project/airdrop-watcher/data` |

### 5.3 stdin JSON 格式

对于需要传递复杂数据的场景，通过 stdin 传递完整的 JSON 数据：

```json
{
  "trigger": "on_change_detected",
  "timestamp": "2025-12-29T10:30:00+08:00",
  "task": {
    "id": "1b77c6d2",
    "name": "币安Alpha活动",
    "url": "https://example.com",
    "description": "监控币安Alpha活动页面变化"
  },
  "change": {
    "detected": true,
    "type": "content_change",
    "similarity": 0.855,
    "summary": "检测到内容变化",
    "old_content": "...(截断至2000字符)...",
    "new_content": "...(截断至2000字符)...",
    "diff": "--- old\n+++ new\n@@ -1,3 +1,3 @@\n..."
  },
  "ai_analysis": {
    "enabled": true,
    "summary": "1. 新增项目: XYZ\n2. 更新时间: 12:00 → 14:00",
    "model": "deepseek-reasoner"
  },
  "notification": {
    "platforms": ["discord"],
    "status": "pending"
  }
}
```

### 5.4 脚本示例

#### Shell 脚本示例

```bash
#!/bin/bash
# /home/user/scripts/log_change.sh

echo "Hook triggered: $WEBMON_HOOK_NAME"
echo "Task: $WEBMON_TASK_NAME"
echo "URL: $WEBMON_TASK_URL"
echo "Change detected: $WEBMON_CHANGE_DETECTED"

# 读取 stdin JSON
PAYLOAD=$(cat)
echo "Full payload: $PAYLOAD"

# 使用 jq 解析
CHANGE_TYPE=$(echo "$PAYLOAD" | jq -r '.change.type')
echo "Change type: $CHANGE_TYPE"

# 记录到日志
echo "[$(date)] Task=$WEBMON_TASK_NAME Type=$CHANGE_TYPE" >> /var/log/webmon_hooks.log
```

#### Python 脚本示例

```python
#!/usr/bin/env python3
# /home/user/scripts/analyze_binance.py

import os
import sys
import json

def main():
    # 从环境变量获取基本信息
    task_name = os.environ.get('WEBMON_TASK_NAME')
    task_url = os.environ.get('WEBMON_TASK_URL')
    change_detected = os.environ.get('WEBMON_CHANGE_DETECTED') == 'true'

    print(f"Processing task: {task_name}")

    # 从 stdin 读取完整数据
    payload = json.load(sys.stdin)

    change_info = payload.get('change', {})
    new_content = change_info.get('new_content', '')

    # 自定义分析逻辑
    if '新增项目' in new_content:
        print("发现新项目！")
        # 执行后续操作...

    # 可通过 stdout 返回结果供日志记录
    result = {
        "status": "success",
        "message": "Analysis completed",
        "findings": ["new_project_detected"]
    }
    print(json.dumps(result))

if __name__ == '__main__':
    main()
```

---

## 6. 执行策略

### 6.1 同步 vs 异步执行

| 模式 | 特点 | 适用场景 |
|------|------|----------|
| **同步 (`async: false`)** | 阻塞后续流程，可获取执行结果 | 需要根据脚本结果决定是否继续 |
| **异步 (`async: true`)** | 不阻塞后续流程，后台执行 | 不影响主流程的辅助任务 |

### 6.2 超时控制

- 默认超时: 30 秒
- 最大超时: 300 秒 (5 分钟)
- 超时行为: 终止进程 (SIGTERM)，5秒后强制 SIGKILL

### 6.3 错误处理

| 错误类型 | 处理方式 |
|----------|----------|
| 脚本不存在 | 记录错误日志，跳过此 Hook |
| 权限不足 | 记录错误日志，跳过此 Hook |
| 执行超时 | 终止进程，记录超时日志 |
| 非零退出码 | 记录错误日志，可配置重试 |
| 异常崩溃 | 记录异常日志，继续后续 Hook |

### 6.4 执行顺序

同一触发点的多个 Hook 按配置顺序依次执行：
- 全局 Hook 先于任务级 Hook
- 同一级别内按配置数组顺序执行

---

## 7. 安全策略

### 7.1 脚本路径验证

```python
class ScriptValidator:
    """脚本路径验证器"""

    # 允许的脚本目录（白名单）
    ALLOWED_DIRS = [
        '/home/*/scripts/',
        '/home/*/webmon/hooks/',
        '{PROJECT_ROOT}/scripts/',
        '{PROJECT_ROOT}/hooks/',
    ]

    # 禁止的路径模式（黑名单）
    BLOCKED_PATTERNS = [
        '/etc/',
        '/usr/',
        '/bin/',
        '/sbin/',
        '/../',
        '..',
    ]
```

### 7.2 执行权限控制

1. **脚本必须存在且可执行**: 验证文件存在性和执行权限
2. **不使用 shell 扩展**: 避免命令注入
3. **限制环境变量大小**: 防止缓冲区溢出
4. **用户权限继承**: 脚本以当前 WebMon 进程用户身份运行

### 7.3 资源限制

| 资源 | 限制值 | 说明 |
|------|--------|------|
| CPU 时间 | 300秒 | 防止无限循环 |
| 内存 | 512MB | 防止内存耗尽 |
| 文件描述符 | 256 | 防止资源泄露 |
| 子进程数 | 16 | 防止 fork 炸弹 |

### 7.4 敏感信息保护

- 环境变量中的敏感信息（如 API Key）不会传递给 Hook 脚本
- 日志输出自动过滤敏感数据

---

## 8. 数据模型

### 8.1 HookConfig 模型

```python
@dataclass
class HookConfig:
    """Hook 配置数据模型"""

    name: str                           # Hook 名称
    type: str                           # 脚本类型: shell / python
    script: str                         # 脚本路径
    enabled: bool = True                # 是否启用
    timeout: int = 30                   # 超时时间（秒）
    async_exec: bool = True             # 是否异步执行
    args: List[str] = field(default_factory=list)  # 额外参数
    env: Dict[str, str] = field(default_factory=dict)  # 额外环境变量
    condition: Optional[str] = None     # 执行条件
    working_dir: Optional[str] = None   # 工作目录
    max_retries: int = 0                # 最大重试次数
```

### 8.2 HookResult 模型

```python
@dataclass
class HookResult:
    """Hook 执行结果数据模型"""

    hook_name: str                      # Hook 名称
    trigger: str                        # 触发点
    task_id: str                        # 任务 ID
    success: bool                       # 是否成功
    exit_code: int                      # 退出码
    stdout: str                         # 标准输出
    stderr: str                         # 标准错误
    execution_time: float               # 执行时间（秒）
    timestamp: datetime                 # 执行时间
    error_message: Optional[str] = None # 错误信息
```

### 8.3 Task 模型扩展

在现有 Task 模型中添加 hooks 字段：

```python
@dataclass
class Task:
    # ... 现有字段 ...

    # 新增 Hook 配置字段
    hooks: Dict[str, List[HookConfig]] = field(default_factory=dict)
    #  结构: {"on_change_detected": [...], "on_after_notify": [...]}
```

---

## 9. CLI 命令扩展

### 9.1 Hook 管理命令

```bash
# 列出所有 Hook
python webmon.py hook list

# 列出特定任务的 Hook
python webmon.py hook list --task <task_id>

# 测试 Hook（模拟触发）
python webmon.py hook test <hook_name> --task <task_id> --trigger on_change_detected

# 验证 Hook 配置
python webmon.py hook validate

# 查看 Hook 执行历史
python webmon.py hook history --limit 20

# 启用/禁用 Hook
python webmon.py hook enable <hook_name>
python webmon.py hook disable <hook_name>
```

### 9.2 命令输出示例

```
$ python webmon.py hook list

全局 Hook:
┌─────────────────────┬────────┬─────────────────────────────────┬─────────┬─────────┐
│ 名称                │ 类型   │ 脚本                            │ 触发点  │ 状态    │
├─────────────────────┼────────┼─────────────────────────────────┼─────────┼─────────┤
│ log_all_changes     │ shell  │ /home/user/scripts/log.sh       │ 变化后  │ ✓ 启用  │
│ backup_to_db        │ python │ /home/user/scripts/backup.py    │ 通知后  │ ✓ 启用  │
└─────────────────────┴────────┴─────────────────────────────────┴─────────┴─────────┘

任务级 Hook (任务: 币安Alpha活动):
┌─────────────────────┬────────┬─────────────────────────────────┬─────────┬─────────┐
│ 名称                │ 类型   │ 脚本                            │ 触发点  │ 状态    │
├─────────────────────┼────────┼─────────────────────────────────┼─────────┼─────────┤
│ binance_analyzer    │ python │ /home/user/scripts/analyze.py   │ 变化后  │ ✓ 启用  │
└─────────────────────┴────────┴─────────────────────────────────┴─────────┴─────────┘
```

---

## 10. WebUI 扩展

### 10.1 Settings 页面扩展

在 Settings 页面添加 "Hook 配置" 标签页：

- 全局 Hook 列表管理
- 添加/编辑/删除 Hook
- 测试 Hook 按钮
- 执行日志查看

### 10.2 Tasks 页面扩展

在任务编辑弹窗中添加 "Hook" 标签页：

- 任务级 Hook 列表
- 快速添加 Hook
- 继承全局 Hook 的开关

### 10.3 History 页面扩展

在历史记录详情中显示 Hook 执行信息：

- 触发的 Hook 列表
- 执行状态和耗时
- 输出日志预览

---

## 11. 模块设计

### 11.1 文件结构

```
webmon/
├── hooks/                          # Hook 模块
│   ├── __init__.py
│   ├── config.py                   # HookConfig 数据模型
│   ├── result.py                   # HookResult 数据模型
│   ├── manager.py                  # HookManager 管理类
│   ├── executor.py                 # HookExecutor 执行器
│   ├── validator.py                # 脚本验证器
│   └── triggers.py                 # 触发点定义
├── cli/
│   └── commands/
│       └── hook_command.py         # CLI hook 命令
└── web/
    └── routers/
        └── hooks.py                # WebUI Hook API
```

### 11.2 类设计

```python
class HookManager:
    """Hook 管理器"""

    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.executor = HookExecutor()
        self.validator = ScriptValidator()

    async def trigger(
        self,
        trigger_point: str,
        task: Task,
        context: Dict[str, Any]
    ) -> List[HookResult]:
        """触发指定点的所有 Hook"""
        pass

    def get_hooks_for_trigger(
        self,
        trigger_point: str,
        task_id: Optional[str] = None
    ) -> List[HookConfig]:
        """获取指定触发点的 Hook 列表"""
        pass

    def validate_all_hooks(self) -> Dict[str, List[str]]:
        """验证所有 Hook 配置"""
        pass


class HookExecutor:
    """Hook 执行器"""

    async def execute(
        self,
        hook: HookConfig,
        context: Dict[str, Any]
    ) -> HookResult:
        """执行单个 Hook"""
        pass

    def build_environment(
        self,
        hook: HookConfig,
        context: Dict[str, Any]
    ) -> Dict[str, str]:
        """构建执行环境变量"""
        pass

    def build_stdin_payload(
        self,
        context: Dict[str, Any]
    ) -> str:
        """构建 stdin JSON 数据"""
        pass
```

---

## 12. 实现优先级

### 12.1 Phase 1: 核心功能 (P0)

- [x] HookConfig 数据模型
- [x] HookResult 数据模型
- [x] HookExecutor 基础实现（Shell/Python 支持）
- [x] HookManager 基础实现
- [x] Task 模型扩展（添加 hooks 字段）
- [x] 环境变量传参实现
- [x] stdin JSON 传参实现
- [x] 集成到 TaskScheduler

### 12.2 Phase 2: 安全与健壮性 (P1)

- [ ] 脚本路径验证
- [ ] 超时控制
- [ ] 资源限制
- [ ] 错误处理与重试
- [ ] 日志记录

### 12.3 Phase 3: CLI 与配置 (P2)

- [ ] CLI hook 命令实现
- [ ] config.json 配置格式支持
- [ ] 配置验证

### 12.4 Phase 4: WebUI (P3)

- [ ] Settings 页面 Hook 配置界面
- [ ] Tasks 编辑页 Hook 配置
- [ ] History 页 Hook 执行记录

---

## 13. 风险与缓解

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| 恶意脚本注入 | 中 | 高 | 路径白名单、权限限制 |
| 脚本执行阻塞主流程 | 中 | 中 | 超时控制、异步执行 |
| 资源耗尽 | 低 | 高 | 资源限制、并发控制 |
| 敏感信息泄露 | 低 | 高 | 环境变量过滤、日志脱敏 |

---

## 14. 测试计划

### 14.1 单元测试

- HookConfig 序列化/反序列化
- HookExecutor Shell 脚本执行
- HookExecutor Python 脚本执行
- 环境变量构建
- stdin JSON 构建
- 超时处理

### 14.2 集成测试

- 端到端触发流程
- 全局 + 任务级 Hook 组合
- 错误处理与恢复

### 14.3 安全测试

- 路径遍历攻击
- 命令注入攻击
- 资源耗尽测试

---

## 15. 附录

### 15.1 完整配置示例

```json
{
  "hooks": {
    "enabled": true,
    "global_hooks": {
      "on_change_detected": [
        {
          "name": "global_logger",
          "type": "shell",
          "script": "/home/user/scripts/log_all.sh",
          "enabled": true,
          "timeout": 10,
          "async": true
        }
      ]
    },
    "defaults": {
      "timeout": 30,
      "async": true,
      "max_retries": 0
    }
  },
  "tasks": [
    {
      "id": "1b77c6d2",
      "name": "币安Alpha活动",
      "url": "https://example.com",
      "hooks": {
        "on_change_detected": [
          {
            "name": "binance_analyzer",
            "type": "python",
            "script": "/home/user/scripts/analyze.py",
            "enabled": true,
            "timeout": 60,
            "async": false
          }
        ],
        "on_after_notify": [
          {
            "name": "trigger_action",
            "type": "shell",
            "script": "/home/user/scripts/action.sh",
            "enabled": true,
            "timeout": 120,
            "async": true,
            "condition": "change_type == 'content_change'"
          }
        ]
      }
    }
  ]
}
```

### 15.2 相关文档

- [设计文档](design.md)
- [API 文档](api.md)
- [WebUI 设计文档](webui_design.md)

---

**审批状态**: ⏳ 待 Human 审批

**修订历史**:
| 版本 | 日期 | 作者 | 说明 |
|------|------|------|------|
| 1.0 | 2025-12-29 | Claude | 初稿 |
