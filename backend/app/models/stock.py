from mongoengine import Document, StringField, FloatField, IntField, DateTimeField
from datetime import datetime


class Stock(Document):
    """Stock model for MongoDB using MongoEngine"""
    symbol = StringField(required=True, max_length=10, unique=True)
    name = StringField(required=True, max_length=200)
    price = FloatField(required=True, min_value=0)
    change_percent = FloatField()
    volume = IntField(min_value=0)
    market_cap = FloatField(min_value=0)
    sector = StringField(max_length=100)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'stocks',
        'indexes': [
            'symbol',
            'sector',
            'created_at'
        ]
    }
    
    def __str__(self):
        return f"Stock(symbol={self.symbol}, name={self.name}, price={self.price})"
    
    def save(self, *args, **kwargs):
        """Override save to update updated_at timestamp"""
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)
