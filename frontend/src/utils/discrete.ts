/**
 * Naive UI Discrete API
 *
 * 用于在 setup 外部使用 message、dialog、notification 等
 * 解决懒加载组件中 useMessage 报错的问题
 */

import { createDiscreteApi, darkTheme } from 'naive-ui'

const { message, notification, dialog, loadingBar } = createDiscreteApi(
  ['message', 'dialog', 'notification', 'loadingBar'],
  {
    configProviderProps: {
      theme: darkTheme,
    },
  }
)

export { message, notification, dialog, loadingBar }
