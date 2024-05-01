import axios from 'axios'
import type { App } from 'vue'
import { router } from '@/router/index'

const baseURL = 'http://localhost:8080/'

const axiosInstance = axios.create({
  baseURL: baseURL, // 设置统一的基础 URL
  timeout: 5000, // 设置请求超时时间
  withCredentials: true // 设置允许携带 cookies
})

// 添加响应拦截器
axiosInstance.interceptors.response.use(
  (response) => {
    return response // 正常响应，直接返回
  },
  (error) => {
    // 处理错误响应
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('system_sa_token')
      router.push('/Login')
      return
    }
    return Promise.reject(error) // 将错误继续向下传递
  }
)

// 添加请求拦截器
axiosInstance.interceptors.request.use(
  (config) => {
    // 在请求头中添加 token
    const token = localStorage.getItem('system_sa_token')
    if (token) {
      config.headers['satoken'] = `${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default {
  install(app: App<Element>) {
    // 添加实例方法
    app.config.globalProperties.$http = axiosInstance
  }
}

export { baseURL }
