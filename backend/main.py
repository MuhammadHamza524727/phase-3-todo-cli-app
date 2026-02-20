from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.database.connection import engine
from src.api.tasks import router as tasks_router
from src.api.auth import router as auth_router
from src.middleware.jwt_auth import get_current_user
from src.models.user import User
from typing import AsyncGenerator
import os

import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for startup and shutdown events
    """
    logger.info("Starting up...")

    # Initialize the database tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield

    # Cleanup
    await engine.dispose()
    logger.info("Shutting down...")


app = FastAPI(
    title="Todo API",
    description="API for the Todo Backend Service",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
allowed_origins = [frontend_url]

# Add wildcard for development and Hugging Face spaces
if os.getenv("SPACE_ID"):  # Running on Hugging Face
    allowed_origins.append("*")
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if "*" not in allowed_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks_router, prefix="/api", tags=["tasks"])
app.include_router(auth_router, prefix="/api", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo Backend API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/protected-test")
async def protected_test(current_user: User = Depends(get_current_user)):
    """
    Test endpoint to verify JWT authentication is working
    """
    return {
        "message": "This is a protected endpoint",
        "user_id": current_user.id,
        "user_email": current_user.email
    }