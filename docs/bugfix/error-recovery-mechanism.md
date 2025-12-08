# 任务自动错误恢复机制

> **创建时间**: 2025-12-08
> **负责人**: Claude
> **状态**: ✅ 已实现

---

## 📋 问题描述

### 原始问题

用户发现所有监控任务都显示 `error` 状态，并提出关键问题：

1. **为什么任务都是error状态？**
2. **程序应该尝试从error状态恢复**
3. **如果失败，要保存详细日志供用户研判**

### 问题根源

```
任务执行流程：
1. 任务执行失败
2. 调度器重试（最多5次）
3. 达到最大重试次数
4. 标记为 status='error'
5. ❌ 任务永久停留在error状态，不会自动恢复
```

**核心问题**：一旦任务被标记为error，调度器不会再次调度它，除非用户手动干预。

---

## 🎯 解决方案

### 1. Task模型增强

在 `webmon/models/task.py` 中添加错误跟踪字段：

```python
# 错误跟踪（用于自动恢复）
error_count: int = 0  # 连续错误次数
last_error: Optional[datetime] = None  # 最后一次错误时间
last_error_message: Optional[str] = None  # 最后一次错误信息
```

**作用**：
- `error_count`：记录连续失败次数，用于计算退避时间
- `last_error`：记录失败时间，用于监控和分析
- `last_error_message`：保存详细错误信息，帮助用户排查问题

---

### 2. 自动错误恢复机制

#### 2.1 失败处理逻辑

```python
# 达到最大重试次数，标记为失败
task.set_status('error')
task.error_count = task.error_count + 1
task.last_error = datetime.now()
task.last_error_message = str(error)

# 更新任务状态（持久化）
self.storage.update_task(task.id, {
    'status': 'error',
    'error_count': task.error_count,
    'last_error': task.last_error.isoformat(),
    'last_error_message': task.last_error_message
})

# 记录详细错误日志
self.logger.error(
    f"任务 {task.name} (ID: {task.id}) 执行失败\n"
    f"  错误次数: {task.error_count}\n"
    f"  错误信息: {task.last_error_message}\n"
    f"  将在下次检查周期自动重试（使用指数退避策略）"
)

# 自动重新调度error任务（使用指数退避）
retry_interval = self._calculate_error_backoff(task.error_count)
await self._schedule_task_with_delay(task, retry_interval)
```

#### 2.2 指数退避策略

```python
def _calculate_error_backoff(self, error_count: int) -> int:
    """计算错误退避时间（指数退避）"""
    base_interval = 300  # 5分钟

    # 公式：2^(error_count-1) * base_interval
    backoff = min(base_interval * (2 ** (error_count - 1)), 86400)  # 最大24小时

    return int(backoff)
```

**退避时间表：**

| 失败次数 | 计算公式 | 退避时间 |
|---------|----------|---------|
| 1 | 2^0 * 300s | 5分钟 |
| 2 | 2^1 * 300s | 10分钟 |
| 3 | 2^2 * 300s | 20分钟 |
| 4 | 2^3 * 300s | 40分钟 |
| 5 | 2^4 * 300s | 80分钟 (1.3小时) |
| 6 | 2^5 * 300s | 160分钟 (2.7小时) |
| 7 | 2^6 * 300s | 320分钟 (5.3小时) |
| 8 | 2^7 * 300s | 640分钟 (10.7小时) |
| 9+ | min(2^8 * 300s, 86400s) | **24小时** (上限) |

#### 2.3 延迟调度

```python
async def _schedule_task_with_delay(self, task: Task, delay_seconds: int):
    """延迟调度任务（用于错误恢复）"""
    next_run = datetime.now() + timedelta(seconds=delay_seconds)

    job = {
        'task': task,
        'next_run': next_run,
        'priority': self.priority_manager.calculate_priority(task) - 20,  # 降低优先级
        'retry_count': 0
    }

    await self.job_queue.put(job)

    self.logger.info(
        f"任务 {task.name} (ID: {task.id}) 已调度错误恢复，"
        f"将在 {delay_seconds}秒 后重试（{next_run.strftime('%Y-%m-%d %H:%M:%S')}）"
    )
```

**特点：**
- 自动将error任务重新加入队列
- 降低优先级，避免影响正常任务
- 记录详细的调度信息

---

### 3. 成功后重置错误计数

```python
# 成功执行：重置错误计数
if task.error_count > 0:
    self.logger.info(f"任务 {task.name} 执行成功，重置错误计数（之前: {task.error_count}）")
    task.error_count = 0
    task.last_error = None
    task.last_error_message = None
    task.set_status('active')

# 保存任务更新
updates = {
    'last_check': task.last_check,
    'updated_at': task.updated_at,
    'error_count': 0,
    'last_error': None,
    'last_error_message': None,
    'status': 'active'
}
```

**作用**：任务恢复后，清零错误计数，重新开始正常的检测周期。

---

## 🔍 完整工作流程

### 场景1：任务持续失败

```
初始状态: error_count=0, status='active'

第1次失败 → error_count=1, 5分钟后重试
第2次失败 → error_count=2, 10分钟后重试
第3次失败 → error_count=3, 20分钟后重试
第4次失败 → error_count=4, 40分钟后重试
...
第9次失败 → error_count=9, 24小时后重试
第10次失败 → error_count=10, 24小时后重试（上限）
```

### 场景2：任务间歇性失败

```
初始状态: error_count=0, status='active'

第1次失败 → error_count=1, 5分钟后重试
  ↓
成功执行 → error_count=0（重置）, status='active'
  ↓
正常运行一段时间...
  ↓
再次失败 → error_count=1, 5分钟后重试（从头开始）
```

### 场景3：任务最终恢复

```
连续5次失败 → error_count=5, 80分钟后重试
  ↓
成功执行 → error_count=0, status='active'
  ↓
恢复正常监控周期（60分钟）
```

---

## 📊 日志示例

### 失败日志

```
2025-12-08 16:30:15 | ERROR | 任务 bian.sqdxw.top (ID: 1b77c6d2) 执行失败
  错误次数: 3
  错误信息: TimeoutError: Page load timeout after 30s
  将在下次检查周期自动重试（使用指数退避策略）

2025-12-08 16:30:15 | INFO | 任务 bian.sqdxw.top (ID: 1b77c6d2) 已调度错误恢复，
  将在 1200秒 后重试（2025-12-08 16:50:15）
```

### 恢复日志

```
2025-12-08 17:10:20 | INFO | 任务 bian.sqdxw.top 执行成功，重置错误计数（之前: 3）
2025-12-08 17:10:20 | INFO | 任务 bian.sqdxw.top 执行完成，耗时: 2.35秒
```

---

## 🎯 设计优势

### 1. **自动化恢复**
- 无需人工干预，系统自动尝试恢复
- error不是终态，而是临时状态

### 2. **智能退避**
- 短期故障快速恢复（5-20分钟）
- 长期故障避免频繁重试（最长24小时）
- 节省系统资源和网络带宽

### 3. **详细日志**
- 错误次数、错误信息、重试时间一目了然
- 帮助用户快速定位问题
- 支持错误趋势分析

### 4. **优先级管理**
- error任务降低优先级
- 不影响正常任务执行
- 公平的资源分配

---

## 🔧 用户操作

### 查看错误任务

```bash
python webmon.py status
```

输出示例：
```
📋 任务详细状态:
====================================================================================================

✅ 🔴 [1b77c6d2] bian.sqdxw.top
   URL: https://bian.sqdxw.top/
   状态: error | 启用: 是
   间隔: 60分钟 | 超时: 30000ms
   最后检测: 2025-12-08T16:30:15
   错误次数: 3
   最后错误: 2025-12-08T16:30:15
   错误信息: TimeoutError: Page load timeout
   下次重试: 2025-12-08T16:50:15 (20分钟后)
```

### 手动重试

如果不想等待自动恢复，可以手动启动：

```bash
python webmon.py start --task 1b77c6d2
```

系统会：
1. 自动启用任务（如果被禁用）
2. 立即执行一次检测
3. 如果成功，重置error_count

---

## 📈 未来优化

### 可能的改进方向

1. **可配置的退避策略**
   ```json
   "error_recovery": {
     "base_interval": 300,
     "max_backoff": 86400,
     "strategy": "exponential"  // 或 "linear", "fibonacci"
   }
   ```

2. **错误类型分类**
   - 网络错误：快速重试
   - 配置错误：降低重试频率
   - 服务器错误：中等重试

3. **健康度评分**
   - 基于历史成功率
   - 动态调整监控间隔

4. **告警阈值**
   - error_count > 5：发送警报邮件
   - error_count > 10：暂停任务，等待人工介入

---

## ✅ 测试验证

### 测试场景

1. ✅ Task模型新字段正常工作
2. ✅ 错误信息正确保存
3. ✅ 指数退避计算准确
4. ✅ 延迟调度功能正常
5. ✅ 成功后重置error_count

### 需要的后续测试

- [ ] 实际监控任务失败恢复
- [ ] 长时间运行稳定性测试
- [ ] 并发错误处理测试

---

## 📝 相关文件

- `webmon/models/task.py` - Task模型定义
- `webmon/scheduler/task_scheduler.py` - 调度器实现
- `webmon/storage/task_storage.py` - 任务存储
- `config/config.json` - 任务配置文件

---

## 🔗 相关提交

- `996d7af` - feat: 实现任务自动错误恢复机制

---

**总结**: 这个改进彻底解决了任务error状态永久化的问题，使系统具备了自愈能力，显著提升了可用性和用户体验。
