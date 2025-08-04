#!/bin/bash

# Test script per verificare la configurazione di rete

echo "🧪 Test configurazione DreamKeeper..."

# Verifica IP locale con metodi diversi
LOCAL_IP=$(ip route get 1.1.1.1 2>/dev/null | grep -oP 'src \K\S+' || hostname -I 2>/dev/null | awk '{print $1}' || ip addr show | grep 'inet ' | grep -v '127.0.0.1' | head -n1 | awk '{print $2}' | cut -d/ -f1 || echo "IP_NON_RILEVATO")
echo "📡 IP locale: $LOCAL_IP"

# Test connettività porte
echo "🔍 Test porte..."

# Test porta backend
if timeout 3 bash -c "</dev/tcp/localhost/5000" 2>/dev/null; then
    echo "✅ Porta backend 5000: APERTA"
else
    echo "❌ Porta backend 5000: CHIUSA"
fi

# Test porta frontend
if timeout 3 bash -c "</dev/tcp/localhost/5173" 2>/dev/null; then
    echo "✅ Porta frontend 5173: APERTA"
else
    echo "❌ Porta frontend 5173: CHIUSA"
fi

# Test API health
echo "🏥 Test API health..."
if command -v curl >/dev/null 2>&1; then
    HEALTH_RESPONSE=$(curl -s -w "%{http_code}" http://localhost:5000/api/health -o /dev/null)
    if [ "$HEALTH_RESPONSE" = "200" ]; then
        echo "✅ API Backend: HEALTHY"
    else
        echo "❌ API Backend: NON RISPONDE (HTTP $HEALTH_RESPONSE)"
    fi
else
    echo "⚠️  curl non disponibile, impossibile testare API"
fi

# Test configurazione CORS
echo "🌐 Test configurazione CORS..."
cd /home/daniele/dream/backend 2>/dev/null || { echo "❌ Directory backend non trovata in $(pwd)"; exit 1; }

if [ -f ".env" ]; then
    echo "✅ File .env trovato"
    echo "📋 Contenuto CORS_ORIGINS:"
    grep CORS_ORIGINS .env || echo "⚠️  CORS_ORIGINS non configurato"
else
    echo "⚠️  File .env non trovato - verrà creato al primo avvio"
fi

echo ""
echo "🔥 Test completato!"
echo "📝 Per avviare i servizi: ./start-local-network.sh"
echo "🛑 Per fermare i servizi: ./stop-local-network.sh"
