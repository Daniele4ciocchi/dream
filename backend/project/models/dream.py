"""
Dream model for storing user dreams
"""
from datetime import datetime
from project import db


class Dream(db.Model):
    """Dream model for storing user dreams."""
    
    __tablename__ = 'dreams'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_dreamed = db.Column(db.Date, nullable=False)
    mood = db.Column(db.String(50))  # happy, sad, scary, weird, etc.
    is_lucid = db.Column(db.Boolean, default=False)
    tags = db.Column(db.String(500))  # comma-separated tags
    is_private = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Foreign key to user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, title, content, date_dreamed, user_id, mood=None, is_lucid=False, tags=None, is_private=True):
        """Initialize dream."""
        self.title = title
        self.content = content
        self.date_dreamed = date_dreamed
        self.user_id = user_id
        self.mood = mood
        self.is_lucid = is_lucid
        self.tags = tags
        self.is_private = is_private
    
    def save_to_db(self):
        """Save dream to database."""
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        """Delete dream from database."""
        db.session.delete(self)
        db.session.commit()
    
    def update_in_db(self):
        """Update dream in database."""
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    @staticmethod
    def find_by_id(dream_id):
        """Find dream by ID."""
        return Dream.query.get(dream_id)
    
    @staticmethod
    def find_by_user_id(user_id, limit=None):
        """Find dreams by user ID."""
        query = Dream.query.filter_by(user_id=user_id).order_by(Dream.date_dreamed.desc())
        if limit:
            query = query.limit(limit)
        return query.all()
    
    @staticmethod
    def search_user_dreams(user_id, search_term):
        """Search dreams by user ID and search term."""
        return Dream.query.filter(
            Dream.user_id == user_id,
            db.or_(
                Dream.title.contains(search_term),
                Dream.content.contains(search_term),
                Dream.tags.contains(search_term)
            )
        ).order_by(Dream.date_dreamed.desc()).all()
    
    def get_tags_list(self):
        """Get tags as a list."""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def set_tags_from_list(self, tags_list):
        """Set tags from a list."""
        if tags_list:
            self.tags = ', '.join(tags_list)
        else:
            self.tags = None
    
    def to_dict(self):
        """Convert dream to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'date_dreamed': self.date_dreamed.isoformat(),
            'mood': self.mood,
            'is_lucid': self.is_lucid,
            'tags': self.get_tags_list(),
            'is_private': self.is_private,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'user_id': self.user_id
        }
    
    def __repr__(self):
        return f'<Dream {self.title} by User {self.user_id}>'
