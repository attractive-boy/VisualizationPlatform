// src/router/index.ts

import type { App } from 'vue'
import { createRouter, createWebHashHistory, onBeforeRouteLeave } from 'vue-router'
import type { RouteMeta, RouteRecordRaw } from 'vue-router'
// 根据src/views/目录下的文件自动引入路由 from 'src/views/..'
// 引入路由的path和meta等属性
// 此处使用typescript内置的高级类型Record来定义这个引入对象的类型
const routeModules: Record<string, RouteMeta> = import.meta.glob('../views/**/page.ts', {
  eager: true,
  import: 'default'
})

// 引入路由组件
const compModules = import.meta.glob('../views/**/IndexView.vue')

// 拼接注册路由数组
const routes: Array<RouteRecordRaw> = Object.entries(routeModules).map((i) => {
  const path = i[0].replace('../views', '').replace('/page.ts', '')
  const component = compModules[i[0].replace('page.ts', 'IndexView.vue')]
  return {
    path,
    component,
    meta: i[1]
  }
})

// 添加默认路由
routes.push({
  path: '/',
  redirect: '/Login' // 这里将默认路由重定向到您指定的首页路径
})

export const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title.toString()
  }
  next()
})

export function setupRouter(app: App) {
  console.log('routers======>', router.getRoutes())
  app.use(router)
  return router.isReady()
}
