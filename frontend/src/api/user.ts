import axios from 'axios'
import { useUserStore } from '@/stores/user'

export const getUserListApi = () => {
  const userStore = useUserStore()
  return axios.get('/api/users', {
    headers: {
      'Authorization': `Bearer ${userStore.token}`
    }
  })
}

// 新增用户
export const addUserApi = (userData: { username: string; password: string }) => {
  const userStore = useUserStore()
  return axios.post('/api/users', userData, {
    headers: {
      // 关键：携带认证令牌（如果接口需要认证）
      'Authorization': `Bearer ${userStore.token}`
    }
  })
}

// 编辑用户
export const editUserApi = (id: number, data: { username: string; password?: string }) => {
  return axios.put(`/api/users/${id}`, data)
}

// 删除用户
export const deleteUserApi = (id: number) => {
  return axios.delete(`/api/users/${id}`)
}