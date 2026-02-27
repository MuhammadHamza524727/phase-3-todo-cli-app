# Implementation Plan: Conversation Persistence for AI Chatbot

**Branch**: `006-conversation-persistence` | **Date**: 2026-02-22 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/006-conversation-persistence/spec.md`

## Summary

Formalize and align the existing Conversation and Message models (implemented in Spec 004) with the Spec-6 data persistence requirements. The models already exist in `backend/src/models/conversation.py`. This plan identifies gaps: add database indexes for performance (FR-012, FR-013), add cascade deletion (FR-011), validate role constraints (FR-015), and ensure the chat service uses paginated queries (FR-010). No new tables — alignment of existing tables to formal spec.

## Technical Context

**Language/Version**: Python 3.11 (Backend)
**Primary Dependencies**: FastAPI, SQLModel, asyncpg, SQLAlchemy (async)
**Storage**: Neon Serverless PostgreSQL (existing — Conversation and Message tables from Spec 004)
**Testing**: pytest + pytest-asyncio
**Target Platform**: Web (backend deployed to Hugging Face Spaces)
**Project Type**: Web application (monorepo: frontend/ + backend/)
**Performance Goals**: Conversation lookup <100ms (SC-002), 50 messages from 500+ in <1s (SC-003)
**Constraints**: One conversation per user (unique constraint), cascade deletion, role validation
**Scale/Scope**: ~500 messages per conversation, same user base as existing app

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Evidence |
|------|--------|----------|
| Spec-Driven Development | PASS | Spec 006 created and approved before planning |
| Security-First Design | PASS | Conversations scoped per user; no cross-user access |
| Deterministic Behavior | PASS | Message storage is append-only; consistent ordering by timestamp |
| Separation of Concerns | PASS | Models in `src/models/`, services in `src/services/` |
| Zero Manual Coding | PASS | All implementation via Claude Code |
| JWT-Based Authentication | PASS | User identity from JWT determines conversation ownership |
| Stateless Server Design | PASS | Conversation reconstructed from DB per request |
| MCP-Driven Task Operations | N/A | This spec covers data persistence, not MCP tools |

## Project Structure

### Documentation (this feature)

```text
specs/006-conversation-persistence/
├── plan.md              # This file
├── research.md          # Phase 0: Gap analysis
├── data-model.md        # Phase 1: Conversation + Message entities
├── quickstart.md        # Phase 1: Verification guide
├── contracts/           # Phase 1: Data access contracts
│   └── data-access.md   # Query patterns and pagination
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   └── conversation.py      # Existing — MODIFY: add indexes, cascade, role validation
│   ├── services/
│   │   └── chat_service.py      # Existing — VERIFY: pagination support
│   └── api/
│       └── chat.py              # Existing — no changes expected
└── tests/
    └── unit/
        └── test_conversation_model.py  # NEW: Model validation tests
```

**Structure Decision**: Modify existing files only. Conversation and Message models already exist from Spec 004. This spec adds indexes, cascade deletion, and validation constraints.

## Complexity Tracking

No constitution violations. All gates pass.

---

## Phase 0: Research Decisions

See [research.md](./research.md) for detailed analysis.

### Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Index strategy | Add index on `conversation.user_id` and `message.conversation_id` + `message.created_at` | SC-002 requires <100ms user lookup; SC-003 requires <1s message retrieval |
| Cascade deletion | SQLAlchemy `cascade="all, delete-orphan"` on relationship | FR-011 requires automatic message deletion |
| Role validation | String constraint in model (max_length=20, limited to "user"/"assistant") | FR-015 — already partially implemented via max_length=20 |
| Unique constraint | Already exists on `conversation.user_id` | FR-003 — one conversation per user |
| Pagination | Already implemented in `chat_service.py` via limit/offset | FR-010 — verify and document |

## Phase 1: Design

### Data Model

See [data-model.md](./data-model.md) for full entity definitions.

### Gap Analysis: Current Implementation vs Spec-6

| Spec-6 Requirement | Current Status | Action Required |
|---------------------|----------------|-----------------|
| FR-001 Conversations store | Exists | None |
| FR-002 Unique ID + user FK | Exists | None |
| FR-003 One conversation per user | Exists (unique=True on user_id) | None |
| FR-004 Created/updated timestamps | Exists | None |
| FR-005 Messages store | Exists | None |
| FR-006 Message unique ID + conversation FK | Exists | None |
| FR-007 Role + content + timestamp | Exists | Verify role validation |
| FR-008 Chronological retrieval | Exists (order_by created_at) | None |
| FR-009 Non-empty content | Not enforced | Add NOT NULL + min_length validation |
| FR-010 Pagination | Exists in chat_service.py | Verify offset/limit |
| FR-011 Cascade deletion | Not explicitly configured | Add cascade="all, delete-orphan" |
| FR-012 Index on user lookup | Not indexed | Add index on conversation.user_id |
| FR-013 Index on message retrieval | Not indexed | Add composite index on message(conversation_id, created_at) |
| FR-014 Coexist with Phase 2 | Already coexists | None |
| FR-015 Role validation | Partial (max_length=20) | Consider adding enum or check |

### Data Access Contracts

See [contracts/data-access.md](./contracts/data-access.md) for query patterns.

### Developer Quickstart

See [quickstart.md](./quickstart.md) for verification guide.
