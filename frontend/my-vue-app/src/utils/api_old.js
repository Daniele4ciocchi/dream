import axios from 'axios';

// ===== CONFIGURAZIONE BASE =====
const api = axios.create({
  baseURL: 'http://localhost:5000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// ===== AGGIUNGI TOKEN AUTOMATICAMENTE =====
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  
  console.log('🚀 API Request:', config.method?.toUpperCase(), config.url)
  console.log('🔑 Token presente:', token ? 'SÌ' : 'NO')
  
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
    console.log('✅ Token aggiunto all\'header')
  }
  
  return config
}, (error) => {
  console.error('💥 Errore richiesta:', error)
  return Promise.reject(error)
})

// ===== GESTIONE RISPOSTE =====
api.interceptors.response.use(
  (response) => {
    console.log('✅ Risposta OK:', response.status, response.config.url)
    return response
  },
  (error) => {
    console.error('💥 Errore API:', error.response?.status, error.config?.url)
    console.error('💥 Messaggio:', error.response?.data?.message)
    
    // Per ora NON facciamo logout automatico sui 401
    // Lasciamo che i componenti decidano cosa fare
    
    return Promise.reject(error)
  }
)

export default api
