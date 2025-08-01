# Dream Keeper Backend

Backend sicuro per l'applicazione Dream Keeper - Un diario digitale per i tuoi sogni.

## Caratteristiche Principali

### 🔐 Sistema di Autenticazione Sicuro
- **Registrazione utenti** con validazione email e password robusta
- **Login sicuro** con JWT (JSON Web Tokens)  
- **Hashing password** con bcrypt per massima sicurezza
- **Rate limiting** per prevenire attacchi di forza bruta
- **Blacklist token** per logout sicuro
- **Refresh token** per mantenere la sessione attiva

### 📝 Gestione Sogni
- **CRUD completo** per i sogni (Create, Read, Update, Delete)
- **Ricerca avanzata** nei contenuti dei sogni
- **Tag personalizzati** per categorizzare i sogni
- **Mood tracking** per monitorare lo stato emotivo
- **Sogni lucidi** - tracciamento separato
- **Privacy** - tutti i sogni sono privati di default
- **Paginazione** per grandi collezioni di sogni

### 📊 Statistiche Avanzate
- Conteggio totale sogni
- Percentuale sogni lucidi
- Distribuzione per umore
- Sogni per mese
- Tag più utilizzati

### 🛡️ Sicurezza
- **Input sanitization** per prevenire XSS
- **SQL injection prevention** tramite ORM SQLAlchemy
- **CORS configurato** per il frontend
- **Rate limiting** su tutte le operazioni sensibili
- **Validazione rigorosa** di tutti gli input

## Installazione

### 1. Requisiti
- Python 3.8+
- pip (gestore pacchetti Python)

### 2. Setup Ambiente Virtuale
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate     # Windows
```

### 3. Installazione Dipendenze
```bash
pip install -r requirements.txt
```

### 4. Configurazione Ambiente
Crea un file `.env` nella directory backend e configura le variabili:

```env
# Flask Configuration
FLASK_DEBUG=True
FLASK_PORT=5000

# Database Configuration
DATABASE_URL=sqlite:///dream_keeper.db

# JWT Configuration  
JWT_SECRET_KEY=your_super_secret_jwt_key_change_in_production
JWT_ACCESS_TOKEN_EXPIRES=3600

# CORS Configuration
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Security
SECRET_KEY=your_super_secret_key_change_in_production
```

### 5. Inizializzazione Database
```bash
python init_db.py
```

### 6. Avvio Server
```bash
python run.py
```

Il server sarà disponibile su `http://localhost:5000`

## API Endpoints

### Autenticazione

#### Registrazione
```
POST /api/auth/register
Content-Type: application/json

{
  "username": "mario_rossi",
  "email": "mario@example.com", 
  "password": "SecurePass123"
}
```

#### Login
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "mario@example.com",
  "password": "SecurePass123"
}
```

#### Informazioni Utente
```
GET /api/auth/me
Authorization: Bearer <access_token>
```

#### Refresh Token
```
POST /api/auth/refresh
Authorization: Bearer <refresh_token>
```

#### Logout
```
POST /api/auth/logout
Authorization: Bearer <access_token>
```

#### Cambio Password
```
PUT /api/auth/change-password
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "old_password": "SecurePass123",
  "new_password": "NewSecurePass456"
}
```

### Gestione Sogni

#### Creazione Sogno
```
POST /api/dreams
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Il mio sogno incredibile",
  "content": "Stanotte ho sognato di volare...",
  "date_dreamed": "2024-01-15",
  "mood": "happy",
  "is_lucid": true,
  "tags": ["volo", "avventura", "libertà"],
  "is_private": true
}
```

#### Lista Sogni
```
GET /api/dreams?page=1&per_page=10&search=volo
Authorization: Bearer <access_token>
```

#### Dettaglio Sogno
```
GET /api/dreams/{id}
Authorization: Bearer <access_token>
```

#### Aggiornamento Sogno
```
PUT /api/dreams/{id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Titolo aggiornato",
  "content": "Contenuto aggiornato..."
}
```

#### Eliminazione Sogno
```
DELETE /api/dreams/{id}
Authorization: Bearer <access_token>
```

#### Ricerca Sogni
```
GET /api/dreams/search?q=volare
Authorization: Bearer <access_token>
```

#### Statistiche
```
GET /api/dreams/stats
Authorization: Bearer <access_token>
```

### Utilità

#### Health Check
```
GET /api/health
```

#### Info API
```
GET /
```

## Struttura del Progetto

```
backend/
├── project/
│   ├── __init__.py          # Inizializzazione estensioni Flask
│   ├── app.py               # Factory applicazione Flask
│   ├── schemas.py           # Schemi Marshmallow per validazione
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # Modello utente
│   │   └── dream.py         # Modello sogno  
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py          # Route autenticazione
│   │   └── dreams.py        # Route gestione sogni
│   └── utils/
│       ├── __init__.py
│       └── security.py      # Utilità sicurezza
├── config.py                # Configurazioni ambiente
├── requirements.txt         # Dipendenze Python
├── run.py                   # Entry point applicazione
├── init_db.py              # Inizializzazione database
├── .env                     # Variabili ambiente (da creare)
└── README.md               # Questa documentazione
```

## Modelli Dati

### User
- `id`: Identificativo univoco
- `username`: Nome utente (univoco)
- `email`: Email (univoca)
- `password_hash`: Password criptata con bcrypt
- `is_active`: Flag attivazione account
- `created_at`: Data creazione
- `updated_at`: Data ultimo aggiornamento

### Dream
- `id`: Identificativo univoco
- `title`: Titolo del sogno
- `content`: Contenuto dettagliato
- `date_dreamed`: Data in cui è stato fatto il sogno
- `mood`: Umore associato (felice, triste, spaventoso, etc.)
- `is_lucid`: Flag per sogni lucidi
- `tags`: Tag separati da virgole
- `is_private`: Flag privacy
- `user_id`: Riferimento all'utente proprietario
- `created_at`: Data creazione record
- `updated_at`: Data ultimo aggiornamento

## Sicurezza

### Password
- Minimo 8 caratteri
- Almeno una lettera maiuscola
- Almeno una lettera minuscola  
- Almeno una cifra
- Hashing con bcrypt e salt

### Rate Limiting
- Registrazione: 5 tentativi/ora
- Login: 10 tentativi/ora
- Creazione sogni: 20/ora
- Aggiornamenti: 30/ora

### Token JWT
- Scadenza configurabile (default 1 ora)
- Refresh token per rinnovo sessione
- Blacklist per logout sicuro
- Claims personalizzati con username

## Produzione

Per l'ambiente di produzione:

1. **Cambiare le chiavi segrete** in `.env`
2. **Utilizzare PostgreSQL** invece di SQLite
3. **Configurare HTTPS** con certificati SSL
4. **Impostare rate limiting** con Redis
5. **Monitoraggio** con logging appropriato
6. **Backup database** automatizzati

## Testing

```bash
# Installa dipendenze test (aggiungi al requirements.txt se necessario)
pip install pytest pytest-flask

# Esegui test
pytest
```

## Contributi

Per contribuire al progetto:

1. Fork del repository
2. Crea branch feature (`git checkout -b feature/AmazingFeature`)
3. Commit modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)  
5. Apri Pull Request

## Licenza

Questo progetto è sotto licenza MIT. Vedi file `LICENSE` per dettagli.

## Supporto

Per supporto e domande:
- Crea un Issue su GitHub
- Contatta gli sviluppatori

---

**Dream Keeper** - *Custodisci i tuoi sogni in modo sicuro* 🌙✨
