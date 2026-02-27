# Research: AI Chatbot for Natural Language Task Management

**Feature**: 004-ai-chatbot | **Date**: 2026-02-21

## R1: AI Agent Framework — OpenAI Agents SDK

**Decision**: Use OpenAI Agents SDK (`openai-agents`) for Python

**Rationale**:
- Constitution mandates OpenAI Agents SDK as the AI agent framework
- Native function/tool calling support — define Python functions as agent tools
- Built-in conversation management — agent handles multi-turn context
- Compatible with GPT-4o-mini for cost-effective task management

**Alternatives Considered**:
- LangChain: More abstraction layers than needed; constitution specifies Agents SDK
- Direct OpenAI API: No agent orchestration; would need manual tool call handling
- Anthropic Claude SDK: Not specified in constitution

**Integration Pattern**:
```
User message → FastAPI endpoint → Load conversation from DB →
Create Agent with tools → Agent.run(messages) →
Parse tool calls → Execute tools → Return response →
Persist messages to DB
```

**Key Package**: `openai-agents` (pip install)
- Requires `OPENAI_API_KEY` env var
- Agent definition: `Agent(name, instructions, tools=[...])`
- Run: `Runner.run(agent, messages)` — returns response with tool call results

## R2: Chat UI Approach — Custom React Components

**Decision**: Build custom chat components using existing Tailwind design system

**Rationale**:
- OpenAI ChatKit (`@openai/chat-kit`) is not a stable/published npm package as of Feb 2026
- The existing frontend uses Tailwind CSS v4 with a well-defined design system (purple theme, glass morphism)
- Building 3 small components (ChatInterface, ChatMessage, ChatInput) is minimal effort
- Maintains visual consistency with the existing dashboard

**Alternatives Considered**:
- `@openai/chat-kit`: Not available as a stable npm package; would require ejecting/customizing
- `@chatscope/chat-ui-kit-react`: External dependency with its own styling — conflicts with existing Tailwind theme
- shadcn/ui chat component: Would need shadcn setup; over-engineered for this scope

**Components Needed**:
1. `ChatInterface.tsx` — Container with message list and input area (~100 lines)
2. `ChatMessage.tsx` — Message bubble with role-based styling (~40 lines)
3. `ChatInput.tsx` — Text input with send button and loading state (~50 lines)

## R3: MCP Tool Implementation Pattern

**Decision**: Define tools as Python functions with OpenAI Agents SDK `function_tool` decorator

**Rationale**:
- OpenAI Agents SDK supports `@function_tool` decorator to convert Python functions into agent tools
- Each tool function directly calls the existing SQLModel queries (same logic as task routes)
- User ID is injected via a shared context object, not passed by the AI agent
- This satisfies the constitution's MCP requirement: all task ops go through defined tool interfaces

**Alternatives Considered**:
- Full MCP server (separate process): Over-engineered for 5 tools; adds deployment complexity
- Direct database queries in agent: Violates constitution (no freeform DB mutations)
- HTTP calls to existing API endpoints: Adds network overhead; auth would need to be forwarded

**Tool Implementation Pattern**:
```python
from agents import function_tool

@function_tool
async def create_task(title: str, description: str = "") -> str:
    """Create a new task for the user."""
    # Uses context.user_id injected by chat service
    # Calls SQLModel directly (same queries as tasks.py routes)
    ...
```

## R4: Conversation Storage Schema

**Decision**: Two new tables — `conversation` and `message` — in existing Neon PostgreSQL

**Rationale**:
- Constitution requires conversation persistence in database
- Simple schema: one conversation per user (initially), messages ordered by timestamp
- SQLModel models consistent with existing User and Task models
- User-scoped via foreign key to User table

**Alternatives Considered**:
- JSON field on User model: Not queryable; poor for message history retrieval
- Separate database/service: Unnecessary complexity for current scale
- File-based storage: Not persistent across deployments; violates cloud-native approach

**Schema Design**:
- `conversation`: id, user_id (FK, unique — one conversation per user), created_at, updated_at
- `message`: id, conversation_id (FK), role (enum: user/assistant), content (text), created_at

## R5: Chat Endpoint Architecture

**Decision**: Single `POST /api/chat` endpoint with JSON request/response (no streaming)

**Rationale**:
- Stateless design: each request is self-contained
- Simple to implement and test
- Frontend shows loading indicator while waiting
- Streaming (SSE) adds complexity without significant UX benefit for short task-management responses

**Alternatives Considered**:
- Server-Sent Events (SSE): Better UX for long responses; overkill for "Task created: Buy groceries"
- WebSockets: Persistent connection contradicts stateless server design
- Multiple endpoints (send/receive): Adds complexity; single endpoint is sufficient

**Request Flow**:
1. Frontend sends `POST /api/chat` with `{ message: "..." }` + JWT header
2. Backend authenticates user via JWT
3. Backend loads or creates conversation for user
4. Backend loads message history from DB
5. Backend creates Agent with MCP tools, runs with history + new message
6. Backend persists user message + assistant response to DB
7. Backend returns `{ response: "...", conversation_id: "...", tool_calls: [...] }`

## R6: Frontend Chat Placement

**Decision**: Collapsible chat panel on the dashboard page

**Rationale**:
- Users can see their task list while chatting (context awareness)
- Toggle button to show/hide chat — non-disruptive
- Consistent with the existing dashboard layout
- Mobile: chat panel overlays full screen; desktop: side panel

**Alternatives Considered**:
- Separate /chat page: Loses context of task list; requires navigation
- Floating chat bubble (bottom-right): Common pattern but feels like support chat, not core feature
- Tab within dashboard: Would require restructuring existing dashboard layout
