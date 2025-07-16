import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from '../components/HelloWorld.vue'
import PomodoroTimer from '../components/PomodoroTimer.vue'
import Home from '../views/Home.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'


const routes = [
   { path: '/', redirect: '/home' },
   { path: '/helloworld', component:  HelloWorld },
   { path: '/pomodoro', component: PomodoroTimer },
   { path: '/home', component: Home },
   { path: '/login', component: Login },
   { path: '/register', component: Register },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
