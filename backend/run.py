#!/usr/bin/env python3
"""
The Fitness Revolution - Flask Backend
Run script for development server
"""

from app import app, db

if __name__ == '__main__':
    with app.app_context():
        # Create all database tables
        db.create_all()
        print("✅ Database tables created")
    
    print("🚀 Starting Fitness Revolution API Server...")
    print("📍 API URL: http://localhost:5000")
    print("📚 API Documentation: http://localhost:5000/api/docs")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )
