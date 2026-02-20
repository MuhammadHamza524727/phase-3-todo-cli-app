#!/bin/bash

# Verification Script for Vercel Deployment
# This script checks if all required files exist before deployment

echo "🔍 Verifying Deployment Readiness..."
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track overall status
ALL_CHECKS_PASSED=true

# Function to check file existence
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
        return 0
    else
        echo -e "${RED}✗${NC} $1 is missing"
        ALL_CHECKS_PASSED=false
        return 1
    fi
}

# Function to check directory existence
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 directory exists"
        return 0
    else
        echo -e "${RED}✗${NC} $1 directory is missing"
        ALL_CHECKS_PASSED=false
        return 1
    fi
}

echo "📁 Checking Required Files..."
echo ""

# Check critical files
check_file "frontend/lib/auth-context.tsx"
check_file "frontend/lib/utils.ts"
check_file "frontend/app/layout.tsx"
check_file "frontend/app/page.tsx"
check_file "frontend/package.json"
check_file "frontend/next.config.ts"

echo ""
echo "📁 Checking Environment Files..."
echo ""

check_file "frontend/.env.local"
check_file "frontend/.env.example"

echo ""
echo "📁 Checking App Routes..."
echo ""

check_dir "frontend/app/login"
check_dir "frontend/app/signup"
check_dir "frontend/app/dashboard"
check_file "frontend/app/login/page.tsx"
check_file "frontend/app/signup/page.tsx"
check_file "frontend/app/dashboard/page.tsx"

echo ""
echo "📁 Checking Services..."
echo ""

check_dir "frontend/services"
check_file "frontend/services/api.ts"
check_file "frontend/services/api-client.ts"

echo ""
echo "🔍 Checking Environment Variable..."
echo ""

if [ -f "frontend/.env.local" ]; then
    if grep -q "NEXT_PUBLIC_API_BASE_URL" "frontend/.env.local"; then
        API_URL=$(grep "NEXT_PUBLIC_API_BASE_URL" "frontend/.env.local" | cut -d '=' -f2)
        echo -e "${GREEN}✓${NC} NEXT_PUBLIC_API_BASE_URL is set to: $API_URL"
    else
        echo -e "${RED}✗${NC} NEXT_PUBLIC_API_BASE_URL not found in .env.local"
        ALL_CHECKS_PASSED=false
    fi
fi

echo ""
echo "🔍 Checking Git Status..."
echo ""

cd frontend 2>/dev/null || cd .

# Check if git is initialized
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Git repository detected"
    
    # Check for uncommitted changes
    if [[ -n $(git status -s) ]]; then
        echo -e "${YELLOW}⚠${NC} You have uncommitted changes:"
        git status -s | head -10
        echo ""
        echo -e "${YELLOW}→${NC} Run: git add . && git commit -m 'fix: Add missing files' && git push"
    else
        echo -e "${GREEN}✓${NC} All changes are committed"
    fi
else
    echo -e "${YELLOW}⚠${NC} Not a git repository or git not initialized"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ "$ALL_CHECKS_PASSED" = true ]; then
    echo -e "${GREEN}✅ All checks passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Ensure environment variable is set in Vercel Dashboard"
    echo "2. Push changes to git: git push origin main"
    echo "3. Vercel will automatically redeploy"
    echo "4. Wait 1-3 minutes for deployment to complete"
    echo "5. Visit your Vercel URL to verify"
else
    echo -e "${RED}❌ Some checks failed!${NC}"
    echo ""
    echo "Please fix the issues above before deploying."
    echo "See DEPLOYMENT_STEPS.md for detailed instructions."
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
