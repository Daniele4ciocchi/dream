"""
Security utilities for authentication and authorization
"""
from functools import wraps
from flask import jsonify, request, g
import jwt
import datetime
from project.models import User

# Configurazione JWT centralizzata
JWT_SECRET_KEY = 'my_super_secret_key_2024'
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24


def create_jwt_token(user):
    """Crea un token JWT per l'utente specificato."""
    payload = {
        'sub': str(user.id),  # subject deve essere stringa
        'username': user.username,
        'email': user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.datetime.utcnow()
    }
    
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    print(f"🔍 Token JWT creato per utente {user.id} ({user.username})")
    return token


def decode_jwt_token(token):
    """Decodifica un token JWT e restituisce il payload."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, 'Token scaduto'
    except jwt.InvalidTokenError:
        return None, 'Token non valido'
    except Exception as e:
        return None, f'Errore decodifica token: {str(e)}'


def get_token_from_request():
    """Estrae il token JWT dall'header Authorization."""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, 'Token mancante nell\'header Authorization'
    
    try:
        token = auth_header.split(' ')[1]
        return token, None
    except IndexError:
        return None, 'Formato token non valido'


def authenticate_request():
    """Autentica la richiesta corrente e restituisce l'utente."""
    # Ottieni il token
    token, error = get_token_from_request()
    if error:
        return None, error
    
    # Decodifica il token
    payload, error = decode_jwt_token(token)
    if error:
        return None, error
    
    # Ottieni l'ID utente
    try:
        user_id = int(payload.get('sub'))
    except (ValueError, TypeError):
        return None, 'ID utente non valido nel token'
    
    # Trova l'utente nel database
    user = User.find_by_id(user_id)
    if not user:
        return None, 'Utente non trovato'
    
    if not user.is_active:
        return None, 'Utente disattivato'
    
    return user, None


def token_required(f):
    """Decorator per richiedere un token JWT valido."""
    @wraps(f)
    def decorated(*args, **kwargs):
        user, error = authenticate_request()
        if error:
            return jsonify({'message': error}), 401
        
        # Salva l'utente nel contesto della richiesta Flask
        g.current_user = user
        
        return f(*args, **kwargs)
    return decorated


def get_current_user():
    """Ottieni l'utente corrente dalla richiesta autenticata."""
    # Prima prova a ottenere l'utente dal contesto Flask
    user = getattr(g, 'current_user', None)
    if user:
        return user
    
    # Se non c'è nel contesto, autentica la richiesta
    user, error = authenticate_request()
    if error:
        print(f"❌ Errore autenticazione: {error}")
        return None
    
    print(f"✅ Utente autenticato: {user.username} (ID: {user.id})")
    return user


def admin_required(f):
    """Decorator per richiedere privilegi admin (per uso futuro)."""
    @wraps(f)
    def decorated(*args, **kwargs):
        user, error = authenticate_request()
        if error:
            return jsonify({'message': error}), 401
        
        # Per ora non abbiamo ruoli admin, ma è preparato per il futuro
        # if not user.is_admin:
        #     return jsonify({'message': 'Privilegi admin richiesti'}), 403
        
        g.current_user = user
        return f(*args, **kwargs)
    return decorated


def validate_password_strength(password):
    """Valida la robustezza della password."""
    if len(password) < 8:
        return False, "La password deve essere lunga almeno 8 caratteri"
    
    if not any(c.isupper() for c in password):
        return False, "La password deve contenere almeno una lettera maiuscola"
    
    if not any(c.islower() for c in password):
        return False, "La password deve contenere almeno una lettera minuscola"
    
    if not any(c.isdigit() for c in password):
        return False, "La password deve contenere almeno un numero"
    
    return True, "Password valida"


def sanitize_input(data):
    """Sanitizzazione di base dell'input per prevenire XSS e injection."""
    if isinstance(data, str):
        import re
        # Rimuovi tag HTML
        data = re.sub(r'<[^>]+>', '', data)
        # Rimuovi script tags
        data = re.sub(r'<script.*?</script>', '', data, flags=re.IGNORECASE | re.DOTALL)
        # Pattern SQL injection di base
        dangerous_patterns = [
            r'union\s+select', r'drop\s+table', r'delete\s+from',
            r'insert\s+into', r'update\s+set', r'exec\s*\(',
            r'execute\s*\(', r'sp_', r'xp_'
        ]
        for pattern in dangerous_patterns:
            data = re.sub(pattern, '', data, flags=re.IGNORECASE)
    
    return data


def validate_password_strength(password):
    """Validate password strength."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    
    return True, "Password is strong"


def sanitize_input(data):
    """Basic input sanitization to prevent XSS and injection attacks."""
    if isinstance(data, str):
        # Remove potentially dangerous characters
        import re
        # Remove HTML tags
        data = re.sub(r'<[^>]+>', '', data)
        # Remove script tags content
        data = re.sub(r'<script.*?</script>', '', data, flags=re.IGNORECASE | re.DOTALL)
        # Remove SQL injection patterns (basic)
        dangerous_patterns = [
            r'union\s+select', r'drop\s+table', r'delete\s+from',
            r'insert\s+into', r'update\s+set', r'exec\s*\(',
            r'execute\s*\(', r'sp_', r'xp_'
        ]
        for pattern in dangerous_patterns:
            data = re.sub(pattern, '', data, flags=re.IGNORECASE)
    
    return data


def rate_limit_check(user_id, action, limit=10, window=3600):
    """
    Basic rate limiting check (in-memory implementation).
    In production, use Redis or similar for distributed rate limiting.
    """
    from datetime import datetime, timedelta
    import threading
    
    # Simple in-memory storage (not suitable for production)
    if not hasattr(rate_limit_check, 'storage'):
        rate_limit_check.storage = {}
        rate_limit_check.lock = threading.Lock()
    
    with rate_limit_check.lock:
        key = f"{user_id}:{action}"
        now = datetime.utcnow()
        
        if key not in rate_limit_check.storage:
            rate_limit_check.storage[key] = []
        
        # Remove old entries
        cutoff = now - timedelta(seconds=window)
        rate_limit_check.storage[key] = [
            timestamp for timestamp in rate_limit_check.storage[key]
            if timestamp > cutoff
        ]
        
        # Check if limit exceeded
        if len(rate_limit_check.storage[key]) >= limit:
            return False
        
        # Add current request
        rate_limit_check.storage[key].append(now)
        return True
