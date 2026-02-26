"""
Trainer model for The Fitness Revolution
"""

from app import db
from datetime import datetime
import uuid

class Trainer(db.Model):
    """Trainer model"""
    __tablename__ = 'trainers'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    
    # Professional details
    specialization = db.Column(db.Text)  # JSON array
    experience_years = db.Column(db.Integer)
    certifications = db.Column(db.Text)  # JSON array
    bio = db.Column(db.Text)
    
    # Schedule
    available_days = db.Column(db.Text)  # JSON array
    available_hours = db.Column(db.Text)  # JSON object
    
    # Rating
    rating = db.Column(db.Float, default=5.0)
    total_reviews = db.Column(db.Integer, default=0)
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    classes = db.relationship('Class', backref='trainer', lazy=True)
    
    def to_dict(self):
        import json
        from .user import User
        
        user = User.query.get(self.user_id)
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': user.get_full_name() if user else None,
            'email': user.email if user else None,
            'profile_image': user.profile_image if user else None,
            'specialization': json.loads(self.specialization) if self.specialization else [],
            'experience_years': self.experience_years,
            'certifications': json.loads(self.certifications) if self.certifications else [],
            'bio': self.bio,
            'available_days': json.loads(self.available_days) if self.available_days else [],
            'rating': self.rating,
            'total_reviews': self.total_reviews,
            'is_active': self.is_active
        }
