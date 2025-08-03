"""
Dreams routes for CRUD operations on user dreams - VERSIONE SEMPLICE
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from datetime import datetime, date

from project.models import Dream, User
from project.schemas import dream_schema, dreams_schema, dream_update_schema
from project.utils.security import rate_limit_check
from project import db

dreams_bp = Blueprint('dreams', __name__, url_prefix='/api/dreams')


@dreams_bp.route('', methods=['POST'])
@jwt_required()
def create_dream():
    """Create a new dream."""
    try:
        # Flask-JWT-Extended fa tutto automaticamente!
        user_id = int(get_jwt_identity())
        current_user = User.find_by_id(user_id)
        
        if not current_user:
            return jsonify({'message': 'User not found'}), 404
        
        if not rate_limit_check(current_user.id, 'create_dream', limit=20, window=3600):
            return jsonify({'message': 'Too many dreams created. Please try again later.'}), 429
        
        # Validate input
        data = dream_schema.load(request.json)
        
        # Create new dream
        dream = Dream(
            title=data['title'],
            content=data['content'],
            date_dreamed=data['date_dreamed'],
            user_id=current_user.id,
            mood=data.get('mood'),
            is_lucid=data.get('is_lucid', False),
            is_private=data.get('is_private', True)
        )
        
        # Handle tags
        if 'tags' in data and data['tags']:
            dream.set_tags_from_list(data['tags'])
        
        dream.save_to_db()
        
        return jsonify({
            'message': 'Dream created successfully',
            'dream': dream_schema.dump(dream)
        }), 201
        
    except ValidationError as e:
        return jsonify({'message': 'Validation error', 'errors': e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create dream', 'error': str(e)}), 500


@dreams_bp.route('', methods=['GET'])
@jwt_required()
def get_user_dreams():
    """Get all dreams for the current user."""
    try:
        # Flask-JWT-Extended fa tutto automaticamente!
        user_id = int(get_jwt_identity())
        current_user = User.find_by_id(user_id)
        
        if not current_user:
            return jsonify({'message': 'User not found'}), 404
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 50)  # Max 50 per page
        search = request.args.get('search', '').strip()
        
        # Build query
        query = Dream.query.filter_by(user_id=current_user.id)
        
        # Add search filter
        if search:
            query = query.filter(
                db.or_(
                    Dream.title.contains(search),
                    Dream.content.contains(search),
                    Dream.tags.contains(search)
                )
            )
        
        # Order by date dreamed (most recent first)
        query = query.order_by(Dream.date_dreamed.desc())
        
        # Paginate
        dreams_pagination = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'dreams': dreams_schema.dump(dreams_pagination.items),
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': dreams_pagination.total,
                'pages': dreams_pagination.pages,
                'has_next': dreams_pagination.has_next,
                'has_prev': dreams_pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to get dreams', 'error': str(e)}), 500


@dreams_bp.route('/<int:dream_id>', methods=['GET'])
@jwt_required()
def get_dream(dream_id):
    """Get a specific dream."""
    try:
        user_id = int(get_jwt_identity())
        current_user = User.find_by_id(user_id)
        
        if not current_user:
            return jsonify({'message': 'User not found'}), 404
        
        dream = Dream.find_by_id(dream_id)
        if not dream:
            return jsonify({'message': 'Dream not found'}), 404
        
        # Check if user owns the dream
        if dream.user_id != current_user.id:
            return jsonify({'message': 'Access denied'}), 403
        
        return jsonify({
            'dream': dream_schema.dump(dream)
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to get dream', 'error': str(e)}), 500


@dreams_bp.route('/<int:dream_id>', methods=['PUT'])
@jwt_required()
def update_dream(dream_id):
    """Update a specific dream."""
    try:
        user_id = int(get_jwt_identity())
        current_user = User.find_by_id(user_id)
        
        if not current_user:
            return jsonify({'message': 'User not found'}), 404
        
        dream = Dream.find_by_id(dream_id)
        if not dream:
            return jsonify({'message': 'Dream not found'}), 404
        
        # Check if user owns the dream
        if dream.user_id != current_user.id:
            return jsonify({'message': 'Access denied'}), 403
        
        # Rate limiting
        if not rate_limit_check(current_user.id, 'update_dream', limit=30, window=3600):
            return jsonify({'message': 'Too many updates. Please try again later.'}), 429
        
        # Validate input
        data = dream_update_schema.load(request.json)
        
        # Update dream fields
        if 'title' in data and data['title']:
            dream.title = data['title']
        if 'content' in data and data['content']:
            dream.content = data['content']
        if 'date_dreamed' in data and data['date_dreamed']:
            dream.date_dreamed = data['date_dreamed']
        if 'mood' in data:
            dream.mood = data['mood']
        if 'is_lucid' in data:
            dream.is_lucid = data['is_lucid']
        if 'is_private' in data:
            dream.is_private = data['is_private']
        if 'tags' in data:
            dream.set_tags_from_list(data['tags'])
        
        dream.update_in_db()
        
        return jsonify({
            'message': 'Dream updated successfully',
            'dream': dream_schema.dump(dream)
        }), 200
        
    except ValidationError as e:
        return jsonify({'message': 'Validation error', 'errors': e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update dream', 'error': str(e)}), 500


@dreams_bp.route('/<int:dream_id>', methods=['DELETE'])
@jwt_required()
def delete_dream(dream_id):
    """Delete a specific dream."""
    try:
        user_id = int(get_jwt_identity())
        current_user = User.find_by_id(user_id)
        
        if not current_user:
            return jsonify({'message': 'User not found'}), 404
        
        dream = Dream.find_by_id(dream_id)
        if not dream:
            return jsonify({'message': 'Dream not found'}), 404
        
        # Check if user owns the dream
        if dream.user_id != current_user.id:
            return jsonify({'message': 'Access denied'}), 403
        
        dream.delete_from_db()
        
        return jsonify({
            'message': 'Dream deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete dream', 'error': str(e)}), 500


@dreams_bp.route('/search', methods=['GET'])
@jwt_required()
def search_dreams():
    """Search dreams by keyword."""
    try:
        user_id = int(get_jwt_identity())
        current_user = User.find_by_id(user_id)
        
        if not current_user:
            return jsonify({'message': 'User not found'}), 404
        
        search_term = request.args.get('q', '').strip()
        if not search_term:
            return jsonify({'message': 'Search term is required'}), 400
        
        if len(search_term) < 2:
            return jsonify({'message': 'Search term must be at least 2 characters long'}), 400
        
        dreams = Dream.search_user_dreams(current_user.id, search_term)
        
        return jsonify({
            'dreams': dreams_schema.dump(dreams),
            'search_term': search_term,
            'count': len(dreams)
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Search failed', 'error': str(e)}), 500


@dreams_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_dream_stats():
    """Get statistics about user's dreams."""
    try:
        user_id = int(get_jwt_identity())
        current_user = User.find_by_id(user_id)
        
        if not current_user:
            return jsonify({'message': 'User not found'}), 404
        
        dreams = Dream.find_by_user_id(current_user.id)
        
        if not dreams:
            return jsonify({
                'total_dreams': 0,
                'lucid_dreams': 0,
                'mood_distribution': {},
                'dreams_by_month': {},
                'most_common_tags': []
            }), 200
        
        # Calculate statistics
        total_dreams = len(dreams)
        lucid_dreams = sum(1 for dream in dreams if dream.is_lucid)
        
        # Mood distribution
        mood_distribution = {}
        for dream in dreams:
            if dream.mood:
                mood_distribution[dream.mood] = mood_distribution.get(dream.mood, 0) + 1
        
        # Dreams by month
        dreams_by_month = {}
        for dream in dreams:
            month_key = dream.date_dreamed.strftime('%Y-%m')
            dreams_by_month[month_key] = dreams_by_month.get(month_key, 0) + 1
        
        # Most common tags
        tag_counts = {}
        for dream in dreams:
            if dream.tags:
                tags_list = dream.get_tags_list()
                for tag in tags_list:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        most_common_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return jsonify({
            'total_dreams': total_dreams,
            'lucid_dreams': lucid_dreams,
            'lucid_percentage': round((lucid_dreams / total_dreams) * 100, 1) if total_dreams > 0 else 0,
            'mood_distribution': mood_distribution,
            'dreams_by_month': dreams_by_month,
            'most_common_tags': most_common_tags
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to get statistics', 'error': str(e)}), 500
