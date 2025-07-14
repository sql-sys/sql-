import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

// 创建axios实例
const axiosInstance = axios.create({
  baseURL: 'http://wyaaa.gnway.cc:8000',
  timeout: 60000, // 设置为60秒
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
axiosInstance.interceptors.request.use(
  (config) => {
    // 自动添加token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// 响应拦截器
axiosInstance.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // 处理401错误
    if (error.response && error.response.status === 401) {
      // 如果不是在登录页面，才显示"请先登录"提示
      if (router.currentRoute.value.path !== '/login') {
        ElMessage.error('请先登录')
        // 清除本地存储的token
        localStorage.removeItem('token')
        localStorage.removeItem('userInfo')
        // 跳转到登录页
        router.push('/login')
      }
      return Promise.reject(error)
    }

    // 其他错误处理
    if (error.response && error.response.data) {
      const errorData = error.response.data
      if (errorData.detail) {
        // 过滤掉不需要显示的错误信息
        const silentErrors = ['未找到答题记录', '未找到相关记录']
        const errorMessage = Array.isArray(errorData.detail)
          ? errorData.detail[0]
          : errorData.detail

        if (!silentErrors.includes(errorMessage)) {
          ElMessage.error(errorMessage)
        }
      } else if (errorData.message) {
        ElMessage.error(errorData.message)
      }
    } else {
      ElMessage.error('网络错误，请检查网络连接')
    }

    return Promise.reject(error)
  },
)

export default axiosInstance
