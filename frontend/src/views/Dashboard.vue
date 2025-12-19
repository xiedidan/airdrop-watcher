<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NCard, NGrid, NGridItem, NStatistic, NSpace, NEmpty } from 'naive-ui'
import { useMonitorStore } from '@/stores/monitor'

const monitorStore = useMonitorStore()

onMounted(() => {
  monitorStore.fetchStatus()
})
</script>

<template>
  <div class="dashboard">
    <n-grid :cols="4" :x-gap="16" :y-gap="16">
      <n-grid-item>
        <n-card title="任务总数">
          <n-statistic :value="monitorStore.totalTasks" />
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card title="活跃任务">
          <n-statistic :value="monitorStore.activeTasks" />
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card title="检测到的变化">
          <n-statistic :value="monitorStore.totalChanges" />
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card title="监控状态">
          <n-statistic :value="monitorStore.isRunning ? '运行中' : '已停止'" />
        </n-card>
      </n-grid-item>
    </n-grid>

    <n-card title="最近变化" style="margin-top: 16px">
      <n-empty description="暂无变化记录" />
    </n-card>
  </div>
</template>

<style scoped>
.dashboard {
  max-width: 1200px;
}
</style>
