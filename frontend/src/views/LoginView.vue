<template>
  <div class="login-container">
    <h2>用户登录</h2>
    <input v-model="username" placeholder="用户名" />
    <input type="password" v-model="password" placeholder="密码" />
    <button @click="handleLogin">登录</button>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { loginApi } from '@/api/auth'  // 新增导入

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()
const userStore = useUserStore()

const handleLogin = async () => {
  try {
    // 改为调用Pinia的login方法（会自动存储localStorage）
    await userStore.login(username.value, password.value)  // 关键修复
    router.push('/')
  } catch (err) {
    error.value = '登录失败，请检查用户名和密码'
  }
}
</script>
