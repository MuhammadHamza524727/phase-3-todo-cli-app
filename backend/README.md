# Backend API Service

A stateless FastAPI backend service with JWT-based authentication and Neon PostgreSQL data persistence. The backend provides secure CRUD operations for todo tasks with strict user-level data ownership enforcement.

## Features

- JWT-based authentication with token validation
- Secure task management with user data isolation
- RESTful API with proper error handling
- Neon Serverless PostgreSQL database integration

## Tech Stack

- **Backend**: Python 3.11 with FastAPI
- **Database**: Neon Serverless PostgreSQL with SQLModel ORM
- **Authentication**: JWT tokens with python-jose
- **Validation**: Pydantic models

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL (or Neon Serverless PostgreSQL access)

### Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Environment Configuration

Copy the `.env` file and update the values:

```bash
cp .env.example .env
```

Update the following variables:
- `DATABASE_URL` - Your PostgreSQL connection string
- `JWT_SECRET` - A strong secret key for JWT signing
- `FRONTEND_URL` - Your frontend URL
- `BACKEND_URL` - Your backend URL

## Running the Application

### Development

```bash
uvicorn main:app --reload --port 8000
```

### Production

Use Docker Compose to run the entire application:

```bash
docker-compose up -d
```

## API Endpoints

- `GET /api/tasks` - Get user's tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion
- `DELETE /api/tasks/{id}` - Delete a task

## Security Features

- JWT-based authentication with expiration
- User data isolation - users can only access their own tasks
- Input validation and sanitization
- Protection against common web vulnerabilities

## Architecture

The application follows a clean architecture with proper separation of concerns:

- **Models**: SQLModel database models
- **API**: FastAPI route handlers
- **Middleware**: JWT authentication and authorization
- **Database**: Connection and session management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.