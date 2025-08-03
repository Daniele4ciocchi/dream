<template>
  <div class="profile-container">
    <div class="profile-card">
      <h2>👤 Il Mio Profilo</h2>
      
      <div v-if="loading">Caricamento...</div>
      
      <div v-else-if="user" class="user-info">
        <p><strong>Username:</strong> {{ user.username }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Registrato il:</strong> {{ formatDate(user.created_at) }}</p>
        
        <button @click="handleLogout" class="logout-btn">
          🚪 Logout
        </button>
      </div>
      
      <div v-else class="error">
        Errore nel caricamento del profilo
      </div>
    </div>
  </div>
</template>

<script>
import api from '../utils/api.js'
import { useAuth } from '../utils/auth.js'

export default {
  name: 'Profile',
  data() {
    return {
      user: null,
      loading: true
    }
  },
  async mounted() {
    await this.loadProfile()
  },
  methods: {
    async loadProfile() {
      try {
        const response = await api.get('/api/auth/me')
        this.user = response.data.user
      } catch (error) {
        console.error('Errore caricamento profilo:', error)
      } finally {
        this.loading = false
      }
    },
    
    handleLogout() {
      const { logout } = useAuth()
      logout()
      this.$router.push('/login')
    },
    
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString('it-IT')
    }
  }
}
</script>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}

.profile-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #4b2e83;
}

.user-info p {
  margin: 1rem 0;
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.logout-btn {
  width: 100%;
  background: #dc3545;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 1rem;
}

.logout-btn:hover {
  background: #c82333;
}

.error {
  color: red;
  text-align: center;
}
</style>
