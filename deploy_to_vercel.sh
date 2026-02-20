#!/bin/bash

# Quick Deployment Script for Vercel
# This script commits changes and pushes to trigger Vercel deployment

echo "🚀 Starting Vercel Deployment Process..."
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Navigate to project root
cd "$(dirname "$0")"

echo -e "${BLUE}Step 1:${NC} Adding all changes to git..."
git add .

echo ""
echo -e "${BLUE}Step 2:${NC} Committing changes..."
git commit -m "fix: Add missing lib files and deployment documentation for 404 fix"

echo ""
echo -e "${BLUE}Step 3:${NC} Pushing to remote repository..."
git push origin main

echo ""
echo -e "${GREEN}✅ Changes pushed successfully!${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${YELLOW}⏳ Vercel is now deploying your application...${NC}"
echo ""
echo "What happens next:"
echo "1. Vercel detects the git push"
echo "2. Starts building your application (1-3 minutes)"
echo "3. Deploys to production"
echo ""
echo "To monitor deployment:"
echo "→ Visit: https://vercel.com/dashboard"
echo "→ Go to your project"
echo "→ Click on 'Deployments' tab"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${YELLOW}⚠ IMPORTANT:${NC} Set environment variable in Vercel Dashboard"
echo ""
echo "Before testing, ensure this is set:"
echo "→ Go to: Settings → Environment Variables"
echo "→ Add: NEXT_PUBLIC_API_BASE_URL"
echo "→ Value: https://hamza-developer-hackathon2-phase2.hf.space"
echo "→ Apply to: Production, Preview, Development"
echo ""
echo "After deployment completes (check Vercel dashboard):"
echo "→ Visit your Vercel URL"
echo "→ The 404 error should be resolved"
echo "→ You should see the homepage"
echo ""
echo -e "${GREEN}✨ Deployment initiated successfully!${NC}"
