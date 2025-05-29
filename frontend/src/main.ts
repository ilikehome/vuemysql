import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useUserStore } from '@/stores/user'  // 保留单次导入

const pinia = createPinia()
const app = createApp(App)

app.use(pinia)
app.use(router)
app.mount('#app')
import './style.css'

// 删除重复的路由守卫（关键修复）
// router.beforeEach((to, from, next) => {
//   const user = useUserStore()
//   if (user.token) {  
//     next()
//   } else {
//     next({ name: 'Login' })
//   }
// })
// 删除末尾重复的 import { useUserStore } from '@/stores/user'
