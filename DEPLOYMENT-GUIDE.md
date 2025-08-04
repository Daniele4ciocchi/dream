# 🌐 Guida: Rendere DreamKeeper Accessibile Online

## 📋 STEP 1: RETE LOCALE (facile)

### Test rapido:
1. Esegui: `./start-local-network.sh`
2. Trova il tuo IP locale: il script te lo dirà
3. Da altri dispositivi sulla stessa WiFi, vai su: `http://TUO_IP:5173`

### Risoluzione problemi comuni:
- **Errore connessione**: Controlla firewall
  ```bash
  sudo ufw allow 5000
  sudo ufw allow 5173
  ```
- **CORS Error**: Aggiungi l'IP del dispositivo in `backend/config.py`

---

## 🌍 STEP 2: INTERNET (opzioni dal più facile al più avanzato)

### 🟢 OPZIONE 1: Railway.app (SUPER FACILE - CONSIGLIATA!)
1. Vai su https://railway.app
2. Connetti il tuo repository GitHub
3. Railway deploierà automaticamente backend e frontend
4. Avrai URL tipo: `https://dreamkeeper-production.up.railway.app`

**Pro**: Gratuito fino a $5/mese, zero configurazione
**Contro**: Limiti sul traffico gratuito

### 🟡 OPZIONE 2: Netlify + Heroku (GRATIS)
**Frontend (Netlify):**
1. Vai su https://netlify.com
2. Connetti GitHub, seleziona cartella `frontend`
3. Build command: `npm run build`
4. Publish directory: `dist`

**Backend (Heroku):**
1. Vai su https://heroku.com
2. Crea app, connetti GitHub cartella `backend`
3. Aggiungi PostgreSQL addon (gratuito)
4. Configura variabili ambiente

### 🟠 OPZIONE 3: VPS (DigitalOcean, Linode) - AVANZATA
1. Noleggia server (€5-10/mese)
2. Installa Docker
3. Usa il file `docker-compose.prod.yml` creato
4. Configura dominio e SSL

### 🔴 OPZIONE 4: Casa tua (MOLTO AVANZATA)
⚠️ **NON CONSIGLIATO** per principianti
- Port forwarding sul router
- DNS dinamico
- Certificati SSL
- Configurazione firewall
- Rischi di sicurezza

---

## 🔒 SICUREZZA IMPORTANTE

### Prima di andare online:
1. **Cambia le chiavi segrete** in `.env`:
   ```
   SECRET_KEY=super-secret-key-molto-lungo-e-casuale
   JWT_SECRET_KEY=altro-secret-key-diverso-e-lungo
   ```

2. **Usa HTTPS sempre** (i servizi sopra lo fanno automaticamente)

3. **Database encryption** per sogni sensibili:
   ```python
   # Aggiungi in models/dream.py
   from cryptography.fernet import Fernet
   ```

4. **Rate limiting** (già configurato in nginx.prod.conf)

---

## 🚀 QUICK START (RACCOMANDATO)

### Per iniziare subito con Railway:
1. Crea account su https://railway.app
2. Fork questo progetto su GitHub
3. Su Railway: "New Project" > "Deploy from GitHub"
4. Seleziona il fork del progetto
5. Railway rileverà automaticamente Flask + Vue.js
6. In 5 minuti avrai un URL pubblico!

### Configurazione Railway:
- Backend: Railway rileva automaticamente `backend/run.py`
- Frontend: Railway rileva automaticamente `frontend/package.json`
- Database: Aggiungi PostgreSQL dal dashboard
- Domini: Collega un dominio personalizzato (opzionale)

---

## 📞 SUPPORTO

Se hai problemi:
1. Controlla i log dell'applicazione
2. Verifica le variabili d'ambiente
3. Testa prima in locale con `./start-local-network.sh`
4. Railway ha ottima documentazione su railway.app/docs

**Suggerimento**: Inizia con Railway, è il più semplice e affidabile!
