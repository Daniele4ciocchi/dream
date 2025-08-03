import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from '../components/HelloWorld.vue'
import PomodoroTimer from '../components/PomodoroTimer.vue'
import Home from '../views/Home.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Profile from '../views/Profile.vue'
import MyDreams from '../views/MyDreams.vue'
import Feed from '../components/Feed.vue'
import Test from '../views/Test.vue'

const routes = [
   { path: '/', redirect: '/feed' },
   { path: '/home', component: Home },
   { path: '/helloworld', component:  HelloWorld },
   { path: '/pomodoro', component: PomodoroTimer },
   { path: '/feed', component: Feed },
   { path: '/login', component: Login },
   { path: '/register', component: Register },
   { path: '/test', component: Test },
   { 
     path: '/profile', 
     component: Profile
   },
   { 
     path: '/dreams', 
     component: MyDreams
   },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
