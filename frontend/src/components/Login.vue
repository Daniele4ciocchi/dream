<!--
  COMPONENTE LOGIN - SCHERMATA DI ACCESSO
  
  Questo componente gestisce l'autenticazione degli utenti con:
  - Form di login con validazione in tempo reale
  - Integrazione con il backend API
  - Gestione errori e stati di caricamento
  - Design responsive e accessibile
-->
<template>
  <!-- Container principale che centra il form di login -->
  <div class="login-container">
    <!-- Card contenente tutto il form di login -->
    <div class="login-card">
      
      <!-- HEADER - Titolo e descrizione -->
      <div class="login-header">
        <h2>🌙 Accedi a DreamKeeper</h2>
        <p>Bentornato! Accedi per continuare il tuo viaggio nei sogni.</p>
      </div>

      <!-- FORM PRINCIPALE - Gestisce l'invio con @submit.prevent -->
      <form @submit.prevent="login" class="login-form">
        
        <!-- CAMPO EMAIL -->
        <div class="form-group">
          <label for="email">📧 Email</label>
          <!-- Input con binding bidirezionale e validazione -->
          <input 
            type="email" 
            id="email"
            v-model="email"
            placeholder="Inserisci la tua email" 
            required
            :class="{ 'error': emailError }"
          >
          <!-- Messaggio di errore mostrato solo se c'è un errore -->
          <span v-if="emailError" class="error-message">{{ emailError }}</span>
        </div>

        <!-- CAMPO PASSWORD -->
        <div class="form-group">
          <label for="password">🔒 Password</label>
          <!-- Input password con binding bidirezionale -->
          <input 
            type="password" 
            id="password"
            v-model="password"
            placeholder="Inserisci la tua password" 
            required
            :class="{ 'error': passwordError }"
          >
          <!-- Messaggio di errore mostrato solo se c'è un errore -->
          <span v-if="passwordError" class="error-message">{{ passwordError }}</span>
        </div>

        <!-- PULSANTE DI INVIO - Disabilitato durante il caricamento -->
        <button type="submit" class="login-button" :disabled="isLoading">
          <!-- Testo dinamico basato sullo stato di caricamento -->
          <span v-if="isLoading">⚡ Accesso in corso...</span>
          <span v-else>✨ Accedi</span>
        </button>

        <!-- ALERT ERRORE GENERALE - Mostrato solo se c'è un errore di login -->
        <div v-if="loginError" class="error-alert">
          {{ loginError }}
        </div>
      </form>

      <!-- FOOTER - Link alla registrazione -->
      <div class="login-footer">
        <p>Non hai ancora un account? 
          <router-link to="/register" class="register-link">Registrati qui</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
/*
  LOGICA JAVASCRIPT DEL COMPONENTE LOGIN
  
  Il componente utilizza:
  - Composition API di Vue 3 per gestire lo stato di autenticazione
  - Validazione in tempo reale dei campi del form
  - Chiamate API per l'autenticazione
  - Gestione errori e stati di caricamento
*/

// IMPORT DELLE DIPENDENZE
import api from '../utils/api.js';           // Utility per chiamate API
import { useAuth } from '../utils/auth.js';  // Store globale per autenticazione

export default {
  name: 'Login',
  
  // DATA - Stato reattivo del componente
  data() {
    return {
      // Campi del form
      email: '',
      password: '',
      
      // Messaggi di errore per ogni campo
      emailError: '',
      passwordError: '',
      loginError: '',      // Errore generale di login
      
      // Stato di caricamento
      isLoading: false
    };
  },
  
  // METHODS - Metodi del componente
  methods: {
    
    // VALIDAZIONE FORM - Controlla tutti i campi prima dell'invio
    validateForm() {
      // Reset degli errori precedenti
      this.emailError = '';
      this.passwordError = '';
      this.loginError = '';
      
      let isValid = true;
      
      // Validazione email
      if (!this.email) {
        this.emailError = 'Email è richiesta';
        isValid = false;
      } else if (!this.isValidEmail(this.email)) {
        this.emailError = 'Inserisci un\'email valida';
        isValid = false;
      }
      
      // Validazione password
      if (!this.password) {
        this.passwordError = 'Password è richiesta';
        isValid = false;
      } else if (this.password.length < 6) {
        this.passwordError = 'Password deve essere di almeno 6 caratteri';
        isValid = false;
      }
      
      return isValid;
    },
    
    // VALIDAZIONE EMAIL - Verifica formato email con regex
    isValidEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    },
    
    // LOGIN PRINCIPALE - Gestisce l'autenticazione dell'utente
    async login() {
      // Se la validazione fallisce, interrompe l'esecuzione
      if (!this.validateForm()) return;
      
      // Attiva lo stato di caricamento
      this.isLoading = true;
      
      try {
        // Chiamata API per l'autenticazione
        const response = await api.post('/api/auth/login', {
          email: this.email,
          password: this.password
        });
        
        // Salva l'utente nello store globale con token
        const { login } = useAuth();
        login(response.data.user, response.data.access_token);
        
        // Reindirizza alla home page dopo il login
        this.$router.push('/profile');
        
      } catch (error) {
        // Disattiva lo stato di caricamento in caso di errore
        this.isLoading = false;
        
        // Gestione degli errori dalla risposta API
        if (error.response && error.response.data) {
          this.loginError = error.response.data.message || 'Errore durante il login';
        } else {
          // Errore generico di connessione
          this.loginError = 'Errore di connessione. Riprova più tardi.';
        }
      }
    }
  }
};
</script>

<style scoped>
/*
  STILI CSS DEL COMPONENTE LOGIN
  
  Il CSS è "scoped" quindi si applica solo a questo componente.
  Utilizza un design moderno con:
  - Layout centrato e responsive
  - Gradiente per i colori del brand
  - Animazioni e transizioni fluide
  - Stati di focus e hover per migliorare l'UX
*/

/* CONTAINER PRINCIPALE - Centra la card di login */
.login-container {
  display: flex;                    /* Layout flexbox */
  justify-content: center;          /* Centramento orizzontale */
  align-items: center;              /* Centramento verticale */
  min-height: calc(100vh - 120px);  /* Altezza minima meno header */
  padding: 2rem;                    /* Padding responsivo */
  flex: 1;                          /* Prende tutto lo spazio disponibile */
}

/* CARD PRINCIPALE - Contenitore del form */
.login-card {
  background: #f7f6fa;             /* Sfondo chiaro */
  border-radius: 16px;             /* Angoli arrotondati */
  padding: 2.5rem;                 /* Padding interno */
  width: 100%;                     /* Larghezza completa */
  max-width: 450px;                /* Larghezza massima per desktop */
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);  /* Ombra profonda */
  border: 2px solid #4b2e83;       /* Bordo del brand */
  color: #333 !important;          /* Forza il colore del testo */
}

/* HEADER - Titolo e descrizione */
.login-header {
  text-align: center;              /* Testo centrato */
  margin-bottom: 2rem;             /* Spazio sotto */
}

.login-header h2 {
  color: #4b2e83;                  /* Colore brand primario */
  font-size: 1.8rem;               /* Dimensione grande */
  margin-bottom: 0.5rem;           /* Spazio sotto ridotto */
  font-weight: 600;                /* Peso del font semi-bold */
}

.login-header p {
  color: #666;                     /* Grigio per il sottotitolo */
  font-size: 1rem;                 /* Dimensione normale */
  margin: 0;                       /* Rimuove margini */
}

/* FORM - Contenitore principale del form */
.login-form {
  margin-bottom: 1.5rem;           /* Spazio sotto il form */
}

/* GRUPPO FORM - Contenitore per ogni campo */
.form-group {
  margin-bottom: 1.5rem;           /* Spazio tra i campi */
}

/* LABEL - Etichette dei campi */
.form-group label {
  display: block;                  /* Display a blocco */
  color: #4b2e83;                  /* Colore brand */
  font-weight: 500;                /* Peso del font medio */
  margin-bottom: 0.5rem;           /* Spazio sotto */
  font-size: 1rem;                 /* Dimensione standard */
}

/* INPUT - Campi di input */
.form-group input {
  width: 100%;                     /* Larghezza completa */
  padding: 12px 16px;              /* Padding interno */
  border: 2px solid #ddd;          /* Bordo grigio chiaro */
  border-radius: 8px;              /* Angoli arrotondati */
  font-size: 1rem;                 /* Dimensione testo */
  transition: all 0.3s ease;       /* Transizione fluida */
  background: white !important;     /* Forza sfondo bianco */
  color: #333 !important;          /* Forza colore testo scuro */
  box-sizing: border-box;          /* Include padding nel calcolo larghezza */
}

/* PLACEHOLDER - Testo segnaposto negli input */
.form-group input::placeholder {
  color: #999 !important;          /* Grigio chiaro per placeholder */
}

/* FOCUS - Stato di focus degli input */
.form-group input:focus {
  outline: none;                   /* Rimuove outline default */
  border-color: #4b2e83;           /* Bordo brand in focus */
  box-shadow: 0 0 0 3px rgba(75, 46, 131, 0.1);  /* Ombra colorata */
}

/* ERRORE - Stato di errore degli input */
.form-group input.error {
  border-color: #e74c3c;           /* Bordo rosso per errori */
  background-color: #fdf2f2;       /* Sfondo rosso chiaro */
}

/* MESSAGGIO ERRORE - Testo di errore sotto gli input */
.error-message {
  color: #e74c3c;                  /* Rosso per errori */
  font-size: 0.875rem;             /* Testo più piccolo */
  margin-top: 0.25rem;             /* Piccolo spazio sopra */
  display: block;                  /* Display a blocco */
}

/* PULSANTE LOGIN - Pulsante principale */
.login-button {
  width: 100%;                     /* Larghezza completa */
  background: linear-gradient(135deg, #4b2e83 0%, #6c47a3 100%);  /* Gradiente brand */
  color: white;                    /* Testo bianco */
  border: none;                    /* Nessun bordo */
  padding: 14px 20px;              /* Padding generoso */
  border-radius: 8px;              /* Angoli arrotondati */
  font-size: 1.1rem;               /* Testo leggermente più grande */
  font-weight: 600;                /* Font semi-bold */
  cursor: pointer;                 /* Cursore a puntatore */
  transition: all 0.3s ease;       /* Transizione fluida */
  text-transform: none;            /* Non trasforma il testo */
}

/* HOVER - Stato hover del pulsante (escluso quando disabilitato) */
.login-button:hover:not(:disabled) {
  background: linear-gradient(135deg, #5d3a99 0%, #7d57b3 100%);  /* Gradiente più scuro */
  transform: translateY(-2px);     /* Solleva il pulsante */
  box-shadow: 0 8px 20px rgba(75, 46, 131, 0.3);  /* Ombra più profonda */
}

/* DISABILITATO - Stato disabilitato del pulsante */
.login-button:disabled {
  opacity: 0.7;                    /* Trasparenza ridotta */
  cursor: not-allowed;             /* Cursore non permesso */
  transform: none;                 /* Nessun movimento */
}

/* ALERT ERRORE - Messaggio di errore generale */
.error-alert {
  background: #fdf2f2;             /* Sfondo rosso chiaro */
  border: 1px solid #e74c3c;       /* Bordo rosso */
  color: #e74c3c;                  /* Testo rosso */
  padding: 12px;                   /* Padding interno */
  border-radius: 8px;              /* Angoli arrotondati */
  margin-top: 1rem;                /* Spazio sopra */
  text-align: center;              /* Testo centrato */
  font-size: 0.9rem;               /* Testo leggermente più piccolo */
}

/* FOOTER - Area con link alla registrazione */
.login-footer {
  text-align: center;              /* Testo centrato */
  color: #666;                     /* Grigio */
}

.login-footer p {
  margin: 0;                       /* Nessun margine */
  font-size: 0.9rem;               /* Testo più piccolo */
}

/* LINK REGISTRAZIONE - Link alla pagina di registrazione */
.register-link {
  color: #4b2e83;                  /* Colore brand */
  text-decoration: none;           /* Nessuna sottolineatura */
  font-weight: 600;                /* Font semi-bold */
  transition: color 0.3s ease;     /* Transizione del colore */
}

/* HOVER LINK - Stato hover del link */
.register-link:hover {
  color: #6c47a3;                  /* Colore più chiaro in hover */
  text-decoration: underline;       /* Sottolineatura in hover */
}

/* MEDIA QUERY - Responsive per dispositivi mobili */
@media (max-width: 480px) {
  .login-container {
    padding: 1rem;                 /* Padding ridotto */
  }
  
  .login-card {
    padding: 1.5rem;               /* Padding card ridotto */
  }
  
  .login-header h2 {
    font-size: 1.5rem;             /* Titolo più piccolo */
  }
}
</style>
