#!/bin/bash

# Script per avviare DreamKeeper sulla rete locale

echo "🌙 Avvio DreamKeeper per rete locale..."

# Ottieni IP locale con metodi diversi
LOCAL_IP=$(ip route get 1.1.1.1 2>/dev/null | grep -oP 'src \K\S+' || hostname -I 2>/dev/null | awk '{print $1}' || ip addr show | grep 'inet ' | grep -v '127.0.0.1' | head -n1 | awk '{print $2}' | cut -d/ -f1 || echo "192.168.1.100")
echo "📡 IP locale rilevato: $LOCAL_IP"

# Crea file .env per backend se non esiste
if [ ! -f backend/.env ]; then
    echo "📝 Creazione file .env per backend..."
    cp backend/.env.example backend/.env
    sed -i "s/http:\/\/localhost:5173/http:\/\/$LOCAL_IP:5173/g" backend/.env
fi

# Aggiorna sempre il CORS per includere l'IP locale corrente
echo "🔧 Configurazione CORS per IP locale: $LOCAL_IP"
cat > backend/.env << EOF
# Development environment variables
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000

# Database
DATABASE_URL=sqlite:///dream_keeper.db

# Security Keys
SECRET_KEY=your-super-secret-development-key-2024
JWT_SECRET_KEY=your-jwt-secret-development-key-2024

# Network Configuration per rete locale
FRONTEND_URL=http://$LOCAL_IP:5173

# CORS Origins (includiamo sia localhost che IP locale)
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://$LOCAL_IP:5173,http://localhost:3000,http://$LOCAL_IP:3000
EOF

# Crea file .env per frontend se non esiste
if [ ! -f frontend/.env ]; then
    echo "📝 Creazione file .env per frontend..."
    cat > frontend/.env << EOF
VITE_API_URL=http://$LOCAL_IP:5000
VITE_NETWORK_MODE=local
EOF
fi

echo "🔧 Configurazione completata!"
echo "🌐 Backend sarà disponibile su: http://$LOCAL_IP:5000"
echo "🎨 Frontend sarà disponibile su: http://$LOCAL_IP:5173"
echo ""
echo "📱 Per accedere da altri dispositivi sulla stessa rete:"
echo "   - Assicurati che il firewall permetta le connessioni sulle porte 5000 e 5173"
echo "   - Usa l'URL: http://$LOCAL_IP:5173"
echo ""
echo "⚠️  IMPORTANTE: Questo setup è solo per rete locale, non per internet!"

# Avvia i servizi in background
echo "🚀 Avvio servizi..."

# Avvia backend
cd backend
echo "🔧 Avvio backend..."

# Controlla se esiste virtual environment
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment non trovato. Creazione..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo "🐍 Ambiente Python attivato: $(which python)"
python run.py &
BACKEND_PID=$!

# Attendi che il backend si avvii
sleep 3

# Avvia frontend
cd ../frontend/my-vue-app
echo "🎨 Avvio frontend..."

# Controlla se esistono node_modules
if [ ! -d "node_modules" ]; then
    echo "📦 Installazione dipendenze npm..."
    npm install
fi

echo "🌐 Frontend configurato per: $LOCAL_IP"
npm run dev &
FRONTEND_PID=$!

echo "✅ Servizi avviati!"
echo "🔄 Backend PID: $BACKEND_PID"
echo "🔄 Frontend PID: $FRONTEND_PID"
echo ""
echo "🌐 Accesso locale:"
echo "   • Da questo computer: http://localhost:5173"
echo "   • Da altri dispositivi: http://$LOCAL_IP:5173"
echo ""
echo "🔧 API Backend disponibile su:"
echo "   • http://localhost:5000"
echo "   • http://$LOCAL_IP:5000"
echo ""
echo "🛑 Per fermare i servizi:"
echo "   • Usa Ctrl+C su questo terminale, oppure"
echo "   • Esegui: ./stop-local-network.sh"
echo "   • O manualmente: kill $BACKEND_PID $FRONTEND_PID"

# Mantieni lo script attivo
wait
