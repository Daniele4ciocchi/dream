"""
Authentication routes for user registration, login, and token management
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity,
    get_jwt, create_refresh_token
)
from marshmallow import ValidationError
from email_validator import validate_email, EmailNotValidError

from project.models import User
from project.schemas import user_registration_schema, user_login_schema, user_schema
from project.utils.security import rate_limit_check, get_current_user
from project import db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Blacklist for invalidated tokens (in production, use Redis)
blacklisted_tokens = set()


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        # Rate limiting
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        if not rate_limit_check(client_ip, 'register', limit=5, window=3600):
            return jsonify({'message': 'Too many registration attempts. Please try again later.'}), 429
        
        # Validate input
        data = user_registration_schema.load(request.json)
        
        # Check if user already exists
        if User.find_by_username(data['username']):
            return jsonify({'message': 'Username already exists'}), 400
        
        if User.find_by_email(data['email']):
            return jsonify({'message': 'Email already registered'}), 400
        
        # Validate email format
        try:
            validate_email(data['email'])
        except EmailNotValidError:
            return jsonify({'message': 'Invalid email format'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        
        user.save_to_db()
        
        # Create access token
        access_token = create_access_token(
            identity=user.id,
            additional_claims={'username': user.username}
        )
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user_schema.dump(user),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
        
    except ValidationError as e:
        return jsonify({'message': 'Validation error', 'errors': e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Registration failed', 'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token."""
    try:
        # Rate limiting
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        if not rate_limit_check(client_ip, 'login', limit=10, window=3600):
            return jsonify({'message': 'Too many login attempts. Please try again later.'}), 429
        
        # Validate input
        data = user_login_schema.load(request.json)
        
        # Find user
        user = User.find_by_email(data['email'])
        
        if not user:
            return jsonify({'message': 'Invalid email or password'}), 401
        
        if not user.is_active:
            return jsonify({'message': 'Account is deactivated'}), 401
        
        # Check password
        if not user.check_password(data['password']):
            return jsonify({'message': 'Invalid email or password'}), 401
        
        # Create tokens
        access_token = create_access_token(
            identity=user.id,
            additional_claims={'username': user.username}
        )
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'message': 'Login successful',
            'user': user_schema.dump(user),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
        
    except ValidationError as e:
        return jsonify({'message': 'Validation error', 'errors': e.messages}), 400
    except Exception as e:
        return jsonify({'message': 'Login failed', 'error': str(e)}), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token using refresh token."""
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({'message': 'User not found or inactive'}), 404
        
        new_token = create_access_token(
            identity=current_user_id,
            additional_claims={'username': user.username}
        )
        
        return jsonify({
            'access_token': new_token
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Token refresh failed', 'error': str(e)}), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user by blacklisting the token."""
    try:
        jti = get_jwt()['jti']  # JWT ID
        blacklisted_tokens.add(jti)
        
        return jsonify({'message': 'Successfully logged out'}), 200
        
    except Exception as e:
        return jsonify({'message': 'Logout failed', 'error': str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user_info():
    """Get current user information."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        return jsonify({
            'user': user_schema.dump(user)
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to get user info', 'error': str(e)}), 500


@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    """Change user password."""
    try:
        data = request.get_json()
        
        if not data or 'old_password' not in data or 'new_password' not in data:
            return jsonify({'message': 'Old password and new password are required'}), 400
        
        user = get_current_user()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Verify old password
        if not user.check_password(data['old_password']):
            return jsonify({'message': 'Invalid old password'}), 401
        
        # Validate new password
        from project.utils.security import validate_password_strength
        is_valid, message = validate_password_strength(data['new_password'])
        if not is_valid:
            return jsonify({'message': message}), 400
        
        # Update password
        user.set_password(data['new_password'])
        user.save_to_db()
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Password change failed', 'error': str(e)}), 500


# JWT token blacklist checker
@auth_bp.before_app_request
def check_if_token_revoked():
    """Check if token is blacklisted before processing request."""
    try:
        if request.endpoint and 'auth' in request.endpoint:
            # Only check JWT for protected routes
            if request.method != 'OPTIONS':  # Skip preflight requests
                jwt_header = request.headers.get('Authorization')
                if jwt_header and jwt_header.startswith('Bearer '):
                    from flask_jwt_extended import decode_token
                    try:
                        token = jwt_header.split(' ')[1]
                        decoded_token = decode_token(token)
                        jti = decoded_token['jti']
                        if jti in blacklisted_tokens:
                            return jsonify({'message': 'Token has been revoked'}), 401
                    except Exception:
                        pass  # Let the normal JWT handling deal with invalid tokens
    except Exception:
        pass  # Don't break the request flow
