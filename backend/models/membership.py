"""
Membership model for The Fitness Revolution
"""

from app import db
from datetime import datetime
import uuid

class Membership(db.Model):
    """Membership plans model"""
    __tablename__ = 'memberships'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False)  # Basic, Premium, Elite
    description = db.Column(db.Text)
    price_monthly = db.Column(db.Float, nullable=False)
    price_yearly = db.Column(db.Float, nullable=False)
    duration_days = db.Column(db.Integer, default=30)
    
    # Features (stored as JSON string)
    features = db.Column(db.Text)
    not_included = db.Column(db.Text)
    
    is_popular = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    users = db.relationship('User', backref='membership', lazy=True)
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price_monthly': self.price_monthly,
            'price_yearly': self.price_yearly,
            'duration_days': self.duration_days,
            'features': json.loads(self.features) if self.features else [],
            'not_included': json.loads(self.not_included) if self.not_included else [],
            'is_popular': self.is_popular,
            'is_active': self.is_active
        }
