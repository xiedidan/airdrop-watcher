<script setup lang="ts">
import { h, ref, computed, onMounted } from 'vue'
import {
  NCard,
  NDataTable,
  NButton,
  NSpace,
  NInput,
  NSelect,
  NTag,
  NIcon,
  NModal,
  NForm,
  NFormItem,
  NInputNumber,
  NSwitch,
  NSpin,
  NPopconfirm,
  NTooltip,
  NText,
  NDivider,
  useMessage,
  useDialog,
  type DataTableColumns,
  type FormInst,
  type FormRules,
} from 'naive-ui'
import {
  AddOutline,
  RefreshOutline,
  CreateOutline,
  TrashOutline,
  PlayOutline,
  PauseOutline,
  FlashOutline,
  SearchOutline,
  LinkOutline,
  WifiOutline,
} from '@vicons/ionicons5'
import { useTaskStore } from '@/stores/task'
import { useSSEStore } from '@/stores/sse'
import type { Task, TaskCreate, TaskUpdate } from '@/types'

const message = useMessage()
const dialog = useDialog()
const taskStore = useTaskStore()
const sseStore = useSSEStore()

// 加载状态
const isLoading = ref(true)

// 搜索和筛选
const searchKeyword = ref('')
const statusFilter = ref<string>('all')

// 状态筛选选项
const statusOptions = [
  { label: '全部状态', value: 'all' },
  { label: '已启用', value: 'enabled' },
  { label: '已禁用', value: 'disabled' },
  { label: '有错误', value: 'error' },
]

// 筛选后的任务列表
const filteredTasks = computed(() => {
  let result = [...taskStore.tasks]

  // 关键词搜索
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    result = result.filter(
      t =>
        t.name.toLowerCase().includes(keyword) ||
        t.url.toLowerCase().includes(keyword) ||
        t.description.toLowerCase().includes(keyword)
    )
  }

  // 状态筛选
  if (statusFilter.value && statusFilter.value !== 'all') {
    switch (statusFilter.value) {
      case 'enabled':
        result = result.filter(t => t.enabled)
        break
      case 'disabled':
        result = result.filter(t => !t.enabled)
        break
      case 'error':
        result = result.filter(t => t.error_count > 0)
        break
    }
  }

  return result
})

// 弹窗状态
const showModal = ref(false)
const modalMode = ref<'add' | 'edit'>('add')
const editingTask = ref<Task | null>(null)
const formRef = ref<FormInst | null>(null)

// 表单数据
const formData = ref<{
  url: string
  name: string
  description: string
  selectors: string
  interval: number
  timeout: number
  enabled: boolean
  ai_prompt: string
}>({
  url: '',
  name: '',
  description: '',
  selectors: '',
  interval: 300,
  timeout: 30000,
  enabled: true,
  ai_prompt: '',
})

// 表单验证规则
const formRules: FormRules = {
  url: [
    { required: true, message: '请输入网页URL', trigger: 'blur' },
    {
      validator: (_rule, value) => {
        if (value && !value.startsWith('http://') && !value.startsWith('https://')) {
          return new Error('URL必须以 http:// 或 https:// 开头')
        }
        return true
      },
      trigger: 'blur',
    },
  ],
  name: [
    { required: true, message: '请输入任务名称', trigger: 'blur' },
    { min: 1, max: 100, message: '任务名称长度应在1-100之间', trigger: 'blur' },
  ],
  interval: [
    { required: true, type: 'number', message: '请输入检测间隔', trigger: 'blur' },
  ],
  timeout: [
    { required: true, type: 'number', message: '请输入超时时间', trigger: 'blur' },
  ],
}

// 默认提示词占位符
const defaultPromptPlaceholder = '留空使用系统默认提示词。支持占位符: {task_name}, {url}, {description}, {changes}'

// 格式化时间
const formatDateTime = (dateStr: string | null): string => {
  if (!dateStr) return '-'
  try {
    const date = new Date(dateStr)
    return date.toLocaleString('zh-CN', {
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch {
    return dateStr
  }
}

// 格式化间隔
const formatInterval = (seconds: number): string => {
  if (seconds < 60) return `${seconds}秒`
  if (seconds < 3600) return `${Math.floor(seconds / 60)}分钟`
  return `${Math.floor(seconds / 3600)}小时`
}

// 表格列定义
const columns: DataTableColumns<Task> = [
  {
    title: '任务名称',
    key: 'name',
    width: 180,
    ellipsis: { tooltip: true },
    render: (row) => {
      return h(NSpace, { align: 'center' }, {
        default: () => [
          h('span', { style: { fontWeight: 500 } }, row.name),
          row.error_count > 0 && h(NTooltip, {}, {
            trigger: () => h(NIcon, { color: '#e88080', size: 16 }, { default: () => h(FlashOutline) }),
            default: () => row.last_error_message || '任务存在错误',
          }),
        ],
      })
    },
  },
  {
    title: 'URL',
    key: 'url',
    width: 250,
    ellipsis: { tooltip: true },
    render: (row) => {
      return h(NSpace, { align: 'center' }, {
        default: () => [
          h(NIcon, { size: 14, color: '#63e2b7' }, { default: () => h(LinkOutline) }),
          h('span', { style: { fontSize: '13px' } }, row.url),
        ],
      })
    },
  },
  {
    title: '状态',
    key: 'status',
    width: 90,
    render: (row) => {
      if (!row.enabled) {
        return h(NTag, { type: 'default', size: 'small' }, { default: () => '已禁用' })
      }
      if (row.error_count > 0) {
        return h(NTag, { type: 'error', size: 'small' }, { default: () => '错误' })
      }
      return h(NTag, { type: 'success', size: 'small' }, { default: () => '正常' })
    },
  },
  {
    title: '检测间隔',
    key: 'interval',
    width: 100,
    render: (row) => formatInterval(row.interval),
  },
  {
    title: '最后检测',
    key: 'last_check',
    width: 120,
    render: (row) => formatDateTime(row.last_check),
  },
  {
    title: '变化次数',
    key: 'change_count',
    width: 90,
    align: 'center',
  },
  {
    title: '操作',
    key: 'actions',
    width: 200,
    fixed: 'right',
    render: (row) => {
      return h(NSpace, { size: 'small' }, {
        default: () => [
          // 启用/禁用
          h(
            NTooltip,
            {},
            {
              trigger: () =>
                h(
                  NButton,
                  {
                    size: 'small',
                    quaternary: true,
                    type: row.enabled ? 'warning' : 'success',
                    onClick: () => handleToggleEnable(row),
                  },
                  {
                    icon: () => h(NIcon, {}, { default: () => h(row.enabled ? PauseOutline : PlayOutline) }),
                  }
                ),
              default: () => (row.enabled ? '禁用' : '启用'),
            }
          ),
          // 立即检测
          h(
            NTooltip,
            {},
            {
              trigger: () =>
                h(
                  NButton,
                  {
                    size: 'small',
                    quaternary: true,
                    type: 'info',
                    onClick: () => handleCheckNow(row),
                  },
                  {
                    icon: () => h(NIcon, {}, { default: () => h(FlashOutline) }),
                  }
                ),
              default: () => '立即检测',
            }
          ),
          // 编辑
          h(
            NTooltip,
            {},
            {
              trigger: () =>
                h(
                  NButton,
                  {
                    size: 'small',
                    quaternary: true,
                    type: 'primary',
                    onClick: () => handleEdit(row),
                  },
                  {
                    icon: () => h(NIcon, {}, { default: () => h(CreateOutline) }),
                  }
                ),
              default: () => '编辑',
            }
          ),
          // 删除
          h(
            NPopconfirm,
            {
              onPositiveClick: () => handleDelete(row),
            },
            {
              trigger: () =>
                h(
                  NButton,
                  {
                    size: 'small',
                    quaternary: true,
                    type: 'error',
                  },
                  {
                    icon: () => h(NIcon, {}, { default: () => h(TrashOutline) }),
                  }
                ),
              default: () => `确定要删除任务 "${row.name}" 吗？`,
            }
          ),
        ],
      })
    },
  },
]

// 加载数据
const loadData = async () => {
  isLoading.value = true
  try {
    await taskStore.fetchTasks()
  } finally {
    isLoading.value = false
  }
}

// 刷新
const handleRefresh = async () => {
  await loadData()
  message.success('刷新成功')
}

// 打开添加弹窗
const handleAdd = () => {
  modalMode.value = 'add'
  editingTask.value = null
  formData.value = {
    url: '',
    name: '',
    description: '',
    selectors: '',
    interval: 300,
    timeout: 30000,
    enabled: true,
    ai_prompt: '',
  }
  showModal.value = true
}

// 打开编辑弹窗
const handleEdit = (task: Task) => {
  modalMode.value = 'edit'
  editingTask.value = task
  formData.value = {
    url: task.url,
    name: task.name,
    description: task.description,
    selectors: task.selectors.join(', '),
    interval: task.interval,
    timeout: task.timeout,
    enabled: task.enabled,
    ai_prompt: task.ai_prompt,
  }
  showModal.value = true
}

// 提交表单
const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
  } catch {
    return
  }

  const data: TaskCreate | TaskUpdate = {
    url: formData.value.url,
    name: formData.value.name,
    description: formData.value.description,
    selectors: formData.value.selectors
      ? formData.value.selectors.split(',').map(s => s.trim()).filter(Boolean)
      : [],
    interval: formData.value.interval,
    timeout: formData.value.timeout,
    enabled: formData.value.enabled,
    ai_prompt: formData.value.ai_prompt,
  }

  if (modalMode.value === 'add') {
    const task = await taskStore.createTask(data as TaskCreate)
    if (task) {
      message.success('任务创建成功')
      showModal.value = false
    } else {
      message.error('任务创建失败')
    }
  } else if (editingTask.value) {
    const task = await taskStore.updateTask(editingTask.value.id, data as TaskUpdate)
    if (task) {
      message.success('任务更新成功')
      showModal.value = false
    } else {
      message.error('任务更新失败')
    }
  }
}

// 启用/禁用任务
const handleToggleEnable = async (task: Task) => {
  const success = task.enabled
    ? await taskStore.disableTask(task.id)
    : await taskStore.enableTask(task.id)

  if (success) {
    message.success(task.enabled ? '已禁用' : '已启用')
  } else {
    message.error('操作失败')
  }
}

// 立即检测
const handleCheckNow = async (task: Task) => {
  message.info(`正在检测 "${task.name}"...`)
  const result = await taskStore.checkTask(task.id)
  if (result) {
    if (result.error) {
      message.error(`检测失败: ${result.error}`)
    } else if (result.changed) {
      message.success('检测到变化！')
    } else {
      message.info('未检测到变化')
    }
    // SSE 会自动更新任务列表，此处不需要手动刷新
  } else {
    message.error('检测请求失败')
  }
}

// 删除任务
const handleDelete = async (task: Task) => {
  const success = await taskStore.deleteTask(task.id)
  if (success) {
    message.success('删除成功')
  } else {
    message.error('删除失败')
  }
}

onMounted(async () => {
  await loadData()
})
</script>

<template>
  <div class="tasks-page">
    <n-spin :show="isLoading">
      <n-card>
        <!-- 标题和操作栏 -->
        <template #header>
          <n-space justify="space-between" align="center" style="width: 100%">
            <n-space align="center">
              <span class="page-title">任务管理</span>
              <n-tooltip v-if="sseStore.isConnected" trigger="hover">
                <template #trigger>
                  <n-tag type="success" size="small" round>
                    <template #icon>
                      <n-icon><WifiOutline /></n-icon>
                    </template>
                    实时更新
                  </n-tag>
                </template>
                <span>任务状态将自动同步更新</span>
              </n-tooltip>
            </n-space>
            <n-space>
              <n-button type="primary" @click="handleAdd">
                <template #icon>
                  <n-icon><AddOutline /></n-icon>
                </template>
                添加任务
              </n-button>
              <n-button quaternary circle @click="handleRefresh">
                <template #icon>
                  <n-icon><RefreshOutline /></n-icon>
                </template>
              </n-button>
            </n-space>
          </n-space>
        </template>

        <!-- 搜索和筛选 -->
        <n-space style="margin-bottom: 16px">
          <n-input
            v-model:value="searchKeyword"
            placeholder="搜索任务名称、URL或描述"
            clearable
            style="width: 300px"
          >
            <template #prefix>
              <n-icon><SearchOutline /></n-icon>
            </template>
          </n-input>
          <n-select
            v-model:value="statusFilter"
            :options="statusOptions"
            style="width: 150px"
            placeholder="状态筛选"
          />
        </n-space>

        <!-- 任务表格 -->
        <n-data-table
          :columns="columns"
          :data="filteredTasks"
          :bordered="false"
          :single-line="false"
          :row-key="(row: Task) => row.id"
          :scroll-x="1100"
          max-height="calc(100vh - 320px)"
        />

        <!-- 统计信息 -->
        <n-space style="margin-top: 16px">
          <n-text depth="3">
            共 {{ taskStore.total }} 个任务，
            {{ taskStore.activeCount }} 个启用，
            {{ taskStore.errorCount }} 个错误
          </n-text>
        </n-space>
      </n-card>
    </n-spin>

    <!-- 添加/编辑弹窗 -->
    <n-modal
      v-model:show="showModal"
      :title="modalMode === 'add' ? '添加任务' : '编辑任务'"
      preset="card"
      style="width: 600px"
      :mask-closable="false"
    >
      <n-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-placement="left"
        label-width="100"
        require-mark-placement="right-hanging"
      >
        <n-form-item label="任务名称" path="name">
          <n-input v-model:value="formData.name" placeholder="请输入任务名称" />
        </n-form-item>

        <n-form-item label="网页URL" path="url">
          <n-input v-model:value="formData.url" placeholder="https://example.com" />
        </n-form-item>

        <n-form-item label="任务描述" path="description">
          <n-input
            v-model:value="formData.description"
            type="textarea"
            placeholder="任务描述，用于AI分析时的上下文"
            :rows="2"
          />
        </n-form-item>

        <n-form-item label="CSS选择器" path="selectors">
          <n-input
            v-model:value="formData.selectors"
            placeholder="多个选择器用逗号分隔，如: .content, #main"
          />
        </n-form-item>

        <n-form-item label="检测间隔" path="interval">
          <n-input-number
            v-model:value="formData.interval"
            :min="10"
            :max="86400"
            style="width: 100%"
          >
            <template #suffix>秒</template>
          </n-input-number>
        </n-form-item>

        <n-form-item label="超时时间" path="timeout">
          <n-input-number
            v-model:value="formData.timeout"
            :min="1000"
            :max="120000"
            :step="1000"
            style="width: 100%"
          >
            <template #suffix>毫秒</template>
          </n-input-number>
        </n-form-item>

        <n-form-item label="启用状态">
          <n-switch v-model:value="formData.enabled" />
        </n-form-item>

        <n-divider style="margin: 16px 0">AI 配置</n-divider>

        <n-form-item label="自定义提示词" path="ai_prompt">
          <n-input
            v-model:value="formData.ai_prompt"
            type="textarea"
            :placeholder="defaultPromptPlaceholder"
            :rows="3"
          />
        </n-form-item>
      </n-form>

      <template #footer>
        <n-space justify="end">
          <n-button @click="showModal = false">取消</n-button>
          <n-button type="primary" @click="handleSubmit" :loading="taskStore.loading">
            {{ modalMode === 'add' ? '添加' : '保存' }}
          </n-button>
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<style scoped>
.tasks-page {
  max-width: 1400px;
}

.page-title {
  font-size: 18px;
  font-weight: 600;
}
</style>
