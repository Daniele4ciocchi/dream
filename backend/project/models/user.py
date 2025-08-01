"""
User model for authentication and user management
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from project import db
import bcrypt


class User(db.Model):
    """User model for authentication."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship with dreams
    dreams = db.relationship('Dream', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, username, email, password):
        """Initialize user with hashed password."""
        self.username = username
        self.email = email
        self.set_password(password)
    
    def set_password(self, password):
        """Hash and set password."""
        # Using bcrypt for stronger password hashing
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """Check if provided password matches hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    @staticmethod
    def find_by_username(username):
        """Find user by username."""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def find_by_email(email):
        """Find user by email."""
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID."""
        return User.query.get(user_id)
    
    def save_to_db(self):
        """Save user to database."""
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        """Delete user from database."""
        db.session.delete(self)
        db.session.commit()
    
    def to_dict(self):
        """Convert user to dictionary (without password)."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<User {self.username}>'
