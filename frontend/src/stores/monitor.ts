import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { monitorApi } from '@/api'
import type { MonitorStatus, SchedulerStats } from '@/types'

export const useMonitorStore = defineStore('monitor', () => {
  // 状态
  const status = ref<MonitorStatus | null>(null)
  const stats = ref<SchedulerStats | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // 计算属性
  const isRunning = computed(() => status.value?.is_running ?? false)
  const totalTasks = computed(() => status.value?.total_tasks ?? 0)
  const activeTasks = computed(() => status.value?.active_tasks ?? 0)
  const runningTasks = computed(() => status.value?.running_tasks ?? 0)
  const totalChanges = computed(() => status.value?.total_changes ?? 0)
  const totalExecutions = computed(() => status.value?.total_executions ?? 0)
  const successfulExecutions = computed(() => status.value?.successful_executions ?? 0)
  const failedExecutions = computed(() => status.value?.failed_executions ?? 0)
  const uptime = computed(() => status.value?.uptime ?? 0)
  const nextCheck = computed(() => status.value?.next_check ?? null)

  // 获取监控状态
  const fetchStatus = async () => {
    try {
      error.value = null
      status.value = await monitorApi.status()
    } catch (e) {
      error.value = '获取监控状态失败'
      console.error('获取监控状态失败:', e)
    }
  }

  // 获取调度器统计
  const fetchStats = async () => {
    try {
      stats.value = await monitorApi.stats()
    } catch (e) {
      console.error('获取调度器统计失败:', e)
    }
  }

  // 刷新所有数据
  const refresh = async () => {
    await Promise.all([fetchStatus(), fetchStats()])
  }

  // 启动监控
  const startMonitor = async () => {
    loading.value = true
    error.value = null
    try {
      status.value = await monitorApi.start()
      return true
    } catch (e) {
      error.value = '启动监控失败'
      console.error('启动监控失败:', e)
      return false
    } finally {
      loading.value = false
    }
  }

  // 停止监控
  const stopMonitor = async () => {
    loading.value = true
    error.value = null
    try {
      status.value = await monitorApi.stop()
      return true
    } catch (e) {
      error.value = '停止监控失败'
      console.error('停止监控失败:', e)
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    // 状态
    status,
    stats,
    loading,
    error,

    // 计算属性
    isRunning,
    totalTasks,
    activeTasks,
    runningTasks,
    totalChanges,
    totalExecutions,
    successfulExecutions,
    failedExecutions,
    uptime,
    nextCheck,

    // 方法
    fetchStatus,
    fetchStats,
    refresh,
    startMonitor,
    stopMonitor,
  }
})
