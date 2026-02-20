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
import asyncio
import traceback

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

    try:
        # Initialize the database tables
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Database tables created/verified successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        logger.error(traceback.format_exc())
        # Don't raise the exception during startup to allow the app to run
        # The database might be initialized later when needed
        logger.warning("Continuing startup despite database initialization error")
    finally:
        yield

    # Cleanup
    try:
        await engine.dispose()
        logger.info("Database engine disposed")
    except Exception as e:
        logger.error(f"Error disposing database engine: {str(e)}")

    logger.info("Shutting down...")

# For Hugging Face Spaces, we need to create the app instance differently
app = FastAPI(
    title="Todo API",
    description="API for the Todo Backend Service",
    version="1.0.0",
    lifespan=lifespan,
    debug=True  # Enable for better error reporting in Hugging Face
)

# Add CORS middleware - Allow all origins for Hugging Face Spaces
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Hugging Face Spaces
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
try:
    app.include_router(tasks_router, prefix="/api", tags=["tasks"])
    app.include_router(auth_router, prefix="/api", tags=["auth"])
    logger.info("Routers included successfully")
except Exception as e:
    logger.error(f"Failed to include routers: {str(e)}")
    logger.error(traceback.format_exc())

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

# For Hugging Face Spaces compatibility
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))  # Hugging Face uses port 7860
    logger.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)