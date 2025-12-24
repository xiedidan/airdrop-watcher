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

/**
 * SSE 事件类型
 */
export const SSEEventType = {
  // 连接事件
  CONNECTED: 'connected',
  HEARTBEAT: 'heartbeat',

  // 监控状态事件
  MONITOR_STARTED: 'monitor_started',
  MONITOR_STOPPED: 'monitor_stopped',
  MONITOR_STATUS: 'monitor_status',

  // 任务事件
  TASK_CREATED: 'task_created',
  TASK_UPDATED: 'task_updated',
  TASK_DELETED: 'task_deleted',
  TASK_ENABLED: 'task_enabled',
  TASK_DISABLED: 'task_disabled',

  // 检测事件
  CHECK_STARTED: 'check_started',
  CHECK_COMPLETED: 'check_completed',
  CHECK_FAILED: 'check_failed',
  CHANGE_DETECTED: 'change_detected',

  // 通知事件
  NOTIFICATION_SENT: 'notification_sent',
  NOTIFICATION_FAILED: 'notification_failed',
} as const

export type SSEEventTypeValue = typeof SSEEventType[keyof typeof SSEEventType]

/**
 * SSE 事件数据
 */
export interface SSEEventData {
  timestamp: string
  [key: string]: any
}

/**
 * SSE 连接状态
 */
export const SSEConnectionState = {
  CONNECTING: 'connecting',
  CONNECTED: 'connected',
  DISCONNECTED: 'disconnected',
  ERROR: 'error',
} as const

export type SSEConnectionStateValue = typeof SSEConnectionState[keyof typeof SSEConnectionState]

// ==================== Settings 配置类型 ====================

/**
 * 速率限制配置
 */
export interface RateLimitConfig {
  requests_per_minute: number
  retry_delay: number
}

/**
 * 监控配置
 */
export interface MonitoringConfig {
  default_interval: number
  default_timeout: number
  max_retries: number
  concurrent_tasks: number
  browser_headless: boolean
  rate_limit?: RateLimitConfig
}

/**
 * 检测配置
 */
export interface DetectionConfig {
  enable_smart_detection: boolean
  similarity_threshold: number
  min_change_length: number
  ignore_selectors: string[]
  extract_fields: Record<string, string>
}

/**
 * 通知配置
 */
export interface NotificationConfig {
  enabled_platforms: string[]
  templates: Record<string, string>
  platform_configs: Record<string, Record<string, any>>
}

/**
 * 平台信息
 */
export interface PlatformInfo {
  name: string
  enabled: boolean
  in_enabled_list: boolean
  config: Record<string, any>
}

/**
 * AI 配置
 */
export interface AIConfig {
  enabled: boolean
  api_url: string
  api_key: string
  model: string
  max_tokens: number
  temperature: number
  timeout: number
  retry_attempts: number
  retry_base_delay: number
  retry_max_delay: number
  system_prompt: string
  user_prompt_template: string
}

/**
 * 存储配置
 */
export interface StorageConfig {
  history_file: string
  max_history_entries: number
  auto_cleanup_days: number
}

/**
 * 日志轮转配置
 */
export interface LogRotationConfig {
  type: string
  interval: number
  retention_days: number
  max_size: number
  backup_count: number
}

/**
 * 日志配置
 */
export interface LoggingConfig {
  level: string
  log_dir: string
  rotation?: LogRotationConfig
  handlers: string[]
  compression: boolean
  async_mode: boolean
  buffer_size: number
}

/**
 * 调度器性能配置
 */
export interface SchedulerPerformanceConfig {
  max_concurrent_tasks: number
  max_browser_resources: number
  scheduler_loop_interval: number
}

/**
 * 调度器重试配置
 */
export interface SchedulerRetryConfig {
  retry_attempts: number
  retry_delay: number
}

/**
 * 调度器配置
 */
export interface SchedulerConfig {
  performance?: SchedulerPerformanceConfig
  retry?: SchedulerRetryConfig
}

/**
 * 所有配置
 */
export interface AllSettings {
  monitoring?: MonitoringConfig
  detection?: DetectionConfig
  notification?: NotificationConfig
  ai?: AIConfig
  storage?: StorageConfig
  logging?: LoggingConfig
  scheduler?: SchedulerConfig
}

/**
 * 配置响应
 */
export interface SettingsResponse {
  success: boolean
  message: string
  data: AllSettings
}

/**
 * 配置段响应
 */
export interface SettingsSectionResponse {
  success: boolean
  message: string
  section: string
  data: Record<string, any>
}

// ==================== About 关于页面类型 ====================

/**
 * 依赖信息
 */
export interface DependencyInfo {
  name: string
  version: string
  description: string
}

/**
 * 系统信息
 */
export interface SystemInfo {
  python_version: string
  platform: string
  platform_version: string
}

/**
 * 项目链接
 */
export interface ProjectLinks {
  repository: string
  documentation: string
  issues: string
}

/**
 * 关于信息响应
 */
export interface AboutInfo {
  name: string
  description: string
  version: string
  author: string
  license: string
  links: ProjectLinks
  system: SystemInfo
  dependencies: DependencyInfo[]
  timestamp: string
}
