import { useUserStore } from '@/stores/user'
import axios from 'axios'

/**
 * 公共认证请求封装（支持GET/POST/PUT/DELETE）
 * @param method 请求方法
 * @param url 请求地址
 * @param data 请求体（可选）
 */
export const authRequest = async <T>(
  method: 'get' | 'post' | 'put' | 'delete',
  url: string,
  data?: Record<string, any>
): Promise<T> => {
  const userStore = useUserStore()
  if (!userStore.token) {
    throw new Error('未找到认证token')
  }

  const response = await axios({
    method,
    url,
    data,
    headers: {
      'Authorization': `Bearer ${userStore.token}`,
      'Cache-Control': 'no-cache'
    }
  })
  return response.data as T
}
