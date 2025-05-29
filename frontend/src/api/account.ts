import axios from 'axios'
import { useUserStore } from '@/stores/user'

export const getAccountListApi = async () => {
  try {
    const userStore = useUserStore()  // 新增：通过Pinia获取token
    const token = userStore.token  // 从Pinia状态获取（已同步localStorage）
    if (!token) throw new Error('未找到认证token')
    
    const response = await axios.get('/api/accounts', {
      headers: { 
        'Authorization': `Bearer ${token}`,
        'Cache-Control': 'no-cache'
      }
    })
    return response.data
  } catch (error) {
    console.error('API请求失败:', error)
    throw error
  }
}

export const addAccountApi = (data: { 
  amount: number;
  type: string;  // 改为string类型接收中文
  remark?: string 
}) => {
  const userStore = useUserStore()  // 添加这行
  const englishType = data.type === '收入' ? 'income' : 'expense'  // 转换为英文
  
  return axios.post('/api/accounts', {
    amount: data.amount,
    type: englishType,  // 使用转换后的值
    remark: data.remark
  }, {
    headers: {
      'Authorization': `Bearer ${userStore.token}`
    }
  })
}

export const editAccountApi = (id: number, data: { amount?: number; type?: string; remark?: string }) => {
  const userStore = useUserStore()
  return axios.put(`/api/accounts/${id}`, data, {
    headers: {
      'Authorization': `Bearer ${userStore.token}`
    }
  })
}

export const deleteAccountApi = (id: number) => {
  const userStore = useUserStore()
  return axios.delete(`/api/accounts/${id}`, {
    headers: {
      'Authorization': `Bearer ${userStore.token}`
    }
  })
}