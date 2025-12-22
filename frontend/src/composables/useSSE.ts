/**
 * SSE 连接管理 Composable
 *
 * 提供与后端 SSE 事件流的连接管理和事件处理。
 */

import { ref, onUnmounted, readonly } from 'vue'
import { SSEConnectionState, SSEEventType } from '@/types'
import type { SSEEventData, SSEConnectionStateValue } from '@/types'

export interface SSEOptions {
  /** 自动重连 */
  autoReconnect?: boolean
  /** 重连延迟（毫秒） */
  reconnectDelay?: number
  /** 最大重连次数 */
  maxReconnectAttempts?: number
  /** 事件处理回调 */
  onEvent?: (eventType: string, data: SSEEventData) => void
  /** 连接成功回调 */
  onConnect?: () => void
  /** 断开连接回调 */
  onDisconnect?: () => void
  /** 错误回调 */
  onError?: (error: Event) => void
}

const DEFAULT_OPTIONS: Required<Pick<SSEOptions, 'autoReconnect' | 'reconnectDelay' | 'maxReconnectAttempts'>> = {
  autoReconnect: true,
  reconnectDelay: 3000,
  maxReconnectAttempts: 10,
}

/**
 * SSE 连接管理 Composable
 *
 * @param url SSE 端点 URL
 * @param options 配置选项
 */
export function useSSE(url: string = '/api/events', options: SSEOptions = {}) {
  const mergedOptions = { ...DEFAULT_OPTIONS, ...options }

  // 状态
  const connectionState = ref<SSEConnectionStateValue>(SSEConnectionState.DISCONNECTED)
  const lastEventId = ref<string | null>(null)
  const reconnectAttempts = ref(0)

  // 内部变量
  let eventSource: EventSource | null = null
  let reconnectTimer: ReturnType<typeof setTimeout> | null = null

  /**
   * 连接到 SSE 端点
   */
  function connect() {
    if (eventSource?.readyState === EventSource.OPEN) {
      console.log('[SSE] 已经连接')
      return
    }

    connectionState.value = SSEConnectionState.CONNECTING

    try {
      // 构建 URL，包含最后的事件 ID 以支持断点续传
      const connectUrl = lastEventId.value
        ? `${url}?last_event_id=${lastEventId.value}`
        : url

      eventSource = new EventSource(connectUrl)

      // 连接打开
      eventSource.onopen = () => {
        console.log('[SSE] 连接已建立')
        connectionState.value = SSEConnectionState.CONNECTED
        reconnectAttempts.value = 0
        mergedOptions.onConnect?.()
      }

      // 通用消息处理
      eventSource.onmessage = (event) => {
        handleEvent('message', event)
      }

      // 错误处理
      eventSource.onerror = (error) => {
        console.error('[SSE] 连接错误:', error)
        connectionState.value = SSEConnectionState.ERROR
        mergedOptions.onError?.(error)

        // 关闭当前连接
        eventSource?.close()
        eventSource = null

        // 自动重连
        if (mergedOptions.autoReconnect) {
          scheduleReconnect()
        } else {
          connectionState.value = SSEConnectionState.DISCONNECTED
          mergedOptions.onDisconnect?.()
        }
      }

      // 注册特定事件类型的监听器
      registerEventListeners()
    } catch (error) {
      console.error('[SSE] 创建连接失败:', error)
      connectionState.value = SSEConnectionState.ERROR
    }
  }

  /**
   * 注册各事件类型的监听器
   */
  function registerEventListeners() {
    if (!eventSource) return

    // 为所有已知事件类型注册监听器
    Object.values(SSEEventType).forEach((eventType) => {
      eventSource!.addEventListener(eventType, (event: MessageEvent) => {
        handleEvent(eventType, event)
      })
    })
  }

  /**
   * 处理接收到的事件
   */
  function handleEvent(eventType: string, event: MessageEvent) {
    try {
      // 更新最后事件 ID
      if (event.lastEventId) {
        lastEventId.value = event.lastEventId
      }

      // 解析事件数据
      const data: SSEEventData = JSON.parse(event.data)

      // 调用事件回调
      mergedOptions.onEvent?.(eventType, data)
    } catch (error) {
      console.error('[SSE] 解析事件数据失败:', error, event.data)
    }
  }

  /**
   * 安排重连
   */
  function scheduleReconnect() {
    if (reconnectTimer) {
      clearTimeout(reconnectTimer)
    }

    if (reconnectAttempts.value >= mergedOptions.maxReconnectAttempts) {
      console.error('[SSE] 已达最大重连次数，停止重连')
      connectionState.value = SSEConnectionState.DISCONNECTED
      mergedOptions.onDisconnect?.()
      return
    }

    reconnectAttempts.value++
    const delay = mergedOptions.reconnectDelay * Math.min(reconnectAttempts.value, 5) // 指数退避，最多5倍

    console.log(`[SSE] ${delay / 1000}秒后尝试第${reconnectAttempts.value}次重连...`)

    reconnectTimer = setTimeout(() => {
      connect()
    }, delay)
  }

  /**
   * 断开连接
   */
  function disconnect() {
    if (reconnectTimer) {
      clearTimeout(reconnectTimer)
      reconnectTimer = null
    }

    if (eventSource) {
      eventSource.close()
      eventSource = null
    }

    connectionState.value = SSEConnectionState.DISCONNECTED
    mergedOptions.onDisconnect?.()
    console.log('[SSE] 连接已断开')
  }

  /**
   * 重新连接
   */
  function reconnect() {
    disconnect()
    reconnectAttempts.value = 0
    connect()
  }

  // 组件卸载时清理
  onUnmounted(() => {
    disconnect()
  })

  return {
    // 状态（只读）
    connectionState: readonly(connectionState),
    lastEventId: readonly(lastEventId),
    reconnectAttempts: readonly(reconnectAttempts),

    // 计算属性
    isConnected: () => connectionState.value === SSEConnectionState.CONNECTED,
    isConnecting: () => connectionState.value === SSEConnectionState.CONNECTING,

    // 方法
    connect,
    disconnect,
    reconnect,
  }
}
