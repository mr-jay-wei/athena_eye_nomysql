import { createRouter, createWebHistory } from 'vue-router'
// 我们将把默认的 HomeView 重命名为更有意义的 DashboardView
import DashboardView from '../views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView
    },
    // 我们为未来的页面先占好位置
    {
      path: '/config',
      name: 'config',
      // 路由懒加载：只有当用户访问这个页面时，才会加载对应的组件代码
      component: () => import('../views/ConfigView.vue')
    },
    {
        path: '/archive',
        name: 'archive',
        component: () => import('../views/ArchiveView.vue')
    }
  ]
})

export default router