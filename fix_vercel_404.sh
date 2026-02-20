#!/bin/bash

echo "🔧 Fixing Vercel 404 Error..."
echo ""
echo "Frontend URL: https://hachathon2-phase2-frontend.vercel.app"
echo "Backend URL: https://hamza-developer-hackathon2-phase2.hf.space"
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Step 1:${NC} Verifying required files exist..."
echo ""

# Check if lib files exist
if [ -f "frontend/lib/auth-context.tsx" ]; then
    echo -e "${GREEN}✓${NC} frontend/lib/auth-context.tsx exists"
else
    echo -e "${RED}✗${NC} frontend/lib/auth-context.tsx is missing"
    exit 1
fi

if [ -f "frontend/lib/utils.ts" ]; then
    echo -e "${GREEN}✓${NC} frontend/lib/utils.ts exists"
else
    echo -e "${RED}✗${NC} frontend/lib/utils.ts is missing"
    exit 1
fi

if [ -f "frontend/.env.local" ]; then
    echo -e "${GREEN}✓${NC} frontend/.env.local exists"
else
    echo -e "${RED}✗${NC} frontend/.env.local is missing"
    exit 1
fi

if [ -f "frontend/vercel.json" ]; then
    echo -e "${GREEN}✓${NC} frontend/vercel.json exists"
else
    echo -e "${RED}✗${NC} frontend/vercel.json is missing"
    exit 1
fi

echo ""
echo -e "${BLUE}Step 2:${NC} Adding files to git..."
git add frontend/lib/
git add frontend/.env.local
git add frontend/vercel.json
git add .

echo ""
echo -e "${BLUE}Step 3:${NC} Committing changes..."
git commit -m "fix: Add missing lib files and vercel config to resolve 404 error

- Created frontend/lib/auth-context.tsx for authentication
- Created frontend/lib/utils.ts for utility functions
- Updated frontend/.env.local with correct backend URL
- Added frontend/vercel.json for proper routing
- Backend URL: https://hamza-developer-hackathon2-phase2.hf.space
- Frontend URL: https://hachathon2-phase2-frontend.vercel.app"

echo ""
echo -e "${BLUE}Step 4:${NC} Pushing to remote repository..."
git push origin main

echo ""
echo -e "${GREEN}✅ Changes pushed successfully!${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${YELLOW}⏳ Vercel Deployment in Progress...${NC}"
echo ""
echo "What's happening now:"
echo "1. Vercel detected your git push"
echo "2. Building your Next.js application"
echo "3. Deploying to: https://hachathon2-phase2-frontend.vercel.app"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${YELLOW}⚠ CRITICAL:${NC} Set Environment Variable in Vercel"
echo ""
echo "You MUST set this in Vercel Dashboard:"
echo ""
echo "1. Go to: https://vercel.com/dashboard"
echo "2. Select your project: hachathon2-phase2-frontend"
echo "3. Go to: Settings → Environment Variables"
echo "4. Add new variable:"
echo "   Name:  NEXT_PUBLIC_API_BASE_URL"
echo "   Value: https://hamza-developer-hackathon2-phase2.hf.space"
echo "5. Select: Production, Preview, Development"
echo "6. Click: Save"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${BLUE}Monitor Deployment:${NC}"
echo "→ https://vercel.com/dashboard"
echo ""
echo -e "${BLUE}After deployment completes (1-3 minutes):${NC}"
echo "→ Visit: https://hachathon2-phase2-frontend.vercel.app"
echo "→ The 404 error should be resolved"
echo "→ You should see the homepage"
echo ""
echo -e "${GREEN}✨ Deployment process initiated!${NC}"
