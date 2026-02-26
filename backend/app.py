"""
The Fitness Revolution - Flask Backend API
A comprehensive backend for the gym and fitness website
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime, timedelta
import os
import uuid

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fitness-revolution-secret-key-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///fitness_revolution.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-fitness-revolution')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

# Initialize extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ============================================
# DATABASE MODELS
# ============================================

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
    role = db.Column(db.String(20), default='member')  # member, trainer, admin
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
        user = User.query.get(self.user_id)
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': f"{user.first_name} {user.last_name}" if user else None,
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

class ContactMessage(db.Model):
    """Contact form messages"""
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'subject': self.subject,
            'message': self.message,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# ============================================
# SCHEMAS (Marshmallow)
# ============================================

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = False
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'role', 
                  'membership_id', 'is_active', 'created_at')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# ============================================
# ROOT & DOCUMENTATION ROUTES
# ============================================

@app.route('/')
def index():
    """API Root - Welcome message"""
    return jsonify({
        'message': 'Welcome to The Fitness Revolution API',
        'version': '1.0.0',
        'status': 'running',
        'documentation': '/api/docs',
        'endpoints': {
            'authentication': '/api/auth/*',
            'users': '/api/users',
            'memberships': '/api/memberships',
            'trainers': '/api/trainers',
            'programs': '/api/programs',
            'classes': '/api/classes',
            'bookings': '/api/bookings',
            'contact': '/api/contact'
        }
    })

@app.route('/api/docs')
def api_docs():
    """API Documentation"""
    return jsonify({
        'title': 'The Fitness Revolution API Documentation',
        'version': '1.0.0',
        'description': 'Complete REST API for gym and fitness management',
        'base_url': request.host_url + 'api',
        'endpoints': {
            'Authentication': {
                'POST /api/auth/register': 'Register new user',
                'POST /api/auth/login': 'Login user',
                'GET /api/auth/me': 'Get current user (requires JWT)',
                'POST /api/auth/change-password': 'Change password (requires JWT)'
            },
            'Users': {
                'GET /api/users': 'Get all users (admin only)',
                'GET /api/users/<id>': 'Get user by ID',
                'PUT /api/users/<id>': 'Update user',
                'DELETE /api/users/<id>': 'Delete user (admin only)'
            },
            'Memberships': {
                'GET /api/memberships': 'Get all memberships',
                'POST /api/memberships': 'Create membership (admin only)',
                'PUT /api/memberships/<id>': 'Update membership (admin only)'
            },
            'Trainers': {
                'GET /api/trainers': 'Get all trainers',
                'POST /api/trainers': 'Create trainer (admin only)',
                'GET /api/trainers/<id>': 'Get trainer by ID'
            },
            'Programs': {
                'GET /api/programs': 'Get all programs',
                'POST /api/programs': 'Create program (admin only)',
                'PUT /api/programs/<id>': 'Update program (admin only)'
            },
            'Classes': {
                'GET /api/classes': 'Get all classes (with filters)',
                'POST /api/classes': 'Create class (admin/trainer)'
            },
            'Bookings': {
                'GET /api/bookings': 'Get bookings (user/admin)',
                'POST /api/bookings': 'Create booking'
            }
        }
    })

# ============================================
# AUTHENTICATION ROUTES
# ============================================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validate required fields
    required = ['email', 'password', 'first_name', 'last_name']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    # Create new user
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    new_user = User(
        email=data['email'],
        password=hashed_password,
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data.get('phone'),
        date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date() if data.get('date_of_birth') else None,
        gender=data.get('gender'),
        role=data.get('role', 'member')
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    # Create access token
    access_token = create_access_token(identity=new_user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'token': access_token,
        'user': new_user.to_dict()
    }), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 403
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'Login successful',
        'token': access_token,
        'user': user.to_dict()
    }), 200


@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current logged-in user details"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user.to_dict()}), 200


@app.route('/api/auth/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    if not bcrypt.check_password_hash(user.password, old_password):
        return jsonify({'error': 'Current password is incorrect'}), 400
    
    user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    db.session.commit()
    
    return jsonify({'message': 'Password changed successfully'}), 200


# ============================================
# USER ROUTES
# ============================================

@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users (admin only)"""
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    users = User.query.all()
    return jsonify({'users': [user.to_dict() for user in users]}), 200


@app.route('/api/users/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get user by ID"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # Users can only view their own profile unless they're admin
    if current_user.role != 'admin' and current_user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user.to_dict()}), 200


@app.route('/api/users/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user profile"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if current_user.role != 'admin' and current_user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Update fields
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'phone' in data:
        user.phone = data['phone']
    if 'height' in data:
        user.height = data['height']
    if 'weight' in data:
        user.weight = data['weight']
    if 'fitness_goal' in data:
        user.fitness_goal = data['fitness_goal']
    if 'activity_level' in data:
        user.activity_level = data['activity_level']
    
    user.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'User updated successfully',
        'user': user.to_dict()
    }), 200


@app.route('/api/users/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Delete user (admin only)"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'User deactivated successfully'}), 200


# ============================================
# MEMBERSHIP ROUTES
# ============================================

@app.route('/api/memberships', methods=['GET'])
def get_memberships():
    """Get all membership plans"""
    memberships = Membership.query.filter_by(is_active=True).all()
    return jsonify({'memberships': [m.to_dict() for m in memberships]}), 200


@app.route('/api/memberships', methods=['POST'])
@jwt_required()
def create_membership():
    """Create new membership plan (admin only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    import json
    
    new_membership = Membership(
        name=data['name'],
        description=data.get('description'),
        price_monthly=data['price_monthly'],
        price_yearly=data['price_yearly'],
        duration_days=data.get('duration_days', 30),
        features=json.dumps(data.get('features', [])),
        not_included=json.dumps(data.get('not_included', [])),
        is_popular=data.get('is_popular', False)
    )
    
    db.session.add(new_membership)
    db.session.commit()
    
    return jsonify({
        'message': 'Membership created successfully',
        'membership': new_membership.to_dict()
    }), 201


@app.route('/api/memberships/<membership_id>', methods=['PUT'])
@jwt_required()
def update_membership(membership_id):
    """Update membership plan (admin only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    membership = Membership.query.get(membership_id)
    if not membership:
        return jsonify({'error': 'Membership not found'}), 404
    
    data = request.get_json()
    import json
    
    if 'name' in data:
        membership.name = data['name']
    if 'description' in data:
        membership.description = data['description']
    if 'price_monthly' in data:
        membership.price_monthly = data['price_monthly']
    if 'price_yearly' in data:
        membership.price_yearly = data['price_yearly']
    if 'features' in data:
        membership.features = json.dumps(data['features'])
    if 'not_included' in data:
        membership.not_included = json.dumps(data['not_included'])
    if 'is_popular' in data:
        membership.is_popular = data['is_popular']
    if 'is_active' in data:
        membership.is_active = data['is_active']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Membership updated successfully',
        'membership': membership.to_dict()
    }), 200


# ============================================
# TRAINER ROUTES
# ============================================

@app.route('/api/trainers', methods=['GET'])
def get_trainers():
    """Get all active trainers"""
    trainers = Trainer.query.filter_by(is_active=True).all()
    return jsonify({'trainers': [t.to_dict() for t in trainers]}), 200


@app.route('/api/trainers', methods=['POST'])
@jwt_required()
def create_trainer():
    """Create new trainer (admin only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    import json
    
    new_trainer = Trainer(
        user_id=data['user_id'],
        specialization=json.dumps(data.get('specialization', [])),
        experience_years=data.get('experience_years', 0),
        certifications=json.dumps(data.get('certifications', [])),
        bio=data.get('bio'),
        available_days=json.dumps(data.get('available_days', []))
    )
    
    db.session.add(new_trainer)
    db.session.commit()
    
    return jsonify({
        'message': 'Trainer created successfully',
        'trainer': new_trainer.to_dict()
    }), 201


@app.route('/api/trainers/<trainer_id>', methods=['GET'])
def get_trainer(trainer_id):
    """Get trainer by ID"""
    trainer = Trainer.query.get(trainer_id)
    if not trainer:
        return jsonify({'error': 'Trainer not found'}), 404
    
    return jsonify({'trainer': trainer.to_dict()}), 200


# ============================================
# PROGRAM ROUTES
# ============================================

@app.route('/api/programs', methods=['GET'])
def get_programs():
    """Get all active programs"""
    programs = Program.query.filter_by(is_active=True).all()
    return jsonify({'programs': [p.to_dict() for p in programs]}), 200


@app.route('/api/programs', methods=['POST'])
@jwt_required()
def create_program():
    """Create new program (admin only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    new_program = Program(
        title=data['title'],
        description=data.get('description'),
        category=data.get('category'),
        image_url=data.get('image_url'),
        duration_minutes=data.get('duration_minutes'),
        calories_burned=data.get('calories_burned'),
        level=data.get('level'),
        max_participants=data.get('max_participants', 20)
    )
    
    db.session.add(new_program)
    db.session.commit()
    
    return jsonify({
        'message': 'Program created successfully',
        'program': new_program.to_dict()
    }), 201


@app.route('/api/programs/<program_id>', methods=['PUT'])
@jwt_required()
def update_program(program_id):
    """Update program (admin only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    program = Program.query.get(program_id)
    if not program:
        return jsonify({'error': 'Program not found'}), 404
    
    data = request.get_json()
    
    for field in ['title', 'description', 'category', 'image_url', 
                  'duration_minutes', 'calories_burned', 'level', 
                  'max_participants', 'is_active']:
        if field in data:
            setattr(program, field, data[field])
    
    db.session.commit()
    
    return jsonify({
        'message': 'Program updated successfully',
        'program': program.to_dict()
    }), 200


# ============================================
# CLASS SCHEDULE ROUTES
# ============================================

@app.route('/api/classes', methods=['GET'])
def get_classes():
    """Get all scheduled classes"""
    from datetime import date
    
    # Filter by date if provided
    date_filter = request.args.get('date')
    trainer_filter = request.args.get('trainer_id')
    program_filter = request.args.get('program_id')
    
    query = Class.query.filter_by(is_active=True)
    
    if date_filter:
        query = query.filter(Class.date == date.fromisoformat(date_filter))
    else:
        query = query.filter(Class.date >= date.today())
    
    if trainer_filter:
        query = query.filter_by(trainer_id=trainer_filter)
    
    if program_filter:
        query = query.filter_by(program_id=program_filter)
    
    classes = query.order_by(Class.date, Class.start_time).all()
    
    return jsonify({'classes': [c.to_dict() for c in classes]}), 200


@app.route('/api/classes', methods=['POST'])
@jwt_required()
def create_class():
    """Schedule a new class (admin/trainer only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role not in ['admin', 'trainer']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    from datetime import datetime, time
    
    new_class = Class(
        program_id=data['program_id'],
        trainer_id=data['trainer_id'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        start_time=datetime.strptime(data['start_time'], '%H:%M').time(),
        end_time=datetime.strptime(data['end_time'], '%H:%M').time(),
        location=data.get('location'),
        is_virtual=data.get('is_virtual', False),
        meeting_link=data.get('meeting_link'),
        max_participants=data.get('max_participants', 20)
    )
    
    db.session.add(new_class)
    db.session.commit()
    
    return jsonify({
        'message': 'Class scheduled successfully',
        'class': new_class.to_dict()
    }), 201


# ============================================
# BOOKING ROUTES
# ============================================

@app.route('/api/bookings', methods=['GET'])
@jwt_required()
def get_bookings():
    """Get user's bookings"""
    user_id = get_jwt_identity()
    
    bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.booked_at.desc()).all()
    
    return jsonify({'bookings': [b.to_dict() for b in bookings]}), 200


@app.route('/api/bookings', methods=['POST'])
@jwt_required()
def create_booking():
    """Book a class"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    class_id = data.get('class_id')
    class_ = Class.query.get(class_id)
    
    if not class_:
        return jsonify({'error': 'Class not found'}), 404
    
    # Check if class is full
    if class_.enrolled_count >= class_.max_participants:
        return jsonify({'error': 'Class is full'}), 400
    
    # Check if user already booked
    existing = Booking.query.filter_by(user_id=user_id, class_id=class_id).first()
    if existing and existing.status == 'confirmed':
        return jsonify({'error': 'Already booked for this class'}), 400
    
    # Create booking
    new_booking = Booking(
        user_id=user_id,
        class_id=class_id,
        status='confirmed'
    )
    
    class_.enrolled_count += 1
    
    db.session.add(new_booking)
    db.session.commit()
    
    return jsonify({
        'message': 'Class booked successfully',
        'booking': new_booking.to_dict()
    }), 201


@app.route('/api/bookings/<booking_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_booking(booking_id):
    """Cancel a booking"""
    user_id = get_jwt_identity()
    
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    if booking.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if booking.status == 'cancelled':
        return jsonify({'error': 'Booking already cancelled'}), 400
    
    booking.status = 'cancelled'
    booking.cancelled_at = datetime.utcnow()
    
    if booking.class_:
        booking.class_.enrolled_count = max(0, booking.class_.enrolled_count - 1)
    
    db.session.commit()
    
    return jsonify({'message': 'Booking cancelled successfully'}), 200


# ============================================
# MEAL PLAN ROUTES
# ============================================

@app.route('/api/meal-plans', methods=['GET'])
def get_meal_plans():
    """Get all meal plans"""
    category = request.args.get('category')
    
    query = MealPlan.query.filter_by(is_active=True)
    
    if category:
        query = query.filter_by(category=category)
    
    meal_plans = query.all()
    
    return jsonify({'meal_plans': [m.to_dict() for m in meal_plans]}), 200


@app.route('/api/meal-plans/<meal_plan_id>', methods=['GET'])
def get_meal_plan(meal_plan_id):
    """Get meal plan by ID"""
    meal_plan = MealPlan.query.get(meal_plan_id)
    
    if not meal_plan:
        return jsonify({'error': 'Meal plan not found'}), 404
    
    return jsonify({'meal_plan': meal_plan.to_dict()}), 200


@app.route('/api/meal-plans', methods=['POST'])
@jwt_required()
def create_meal_plan():
    """Create new meal plan (admin/nutritionist only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role not in ['admin', 'nutritionist']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    import json
    
    new_meal_plan = MealPlan(
        title=data['title'],
        description=data.get('description'),
        category=data.get('category'),
        image_url=data.get('image_url'),
        calories=data.get('calories'),
        protein_percent=data.get('protein_percent'),
        carbs_percent=data.get('carbs_percent'),
        fat_percent=data.get('fat_percent'),
        meals=json.dumps(data.get('meals', []))
    )
    
    db.session.add(new_meal_plan)
    db.session.commit()
    
    return jsonify({
        'message': 'Meal plan created successfully',
        'meal_plan': new_meal_plan.to_dict()
    }), 201


# ============================================
# PROGRESS LOG ROUTES
# ============================================

@app.route('/api/progress', methods=['GET'])
@jwt_required()
def get_progress_logs():
    """Get user's progress logs"""
    user_id = get_jwt_identity()
    
    logs = ProgressLog.query.filter_by(user_id=user_id).order_by(ProgressLog.log_date.desc()).all()
    
    return jsonify({'progress_logs': [log.to_dict() for log in logs]}), 200


@app.route('/api/progress', methods=['POST'])
@jwt_required()
def create_progress_log():
    """Create new progress log"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Calculate BMI if height and weight provided
    bmi = None
    if data.get('height') and data.get('weight'):
        height_m = data['height'] / 100
        bmi = round(data['weight'] / (height_m ** 2), 2)
    
    new_log = ProgressLog(
        user_id=user_id,
        weight=data.get('weight'),
        height=data.get('height'),
        body_fat_percent=data.get('body_fat_percent'),
        muscle_mass=data.get('muscle_mass'),
        bmi=bmi,
        workouts_completed=data.get('workouts_completed'),
        calories_burned=data.get('calories_burned'),
        notes=data.get('notes'),
        log_date=datetime.strptime(data['log_date'], '%Y-%m-%d').date() if data.get('log_date') else datetime.utcnow().date()
    )
    
    db.session.add(new_log)
    db.session.commit()
    
    return jsonify({
        'message': 'Progress log created successfully',
        'progress_log': new_log.to_dict()
    }), 201


# ============================================
# CONTACT ROUTES
# ============================================

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """Submit contact form"""
    data = request.get_json()
    
    required = ['name', 'email', 'message']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    new_message = ContactMessage(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        subject=data.get('subject'),
        message=data['message']
    )
    
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify({'message': 'Message sent successfully'}), 201


@app.route('/api/contact', methods=['GET'])
@jwt_required()
def get_contact_messages():
    """Get all contact messages (admin only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    
    return jsonify({'messages': [m.to_dict() for m in messages]}), 200


@app.route('/api/contact/<message_id>/read', methods=['POST'])
@jwt_required()
def mark_message_read(message_id):
    """Mark contact message as read (admin only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    message = ContactMessage.query.get(message_id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    
    message.is_read = True
    db.session.commit()
    
    return jsonify({'message': 'Message marked as read'}), 200


# ============================================
# ADMIN DASHBOARD ROUTES
# ============================================

@app.route('/api/admin/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    """Get admin dashboard statistics"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Statistics
    total_users = User.query.count()
    active_members = User.query.filter_by(is_active=True).count()
    total_trainers = Trainer.query.filter_by(is_active=True).count()
    total_bookings = Booking.query.filter_by(status='confirmed').count()
    
    # Recent bookings
    recent_bookings = Booking.query.order_by(Booking.booked_at.desc()).limit(10).all()
    
    # Unread messages
    unread_messages = ContactMessage.query.filter_by(is_read=False).count()
    
    return jsonify({
        'stats': {
            'total_users': total_users,
            'active_members': active_members,
            'total_trainers': total_trainers,
            'total_bookings': total_bookings,
            'unread_messages': unread_messages
        },
        'recent_bookings': [b.to_dict() for b in recent_bookings]
    }), 200


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500


# ============================================
# INITIALIZE DATABASE
# ============================================

@app.route('/api/init-db', methods=['POST'])
def init_db():
    """Initialize database with sample data"""
    import json
    
    # Create tables
    db.create_all()
    
    # Check if data already exists
    if Membership.query.first():
        return jsonify({'message': 'Database already initialized'}), 200
    
    # Create membership plans
    memberships = [
        Membership(
            name='Basic',
            description='Essential access to gym facilities',
            price_monthly=2499,
            price_yearly=24999,
            features=json.dumps([
                'Access to gym equipment',
                'Locker room access',
                'Free WiFi',
                'Fitness assessment',
                'Mobile app access'
            ]),
            not_included=json.dumps([
                'Group classes',
                'Personal training',
                'Nutrition consultation'
            ])
        ),
        Membership(
            name='Premium',
            description='Full access with additional perks',
            price_monthly=3999,
            price_yearly=39999,
            features=json.dumps([
                'Access to gym equipment',
                'Locker room access',
                'Free WiFi',
                'Fitness assessment',
                'Mobile app access',
                'Unlimited group classes',
                '2 personal training sessions/month',
                'Towel service'
            ]),
            not_included=json.dumps([
                'Nutrition consultation',
                'Guest passes'
            ]),
            is_popular=True
        ),
        Membership(
            name='Elite',
            description='The ultimate fitness experience',
            price_monthly=5999,
            price_yearly=59999,
            features=json.dumps([
                'Access to gym equipment',
                'Locker room access',
                'Free WiFi',
                'Fitness assessment',
                'Mobile app access',
                'Unlimited group classes',
                '4 personal training sessions/month',
                'Towel service',
                'Nutrition consultation',
                '4 guest passes/month',
                'Priority class booking',
                'Recovery spa access'
            ]),
            not_included=json.dumps([])
        )
    ]
    
    for m in memberships:
        db.session.add(m)
    
    # Create programs
    programs = [
        Program(
            title='HIIT Training',
            description='High-Intensity Interval Training that burns calories and builds endurance through explosive workouts.',
            category='HIIT',
            image_url='/program-hiit.jpg',
            duration_minutes=45,
            calories_burned='500-700',
            level='advanced'
        ),
        Program(
            title='Yoga & Meditation',
            description='Find your inner peace with our expert-led yoga sessions designed for all skill levels.',
            category='Yoga',
            image_url='/program-yoga.jpg',
            duration_minutes=60,
            calories_burned='200-300',
            level='all_levels'
        ),
        Program(
            title='Strength Training',
            description='Build muscle and increase power with our comprehensive strength training programs.',
            category='Strength',
            image_url='/program-strength.jpg',
            duration_minutes=50,
            calories_burned='400-600',
            level='intermediate'
        ),
        Program(
            title='Cardio Blast',
            description='Improve your cardiovascular health with dynamic cardio workouts.',
            category='Cardio',
            image_url='/program-cardio.jpg',
            duration_minutes=40,
            calories_burned='350-500',
            level='all_levels'
        )
    ]
    
    for p in programs:
        db.session.add(p)
    
    # Create meal plans
    meal_plans = [
        MealPlan(
            title='Weight Loss Plan',
            description='A calorie-deficit meal plan designed to promote healthy weight loss with Indian cuisine options.',
            category='weight_loss',
            image_url='/meal-healthy.jpg',
            calories=1800,
            protein_percent=40,
            carbs_percent=30,
            fat_percent=30,
            meals=json.dumps([
                {'name': 'Breakfast', 'time': '8:00 AM', 'description': 'Vegetable oats upma with sprouts', 'calories': 300},
                {'name': 'Lunch', 'time': '12:30 PM', 'description': 'Roti with paneer bhurji and cucumber raita', 'calories': 450},
                {'name': 'Snack', 'time': '3:30 PM', 'description': 'Roasted chana with a small apple', 'calories': 200},
                {'name': 'Dinner', 'time': '7:00 PM', 'description': 'Grilled fish with steamed brown rice', 'calories': 550}
            ])
        ),
        MealPlan(
            title='Muscle Gain Plan',
            description='A protein-rich meal plan designed to support muscle growth and recovery.',
            category='muscle_gain',
            image_url='/meal-healthy.jpg',
            calories=3000,
            protein_percent=35,
            carbs_percent=45,
            fat_percent=20,
            meals=json.dumps([
                {'name': 'Breakfast', 'time': '7:00 AM', 'description': 'Protein oatmeal with banana and peanut butter', 'calories': 500},
                {'name': 'Mid-Morning', 'time': '10:00 AM', 'description': 'Protein shake with almonds', 'calories': 350},
                {'name': 'Lunch', 'time': '1:00 PM', 'description': 'Grilled chicken with brown rice and vegetables', 'calories': 700},
                {'name': 'Dinner', 'time': '8:00 PM', 'description': 'Salmon with quinoa and roasted veggies', 'calories': 650}
            ])
        ),
        MealPlan(
            title='Vegetarian Plan',
            description='A plant-based meal plan rich in nutrients and protein alternatives.',
            category='vegetarian',
            image_url='/meal-healthy.jpg',
            calories=2200,
            protein_percent=25,
            carbs_percent=50,
            fat_percent=25,
            meals=json.dumps([
                {'name': 'Breakfast', 'time': '8:00 AM', 'description': 'Paneer bhurji with whole grain toast', 'calories': 400},
                {'name': 'Lunch', 'time': '12:30 PM', 'description': 'Dal tadka with brown rice and salad', 'calories': 500},
                {'name': 'Snack', 'time': '3:30 PM', 'description': 'Hummus with carrot and cucumber sticks', 'calories': 250},
                {'name': 'Dinner', 'time': '7:30 PM', 'description': 'Tofu curry with quinoa', 'calories': 450}
            ])
        )
    ]
    
    for mp in meal_plans:
        db.session.add(mp)
    
    # Create admin user
    admin_user = User(
        email='admin@fitnessrevolution.in',
        password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
        first_name='Admin',
        last_name='User',
        phone='+91 80 1234 5678',
        role='admin',
        is_verified=True
    )
    db.session.add(admin_user)
    
    # Create sample trainer users
    trainer_users = [
        User(
            email='arjun@fitnessrevolution.in',
            password=bcrypt.generate_password_hash('trainer123').decode('utf-8'),
            first_name='Arjun',
            last_name='Sharma',
            phone='+91 98765 43210',
            role='trainer'
        ),
        User(
            email='priya@fitnessrevolution.in',
            password=bcrypt.generate_password_hash('trainer123').decode('utf-8'),
            first_name='Priya',
            last_name='Patel',
            phone='+91 98765 43211',
            role='trainer'
        ),
        User(
            email='rahul@fitnessrevolution.in',
            password=bcrypt.generate_password_hash('trainer123').decode('utf-8'),
            first_name='Rahul',
            last_name='Kumar',
            phone='+91 98765 43212',
            role='trainer'
        ),
        User(
            email='ananya@fitnessrevolution.in',
            password=bcrypt.generate_password_hash('trainer123').decode('utf-8'),
            first_name='Ananya',
            last_name='Reddy',
            phone='+91 98765 43213',
            role='nutritionist'
        )
    ]
    
    for tu in trainer_users:
        db.session.add(tu)
    
    db.session.commit()
    
    # Create trainer profiles
    trainers = [
        Trainer(
            user_id=trainer_users[0].id,
            specialization=json.dumps(['Strength Training', 'Powerlifting', 'Bodybuilding']),
            experience_years=10,
            certifications=json.dumps(['ACE Certified', 'NSCA-CPT']),
            bio='Expert strength coach with 10+ years of experience in powerlifting and bodybuilding.',
            available_days=json.dumps(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
        ),
        Trainer(
            user_id=trainer_users[1].id,
            specialization=json.dumps(['HIIT', 'Cardio', 'Weight Loss']),
            experience_years=8,
            certifications=json.dumps(['ACE Certified', 'CrossFit L2']),
            bio='HIIT specialist helping clients achieve their weight loss goals through high-intensity workouts.',
            available_days=json.dumps(['Monday', 'Wednesday', 'Friday', 'Saturday'])
        ),
        Trainer(
            user_id=trainer_users[2].id,
            specialization=json.dumps(['Yoga', 'Meditation', 'Mindfulness']),
            experience_years=15,
            certifications=json.dumps(['RYT-500', 'Yoga Alliance']),
            bio='Yoga master with 15 years of practice in Hatha and Vinyasa yoga.',
            available_days=json.dumps(['Tuesday', 'Thursday', 'Saturday', 'Sunday'])
        )
    ]
    
    for t in trainers:
        db.session.add(t)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Database initialized successfully with sample data',
        'data': {
            'memberships': len(memberships),
            'programs': len(programs),
            'meal_plans': len(meal_plans),
            'trainers': len(trainers),
            'admin_email': 'admin@fitnessrevolution.in',
            'admin_password': 'admin123'
        }
    }), 201


# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
