<script setup lang="ts">
import { h, ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { NLayout, NLayoutHeader, NLayoutContent, NLayoutFooter, NMenu, NIcon, NSpace, NButton, NBadge, NText } from 'naive-ui'
import {
  HomeOutline,
  ListOutline,
  TimeOutline,
  SettingsOutline,
  PlayCircleOutline,
  StopCircleOutline,
} from '@vicons/ionicons5'
import { useMonitorStore } from '@/stores/monitor'

const router = useRouter()
const route = useRoute()
const monitorStore = useMonitorStore()

// 菜单项
const menuOptions = [
  {
    label: '仪表盘',
    key: '/',
    icon: () => h(NIcon, null, { default: () => h(HomeOutline) }),
  },
  {
    label: '任务管理',
    key: '/tasks',
    icon: () => h(NIcon, null, { default: () => h(ListOutline) }),
  },
  {
    label: '变化历史',
    key: '/history',
    icon: () => h(NIcon, null, { default: () => h(TimeOutline) }),
  },
  {
    label: '系统设置',
    key: '/settings',
    icon: () => h(NIcon, null, { default: () => h(SettingsOutline) }),
  },
]

// 当前选中的菜单
const activeKey = computed(() => route.path)

// 菜单点击
const handleMenuClick = (key: string) => {
  router.push(key)
}

// 监控控制
const handleToggleMonitor = async () => {
  if (monitorStore.isRunning) {
    await monitorStore.stopMonitor()
  } else {
    await monitorStore.startMonitor()
  }
}

// 初始化获取状态
monitorStore.fetchStatus()
</script>

<template>
  <n-layout class="app-layout" position="absolute">
    <!-- 顶部导航 -->
    <n-layout-header bordered class="app-header">
      <div class="header-left">
        <span class="logo">WebMon</span>
        <n-menu
          mode="horizontal"
          :value="activeKey"
          :options="menuOptions"
          @update:value="handleMenuClick"
        />
      </div>
      <div class="header-right">
        <n-space align="center">
          <n-badge :dot="monitorStore.isRunning" :type="monitorStore.isRunning ? 'success' : 'default'">
            <n-text :type="monitorStore.isRunning ? 'success' : 'default'">
              {{ monitorStore.isRunning ? '运行中' : '已停止' }}
            </n-text>
          </n-badge>
          <n-button
            :type="monitorStore.isRunning ? 'error' : 'success'"
            size="small"
            @click="handleToggleMonitor"
            :loading="monitorStore.loading"
          >
            <template #icon>
              <n-icon>
                <StopCircleOutline v-if="monitorStore.isRunning" />
                <PlayCircleOutline v-else />
              </n-icon>
            </template>
            {{ monitorStore.isRunning ? '停止' : '启动' }}
          </n-button>
        </n-space>
      </div>
    </n-layout-header>

    <!-- 主内容区 -->
    <n-layout-content class="app-content">
      <router-view />
    </n-layout-content>

    <!-- 底部状态栏 -->
    <n-layout-footer bordered class="app-footer">
      <n-space justify="space-between" style="width: 100%">
        <n-space>
          <n-text depth="3">
            任务: {{ monitorStore.activeTasks }}/{{ monitorStore.totalTasks }}
          </n-text>
          <n-text depth="3">|</n-text>
          <n-text depth="3">
            变化: {{ monitorStore.totalChanges }}
          </n-text>
        </n-space>
        <n-text depth="3">WebMon v1.0.0</n-text>
      </n-space>
    </n-layout-footer>
  </n-layout>
</template>

<style scoped>
.app-layout {
  height: 100vh;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  height: 64px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 24px;
}

.logo {
  font-size: 20px;
  font-weight: bold;
  color: #63e2b7;
}

.header-right {
  display: flex;
  align-items: center;
}

.app-content {
  padding: 24px;
  overflow: auto;
}

.app-footer {
  padding: 12px 24px;
}
</style>
