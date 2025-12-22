/**
 * SSE 事件 Store
 *
 * 集中管理 SSE 连接，将事件分发到其他 Store。
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useSSE } from '@/composables/useSSE'
import { useMonitorStore } from './monitor'
import { useTaskStore } from './task'
import { SSEEventType, SSEConnectionState } from '@/types'
import type { SSEEventData, Task, MonitorStatus, SSEConnectionStateValue } from '@/types'

export const useSSEStore = defineStore('sse', () => {
  // SSE 连接实例
  let sseInstance: ReturnType<typeof useSSE> | null = null

  // 状态
  const connectionState = ref<SSEConnectionStateValue>(SSEConnectionState.DISCONNECTED)
  const lastEventTime = ref<string | null>(null)
  const eventCount = ref(0)

  // 最近事件队列（用于调试和展示）
  const recentEvents = ref<Array<{ type: string; data: SSEEventData; time: string }>>([])
  const maxRecentEvents = 50

  // 计算属性
  const isConnected = computed(() => connectionState.value === SSEConnectionState.CONNECTED)
  const isConnecting = computed(() => connectionState.value === SSEConnectionState.CONNECTING)

  /**
   * 处理 SSE 事件
   */
  function handleEvent(eventType: string, data: SSEEventData) {
    eventCount.value++
    lastEventTime.value = data.timestamp || new Date().toISOString()

    // 添加到最近事件队列
    recentEvents.value.unshift({
      type: eventType,
      data,
      time: lastEventTime.value,
    })
    if (recentEvents.value.length > maxRecentEvents) {
      recentEvents.value.pop()
    }

    // 根据事件类型分发到相应 Store
    switch (eventType) {
      // 心跳事件（忽略）
      case SSEEventType.HEARTBEAT:
        break

      // 监控状态事件
      case SSEEventType.MONITOR_STARTED:
      case SSEEventType.MONITOR_STOPPED:
      case SSEEventType.MONITOR_STATUS:
        handleMonitorEvent(eventType, data)
        break

      // 任务事件
      case SSEEventType.TASK_CREATED:
      case SSEEventType.TASK_UPDATED:
      case SSEEventType.TASK_DELETED:
      case SSEEventType.TASK_ENABLED:
      case SSEEventType.TASK_DISABLED:
        handleTaskEvent(eventType, data)
        break

      // 检测事件
      case SSEEventType.CHECK_STARTED:
      case SSEEventType.CHECK_COMPLETED:
      case SSEEventType.CHECK_FAILED:
      case SSEEventType.CHANGE_DETECTED:
        handleCheckEvent(eventType, data)
        break

      // 通知事件
      case SSEEventType.NOTIFICATION_SENT:
      case SSEEventType.NOTIFICATION_FAILED:
        handleNotificationEvent(eventType, data)
        break

      default:
        console.log('[SSE Store] 未知事件类型:', eventType, data)
    }
  }

  /**
   * 处理监控状态事件
   */
  function handleMonitorEvent(eventType: string, data: SSEEventData) {
    const monitorStore = useMonitorStore()

    switch (eventType) {
      case SSEEventType.MONITOR_STARTED:
        // 刷新监控状态
        monitorStore.fetchStatus()
        break

      case SSEEventType.MONITOR_STOPPED:
        // 刷新监控状态
        monitorStore.fetchStatus()
        break

      case SSEEventType.MONITOR_STATUS:
        // 直接更新状态（如果数据完整）
        if (data.status) {
          monitorStore.status = data.status as MonitorStatus
        } else {
          monitorStore.fetchStatus()
        }
        break
    }
  }

  /**
   * 处理任务事件
   */
  function handleTaskEvent(eventType: string, data: SSEEventData) {
    const taskStore = useTaskStore()

    switch (eventType) {
      case SSEEventType.TASK_CREATED:
        // 刷新任务列表
        taskStore.fetchTasks()
        break

      case SSEEventType.TASK_UPDATED:
      case SSEEventType.TASK_ENABLED:
      case SSEEventType.TASK_DISABLED:
        // 更新单个任务
        if (data.task) {
          const task = data.task as Task
          const index = taskStore.tasks.findIndex(t => t.id === task.id)
          if (index !== -1) {
            taskStore.tasks[index] = task
          }
        } else {
          taskStore.fetchTasks()
        }
        break

      case SSEEventType.TASK_DELETED:
        // 从列表中移除任务
        if (data.task_id) {
          taskStore.tasks = taskStore.tasks.filter(t => t.id !== data.task_id)
        } else {
          taskStore.fetchTasks()
        }
        break
    }
  }

  /**
   * 处理检测事件
   */
  function handleCheckEvent(eventType: string, data: SSEEventData) {
    const taskStore = useTaskStore()
    const monitorStore = useMonitorStore()

    switch (eventType) {
      case SSEEventType.CHECK_STARTED:
        // 更新任务状态为检测中
        if (data.task_id) {
          const task = taskStore.tasks.find(t => t.id === data.task_id)
          if (task) {
            task.status = 'checking'
          }
        }
        break

      case SSEEventType.CHECK_COMPLETED:
        // 更新任务最后检测时间
        if (data.task_id) {
          const task = taskStore.tasks.find(t => t.id === data.task_id)
          if (task) {
            task.status = 'active'
            task.last_check = data.timestamp || new Date().toISOString()
            if (data.changed) {
              task.change_count = (task.change_count || 0) + 1
              task.last_change = task.last_check
            }
          }
        }
        // 更新监控统计
        monitorStore.fetchStatus()
        break

      case SSEEventType.CHECK_FAILED:
        // 更新任务错误状态
        if (data.task_id) {
          const task = taskStore.tasks.find(t => t.id === data.task_id)
          if (task) {
            task.status = 'error'
            task.error_count = (task.error_count || 0) + 1
            task.last_error = data.timestamp || new Date().toISOString()
            task.last_error_message = data.error || '检测失败'
          }
        }
        break

      case SSEEventType.CHANGE_DETECTED:
        // 变化检测到，刷新相关数据
        if (data.task_id) {
          const task = taskStore.tasks.find(t => t.id === data.task_id)
          if (task) {
            task.change_count = (task.change_count || 0) + 1
            task.last_change = data.timestamp || new Date().toISOString()
          }
        }
        // 刷新监控状态以更新变化计数
        monitorStore.fetchStatus()
        break
    }
  }

  /**
   * 处理通知事件
   */
  function handleNotificationEvent(eventType: string, data: SSEEventData) {
    // 通知事件目前只记录日志
    if (eventType === SSEEventType.NOTIFICATION_SENT) {
      console.log('[SSE Store] 通知已发送:', data)
    } else if (eventType === SSEEventType.NOTIFICATION_FAILED) {
      console.warn('[SSE Store] 通知发送失败:', data)
    }
  }

  /**
   * 初始化 SSE 连接
   */
  function init() {
    if (sseInstance) {
      console.log('[SSE Store] 已初始化，跳过')
      return
    }

    sseInstance = useSSE('/api/events', {
      autoReconnect: true,
      reconnectDelay: 3000,
      maxReconnectAttempts: 10,
      onEvent: handleEvent,
      onConnect: () => {
        connectionState.value = SSEConnectionState.CONNECTED
        console.log('[SSE Store] 连接成功')
      },
      onDisconnect: () => {
        connectionState.value = SSEConnectionState.DISCONNECTED
        console.log('[SSE Store] 连接断开')
      },
      onError: () => {
        connectionState.value = SSEConnectionState.ERROR
      },
    })

    sseInstance.connect()
  }

  /**
   * 断开 SSE 连接
   */
  function disconnect() {
    if (sseInstance) {
      sseInstance.disconnect()
      sseInstance = null
    }
    connectionState.value = SSEConnectionState.DISCONNECTED
  }

  /**
   * 重新连接
   */
  function reconnect() {
    if (sseInstance) {
      sseInstance.reconnect()
    } else {
      init()
    }
  }

  /**
   * 清除最近事件
   */
  function clearRecentEvents() {
    recentEvents.value = []
  }

  return {
    // 状态
    connectionState,
    lastEventTime,
    eventCount,
    recentEvents,

    // 计算属性
    isConnected,
    isConnecting,

    // 方法
    init,
    disconnect,
    reconnect,
    clearRecentEvents,
  }
})
