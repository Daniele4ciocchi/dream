#!/bin/bash

# Script per configurare DDNS e port forwarding per DreamKeeper

echo "🏠 Configurazione DDNS per DreamKeeper..."
echo "⚠️  ATTENZIONE: Questo espone il tuo server su internet!"
echo ""

# Verifica prerequisiti
echo "📋 PREREQUISITI NECESSARI:"
echo "1. Router con supporto port forwarding"
echo "2. Account DDNS (No-IP, DuckDNS, Dynu, etc.)"
echo "3. Certificati SSL per HTTPS"
echo "4. Firewall configurato correttamente"
echo ""

read -p "Vuoi continuare? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Configurazione annullata"
    exit 1
fi

# Rileva IP pubblico
echo "🔍 Rilevamento IP pubblico..."
PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s ipinfo.io/ip 2>/dev/null || echo "NON_RILEVATO")
echo "🌐 Il tuo IP pubblico è: $PUBLIC_IP"

# Informazioni DDNS
echo ""
echo "🔧 CONFIGURAZIONE DDNS:"
echo ""
echo "📝 PASSI DA SEGUIRE:"
echo ""
echo "1️⃣  REGISTRA UN DOMINIO DINAMICO:"
echo "   • No-IP: https://www.noip.com (gratuito)"
echo "   • DuckDNS: https://www.duckdns.org (gratuito)"
echo "   • Dynu: https://www.dynu.com (gratuito)"
echo "   Esempio: tuonome.ddns.net"
echo ""
echo "2️⃣  CONFIGURA IL ROUTER:"
echo "   • Accedi al pannello router (di solito 192.168.1.1)"
echo "   • Vai in 'Port Forwarding' o 'Virtual Server'"
echo "   • Aggiungi regole:"
echo "     - Porta 80 (HTTP) → IP del tuo PC:80"
echo "     - Porta 443 (HTTPS) → IP del tuo PC:443"
echo "     - Porta 5000 (API) → IP del tuo PC:5000"
echo ""
echo "3️⃣  CONFIGURA DDNS SUL ROUTER:"
echo "   • Inserisci le credenziali del servizio DDNS"
echo "   • Il router aggiornerà automaticamente l'IP"
echo ""
echo "4️⃣  CONFIGURA CERTIFICATI SSL:"

# Crea script per certificati SSL
cat > setup-ssl.sh << 'EOF'
#!/bin/bash
# Setup SSL con Let's Encrypt per DreamKeeper

echo "🔒 Configurazione SSL..."

# Installa certbot se non presente
if ! command -v certbot &> /dev/null; then
    echo "📦 Installazione Certbot..."
    sudo apt update
    sudo apt install -y certbot
fi

echo "📝 Per ottenere certificati SSL:"
echo "sudo certbot certonly --standalone -d tuodominio.ddns.net"
echo ""
echo "I certificati saranno in: /etc/letsencrypt/live/tuodominio.ddns.net/"
EOF

chmod +x setup-ssl.sh

echo "   • Esegui: ./setup-ssl.sh"
echo "   • Usa un dominio reale (es: tuonome.ddns.net)"
echo ""

# Crea configurazione Nginx per DDNS
cat > nginx-ddns.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    
    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name tuodominio.ddns.net;  # SOSTITUISCI CON IL TUO DOMINIO
        return 301 https://$server_name$request_uri;
    }

    # HTTPS Server
    server {
        listen 443 ssl http2;
        server_name tuodominio.ddns.net;  # SOSTITUISCI CON IL TUO DOMINIO

        # SSL Configuration
        ssl_certificate /etc/letsencrypt/live/tuodominio.ddns.net/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/tuodominio.ddns.net/privkey.pem;
        
        # Security headers
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header X-Frame-Options DENY always;
        add_header X-Content-Type-Options nosniff always;

        # API Backend
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://localhost:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Frontend
        location / {
            proxy_pass http://localhost:5173;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
EOF

echo "5️⃣  AVVIA CON NGINX:"
echo "   • Installa nginx: sudo apt install nginx"
echo "   • Copia: sudo cp nginx-ddns.conf /etc/nginx/nginx.conf"
echo "   • Riavvia: sudo systemctl restart nginx"
echo ""

echo "⚠️  SICUREZZA IMPORTANTE:"
echo "❗ Cambia tutte le password e chiavi segrete"
echo "❗ Configura firewall: sudo ufw enable"
echo "❗ Aggiorna regolarmente il sistema"
echo "❗ Monitora i log di accesso"
echo ""

echo "✅ File creati:"
echo "   • setup-ssl.sh (per certificati SSL)"
echo "   • nginx-ddns.conf (configurazione Nginx)"
echo ""
echo "📖 Guida completa nel file DDNS-GUIDE.md"

# Crea guida dettagliata
cat > DDNS-GUIDE.md << 'EOF'
# 🌐 Guida DDNS per DreamKeeper

## ⚠️ ATTENZIONE
Esporre un server su internet comporta rischi di sicurezza. Segui attentamente tutte le procedure.

## 📋 Requisiti
- Router con port forwarding
- IP pubblico (no CGNAT)
- Dominio dinamico (DDNS)
- Certificati SSL

## 🔧 Configurazione Passo-Passo

### 1. Verifica IP Pubblico
```bash
curl ifconfig.me
```

### 2. Registra Dominio DDNS
Servizi gratuiti consigliati:
- **No-IP**: https://www.noip.com
- **DuckDNS**: https://www.duckdns.org  
- **Dynu**: https://www.dynu.com

### 3. Configura Router
Accedi al router (di solito 192.168.1.1) e aggiungi:
- Porta 80 → IP_PC:80
- Porta 443 → IP_PC:443
- Porta 5000 → IP_PC:5000

### 4. Installa Nginx
```bash
sudo apt update
sudo apt install nginx certbot
```

### 5. Ottieni Certificati SSL
```bash
sudo certbot certonly --standalone -d tuodominio.ddns.net
```

### 6. Configura Nginx
```bash
sudo cp nginx-ddns.conf /etc/nginx/nginx.conf
sudo nginx -t
sudo systemctl restart nginx
```

### 7. Avvia DreamKeeper
```bash
./start-local-network.sh
```

## 🔒 Sicurezza
1. Cambia tutte le password di default
2. Configura firewall: `sudo ufw enable`
3. Aggiorna regolarmente il sistema
4. Monitora i log

## 🔧 Troubleshooting
- **Porta chiusa**: Verifica port forwarding router
- **SSL error**: Controlla certificati e dominio
- **CORS error**: Aggiorna CORS_ORIGINS in .env
- **Connessione rifiutata**: Verifica firewall

## 📞 Alternative Consigliate
Per progetti piccoli, considera servizi cloud:
- Railway.app (più semplice)
- Heroku + Netlify (gratuito)
- Vercel + PlanetScale
EOF

echo "📖 Guida dettagliata salvata in: DDNS-GUIDE.md"
echo ""
echo "🚀 ALTERNATIVE PIÙ SEMPLICI:"
echo "   • Railway.app (consigliato per principianti)"
echo "   • Heroku + Netlify (gratuito)"
echo "   • Vercel + PlanetScale"
echo "   • DigitalOcean App Platform"
