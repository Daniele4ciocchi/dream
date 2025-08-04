#!/bin/bash

# Script per fermare DreamKeeper

echo "🛑 Arresto DreamKeeper..."

# Trova e ferma tutti i processi Python e Node relativi al progetto
echo "🔍 Ricerca processi attivi..."

# Ferma backend Flask
FLASK_PIDS=$(pgrep -f "python.*run.py")
if [ ! -z "$FLASK_PIDS" ]; then
    echo "🐍 Arresto backend Flask (PID: $FLASK_PIDS)..."
    kill $FLASK_PIDS
fi

# Ferma frontend Vue/Vite
VITE_PIDS=$(pgrep -f "vite.*dev")
if [ ! -z "$VITE_PIDS" ]; then
    echo "🎨 Arresto frontend Vite (PID: $VITE_PIDS)..."
    kill $VITE_PIDS
fi

# Ferma processi npm dev
NPM_PIDS=$(pgrep -f "npm.*run.*dev")
if [ ! -z "$NPM_PIDS" ]; then
    echo "📦 Arresto processi npm dev (PID: $NPM_PIDS)..."
    kill $NPM_PIDS
fi

# Aspetta un po' e poi forza la chiusura se necessario
sleep 2

# Controllo finale e force kill se necessario
REMAINING_FLASK=$(pgrep -f "python.*run.py")
REMAINING_VITE=$(pgrep -f "vite.*dev")

if [ ! -z "$REMAINING_FLASK" ]; then
    echo "⚡ Force kill backend Flask..."
    kill -9 $REMAINING_FLASK
fi

if [ ! -z "$REMAINING_VITE" ]; then
    echo "⚡ Force kill frontend Vite..."
    kill -9 $REMAINING_VITE
fi

echo "✅ DreamKeeper arrestato!"
echo "🧹 Pulizia porte..."

# Libera le porte se occupate
lsof -ti:5000 | xargs kill -9 2>/dev/null || true
lsof -ti:5173 | xargs kill -9 2>/dev/null || true

echo "🏁 Arresto completato!"
