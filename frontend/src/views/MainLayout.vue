<template>
  <div class="main-layout">
    <!-- 左侧导航 -->
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
      </nav>
    </aside>
    
    <!-- 右侧内容区 -->
    <section class="content">
      <router-view />
    </section>
  </div>
</template>

<style scoped>
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