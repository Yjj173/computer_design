import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/HomeView.vue'
import Login from '@/views/LoginView.vue'
import Detail from '@/views/Detail.vue'
import AverageTemp from '@/views/AverageTemp.vue'
import TemperatureChange from '@/views/TemperatureChange.vue'
import AdjustTemp from '@/views/AdjustTemp.vue'


const routes = [
  {
    path:'/',//url路径名
    redirect:'/login'
    //访问：<router-link to="/loginView">文本</router-link>,this.$router.push("/loginView");两种方式
  },
  {
    path: '/login',
    name: 'login',
    component:Login
  },
  {
    path: '/home',
    component: Home,
    meta: { requiresAuth: true } 
  },
  {
    path:'/detail',
    component:Detail
  },
  {
    path: '/AverageTemp',
    component: AverageTemp,
    meta: { requiresAuth: true } 
  },
  {
    path: '/AdjustTemp',
    component:  AdjustTemp,
    meta: { requiresAuth: true } 
  },
  {
    path: '/TemperatureChange',
    component:  TemperatureChange,
    meta: { requiresAuth: true } 
  },

]


const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// 添加路由守卫
router.beforeEach((to, from, next) => {
  // 检查需要鉴权的页面是否存在 JWT token
  if (to.meta.requiresAuth && !localStorage.getItem('jwt')) {
    // 如果不存在，就跳转到登录页面
    next('/login')
  } else {
    // 如果存在，就继续访问
    next()
  }
})



export default router
