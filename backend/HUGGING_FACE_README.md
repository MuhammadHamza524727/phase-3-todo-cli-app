---
title: Todo Backend API
emoji: 🚀
colorFrom: purple
colorTo: yellow
sdk: docker
---

# Todo Backend API

A stateless FastAPI backend service with JWT-based authentication and Neon PostgreSQL data persistence. The backend provides secure CRUD operations for todo tasks with strict user-level data ownership enforcement.

## Features

- JWT-based authentication with token validation
- Secure task management with user data isolation
- RESTful API with proper error handling
- Neon Serverless PostgreSQL database integration

## API Endpoints

- `GET /api/tasks` - Get user's tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion
- `DELETE /api/tasks/{id}` - Delete a task
- `POST /api/register` - Register a new user
- `POST /api/login` - Login and get JWT token

## Security Features

- JWT-based authentication with expiration
- User data isolation - users can only access their own tasks
- Input validation and sanitization
- Protection against common web vulnerabilities