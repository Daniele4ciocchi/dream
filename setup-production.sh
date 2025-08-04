#!/bin/bash

# Script di deployment per produzione

echo "🌐 Setup DreamKeeper per produzione..."

# Verifica requisiti
command -v docker >/dev/null 2>&1 || { echo "❌ Docker richiesto ma non installato."; exit 1; }

# Crea file docker-compose per produzione
cat > docker-compose.prod.yml << 'EOF'
version: '3.8'

services:
  # Database PostgreSQL per produzione
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: dreamkeeper
      POSTGRES_USER: dreamkeeper
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - dream_network
    restart: unless-stopped

  # Backend Flask
  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile.prod
    environment:
      FLASK_ENV: production
      DATABASE_URL: postgresql://dreamkeeper:${DB_PASSWORD}@db:5432/dreamkeeper
      SECRET_KEY: ${SECRET_KEY}
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
      CORS_ORIGINS: ${FRONTEND_URL}
    depends_on:
      - db
    networks:
      - dream_network
    restart: unless-stopped

  # Frontend Vue.js
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
      args:
        VITE_API_URL: ${BACKEND_URL}
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - backend
    networks:
      - dream_network
    restart: unless-stopped
    volumes:
      - ./ssl:/etc/ssl/certs
      - ./nginx.conf:/etc/nginx/nginx.conf

  # Reverse Proxy Nginx
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.prod.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl/certs
    depends_on:
      - backend
      - frontend
    networks:
      - dream_network
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  dream_network:
    driver: bridge
EOF

# Crea configurazione Nginx per produzione
cat > nginx.prod.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:5000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        
        # Redirect HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        # SSL Configuration
        ssl_certificate /etc/ssl/certs/fullchain.pem;
        ssl_certificate_key /etc/ssl/certs/privkey.pem;
        ssl_session_timeout 1d;
        ssl_session_cache shared:SSL:50m;
        ssl_session_tickets off;

        # Security headers
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header X-Frame-Options DENY always;
        add_header X-Content-Type-Options nosniff always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;
        add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self';" always;

        # API routes
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Login rate limiting
        location /api/auth/login {
            limit_req zone=login burst=5 nodelay;
            
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Frontend
        location / {
            proxy_pass http://frontend:80;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
EOF

# Crea Dockerfile per produzione backend
mkdir -p backend
cat > backend/Dockerfile.prod << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 dreamkeeper && chown -R dreamkeeper:dreamkeeper /app
USER dreamkeeper

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "run:app"]
EOF

# Crea Dockerfile per produzione frontend
mkdir -p frontend
cat > frontend/Dockerfile.prod << 'EOF'
# Build stage
FROM node:18-alpine as build-stage

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY . .

# Build for production
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# Production stage
FROM nginx:alpine as production-stage

# Copy built files
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
EOF

echo "📁 File di configurazione creati!"
echo ""
echo "🔧 PROSSIMI PASSI PER PRODUZIONE:"
echo "1. Ottieni un dominio (es: yourdomain.com)"
echo "2. Configura DNS per puntare al tuo server"
echo "3. Ottieni certificati SSL (Let's Encrypt)"
echo "4. Crea file .env.prod con le tue configurazioni"
echo "5. Esegui: docker-compose -f docker-compose.prod.yml up -d"
echo ""
echo "📋 ALTERNATIVE FACILI:"
echo "• Netlify + Heroku (gratuito per piccoli progetti)"
echo "• Vercel + PlanetScale"
echo "• Railway.app (tutto in uno)"
echo "• DigitalOcean App Platform"
