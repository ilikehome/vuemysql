import { createRouter, createWebHistory, type RouteRecordRaw, type NavigationGuardNext, type RouteLocationNormalized } from 'vue-router';
import { useUserStore } from '@/stores/user'; // 新增：引入用户状态
// 尝试使用别名来引入 LoginView 组件，避免相对路径找不到模块的问题，假设 @ 代表 src 目录
import LoginView from '@/views/LoginView.vue'
import MainLayout from '@/views/MainLayout.vue'
import UserManage from '@/views/UserManage.vue'
import AccountManage from '@/views/AccountManage.vue'
import NotFound from '@/views/NotFound.vue' 

const routes: RouteRecordRaw[] = [
  { path: '/login', name: 'Login', component: LoginView },
  {
    path: '/',
    component: MainLayout,
    meta: { requiresAuth: true }, // 新增：标记需要登录的路由
    children: [
      { path: '', name: 'UserManage', component: UserManage, meta: { title: '用户管理' } },
      { path: '/account', name: 'AccountManage', component: AccountManage, meta: { title: '记账管理' } }
    ]
  },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound } // 新增：404页面路由
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 新增：全局前置守卫（权限控制）
router.beforeEach((to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
  console.log('当前路由:', to.path, '是否需要认证:', to.meta.requiresAuth); // 添加日志
  const userStore = useUserStore();
  if (to.meta.requiresAuth && !userStore.token) {
    next({ name: 'Login' });
  } else {
    next();
  }
})

export default router