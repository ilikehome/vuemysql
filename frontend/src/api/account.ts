import { authRequest } from './utils'  // 导入公共认证请求函数

// 简化获取账目列表（移除冗余的.then(res => res.data)）
export const getAccountListApi = () => {
  return authRequest<any>('get', '/api/accounts')
}

// 新增账目（已正确使用authRequest）
export const addAccountApi = (data: { amount: number; type: string; remark?: string }) => {
  const englishType = data.type === '收入' ? 'income' : 'expense'
  return authRequest('post', '/api/accounts', { ...data, type: englishType })
}

// 编辑账目（改为使用authRequest）
export const editAccountApi = (id: number, data: { amount?: number; type?: string; remark?: string }) => {
  const englishType = data.type ? (data.type === '收入' ? 'income' : 'expense') : undefined
  return authRequest('put', `/api/accounts/${id}`, { ...data, type: englishType })
}

// 删除账目（改为使用authRequest）
export const deleteAccountApi = (id: number) => {
  return authRequest('delete', `/api/accounts/${id}`)
}