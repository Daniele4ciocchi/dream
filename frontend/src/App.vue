<template>
  <div class="app">
    <header class="app-header">
      <div class="nav-container">
        <!-- Logo sempre visibile -->
        <div class="nav-item nav-item-left">
          <div class="nav-menu-item">
            <router-link class="logo" to="/home" @click="closeMobileMenu">DreamKeeper</router-link>
          </div>
        </div>

        <!-- Hamburger menu per mobile -->
        <button class="mobile-menu-toggle" @click="toggleMobileMenu" :class="{ active: isMobileMenuOpen }">
          <span></span>
          <span></span>
          <span></span>
        </button>

        <!-- Menu responsive -->
        <div class="nav-menu" :class="{ 'mobile-open': isMobileMenuOpen }">
          <!-- Menu centrale -->
          <div class="nav-item nav-item-center">
            <ul class="nav-ul">
              <li class="nav-menu-item">
                <router-link to="/" @click="closeMobileMenu">Feed</router-link>
              </li>
              <li class="nav-menu-item">
                <router-link to="/pomodoro" @click="closeMobileMenu">Pomodoro</router-link>
              </li>
              <li class="nav-menu-item" v-if="isAuthenticated">
                <router-link to="/dreams" @click="closeMobileMenu">My Dreams</router-link>
              </li>
              <li class="nav-menu-item" v-if="isAuthenticated">
                <router-link to="/find" @click="closeMobileMenu">Find</router-link>
              </li>
            </ul>
          </div>

          <!-- Menu destro -->
          <div class="nav-item nav-item-right">
            <ul class="nav-ul">
              <!-- Mostra login/register se NON autenticato -->
              <template v-if="!isAuthenticated">
                <li class="nav-menu-item">
                  <router-link to="/login" @click="closeMobileMenu">Login</router-link>
                </li>
                <li class="nav-menu-item">
                  <router-link to="/register" @click="closeMobileMenu">Register</router-link>
                </li>
                <li class="nav-menu-item">
                  <router-link to="/login" @click="closeMobileMenu">
                    <svg class="feather" id="Login">
                      <use href="/feather-sprite-v4.29.0.svg#user"></use>
                    </svg>
                  </router-link>
                </li>
              </template>
              
              <!-- Mostra profilo e logout se autenticato -->
              <template v-else>
                <li class="nav-menu-item">
                  <router-link to="/profile" class="profile-link" @click="closeMobileMenu">
                    <svg class="feather">
                      <use href="/feather-sprite-v4.29.0.svg#user"></use>
                    </svg>
                    <span class="welcome-text">{{ userName }}</span>
                  </router-link>
                </li>
                <li class="nav-menu-item">
                  <button @click="logout(); closeMobileMenu()" class="logout-btn">
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
      </div>
    </header>

    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useAuth } from './utils/auth.js'
import { useRouter } from 'vue-router'

const { store, initAuth, logout: authLogout } = useAuth()
const router = useRouter()

// Stato per il menu mobile
const isMobileMenuOpen = ref(false)

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

// Toggle menu mobile
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

// Chiudi menu quando si clicca su un link
const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
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
  padding: 10px 0;
}

.nav-container {
  display: flex;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  position: relative;
  justify-content: center;
}

/* Logo */
.nav-item-left {
  background-color: rgba(74, 46, 131, 0.5);
  backdrop-filter: blur(10px);
  color: white;
  border: 2px solid rgba(74, 46, 131, 0.5);
  border-radius: 12px;
  padding: 8px 16px;
  transition: all 0.3s ease;
  position: absolute;
  left: 20px;
}

.nav-item-left:hover {
  background-color: rgba(74, 46, 131, 0.3);
  border-color: rgba(74, 46, 131, 0.7);
}

.logo {
  text-decoration: none;
  color: white;
  font-weight: 600;
  font-size: 1.1rem;
}

/* Hamburger menu (nascosto su desktop) */
.mobile-menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: space-around;
  width: 30px;
  height: 30px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 1001;
}

.mobile-menu-toggle span {
  width: 25px;
  height: 3px;
  background: #4b2e83;
  border-radius: 2px;
  transition: all 0.3s ease;
  transform-origin: 1px;
}

.mobile-menu-toggle.active span:first-child {
  transform: rotate(45deg);
}

.mobile-menu-toggle.active span:nth-child(2) {
  opacity: 0;
}

.mobile-menu-toggle.active span:nth-child(3) {
  transform: rotate(-45deg);
}

/* Menu principale */
.nav-menu {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-item-right {
  position: absolute;
  right: 20px;
}

.nav-item {
  display: flex;
  align-items: center;
  background-color: rgba(74, 46, 131, 0.5);
  backdrop-filter: blur(10px);
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

.profile-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.welcome-text {
  color: white;
  font-weight: 500;
  font-size: 0.9rem;
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



@media (max-width: 1000px) {
  .nav-container {
    padding: 0 15px;
    justify-content: space-between;
  }
  
  .nav-item-left {
    position: static;
    left: auto;
  }
  
  .nav-item-right {
    position: static;
    right: auto;
  }
  
  /* Mostra hamburger menu */
  .mobile-menu-toggle {
    display: flex;
  }
  
  /* Menu mobile */
  .nav-menu {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(20px);
    border-radius: 0 0 15px 15px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    border: 1px solid rgba(74, 46, 131, 0.2);
    flex-direction: column;
    gap: 0;
    padding: 20px;
    transform: translateY(-20px);
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
  }
  
  .nav-menu.mobile-open {
    transform: translateY(0);
    opacity: 1;
    visibility: visible;
  }
  
  .nav-item-center,
  .nav-item-right {
    width: 100%;
    margin-bottom: 15px;
    background: transparent;
    border: none;
    padding: 0;
  }
  
  .nav-item-center:hover,
  .nav-item-right:hover {
    background: transparent;
    border: none;
  }
  
  .nav-ul {
    flex-direction: column;
    gap: 8px;
    width: 100%;
  }
  
  .nav-menu-item {
    width: 100%;
    text-align: center;
    padding: 12px;
    background: rgba(74, 46, 131, 0.1);
    border: 1px solid rgba(74, 46, 131, 0.2);
    border-radius: 8px;
    color: #4b2e83;
  }
  
  .nav-menu-item:hover {
    background: rgba(74, 46, 131, 0.2);
    border-color: rgba(74, 46, 131, 0.4);
  }
  
  .nav-menu-item a {
    color: #4b2e83;
    font-weight: 500;
  }
  
  .nav-menu-item a.router-link-active {
    color: #6c47a3;
    font-weight: 700;
  }
  
  .welcome-text {
    color: #4b2e83;
  }
  
  .logout-btn {
    color: #4b2e83;
    justify-content: center;
    width: 100%;
  }
  
  .logout-btn:hover {
    color: #ff6b6b;
  }
  
  .app-header {
    padding: 15px 0;
  }
}

@media (max-width: 480px) {
  .nav-container {
    padding: 0 10px;
  }
  
  .logo {
    font-size: 1rem;
  }
  
  .nav-menu {
    padding: 15px;
  }
  
  .nav-menu-item {
    padding: 10px;
  }
  
  .nav-menu-item a {
    font-size: 0.9rem;
  }
  
  .welcome-text {
    font-size: 0.8rem;
  }
  
  .logout-btn {
    font-size: 0.9rem;
  }
}
</style>
