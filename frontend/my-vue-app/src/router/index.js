import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from '../components/HelloWorld.vue'
import PomodoroTimer from '../components/PomodoroTimer.vue'
import Home from '../views/Home.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Profile from '../views/Profile.vue'
import MyDreams from '../views/MyDreams.vue'
import { authService } from '../utils/auth.js'

const routes = [
   { path: '/', redirect: '/home' },
   { path: '/helloworld', component:  HelloWorld },
   { path: '/pomodoro', component: PomodoroTimer },
   { path: '/home', component: Home },
   { path: '/login', component: Login },
   { path: '/register', component: Register },
   { 
     path: '/profile', 
     component: Profile,
     meta: { requiresAuth: true }
   },
   { 
     path: '/dreams', 
     component: MyDreams,
     meta: { requiresAuth: true }
   },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation guard per le route protette
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !authService.isAuthenticated()) {
    next('/login')
  } else {
    next()
  }
})

export default router
