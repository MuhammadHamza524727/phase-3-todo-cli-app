# Quickstart Guide: Backend API & Data Persistence (Spec 2)

**Feature**: Backend API & Data Persistence (Spec 2)
**Date**: 2026-01-23
**Phase**: Phase 1 - Developer Setup

## Overview

This guide provides the essential information needed to get started with developing the Backend API & Data Persistence service.

## Prerequisites

### System Requirements
- Python 3.11+
- PostgreSQL (or access to Neon Serverless PostgreSQL)
- Git

### Environment Variables
Create `.env` file in the backend directory:

**Backend (.env):**
```
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
JWT_SECRET=your-super-secret-jwt-key-here
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
```

## Setting Up the Development Environment

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up database
alembic upgrade head

# Run the backend server
uvicorn main:app --reload --port 8000
```

### 3. Database Setup
```bash
# Using Docker (recommended)
docker run --name neon-db -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15

# Or set up Neon Serverless PostgreSQL manually and update DATABASE_URL
```

## Running the Application

### Development Mode
1. Start the database
2. Start the backend: `cd backend && uvicorn main:app --reload`
3. Access the API at `http://localhost:8000`

### Production Mode
```bash
# Build and start with Docker
docker build -t backend-api .
docker run -p 8000:8000 --env-file .env backend-api
```

## Key Technologies & Architecture

### Backend (FastAPI)
- Python 3.11
- FastAPI for web framework
- SQLModel for database modeling
- python-jose for JWT handling
- Pydantic for request/response validation

### Database
- Neon Serverless PostgreSQL
- SQLModel ORM
- Connection pooling for performance

## Important Directories & Files

### Backend Structure
```
backend/
├── src/
│   ├── models/          # SQLModel database models
│   ├── api/            # API route handlers
│   ├── middleware/     # Authentication and other middleware
│   └── database/       # Database connection and utilities
├── tests/             # Unit and integration tests
├── requirements.txt   # Python dependencies
└── alembic/           # Database migrations
```

## Common Commands

### Backend
```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src

# Format code
black src tests

# Lint code
flake8 src tests

# Run database migrations
alembic upgrade head
```

## Authentication Flow

1. Frontend sends JWT token in Authorization header
2. Backend middleware extracts and validates JWT
3. User identity is extracted from JWT payload
4. All data access is scoped to authenticated user's ID
5. Cross-user access attempts are blocked

## Database Models

### Task Model
- id (UUID, Primary Key)
- title (String, Required)
- description (String, Optional)
- completed (Boolean, Default: False)
- owner_user_id (UUID, Foreign Key)
- created_at, updated_at (DateTime)
- due_date (DateTime, Optional)

## API Endpoints

### Tasks
- GET `/api/tasks` - Get user's tasks
- POST `/api/tasks` - Create new task
- GET `/api/tasks/{id}` - Get specific task
- PUT `/api/tasks/{id}` - Update task
- PATCH `/api/tasks/{id}/complete` - Toggle completion
- DELETE `/api/tasks/{id}` - Delete task

## Testing Strategy

### Backend Tests
- Unit tests for models and services
- Integration tests for API endpoints
- Contract tests for API compliance

## Security Considerations

1. JWT tokens are validated on every request
2. User data isolation is enforced at the database level
3. All inputs are validated using Pydantic models
4. SQL injection is prevented by using ORM
5. Authorization is enforced server-side using JWT-derived user ID

## Troubleshooting

### Common Issues
- **Database connection errors**: Verify DATABASE_URL and database is running
- **Authentication errors**: Check JWT_SECRET configuration
- **CORS issues**: Verify FRONTEND_URL in configuration
- **JWT validation failures**: Ensure token format and secret match

### Debugging Tips
- Enable debug logging by setting LOG_LEVEL=DEBUG
- Check API response headers for request IDs
- Use API testing tools like Postman to test endpoints directly
- Monitor server logs for error details

## Next Steps

1. Review the detailed API documentation
2. Examine the data model definitions
3. Look at existing tests for examples
4. Check the CI/CD pipeline configuration
5. Review security and deployment configurations