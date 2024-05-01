<template>
  <div class="login-container">
    <div class="login-box">
      <h2 class="login-title">可视化平台</h2>
      <el-form ref="loginForm" :model="form" :rules="loginRules" label-width="0" class="login-form">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名"></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input type="password" v-model="form.password" placeholder="密码"></el-input>
        </el-form-item>
        <el-form-item class="login-btn">
          <el-button type="primary" @click="login(loginForm)">登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  reactive,
  toRefs,
  ref,
  getCurrentInstance,
  onBeforeMount,
  onBeforeUnmount,
  inject,
  type ComponentInternalInstance
} from 'vue'
import { ElForm, ElFormItem, ElInput, ElButton, ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { router } from '@/router/index'
import type { MessageParamsWithType } from 'element-plus/lib';

const { proxy, refs } = getCurrentInstance() as ComponentInternalInstance

const loginForm = ref<FormInstance>()

// 登录方法
const login = (FormEl: any) => {
  // 执行登录操作
  FormEl.validate((valid: any, fields: any) => {
    if (valid) {
      const username = form.username
      const password = form.password

      // 发起登录请求
      proxy?.$http
        .post('/user/checkExistence', { username, password })
        .then((response: { data: any; }) => {
          console.log(response)
          // 处理登录成功的逻辑
          if (response.data) {
            loginRequest(username, password)
          } else {
            ElMessage.error('用户不存在，请先注册')
          }
        })
        .catch((error: any) => {
          // 处理登录失败的逻辑
          console.error('登录失败', error)
        })
    } else {
      ElMessage.error('请完善表单信息')
    }
  })
}
</script>

<style scoped>
.login-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f2f5;
}

.login-box {
  width: 400px;
  padding: 20px;
  border-radius: 10px;
  background-color: #fff;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

.login-title {
  text-align: center;
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

.login-form {
  margin-top: 20px;
}

.login-btn {
  text-align: center;
}

.login-btn :deep() .el-form-item__content .el-button {
  width: 100%;
}

.switch-btn {
  margin-top: 20px;
  display: block;
  margin-left: auto;
  margin-right: auto;
}
</style>
