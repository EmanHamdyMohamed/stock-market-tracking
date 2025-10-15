from mongoengine import (
    Document,
    StringField,
    EmailField,
    DateTimeField,
    BooleanField,
    ListField
)
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(Document):
    """User model for MongoDB using MongoEngine"""
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, max_length=255)
    name = StringField(max_length=100)
    is_active = BooleanField(default=True)
    is_verified = BooleanField(default=False)
    is_admin = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    last_login = DateTimeField()

    # User preferences for stock tracking
    watchlist = ListField(StringField(max_length=10))  # List of stock symbols
    preferred_sectors = ListField(StringField(max_length=100))
    notification_settings = {
        'email_notifications': BooleanField(default=True),
        'price_alerts': BooleanField(default=True),
        'news_updates': BooleanField(default=False)
    }

    meta = {
        'collection': 'users',
        'indexes': [
            'email',
            'is_active',
            'created_at'
        ]
    }

    def set_password(self, password: str):
        """Hash and set password"""
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if provided password matches hash"""
        return check_password_hash(self.password, password)

    def to_dict(self):
        """Convert user to dictionary, excluding sensitive data"""
        return {
            'id': str(self.id),
            'email': self.email,
            'name': self.first_name,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'is_admin': self.is_admin,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'last_login': self.last_login,
            'watchlist': self.watchlist,
            'preferred_sectors': self.preferred_sectors
        }

    def __str__(self):
        return f"User(email={self.email}, name={self.name})"

    def save(self, *args, **kwargs):
        """Override save to update updated_at timestamp"""
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)
