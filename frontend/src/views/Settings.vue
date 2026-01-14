<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import {
  NCard,
  NTabs,
  NTabPane,
  NForm,
  NFormItem,
  NInput,
  NInputNumber,
  NSwitch,
  NButton,
  NSpace,
  NSelect,
  NDynamicTags,
  NAlert,
  NDescriptions,
  NDescriptionsItem,
  NCollapse,
  NCollapseItem,
  NSpin,
  NIcon,
  NTag,
  NTooltip,
  NSlider,
  NDivider,
  NText,
  NA,
  NList,
  NListItem,
  NThing,
  NModal,
  NPopconfirm,
  NEmpty,
  NCode,
  NScrollbar,
} from 'naive-ui'
import {
  SettingsOutline,
  NotificationsOutline,
  SparklesOutline,
  ServerOutline,
  DocumentTextOutline,
  TimeOutline,
  RefreshOutline,
  SaveOutline,
  InformationCircleOutline,
  LogoGithub,
  BookOutline,
  BugOutline,
  HeartOutline,
  CodeSlashOutline,
  AddOutline,
  CreateOutline,
  TrashOutline,
  PlayOutline,
  PauseOutline,
  FlashOutline,
} from '@vicons/ionicons5'
import { settingsApi, notificationApi, aboutApi, hookApi } from '@/api'
import { message, dialog } from '@/utils/discrete'
import type {
  AllSettings,
  MonitoringConfig,
  DetectionConfig,
  NotificationConfig,
  AIConfig,
  StorageConfig,
  LoggingConfig,
  SchedulerConfig,
  PlatformInfo,
  AboutInfo,
  HookConfig,
  HookResult,
  TriggerInfo,
} from '@/types'
import type { PlatformTestResult } from '@/api'

// 加载状态
const loading = ref(true)
const saving = ref(false)
const testingNotification = ref(false)

// 当前活动标签
const activeTab = ref('monitoring')

// 配置数据
const settings = reactive<AllSettings>({})
const platforms = ref<PlatformInfo[]>([])
const aboutInfo = ref<AboutInfo | null>(null)

// 表单数据（用于编辑，带默认值防止空指针）
const monitoringForm = reactive<Partial<MonitoringConfig>>({
  rate_limit: { requests_per_minute: 30, retry_delay: 60 }
})
const detectionForm = reactive<Partial<DetectionConfig>>({
  ignore_selectors: []
})
const notificationForm = reactive<Partial<NotificationConfig>>({
  enabled_platforms: []
})
const aiForm = reactive<Partial<AIConfig>>({})
const storageForm = reactive<Partial<StorageConfig>>({})
const loggingForm = reactive<Partial<LoggingConfig>>({
  rotation: { type: 'time', interval: 7, retention_days: 30, max_size: 10485760, backup_count: 5 }
})
const schedulerForm = reactive<Partial<SchedulerConfig>>({
  performance: { max_concurrent_tasks: 15, max_browser_resources: 8, scheduler_loop_interval: 0.2 },
  retry: { retry_attempts: 5, retry_delay: 120 }
})

// AI 提示词占位符说明
const promptPlaceholders = [
  { name: '{task_name}', description: '任务名称' },
  { name: '{url}', description: '监控的 URL 地址' },
  { name: '{description}', description: '任务描述' },
  { name: '{changes}', description: '变化内容' },
  { name: '{old_content}', description: '旧内容' },
  { name: '{new_content}', description: '新内容' },
]

// 日志级别选项
const logLevelOptions = [
  { label: 'DEBUG', value: 'DEBUG' },
  { label: 'INFO', value: 'INFO' },
  { label: 'WARNING', value: 'WARNING' },
  { label: 'ERROR', value: 'ERROR' },
  { label: 'CRITICAL', value: 'CRITICAL' },
]

// ==================== Hook 相关 ====================

// Hook 数据
const hooksEnabled = ref(false)
const hooks = ref<Record<string, HookConfig[]>>({})
const hookDefaults = ref<Record<string, any>>({})
const triggers = ref<TriggerInfo[]>([])
const loadingHooks = ref(false)
const testingHook = ref<string | null>(null)

// Hook 弹窗状态
const showHookModal = ref(false)
const hookModalMode = ref<'add' | 'edit'>('add')
const editingHook = ref<HookConfig | null>(null)
const editingHookTrigger = ref<string>('')

// Hook 测试结果弹窗
const showTestResultModal = ref(false)
const testResult = ref<HookResult | null>(null)

// Hook 表单
const hookForm = reactive<{
  name: string
  type: 'shell' | 'python'
  script: string
  trigger: string
  enabled: boolean
  timeout: number
  async: boolean
  args: string
  env: string
  condition: string
  working_dir: string
  max_retries: number
}>({
  name: '',
  type: 'shell',
  script: '',
  trigger: 'on_change_detected',
  enabled: true,
  timeout: 30,
  async: true,
  args: '',
  env: '',
  condition: '',
  working_dir: '',
  max_retries: 0,
})

// 脚本类型选项
const scriptTypeOptions = [
  { label: 'Shell', value: 'shell' },
  { label: 'Python', value: 'python' },
]

// 加载 Hook 配置
async function loadHooks() {
  loadingHooks.value = true
  try {
    const response = await hookApi.list()
    hooks.value = response.hooks
    hooksEnabled.value = response.enabled
    hookDefaults.value = response.defaults
    triggers.value = await hookApi.getTriggers()
  } catch (error) {
    console.error('加载 Hook 配置失败:', error)
    message.error('加载 Hook 配置失败')
  } finally {
    loadingHooks.value = false
  }
}

// 触发点选项
const triggerOptions = computed(() =>
  triggers.value.map(t => ({
    label: `${t.name} - ${t.description}`,
    value: t.name,
  }))
)

// 所有 Hook 列表
const allHooks = computed(() => {
  const result: Array<{ trigger: string; hook: HookConfig }> = []
  for (const [trigger, hookList] of Object.entries(hooks.value)) {
    for (const hook of hookList) {
      result.push({ trigger, hook })
    }
  }
  return result
})

// 切换全局 Hook 开关
async function toggleGlobalHooks() {
  try {
    const newState = await hookApi.toggleGlobal()
    hooksEnabled.value = newState
    message.success(newState ? 'Hook 功能已启用' : 'Hook 功能已禁用')
  } catch (error) {
    console.error('切换 Hook 状态失败:', error)
    message.error('操作失败')
  }
}

// 打开添加 Hook 弹窗
function openAddHookModal() {
  hookModalMode.value = 'add'
  editingHook.value = null
  editingHookTrigger.value = ''
  Object.assign(hookForm, {
    name: '',
    type: 'shell',
    script: '',
    trigger: 'on_change_detected',
    enabled: true,
    timeout: hookDefaults.value.timeout || 30,
    async: hookDefaults.value.async !== false,
    args: '',
    env: '',
    condition: '',
    working_dir: '',
    max_retries: hookDefaults.value.max_retries || 0,
  })
  showHookModal.value = true
}

// 打开编辑 Hook 弹窗
function openEditHookModal(trigger: string, hook: HookConfig) {
  hookModalMode.value = 'edit'
  editingHook.value = hook
  editingHookTrigger.value = trigger
  Object.assign(hookForm, {
    name: hook.name,
    type: hook.type,
    script: hook.script,
    trigger: trigger,
    enabled: hook.enabled,
    timeout: hook.timeout,
    async: hook.async,
    args: hook.args.join(', '),
    env: Object.entries(hook.env).map(([k, v]) => `${k}=${v}`).join('\n'),
    condition: hook.condition || '',
    working_dir: hook.working_dir || '',
    max_retries: hook.max_retries,
  })
  showHookModal.value = true
}

// 保存 Hook
async function saveHook() {
  saving.value = true
  try {
    const hookConfig: HookConfig = {
      name: hookForm.name,
      type: hookForm.type,
      script: hookForm.script,
      enabled: hookForm.enabled,
      timeout: hookForm.timeout,
      async: hookForm.async,
      args: hookForm.args ? hookForm.args.split(',').map(s => s.trim()).filter(Boolean) : [],
      env: hookForm.env
        ? Object.fromEntries(
            hookForm.env.split('\n')
              .map(line => line.trim())
              .filter(Boolean)
              .map(line => {
                const idx = line.indexOf('=')
                return idx > 0 ? [line.slice(0, idx), line.slice(idx + 1)] : [line, '']
              })
          )
        : {},
      condition: hookForm.condition || undefined,
      working_dir: hookForm.working_dir || undefined,
      max_retries: hookForm.max_retries,
    }

    if (hookModalMode.value === 'add') {
      await hookApi.create({
        trigger: hookForm.trigger,
        hook: hookConfig,
      })
      message.success('Hook 已添加')
    } else {
      await hookApi.update(editingHook.value!.name, hookConfig)
      message.success('Hook 已更新')
    }

    showHookModal.value = false
    await loadHooks()
  } catch (error: any) {
    console.error('保存 Hook 失败:', error)
    message.error(error.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

// 删除 Hook
async function deleteHook(hookName: string) {
  try {
    await hookApi.delete(hookName)
    message.success('Hook 已删除')
    await loadHooks()
  } catch (error) {
    console.error('删除 Hook 失败:', error)
    message.error('删除失败')
  }
}

// 切换 Hook 启用状态
async function toggleHook(hookName: string) {
  try {
    const newState = await hookApi.toggle(hookName)
    message.success(newState ? 'Hook 已启用' : 'Hook 已禁用')
    await loadHooks()
  } catch (error) {
    console.error('切换 Hook 状态失败:', error)
    message.error('操作失败')
  }
}

// 测试 Hook
async function testHook(hookName: string) {
  testingHook.value = hookName
  try {
    const response = await hookApi.test(hookName)
    if (response.result) {
      testResult.value = response.result
      showTestResultModal.value = true
    }
    if (response.success) {
      message.success('测试成功')
    } else {
      message.warning(response.message)
    }
  } catch (error: any) {
    console.error('测试 Hook 失败:', error)
    message.error(error.response?.data?.detail || '测试失败')
  } finally {
    testingHook.value = null
  }
}

// 获取触发点描述
function getTriggerDescription(trigger: string): string {
  const t = triggers.value.find(t => t.name === trigger)
  return t?.description || trigger
}

// 加载所有配置
async function loadSettings() {
  loading.value = true
  try {
    const data = await settingsApi.getAll()
    Object.assign(settings, data)

    // 初始化表单数据
    if (data.monitoring) Object.assign(monitoringForm, data.monitoring)
    if (data.detection) Object.assign(detectionForm, data.detection)
    if (data.notification) Object.assign(notificationForm, data.notification)
    if (data.ai) Object.assign(aiForm, data.ai)
    if (data.storage) Object.assign(storageForm, data.storage)
    if (data.logging) Object.assign(loggingForm, data.logging)
    if (data.scheduler) Object.assign(schedulerForm, data.scheduler)

    // 加载平台列表
    platforms.value = await settingsApi.getNotificationPlatforms()

    // 加载关于信息
    aboutInfo.value = await aboutApi.getInfo()
  } catch (error) {
    console.error('加载配置失败:', error)
    message.error('加载配置失败')
  } finally {
    loading.value = false
  }
}

// 保存监控配置
async function saveMonitoring() {
  saving.value = true
  try {
    await settingsApi.updateMonitoring(monitoringForm)
    message.success('监控配置已保存')
  } catch (error) {
    console.error('保存失败:', error)
    message.error('保存失败')
  } finally {
    saving.value = false
  }
}

// 保存检测配置
async function saveDetection() {
  saving.value = true
  try {
    await settingsApi.updateDetection(detectionForm)
    message.success('检测配置已保存')
  } catch (error) {
    console.error('保存失败:', error)
    message.error('保存失败')
  } finally {
    saving.value = false
  }
}

// 保存通知配置
async function saveNotification() {
  saving.value = true
  try {
    await settingsApi.updateNotification(notificationForm)
    message.success('通知配置已保存')
  } catch (error) {
    console.error('保存失败:', error)
    message.error('保存失败')
  } finally {
    saving.value = false
  }
}

// 测试通知
async function testNotification(platform?: string) {
  testingNotification.value = true
  try {
    const result = await notificationApi.test(platform)

    if (result.success) {
      message.success(result.message)
    } else {
      message.warning(result.message)
    }

    // 显示详细结果
    if (result.results && result.results.length > 0) {
      const details = result.results
        .map((r: PlatformTestResult) => `${r.platform}: ${r.success ? '成功' : '失败'}${r.error ? ` - ${r.error}` : ''}`)
        .join('\n')

      dialog.info({
        title: '通知测试结果',
        content: details,
        positiveText: '确定'
      })
    }
  } catch (error) {
    console.error('测试失败:', error)
    message.error('测试通知失败')
  } finally {
    testingNotification.value = false
  }
}

// 保存 AI 配置
async function saveAI() {
  saving.value = true
  try {
    await settingsApi.updateAI(aiForm)
    message.success('AI 配置已保存')
  } catch (error) {
    console.error('保存失败:', error)
    message.error('保存失败')
  } finally {
    saving.value = false
  }
}

// 保存存储配置
async function saveStorage() {
  saving.value = true
  try {
    await settingsApi.updateStorage(storageForm)
    message.success('存储配置已保存')
  } catch (error) {
    console.error('保存失败:', error)
    message.error('保存失败')
  } finally {
    saving.value = false
  }
}

// 保存日志配置
async function saveLogging() {
  saving.value = true
  try {
    await settingsApi.updateLogging(loggingForm)
    message.success('日志配置已保存')
  } catch (error) {
    console.error('保存失败:', error)
    message.error('保存失败')
  } finally {
    saving.value = false
  }
}

// 保存调度器配置
async function saveScheduler() {
  saving.value = true
  try {
    await settingsApi.updateScheduler(schedulerForm)
    message.success('调度器配置已保存')
  } catch (error) {
    console.error('保存失败:', error)
    message.error('保存失败')
  } finally {
    saving.value = false
  }
}

// 重置配置段
async function resetSection(section: string) {
  dialog.warning({
    title: '确认重置',
    content: `确定要将 ${getSectionName(section)} 重置为默认值吗？`,
    positiveText: '确定',
    negativeText: '取消',
    onPositiveClick: async () => {
      try {
        const data = await settingsApi.resetSection(section)
        // 更新对应的表单数据
        switch (section) {
          case 'monitoring':
            Object.assign(monitoringForm, data)
            break
          case 'detection':
            Object.assign(detectionForm, data)
            break
          case 'notification':
            Object.assign(notificationForm, data)
            break
          case 'ai':
            Object.assign(aiForm, data)
            break
          case 'storage':
            Object.assign(storageForm, data)
            break
          case 'logging':
            Object.assign(loggingForm, data)
            break
          case 'scheduler':
            Object.assign(schedulerForm, data)
            break
        }
        message.success('配置已重置为默认值')
      } catch (error) {
        console.error('重置失败:', error)
        message.error('重置失败')
      }
    },
  })
}

// 获取配置段名称
function getSectionName(section: string): string {
  const names: Record<string, string> = {
    monitoring: '监控配置',
    detection: '检测配置',
    notification: '通知配置',
    ai: 'AI 配置',
    storage: '存储配置',
    logging: '日志配置',
    scheduler: '调度器配置',
  }
  return names[section] || section
}

// 格式化时间间隔
function formatInterval(seconds: number): string {
  if (seconds < 60) return `${seconds} 秒`
  if (seconds < 3600) return `${Math.floor(seconds / 60)} 分钟`
  return `${Math.floor(seconds / 3600)} 小时`
}

onMounted(() => {
  loadSettings()
  loadHooks()
})
</script>

<template>
  <div class="settings">
    <n-spin :show="loading">
      <n-card title="系统设置" :bordered="false">
        <template #header-extra>
          <n-button text @click="loadSettings">
            <template #icon>
              <n-icon><RefreshOutline /></n-icon>
            </template>
            刷新
          </n-button>
        </template>

        <n-tabs v-model:value="activeTab" type="line" animated>
          <!-- 监控配置 -->
          <n-tab-pane name="monitoring" tab="监控配置">
            <template #tab>
              <n-space align="center" :size="4">
                <n-icon><SettingsOutline /></n-icon>
                <span>监控配置</span>
              </n-space>
            </template>

            <n-form label-placement="left" label-width="140px" :show-feedback="false">
              <n-form-item label="默认检测间隔">
                <n-input-number
                  v-model:value="monitoringForm.default_interval"
                  :min="10"
                  :max="86400"
                  :step="60"
                  style="width: 200px"
                />
                <n-text depth="3" style="margin-left: 12px">
                  {{ formatInterval(monitoringForm.default_interval || 300) }}
                </n-text>
              </n-form-item>

              <n-form-item label="默认超时时间">
                <n-input-number
                  v-model:value="monitoringForm.default_timeout"
                  :min="1000"
                  :max="120000"
                  :step="1000"
                  style="width: 200px"
                />
                <n-text depth="3" style="margin-left: 12px">毫秒</n-text>
              </n-form-item>

              <n-form-item label="最大重试次数">
                <n-input-number
                  v-model:value="monitoringForm.max_retries"
                  :min="0"
                  :max="10"
                  style="width: 200px"
                />
              </n-form-item>

              <n-form-item label="并发任务数">
                <n-input-number
                  v-model:value="monitoringForm.concurrent_tasks"
                  :min="1"
                  :max="50"
                  style="width: 200px"
                />
              </n-form-item>

              <n-form-item label="浏览器无头模式">
                <n-switch v-model:value="monitoringForm.browser_headless" />
              </n-form-item>

              <n-divider />

              <n-form-item label="速率限制">
                <n-space vertical>
                  <n-space align="center">
                    <n-text>每分钟请求数:</n-text>
                    <n-input-number
                      v-model:value="monitoringForm.rate_limit!.requests_per_minute"
                      :min="1"
                      :max="1000"
                      style="width: 120px"
                    />
                  </n-space>
                  <n-space align="center">
                    <n-text>重试延迟 (秒):</n-text>
                    <n-input-number
                      v-model:value="monitoringForm.rate_limit!.retry_delay"
                      :min="1"
                      :max="3600"
                      style="width: 120px"
                    />
                  </n-space>
                </n-space>
              </n-form-item>

              <n-form-item>
                <n-space>
                  <n-button type="primary" :loading="saving" @click="saveMonitoring">
                    <template #icon>
                      <n-icon><SaveOutline /></n-icon>
                    </template>
                    保存
                  </n-button>
                  <n-button @click="resetSection('monitoring')">重置为默认值</n-button>
                </n-space>
              </n-form-item>
            </n-form>
          </n-tab-pane>

          <!-- 检测配置 -->
          <n-tab-pane name="detection" tab="检测配置">
            <template #tab>
              <n-space align="center" :size="4">
                <n-icon><DocumentTextOutline /></n-icon>
                <span>检测配置</span>
              </n-space>
            </template>

            <n-form label-placement="left" label-width="140px" :show-feedback="false">
              <n-form-item label="启用智能检测">
                <n-switch v-model:value="detectionForm.enable_smart_detection" />
              </n-form-item>

              <n-form-item label="相似度阈值">
                <n-slider
                  v-model:value="detectionForm.similarity_threshold"
                  :min="0"
                  :max="1"
                  :step="0.01"
                  :format-tooltip="(v: number) => `${(v * 100).toFixed(0)}%`"
                  style="width: 300px"
                />
                <n-text depth="3" style="margin-left: 12px">
                  {{ ((detectionForm.similarity_threshold || 0.85) * 100).toFixed(0) }}%
                </n-text>
              </n-form-item>

              <n-form-item label="最小变化长度">
                <n-input-number
                  v-model:value="detectionForm.min_change_length"
                  :min="1"
                  :max="1000"
                  style="width: 200px"
                />
                <n-text depth="3" style="margin-left: 12px">字符</n-text>
              </n-form-item>

              <n-form-item label="忽略的选择器">
                <n-dynamic-tags v-model:value="detectionForm.ignore_selectors" />
              </n-form-item>

              <n-form-item>
                <n-space>
                  <n-button type="primary" :loading="saving" @click="saveDetection">
                    <template #icon>
                      <n-icon><SaveOutline /></n-icon>
                    </template>
                    保存
                  </n-button>
                  <n-button @click="resetSection('detection')">重置为默认值</n-button>
                </n-space>
              </n-form-item>
            </n-form>
          </n-tab-pane>

          <!-- 通知配置 -->
          <n-tab-pane name="notification" tab="通知配置">
            <template #tab>
              <n-space align="center" :size="4">
                <n-icon><NotificationsOutline /></n-icon>
                <span>通知配置</span>
              </n-space>
            </template>

            <n-alert type="info" title="通知平台配置" style="margin-bottom: 16px">
              请在 config.json 或环境变量中配置各平台的 Token/Webhook。支持的占位符格式：${VAR_NAME}
            </n-alert>

            <n-collapse>
              <n-collapse-item
                v-for="platform in platforms"
                :key="platform.name"
                :title="platform.name"
                :name="platform.name"
              >
                <template #header>
                  <n-space align="center">
                    <span style="text-transform: capitalize">{{ platform.name }}</span>
                    <n-tag v-if="platform.enabled" type="success" size="small">已启用</n-tag>
                    <n-tag v-else type="default" size="small">未启用</n-tag>
                  </n-space>
                </template>

                <template #header-extra>
                  <n-button
                    size="small"
                    type="primary"
                    ghost
                    :loading="testingNotification"
                    @click.stop="testNotification(platform.name)"
                  >
                    测试
                  </n-button>
                </template>

                <n-descriptions :column="1" bordered>
                  <n-descriptions-item label="启用状态">
                    {{ platform.enabled ? '已启用' : '未启用' }}
                  </n-descriptions-item>
                  <n-descriptions-item
                    v-for="(value, key) in platform.config"
                    :key="key"
                    :label="String(key)"
                  >
                    <n-text v-if="String(key).includes('token') || String(key).includes('webhook') || String(key).includes('key')">
                      {{ value || '(未配置)' }}
                    </n-text>
                    <span v-else>{{ value }}</span>
                  </n-descriptions-item>
                </n-descriptions>
              </n-collapse-item>
            </n-collapse>

            <n-divider />

            <n-form-item label="已启用的平台">
              <n-select
                v-model:value="notificationForm.enabled_platforms"
                multiple
                :options="platforms.map(p => ({ label: p.name, value: p.name }))"
                placeholder="选择要启用的通知平台"
              />
            </n-form-item>

            <n-form-item>
              <n-space>
                <n-button type="primary" :loading="saving" @click="saveNotification">
                  <template #icon>
                    <n-icon><SaveOutline /></n-icon>
                  </template>
                  保存
                </n-button>
                <n-button
                  type="info"
                  :loading="testingNotification"
                  @click="testNotification()"
                >
                  测试所有平台
                </n-button>
                <n-button @click="resetSection('notification')">重置为默认值</n-button>
              </n-space>
            </n-form-item>
          </n-tab-pane>

          <!-- AI 配置 -->
          <n-tab-pane name="ai" tab="AI 配置">
            <template #tab>
              <n-space align="center" :size="4">
                <n-icon><SparklesOutline /></n-icon>
                <span>AI 配置</span>
              </n-space>
            </template>

            <n-form label-placement="left" label-width="140px" :show-feedback="false">
              <n-form-item label="启用 AI 分析">
                <n-switch v-model:value="aiForm.enabled" />
              </n-form-item>

              <n-form-item label="API 地址">
                <n-input
                  v-model:value="aiForm.api_url"
                  placeholder="https://api.deepseek.com/v1"
                  style="width: 400px"
                />
              </n-form-item>

              <n-form-item label="API Key">
                <n-input
                  v-model:value="aiForm.api_key"
                  type="password"
                  show-password-on="click"
                  placeholder="${AI_API_KEY}"
                  style="width: 400px"
                />
                <n-tooltip>
                  <template #trigger>
                    <n-icon style="margin-left: 8px; cursor: help">
                      <InformationCircleOutline />
                    </n-icon>
                  </template>
                  可使用环境变量占位符 ${AI_API_KEY}
                </n-tooltip>
              </n-form-item>

              <n-form-item label="模型">
                <n-input
                  v-model:value="aiForm.model"
                  placeholder="deepseek-reasoner"
                  style="width: 300px"
                />
              </n-form-item>

              <n-form-item label="最大 Token 数">
                <n-input-number
                  v-model:value="aiForm.max_tokens"
                  :min="100"
                  :max="32000"
                  :step="100"
                  style="width: 200px"
                />
              </n-form-item>

              <n-form-item label="温度参数">
                <n-slider
                  v-model:value="aiForm.temperature"
                  :min="0"
                  :max="2"
                  :step="0.1"
                  style="width: 300px"
                />
                <n-text depth="3" style="margin-left: 12px">{{ aiForm.temperature }}</n-text>
              </n-form-item>

              <n-form-item label="请求超时 (秒)">
                <n-input-number
                  v-model:value="aiForm.timeout"
                  :min="10"
                  :max="600"
                  style="width: 200px"
                />
              </n-form-item>

              <n-form-item label="重试次数">
                <n-input-number
                  v-model:value="aiForm.retry_attempts"
                  :min="0"
                  :max="10"
                  style="width: 200px"
                />
              </n-form-item>

              <n-divider />

              <n-alert type="info" style="margin-bottom: 16px">
                <template #header>提示词占位符说明</template>
                <n-space wrap>
                  <n-tag v-for="p in promptPlaceholders" :key="p.name" type="info">
                    {{ p.name }} - {{ p.description }}
                  </n-tag>
                </n-space>
              </n-alert>

              <n-form-item label="系统提示词">
                <n-input
                  v-model:value="aiForm.system_prompt"
                  type="textarea"
                  :rows="4"
                  placeholder="你是一个网页变化分析助手..."
                  style="width: 100%"
                />
              </n-form-item>

              <n-form-item label="用户提示词模板">
                <n-input
                  v-model:value="aiForm.user_prompt_template"
                  type="textarea"
                  :rows="6"
                  placeholder="请分析以下网页变化：
任务：{task_name}
URL：{url}
描述：{description}
变化内容：{changes}"
                  style="width: 100%"
                />
              </n-form-item>

              <n-form-item>
                <n-space>
                  <n-button type="primary" :loading="saving" @click="saveAI">
                    <template #icon>
                      <n-icon><SaveOutline /></n-icon>
                    </template>
                    保存
                  </n-button>
                  <n-button @click="resetSection('ai')">重置为默认值</n-button>
                </n-space>
              </n-form-item>
            </n-form>
          </n-tab-pane>

          <!-- 存储配置 -->
          <n-tab-pane name="storage" tab="存储配置">
            <template #tab>
              <n-space align="center" :size="4">
                <n-icon><ServerOutline /></n-icon>
                <span>存储配置</span>
              </n-space>
            </template>

            <n-form label-placement="left" label-width="140px" :show-feedback="false">
              <n-form-item label="历史记录文件">
                <n-input
                  v-model:value="storageForm.history_file"
                  placeholder="data/history.json"
                  style="width: 400px"
                />
              </n-form-item>

              <n-form-item label="最大记录数">
                <n-input-number
                  v-model:value="storageForm.max_history_entries"
                  :min="100"
                  :max="100000"
                  :step="100"
                  style="width: 200px"
                />
              </n-form-item>

              <n-form-item label="自动清理天数">
                <n-input-number
                  v-model:value="storageForm.auto_cleanup_days"
                  :min="1"
                  :max="365"
                  style="width: 200px"
                />
                <n-text depth="3" style="margin-left: 12px">天</n-text>
              </n-form-item>

              <n-form-item>
                <n-space>
                  <n-button type="primary" :loading="saving" @click="saveStorage">
                    <template #icon>
                      <n-icon><SaveOutline /></n-icon>
                    </template>
                    保存
                  </n-button>
                  <n-button @click="resetSection('storage')">重置为默认值</n-button>
                </n-space>
              </n-form-item>
            </n-form>
          </n-tab-pane>

          <!-- 日志配置 -->
          <n-tab-pane name="logging" tab="日志配置">
            <template #tab>
              <n-space align="center" :size="4">
                <n-icon><DocumentTextOutline /></n-icon>
                <span>日志配置</span>
              </n-space>
            </template>

            <n-form label-placement="left" label-width="140px" :show-feedback="false">
              <n-form-item label="日志级别">
                <n-select
                  v-model:value="loggingForm.level"
                  :options="logLevelOptions"
                  style="width: 200px"
                />
              </n-form-item>

              <n-form-item label="日志目录">
                <n-input
                  v-model:value="loggingForm.log_dir"
                  placeholder="./logs"
                  style="width: 300px"
                />
              </n-form-item>

              <n-form-item label="日志压缩">
                <n-switch v-model:value="loggingForm.compression" />
              </n-form-item>

              <n-form-item label="异步模式">
                <n-switch v-model:value="loggingForm.async_mode" />
              </n-form-item>

              <n-form-item label="缓冲区大小">
                <n-input-number
                  v-model:value="loggingForm.buffer_size"
                  :min="100"
                  :max="10000"
                  :step="100"
                  style="width: 200px"
                />
              </n-form-item>

              <n-divider>轮转配置</n-divider>

              <n-form-item label="轮转间隔 (天)">
                <n-input-number
                  v-model:value="loggingForm.rotation!.interval"
                  :min="1"
                  :max="365"
                  style="width: 200px"
                  :disabled="!loggingForm.rotation"
                />
              </n-form-item>

              <n-form-item label="保留天数">
                <n-input-number
                  v-model:value="loggingForm.rotation!.retention_days"
                  :min="1"
                  :max="365"
                  style="width: 200px"
                  :disabled="!loggingForm.rotation"
                />
              </n-form-item>

              <n-form-item label="备份文件数">
                <n-input-number
                  v-model:value="loggingForm.rotation!.backup_count"
                  :min="1"
                  :max="100"
                  style="width: 200px"
                  :disabled="!loggingForm.rotation"
                />
              </n-form-item>

              <n-form-item>
                <n-space>
                  <n-button type="primary" :loading="saving" @click="saveLogging">
                    <template #icon>
                      <n-icon><SaveOutline /></n-icon>
                    </template>
                    保存
                  </n-button>
                  <n-button @click="resetSection('logging')">重置为默认值</n-button>
                </n-space>
              </n-form-item>
            </n-form>
          </n-tab-pane>

          <!-- 调度器配置 -->
          <n-tab-pane name="scheduler" tab="调度器配置">
            <template #tab>
              <n-space align="center" :size="4">
                <n-icon><TimeOutline /></n-icon>
                <span>调度器配置</span>
              </n-space>
            </template>

            <n-form label-placement="left" label-width="180px" :show-feedback="false">
              <n-divider>性能配置</n-divider>

              <n-form-item label="最大并发任务数">
                <n-input-number
                  v-model:value="schedulerForm.performance!.max_concurrent_tasks"
                  :min="1"
                  :max="100"
                  style="width: 200px"
                  :disabled="!schedulerForm.performance"
                />
              </n-form-item>

              <n-form-item label="最大浏览器资源数">
                <n-input-number
                  v-model:value="schedulerForm.performance!.max_browser_resources"
                  :min="1"
                  :max="50"
                  style="width: 200px"
                  :disabled="!schedulerForm.performance"
                />
              </n-form-item>

              <n-form-item label="调度循环间隔 (秒)">
                <n-input-number
                  v-model:value="schedulerForm.performance!.scheduler_loop_interval"
                  :min="0.1"
                  :max="5"
                  :step="0.1"
                  style="width: 200px"
                  :disabled="!schedulerForm.performance"
                />
              </n-form-item>

              <n-divider>重试配置</n-divider>

              <n-form-item label="重试次数">
                <n-input-number
                  v-model:value="schedulerForm.retry!.retry_attempts"
                  :min="0"
                  :max="20"
                  style="width: 200px"
                  :disabled="!schedulerForm.retry"
                />
              </n-form-item>

              <n-form-item label="重试延迟 (秒)">
                <n-input-number
                  v-model:value="schedulerForm.retry!.retry_delay"
                  :min="10"
                  :max="3600"
                  style="width: 200px"
                  :disabled="!schedulerForm.retry"
                />
              </n-form-item>

              <n-form-item>
                <n-space>
                  <n-button type="primary" :loading="saving" @click="saveScheduler">
                    <template #icon>
                      <n-icon><SaveOutline /></n-icon>
                    </template>
                    保存
                  </n-button>
                  <n-button @click="resetSection('scheduler')">重置为默认值</n-button>
                </n-space>
              </n-form-item>
            </n-form>
          </n-tab-pane>

          <!-- Hook 配置 -->
          <n-tab-pane name="hooks" tab="Hook 配置">
            <template #tab>
              <n-space align="center" :size="4">
                <n-icon><CodeSlashOutline /></n-icon>
                <span>Hook 配置</span>
              </n-space>
            </template>

            <n-spin :show="loadingHooks">
              <!-- 全局开关 -->
              <n-space align="center" justify="space-between" style="margin-bottom: 16px">
                <n-space align="center">
                  <n-text>Hook 功能</n-text>
                  <n-switch :value="hooksEnabled" @update:value="toggleGlobalHooks" />
                  <n-tag :type="hooksEnabled ? 'success' : 'default'" size="small">
                    {{ hooksEnabled ? '已启用' : '已禁用' }}
                  </n-tag>
                </n-space>
                <n-space>
                  <n-button type="primary" @click="openAddHookModal" :disabled="!hooksEnabled">
                    <template #icon>
                      <n-icon><AddOutline /></n-icon>
                    </template>
                    添加 Hook
                  </n-button>
                  <n-button @click="loadHooks">
                    <template #icon>
                      <n-icon><RefreshOutline /></n-icon>
                    </template>
                    刷新
                  </n-button>
                </n-space>
              </n-space>

              <n-alert v-if="!hooksEnabled" type="info" style="margin-bottom: 16px">
                Hook 功能当前已禁用。启用后可以在页面变化检测时自动执行自定义脚本。
              </n-alert>

              <!-- Hook 列表 -->
              <n-empty v-if="allHooks.length === 0" description="暂无 Hook 配置">
                <template #extra>
                  <n-button size="small" @click="openAddHookModal" :disabled="!hooksEnabled">
                    添加第一个 Hook
                  </n-button>
                </template>
              </n-empty>

              <n-list v-else bordered>
                <n-list-item v-for="{ trigger, hook } in allHooks" :key="hook.name">
                  <n-thing>
                    <template #header>
                      <n-space align="center">
                        <span class="hook-name">{{ hook.name }}</span>
                        <n-tag :type="hook.enabled ? 'success' : 'default'" size="small">
                          {{ hook.enabled ? '启用' : '禁用' }}
                        </n-tag>
                        <n-tag type="info" size="small">{{ hook.type }}</n-tag>
                        <n-tag v-if="hook.async" type="warning" size="small">异步</n-tag>
                      </n-space>
                    </template>
                    <template #header-extra>
                      <n-space>
                        <n-tooltip>
                          <template #trigger>
                            <n-button
                              size="small"
                              quaternary
                              type="info"
                              :loading="testingHook === hook.name"
                              @click="testHook(hook.name)"
                            >
                              <template #icon>
                                <n-icon><FlashOutline /></n-icon>
                              </template>
                            </n-button>
                          </template>
                          测试
                        </n-tooltip>
                        <n-tooltip>
                          <template #trigger>
                            <n-button
                              size="small"
                              quaternary
                              :type="hook.enabled ? 'warning' : 'success'"
                              @click="toggleHook(hook.name)"
                            >
                              <template #icon>
                                <n-icon>
                                  <PauseOutline v-if="hook.enabled" />
                                  <PlayOutline v-else />
                                </n-icon>
                              </template>
                            </n-button>
                          </template>
                          {{ hook.enabled ? '禁用' : '启用' }}
                        </n-tooltip>
                        <n-tooltip>
                          <template #trigger>
                            <n-button
                              size="small"
                              quaternary
                              type="primary"
                              @click="openEditHookModal(trigger, hook)"
                            >
                              <template #icon>
                                <n-icon><CreateOutline /></n-icon>
                              </template>
                            </n-button>
                          </template>
                          编辑
                        </n-tooltip>
                        <n-popconfirm @positive-click="deleteHook(hook.name)">
                          <template #trigger>
                            <n-button size="small" quaternary type="error">
                              <template #icon>
                                <n-icon><TrashOutline /></n-icon>
                              </template>
                            </n-button>
                          </template>
                          确定要删除 Hook "{{ hook.name }}" 吗？
                        </n-popconfirm>
                      </n-space>
                    </template>
                    <template #description>
                      <n-space vertical :size="4">
                        <n-text depth="3">
                          <n-icon><CodeSlashOutline /></n-icon>
                          {{ hook.script }}
                        </n-text>
                        <n-text depth="3">
                          触发点: {{ getTriggerDescription(trigger) }}
                        </n-text>
                        <n-space v-if="hook.condition">
                          <n-text depth="3">条件: {{ hook.condition }}</n-text>
                        </n-space>
                      </n-space>
                    </template>
                  </n-thing>
                </n-list-item>
              </n-list>

              <!-- Hook 说明 -->
              <n-divider />
              <n-alert type="info" title="Hook 使用说明">
                <n-space vertical :size="4">
                  <n-text>Hook 是在特定事件发生时自动执行的脚本，支持 Shell 和 Python。</n-text>
                  <n-text>脚本会通过环境变量和 stdin 接收上下文数据（JSON 格式）。</n-text>
                  <n-text>脚本路径支持绝对路径或相对于项目 hooks/ 目录的路径。</n-text>
                </n-space>
              </n-alert>
            </n-spin>
          </n-tab-pane>

          <!-- 关于 -->
          <n-tab-pane name="about" tab="关于">
            <template #tab>
              <n-space align="center" :size="4">
                <n-icon><InformationCircleOutline /></n-icon>
                <span>关于</span>
              </n-space>
            </template>

            <div v-if="aboutInfo" class="about-content">
              <!-- 项目信息卡片 -->
              <n-card class="about-card" :bordered="false">
                <div class="project-header">
                  <h1 class="project-name">{{ aboutInfo.name }}</h1>
                  <n-tag type="primary" size="large">v{{ aboutInfo.version }}</n-tag>
                </div>
                <p class="project-description">{{ aboutInfo.description }}</p>

                <n-divider />

                <!-- 项目链接 -->
                <div class="project-links">
                  <n-space :size="16">
                    <n-button
                      tag="a"
                      :href="aboutInfo.links.repository"
                      target="_blank"
                      type="default"
                      secondary
                    >
                      <template #icon>
                        <n-icon><LogoGithub /></n-icon>
                      </template>
                      GitHub
                    </n-button>
                    <n-button
                      tag="a"
                      :href="aboutInfo.links.documentation"
                      target="_blank"
                      type="default"
                      secondary
                    >
                      <template #icon>
                        <n-icon><BookOutline /></n-icon>
                      </template>
                      文档
                    </n-button>
                    <n-button
                      tag="a"
                      :href="aboutInfo.links.issues"
                      target="_blank"
                      type="default"
                      secondary
                    >
                      <template #icon>
                        <n-icon><BugOutline /></n-icon>
                      </template>
                      反馈问题
                    </n-button>
                  </n-space>
                </div>
              </n-card>

              <!-- 系统信息 -->
              <n-card title="系统信息" class="about-card" :bordered="false">
                <n-descriptions :column="2" label-placement="left" bordered>
                  <n-descriptions-item label="Python 版本">
                    {{ aboutInfo.system.python_version }}
                  </n-descriptions-item>
                  <n-descriptions-item label="操作系统">
                    {{ aboutInfo.system.platform }}
                  </n-descriptions-item>
                  <n-descriptions-item label="系统版本">
                    {{ aboutInfo.system.platform_version }}
                  </n-descriptions-item>
                  <n-descriptions-item label="许可证">
                    {{ aboutInfo.license }}
                  </n-descriptions-item>
                </n-descriptions>
              </n-card>

              <!-- 核心依赖 -->
              <n-card title="核心依赖" class="about-card" :bordered="false">
                <n-list bordered>
                  <n-list-item v-for="dep in aboutInfo.dependencies" :key="dep.name">
                    <n-thing>
                      <template #header>
                        <n-space align="center">
                          <span class="dep-name">{{ dep.name }}</span>
                          <n-tag type="info" size="small">{{ dep.version }}</n-tag>
                        </n-space>
                      </template>
                      <template #description>
                        <n-text depth="3">{{ dep.description }}</n-text>
                      </template>
                    </n-thing>
                  </n-list-item>
                </n-list>
              </n-card>

              <!-- 致谢 -->
              <n-card class="about-card" :bordered="false">
                <n-space align="center" justify="center" class="thanks">
                  <n-icon color="#f5222d" size="18"><HeartOutline /></n-icon>
                  <n-text depth="2">感谢所有开源项目贡献者</n-text>
                </n-space>
              </n-card>
            </div>

            <n-spin v-else :show="loading">
              <div style="height: 200px"></div>
            </n-spin>
          </n-tab-pane>
        </n-tabs>
      </n-card>
    </n-spin>

    <!-- Hook 编辑弹窗 -->
    <n-modal
      v-model:show="showHookModal"
      :title="hookModalMode === 'add' ? '添加 Hook' : '编辑 Hook'"
      preset="card"
      style="width: 650px"
      :mask-closable="false"
    >
      <n-form label-placement="left" label-width="100">
        <n-form-item label="Hook 名称" required>
          <n-input
            v-model:value="hookForm.name"
            placeholder="输入 Hook 名称"
            :disabled="hookModalMode === 'edit'"
          />
        </n-form-item>

        <n-form-item label="触发点" required>
          <n-select
            v-model:value="hookForm.trigger"
            :options="triggerOptions"
            placeholder="选择触发点"
            :disabled="hookModalMode === 'edit'"
          />
        </n-form-item>

        <n-form-item label="脚本类型" required>
          <n-select
            v-model:value="hookForm.type"
            :options="scriptTypeOptions"
            placeholder="选择脚本类型"
          />
        </n-form-item>

        <n-form-item label="脚本路径" required>
          <n-input
            v-model:value="hookForm.script"
            placeholder="hooks/my_script.sh 或绝对路径"
          />
        </n-form-item>

        <n-form-item label="启用状态">
          <n-switch v-model:value="hookForm.enabled" />
        </n-form-item>

        <n-form-item label="异步执行">
          <n-switch v-model:value="hookForm.async" />
          <n-text depth="3" style="margin-left: 12px">
            异步执行不会阻塞后续流程
          </n-text>
        </n-form-item>

        <n-form-item label="超时时间">
          <n-input-number
            v-model:value="hookForm.timeout"
            :min="1"
            :max="300"
            style="width: 150px"
          />
          <n-text depth="3" style="margin-left: 12px">秒</n-text>
        </n-form-item>

        <n-form-item label="重试次数">
          <n-input-number
            v-model:value="hookForm.max_retries"
            :min="0"
            :max="5"
            style="width: 150px"
          />
        </n-form-item>

        <n-divider style="margin: 16px 0">高级选项</n-divider>

        <n-form-item label="命令行参数">
          <n-input
            v-model:value="hookForm.args"
            placeholder="多个参数用逗号分隔"
          />
        </n-form-item>

        <n-form-item label="环境变量">
          <n-input
            v-model:value="hookForm.env"
            type="textarea"
            :rows="3"
            placeholder="每行一个，格式: KEY=VALUE"
          />
        </n-form-item>

        <n-form-item label="执行条件">
          <n-input
            v-model:value="hookForm.condition"
            placeholder="例如: change_type == 'content_change'"
          />
        </n-form-item>

        <n-form-item label="工作目录">
          <n-input
            v-model:value="hookForm.working_dir"
            placeholder="留空使用项目根目录"
          />
        </n-form-item>
      </n-form>

      <template #footer>
        <n-space justify="end">
          <n-button @click="showHookModal = false">取消</n-button>
          <n-button type="primary" :loading="saving" @click="saveHook">
            {{ hookModalMode === 'add' ? '添加' : '保存' }}
          </n-button>
        </n-space>
      </template>
    </n-modal>

    <!-- Hook 测试结果弹窗 -->
    <n-modal
      v-model:show="showTestResultModal"
      title="Hook 测试结果"
      preset="card"
      style="width: 700px"
    >
      <template v-if="testResult">
        <n-descriptions :column="2" label-placement="left" bordered>
          <n-descriptions-item label="Hook 名称">
            {{ testResult.hook_name }}
          </n-descriptions-item>
          <n-descriptions-item label="执行状态">
            <n-tag :type="testResult.success ? 'success' : 'error'" size="small">
              {{ testResult.success ? '成功' : '失败' }}
            </n-tag>
          </n-descriptions-item>
          <n-descriptions-item label="退出码">
            {{ testResult.exit_code ?? '-' }}
          </n-descriptions-item>
          <n-descriptions-item label="执行耗时">
            {{ testResult.execution_time.toFixed(2) }}s
          </n-descriptions-item>
          <n-descriptions-item v-if="testResult.error_message" label="错误信息" :span="2">
            <n-text type="error">{{ testResult.error_message }}</n-text>
          </n-descriptions-item>
        </n-descriptions>

        <template v-if="testResult.stdout">
          <n-divider>标准输出</n-divider>
          <n-scrollbar style="max-height: 200px">
            <n-code :code="testResult.stdout" language="text" />
          </n-scrollbar>
        </template>

        <template v-if="testResult.stderr">
          <n-divider>标准错误</n-divider>
          <n-scrollbar style="max-height: 200px">
            <n-code :code="testResult.stderr" language="text" />
          </n-scrollbar>
        </template>
      </template>
    </n-modal>
  </div>
</template>

<style scoped>
.settings {
  max-width: 1000px;
}

:deep(.n-form-item) {
  margin-bottom: 16px;
}

:deep(.n-divider) {
  margin: 24px 0;
}

:deep(.n-collapse-item__header-main) {
  font-weight: 500;
}

:deep(.n-tabs .n-tabs-nav) {
  background: transparent;
}

:deep(.n-collapse) {
  background: transparent;
}

:deep(.n-collapse-item) {
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border-default);
  border-radius: 8px;
  margin-bottom: 8px;
}

/* 关于页面样式 */
.about-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.about-card {
  background: transparent;
}

.project-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
}

.project-name {
  font-size: 28px;
  font-weight: 600;
  margin: 0;
  background: linear-gradient(90deg, #10b981, #3b82f6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.project-description {
  font-size: 16px;
  color: var(--color-text-muted);
  margin: 0;
}

.project-links {
  margin-top: 8px;
}

.dep-name {
  font-weight: 500;
}

.thanks {
  padding: 16px 0;
}
</style>
