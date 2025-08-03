#!/usr/bin/env python3
"""
Dream Keeper Backend Application Entry Point
A secure Flask API for managing dream journal entries with user authentication.
"""

import os
import sys

# Add project directory to path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Load environment variables (skip dotenv for now)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  dotenv non disponibile, usando variabili di ambiente di default")
    os.environ.setdefault('FLASK_ENV', 'development')
    os.environ.setdefault('SECRET_KEY', 'dev-secret-key-change-in-production')

from project.app import create_app

# Create Flask application
app = create_app()

if __name__ == "__main__":
    # Configuration for development
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    host = '0.0.0.0'
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    print(f"🌙 Starting Dream Keeper API server...")
    print(f"🔧 Debug mode: {debug_mode}")
    print(f"🌐 Server: http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/")
    print(f"❤️  Health Check: http://{host}:{port}/api/health")
    
    app.run(
        debug=debug_mode,
        host=host,
        port=port
    )
