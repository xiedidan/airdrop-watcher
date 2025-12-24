import axios from 'axios'
import type {
  ApiResponse,
  TaskListResponse,
  Task,
  TaskCreate,
  TaskUpdate,
  MonitorStatus,
  SchedulerStats,
  HistoryListResponse,
  HistoryEntry,
  ChangeDetails,
  HistoryStatistics,
  AllSettings,
  SettingsResponse,
  SettingsSectionResponse,
  PlatformInfo,
  MonitoringConfig,
  DetectionConfig,
  NotificationConfig,
  AIConfig,
  StorageConfig,
  LoggingConfig,
  SchedulerConfig,
  AboutInfo,
} from '@/types'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// 响应拦截器
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

/**
 * 任务 API
 */
export const taskApi = {
  // 获取任务列表
  async list(): Promise<TaskListResponse> {
    const response = await api.get<ApiResponse<TaskListResponse>>('/tasks')
    return response.data.data
  },

  // 获取单个任务
  async get(id: string): Promise<Task> {
    const response = await api.get<ApiResponse<Task>>(`/tasks/${id}`)
    return response.data.data
  },

  // 创建任务
  async create(data: TaskCreate): Promise<Task> {
    const response = await api.post<ApiResponse<{ task: Task }>>('/tasks', data)
    return response.data.data.task
  },

  // 更新任务
  async update(id: string, data: TaskUpdate): Promise<Task> {
    const response = await api.put<ApiResponse<{ task: Task }>>(`/tasks/${id}`, data)
    return response.data.data.task
  },

  // 删除任务
  async delete(id: string): Promise<void> {
    await api.delete(`/tasks/${id}`)
  },

  // 启用任务
  async enable(id: string): Promise<Task> {
    const response = await api.post<ApiResponse<{ task: Task }>>(`/tasks/${id}/enable`)
    return response.data.data.task
  },

  // 禁用任务
  async disable(id: string): Promise<Task> {
    const response = await api.post<ApiResponse<{ task: Task }>>(`/tasks/${id}/disable`)
    return response.data.data.task
  },

  // 立即检测
  async check(id: string): Promise<{ changed: boolean; error?: string }> {
    const response = await api.post<ApiResponse<{ changed: boolean; error?: string }>>(`/tasks/${id}/check`)
    return response.data.data
  },
}

/**
 * 监控 API
 */
export const monitorApi = {
  // 获取监控状态
  async status(): Promise<MonitorStatus> {
    const response = await api.get<ApiResponse<MonitorStatus>>('/monitor/status')
    return response.data.data
  },

  // 获取调度器统计
  async stats(): Promise<SchedulerStats> {
    const response = await api.get<ApiResponse<SchedulerStats>>('/monitor/stats')
    return response.data.data
  },

  // 启动监控
  async start(): Promise<MonitorStatus> {
    const response = await api.post<ApiResponse<{ status: MonitorStatus }>>('/monitor/start')
    return response.data.data.status
  },

  // 停止监控
  async stop(): Promise<MonitorStatus> {
    const response = await api.post<ApiResponse<{ status: MonitorStatus }>>('/monitor/stop')
    return response.data.data.status
  },
}

/**
 * 历史记录 API
 */
export const historyApi = {
  // 获取历史记录列表
  async list(params?: {
    task_id?: string
    entry_type?: string
    page?: number
    page_size?: number
  }): Promise<HistoryListResponse> {
    const response = await api.get<HistoryListResponse>('/history', { params })
    return response.data
  },

  // 搜索历史记录
  async search(params?: {
    task_id?: string
    keyword?: string
    start_date?: string
    end_date?: string
    success_only?: boolean
    changed_only?: boolean
    entry_type?: string
    page?: number
    page_size?: number
  }): Promise<HistoryListResponse> {
    const response = await api.get<HistoryListResponse>('/history/search', { params })
    return response.data
  },

  // 获取单条历史记录详情
  async get(id: string): Promise<HistoryEntry> {
    const response = await api.get<HistoryEntry>(`/history/entry/${id}`)
    return response.data
  },

  // 获取变化详情
  async getChangeDetails(id: string): Promise<ChangeDetails> {
    const response = await api.get<ChangeDetails>(`/history/change-details/${id}`)
    return response.data
  },

  // 获取统计信息
  async getStatistics(taskId?: string): Promise<HistoryStatistics> {
    const response = await api.get<HistoryStatistics>('/history/statistics', {
      params: taskId ? { task_id: taskId } : undefined
    })
    return response.data
  },

  // 获取最近变化
  async getRecentChanges(limit: number = 10): Promise<HistoryListResponse> {
    const response = await api.get<HistoryListResponse>('/history/recent-changes', {
      params: { limit }
    })
    return response.data
  },

  // 清理历史记录
  async cleanup(days?: number): Promise<{ success: boolean; message: string; removed_count: number }> {
    const response = await api.delete<{ success: boolean; message: string; removed_count: number }>('/history/cleanup', {
      params: days ? { days } : undefined
    })
    return response.data
  },
}

/**
 * 配置管理 API
 */
export const settingsApi = {
  // 获取所有配置
  async getAll(maskSecrets: boolean = true): Promise<AllSettings> {
    const response = await api.get<SettingsResponse>('/settings', {
      params: { mask_secrets: maskSecrets }
    })
    return response.data.data
  },

  // 获取指定配置段
  async getSection<T = Record<string, any>>(section: string, maskSecrets: boolean = true): Promise<T> {
    const response = await api.get<SettingsSectionResponse>(`/settings/${section}`, {
      params: { mask_secrets: maskSecrets }
    })
    return response.data.data as T
  },

  // 更新监控配置
  async updateMonitoring(config: Partial<MonitoringConfig>): Promise<MonitoringConfig> {
    const response = await api.put<ApiResponse<MonitoringConfig>>('/settings/monitoring', config)
    return response.data.data
  },

  // 更新检测配置
  async updateDetection(config: Partial<DetectionConfig>): Promise<DetectionConfig> {
    const response = await api.put<ApiResponse<DetectionConfig>>('/settings/detection', config)
    return response.data.data
  },

  // 更新通知配置
  async updateNotification(config: Partial<NotificationConfig>): Promise<NotificationConfig> {
    const response = await api.put<ApiResponse<NotificationConfig>>('/settings/notification', config)
    return response.data.data
  },

  // 获取通知平台列表
  async getNotificationPlatforms(): Promise<PlatformInfo[]> {
    const response = await api.get<ApiResponse<{ platforms: PlatformInfo[] }>>('/settings/notification/platforms')
    return response.data.data.platforms
  },

  // 更新单个平台配置
  async updatePlatformConfig(platform: string, config: Record<string, any>, enable?: boolean): Promise<void> {
    await api.put(`/settings/notification/platforms/${platform}`, config, {
      params: enable !== undefined ? { enable } : undefined
    })
  },

  // 更新 AI 配置
  async updateAI(config: Partial<AIConfig>): Promise<AIConfig> {
    const response = await api.put<ApiResponse<AIConfig>>('/settings/ai', config)
    return response.data.data
  },

  // 更新存储配置
  async updateStorage(config: Partial<StorageConfig>): Promise<StorageConfig> {
    const response = await api.put<ApiResponse<StorageConfig>>('/settings/storage', config)
    return response.data.data
  },

  // 更新日志配置
  async updateLogging(config: Partial<LoggingConfig>): Promise<LoggingConfig> {
    const response = await api.put<ApiResponse<LoggingConfig>>('/settings/logging', config)
    return response.data.data
  },

  // 更新调度器配置
  async updateScheduler(config: Partial<SchedulerConfig>): Promise<SchedulerConfig> {
    const response = await api.put<ApiResponse<SchedulerConfig>>('/settings/scheduler', config)
    return response.data.data
  },

  // 重置配置段
  async resetSection(section: string): Promise<Record<string, any>> {
    const response = await api.post<ApiResponse<Record<string, any>>>(`/settings/${section}/reset`)
    return response.data.data
  },
}

/**
 * 通知测试结果
 */
export interface PlatformTestResult {
  platform: string
  success: boolean
  message: string
  error?: string
}

/**
 * 测试通知响应
 */
export interface TestNotificationResponse {
  success: boolean
  message: string
  results: PlatformTestResult[]
  total_platforms: number
  success_count: number
}

/**
 * 通知 API
 */
export const notificationApi = {
  // 测试通知
  async test(platform?: string, title?: string, message?: string): Promise<TestNotificationResponse> {
    const response = await api.post<TestNotificationResponse>('/notification/test', {
      platform,
      title,
      message
    })
    return response.data
  },

  // 测试所有平台
  async testAll(): Promise<TestNotificationResponse> {
    const response = await api.post<TestNotificationResponse>('/notification/test-all')
    return response.data
  },

  // 获取可用平台
  async getPlatforms(): Promise<{
    enabled_platforms: string[]
    configured_platforms: string[]
    platform_status: Record<string, any>
  }> {
    const response = await api.get<ApiResponse<{
      enabled_platforms: string[]
      configured_platforms: string[]
      platform_status: Record<string, any>
    }>>('/notification/platforms')
    return response.data.data
  },

  // 获取平台信息
  async getPlatformInfo(platform: string): Promise<Record<string, any>> {
    const response = await api.get<ApiResponse<Record<string, any>>>(`/notification/platforms/${platform}/info`)
    return response.data.data
  },
}

/**
 * 关于 API
 */
export const aboutApi = {
  // 获取关于信息
  async getInfo(): Promise<AboutInfo> {
    const response = await api.get<AboutInfo>('/about')
    return response.data
  },

  // 获取版本号
  async getVersion(): Promise<string> {
    const response = await api.get<{ version: string }>('/about/version')
    return response.data.version
  },
}

export default api
