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
} from '@vicons/ionicons5'
import { settingsApi, notificationApi, aboutApi } from '@/api'
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
  background: linear-gradient(90deg, #18a058, #2080f0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.project-description {
  font-size: 16px;
  color: var(--n-text-color-3);
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
