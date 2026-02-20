# Vercel Deployment Guide

## Prerequisites
- Vercel account
- GitHub repository connected to Vercel
- Backend API deployed and accessible

## Environment Variables

Add the following environment variable in your Vercel project settings:

```
NEXT_PUBLIC_API_BASE_URL=https://hamza-developer-hackathon2-phase2.hf.space
```

### How to Add Environment Variables in Vercel:

1. Go to your project in Vercel Dashboard
2. Click on "Settings"
3. Navigate to "Environment Variables"
4. Add the variable:
   - **Name**: `NEXT_PUBLIC_API_BASE_URL`
   - **Value**: `https://hamza-developer-hackathon2-phase2.hf.space`
   - **Environment**: Select all (Production, Preview, Development)
5. Click "Save"

## Deployment Steps

### Option 1: Deploy via Vercel Dashboard

1. Push your code to GitHub
2. Go to [Vercel Dashboard](https://vercel.com/dashboard)
3. Click "Add New Project"
4. Import your GitHub repository
5. Configure project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
6. Add environment variables (see above)
7. Click "Deploy"

### Option 2: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend directory
cd frontend

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

## Post-Deployment

After deployment:

1. Visit your deployed URL
2. Test the following:
   - Homepage loads correctly
   - Sign up functionality works
   - Login functionality works
   - Dashboard is accessible after login
   - Task creation, editing, and deletion work

## Troubleshooting

### 404 Error on Deployment

If you see a 404 error:
- Ensure the `lib/auth-context.tsx` and `lib/utils.ts` files exist
- Check that environment variables are set correctly
- Verify the build completed successfully in Vercel logs

### API Connection Issues

If API calls fail:
- Verify `NEXT_PUBLIC_API_BASE_URL` is set correctly
- Check that the backend API is accessible
- Ensure CORS is configured on the backend to allow your Vercel domain

### Build Failures

If the build fails:
- Check Vercel build logs for specific errors
- Ensure all dependencies are in `package.json`
- Verify TypeScript types are correct

## Redeployment

To redeploy after fixes:

1. Push changes to GitHub
2. Vercel will automatically redeploy
3. Or manually trigger deployment from Vercel Dashboard

## Important Files

- [`lib/auth-context.tsx`](lib/auth-context.tsx) - Authentication context provider
- [`lib/utils.ts`](lib/utils.ts) - Utility functions
- [`.env.local`](.env.local) - Local environment variables (not committed)
- [`.env.example`](.env.example) - Example environment variables

## Support

For issues, check:
- Vercel deployment logs
- Browser console for frontend errors
- Backend API logs for server errors
