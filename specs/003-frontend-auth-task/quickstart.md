# Quickstart Guide: Frontend Application with Authentication

## Prerequisites
- Node.js 18+ installed
- Access to backend API endpoint
- Environment properly configured

## Setup Instructions

### 1. Environment Configuration
```bash
# Copy environment file
cp .env.local.example .env.local

# Update environment variables
NEXT_PUBLIC_API_BASE_URL="https://your-backend-api.com/api"
NEXTAUTH_URL="http://localhost:3000"
```

### 2. Install Dependencies
```bash
cd frontend
npm install
```

### 3. Run Development Server
```bash
npm run dev
```

Application will be available at http://localhost:3000

## Key Commands
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter
- `npm run test` - Run tests (when implemented)

## Feature Overview
1. **Authentication Flow**:
   - Navigate to `/signup` to create account
   - Use `/login` to access existing account
   - Auth state persists across browser sessions

2. **Task Management**:
   - Accessible from `/dashboard` route
   - Create, read, update, and delete tasks
   - Toggle task completion status

3. **Protected Routes**:
   - Unauthorized users redirected to login
   - JWT tokens automatically attached to API requests