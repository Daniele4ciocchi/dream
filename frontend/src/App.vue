<template>
  <div class="app">
    <header class="app-header">
      <div class="nav-container">
        <div class="nav-item nav-item-left">
          <div class="nav-menu-item">
            <router-link class="logo" to="/home">DreamKeeper</router-link>
          </div>
        </div>

        <div class="nav-item nav-item-center">
          <ul class="nav-ul">
            <li class="nav-menu-item"><router-link to="/">Feed</router-link></li>
            <li class="nav-menu-item"><router-link to="/pomodoro">Pomodoro</router-link></li>
            <li class="nav-menu-item" v-if="isAuthenticated"><router-link to="/dreams">My Dreams</router-link></li>
          </ul>
        </div>

        <div class="nav-item nav-item-right">
          <ul class="nav-ul">
            <!-- Mostra login/register se NON autenticato -->
            <template v-if="!isAuthenticated">
              <li class="nav-menu-item"><router-link to="/login">Login</router-link></li>
              <li class="nav-menu-item"><router-link to="/register">Register</router-link></li>
              <li class="nav-menu-item">
                <router-link to="/login">
                  <svg class="feather" id="Login">
                    <use href="/feather-sprite-v4.29.0.svg#user"></use>
                  </svg>
                </router-link>
              </li>
            </template>
            
            <!-- Mostra profilo e logout se autenticato -->
            <template v-else>
              
              <li class="nav-menu-item">
                <router-link to="/profile" class="profile-link">
                  <svg class="feather">
                    <use href="/feather-sprite-v4.29.0.svg#user"></use>
                  </svg>
                  <span class="welcome-text">{{ userName }}</span>
                </router-link>
              </li>
              <li class="nav-menu-item">
                <button @click="logout" class="logout-btn">
                  <svg class="feather">
                    <use href="/feather-sprite-v4.29.0.svg#log-out"></use>
                  </svg>
                  Logout
                </button>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </header>

    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAuth } from './utils/auth.js'
import { useRouter } from 'vue-router'

const { store, initAuth, logout: authLogout } = useAuth()
const router = useRouter()

// Inizializza auth quando l'app si carica
onMounted(() => {
  initAuth()
})

// Computed properties
const isAuthenticated = computed(() => store.isAuthenticated)
const userName = computed(() => store.user?.username || '')

// Methods
const logout = () => {
  authLogout()
  router.push('/home')
}
</script>

<style>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  backdrop-filter: blur(10px);
  padding: 10px 0;
}

.nav-container {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  gap: 20px;
}

.nav-item {
  display: flex;
  align-items: center;
  background-color: rgba(74, 46, 131, 0.2);
  color: white;
  border: 2px solid rgba(74, 46, 131, 0.5);
  border-radius: 12px;
  padding: 8px 16px;
  transition: all 0.3s ease;
}

.nav-item:hover {
  background-color: rgba(74, 46, 131, 0.3);
  border-color: rgba(74, 46, 131, 0.7);
}

.nav-item-left {
  justify-self: start;
}

.nav-item-center {
  justify-self: center;
}

.nav-item-right {
  justify-self: end;
}

.logo {
  text-decoration: none;
  color: white;
  font-weight: 600;
  font-size: 1.1rem;
}

.nav-ul {
  list-style: none;
  display: flex;
  gap: 15px;
  padding: 0;
  margin: 0;
  align-items: center;
}

.nav-menu-item {
  padding: 8px 12px;
  color: rgba(255, 255, 255, 0.8);
  border: 2px solid transparent;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-menu-item:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  color: white;
}

.nav-menu-item a {
  text-decoration: none;
  color: inherit;
  font-size: 0.9rem;
}

.nav-menu-item a.router-link-active {
  color: #6c47a3;
  font-weight: 600;
}

.user-info {
  background: linear-gradient(135deg, #4b2e83 0%, #6c47a3 100%);
  border-color: #6c47a3;
}

.welcome-text {
  color: white;
  font-weight: 500;
  font-size: 0.9rem;
}

.profile-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.logout-btn {
  background: none;
  border: none;
  color: inherit;
  font-size: 0.9rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  padding: 0;
}

.logout-btn:hover {
  color: #ff6b6b;
}

.feather {
  width: 20px;
  height: 20px;
  fill: currentColor;
}

.app-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .nav-container {
    grid-template-columns: auto 1fr auto;
    gap: 15px;
  }
  
  .nav-ul {
    gap: 10px;
  }
  
  .nav-menu-item {
    padding: 6px 10px;
  }
  
  .nav-menu-item a {
    font-size: 0.85rem;
  }
  
  .welcome-text {
    font-size: 0.8rem;
  }
}

@media (max-width: 768px) {
  .nav-container {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto auto;
    text-align: center;
    gap: 10px;
  }
  
  .nav-item-left,
  .nav-item-center,
  .nav-item-right {
    justify-self: center;
  }
  
  .nav-item-center {
    order: 2;
  }
  
  .nav-item-right {
    order: 3;
  }
  
  .app-header {
    padding: 15px 0;
  }
  
  .user-info {
    order: 1;
  }
}

@media (max-width: 480px) {
  .nav-container {
    padding: 0 10px;
  }
  
  .nav-ul {
    flex-wrap: wrap;
    justify-content: center;
    gap: 8px;
  }
  
  .nav-menu-item {
    padding: 4px 8px;
  }
  
  .nav-menu-item a {
    font-size: 0.8rem;
  }
  
  .logo {
    font-size: 1rem;
  }
  
  .welcome-text {
    font-size: 0.75rem;
  }
  
  .logout-btn {
    font-size: 0.8rem;
  }
}
</style>
