import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { taskApi } from '@/api'
import type { Task, TaskCreate, TaskUpdate } from '@/types'

export const useTaskStore = defineStore('task', () => {
  // 状态
  const tasks = ref<Task[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // 计算属性
  const total = computed(() => tasks.value.length)
  const activeTasks = computed(() => tasks.value.filter(t => t.enabled))
  const activeCount = computed(() => activeTasks.value.length)
  const errorTasks = computed(() => tasks.value.filter(t => t.error_count > 0))
  const errorCount = computed(() => errorTasks.value.length)

  // 获取任务列表
  const fetchTasks = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await taskApi.list()
      tasks.value = response.items
    } catch (e) {
      error.value = '获取任务列表失败'
      console.error('获取任务列表失败:', e)
    } finally {
      loading.value = false
    }
  }

  // 创建任务
  const createTask = async (data: TaskCreate): Promise<Task | null> => {
    loading.value = true
    error.value = null
    try {
      const task = await taskApi.create(data)
      tasks.value.push(task)
      return task
    } catch (e) {
      error.value = '创建任务失败'
      console.error('创建任务失败:', e)
      return null
    } finally {
      loading.value = false
    }
  }

  // 更新任务
  const updateTask = async (id: string, data: TaskUpdate): Promise<Task | null> => {
    loading.value = true
    error.value = null
    try {
      const task = await taskApi.update(id, data)
      const index = tasks.value.findIndex(t => t.id === id)
      if (index !== -1) {
        tasks.value[index] = task
      }
      return task
    } catch (e) {
      error.value = '更新任务失败'
      console.error('更新任务失败:', e)
      return null
    } finally {
      loading.value = false
    }
  }

  // 删除任务
  const deleteTask = async (id: string): Promise<boolean> => {
    loading.value = true
    error.value = null
    try {
      await taskApi.delete(id)
      tasks.value = tasks.value.filter(t => t.id !== id)
      return true
    } catch (e) {
      error.value = '删除任务失败'
      console.error('删除任务失败:', e)
      return false
    } finally {
      loading.value = false
    }
  }

  // 启用任务
  const enableTask = async (id: string): Promise<boolean> => {
    try {
      const task = await taskApi.enable(id)
      const index = tasks.value.findIndex(t => t.id === id)
      if (index !== -1) {
        tasks.value[index] = task
      }
      return true
    } catch (e) {
      console.error('启用任务失败:', e)
      return false
    }
  }

  // 禁用任务
  const disableTask = async (id: string): Promise<boolean> => {
    try {
      const task = await taskApi.disable(id)
      const index = tasks.value.findIndex(t => t.id === id)
      if (index !== -1) {
        tasks.value[index] = task
      }
      return true
    } catch (e) {
      console.error('禁用任务失败:', e)
      return false
    }
  }

  // 立即检测
  const checkTask = async (id: string): Promise<{ changed: boolean; error?: string } | null> => {
    try {
      return await taskApi.check(id)
    } catch (e) {
      console.error('检测任务失败:', e)
      return null
    }
  }

  // 获取单个任务
  const getTask = (id: string): Task | undefined => {
    return tasks.value.find(t => t.id === id)
  }

  return {
    // 状态
    tasks,
    loading,
    error,

    // 计算属性
    total,
    activeTasks,
    activeCount,
    errorTasks,
    errorCount,

    // 方法
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    enableTask,
    disableTask,
    checkTask,
    getTask,
  }
})
