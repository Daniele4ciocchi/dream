"""
Marshmallow schemas for serialization and validation
"""
from marshmallow import Schema, fields, validate, ValidationError, pre_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from project.models import User, Dream
from project import ma
import re


class UserRegistrationSchema(Schema):
    """Schema for user registration."""
    username = fields.Str(required=True, validate=[
        validate.Length(min=3, max=80),
        validate.Regexp(r'^[a-zA-Z0-9_]+$', error='Username can only contain letters, numbers, and underscores')
    ])
    email = fields.Email(required=True, validate=validate.Length(max=120))
    password = fields.Str(required=True, validate=[
        validate.Length(min=8, max=128),
        validate.Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', 
                       error='Password must contain at least one uppercase letter, one lowercase letter, and one digit')
    ])
    
    @pre_load
    def clean_input(self, data, **kwargs):
        """Clean and validate input data."""
        if 'username' in data:
            data['username'] = data['username'].strip().lower()
        if 'email' in data:
            data['email'] = data['email'].strip().lower()
        return data


class UserLoginSchema(Schema):
    """Schema for user login."""
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=1))
    
    @pre_load
    def clean_input(self, data, **kwargs):
        """Clean input data."""
        if 'email' in data:
            data['email'] = data['email'].strip().lower()
        return data


class UserSchema(SQLAlchemyAutoSchema):
    """Schema for user serialization."""
    class Meta:
        model = User
        exclude = ['password_hash']
        load_instance = True
    
    username = fields.Str(dump_only=True)
    email = fields.Email(dump_only=True)
    is_active = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class DreamSchema(Schema):
    """Schema for dream serialization and validation."""
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    content = fields.Str(required=True, validate=validate.Length(min=1, max=5000))
    date_dreamed = fields.Date(required=True)
    mood = fields.Str(validate=validate.Length(max=50), allow_none=True)
    is_lucid = fields.Bool(missing=False)
    tags = fields.List(fields.Str(validate=validate.Length(max=50)), allow_none=True)
    is_private = fields.Bool(missing=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)
    
    @pre_load
    def clean_input(self, data, **kwargs):
        """Clean input data."""
        if 'title' in data:
            data['title'] = data['title'].strip()
        if 'content' in data:
            data['content'] = data['content'].strip()
        if 'mood' in data and data['mood']:
            data['mood'] = data['mood'].strip().lower()
        return data


class DreamUpdateSchema(Schema):
    """Schema for dream updates (all fields optional)."""
    title = fields.Str(validate=validate.Length(min=1, max=200), allow_none=True)
    content = fields.Str(validate=validate.Length(min=1, max=5000), allow_none=True)
    date_dreamed = fields.Date(allow_none=True)
    mood = fields.Str(validate=validate.Length(max=50), allow_none=True)
    is_lucid = fields.Bool(allow_none=True)
    tags = fields.List(fields.Str(validate=validate.Length(max=50)), allow_none=True)
    is_private = fields.Bool(allow_none=True)
    
    @pre_load
    def clean_input(self, data, **kwargs):
        """Clean input data."""
        if 'title' in data and data['title']:
            data['title'] = data['title'].strip()
        if 'content' in data and data['content']:
            data['content'] = data['content'].strip()
        if 'mood' in data and data['mood']:
            data['mood'] = data['mood'].strip().lower()
        return data


# Schema instances
user_registration_schema = UserRegistrationSchema()
user_login_schema = UserLoginSchema()
user_schema = UserSchema()
dream_schema = DreamSchema()
dreams_schema = DreamSchema(many=True)
dream_update_schema = DreamUpdateSchema()
