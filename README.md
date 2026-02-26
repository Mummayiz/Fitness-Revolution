# Fitness Revolution 

A comprehensive gym and fitness management system with a modern React frontend and robust Flask backend API.

## Features

### Frontend (React + Vite + TypeScript)
-  Modern UI with Tailwind CSS and shadcn/ui components
-  Fully responsive design
-  Fast development with Vite
-  TypeScript for type safety
-  Beautiful UI components from Radix UI

### Backend (Flask + SQLAlchemy)
-  JWT Authentication
-  User Management (Members, Trainers, Admins)
-  Membership Plans
-  Fitness Programs
-  Class Scheduling & Bookings
-  Progress Tracking
-  Meal Plans
-  Contact Management

## Tech Stack

### Frontend
- React 19
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui
- Radix UI
- React Hook Form
- Zod
- Recharts

### Backend
- Python 3.x
- Flask
- SQLAlchemy
- Flask-JWT-Extended
- Flask-CORS
- Flask-Bcrypt
- Marshmallow

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```
cd backend
```

2. Create and activate virtual environment:
```
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # macOS/Linux
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Create .env file:
```
cp .env.example .env
```

5. Run the server:
```
python run.py
```

The API will be available at http://localhost:5000

### Frontend Setup

1. Navigate to the app directory:
```
cd app
```

2. Install dependencies:
```
npm install
```

3. Start the development server:
```
npm run dev
```

The frontend will be available at http://localhost:5173

## API Endpoints

### Authentication
- POST /api/auth/register - Register new user
- POST /api/auth/login - Login user
- GET /api/auth/me - Get current user
- POST /api/auth/change-password - Change password

### Users
- GET /api/users - Get all users (admin)
- GET /api/users/<id> - Get user by ID
- PUT /api/users/<id> - Update user
- DELETE /api/users/<id> - Delete user (admin)

### Memberships
- GET /api/memberships - Get all memberships
- POST /api/memberships - Create membership (admin)
- PUT /api/memberships/<id> - Update membership (admin)

### Trainers
- GET /api/trainers - Get all trainers
- POST /api/trainers - Create trainer (admin)
- GET /api/trainers/<id> - Get trainer by ID

### Programs
- GET /api/programs - Get all programs
- POST /api/programs - Create program (admin)
- PUT /api/programs/<id> - Update program (admin)

### Classes
- GET /api/classes - Get all classes
- POST /api/classes - Create class (admin/trainer)

### Bookings
- GET /api/bookings - Get bookings
- POST /api/bookings - Create booking

## Project Structure

```
Fitness-Revolution/
 app/                    # Frontend React application
    public/            # Static assets
    src/
       components/    # React components
       hooks/        # Custom hooks
       lib/          # Utilities
    package.json

 backend/               # Flask API backend
    models/           # Database models
    app.py           # Main application
    config.py        # Configuration
    run.py           # Server entry point
    requirements.txt

 README.md
```

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For support, email support@fitnessrevolution.com or open an issue in the repository.
