#!/usr/bin/env python3
"""
Test script to simulate the registration process locally
"""
import asyncio
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.database.connection import engine, get_session
from src.api.auth import UserCreate
from src.services.auth_service import create_new_user
from src.middleware.jwt_auth import create_access_token

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown events"""
    print("Starting up...")

    # Initialize the database tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    print("Database tables created successfully")

    yield

    # Cleanup
    await engine.dispose()
    print("Engine disposed")

# Create test app with lifespan
app = FastAPI(lifespan=lifespan)

@app.post("/test-register")
async def test_register(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    """Test registration endpoint"""
    try:
        print(f"Registration attempt for email: {user_data.email}")

        # Check if passwords match
        if user_data.password != user_data.password_confirm:
            return {"error": "Passwords do not match"}

        # Use the authentication service to create the user
        db_user = await create_new_user(session, user_data)
        print(f"User created successfully: {db_user.id}")

        # Create access token
        access_token = create_access_token(data={"sub": str(db_user.id)})

        # Convert user to dict for response
        user_dict = {
            "id": str(db_user.id),
            "email": db_user.email,
            "name": db_user.name,
            "created_at": db_user.created_at.isoformat() if db_user.created_at else None,
            "updated_at": db_user.updated_at.isoformat() if db_user.updated_at else None,
            "is_active": db_user.is_active
        }

        return {"user": user_dict, "token": access_token}

    except Exception as e:
        print(f"Registration error: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return {"error": str(e)}

async def run_test():
    """Run the registration test"""
    print("Testing registration process...")

    # Create user data
    user_data = UserCreate(
        email="test@example.com",
        name="Test User",
        password="securepassword123",
        password_confirm="securepassword123"
    )

    # Simulate the registration process
    async with app.router.lifespan_context(app):
        try:
            # This simulates what happens in the actual registration endpoint
            result = await test_register(user_data, next(await app.dependency_overrides.get(get_session, get_session)()))
            print(f"Registration result: {result}")
        except Exception as e:
            print(f"Error during registration: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_test())