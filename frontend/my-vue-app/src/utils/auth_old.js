import { reactive, computed } from 'vue'

// ===== STATO SEMPLICE =====
const state = reactive({
  user: null,
  isAuthenticated: false,
  loading: false
})

// ===== FUNZIONI UTILITY =====
const getToken = () => localStorage.getItem('token')
const getUser = () => {
  const userData = localStorage.getItem('user')
  return userData ? JSON.parse(userData) : null
}
const clearAuth = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  state.user = null
  state.isAuthenticated = false
}

// ===== AZIONI =====
const actions = {
  // Inizializza autenticazione
  init() {
    const token = getToken()
    const user = getUser()
    
    if (token && user) {
      state.user = user
      state.isAuthenticated = true
      console.log('✅ Auth inizializzato:', user.username)
    } else {
      state.user = null
      state.isAuthenticated = false
      console.log('❌ Non autenticato')
    }
  },

  // Login
  login(userData, token) {
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(userData))
    state.user = userData
    state.isAuthenticated = true
    console.log('✅ Login completato:', userData.username)
  },

  // Logout
  logout() {
    clearAuth()
    console.log('🚪 Logout completato')
  },

  // Aggiorna dati utente
  updateUser(userData) {
    localStorage.setItem('user', JSON.stringify(userData))
    state.user = userData
    console.log('🔄 Dati utente aggiornati')
  }
}

// ===== GETTERS =====
const getters = {
  isAuthenticated: computed(() => state.isAuthenticated),
  user: computed(() => state.user),
  userName: computed(() => state.user?.username || ''),
  userEmail: computed(() => state.user?.email || ''),
  loading: computed(() => state.loading)
}

// ===== COMPOSABLE =====
export const useAuthStore = () => ({ state, actions, getters })

// ===== LEGACY SERVICE =====
export const authService = {
  isAuthenticated: () => state.isAuthenticated,
  getCurrentUser: () => state.user,
  getToken,
  logout: actions.logout,
  getAuthHeader: () => {
    const token = getToken()
    return token ? { Authorization: `Bearer ${token}` } : {}
  }
}

// ===== ROUTE GUARD =====
export const requireAuth = (to, from, next) => {
  if (state.isAuthenticated) {
    next()
  } else {
    next('/login')
  }
}

export default { useAuthStore, authService, requireAuth }
