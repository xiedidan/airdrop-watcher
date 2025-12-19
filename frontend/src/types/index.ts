/**
 * 通用 API 响应结构
 */
export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

/**
 * 任务模型
 */
export interface Task {
  id: string
  url: string
  name: string
  description: string
  selectors: string[]
  interval: number
  timeout: number
  enabled: boolean
  ai_prompt: string

  // 时间戳
  created_at: string | null
  updated_at: string | null
  last_check: string | null
  last_change: string | null

  // 统计信息
  change_count: number
  status: string

  // 错误信息
  error_count: number
  last_error: string | null
  last_error_message: string | null
}

/**
 * 任务列表响应
 */
export interface TaskListResponse {
  items: Task[]
  total: number
}

/**
 * 创建任务请求
 */
export interface TaskCreate {
  url: string
  name: string
  description?: string
  selectors?: string[]
  interval?: number
  timeout?: number
  enabled?: boolean
  ai_prompt?: string
}

/**
 * 更新任务请求
 */
export interface TaskUpdate {
  url?: string
  name?: string
  description?: string
  selectors?: string[]
  interval?: number
  timeout?: number
  enabled?: boolean
  ai_prompt?: string
}

/**
 * 监控状态
 */
export interface MonitorStatus {
  status: string
  is_running: boolean
  start_time: string | null
  uptime: number

  // 任务统计
  total_tasks: number
  active_tasks: number
  running_tasks: number

  // 执行统计
  total_executions: number
  successful_executions: number
  failed_executions: number
  total_changes: number

  // 下次执行
  next_check: string | null
}

/**
 * 调度器统计
 */
export interface SchedulerStats {
  total_executions: number
  successful_executions: number
  failed_executions: number
  total_changes: number
  start_time: string | null
  uptime: number
  max_concurrent_tasks: number
  default_interval: number
}

/**
 * 历史记录项
 */
export interface HistoryItem {
  id: string
  task_id: string
  task_name: string
  url: string
  timestamp: string
  change_type: string
  summary: string | null
  ai_summary: string | null
}

/**
 * 历史记录列表响应
 */
export interface HistoryListResponse {
  items: HistoryItem[]
  total: number
}
