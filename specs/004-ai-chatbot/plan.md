# Implementation Plan: AI Chatbot for Natural Language Task Management

**Branch**: `004-ai-chatbot` | **Date**: 2026-02-21 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-ai-chatbot/spec.md`

## Summary

Extend the existing full-stack todo application with an AI chatbot that enables natural language task management. The backend adds a FastAPI chat endpoint that uses OpenAI Agents SDK with MCP tools wrapping existing task CRUD operations. The frontend adds a ChatKit-based conversational UI on the dashboard. Conversation history is persisted in Neon PostgreSQL. The server remains stateless — context is reconstructed from stored messages on each request.

## Technical Context

**Language/Version**: Python 3.11 (Backend), TypeScript/JavaScript ES2022 (Frontend)
**Primary Dependencies**:
- Backend: FastAPI, OpenAI Agents SDK (`openai-agents`), SQLModel, python-jose, asyncpg
- Frontend: Next.js 16+ (App Router), OpenAI ChatKit (`@openai/chat-kit` or custom chat UI), Axios
**Storage**: Neon Serverless PostgreSQL (existing) — extended with Conversation and Message tables
**Testing**: pytest + pytest-asyncio (backend), manual test scenarios (frontend)
**Target Platform**: Web (Vercel frontend, Hugging Face Spaces backend)
**Project Type**: Web application (monorepo: frontend/ + backend/)
**Performance Goals**: Chat responses within 5 seconds, conversation history load within 3 seconds
**Constraints**: Stateless server, all task ops via MCP tools, JWT auth on all chat endpoints, OpenAI API key server-side only
**Scale/Scope**: Single-user conversations, ~100 messages per conversation, same user base as existing app

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Evidence |
|------|--------|----------|
| Spec-Driven Development | PASS | Spec 004 created and approved before planning |
| Security-First Design | PASS | JWT auth enforced on all chat endpoints; user data isolation in MCP tools |
| Deterministic Behavior | PASS | AI responses routed through MCP tools; no freeform DB mutations |
| Separation of Concerns | PASS | AI agent layer isolated; backend is sole gateway; no direct frontend-to-AI |
| Zero Manual Coding | PASS | All implementation via Claude Code |
| JWT-Based Authentication | PASS | Chat requests carry user JWT; MCP tools inherit authenticated user context |
| Stateless Server Design | PASS | Conversation reconstructed from DB per request; no in-memory state |
| MCP-Driven Task Operations | PASS | All 5 task operations defined as MCP tools; no direct DB access from agent |

## Project Structure

### Documentation (this feature)

```text
specs/004-ai-chatbot/
├── plan.md              # This file
├── research.md          # Phase 0: Technology decisions
├── data-model.md        # Phase 1: Conversation/Message entities
├── quickstart.md        # Phase 1: Developer setup guide
├── contracts/           # Phase 1: API contracts
│   └── chat-api.md      # Chat endpoint contract
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── main.py                          # Existing — add chat router
├── src/
│   ├── api/
│   │   ├── auth.py                  # Existing — no changes
│   │   ├── tasks.py                 # Existing — no changes
│   │   └── chat.py                  # NEW: Chat endpoint (POST /api/chat)
│   ├── models/
│   │   ├── user.py                  # Existing — no changes
│   │   ├── task.py                  # Existing — no changes
│   │   ├── conversation.py          # NEW: Conversation + Message models
│   │   └── base_response.py         # Existing — extend with chat response
│   ├── services/
│   │   ├── auth_service.py          # Existing — no changes
│   │   └── chat_service.py          # NEW: AI agent orchestration
│   ├── tools/
│   │   └── task_tools.py            # NEW: MCP tool definitions for task ops
│   ├── middleware/
│   │   └── jwt_auth.py              # Existing — reuse get_current_user
│   └── database/
│       └── connection.py            # Existing — no changes
├── requirements.txt                 # Existing — add openai-agents, mcp deps
└── .env                             # Existing — add OPENAI_API_KEY

frontend/
├── app/
│   ├── dashboard/
│   │   └── page.tsx                 # Existing — add chat toggle/section
│   └── layout.tsx                   # Existing — no changes
├── components/
│   ├── chat/
│   │   ├── ChatInterface.tsx        # NEW: Main chat container
│   │   ├── ChatMessage.tsx          # NEW: Individual message bubble
│   │   └── ChatInput.tsx            # NEW: Message input with send button
│   └── tasks/                       # Existing — no changes
├── services/
│   ├── chat.ts                      # NEW: Chat API service
│   └── api-client.ts               # Existing — reuse for chat requests
├── types/
│   └── index.ts                     # Existing — extend with chat types
└── package.json                     # Existing — no new deps needed (fetch-based)
```

**Structure Decision**: Extend existing monorepo structure. Backend adds `src/tools/` for MCP tool definitions and `src/api/chat.py` for the chat endpoint. Frontend adds `components/chat/` for the chat UI. No new top-level directories needed.

## Complexity Tracking

No constitution violations. All gates pass.

---

## Phase 0: Research Decisions

See [research.md](./research.md) for detailed analysis.

### Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| AI Agent Framework | OpenAI Agents SDK (Python) | Constitution mandates this; native tool-calling support |
| Chat UI | Custom React components (ChatKit-inspired) | ChatKit is not a published npm package; build lightweight custom components using existing Tailwind design system |
| Tool Protocol | OpenAI Agents SDK function tools (MCP-compatible) | Agents SDK has built-in function tool support; define tools as Python functions |
| Conversation Storage | New Conversation + Message tables in existing Neon DB | Follows constitution; user-scoped, persisted across sessions |
| Chat Endpoint Pattern | Single POST /api/chat with streaming disabled (simple JSON response) | Stateless; each request sends message + gets response; conversation loaded from DB |
| Frontend Chat Placement | Slide-out panel on dashboard page | Non-disruptive; user can see tasks while chatting |

## Phase 1: Design

### Data Model

See [data-model.md](./data-model.md) for full entity definitions.

**New Entities**:
- `Conversation`: id (UUID), user_id (FK→User), created_at, updated_at
- `Message`: id (UUID), conversation_id (FK→Conversation), role (user|assistant), content (text), created_at

### API Contracts

See [contracts/chat-api.md](./contracts/chat-api.md) for full endpoint contracts.

**New Endpoint**:
- `POST /api/chat` — Send a message, receive AI response. Requires JWT. Creates/loads conversation. Persists both messages.

**Request**:
```json
{
  "message": "Add a task to buy groceries"
}
```

**Response**:
```json
{
  "response": "I've created a task 'Buy groceries' for you.",
  "conversation_id": "uuid",
  "tool_calls": [
    {"tool": "create_task", "result": {"id": "uuid", "title": "Buy groceries"}}
  ]
}
```

### MCP Tool Definitions

Five tools wrapping existing CRUD operations:

| Tool | Maps To | Parameters | Returns |
|------|---------|------------|---------|
| `create_task` | POST /api/tasks | title, description? | Created task |
| `list_tasks` | GET /api/tasks | completed? (filter) | Task list |
| `get_task` | GET /api/tasks/{id} | task_id | Single task |
| `update_task` | PUT /api/tasks/{id} | task_id, title?, description?, completed? | Updated task |
| `delete_task` | DELETE /api/tasks/{id} | task_id | Confirmation |

Each tool receives the authenticated user_id from the chat service (not from the AI agent) to enforce ownership.

### Developer Quickstart

See [quickstart.md](./quickstart.md) for setup instructions.
