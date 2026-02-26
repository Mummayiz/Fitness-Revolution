# 🏋️ The Fitness Revolution - Flask Backend API

A comprehensive Flask backend API for The Fitness Revolution gym and fitness website.

## ✨ Features

- **User Authentication** - JWT-based auth with role-based access control
- **Membership Management** - Multiple membership plans with features
- **Trainer Profiles** - Trainer management with specializations
- **Program & Classes** - Fitness programs and class scheduling
- **Booking System** - Class booking and cancellation
- **Meal Plans** - Nutrition plans with macro breakdowns
- **Progress Tracking** - User fitness progress logs
- **Contact Forms** - Message management for inquiries
- **Admin Dashboard** - Statistics and management endpoints

## 🛠️ Tech Stack

- **Flask** - Web framework
- **SQLAlchemy** - ORM for database
- **Flask-JWT-Extended** - Authentication
- **Flask-Marshmallow** - Serialization
- **Flask-CORS** - Cross-origin requests
- **Flask-Bcrypt** - Password hashing

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Run the Server

```bash
python run.py
```

The API will be available at `http://localhost:5000`

### 4. Initialize Database (Optional)

To populate the database with sample data:

```bash
curl -X POST http://localhost:5000/api/init-db
```

## 📚 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login user |
| GET | `/api/auth/me` | Get current user |
| POST | `/api/auth/change-password` | Change password |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users` | Get all users (admin) |
| GET | `/api/users/<id>` | Get user by ID |
| PUT | `/api/users/<id>` | Update user |
| DELETE | `/api/users/<id>` | Deactivate user |

### Memberships
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/memberships` | Get all memberships |
| POST | `/api/memberships` | Create membership (admin) |
| PUT | `/api/memberships/<id>` | Update membership (admin) |

### Trainers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/trainers` | Get all trainers |
| GET | `/api/trainers/<id>` | Get trainer by ID |
| POST | `/api/trainers` | Create trainer (admin) |

### Programs
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/programs` | Get all programs |
| POST | `/api/programs` | Create program (admin) |
| PUT | `/api/programs/<id>` | Update program (admin) |

### Classes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/classes` | Get scheduled classes |
| POST | `/api/classes` | Schedule class (admin/trainer) |

### Bookings
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/bookings` | Get user bookings |
| POST | `/api/bookings` | Book a class |
| POST | `/api/bookings/<id>/cancel` | Cancel booking |

### Meal Plans
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/meal-plans` | Get all meal plans |
| GET | `/api/meal-plans/<id>` | Get meal plan by ID |
| POST | `/api/meal-plans` | Create meal plan (admin) |

### Progress
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/progress` | Get progress logs |
| POST | `/api/progress` | Create progress log |

### Contact
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/contact` | Submit contact form |
| GET | `/api/contact` | Get messages (admin) |
| POST | `/api/contact/<id>/read` | Mark as read (admin) |

### Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/admin/dashboard` | Dashboard stats |
| POST | `/api/init-db` | Initialize database |

## 🔐 Default Credentials

After running `/api/init-db`:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@fitnessrevolution.in | admin123 |
| Trainer | arjun@fitnessrevolution.in | trainer123 |
| Trainer | priya@fitnessrevolution.in | trainer123 |
| Trainer | rahul@fitnessrevolution.in | trainer123 |
| Nutritionist | ananya@fitnessrevolution.in | trainer123 |

## 📁 Project Structure

```
backend/
├── app.py              # Main Flask application
├── run.py              # Development server runner
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🗄️ Database Models

### User
- id, email, password, first_name, last_name
- phone, date_of_birth, gender
- role (member, trainer, admin, nutritionist)
- membership_id, fitness details
- is_active, created_at

### Membership
- id, name, description
- price_monthly, price_yearly
- features, not_included
- is_popular, is_active

### Trainer
- id, user_id, specialization
- experience_years, certifications
- available_days, rating

### Program
- id, title, description, category
- duration_minutes, calories_burned
- level, max_participants

### Class
- id, program_id, trainer_id
- date, start_time, end_time
- location, max_participants

### Booking
- id, user_id, class_id
- status, booked_at

### MealPlan
- id, title, description, category
- calories, protein, carbs, fat
- meals (JSON)

### ProgressLog
- id, user_id, weight, height
- body_fat_percent, bmi
- workouts_completed, calories_burned

### ContactMessage
- id, name, email, message
- is_read, created_at

## 🧪 Testing with cURL

### Register a User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+91 98765 43210"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@fitnessrevolution.in",
    "password": "admin123"
  }'
```

### Get Memberships
```bash
curl http://localhost:5000/api/memberships
```

### Submit Contact Form
```bash
curl -X POST http://localhost:5000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+91 98765 43210",
    "message": "I am interested in joining your gym."
  }'
```

## 🚀 Production Deployment

### Using Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Variables for Production
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secure-secret-key
export JWT_SECRET_KEY=your-secure-jwt-key
export DATABASE_URL=postgresql://user:pass@host/dbname
```

## 📄 License

This project is part of The Fitness Revolution academic project.
