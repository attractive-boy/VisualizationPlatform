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


const activeIndex = ref('/Home')

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
    return route.meta && route.meta.title
  })

  routes = routes.sort((a: { meta: { orderNum: number; }; }, b: { meta: { orderNum: number; }; }) => {
    return a.meta.orderNum - b.meta.orderNum
  })
}
changeRoute()
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
