# Vercel Deployment Setup Guide

This guide explains how to properly configure your frontend for deployment on Vercel with the external backend API.

## Required Environment Variables

For your frontend to connect properly to the backend API, you need to set the following environment variables in your Vercel project:

### Required Variables:
- `NEXT_PUBLIC_API_BASE_URL` = `https://hamza-developer-phase2-backend.hf.space`

### Optional Variables (but recommended):
- `FRONTEND_URL` = `https://your-project-name.vercel.app` (replace with your actual Vercel URL)
- `BACKEND_URL` = `https://hamza-developer-phase2-backend.hf.space`

## How to Set Environment Variables in Vercel

### Option 1: Via Vercel Dashboard
1. Go to your Vercel dashboard: https://vercel.com/dashboard
2. Select your project
3. Navigate to **Settings** → **Environment Variables**
4. Add the following variables:
   - Key: `NEXT_PUBLIC_API_BASE_URL`, Value: `https://hamza-developer-phase2-backend.hf.space`
   - Key: `FRONTEND_URL`, Value: `https://your-project-name.vercel.app`
   - Key: `BACKEND_URL`, Value: `https://hamza-developer-phase2-backend.hf.space`
5. Click **Save** and then **Redeploy** your project

### Option 2: Via Vercel CLI
```bash
# Install Vercel CLI if you haven't already
npm install -g vercel

# Navigate to your frontend directory
cd /path/to/your/frontend

# Add environment variables
vercel env add NEXT_PUBLIC_API_BASE_URL production
# When prompted, enter: https://hamza-developer-phase2-backend.hf.space

vercel env add FRONTEND_URL production
# When prompted, enter: https://your-project-name.vercel.app

vercel env add BACKEND_URL production
# When prompted, enter: https://hamza-developer-phase2-backend.hf.space
```

## Verifying the Setup

After setting the environment variables and redeploying:

1. Your frontend should be able to make API requests to the backend
2. Authentication endpoints (`/api/login`, `/api/register`) should work
3. Task endpoints (`/api/tasks`) should work with proper authentication

## Troubleshooting

### If you still get 404 errors or API connection issues after deployment:

1. **Verify the API URL**: Check that `NEXT_PUBLIC_API_BASE_URL` is exactly `https://hamza-developer-phase2-backend.hf.space`
2. **Check browser console**: Open Developer Tools (F12) → Network tab to see the actual API requests being made
3. **Verify backend status**: The backend should be accessible at https://hamza-developer-phase2-backend.hf.space
4. **Confirm environment variables**: Double-check that the environment variables are set in the Vercel dashboard, not just in local files
5. **Check for CORS issues**: The backend should have proper CORS configuration to accept requests from your Vercel domain
6. **Force redeployment**: After setting environment variables, make sure to trigger a new deployment

### Backend API Endpoints
Your backend supports these endpoints:
- `POST /api/login` - User login
- `POST /api/register` - User registration
- `GET /api/tasks` - Get user tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{task_id}` - Update task
- `DELETE /api/tasks/{task_id}` - Delete task
- `PATCH /api/tasks/{task_id}/complete` - Toggle task completion

## Redeployment
After setting the environment variables, make sure to redeploy your project for the changes to take effect.

## Testing Locally
To test the configuration locally, make sure your `.env.local` file contains:
```
NEXT_PUBLIC_API_BASE_URL=https://hamza-developer-phase2-backend.hf.space
FRONTEND_URL=http://localhost:3000
BACKEND_URL=https://hamza-developer-phase2-backend.hf.space
```

## Note about vercel.json
The `vercel.json` file in your project has been configured with `"framework": "nextjs"` to ensure proper Next.js deployment. Environment variables should be set via the Vercel dashboard rather than in the `vercel.json` file for better security and flexibility.