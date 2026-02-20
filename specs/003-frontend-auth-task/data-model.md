# Data Model: Frontend Application with Authentication

## Entities

### User
- **Fields**:
  - id: string (unique identifier from backend)
  - email: string (user's email address)
  - createdAt: Date (account creation timestamp)
  - updatedAt: Date (last account update timestamp)
- **Relationships**:
  - Has many Tasks
- **Validation rules**:
  - Email must be valid email format
  - Email must be unique
  - All fields required for registration

### Task
- **Fields**:
  - id: string (unique identifier from backend)
  - title: string (task title/description)
  - description: string (optional detailed description)
  - completed: boolean (completion status)
  - userId: string (foreign key linking to User)
  - createdAt: Date (task creation timestamp)
  - updatedAt: Date (last task update timestamp)
- **Relationships**:
  - Belongs to User
- **Validation rules**:
  - Title is required
  - UserId must correspond to authenticated user
  - Completed defaults to false
  - All tasks belong to the authenticated user only

### Authentication Token
- **Fields**:
  - accessToken: string (JWT token for API authentication)
  - refreshToken: string (token for refreshing access token)
  - expiresAt: Date (expiration timestamp for access token)
- **Relationships**:
  - Associated with User session
- **Validation rules**:
  - Tokens must be properly formatted JWT
  - Access tokens must not be expired when making API calls
  - Refresh tokens must be securely stored

## State Transitions

### User Authentication State
- **Unauthenticated** → **Authenticating** → **Authenticated** → **Expired/Logged Out**
- Transitions triggered by login/signup/logout actions
- Protected routes redirect to login when transitioning to unauthenticated

### Task State
- **Pending** (completed: false) ↔ **Completed** (completed: true)
- Transitions triggered by toggle completion actions
- State persisted through API calls to backend

### API Request State
- **Idle** → **Loading** → **Success/Error** → **Idle**
- Loading states displayed during API operations
- Error states trigger appropriate user feedback