import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import router from '@/router'

// Create axios instance
const service = axios.create({
    baseURL: '/api',
    timeout: 5000,
    withCredentials: true  // Enable cookie-based authentication
})

// Request interceptor (simplified - no token handling needed)
service.interceptors.request.use(
    config => {
        return config
    },
    error => {
        console.log(error)
        return Promise.reject(error)
    }
)

// Response interceptor
service.interceptors.response.use(
    response => {
        return response.data
    },
    error => {
        console.log('err' + error)
        let message = error.message

        if (error.response) {
            if (error.response.data && error.response.data.error) {
                message = error.response.data.error
            } else {
                switch (error.response.status) {
                    case 401:
                        message = '未授权，请重新登录'
                        const userStore = useUserStore()
                        userStore.logout()
                        router.push('/login')
                        break
                    case 403:
                        message = '拒绝访问'
                        break
                    case 404:
                        message = '请求错误,未找到该资源'
                        break
                    case 500:
                        message = '服务器端出错'
                        break
                    default:
                        message = `连接错误${error.response.status}`
                }
            }
        }

        ElMessage({
            message: message,
            type: 'error',
            duration: 5 * 1000
        })
        return Promise.reject(error)
    }
)

export default service
