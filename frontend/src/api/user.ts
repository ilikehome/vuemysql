import axios from 'axios'
import { useUserStore } from '@/stores/user'

// 获取用户列表（已携带认证头）
export const getUserListApi = () => {
  const userStore = useUserStore()
  return axios.get('/api/users', {
    headers: {
      'Authorization': `Bearer ${userStore.token}`
    }
  })
}

// 新增用户（已携带认证头）
export const addUserApi = (userData: { username: string; password: string }) => {
  const userStore = useUserStore()
  return axios.post('/api/users', userData, {
    headers: {
      'Authorization': `Bearer ${userStore.token}`
    }
  })
}

// 编辑用户（补充认证头）
export const editUserApi = (id: number, data: { username: string; password?: string }) => {
  const userStore = useUserStore()
  return axios.put(`/api/users/${id}`, data, {
    headers: {
      'Authorization': `Bearer ${userStore.token}`
    }
  })
}

// 删除用户（补充认证头）
export const deleteUserApi = (id: number) => {
  const userStore = useUserStore()
  return axios.delete(`/api/users/${id}`, {
    headers: {
      'Authorization': `Bearer ${userStore.token}`
    }
  })
}