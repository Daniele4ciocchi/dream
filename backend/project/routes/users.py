"""
Users routes for CRUD operations on user accounts - VERSIONE SEMPLICE
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from datetime import datetime, date

from project.models import Dream, User
from project.schemas import dream_schema, dreams_schema, dream_update_schema
from project.utils.security import rate_limit_check
from project import db

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/find', methods=['GET'])
@jwt_required()
def find_users():
    """Find users by username with real-time search"""
    try:
        # Parametri di ricerca
        query = request.args.get('q', '').strip()
        limit = min(int(request.args.get('limit', 10)), 50)  # Massimo 50 risultati
        
        current_user_id = get_jwt_identity()
        
        if not query:
            return jsonify({'users': [], 'total': 0}), 200
        
        if len(query) < 2:
            return jsonify({'users': [], 'total': 0, 'message': 'Minimum 2 characters required'}), 200
        
        # Query di ricerca con esclusione dell'utente corrente
        users_query = User.query.filter(
            User.id != current_user_id,  # Escludi te stesso
            User.username.ilike(f'%{query}%')  # Case-insensitive search
        ).limit(limit)
        
        users = users_query.all()
        
        # Converti in formato JSON
        users_data = []
        for user in users:
            users_data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email if hasattr(user, 'email') else None,
                'created_at': user.created_at.isoformat() if hasattr(user, 'created_at') else None
            })
        
        return jsonify({
            'users': users_data,
            'total': len(users_data),
            'query': query
        }), 200
    
    except Exception as e:
        print(f"🚨 Error finding users: {str(e)}")
        return jsonify({'error': 'Internal server error', 'users': [], 'total': 0}), 500

