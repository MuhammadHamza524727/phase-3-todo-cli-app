# Frontend Deployment Troubleshooting Guide

## Issue: 404 errors after deploying frontend to Vercel

### Root Cause Analysis:
- Frontend deployed successfully but cannot connect to backend API
- API calls from frontend to backend are failing
- Neon database connection might be affected by the domain change

### Solutions:

#### 1. Environment Variables Check
Your `vercel.json` now includes:
```json
{
  "env": {
    "NEXT_PUBLIC_API_BASE_URL": "https://hamza-developer-phase2-backend.hf.space",
    "FRONTEND_URL": "https://hackathon-phase2-frontend.vercel.app",
    "BACKEND_URL": "https://hamza-developer-phase2-backend.hf.space"
  }
}
```

#### 2. Backend Configuration Needed
Your backend API might need to be configured to accept requests from your Vercel domain. Check if your backend has CORS settings that include:
- `https://hackathon-phase2-frontend.vercel.app`
- Your Vercel domain

#### 3. Neon Database Connection
The Neon database connection is handled by your backend API, not the frontend. The 404 errors suggest the issue is with API endpoint access, not database connection directly.

#### 4. Authentication Flow
The authentication flow works as follows:
1. Frontend makes login/signup requests to backend
2. Backend authenticates and creates JWT tokens
3. Backend returns tokens to frontend
4. Frontend stores tokens in localStorage
5. Frontend uses tokens for subsequent API requests

#### 5. Debugging Steps
1. Check browser console (F12) → Network tab after visiting your deployed site
2. Look for failed API requests (they'll show as 404, 401, or 500 errors)
3. Verify the request URLs are pointing to the correct backend
4. Check if CORS errors appear in the console

#### 6. Verification Commands
Test the backend endpoints directly:
```bash
curl -X GET https://hamza-developer-phase2-backend.hf.space/health
curl -X GET https://hamza-developer-phase2-backend.hf.space/docs
```

#### 7. Common Issues & Fixes
- **CORS errors**: Backend needs to allow requests from your Vercel domain
- **404 errors**: Wrong API endpoint URLs or backend not configured properly
- **401 errors**: Authentication tokens not being sent properly
- **Connection timeouts**: Backend might be down or overloaded

#### 8. Next Steps
1. Redeploy your frontend with the updated `vercel.json`
2. Monitor the browser console for specific error messages
3. If issues persist, check your backend logs for any domain-restriction settings