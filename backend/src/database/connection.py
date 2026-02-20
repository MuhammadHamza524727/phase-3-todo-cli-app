from sqlmodel import create_engine
from sqlalchemy.pool import StaticPool
import os
from typing import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession as SQLAlchemyAsyncSession
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# For PostgreSQL, use async engine
if DATABASE_URL.startswith("postgresql"):
    # Replace postgresql:// with postgresql+asyncpg:// and remove unsupported params
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

    # Remove sslmode and channel_binding parameters as they're not supported by asyncpg
    if "sslmode=" in DATABASE_URL:
        import re
        DATABASE_URL = re.sub(r'[&\?]sslmode=[^&]*', '', DATABASE_URL)
        # Handle the case where sslmode is the first parameter after ?
        DATABASE_URL = re.sub(r'postgresql\+asyncpg://([^?]+)\?sslmode=[^&]*(&|$)', r'postgresql+asyncpg://\1\2', DATABASE_URL)
        # Clean up any double ampersands or trailing characters
        DATABASE_URL = DATABASE_URL.replace('&&', '&').rstrip('&')

    if "channel_binding=" in DATABASE_URL:
        import re
        DATABASE_URL = re.sub(r'[&\?]channel_binding=[^&]*', '', DATABASE_URL)
        # Handle the case where channel_binding is the first parameter after ?
        DATABASE_URL = re.sub(r'postgresql\+asyncpg://([^?]+)\?channel_binding=[^&]*(&|$)', r'postgresql+asyncpg://\1\2', DATABASE_URL)
        # Clean up any double ampersands or trailing characters
        DATABASE_URL = DATABASE_URL.replace('&&', '&').rstrip('&')

    # Additional cleanup for any remaining problematic parameters
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

    engine = create_async_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        # Add connection timeout and other parameters for reliability
        connect_args={
            "server_settings": {
                "application_name": "todo-app",
            },
            "timeout": 10,
        }
    )
else:
    # For SQLite (fallback) - use the async SQLite driver
    DATABASE_URL = DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")
    engine = create_async_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session