// Configuration per diversi ambienti
const config = {
  development: {
    API_BASE_URL: 'http://localhost:5000',
    WS_BASE_URL: 'ws://localhost:5000'
  },
  production: {
    API_BASE_URL: process.env.VITE_API_URL || 'https://yourdomain.com',
    WS_BASE_URL: process.env.VITE_WS_URL || 'wss://yourdomain.com'
  },
  local_network: {
    // Sostituisci con il tuo IP locale
    API_BASE_URL: process.env.VITE_API_URL || 'http://192.168.1.100:5000',
    WS_BASE_URL: process.env.VITE_WS_URL || 'ws://192.168.1.100:5000'
  }
}

// Determina ambiente automaticamente
const getEnvironment = () => {
  if (import.meta.env.PROD) return 'production'
  if (import.meta.env.VITE_NETWORK_MODE === 'local') return 'local_network'
  return 'development'
}

const currentConfig = config[getEnvironment()]

export default currentConfig
