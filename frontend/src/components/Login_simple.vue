<template>
  <div class="login-container">
    <div class="login-card">
      <h2>🌙 Login</h2>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Email:</label>
          <input 
            type="email" 
            v-model="email" 
            required 
            placeholder="Inserisci email"
          >
        </div>
        
        <div class="form-group">
          <label>Password:</label>
          <input 
            type="password" 
            v-model="password" 
            required 
            placeholder="Inserisci password"
          >
        </div>
        
        <button type="submit" :disabled="loading">
          {{ loading ? 'Accesso...' : 'Accedi' }}
        </button>
        
        <div v-if="error" class="error">{{ error }}</div>
      </form>
      
      <p>
        Non hai un account? 
        <router-link to="/register">Registrati</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import api from '../utils/api.js'
import { useAuth } from '../utils/auth.js'

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      loading: false,
      error: ''
    }
  },
  setup() {
    const { login } = useAuth()
    return { login }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.error = ''
      
      try {
        const response = await api.post('/api/auth/login', {
          email: this.email,
          password: this.password
        })
        
        // Login nello store
        this.login(response.data.user, response.data.access_token)
        
        // Redirect
        this.$router.push('/profile')
        
      } catch (error) {
        this.error = error.response?.data?.message || 'Errore di login'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  width: 100%;
  background: #4b2e83;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  opacity: 0.6;
}

.error {
  color: red;
  margin-top: 1rem;
  text-align: center;
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #4b2e83;
}

p {
  text-align: center;
  margin-top: 1rem;
}
</style>
