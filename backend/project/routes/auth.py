"""
Authentication routes - VERSIONE SEMPLICE CON FLASK-JWT-EXTENDED
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from project.models import User
from project import db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login semplice."""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'message': 'Email e password richiesti'}), 400
        
        # Trova utente
        user = User.find_by_email(email)
        if not user or not user.check_password(password):
            return jsonify({'message': 'Credenziali non valide'}), 401
        
        # Crea token - usa STRINGA per l'identity
        token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Login successful',
            'access_token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 200
        
    except Exception as e:
        print(f"🚨 Errore login: {str(e)}")
        return jsonify({'message': f'Errore interno'}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    """Ottieni info utente corrente."""
    try:
        # Flask-JWT-Extended fa tutto automaticamente!
        user_id = int(get_jwt_identity())
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({'message': 'Utente non trovato'}), 404
        
        return jsonify({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        print(f"🚨 Errore get_me: {str(e)}")
        return jsonify({'message': f'Errore interno'}), 500


@auth_bp.route('/register', methods=['POST'])
def register():
    """Registrazione semplice."""
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return jsonify({'message': 'Username, email e password richiesti'}), 400
        
        # Controlla se esiste già
        if User.find_by_email(email):
            return jsonify({'message': 'Email già registrata'}), 400
        
        if User.find_by_username(username):
            return jsonify({'message': 'Username già esistente'}), 400
        
        # Crea utente
        user = User(username=username, email=email, password=password)
        user.save_to_db()
        
        # Crea token - usa STRINGA per l'identity
        token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Registrazione completata',
            'access_token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Errore interno'}), 500

@auth_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    """Get user statistics."""
    try:
        user_id = int(get_jwt_identity())
        user = User.find_by_id(user_id)
        print(f"User ID: {user_id}, User: {user}")
        
        if not user:
            return jsonify({'message': 'User not found'}), 404

        stats = user.get_stats()
        return jsonify(stats), 200
        
    except Exception as e:
        print(f"Errore nel recupero statistiche: {e}")
        return jsonify({'message': 'Errore interno del server'}), 500
