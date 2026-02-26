#!/usr/bin/env python3
"""
Test script for The Fitness Revolution API
Run this to verify all endpoints are working
"""

import requests
import json

BASE_URL = 'http://localhost:5000'

# Test results
tests_passed = 0
tests_failed = 0

def test_endpoint(name, method, endpoint, data=None, headers=None):
    """Test an API endpoint"""
    global tests_passed, tests_failed
    
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=5)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers, timeout=5)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers, timeout=5)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=5)
        else:
            print(f"❌ {name}: Unknown method {method}")
            tests_failed += 1
            return None
        
        if response.status_code in [200, 201]:
            print(f"✅ {name} ({response.status_code})")
            tests_passed += 1
            return response.json()
        else:
            print(f"❌ {name} ({response.status_code}): {response.text[:100]}")
            tests_failed += 1
            return None
            
    except Exception as e:
        print(f"❌ {name}: {str(e)}")
        tests_failed += 1
        return None

def run_tests():
    """Run all API tests"""
    global tests_passed, tests_failed
    
    print("=" * 60)
    print("🧪 The Fitness Revolution API Tests")
    print("=" * 60)
    print()
    
    # Initialize database
    print("📦 Initializing database...")
    test_endpoint("Init Database", "POST", "/api/init-db")
    print()
    
    # Public endpoints
    print("🔓 Testing Public Endpoints...")
    print("-" * 40)
    test_endpoint("Get Memberships", "GET", "/api/memberships")
    test_endpoint("Get Programs", "GET", "/api/programs")
    test_endpoint("Get Trainers", "GET", "/api/trainers")
    test_endpoint("Get Meal Plans", "GET", "/api/meal-plans")
    test_endpoint("Get Classes", "GET", "/api/classes")
    
    # Contact form
    contact_data = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "+91 98765 43210",
        "subject": "Test Inquiry",
        "message": "This is a test message from the API test script."
    }
    test_endpoint("Submit Contact", "POST", "/api/contact", contact_data)
    print()
    
    # Authentication
    print("🔐 Testing Authentication...")
    print("-" * 40)
    
    # Register
    register_data = {
        "email": "newuser@example.com",
        "password": "password123",
        "first_name": "New",
        "last_name": "User",
        "phone": "+91 98765 43210"
    }
    register_result = test_endpoint("Register User", "POST", "/api/auth/register", register_data)
    
    # Login
    login_data = {
        "email": "admin@fitnessrevolution.in",
        "password": "admin123"
    }
    login_result = test_endpoint("Admin Login", "POST", "/api/auth/login", login_data)
    
    if login_result and 'token' in login_result:
        token = login_result['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        print()
        print("🔒 Testing Protected Endpoints...")
        print("-" * 40)
        
        # User endpoints
        test_endpoint("Get Current User", "GET", "/api/auth/me", headers=headers)
        test_endpoint("Get All Users", "GET", "/api/users", headers=headers)
        
        # Contact messages (admin)
        test_endpoint("Get Contact Messages", "GET", "/api/contact", headers=headers)
        
        # Admin dashboard
        test_endpoint("Admin Dashboard", "GET", "/api/admin/dashboard", headers=headers)
        
        # Create membership (admin)
        membership_data = {
            "name": "Test Membership",
            "description": "Test membership plan",
            "price_monthly": 999,
            "price_yearly": 9999,
            "features": ["Feature 1", "Feature 2"],
            "not_included": ["Feature 3"]
        }
        test_endpoint("Create Membership", "POST", "/api/memberships", membership_data, headers)
        
        # Create program (admin)
        program_data = {
            "title": "Test Program",
            "description": "Test fitness program",
            "category": "Test",
            "duration_minutes": 45,
            "calories_burned": "300-400",
            "level": "beginner"
        }
        test_endpoint("Create Program", "POST", "/api/programs", program_data, headers)
        
    else:
        print("⚠️  Skipping protected endpoints (login failed)")
    
    print()
    print("=" * 60)
    print(f"📊 Test Results: {tests_passed} passed, {tests_failed} failed")
    print("=" * 60)
    
    return tests_failed == 0

if __name__ == '__main__':
    import sys
    
    print("\n⚠️  Make sure the Flask server is running on http://localhost:5000\n")
    
    try:
        success = run_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 Tests interrupted by user")
        sys.exit(1)
