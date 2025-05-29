import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  
  const login = async (username: string, password: string) => {
    const res = await axios.post('/api/login', { username, password })
    token.value = res.data.token
    localStorage.setItem('token', res.data.token)
  }

  const logout = () => {
    token.value = null
    localStorage.removeItem('token')
  }

  return { token, login, logout }
})