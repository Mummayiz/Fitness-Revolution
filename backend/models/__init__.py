"""
Database models for The Fitness Revolution
"""

from .user import User
from .membership import Membership
from .trainer import Trainer
from .program import Program, Class, Booking
from .meal_plan import MealPlan
from .progress import ProgressLog
from .contact import ContactMessage

__all__ = [
    'User',
    'Membership', 
    'Trainer',
    'Program',
    'Class',
    'Booking',
    'MealPlan',
    'ProgressLog',
    'ContactMessage'
]
