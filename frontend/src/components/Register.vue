<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <h2>✨ Unisciti a DreamKeeper</h2>
        <p>Crea il tuo account e inizia a custodire i tuoi sogni oggi stesso.</p>
      </div>

      <form @submit.prevent="register" class="register-form">
        <div class="form-group">
          <label for="username">👤 Nome Utente</label>
          <input 
            type="text" 
            id="username"
            v-model="username" 
            placeholder="Scegli un nome utente" 
            required
            :class="{ 'error': usernameError }"
          >
          <span v-if="usernameError" class="error-message">{{ usernameError }}</span>
        </div>

        <div class="form-group">
          <label for="email">📧 Email</label>
          <input 
            type="email" 
            id="email"
            v-model="email" 
            placeholder="Inserisci la tua email" 
            required
            :class="{ 'error': emailError }"
          >
          <span v-if="emailError" class="error-message">{{ emailError }}</span>
        </div>

        <div class="form-group">
          <label for="password">🔒 Password</label>
          <input 
            type="password" 
            id="password"
            v-model="password" 
            placeholder="Crea una password sicura" 
            required
            :class="{ 'error': passwordError }"
          >
          <span v-if="passwordError" class="error-message">{{ passwordError }}</span>
          <div class="password-strength">
            <div class="strength-indicator" :class="passwordStrength.class">
              {{ passwordStrength.text }}
            </div>
          </div>
        </div>

        <div class="form-group">
          <label for="confirmPassword">🔐 Conferma Password</label>
          <input 
            type="password" 
            id="confirmPassword"
            v-model="confirmPassword" 
            placeholder="Ripeti la password" 
            required
            :class="{ 'error': confirmPasswordError }"
          >
          <span v-if="confirmPasswordError" class="error-message">{{ confirmPasswordError }}</span>
        </div>

        <div class="form-group checkbox-group">
          <label class="checkbox-label">
            <input type="checkbox" v-model="acceptTerms" required>
            <span class="checkmark"></span>
            Accetto i <a href="#" class="terms-link">termini e condizioni</a>
          </label>
          <span v-if="termsError" class="error-message">{{ termsError }}</span>
        </div>

        <button type="submit" class="register-button" :disabled="isLoading">
          <span v-if="isLoading">⚡ Registrazione in corso...</span>
          <span v-else>🌟 Crea Account</span>
        </button>

        <div v-if="registerError" class="error-alert">
          {{ registerError }}
        </div>

        <div v-if="successMessage" class="success-alert">
          {{ successMessage }}
        </div>
      </form>

      <div class="register-footer">
        <p>Hai già un account? 
          <router-link to="/login" class="login-link">Accedi qui</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../utils/api.js';
import { useAuth } from '../utils/auth.js';

export default {
  name: 'Register',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      acceptTerms: false,
      usernameError: '',
      emailError: '',
      passwordError: '',
      confirmPasswordError: '',
      termsError: '',
      registerError: '',
      successMessage: '',
      isLoading: false
    };
  },
  computed: {
    passwordStrength() {
      if (!this.password) return { text: '', class: '' };
      
      let score = 0;
      let text = '';
      let className = '';
      
      // Lunghezza
      if (this.password.length >= 8) score++;
      if (this.password.length >= 12) score++;
      
      // Caratteri speciali
      if (/[a-z]/.test(this.password)) score++;
      if (/[A-Z]/.test(this.password)) score++;
      if (/\d/.test(this.password)) score++;
      if (/[^a-zA-Z0-9]/.test(this.password)) score++;
      
      if (score <= 2) {
        text = 'Debole';
        className = 'weak';
      } else if (score <= 4) {
        text = 'Media'; 
        className = 'medium';
      } else {
        text = 'Forte';
        className = 'strong';
      }
      
      return { text, class: className };
    }
  },
  methods: {
    validateForm() {
      this.usernameError = '';
      this.emailError = '';
      this.passwordError = '';
      this.confirmPasswordError = '';
      this.termsError = '';
      this.registerError = '';
      
      let isValid = true;
      
      // Username validation
      if (!this.username) {
        this.usernameError = 'Nome utente è richiesto';
        isValid = false;
      } else if (this.username.length < 3) {
        this.usernameError = 'Nome utente deve essere di almeno 3 caratteri';
        isValid = false;
      } else if (!/^[a-zA-Z0-9_]+$/.test(this.username)) {
        this.usernameError = 'Nome utente può contenere solo lettere, numeri e underscore';
        isValid = false;
      }
      
      // Email validation
      if (!this.email) {
        this.emailError = 'Email è richiesta';
        isValid = false;
      } else if (!this.isValidEmail(this.email)) {
        this.emailError = 'Inserisci un\'email valida';
        isValid = false;
      }
      
      // Password validation
      if (!this.password) {
        this.passwordError = 'Password è richiesta';
        isValid = false;
      } else if (this.password.length < 8) {
        this.passwordError = 'Password deve essere di almeno 8 caratteri';
        isValid = false;
      } else if (!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(this.password)) {
        this.passwordError = 'Password deve contenere almeno una lettera minuscola, maiuscola e un numero';
        isValid = false;
      }
      
      // Confirm password validation
      if (!this.confirmPassword) {
        this.confirmPasswordError = 'Conferma password è richiesta';
        isValid = false;
      } else if (this.password !== this.confirmPassword) {
        this.confirmPasswordError = 'Le password non coincidono';
        isValid = false;
      }
      
      // Terms validation
      if (!this.acceptTerms) {
        this.termsError = 'Devi accettare i termini e condizioni';
        isValid = false;
      }
      
      return isValid;
    },
    
    isValidEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    },
    
    async register() {
      if (!this.validateForm()) return;
      
      this.isLoading = true;
      try {
        const response = await api.post('/api/auth/register', {
          username: this.username,
          email: this.email,
          password: this.password
        });
        
        this.successMessage = 'Registrazione completata con successo! Reindirizzamento al login...';
        
        // Reindirizza dopo 2 secondi
        setTimeout(() => {
          this.$router.push('/login');
        }, 2000);
        
      } catch (error) {
        this.isLoading = false;
        if (error.response && error.response.data) {
          this.registerError = error.response.data.message || 'Errore durante la registrazione';
        } else {
          this.registerError = 'Errore di connessione. Riprova più tardi.';
        }
      }
    }
  }
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 120px);
  padding: 2rem;
  flex: 1;
}

.register-card {
  background: #f7f6fa;
  border-radius: 16px;
  padding: 2.5rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  border: 2px solid #4b2e83;
  color: #333 !important;
}

.register-header {
  text-align: center;
  margin-bottom: 2rem;
}

.register-header h2 {
  color: #4b2e83;
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.register-header p {
  color: #666;
  font-size: 1rem;
  margin: 0;
}

.register-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  color: #4b2e83;
  font-weight: 500;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.form-group input[type="text"],
.form-group input[type="email"],
.form-group input[type="password"] {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white !important;
  color: #333 !important;
  box-sizing: border-box;
}

.form-group input::placeholder {
  color: #999 !important;
}

.form-group input:focus {
  outline: none;
  border-color: #4b2e83;
  box-shadow: 0 0 0 3px rgba(75, 46, 131, 0.1);
}

.form-group input.error {
  border-color: #e74c3c;
  background-color: #fdf2f2;
}

.error-message {
  color: #e74c3c;
  font-size: 0.875rem;
  margin-top: 0.25rem;
  display: block;
}

.password-strength {
  margin-top: 0.5rem;
}

.strength-indicator {
  font-size: 0.875rem;
  font-weight: 500;
  padding: 2px 8px;
  border-radius: 4px;
  display: inline-block;
}

.strength-indicator.weak {
  background-color: #ffebee;
  color: #e74c3c;
}

.strength-indicator.medium {
  background-color: #fff3e0;
  color: #ff9800;
}

.strength-indicator.strong {
  background-color: #e8f5e8;
  color: #4caf50;
}

.checkbox-group {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.9rem;
  color: #666;
  line-height: 1.4;
}

.checkbox-label input[type="checkbox"] {
  margin: 0;
  width: auto;
}

.terms-link {
  color: #4b2e83;
  text-decoration: none;
}

.terms-link:hover {
  text-decoration: underline;
}

.register-button {
  width: 100%;
  background: linear-gradient(135deg, #4b2e83 0%, #6c47a3 100%);
  color: white;
  border: none;
  padding: 14px 20px;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: none;
}

.register-button:hover:not(:disabled) {
  background: linear-gradient(135deg, #5d3a99 0%, #7d57b3 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(75, 46, 131, 0.3);
}

.register-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.error-alert {
  background: #fdf2f2;
  border: 1px solid #e74c3c;
  color: #e74c3c;
  padding: 12px;
  border-radius: 8px;
  margin-top: 1rem;
  text-align: center;
  font-size: 0.9rem;
}

.success-alert {
  background: #e8f5e8;
  border: 1px solid #4caf50;
  color: #2e7d32;
  padding: 12px;
  border-radius: 8px;
  margin-top: 1rem;
  text-align: center;
  font-size: 0.9rem;
}

.register-footer {
  text-align: center;
  color: #666;
}

.register-footer p {
  margin: 0;
  font-size: 0.9rem;
}

.login-link {
  color: #4b2e83;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.login-link:hover {
  color: #6c47a3;
  text-decoration: underline;
}

@media (max-width: 480px) {
  .register-container {
    padding: 1rem;
  }
  
  .register-card {
    padding: 1.5rem;
  }
  
  .register-header h2 {
    font-size: 1.5rem;
  }
}
</style>
