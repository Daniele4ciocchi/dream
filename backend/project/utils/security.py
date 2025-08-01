"""
Security utilities for authentication and authorization
"""
from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from project.models import User


def token_required(f):
    """Decorator to require valid JWT token."""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Token is invalid or expired', 'error': str(e)}), 401
    return decorated


def get_current_user():
    """Get current authenticated user from JWT token."""
    try:
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        if not user or not user.is_active:
            return None
        return user
    except Exception:
        return None


def admin_required(f):
    """Decorator to require admin privileges (for future use)."""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user = get_current_user()
            if not current_user:
                return jsonify({'message': 'User not found'}), 404
            
            # For now, we don't have admin roles, but this is prepared for future use
            # if not current_user.is_admin:
            #     return jsonify({'message': 'Admin access required'}), 403
            
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Token is invalid or expired', 'error': str(e)}), 401
    return decorated


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
