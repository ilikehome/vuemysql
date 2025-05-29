import axios from 'axios'

export const loginApi = (data: { username: string; password: string }) => {
  return axios.post('/api/login', data)
}