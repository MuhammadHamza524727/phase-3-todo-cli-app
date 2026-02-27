# Quickstart: AI Chatbot Feature

**Feature**: 004-ai-chatbot | **Date**: 2026-02-21

## Prerequisites

- Existing backend running (Phase 2 complete)
- Existing frontend running (Phase 3 Spec 003 complete)
- OpenAI API key

## Backend Setup

### 1. Install new dependencies

```bash
cd backend
pip install openai-agents
```

### 2. Add environment variable

Add to `backend/.env`:
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### 3. Database tables

New Conversation and Message tables are auto-created on startup via SQLModel `metadata.create_all` (same pattern as existing tables).

### 4. Verify

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Test chat endpoint:
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Show my tasks"}'
```

## Frontend Setup

No new dependencies needed. Chat components use existing Axios client and Tailwind CSS.

### Verify

```bash
cd frontend
npm run dev
```

Navigate to dashboard — chat panel should be accessible via toggle button.

## File Checklist

### Backend (new files)
- [ ] `src/models/conversation.py` — Conversation + Message SQLModel models
- [ ] `src/tools/task_tools.py` — MCP tool definitions (5 tools)
- [ ] `src/services/chat_service.py` — Agent orchestration service
- [ ] `src/api/chat.py` — Chat endpoint router

### Backend (modified files)
- [ ] `main.py` — Register chat router
- [ ] `requirements.txt` — Add openai-agents
- [ ] `.env` — Add OPENAI_API_KEY
- [ ] `src/models/base_response.py` — Add ChatResponse schema

### Frontend (new files)
- [ ] `components/chat/ChatInterface.tsx` — Chat container
- [ ] `components/chat/ChatMessage.tsx` — Message bubble
- [ ] `components/chat/ChatInput.tsx` — Input with send
- [ ] `services/chat.ts` — Chat API service

### Frontend (modified files)
- [ ] `app/dashboard/page.tsx` — Add chat toggle + panel
- [ ] `types/index.ts` — Add chat types

## Environment Variables Summary

| Variable | Location | Required | Description |
|----------|----------|----------|-------------|
| `OPENAI_API_KEY` | backend/.env | YES | OpenAI API key for Agents SDK |
| `DATABASE_URL` | backend/.env | Existing | Neon PostgreSQL (already configured) |
| `JWT_SECRET` | backend/.env | Existing | JWT signing key (already configured) |
