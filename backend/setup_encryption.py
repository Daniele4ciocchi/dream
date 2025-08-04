#!/usr/bin/env python3
"""
Setup script per SQLCipher - Database encryption at file level
Questa è la soluzione più semplice ed elegante per crittografare tutto il database
"""
import os
import sys
import shutil
import subprocess
from datetime import datetime


def check_sqlcipher():
    """Verifica se SQLCipher è installato."""
    try:
        result = subprocess.run(['sqlcipher', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ SQLCipher trovato: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ SQLCipher non trovato")
    return False


def install_sqlcipher():
    """Installa SQLCipher."""
    print("📦 Installazione SQLCipher...")
    
    # Detect OS
    import platform
    system = platform.system().lower()
    
    if system == "linux":
        print("🐧 Sistema Linux rilevato")
        commands = [
            ["sudo", "apt", "update"],
            ["sudo", "apt", "install", "-y", "sqlcipher", "libsqlcipher-dev"]
        ]
    elif system == "darwin":  # macOS
        print("🍎 Sistema macOS rilevato")
        commands = [
            ["brew", "install", "sqlcipher"]
        ]
    else:
        print("❌ Sistema non supportato automaticamente")
        print("Installa manualmente SQLCipher:")
        print("- Ubuntu/Debian: sudo apt install sqlcipher libsqlcipher-dev")
        print("- macOS: brew install sqlcipher")
        print("- Windows: Scarica da https://www.zetetic.net/sqlcipher/")
        return False
    
    for cmd in commands:
        try:
            print(f"Eseguo: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Errore durante installazione: {e}")
            return False
    
    return check_sqlcipher()


def create_encrypted_database():
    """Crea un nuovo database crittografato."""
    
    # Percorsi
    original_db = "instance/dream_keeper.db"
    encrypted_db = "instance/dream_keeper_encrypted.db"
    backup_db = f"instance/dream_keeper_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    
    # Password di crittografia
    encryption_password = os.getenv('DB_ENCRYPTION_KEY', 'default-secure-password-change-in-production')
    
    if os.path.exists(original_db):
        # Backup del database originale
        print(f"📋 Backup database: {backup_db}")
        shutil.copy2(original_db, backup_db)
        
        # Crittografa il database esistente
        print("🔒 Crittografando database esistente...")
        
        sqlcipher_script = f"""
.open {original_db}
ATTACH DATABASE '{encrypted_db}' AS encrypted KEY '{encryption_password}';
SELECT sqlcipher_export('encrypted');
DETACH DATABASE encrypted;
.exit
"""
        
        try:
            process = subprocess.Popen(['sqlcipher'], stdin=subprocess.PIPE, text=True)
            process.communicate(input=sqlcipher_script)
            
            if process.returncode == 0 and os.path.exists(encrypted_db):
                print("✅ Database crittografato con successo!")
                
                # Sostituisci il database originale
                shutil.move(original_db, f"{original_db}.old")
                shutil.move(encrypted_db, original_db)
                
                print("🔄 Database originale sostituito con versione crittografata")
                return True
            else:
                print("❌ Errore durante crittografia")
                return False
                
        except Exception as e:
            print(f"❌ Errore SQLCipher: {e}")
            return False
    else:
        print("⚠️  Database originale non trovato, verrà creato crittografato al primo avvio")
        return True


def update_config():
    """Aggiorna la configurazione per usare SQLCipher."""
    
    config_update = """
# Aggiungi queste righe al tuo config.py per usare SQLCipher:

# Importa pysqlcipher3 invece di sqlite3
try:
    from pysqlcipher3 import dbapi2 as sqlite
    SQLCIPHER_AVAILABLE = True
except ImportError:
    SQLCIPHER_AVAILABLE = False

# Database configuration
if SQLCIPHER_AVAILABLE:
    # SQLCipher database URL with encryption
    db_password = os.getenv('DB_ENCRYPTION_KEY', 'default-secure-password')
    SQLALCHEMY_DATABASE_URI = f"sqlite+pysqlcipher://:{db_password}@/{os.path.abspath('instance/dream_keeper.db')}"
else:
    # Fallback to regular SQLite
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dream_keeper.db')
"""
    
    print("📝 Configurazione SQLCipher:")
    print(config_update)
    
    # Aggiorna requirements
    print("📦 Aggiungendo pysqlcipher3 ai requirements...")
    with open('requirements_fixed.txt', 'r') as f:
        requirements = f.read()
    
    if 'pysqlcipher3' not in requirements:
        with open('requirements_fixed.txt', 'a') as f:
            f.write('\npysqlcipher3==1.2.0\n')
        print("✅ pysqlcipher3 aggiunto ai requirements")


def main():
    """Funzione principale."""
    print("🔒 SQLCipher Setup per DreamKeeper")
    print("=" * 50)
    
    # Verifica se SQLCipher è installato
    if not check_sqlcipher():
        if input("Vuoi installare SQLCipher automaticamente? (y/N): ").lower() == 'y':
            if not install_sqlcipher():
                print("❌ Installazione fallita")
                sys.exit(1)
        else:
            print("⚠️  Installa SQLCipher manualmente e riprova")
            sys.exit(1)
    
    # Installa pysqlcipher3
    print("📦 Installando pysqlcipher3...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pysqlcipher3==1.2.0'], check=True)
        print("✅ pysqlcipher3 installato")
    except subprocess.CalledProcessError:
        print("❌ Errore installazione pysqlcipher3")
        sys.exit(1)
    
    # Crea database crittografato
    if create_encrypted_database():
        print("✅ Database crittografato!")
    else:
        print("❌ Errore crittografia database")
        sys.exit(1)
    
    # Aggiorna configurazione
    update_config()
    
    print("\n🎉 Setup completato!")
    print("📋 Prossimi passi:")
    print("1. Aggiorna config.py con la configurazione SQLCipher mostrata sopra")
    print("2. Cambia DB_ENCRYPTION_KEY nel file .env con una password sicura")
    print("3. Riavvia l'applicazione")
    print("4. I dati saranno ora crittografati a livello di file!")


if __name__ == "__main__":
    main()
