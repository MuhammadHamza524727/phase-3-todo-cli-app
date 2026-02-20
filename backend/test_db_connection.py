#!/usr/bin/env python3
"""
Test script to verify database connection issues
"""
import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.models.user import User

load_dotenv()

async def test_database_connection():
    """Test database connection and basic operations"""
    # Get database URL from environment
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        print("❌ DATABASE_URL environment variable is not set")
        return False

    print(f"Using database URL: {DATABASE_URL}")

    # Process the database URL like in the connection file
    if DATABASE_URL.startswith("postgresql"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

        # Remove problematic parameters
        if "?" in DATABASE_URL:
            base_url, params_str = DATABASE_URL.split("?", 1)
            params = []
            for param in params_str.split("&"):
                if param and not any(x in param for x in ["sslmode=", "channel_binding=", "ssl=", "target_session_attrs="]):
                    params.append(param)

            if params:
                DATABASE_URL = f"{base_url}?{'&'.join(params)}"
            else:
                DATABASE_URL = base_url

        print(f"Processed database URL: {DATABASE_URL}")

    try:
        # Create engine
        engine = create_async_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=300,
            connect_args={
                "server_settings": {
                    "application_name": "todo-app-test",
                },
                "timeout": 10,
            }
        )

        print("✅ Engine created successfully")

        # Test connection
        async with engine.begin() as conn:
            print("✅ Database connection established")

            # Test a simple query
            result = await conn.execute(select(1))
            test_result = result.scalar()
            print(f"✅ Basic query test passed: {test_result}")

            # Try to query users table (might not exist yet)
            try:
                from sqlmodel import text
                await conn.execute(text("SELECT 1 FROM users LIMIT 1"))
                print("✅ Users table exists and is accessible")
            except Exception as e:
                print(f"⚠️ Users table might not exist yet: {str(e)}")

        return True

    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        return False
    finally:
        await engine.dispose()

if __name__ == "__main__":
    print("Testing database connection...")
    success = asyncio.run(test_database_connection())
    if success:
        print("\n✅ Database connection test PASSED")
    else:
        print("\n❌ Database connection test FAILED")