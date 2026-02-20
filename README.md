# Todo Full-Stack Web Application

A secure, full-stack todo application with JWT-based authentication and user data isolation.

## Features

- User registration and authentication with JWT tokens
- Secure todo management with user data isolation
- Responsive UI that works on desktop and mobile
- RESTful API with proper error handling
- Neon Serverless PostgreSQL database

## Tech Stack

- **Frontend**: Next.js 16+ with App Router
- **Backend**: FastAPI with Python 3.11
- **Database**: Neon Serverless PostgreSQL with SQLModel ORM
- **Authentication**: Better Auth with JWT
- **Styling**: Tailwind CSS

## Setup

### Prerequisites

- Node.js 18+
- Python 3.11+
- Docker (for database)

### Installation

1. Clone the repository
2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

### Environment Configuration

Copy the `.env` file and update the values:

```bash
cp .env.example .env
```

Update the following variables:
- `DATABASE_URL` - Your PostgreSQL connection string
- `BETTER_AUTH_SECRET` - A strong secret key for JWT signing
- `FRONTEND_URL` - Your frontend URL
- `BACKEND_URL` - Your backend URL

### Running the Application

#### Development

1. Start the database:
   ```bash
   docker-compose up db
   ```

2. Start the backend:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

3. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

#### Production

Use Docker Compose to run the entire application:

```bash
docker-compose up -d
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token

### Tasks
- `GET /v1/tasks` - Get user's tasks
- `POST /v1/tasks` - Create a new task
- `GET /v1/tasks/{id}` - Get a specific task
- `PUT /v1/tasks/{id}` - Update a task
- `PATCH /v1/tasks/{id}/complete` - Toggle task completion
- `DELETE /v1/tasks/{id}` - Delete a task

## Security Features

- JWT-based authentication with 24-hour expiration
- User data isolation - users can only access their own tasks
- Password hashing with bcrypt
- Input validation and sanitization
- Protection against common web vulnerabilities

## Architecture

The application follows a clean architecture with proper separation of concerns:

- **Frontend**: Next.js application with App Router
- **Backend**: FastAPI with SQLModel ORM
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT tokens with Better Auth integration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.