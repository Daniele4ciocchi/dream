# 🔒 Guida alla Sicurezza Database DreamKeeper

## Situazione Attuale
- ✅ **Password utenti**: Crittografate con bcrypt + salt (sicure)
- ✅ **JWT tokens**: Firmati e sicuri per autenticazione
- ❌ **Contenuto sogni**: Memorizzato in chiaro nel database SQLite

## Opzioni per Proteggere i Dati Utente

### 🏆 **OPZIONE 1: SQLCipher (CONSIGLIATA)**
**Crittografia completa del database a livello di file**

**Vantaggi:**
- ✅ Tutto il database è crittografato (inclusi metadati)
- ✅ Soluzione semplice e pulita
- ✅ Zero modifiche al codice esistente
- ✅ Performance eccellenti
- ✅ Standard industriale

**Come implementare:**
```bash
# 1. Esegui lo script di setup
python setup_encryption.py

# 2. Il database diventa completamente crittografato
# 3. Anche se qualcuno ruba il file .db, non può leggerlo
```

**Risultato:** Il file database diventa illeggibile senza la password.

---

### 📁 **OPZIONE 2: Crittografia File System**
**Crittografia dell'intera cartella del progetto**

**Linux (LUKS/dm-crypt):**
```bash
# Crea volume crittografato
sudo cryptsetup luksFormat /dev/sdX
sudo cryptsetup open /dev/sdX dreamkeeper
sudo mkfs.ext4 /dev/mapper/dreamkeeper

# Monta e usa
sudo mount /dev/mapper/dreamkeeper /var/dreamkeeper
```

**Vantaggi:**
- ✅ Crittografia trasparente
- ✅ Protegge tutto (codice + database)
- ✅ Zero modifiche al codice

---

### 🌐 **OPZIONE 3: Database Remoto Sicuro**
**Usa PostgreSQL/MySQL con crittografia SSL**

```python
# config.py
SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@secure-server:5432/dreamkeeper?sslmode=require'
```

**Vantaggi:**
- ✅ Crittografia in transito (SSL/TLS)
- ✅ Database professionale
- ✅ Backup automatici
- ✅ Scalabilità

---

## 🎯 **Raccomandazione**

Per la tua applicazione, **SQLCipher è la scelta migliore** perché:

1. **Semplice**: Un comando e tutto è crittografato
2. **Efficace**: File database completamente illeggibile
3. **Zero breaking changes**: Il codice rimane identico
4. **Sicuro**: Anche con accesso fisico, i dati sono protetti

## 🚀 **Implementazione Immediata**

```bash
# Nel backend
cd /home/daniele/dream/backend
python setup_encryption.py
```

**Cosa succede:**
1. Il database SQLite viene convertito in SQLCipher
2. Tutti i dati diventano crittografati
3. L'app funziona normalmente
4. Anche rubando il file .db, i dati sono illeggibili

## 🔑 **Sicurezza della Chiave**

Assicurati di:
- Cambiare `DB_ENCRYPTION_KEY` in produzione
- Non committare mai la chiave nel repository
- Usare variabili d'ambiente sicure
- Fare backup sicuri della chiave

## ⚡ **Alternativa Rapida per Test**

Se vuoi testare subito la crittografia:

```bash
# Cripta il database attuale manualmente
sqlcipher instance/dream_keeper.db
> .open --new encrypted.db
> PRAGMA key = 'tua-password-sicura';
> .dump
> .exit

# Sostituisci il database originale
mv instance/dream_keeper.db instance/dream_keeper.backup
mv encrypted.db instance/dream_keeper.db
```

**Vuoi che procediamo con SQLCipher?**
