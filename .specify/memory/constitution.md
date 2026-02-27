<!--
Sync Impact Report:
- Version change: 1.1.0 → 2.0.0
- Modified principles:
  - "Separation of Concerns" → "Separation of Concerns (Monorepo)"
  - "Architecture Standards" expanded for Phase III AI stack
  - "Success Criteria" expanded for Phase III chatbot features
- Added sections:
  - AI Chatbot Architecture
  - MCP-Driven Task Operations
  - Conversation Management
  - Phase III Spec Mapping
- Removed sections: None
- Templates requiring updates:
  - .specify/templates/plan-template.md (⚠ pending — add AI/MCP constitution gates)
  - .specify/templates/spec-template.md (⚠ pending — no structural changes needed)
  - .specify/templates/tasks-template.md (⚠ pending — no structural changes needed)
- Follow-up TODOs: None
-->
# Todo AI Chatbot — Full-Stack Web Application Constitution

## Core Principles

### Spec-Driven Development
No implementation without an approved spec. Every feature MUST trace back to a written spec. All changes MUST follow: Spec → Plan → Tasks → Implement. Phase III introduces three new specs (004, 005, 006) that govern all AI chatbot functionality.

### Security-First Design
Authentication, authorization, and data isolation are paramount. All protected endpoints MUST require a valid JWT. Requests without JWT MUST return 401 Unauthorized. User data isolation is mandatory (no cross-user data access). Conversation history MUST be scoped per user.

### Deterministic Behavior
Predictable, testable API and UI flows. All API behavior MUST match the defined REST contract exactly. API responses MUST be consistent and typed. Meaningful HTTP status codes for all API responses. AI chatbot responses MUST be routed through defined MCP tool operations — no freeform database mutations.

### Separation of Concerns (Monorepo)
Authentication, backend, frontend, and AI agent layer are clearly isolated within a single monorepo. No shared session state between frontend and backend. JWT verification MUST be stateless and backend-controlled. The AI agent layer MUST NOT bypass the backend API for data access.

### Zero Manual Coding
All implementation via Claude Code. No manual code edits allowed. No feature creep beyond defined requirements.

### JWT-Based Authentication
JWT signature MUST be verified using shared secret. JWT expiration MUST be respected. Task ownership MUST be enforced at query level. Backend MUST NOT trust client-provided user IDs blindly. AI chatbot requests MUST carry the user's JWT for all task operations.

### Stateless Server Design
The backend server MUST remain stateless. All conversation context MUST be persisted in the database, not in server memory. Each AI request MUST be self-contained — the server reconstructs context from stored conversation history.

### MCP-Driven Task Operations
All task CRUD operations initiated by the AI chatbot MUST be executed through MCP (Model Context Protocol) tools. The AI agent MUST NOT generate raw SQL or directly mutate the database. MCP tools are the single interface between the AI agent and the task data layer.

## Architecture Standards

### Phase I–III Shared Stack
- **Frontend**: Next.js 16+ (App Router)
- **Backend**: Python FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth (JWT-based)
- **Communication**: RESTful APIs with JSON
- **Authorization**: Bearer JWT via Authorization header

### Phase III AI Chatbot Stack
- **AI Agent Framework**: OpenAI Agents SDK (Python)
- **AI Chat Frontend**: OpenAI ChatKit (React)
- **Tool Protocol**: MCP (Model Context Protocol)
- **Conversation Storage**: Neon PostgreSQL (conversation + message tables)
- **Server Model**: Stateless — conversation reconstructed from DB per request

## AI Chatbot Architecture

The AI chatbot enables users to manage tasks via natural language. The architecture enforces:

1. **Frontend (ChatKit)** sends user messages with JWT to the backend.
2. **Backend (FastAPI)** authenticates the request, loads conversation history from DB, invokes the AI agent.
3. **AI Agent (Agents SDK)** processes the message using MCP tools to read/write tasks.
4. **MCP Tools** execute task operations (create, read, update, delete, list) against the database via SQLModel.
5. **Response** flows back through the agent → backend → frontend. Conversation turn is persisted to DB.

No direct frontend-to-AI communication. The backend is the sole gateway.

## MCP-Driven Task Operations

All task operations available to the AI agent MUST be defined as MCP tools:

- `create_task` — Create a new task for the authenticated user
- `list_tasks` — List tasks with optional filters (status, priority)
- `update_task` — Update task fields (title, description, status, priority)
- `delete_task` — Delete a task by ID
- `get_task` — Retrieve a single task by ID

Each MCP tool MUST enforce user ownership via JWT-extracted user ID. No tool may operate on another user's data.

## Conversation Management

- Conversations MUST be stored in the database with user ownership.
- Each message (user or assistant) MUST be persisted as a row with role, content, and timestamp.
- The backend MUST load conversation history before each AI agent invocation.
- Conversation history MUST be scoped to the authenticated user only.
- Old conversations MAY be paginated or summarized for context window management.

## Security Standards

All protected endpoints MUST require a valid JWT. Requests without JWT MUST return 401 Unauthorized. JWT signature MUST be verified using shared secret. JWT expiration MUST be respected. Task ownership MUST be enforced at query level. Backend MUST NOT trust client-provided user IDs blindly. AI agent tool calls MUST inherit the authenticated user context — no privilege escalation.

## Development Constraints

No manual code edits allowed. All changes MUST follow: Spec → Plan → Tasks → Implement. No feature creep beyond defined requirements. No shared session state between frontend and backend. All configuration via environment variables. All errors MUST return structured JSON responses. AI agent API keys MUST be server-side only — never exposed to the frontend.

## Quality Constraints

API responses MUST be consistent and typed. Frontend MUST be responsive (mobile-first). Clear loading, error, and empty states in UI. Meaningful HTTP status codes for all API responses. Database schema MUST support future extensibility. AI chatbot MUST handle tool failures gracefully with user-friendly messages.

## Testing & Validation Requirements

Manual test scenarios MUST be defined in specs. Auth flow MUST be tested end-to-end. Multi-user isolation MUST be validated. Token expiry behavior MUST be verifiable. CRUD operations MUST be validated per user. AI chatbot conversations MUST be tested for correct MCP tool invocation and response formatting.

## Documentation Standards

Specs MUST be human-readable and unambiguous. API endpoints MUST be clearly documented. Auth flow MUST be diagrammable from spec alone. Environment variables MUST be explicitly listed. Assumptions MUST be stated explicitly. MCP tool interfaces MUST be documented with input/output schemas.

## Phase III Spec Mapping

| Spec | Name | Scope |
|------|------|-------|
| 004 | AI Chatbot Backend | Agents SDK integration, MCP tool definitions, conversation persistence, FastAPI endpoints for chat |
| 005 | AI Chatbot Frontend | ChatKit integration, chat UI, message streaming, JWT-authenticated chat requests |
| 006 | AI Task Intelligence | Smart task suggestions, natural language task parsing, multi-step task workflows via agent |

## Success Criteria

### Phase I–II (Existing)
Users can signup and signin successfully. Authenticated users receive valid JWTs. JWT-secured API accepts only authorized requests. Each user can only access their own tasks. All CRUD task operations function correctly. Data persists in Neon PostgreSQL across sessions. Frontend and backend operate independently but securely.

### Phase III (AI Chatbot)
Users can interact with an AI chatbot to manage tasks via natural language. The chatbot correctly invokes MCP tools to create, list, update, and delete tasks. Conversation history persists across sessions. The server remains stateless — no in-memory conversation state. All chatbot operations enforce JWT authentication and user data isolation. The system passes hackathon review for architecture, security, AI integration, and process.

## Governance

Constitution supersedes all other practices. Amendments require documentation, approval, and migration plan. All PRs/reviews MUST verify compliance. Complexity MUST be justified. Environment-based secrets management (no hardcoded secrets). Use development guidance for runtime development guidance.

**Version**: 2.0.0 | **Ratified**: 2026-01-23 | **Last Amended**: 2026-02-21
