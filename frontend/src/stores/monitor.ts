import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useMonitorStore = defineStore('monitor', () => {
  // 状态
  const isRunning = ref(false)
  const loading = ref(false)
  const activeTasks = ref(0)
  const totalTasks = ref(0)
  const totalChanges = ref(0)

  // 获取监控状态
  const fetchStatus = async () => {
    try {
      const response = await axios.get('/api/monitor/status')
      if (response.data.code === 0) {
        isRunning.value = response.data.data.is_running
      }
    } catch (error) {
      console.error('获取监控状态失败:', error)
    }

    // 获取统计数据
    try {
      const statsResponse = await axios.get('/api/monitor/stats')
      if (statsResponse.data.code === 0) {
        const stats = statsResponse.data.data
        activeTasks.value = stats.active_tasks || 0
        totalTasks.value = stats.total_tasks || 0
        totalChanges.value = stats.total_changes || 0
      }
    } catch (error) {
      console.error('获取统计数据失败:', error)
    }
  }

  // 启动监控
  const startMonitor = async () => {
    loading.value = true
    try {
      const response = await axios.post('/api/monitor/start')
      if (response.data.code === 0) {
        isRunning.value = true
      }
    } catch (error) {
      console.error('启动监控失败:', error)
    } finally {
      loading.value = false
    }
  }

  // 停止监控
  const stopMonitor = async () => {
    loading.value = true
    try {
      const response = await axios.post('/api/monitor/stop')
      if (response.data.code === 0) {
        isRunning.value = false
      }
    } catch (error) {
      console.error('停止监控失败:', error)
    } finally {
      loading.value = false
    }
  }

  return {
    isRunning,
    loading,
    activeTasks,
    totalTasks,
    totalChanges,
    fetchStatus,
    startMonitor,
    stopMonitor,
  }
})
