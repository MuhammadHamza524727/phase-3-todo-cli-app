#!/usr/bin/env python3
"""
Test script to check if the backend application starts correctly
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Test importing the main app
try:
    from main import app
    print("✓ Successfully imported main FastAPI app")
except Exception as e:
    print(f"✗ Failed to import main app: {e}")
    sys.exit(1)

# Test importing database connection
try:
    from src.database.connection import engine
    print("✓ Successfully imported database connection")
except Exception as e:
    print(f"✗ Failed to import database connection: {e}")
    sys.exit(1)

# Test importing models
try:
    from src.models.user import User
    from src.models.task import Task
    print("✓ Successfully imported models")
except Exception as e:
    print(f"✗ Failed to import models: {e}")
    sys.exit(1)

# Test importing API routes
try:
    from src.api import tasks, auth
    print("✓ Successfully imported API routes")
except Exception as e:
    print(f"✗ Failed to import API routes: {e}")
    sys.exit(1)

# Test importing services
try:
    from src.services.auth_service import authenticate_user, create_new_user
    print("✓ Successfully imported services")
except Exception as e:
    print(f"✗ Failed to import services: {e}")
    sys.exit(1)

print("\n🎉 All imports successful! The backend is properly configured.")
print("\nTo run the application, use:")
print("  cd backend && uvicorn main:app --reload --port 8000")
print("\nThe .env file has been updated to use SQLite for local development.")
print("For production, you can switch back to PostgreSQL by changing DATABASE_URL.")