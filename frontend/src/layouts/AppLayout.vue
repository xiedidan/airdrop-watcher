<script setup lang="ts">
import { h, ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { NLayout, NLayoutHeader, NLayoutContent, NLayoutFooter, NMenu, NIcon, NSpace, NButton, NBadge, NText, NTooltip } from 'naive-ui'
import {
  HomeOutline,
  ListOutline,
  TimeOutline,
  SettingsOutline,
  PlayCircleOutline,
  StopCircleOutline,
  WifiOutline,
  CloudOfflineOutline,
  EllipseOutline,
} from '@vicons/ionicons5'
import { useMonitorStore } from '@/stores/monitor'
import { useTaskStore } from '@/stores/task'
import { useSSEStore } from '@/stores/sse'
import { SSEConnectionState } from '@/types'
import type { SSEConnectionStateValue } from '@/types'

const router = useRouter()
const route = useRoute()
const monitorStore = useMonitorStore()
const taskStore = useTaskStore()
const sseStore = useSSEStore()

// 当前时间（用于相对时间计算）
const now = ref(new Date())
let timeUpdateInterval: ReturnType<typeof setInterval> | null = null

// 菜单项
const menuOptions = [
  {
    label: '仪表盘',
    key: '/',
    icon: () => h(NIcon, null, { default: () => h(HomeOutline) }),
  },
  {
    label: '任务管理',
    key: '/tasks',
    icon: () => h(NIcon, null, { default: () => h(ListOutline) }),
  },
  {
    label: '变化历史',
    key: '/history',
    icon: () => h(NIcon, null, { default: () => h(TimeOutline) }),
  },
  {
    label: '系统设置',
    key: '/settings',
    icon: () => h(NIcon, null, { default: () => h(SettingsOutline) }),
  },
]

// 当前选中的菜单
const activeKey = computed(() => route.path)

// 菜单点击
const handleMenuClick = (key: string) => {
  router.push(key)
}

// 监控控制
const handleToggleMonitor = async () => {
  if (monitorStore.isRunning) {
    await monitorStore.stopMonitor()
  } else {
    await monitorStore.startMonitor()
  }
}

// 初始化获取状态
monitorStore.fetchStatus()
taskStore.fetchTasks()

// 最近变化时间（从任务列表中获取最新的变化时间）
const lastChangeTime = computed(() => {
  const tasksWithChanges = taskStore.tasks.filter(t => t.last_change)
  if (tasksWithChanges.length === 0) return null

  const latestTask = tasksWithChanges.reduce((latest, current) => {
    const latestTime = new Date(latest.last_change || 0).getTime()
    const currentTime = new Date(current.last_change || 0).getTime()
    return currentTime > latestTime ? current : latest
  })

  return latestTask.last_change
})

// 格式化相对时间
const formatRelativeTime = (dateStr: string | null): string => {
  if (!dateStr) return '无'

  const date = new Date(dateStr)
  const diffMs = now.value.getTime() - date.getTime()
  const diffSeconds = Math.floor(diffMs / 1000)
  const diffMinutes = Math.floor(diffSeconds / 60)
  const diffHours = Math.floor(diffMinutes / 60)
  const diffDays = Math.floor(diffHours / 24)

  if (diffSeconds < 60) return '刚刚'
  if (diffMinutes < 60) return `${diffMinutes}分钟前`
  if (diffHours < 24) return `${diffHours}小时前`
  if (diffDays < 30) return `${diffDays}天前`

  return date.toLocaleDateString('zh-CN')
}

// 监控状态文本
const monitorStatusText = computed(() => {
  return monitorStore.isRunning ? '运行中' : '已停止'
})

// SSE 连接状态信息
const sseStatusText = computed(() => {
  switch (sseStore.connectionState) {
    case SSEConnectionState.CONNECTED:
      return '实时连接'
    case SSEConnectionState.CONNECTING:
      return '连接中...'
    case SSEConnectionState.ERROR:
      return '连接错误'
    default:
      return '未连接'
  }
})

const sseStatusType = computed(() => {
  switch (sseStore.connectionState) {
    case SSEConnectionState.CONNECTED:
      return 'success'
    case SSEConnectionState.CONNECTING:
      return 'warning'
    case SSEConnectionState.ERROR:
      return 'error'
    default:
      return 'default'
  }
})

// 初始化 SSE 连接
onMounted(() => {
  sseStore.init()
  // 每分钟更新一次当前时间（用于相对时间计算）
  timeUpdateInterval = setInterval(() => {
    now.value = new Date()
  }, 60000)
})

onUnmounted(() => {
  if (timeUpdateInterval) {
    clearInterval(timeUpdateInterval)
    timeUpdateInterval = null
  }
})
</script>

<template>
  <n-layout class="app-layout" position="absolute">
    <!-- 顶部导航 -->
    <n-layout-header bordered class="app-header">
      <div class="header-left">
        <span class="logo">WebMon</span>
        <n-menu
          mode="horizontal"
          :value="activeKey"
          :options="menuOptions"
          @update:value="handleMenuClick"
        />
      </div>
      <div class="header-right">
        <n-space align="center">
          <n-badge :dot="monitorStore.isRunning" :type="monitorStore.isRunning ? 'success' : 'default'">
            <n-text :type="monitorStore.isRunning ? 'success' : 'default'">
              {{ monitorStore.isRunning ? '运行中' : '已停止' }}
            </n-text>
          </n-badge>
          <n-button
            :type="monitorStore.isRunning ? 'error' : 'success'"
            size="small"
            @click="handleToggleMonitor"
            :loading="monitorStore.loading"
          >
            <template #icon>
              <n-icon>
                <StopCircleOutline v-if="monitorStore.isRunning" />
                <PlayCircleOutline v-else />
              </n-icon>
            </template>
            {{ monitorStore.isRunning ? '停止' : '启动' }}
          </n-button>
        </n-space>
      </div>
    </n-layout-header>

    <!-- 主内容区 -->
    <n-layout-content class="app-content">
      <router-view />
    </n-layout-content>

    <!-- 底部状态栏 -->
    <n-layout-footer bordered class="app-footer">
      <n-space justify="space-between" style="width: 100%">
        <n-space align="center" :size="16">
          <!-- 监控状态 -->
          <n-tooltip trigger="hover">
            <template #trigger>
              <n-space align="center" :size="4" style="cursor: pointer;">
                <span
                  class="status-dot"
                  :class="monitorStore.isRunning ? 'status-running' : 'status-stopped'"
                ></span>
                <n-text :type="monitorStore.isRunning ? 'success' : 'default'">
                  {{ monitorStatusText }}
                </n-text>
              </n-space>
            </template>
            <span>监控状态: {{ monitorStatusText }}</span>
          </n-tooltip>

          <n-text depth="3">|</n-text>

          <!-- 任务统计 -->
          <n-tooltip trigger="hover">
            <template #trigger>
              <n-text depth="3" style="cursor: pointer;">
                任务: {{ taskStore.activeCount }}/{{ taskStore.total }}
              </n-text>
            </template>
            <span>活跃任务 {{ taskStore.activeCount }} / 总任务 {{ taskStore.total }}</span>
          </n-tooltip>

          <n-text depth="3">|</n-text>

          <!-- 最近变化 -->
          <n-tooltip trigger="hover">
            <template #trigger>
              <n-text depth="3" style="cursor: pointer;">
                最近变化: {{ formatRelativeTime(lastChangeTime) }}
              </n-text>
            </template>
            <span v-if="lastChangeTime">{{ new Date(lastChangeTime).toLocaleString('zh-CN') }}</span>
            <span v-else>暂无变化记录</span>
          </n-tooltip>

          <n-text depth="3">|</n-text>

          <!-- SSE 连接状态 -->
          <n-tooltip trigger="hover">
            <template #trigger>
              <n-text :type="sseStatusType" style="cursor: pointer;">
                <n-icon size="14" style="vertical-align: middle; margin-right: 4px;">
                  <WifiOutline v-if="sseStore.isConnected" />
                  <CloudOfflineOutline v-else />
                </n-icon>
                {{ sseStatusText }}
              </n-text>
            </template>
            <span>SSE 事件流 - 接收事件: {{ sseStore.eventCount }}</span>
          </n-tooltip>
        </n-space>
        <n-text depth="3">WebMon v1.0.0</n-text>
      </n-space>
    </n-layout-footer>
  </n-layout>
</template>

<style scoped>
.app-layout {
  height: 100vh;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  height: 64px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 24px;
}

.logo {
  font-size: 20px;
  font-weight: bold;
  color: #63e2b7;
}

.header-right {
  display: flex;
  align-items: center;
}

.app-content {
  padding: 24px;
  overflow: auto;
}

.app-footer {
  padding: 12px 24px;
}

/* 状态指示器 */
.status-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 2px;
}

.status-running {
  background-color: #63e2b7;
  box-shadow: 0 0 8px rgba(99, 226, 183, 0.6);
  animation: pulse 2s ease-in-out infinite;
}

.status-stopped {
  background-color: #6c757d;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style>
