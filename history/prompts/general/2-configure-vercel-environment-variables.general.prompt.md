---
id: 2
title: configure-vercel-environment-variables
stage: general
date: 2026-02-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: claude
command: general
labels: ["deployment", "configuration", "environment", "vercel", "backend-integration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - /mnt/d/desktop/hackhathon_spec_driven/hackathon2/phase-2-todo-cli-app/frontend/VERCEL_SETUP.md
  - /mnt/d/desktop/hackhathon_spec_driven/hackathon2/phase-2-todo-cli-app/frontend/check-env.js
tests_yaml: []
---

# Prompt
Address 404 error after deploying frontend to Vercel where frontend cannot connect to backend API at https://hamza-developer-phase2-backend.hf.space

# Response
Identified and documented the solution for the 404 error occurring after deploying the frontend to Vercel. The issue was that the environment variables were not properly configured in the Vercel deployment to connect to the external backend API.

Root cause analysis showed that:
1. The backend API at https://hamza-developer-phase2-backend.hf.space is working correctly with all required endpoints
2. The backend exposes the proper API routes (/api/login, /api/register, /api/tasks, etc.)
3. The frontend expects the NEXT_PUBLIC_API_BASE_URL environment variable to be set to connect to the backend
4. The Vercel deployment was missing the environment variable configuration

Created VERCEL_SETUP.md guide with detailed instructions on how to configure the environment variables in Vercel:
- NEXT_PUBLIC_API_BASE_URL = https://hamza-developer-phase2-backend.hf.space
- FRONTEND_URL = https://your-project-name.vercel.app
- BACKEND_URL = https://hamza-developer-phase2-backend.hf.space

Also created a check-env.js script to verify environment variable configuration.

The backend API endpoints are confirmed to be working:
- Health check: GET /health
- Login: POST /api/login
- Register: POST /api/register
- Tasks: GET/POST/PUT/DELETE/PATCH /api/tasks/*

# Outcome
Documented the exact steps needed to configure Vercel environment variables to connect the frontend to the external backend API. Created comprehensive setup guide and verification tools.

# Evaluation
The solution addresses the core issue by providing clear, step-by-step instructions for configuring the environment variables in Vercel. The backend connectivity issue will be resolved once the user follows the documented steps to set the environment variables and redeploy the application.