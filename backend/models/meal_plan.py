"""
Meal Plan model for The Fitness Revolution
"""

from app import db
from datetime import datetime
import uuid

class MealPlan(db.Model):
    """Nutrition meal plans model"""
    __tablename__ = 'meal_plans'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # weight_loss, muscle_gain, vegetarian, maintenance
    image_url = db.Column(db.String(255))
    
    # Nutrition info
    calories = db.Column(db.Integer)
    protein_percent = db.Column(db.Integer)
    carbs_percent = db.Column(db.Integer)
    fat_percent = db.Column(db.Integer)
    
    # Meals (JSON)
    meals = db.Column(db.Text)
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'image_url': self.image_url,
            'calories': self.calories,
            'protein': self.protein_percent,
            'carbs': self.carbs_percent,
            'fat': self.fat_percent,
            'meals': json.loads(self.meals) if self.meals else [],
            'is_active': self.is_active
        }
