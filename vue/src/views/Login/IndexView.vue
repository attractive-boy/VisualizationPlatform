<template>
  <div class="login-container">
    <div class="login-box">
      <h2 class="login-title">可视化平台</h2>
      <el-form ref="loginForm" :model="form" label-width="0" class="login-form">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名"></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input type="password" v-model="form.password" placeholder="密码"></el-input>
        </el-form-item>
        <el-form-item class="login-btn">
          <el-button type="primary" @click="login()">登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { ElForm, ElFormItem, ElInput, ElButton, ElMessage } from 'element-plus';
import { router } from '@/router/index';

const form = ref({
  username: '',
  password: ''
});

// 登录方法
const login = () => {
  const { username, password } = form.value;
  if (username === 'admin' && password === 'admin') {
    // 用户名和密码都是 admin，执行登录成功的逻辑
    // 例如，可以直接跳转到首页
    router.push('/Home');
  } else {
    // 用户名或密码不是 admin，显示错误信息
    ElMessage.error('用户名或密码错误');
  }
};
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

</style>
