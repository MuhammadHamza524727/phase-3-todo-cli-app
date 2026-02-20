#!/usr/bin/env python3
"""
Test script to check database table creation and registration process
"""
import asyncio
import os
from dotenv import load_dotenv
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.database.connection import engine, get_session
from src.models.user import User, UserCreate
from src.services.auth_service import create_new_user
from src.middleware.jwt_auth import create_access_token
import uuid

load_dotenv()

async def test_table_creation_and_registration():
    """Test that tables are created and registration works"""
    print("Testing database table creation and registration...")

    # First, create tables manually to simulate startup
    print("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Tables created successfully")

    # Create a test session
    async with AsyncSession(engine) as session:
        # Test creating a user
        print("Testing user creation...")

        user_data = UserCreate(
            email="test@example.com",
            name="Test User",
            password="securepassword123",
            password_confirm="securepassword123"
        )

        try:
            # Create the user
            db_user = await create_new_user(session, user_data)
            print(f"✅ User created successfully: {db_user.id}")

            # Create access token
            access_token = create_access_token(data={"sub": str(db_user.id)})
            print("✅ Access token created successfully")

            # Convert user to dict for response (this is where datetime issues might occur)
            user_dict = {
                "id": str(db_user.id),
                "email": db_user.email,
                "name": db_user.name,
                "created_at": db_user.created_at.isoformat() if db_user.created_at else None,
                "updated_at": db_user.updated_at.isoformat() if db_user.updated_at else None,
                "is_active": db_user.is_active
            }

            print(f"✅ User data serialized successfully: {user_dict}")
            return True

        except Exception as e:
            print(f"❌ Error during user creation: {str(e)}")
            import traceback
            print(f"Full traceback: {traceback.format_exc()}")
            return False

if __name__ == "__main__":
    import traceback
    success = asyncio.run(test_table_creation_and_registration())
    if success:
        print("\n✅ Registration process test PASSED")
    else:
        print("\n❌ Registration process test FAILED")