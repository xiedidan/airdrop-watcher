<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import {
  NCard,
  NGrid,
  NGridItem,
  NStatistic,
  NSpace,
  NEmpty,
  NDataTable,
  NTag,
  NButton,
  NIcon,
  NText,
  NSpin,
  NProgress,
  NTooltip,
} from 'naive-ui'
import {
  RefreshOutline,
  CheckmarkCircleOutline,
  AlertCircleOutline,
  TimeOutline,
  FlashOutline,
  TrendingUpOutline,
  WifiOutline,
} from '@vicons/ionicons5'
import { useMonitorStore } from '@/stores/monitor'
import { useTaskStore } from '@/stores/task'
import { useSSEStore } from '@/stores/sse'
import type { Task } from '@/types'

const router = useRouter()
const monitorStore = useMonitorStore()
const taskStore = useTaskStore()
const sseStore = useSSEStore()

// 加载状态
const isLoading = ref(true)

// 格式化时间
const formatTime = (seconds: number): string => {
  if (seconds < 60) {
    return `${Math.floor(seconds)}秒`
  } else if (seconds < 3600) {
    return `${Math.floor(seconds / 60)}分钟`
  } else if (seconds < 86400) {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    return `${hours}小时${minutes}分钟`
  } else {
    const days = Math.floor(seconds / 86400)
    const hours = Math.floor((seconds % 86400) / 3600)
    return `${days}天${hours}小时`
  }
}

// 格式化日期时间
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

// 成功率
const successRate = computed(() => {
  const total = monitorStore.totalExecutions
  if (total === 0) return 100
  return Math.round((monitorStore.successfulExecutions / total) * 100)
})

// 最近变化的任务（按 last_change 排序）
const recentChangedTasks = computed(() => {
  return [...taskStore.tasks]
    .filter(t => t.last_change)
    .sort((a, b) => {
      const dateA = new Date(a.last_change || 0).getTime()
      const dateB = new Date(b.last_change || 0).getTime()
      return dateB - dateA
    })
    .slice(0, 5)
})

// 任务概览表格列
const taskColumns = [
  {
    title: '任务名称',
    key: 'name',
    ellipsis: { tooltip: true },
  },
  {
    title: '状态',
    key: 'status',
    width: 100,
    render: (row: Task) => {
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
    title: '最后变化',
    key: 'last_change',
    width: 140,
    render: (row: Task) => formatDateTime(row.last_change),
  },
  {
    title: '变化次数',
    key: 'change_count',
    width: 90,
    align: 'center' as const,
  },
]

// 使用 h 函数
import { h } from 'vue'

// 加载数据
const loadData = async () => {
  isLoading.value = true
  try {
    await Promise.all([
      monitorStore.fetchStatus(),
      taskStore.fetchTasks(),
    ])
  } finally {
    isLoading.value = false
  }
}

// 刷新数据
const handleRefresh = async () => {
  await loadData()
}

// 导航到任务页面
const goToTasks = () => {
  router.push('/tasks')
}

// 导航到历史页面
const goToHistory = () => {
  router.push('/history')
}

// 初始化加载数据（后续由 SSE 自动更新）
onMounted(async () => {
  await loadData()
})
</script>

<template>
  <div class="dashboard">
    <n-spin :show="isLoading">
      <!-- 顶部操作栏 -->
      <div class="dashboard-header">
        <n-space align="center">
          <h2 class="page-title">仪表盘</h2>
          <n-tooltip v-if="sseStore.isConnected" trigger="hover">
            <template #trigger>
              <n-tag type="success" size="small" round>
                <template #icon>
                  <n-icon><WifiOutline /></n-icon>
                </template>
                实时更新
              </n-tag>
            </template>
            <span>SSE 实时连接已建立，数据将自动更新</span>
          </n-tooltip>
        </n-space>
        <n-button quaternary circle @click="handleRefresh" :loading="isLoading">
          <template #icon>
            <n-icon><RefreshOutline /></n-icon>
          </template>
        </n-button>
      </div>

      <!-- 统计卡片 -->
      <n-grid :cols="24" :x-gap="16" :y-gap="16">
        <n-grid-item :span="6">
          <n-card class="stat-card">
            <n-space vertical>
              <n-space align="center" justify="space-between" style="width: 100%">
                <span class="stat-label">任务总数</span>
                <n-icon size="24" color="#63e2b7"><FlashOutline /></n-icon>
              </n-space>
              <n-statistic :value="taskStore.total" />
              <n-text depth="3">活跃: {{ taskStore.activeCount }}</n-text>
            </n-space>
          </n-card>
        </n-grid-item>

        <n-grid-item :span="6">
          <n-card class="stat-card">
            <n-space vertical>
              <n-space align="center" justify="space-between" style="width: 100%">
                <span class="stat-label">检测到的变化</span>
                <n-icon size="24" color="#f2c97d"><TrendingUpOutline /></n-icon>
              </n-space>
              <n-statistic :value="monitorStore.totalChanges" />
              <n-text depth="3">执行次数: {{ monitorStore.totalExecutions }}</n-text>
            </n-space>
          </n-card>
        </n-grid-item>

        <n-grid-item :span="6">
          <n-card class="stat-card">
            <n-space vertical>
              <n-space align="center" justify="space-between" style="width: 100%">
                <span class="stat-label">成功率</span>
                <n-icon size="24" color="#70c0e8"><CheckmarkCircleOutline /></n-icon>
              </n-space>
              <n-statistic :value="successRate" suffix="%" />
              <n-progress
                type="line"
                :percentage="successRate"
                :show-indicator="false"
                :height="4"
                :color="successRate >= 80 ? '#63e2b7' : successRate >= 50 ? '#f2c97d' : '#e88080'"
              />
            </n-space>
          </n-card>
        </n-grid-item>

        <n-grid-item :span="6">
          <n-card class="stat-card">
            <n-space vertical>
              <n-space align="center" justify="space-between" style="width: 100%">
                <span class="stat-label">运行时间</span>
                <n-icon size="24" :color="monitorStore.isRunning ? '#63e2b7' : '#909399'">
                  <TimeOutline />
                </n-icon>
              </n-space>
              <div class="stat-value">
                <template v-if="monitorStore.isRunning">
                  {{ formatTime(monitorStore.uptime) }}
                </template>
                <template v-else>
                  <n-text depth="3">已停止</n-text>
                </template>
              </div>
              <n-text depth="3">
                状态:
                <n-text :type="monitorStore.isRunning ? 'success' : 'default'">
                  {{ monitorStore.isRunning ? '运行中' : '已停止' }}
                </n-text>
              </n-text>
            </n-space>
          </n-card>
        </n-grid-item>
      </n-grid>

      <!-- 下方两栏 -->
      <n-grid :cols="24" :x-gap="16" :y-gap="16" style="margin-top: 16px">
        <!-- 最近变化 -->
        <n-grid-item :span="12">
          <n-card title="最近变化" class="list-card">
            <template #header-extra>
              <n-button text type="primary" @click="goToHistory">查看全部</n-button>
            </template>
            <template v-if="recentChangedTasks.length > 0">
              <div class="change-list">
                <div
                  v-for="task in recentChangedTasks"
                  :key="task.id"
                  class="change-item"
                >
                  <n-space align="center" justify="space-between" style="width: 100%">
                    <n-space align="center">
                      <n-icon color="#63e2b7"><CheckmarkCircleOutline /></n-icon>
                      <span class="task-name">{{ task.name }}</span>
                    </n-space>
                    <n-space align="center">
                      <n-tag size="small" round>{{ task.change_count }}次</n-tag>
                      <n-text depth="3" style="font-size: 12px">
                        {{ formatDateTime(task.last_change) }}
                      </n-text>
                    </n-space>
                  </n-space>
                </div>
              </div>
            </template>
            <template v-else>
              <n-empty description="暂无变化记录" />
            </template>
          </n-card>
        </n-grid-item>

        <!-- 任务概览 -->
        <n-grid-item :span="12">
          <n-card title="任务概览" class="list-card">
            <template #header-extra>
              <n-button text type="primary" @click="goToTasks">管理任务</n-button>
            </template>
            <template v-if="taskStore.tasks.length > 0">
              <n-data-table
                :columns="taskColumns"
                :data="taskStore.tasks.slice(0, 5)"
                :bordered="false"
                size="small"
                :pagination="false"
              />
              <div v-if="taskStore.total > 5" class="more-hint">
                <n-text depth="3">共 {{ taskStore.total }} 个任务</n-text>
              </div>
            </template>
            <template v-else>
              <n-empty description="暂无任务">
                <template #extra>
                  <n-button size="small" @click="goToTasks">添加任务</n-button>
                </template>
              </n-empty>
            </template>
          </n-card>
        </n-grid-item>
      </n-grid>

      <!-- 错误任务提示 -->
      <n-card
        v-if="taskStore.errorCount > 0"
        class="error-card"
        style="margin-top: 16px"
      >
        <n-space align="center">
          <n-icon size="20" color="#e88080"><AlertCircleOutline /></n-icon>
          <n-text type="error">
            {{ taskStore.errorCount }} 个任务存在错误，请检查任务配置
          </n-text>
          <n-button size="small" text type="primary" @click="goToTasks">
            查看详情
          </n-button>
        </n-space>
      </n-card>
    </n-spin>
  </div>
</template>

<style scoped>
.dashboard {
  max-width: 1400px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.page-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.stat-card {
  height: 140px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.stat-value {
  font-size: 28px;
  font-weight: 600;
  line-height: 1.2;
}

.list-card {
  min-height: 300px;
}

.change-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.change-item {
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.04);
  border-radius: 6px;
  transition: background 0.2s;
}

.change-item:hover {
  background: rgba(255, 255, 255, 0.08);
}

.task-name {
  font-size: 14px;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.more-hint {
  text-align: center;
  margin-top: 12px;
}

.error-card {
  background: rgba(232, 128, 128, 0.1);
}
</style>
