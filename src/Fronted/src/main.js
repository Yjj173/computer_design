import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCN from 'element-plus/dist/locale/zh-cn.mjs'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import axios from 'axios'

let app=createApp(App)
//设置访问的项目目录
axios.defaults.baseURL="http://localhost:8088/crm/"
// 给axios在vue中设置别名
app.config.globalProperties.$axios=axios
app.use(router).use(ElementPlus,{locale:zhCN}).mount('#app')

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}