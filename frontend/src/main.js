import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

console.log('Starting Vue app...')

const app = createApp(App)
app.use(router)
app.mount('#app')

console.log('Vue app mounted!')
