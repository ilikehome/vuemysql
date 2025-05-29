<template>
  <div class="main-layout">
    <!-- 左侧导航（新增退出登录按钮） -->
    <aside class="sidebar">
      <nav>
        <router-link 
          :to="{ name: 'UserManage' }" 
          class="nav-item"
        >用户管理</router-link>
        <router-link 
          :to="{ name: 'AccountManage' }" 
          class="nav-item"
        >记账管理</router-link>
        
        <!-- 新增退出登录按钮 -->
        <button 
          @click="handleLogout" 
          class="nav-item"
        >退出登录</button>
      </nav>
    </aside>
    
    <!-- 右侧内容区保持不变 -->
    <section class="content">
      <router-view />
    </section>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

// 定义退出登录方法
const handleLogout = () => {
  userStore.logout()
  router.push({ name: 'Login' })
}
</script>

<style scoped>
/* 保持原有样式，新增按钮样式与导航项一致 */
.nav-item {
  display: block;
  padding: 10px;
  margin: 5px 0;
  text-decoration: none;
  color: #333;
  border-radius: 4px;
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
}
.nav-item:hover {
  background: #e2e8f0;
}
.main-layout {
  display: flex;
  min-height: 100vh;
}
.sidebar {
  width: 200px;
  background: #f5f7fa;
  padding: 20px;
  border-right: 1px solid #e5e7eb;
}
.nav-item {
  display: block;
  padding: 10px;
  margin: 5px 0;
  text-decoration: none;
  color: #333;
  border-radius: 4px;
}
.nav-item.router-link-exact-active {
  background: #e2e8f0;
  color: #2563eb;
}
.content {
  flex: 1;
  padding: 20px;
  min-width: 0;  /* 新增：防止内容溢出导致隐藏 */
}
</style>