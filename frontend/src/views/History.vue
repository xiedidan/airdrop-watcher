<script setup lang="ts">
import { h, ref, computed, onMounted, watch } from 'vue'
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
  NSpin,
  NTooltip,
  NText,
  NPagination,
  NDatePicker,
  NEmpty,
  NCode,
  NScrollbar,
  NDescriptions,
  NDescriptionsItem,
  NDivider,
  NStatistic,
  NGrid,
  NGridItem,
  useMessage,
  type DataTableColumns,
} from 'naive-ui'
import {
  RefreshOutline,
  SearchOutline,
  EyeOutline,
  CheckmarkCircleOutline,
  CloseCircleOutline,
  SwapHorizontalOutline,
  TimeOutline,
  DocumentTextOutline,
  SparklesOutline,
} from '@vicons/ionicons5'
import { historyApi } from '@/api'
import { useTaskStore } from '@/stores/task'
import type { HistoryEntry, ChangeDetails, HistoryStatistics, Task } from '@/types'

const message = useMessage()
const taskStore = useTaskStore()

// 加载状态
const isLoading = ref(true)

// 数据
const historyItems = ref<HistoryEntry[]>([])
const statistics = ref<HistoryStatistics | null>(null)
const totalItems = ref(0)
const totalPages = ref(1)

// 筛选条件
const searchKeyword = ref('')
const selectedTaskId = ref('')
const entryTypeFilter = ref('')
const changedOnlyFilter = ref(false)
const dateRange = ref<[number, number] | null>(null)
const currentPage = ref(1)
const pageSize = ref(20)

// 类型筛选选项
const entryTypeOptions = [
  { label: '全部类型', value: '' },
  { label: '检测结果', value: 'check_result' },
  { label: '变化详情', value: 'change_details' },
]

// 任务选项
const taskOptions = computed(() => {
  const options: { label: string; value: string }[] = [
    { label: '全部任务', value: '' },
  ]
  taskStore.tasks.forEach((task: Task) => {
    options.push({ label: task.name, value: task.id })
  })
  return options
})

// 详情弹窗
const showDetailModal = ref(false)
const selectedEntry = ref<HistoryEntry | null>(null)
const changeDetails = ref<ChangeDetails | null>(null)
const isLoadingDetail = ref(false)

// 格式化时间
const formatDateTime = (dateStr: string | null): string => {
  if (!dateStr) return '-'
  try {
    const date = new Date(dateStr)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    })
  } catch {
    return dateStr
  }
}

// 格式化简短时间
const formatShortDateTime = (dateStr: string | null): string => {
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

// 格式化日期范围为 ISO 字符串
const formatDateToISO = (timestamp: number): string => {
  return new Date(timestamp).toISOString()
}

// 获取任务名称
const getTaskName = (taskId: string): string => {
  const task = taskStore.tasks.find((t: Task) => t.id === taskId)
  return task ? task.name : taskId
}

// 获取变化类型标签
const getChangeTypeTag = (entry: HistoryEntry) => {
  const data = entry.data || {}
  const changed = data.changed || false
  const success = data.success !== false

  if (!success) {
    return h(NTag, { type: 'error', size: 'small' }, { default: () => '失败' })
  }
  if (changed) {
    return h(NTag, { type: 'warning', size: 'small' }, { default: () => '有变化' })
  }
  return h(NTag, { type: 'success', size: 'small' }, { default: () => '无变化' })
}

// 表格列定义
const columns: DataTableColumns<HistoryEntry> = [
  {
    title: '时间',
    key: 'timestamp',
    width: 140,
    render: (row) => formatShortDateTime(row.timestamp),
  },
  {
    title: '任务',
    key: 'task_id',
    width: 180,
    ellipsis: { tooltip: true },
    render: (row) => getTaskName(row.task_id),
  },
  {
    title: '类型',
    key: 'type',
    width: 100,
    render: (row) => {
      const typeLabel = row.type === 'check_result' ? '检测结果' : '变化详情'
      const typeColor = row.type === 'check_result' ? 'info' : 'warning'
      return h(NTag, { type: typeColor, size: 'small' }, { default: () => typeLabel })
    },
  },
  {
    title: '状态',
    key: 'status',
    width: 90,
    render: (row) => getChangeTypeTag(row),
  },
  {
    title: 'URL',
    key: 'url',
    ellipsis: { tooltip: true },
    render: (row) => h('span', { style: { fontSize: '12px', color: '#909399' } }, row.url),
  },
  {
    title: '摘要',
    key: 'summary',
    width: 200,
    ellipsis: { tooltip: true },
    render: (row) => {
      const data = row.data || {}
      const summary = data.changes_summary || data.change_summary || data.ai_summary
      if (summary) {
        return h('span', { style: { fontSize: '12px' } }, summary)
      }
      return h(NText, { depth: 3, style: { fontSize: '12px' } }, { default: () => '-' })
    },
  },
  {
    title: '操作',
    key: 'actions',
    width: 80,
    fixed: 'right',
    render: (row) => {
      return h(
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
                onClick: () => handleViewDetail(row),
              },
              {
                icon: () => h(NIcon, {}, { default: () => h(EyeOutline) }),
              }
            ),
          default: () => '查看详情',
        }
      )
    },
  },
]

// 加载历史记录
const loadHistory = async () => {
  isLoading.value = true
  try {
    const params: Record<string, any> = {
      page: currentPage.value,
      page_size: pageSize.value,
    }

    if (selectedTaskId.value) {
      params.task_id = selectedTaskId.value
    }
    if (entryTypeFilter.value) {
      params.entry_type = entryTypeFilter.value
    }
    if (searchKeyword.value) {
      params.keyword = searchKeyword.value
    }
    if (changedOnlyFilter.value) {
      params.changed_only = true
    }
    if (dateRange.value) {
      params.start_date = formatDateToISO(dateRange.value[0])
      params.end_date = formatDateToISO(dateRange.value[1])
    }

    // 使用搜索接口如果有筛选条件
    const hasFilters = searchKeyword.value || dateRange.value || changedOnlyFilter.value
    const response = hasFilters
      ? await historyApi.search(params)
      : await historyApi.list(params)

    historyItems.value = response.items
    totalItems.value = response.total
    totalPages.value = response.total_pages
  } catch (error) {
    console.error('加载历史记录失败:', error)
    message.error('加载历史记录失败')
  } finally {
    isLoading.value = false
  }
}

// 加载统计信息
const loadStatistics = async () => {
  try {
    const taskId = selectedTaskId.value || undefined
    statistics.value = await historyApi.getStatistics(taskId)
  } catch (error) {
    console.error('加载统计信息失败:', error)
  }
}

// 刷新数据
const handleRefresh = async () => {
  await Promise.all([loadHistory(), loadStatistics()])
  message.success('刷新成功')
}

// 查看详情
const handleViewDetail = async (entry: HistoryEntry) => {
  selectedEntry.value = entry
  changeDetails.value = null
  showDetailModal.value = true

  // 如果是变化详情类型，加载详细内容
  if (entry.type === 'change_details') {
    isLoadingDetail.value = true
    try {
      changeDetails.value = await historyApi.getChangeDetails(entry.id)
    } catch (error) {
      console.error('加载变化详情失败:', error)
      message.error('加载变化详情失败')
    } finally {
      isLoadingDetail.value = false
    }
  }
}

// 页码变化
const handlePageChange = (page: number) => {
  currentPage.value = page
}

// 页大小变化
const handlePageSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
}

// 监听筛选条件变化
watch(
  [selectedTaskId, entryTypeFilter, changedOnlyFilter, dateRange],
  () => {
    currentPage.value = 1
    loadHistory()
  }
)

// 监听页码变化
watch([currentPage, pageSize], () => {
  loadHistory()
})

// 搜索防抖
let searchTimeout: number | null = null
watch(searchKeyword, () => {
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
  searchTimeout = window.setTimeout(() => {
    currentPage.value = 1
    loadHistory()
  }, 300)
})

// 初始化
onMounted(async () => {
  await taskStore.fetchTasks()
  await Promise.all([loadHistory(), loadStatistics()])
})
</script>

<template>
  <div class="history-page">
    <n-spin :show="isLoading">
      <!-- 统计卡片 -->
      <n-grid :cols="24" :x-gap="16" :y-gap="16" v-if="statistics">
        <n-grid-item :span="6">
          <n-card class="stat-card">
            <n-statistic label="总记录数" :value="statistics.total_entries">
              <template #prefix>
                <n-icon color="#63e2b7"><DocumentTextOutline /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item :span="6">
          <n-card class="stat-card">
            <n-statistic label="检测次数" :value="statistics.check_results">
              <template #prefix>
                <n-icon color="#70c0e8"><TimeOutline /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item :span="6">
          <n-card class="stat-card">
            <n-statistic label="变化记录" :value="statistics.change_details">
              <template #prefix>
                <n-icon color="#f2c97d"><SwapHorizontalOutline /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item :span="6">
          <n-card class="stat-card">
            <n-statistic label="变化率" :value="statistics.change_rate.toFixed(1)" suffix="%">
              <template #prefix>
                <n-icon color="#e88080"><SparklesOutline /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
      </n-grid>

      <n-card style="margin-top: 16px">
        <!-- 标题和操作栏 -->
        <template #header>
          <n-space justify="space-between" align="center" style="width: 100%">
            <span class="page-title">变化历史</span>
            <n-button quaternary circle @click="handleRefresh">
              <template #icon>
                <n-icon><RefreshOutline /></n-icon>
              </template>
            </n-button>
          </n-space>
        </template>

        <!-- 筛选器 -->
        <n-space style="margin-bottom: 16px" wrap>
          <n-input
            v-model:value="searchKeyword"
            placeholder="搜索关键词"
            clearable
            style="width: 200px"
          >
            <template #prefix>
              <n-icon><SearchOutline /></n-icon>
            </template>
          </n-input>
          <n-select
            v-model:value="selectedTaskId"
            :options="taskOptions"
            style="width: 180px"
            placeholder="选择任务"
            clearable
          />
          <n-select
            v-model:value="entryTypeFilter"
            :options="entryTypeOptions"
            style="width: 140px"
            placeholder="记录类型"
            clearable
          />
          <n-date-picker
            v-model:value="dateRange"
            type="daterange"
            clearable
            style="width: 280px"
            :shortcuts="{
              '最近7天': () => {
                const end = Date.now()
                const start = end - 7 * 24 * 60 * 60 * 1000
                return [start, end]
              },
              '最近30天': () => {
                const end = Date.now()
                const start = end - 30 * 24 * 60 * 60 * 1000
                return [start, end]
              },
            }"
          />
          <n-button
            :type="changedOnlyFilter ? 'primary' : 'default'"
            @click="changedOnlyFilter = !changedOnlyFilter"
          >
            <template #icon>
              <n-icon><SwapHorizontalOutline /></n-icon>
            </template>
            仅显示变化
          </n-button>
        </n-space>

        <!-- 数据表格 -->
        <n-data-table
          :columns="columns"
          :data="historyItems"
          :bordered="false"
          :single-line="false"
          :row-key="(row: HistoryEntry) => row.id"
          :scroll-x="1000"
          max-height="calc(100vh - 480px)"
        />

        <!-- 分页 -->
        <n-space justify="end" style="margin-top: 16px">
          <n-pagination
            v-model:page="currentPage"
            :page-count="totalPages"
            :page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            show-size-picker
            @update:page="handlePageChange"
            @update:page-size="handlePageSizeChange"
          />
        </n-space>

        <!-- 空状态 -->
        <n-empty
          v-if="historyItems.length === 0 && !isLoading"
          description="暂无历史记录"
          style="margin-top: 40px"
        />
      </n-card>
    </n-spin>

    <!-- 详情弹窗 -->
    <n-modal
      v-model:show="showDetailModal"
      preset="card"
      :title="selectedEntry?.type === 'check_result' ? '检测结果详情' : '变化详情'"
      style="width: 800px; max-width: 90vw"
      :mask-closable="true"
    >
      <n-spin :show="isLoadingDetail">
        <template v-if="selectedEntry">
          <!-- 基本信息 -->
          <n-descriptions :column="2" label-placement="left" bordered>
            <n-descriptions-item label="记录ID">
              <n-text code>{{ selectedEntry.id }}</n-text>
            </n-descriptions-item>
            <n-descriptions-item label="记录类型">
              <n-tag :type="selectedEntry.type === 'check_result' ? 'info' : 'warning'" size="small">
                {{ selectedEntry.type === 'check_result' ? '检测结果' : '变化详情' }}
              </n-tag>
            </n-descriptions-item>
            <n-descriptions-item label="任务名称">
              {{ getTaskName(selectedEntry.task_id) }}
            </n-descriptions-item>
            <n-descriptions-item label="记录时间">
              {{ formatDateTime(selectedEntry.timestamp) }}
            </n-descriptions-item>
            <n-descriptions-item label="URL" :span="2">
              <n-text style="word-break: break-all">{{ selectedEntry.url }}</n-text>
            </n-descriptions-item>
          </n-descriptions>

          <!-- 检测结果详情 -->
          <template v-if="selectedEntry.type === 'check_result'">
            <n-divider>检测结果</n-divider>
            <n-descriptions :column="2" label-placement="left" bordered>
              <n-descriptions-item label="检测状态">
                <n-space align="center">
                  <n-icon :color="selectedEntry.data?.success !== false ? '#63e2b7' : '#e88080'">
                    <CheckmarkCircleOutline v-if="selectedEntry.data?.success !== false" />
                    <CloseCircleOutline v-else />
                  </n-icon>
                  <span>{{ selectedEntry.data?.success !== false ? '成功' : '失败' }}</span>
                </n-space>
              </n-descriptions-item>
              <n-descriptions-item label="是否有变化">
                <n-tag :type="selectedEntry.data?.changed ? 'warning' : 'success'" size="small">
                  {{ selectedEntry.data?.changed ? '有变化' : '无变化' }}
                </n-tag>
              </n-descriptions-item>
              <n-descriptions-item label="加载时间">
                {{ (selectedEntry.data?.load_time || 0).toFixed(2) }}秒
              </n-descriptions-item>
              <n-descriptions-item label="内容大小">
                {{ ((selectedEntry.data?.content_size || 0) / 1024).toFixed(2) }} KB
              </n-descriptions-item>
              <n-descriptions-item v-if="selectedEntry.data?.added_lines > 0" label="新增行数">
                <n-text type="success">+{{ selectedEntry.data.added_lines }}</n-text>
              </n-descriptions-item>
              <n-descriptions-item v-if="selectedEntry.data?.removed_lines > 0" label="删除行数">
                <n-text type="error">-{{ selectedEntry.data.removed_lines }}</n-text>
              </n-descriptions-item>
            </n-descriptions>

            <!-- 变化摘要 -->
            <template v-if="selectedEntry.data?.changes_summary">
              <n-divider>变化摘要</n-divider>
              <n-card embedded>
                <n-text>{{ selectedEntry.data.changes_summary }}</n-text>
              </n-card>
            </template>

            <!-- 错误信息 -->
            <template v-if="selectedEntry.data?.error_message">
              <n-divider>错误信息</n-divider>
              <n-card embedded>
                <n-text type="error">{{ selectedEntry.data.error_message }}</n-text>
              </n-card>
            </template>

            <!-- 内容差异 -->
            <template v-if="selectedEntry.data?.content_diff">
              <n-divider>内容差异</n-divider>
              <n-scrollbar style="max-height: 300px">
                <n-code :code="selectedEntry.data.content_diff" language="diff" />
              </n-scrollbar>
            </template>
          </template>

          <!-- 变化详情 -->
          <template v-if="selectedEntry.type === 'change_details' && changeDetails">
            <n-divider>变化信息</n-divider>
            <n-descriptions :column="2" label-placement="left" bordered>
              <n-descriptions-item label="变化类型">
                <n-tag type="warning" size="small">{{ changeDetails.change_type || '-' }}</n-tag>
              </n-descriptions-item>
              <n-descriptions-item label="变化时间">
                {{ formatDateTime(changeDetails.timestamp) }}
              </n-descriptions-item>
            </n-descriptions>

            <!-- AI 分析摘要 -->
            <template v-if="changeDetails.ai_summary">
              <n-divider>
                <n-space align="center">
                  <n-icon color="#f2c97d"><SparklesOutline /></n-icon>
                  <span>AI 分析</span>
                </n-space>
              </n-divider>
              <n-card embedded>
                <n-text>{{ changeDetails.ai_summary }}</n-text>
              </n-card>
            </template>

            <!-- 变化摘要 -->
            <template v-if="changeDetails.change_summary">
              <n-divider>变化摘要</n-divider>
              <n-card embedded>
                <n-text>{{ changeDetails.change_summary }}</n-text>
              </n-card>
            </template>

            <!-- 内容对比 -->
            <template v-if="changeDetails.diff">
              <n-divider>内容对比 (Diff)</n-divider>
              <n-scrollbar style="max-height: 400px">
                <n-code :code="changeDetails.diff" language="diff" />
              </n-scrollbar>
            </template>

            <!-- 新旧内容对比 -->
            <template v-if="changeDetails.old_content || changeDetails.new_content">
              <n-divider>内容变化</n-divider>
              <n-grid :cols="2" :x-gap="16">
                <n-grid-item v-if="changeDetails.old_content">
                  <n-card title="旧内容" size="small" embedded>
                    <n-scrollbar style="max-height: 200px">
                      <n-code :code="changeDetails.old_content" />
                    </n-scrollbar>
                  </n-card>
                </n-grid-item>
                <n-grid-item v-if="changeDetails.new_content">
                  <n-card title="新内容" size="small" embedded>
                    <n-scrollbar style="max-height: 200px">
                      <n-code :code="changeDetails.new_content" />
                    </n-scrollbar>
                  </n-card>
                </n-grid-item>
              </n-grid>
            </template>
          </template>
        </template>
      </n-spin>
    </n-modal>
  </div>
</template>

<style scoped>
.history-page {
  max-width: 1400px;
}

.page-title {
  font-size: 18px;
  font-weight: 600;
}

.stat-card {
  text-align: center;
}

.stat-card :deep(.n-statistic .n-statistic-value) {
  font-size: 24px;
}
</style>
