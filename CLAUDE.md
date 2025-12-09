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
├── cli/                       # 命令行接口模块
│   ├── commands/             # CLI命令实现
├── config/                    # 配置管理模块
├── core/                      # 核心模块（预留）
├── detection/                 # 变化检测模块
├── exceptions/                # 异常定义模块
├── models/                    # 数据模型模块
├── notification/              # 通知服务模块
│   ├── platforms/            # 各推送平台实现
├── scheduler/                 # 任务调度模块
├── storage/                   # 存储管理模块
├── tests/                     # 单元测试模块
│   ├── unit/                 # 单元测试
│   ├── integration/          # 集成测试
├── utils/                     # 工具函数模块
│   ├── logger.py             # 日志管理
│   ├── enhanced_logger.py    # 增强日志
│   ├── log_config.py         # 日志配置
│   ├── formatters.py         # 格式化工具
│   ├── validators.py         # 验证工具
└── __init__.py
```

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
