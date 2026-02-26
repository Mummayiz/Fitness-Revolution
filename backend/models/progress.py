"""
Progress Log model for The Fitness Revolution
"""

from app import db
from datetime import datetime
import uuid

class ProgressLog(db.Model):
    """User fitness progress tracking"""
    __tablename__ = 'progress_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    
    # Measurements
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    body_fat_percent = db.Column(db.Float)
    muscle_mass = db.Column(db.Float)
    bmi = db.Column(db.Float)
    
    # Workout stats
    workouts_completed = db.Column(db.Integer)
    calories_burned = db.Column(db.Integer)
    
    notes = db.Column(db.Text)
    log_date = db.Column(db.Date, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'weight': self.weight,
            'height': self.height,
            'body_fat_percent': self.body_fat_percent,
            'muscle_mass': self.muscle_mass,
            'bmi': self.bmi,
            'workouts_completed': self.workouts_completed,
            'calories_burned': self.calories_burned,
            'notes': self.notes,
            'log_date': self.log_date.isoformat() if self.log_date else None
        }
    
    def calculate_bmi(self):
        """Calculate BMI from height and weight"""
        if self.height and self.weight:
            height_m = self.height / 100
            self.bmi = round(self.weight / (height_m ** 2), 2)
        return self.bmi
