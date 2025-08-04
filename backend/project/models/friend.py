"""
Friend model for managing friendships in the DreamKeeper application.
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from project import db
import bcrypt

class Friendship(db.Model):
    """Friend model for managing friendships."""
    
    __tablename__ = 'friendships'
    
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    addressee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, accepted, declined, blocked
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships - usa le COLONNE, non le variabili
    requester = db.relationship('User', foreign_keys=[requester_id], backref='sent_friend_requests')
    addressee = db.relationship('User', foreign_keys=[addressee_id], backref='received_friend_requests')
    
    def __init__(self, requester_id, addressee_id, status='pending'):
        """Initialize friendship."""
        self.requester_id = requester_id
        self.addressee_id = addressee_id
        self.status = status