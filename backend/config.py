import os
from datetime import timedelta

# Carica dotenv solo se disponibile
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  dotenv non disponibile, usando variabili di ambiente di sistema")

class Config:
    """Base configuration class."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_super_secret_key_2024')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'my_super_secret_key_2024')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=86400)  # 24 ore
    
    # CORS Origins - supporta localhost e rete locale dinamicamente
    @staticmethod
    def get_cors_origins():
        """Genera dinamicamente gli origins CORS"""
        base_origins = [
            'http://localhost:5173',
            'http://localhost:3000',
            'http://127.0.0.1:5173',
            'http://127.0.0.1:3000',
        ]
        
        # Aggiungi URL da variabile d'ambiente
        env_frontend = os.getenv('FRONTEND_URL')
        if env_frontend and env_frontend not in base_origins:
            base_origins.append(env_frontend)
        
        # Aggiungi origins da CORS_ORIGINS
        env_cors = os.getenv('CORS_ORIGINS', '')
        if env_cors:
            cors_list = [origin.strip() for origin in env_cors.split(',') if origin.strip()]
            for origin in cors_list:
                if origin not in base_origins:
                    base_origins.append(origin)
        
        return base_origins

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dream_keeper.db')

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    # Security headers for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
