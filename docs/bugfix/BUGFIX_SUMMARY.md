# Bug修复总结 - 相似度0%问题

## 问题描述

监控服务疯狂发送Discord通知，每次检测都显示"相似度: 0%"，即使内容几乎没有变化。

## 根本原因

两个问题导致相似度始终为0%：

### 问题1: 历史记录未保存内容预览

**位置**: `webmon/scheduler/task_scheduler.py:429-444`

**原因**: 创建CheckResult时只保存了基本信息，没有调用set_content()保存内容预览。

**后果**:
- 历史记录中 `content_preview` 为空
- 下次检测时 `old_content = ""`（空字符串）
- 变化检测器判断为 `content_missing`
- 每次都触发通知

### 问题2: 未变化时相似度字段缺失

**位置**: `webmon/detection/change_detector.py:186-236`

**原因**: 哈希检测发现内容相同时直接返回，没有添加similarity字段。

**后果**:
- 内容完全相同时，相似度显示 0%（实际应该是 100%）
- 通知中显示误导性的信息

## 修复方案

### 修复1: 保存内容预览 (task_scheduler.py:439-441)

```python
# 保存内容预览（用于下次对比）
new_content = page_content.get('content', '') if isinstance(page_content, dict) else str(page_content)
check_result.set_content(new_content, calculate_hash=False)
```

### 修复2: 补充相似度字段 (change_detector.py:224-229)

```python
# 内容未变化，添加相似度为100%
if not hash_result["changed"]:
    hash_result["similarity"] = 1.0
    hash_result["algorithm"] = "hash"
    hash_result["auto_reason"] = "hash_unchanged"
```

## 验证结果

运行测试脚本 `test_similarity.py`：

```
1. 第一次检测（无历史）
   变化: True, 相似度: 0.0%
   ✅ 已保存历史（content_preview: 178字符）

2. 第二次检测（内容完全相同）
   变化: False, 相似度: 100.0% ✅

3. 第三次检测（轻微变化）
   变化: False, 相似度: 90.9% ✅

4. 第四次检测（重大变化）
   变化: True, 相似度: 19.8% ✅
```

**所有测试通过！**

## 影响范围

- **修改文件**: 2个
  - `webmon/scheduler/task_scheduler.py` (添加3行)
  - `webmon/detection/change_detector.py` (添加6行)

- **影响功能**:
  - ✅ 变化检测准确性提升
  - ✅ 相似度计算正确
  - ✅ 大幅减少误报通知

- **向后兼容**: 完全兼容

## 清理操作

- ✅ 已备份旧历史数据到 `data/history.json.backup`
- ✅ 已重置历史文件
- ✅ 已禁用所有测试任务

## 后续建议

1. **重新配置任务**: 调整检测间隔到合理值（5-30分钟）
2. **使用选择器**: 对于经常变化的网站，使用CSS选择器精确监控
3. **先测试一个**: 启用一个任务验证后再启用其他

## 修复完成时间

2025-12-07 18:30
