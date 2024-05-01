<template>
  <el-container>
    <el-header class="header-container">
      <HeaderComponent />
    </el-header>
    <el-container>
      <el-main class="main">
        <RouterView />
      </el-main>
    </el-container>
  </el-container>
</template>
<script lang="ts" setup>
import { onMounted, ref, watch, computed, watchEffect, getCurrentInstance, inject } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { router } from '@/router/index'
import { useRoute } from 'vue-router'
import HeaderComponent from '@/components/Header/HeaderComponent.vue'




</script>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

.el-header {
  padding: 0;
}

.el-header .header-title {
  pointer-events: none;
}

.el-header .header-user {
  pointer-events: none;
}

.el-header .header-user :deep() .el-dropdown {
  pointer-events: all;
}

.main-aside {
  width: 12rem;
  margin-right: 1rem;
}

.main {
  background-color: white;
  border-radius: 10px;
}

.header-container {
  margin-bottom: 1rem;
}
</style>
