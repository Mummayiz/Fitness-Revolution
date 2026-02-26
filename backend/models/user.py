"""
User model for The Fitness Revolution
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

# Note: db will be imported from app
from app import db

class User(db.Model):
    """User model for members, trainers, and admins"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    role = db.Column(db.String(20), default='member')  # member, trainer, admin, nutritionist
    profile_image = db.Column(db.String(255))
    
    # Fitness details
    height = db.Column(db.Float)  # in cm
    weight = db.Column(db.Float)  # in kg
    fitness_goal = db.Column(db.String(50))  # weight_loss, muscle_gain, maintenance
    activity_level = db.Column(db.String(20))  # sedentary, light, moderate, active
    
    # Membership
    membership_id = db.Column(db.String(36), db.ForeignKey('memberships.id'))
    membership_start = db.Column(db.Date)
    membership_end = db.Column(db.Date)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy=True)
    progress_logs = db.relationship('ProgressLog', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'role': self.role,
            'membership_id': self.membership_id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
