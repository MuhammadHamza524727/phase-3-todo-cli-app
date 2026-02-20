# API Contracts: Frontend Application with Authentication

## Authentication Endpoints

### POST /api/auth/signup
**Description**: Register a new user account
- **Request Body**:
  ```json
  {
    "email": "string (required)",
    "password": "string (required, min 8 chars)"
  }
  ```
- **Response (200)**:
  ```json
  {
    "user": {
      "id": "string",
      "email": "string"
    },
    "token": "string (JWT)"
  }
  ```
- **Response (400)**:
  ```json
  {
    "error": "string"
  }
  ```

### POST /api/auth/login
**Description**: Authenticate user and return JWT
- **Request Body**:
  ```json
  {
    "email": "string (required)",
    "password": "string (required)"
  }
  ```
- **Response (200)**:
  ```json
  {
    "user": {
      "id": "string",
      "email": "string"
    },
    "token": "string (JWT)"
  }
  ```
- **Response (401)**:
  ```json
  {
    "error": "Invalid credentials"
  }
  ```

## Task Management Endpoints

### GET /api/tasks
**Description**: Retrieve authenticated user's tasks
- **Headers**: `Authorization: Bearer {token}`
- **Response (200)**:
  ```json
  {
    "tasks": [
      {
        "id": "string",
        "title": "string",
        "description": "string (optional)",
        "completed": "boolean",
        "userId": "string",
        "createdAt": "timestamp",
        "updatedAt": "timestamp"
      }
    ]
  }
  ```
- **Response (401)**: Unauthorized

### POST /api/tasks
**Description**: Create a new task for authenticated user
- **Headers**: `Authorization: Bearer {token}`
- **Request Body**:
  ```json
  {
    "title": "string (required)",
    "description": "string (optional)",
    "completed": "boolean (optional, default false)"
  }
  ```
- **Response (201)**:
  ```json
  {
    "task": {
      "id": "string",
      "title": "string",
      "description": "string (optional)",
      "completed": "boolean",
      "userId": "string",
      "createdAt": "timestamp",
      "updatedAt": "timestamp"
    }
  }
  ```

### PUT /api/tasks/{id}
**Description**: Update an existing task
- **Headers**: `Authorization: Bearer {token}`
- **Request Body**:
  ```json
  {
    "title": "string (optional)",
    "description": "string (optional)",
    "completed": "boolean (optional)"
  }
  ```
- **Response (200)**:
  ```json
  {
    "task": {
      "id": "string",
      "title": "string",
      "description": "string (optional)",
      "completed": "boolean",
      "userId": "string",
      "createdAt": "timestamp",
      "updatedAt": "timestamp"
    }
  }
  ```

### DELETE /api/tasks/{id}
**Description**: Delete a task
- **Headers**: `Authorization: Bearer {token}`
- **Response (204)**: No content
- **Response (404)**: Task not found

### PATCH /api/tasks/{id}/toggle
**Description**: Toggle task completion status
- **Headers**: `Authorization: Bearer {token}`
- **Response (200)**:
  ```json
  {
    "task": {
      "id": "string",
      "title": "string",
      "description": "string (optional)",
      "completed": "boolean",
      "userId": "string",
      "createdAt": "timestamp",
      "updatedAt": "timestamp"
    }
  }
  ```