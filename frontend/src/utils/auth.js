import { reactive } from 'vue'

// Store semplice per autenticazione
const authStore = reactive({
  user: null,
  token: null,
  isAuthenticated: false
})

// Inizializza store da localStorage
function initAuth() {
  const token = localStorage.getItem('token')
  const user = localStorage.getItem('user')
  
  if (token && user) {
    authStore.token = token
    authStore.user = JSON.parse(user)
    authStore.isAuthenticated = true
  }
}

// Login
function login(userData, token) {
  localStorage.setItem('token', token)
  localStorage.setItem('user', JSON.stringify(userData))
  
  authStore.token = token
  authStore.user = userData
  authStore.isAuthenticated = true
}

// Logout
function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  
  authStore.token = null
  authStore.user = null
  authStore.isAuthenticated = false
}

// Esporta tutto
export const useAuth = () => ({
  store: authStore,
  login,
  logout,
  initAuth
})

export default useAuth
