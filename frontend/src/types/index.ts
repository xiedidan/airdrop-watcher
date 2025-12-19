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
 * 历史记录条目（来自后端API）
 */
export interface HistoryEntry {
  id: string
  type: 'check_result' | 'change_details'
  task_id: string
  url: string
  timestamp: string
  data: Record<string, any>
}

/**
 * 检测结果
 */
export interface CheckResult {
  id: string
  task_id: string
  url: string
  timestamp: string | null
  success: boolean
  content_hash: string
  content_size: number
  load_time: number
  changed: boolean
  change_type: string
  content_diff: string | null
  added_lines: number
  removed_lines: number
  modified_lines: number
  changes_summary: string | null
  change_details: Record<string, any>[]
  error_message: string | null
  error_type: string | null
  content_preview: string | null
  status_code: number | null
}

/**
 * 变化详情
 */
export interface ChangeDetails {
  id: string
  task_id: string
  url: string
  timestamp: string | null
  change_type: string
  change_summary: string | null
  old_content: string | null
  new_content: string | null
  diff: string | null
  ai_summary: string | null
}

/**
 * 历史记录列表响应
 */
export interface HistoryListResponse {
  items: HistoryEntry[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

/**
 * 历史统计信息
 */
export interface HistoryStatistics {
  total_entries: number
  check_results: number
  change_details: number
  success_rate: number
  change_rate: number
  first_date: string | null
  last_date: string | null
}
