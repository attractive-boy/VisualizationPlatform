<template>
  <div style="app-header">
    <el-menu :default-active="activeIndex" mode="horizontal" :ellipsis="false" class="el-menu" @select="handleSelect">
      <el-menu-item index="0" class="header-title">
        <h4>可视化平台</h4>
      </el-menu-item>
      <div class="flex-grow" />
      <el-menu-item v-for="(item, index) in routes" :key="index" :index="item.path">{{
        item.meta.title
      }}</el-menu-item>
    </el-menu>
  </div>
</template>
<script setup lang="ts">

import { ref, shallowRef, onBeforeUnmount, defineEmits, watch, getCurrentInstance } from 'vue'
import { baseURL } from '@/plugins/axios'
import { router } from '@/router/index'
const { proxy } = getCurrentInstance()


const activeIndex = ref('/Home')
const username = ref(localStorage.getItem('system_username'))

const props = defineProps({})

const role = ref(localStorage.getItem('system_userRole'))

watch(
  () => router.currentRoute.value.path,
  (toPath) => {
    activeIndex.value = toPath
  },
  { immediate: true, deep: true }
)

const handleSelect = (key: string, keyPath: string[]) => {
  router.push(key)
}

let routes: any

const changeRoute = () => {
  routes = router.getRoutes().filter((route: any) => {
    return route.meta && route.meta.title && route.meta.role?.includes(role.value)
  })

  routes = routes.sort((a: { meta: { orderNum: number; }; }, b: { meta: { orderNum: number; }; }) => {
    return a.meta.orderNum - b.meta.orderNum
  })
}
changeRoute()
const toLogin = () => {
  router.push('/Login')
}

const logout = () => {
  localStorage.removeItem('system_sa_token')
  username.value = null
  router.push('/Login')
}
proxy.$bus.on('setUserName', (data: string) => {
  username.value = data
  localStorage.setItem('system_username', data)
})

proxy.$bus.on('setUserRole', (data: string) => {
  role.value = data
  localStorage.setItem('system_userRole', data)
  changeRoute()
})
</script>

<style scoped>
.el-menu {
  border-radius: 10px;
  overflow: hidden;
}

.flex-grow {
  flex-grow: 1;
}
</style>
