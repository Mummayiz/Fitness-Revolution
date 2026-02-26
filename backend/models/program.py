"""
Program, Class, and Booking models for The Fitness Revolution
"""

from app import db
from datetime import datetime
import uuid

class Program(db.Model):
    """Fitness programs/classes model"""
    __tablename__ = 'programs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # HIIT, Yoga, Strength, Cardio
    image_url = db.Column(db.String(255))
    
    # Details
    duration_minutes = db.Column(db.Integer)
    calories_burned = db.Column(db.String(20))
    level = db.Column(db.String(20))  # beginner, intermediate, advanced
    max_participants = db.Column(db.Integer, default=20)
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    classes = db.relationship('Class', backref='program', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'image_url': self.image_url,
            'duration_minutes': self.duration_minutes,
            'calories_burned': self.calories_burned,
            'level': self.level,
            'max_participants': self.max_participants,
            'is_active': self.is_active
        }


class Class(db.Model):
    """Scheduled classes model"""
    __tablename__ = 'classes'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    program_id = db.Column(db.String(36), db.ForeignKey('programs.id'))
    trainer_id = db.Column(db.String(36), db.ForeignKey('trainers.id'))
    
    # Schedule
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    
    # Location
    location = db.Column(db.String(100))  # room name or virtual
    is_virtual = db.Column(db.Boolean, default=False)
    meeting_link = db.Column(db.String(255))
    
    # Capacity
    max_participants = db.Column(db.Integer, default=20)
    enrolled_count = db.Column(db.Integer, default=0)
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='class_', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'program': self.program.to_dict() if self.program else None,
            'trainer': self.trainer.to_dict() if self.trainer else None,
            'date': self.date.isoformat() if self.date else None,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'location': self.location,
            'is_virtual': self.is_virtual,
            'max_participants': self.max_participants,
            'enrolled_count': self.enrolled_count,
            'available_spots': self.max_participants - self.enrolled_count,
            'is_active': self.is_active
        }


class Booking(db.Model):
    """Class booking model"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    class_id = db.Column(db.String(36), db.ForeignKey('classes.id'))
    
    status = db.Column(db.String(20), default='confirmed')  # confirmed, cancelled, attended
    booked_at = db.Column(db.DateTime, default=datetime.utcnow)
    cancelled_at = db.Column(db.DateTime)
    attended = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'class_id': self.class_id,
            'class_details': self.class_.to_dict() if self.class_ else None,
            'status': self.status,
            'booked_at': self.booked_at.isoformat() if self.booked_at else None,
            'attended': self.attended
        }
