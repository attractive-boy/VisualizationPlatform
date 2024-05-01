import './assets/main.css'
import 'element-plus/dist/index.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'

// @ts-ignore
import App from './App.vue'
import { setupRouter } from './router'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import axiosPlugin from './plugins/axios'
import eventBus from 'vue3-eventbus'

const app = createApp(App)

setupRouter(app)
app.use(createPinia())
app.use(eventBus)
app.config.globalProperties.$bus = eventBus
app.use(ElementPlus)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.use(axiosPlugin)
app.mount('#app')
