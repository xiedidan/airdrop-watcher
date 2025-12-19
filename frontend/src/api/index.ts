import axios from 'axios'
import type { ApiResponse, TaskListResponse, Task, TaskCreate, TaskUpdate, MonitorStatus, SchedulerStats, HistoryListResponse, HistoryItem } from '@/types'

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
  async list(params?: { task_id?: string; limit?: number; offset?: number }): Promise<HistoryListResponse> {
    const response = await api.get<ApiResponse<HistoryListResponse>>('/history', { params })
    return response.data.data
  },

  // 获取单条历史记录详情
  async get(id: string): Promise<HistoryItem> {
    const response = await api.get<ApiResponse<HistoryItem>>(`/history/${id}`)
    return response.data.data
  },
}

export default api
