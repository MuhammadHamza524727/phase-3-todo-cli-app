# Todo App Frontend

A secure todo application with authentication built using Next.js 16+ with App Router.

## Features

- User authentication (signup/login/logout)
- Secure JWT-based authentication
- Task management (create, read, update, delete, toggle completion)
- Responsive design (mobile-first)
- Clean, intuitive user interface
- Protected routes for authenticated users

## Tech Stack

- Next.js 16+ (App Router)
- React 18+
- TypeScript
- Tailwind CSS
- Better Auth
- Axios for API requests

## Getting Started

### Prerequisites

- Node.js 18+
- Access to the backend API (FastAPI server running)

### Installation

1. Clone the repository
2. Navigate to the frontend directory
3. Install dependencies:

```bash
cd frontend
npm install
```

### Configuration

Create a `.env.local` file in the frontend directory with the following content:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
```

Replace `http://localhost:8000/api` with your actual backend API URL.

### Running the Application

```bash
# Development mode
npm run dev

# Production build
npm run build
npm start
```

The application will be available at [http://localhost:3000](http://localhost:3000).

## Usage

1. Visit the application homepage
2. Click "Sign Up" to create an account
3. Log in with your credentials
4. Navigate to the dashboard to manage your tasks
5. Create, edit, delete, or toggle completion of your tasks

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL`: Base URL for the backend API (e.g., http://localhost:8000/api)

## Project Structure

```
frontend/
├── app/                 # Next.js App Router pages
│   ├── login/           # Login page
│   ├── signup/          # Signup page
│   ├── dashboard/       # Task dashboard
│   └── layout.tsx       # Global layout with auth provider
├── components/          # Reusable UI components
│   ├── auth/            # Authentication components
│   ├── tasks/           # Task management components
│   └── ui/              # General UI components
├── services/            # API service functions
├── lib/                 # Utilities and context
├── types/               # TypeScript type definitions
└── public/              # Static assets
```

## API Integration

The application communicates with the backend API for:
- User authentication (signup/login/logout)
- Task management (CRUD operations)
- All requests include JWT tokens in the Authorization header

## Security Features

- JWT-based authentication
- Protected routes
- Secure token storage
- Automatic logout on token expiration
- Input validation

## Learn More

To learn more about the technologies used in this project:

- [Next.js Documentation](https://nextjs.org/docs) - Next.js features and API
- [Learn Next.js](https://nextjs.org/learn) - Interactive Next.js tutorial
- [Tailwind CSS](https://tailwindcss.com/docs) - Utility-first CSS framework
- [Better Auth](https://better-auth.com/docs) - Authentication library
