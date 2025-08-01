"""
Routes initialization
"""
from .auth import auth_bp
from .dreams import dreams_bp

__all__ = ['auth_bp', 'dreams_bp']
