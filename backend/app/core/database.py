from mongoengine import connect, disconnect
from app.core.config import settings


def connect_to_mongo():
    """Create database connection"""
    connect(
        db=settings.mongodb_database,
        host=settings.mongodb_url,
        alias='default'
    )
    print(f"Connected to MongoDB: {settings.mongodb_database}")


def close_mongo_connection():
    """Close database connection"""
    disconnect(alias='default')
    print("Disconnected from MongoDB")
