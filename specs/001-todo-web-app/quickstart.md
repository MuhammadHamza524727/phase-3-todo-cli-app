# Quickstart Guide: Todo Full-Stack Web Application

**Feature**: Todo Full-Stack Web Application
**Date**: 2026-01-23
**Phase**: Phase 1 - Developer Setup

## Overview

This guide provides the essential information needed to get started with developing the Todo Full-Stack Web Application.

## Prerequisites

### System Requirements
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)
- Docker & Docker Compose (for database and services)
- Git

### Environment Variables
Create `.env` files in both frontend and backend directories:

**Backend (.env):**
```
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
BETTER_AUTH_DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
```

**Frontend (.env.local):**
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/v1
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000/auth
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

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run the frontend development server
npm run dev
```

### 4. Database Setup
```bash
# Using Docker Compose (recommended)
docker-compose up -d

# Or set up Neon Serverless PostgreSQL manually and update DATABASE_URL
```

## Running the Application

### Development Mode
1. Start the database: `docker-compose up -d`
2. Start the backend: `cd backend && uvicorn main:app --reload`
3. Start the frontend: `cd frontend && npm run dev`
4. Access the application at `http://localhost:3000`

### Production Mode
```bash
# Build frontend
cd frontend && npm run build

# Start both services with Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

## Key Technologies & Architecture

### Frontend (Next.js 16+)
- App Router for navigation
- Better Auth for authentication
- TypeScript for type safety
- Tailwind CSS for styling

### Backend (FastAPI)
- Python 3.11
- SQLModel for database modeling
- JWT middleware for authentication
- Pydantic for request/response validation

### Database
- Neon Serverless PostgreSQL
- Alembic for migrations
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

### Frontend Structure
```
frontend/
├── src/
│   ├── app/           # Next.js App Router pages
│   ├── components/    # Reusable React components
│   ├── services/      # API and authentication services
│   └── lib/          # Utility functions
├── public/           # Static assets
└── package.json      # Node.js dependencies
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

### Frontend
```bash
# Run tests
npm test

# Run tests with coverage
npm test -- --coverage

# Format code
npm run format

# Lint code
npm run lint

# Build for production
npm run build
```

## Authentication Flow

1. User registers/logins via Better Auth
2. Better Auth issues JWT token
3. Frontend stores token in browser session
4. Frontend attaches token to API requests via Authorization header
5. Backend validates JWT and extracts user ID
6. Backend enforces data isolation based on user ID

## Database Models

### User Model
- id (UUID, Primary Key)
- email (String, Unique)
- password_hash (String)
- name (String, Optional)
- created_at, updated_at (DateTime)

### Task Model
- id (UUID, Primary Key)
- title (String, Required)
- description (String, Optional)
- completed (Boolean, Default: False)
- user_id (UUID, Foreign Key)
- created_at, updated_at (DateTime)
- due_date (DateTime, Optional)

## API Endpoints

### Authentication
- POST `/auth/register` - Register new user
- POST `/auth/login` - Login existing user

### Tasks
- GET `/tasks` - Get user's tasks
- POST `/tasks` - Create new task
- GET `/tasks/{id}` - Get specific task
- PUT `/tasks/{id}` - Update task
- PATCH `/tasks/{id}/complete` - Toggle completion
- DELETE `/tasks/{id}` - Delete task

## Testing Strategy

### Backend Tests
- Unit tests for models and services
- Integration tests for API endpoints
- Contract tests for API compliance

### Frontend Tests
- Component tests for UI components
- Integration tests for API integration
- End-to-end tests for critical user flows

## Security Considerations

1. JWT tokens are validated on every request
2. User data isolation is enforced at the database level
3. All inputs are validated using Pydantic models
4. Passwords are hashed using secure algorithms
5. SQL injection is prevented by using ORM

## Troubleshooting

### Common Issues
- **Database connection errors**: Verify DATABASE_URL and database is running
- **Authentication errors**: Check BETTER_AUTH_SECRET consistency between frontend and backend
- **CORS issues**: Verify FRONTEND_URL in backend configuration
- **JWT validation failures**: Ensure JWT signing keys match

### Debugging Tips
- Enable debug logging by setting LOG_LEVEL=DEBUG
- Check API response headers for request IDs
- Use browser developer tools to inspect network requests
- Monitor server logs for error details

## Next Steps

1. Review the detailed API documentation
2. Examine the data model definitions
3. Look at existing tests for examples
4. Check the CI/CD pipeline configuration
5. Review security and deployment configurations