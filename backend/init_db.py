"""
Initialize database migrations
"""
from flask import Flask
from flask_migrate import init, migrate, upgrade
import os
import sys

# Add project directory to path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from project.app import create_app

def init_db():
    """Initialize database and migrations."""
    app = create_app()
    
    with app.app_context():
        try:
            # Initialize migrations if not already done
            if not os.path.exists('migrations'):
                print("Initializing database migrations...")
                init()
            
            # Create migration for current models
            print("Creating migration...")
            migrate(message='Initial migration')
            
            # Apply migrations
            print("Applying migrations...")
            upgrade()
            
            print("✅ Database initialized successfully!")
            
        except Exception as e:
            print(f"❌ Error initializing database: {e}")

if __name__ == '__main__':
    init_db()
