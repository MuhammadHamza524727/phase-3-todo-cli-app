# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a full-stack todo web application with secure multi-user authentication using JWT tokens. The application consists of a Next.js 16+ frontend with App Router and a FastAPI backend with SQLModel ORM connected to Neon Serverless PostgreSQL. Better Auth handles user registration/login and JWT token issuance, while the backend enforces user data isolation by validating JWT tokens and restricting access to user-owned tasks only.

## Technical Context

**Language/Version**: Python 3.11 (Backend/FastAPI), JavaScript/TypeScript (Frontend/Next.js 16+)
**Primary Dependencies**: Next.js 16+ (App Router), FastAPI, SQLModel, Better Auth, Neon Serverless PostgreSQL
**Storage**: Neon Serverless PostgreSQL database with SQLModel ORM
**Testing**: pytest (Backend), Jest/Cypress (Frontend)
**Target Platform**: Web application (Responsive - Desktop/Mobile browsers)
**Project Type**: Web (Full-stack with separate frontend and backend services)
**Performance Goals**: <2 second API response time, 95% uptime, Mobile-responsive UI
**Constraints**: No manual coding allowed (Claude Code only), JWT-based authentication, Data isolation between users
**Scale/Scope**: Multi-user support, Individual task ownership, Production-ready security

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Verification

**Spec-Driven Development**: ✅ All changes follow Spec → Plan → Tasks → Implement workflow
- Plan is based on approved feature specification (specs/001-todo-web-app/spec.md)
- No implementation without approved spec

**Security-First Design**: ✅ All security requirements addressed
- JWT-based authentication implemented via Better Auth
- Protected endpoints require valid JWT tokens
- 401 Unauthorized responses for unauthenticated requests
- User data isolation enforced at query level through user_id foreign key constraint

**Deterministic Behavior**: ✅ All behavior is predictable and testable
- REST API contracts clearly defined in OpenAPI specification
- Consistent HTTP status codes used (200, 201, 204, 400, 401, 403, 404, 500)
- Typed API responses with consistent structure

**Separation of Concerns**: ✅ Proper architectural separation
- Frontend (Next.js) and backend (FastAPI) operate independently
- No shared session state between frontend and backend
- JWT verification is stateless and backend-controlled
- Clear API boundaries defined in contracts/api-contract.yaml

**Zero Manual Coding**: ✅ All implementation via Claude Code
- No manual code edits allowed
- All development through Claude Code commands
- Automated project structure generation

**JWT-Based Authentication**: ✅ Authentication requirements met
- JWT signature verification using shared secret (BETTER_AUTH_SECRET)
- Token expiration respected (24-hour default)
- Task ownership enforced at query level via user_id filtering
- Backend does not trust client-provided user IDs blindly - extracts from JWT

**Architecture Standards**: ✅ Technology stack compliance
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT-based)
- Communication: RESTful APIs with JSON
- Authorization: Bearer JWT via Authorization header

**Security Standards**: ✅ Security requirements satisfied
- All protected endpoints require valid JWT
- Requests without JWT return 401 Unauthorized
- JWT signature verified using shared secret
- JWT expiration respected
- Task ownership enforced at query level via user_id foreign key
- Backend does not trust client-provided user IDs blindly - validates against JWT claims

### Post-Design Verification

**Data Model Alignment**: ✅ Data models match functional requirements
- User entity supports registration/login requirements (FR-001, FR-002)
- Task entity supports CRUD operations (FR-005-008)
- User ID foreign key enforces data isolation (FR-009)

**API Contract Alignment**: ✅ API contracts satisfy requirements
- Authentication endpoints support JWT issuance (FR-002, FR-003)
- Task endpoints enforce user-based access controls (FR-009)
- Proper HTTP status codes implemented (FR-012)
- Token expiration handling defined (FR-013)

**Architecture Validation**: ✅ Architecture meets constraints
- Full-stack separation maintained (Frontend/Backend directories)
- JWT-based authentication implemented
- Neon PostgreSQL database utilized
- No manual coding - all automated through Claude Code

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-web-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── jwt_auth.py
│   └── database/
│       ├── __init__.py
│       └── connection.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
├── requirements.txt
├── main.py
└── alembic/
    └── versions/

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── auth/
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── signup/
│   │   │       └── page.tsx
│   │   └── todos/
│   │       ├── page.tsx
│   │       └── [id]/
│   │           └── page.tsx
│   ├── components/
│   │   ├── Auth/
│   │   │   ├── LoginForm.tsx
│   │   │   └── SignupForm.tsx
│   │   ├── Todo/
│   │   │   ├── TodoList.tsx
│   │   │   ├── TodoItem.tsx
│   │   │   └── TodoForm.tsx
│   │   └── UI/
│   │       ├── Button.tsx
│   │       └── Input.tsx
│   ├── services/
│   │   ├── api.ts
│   │   └── auth.ts
│   └── lib/
│       └── utils.ts
├── public/
├── styles/
├── package.json
├── tsconfig.json
└── next.config.js

.env
docker-compose.yml
README.md
```

**Structure Decision**: Web application with separate frontend and backend services as required by the architecture standards. The frontend uses Next.js 16+ with App Router and the backend uses FastAPI with SQLModel ORM connecting to Neon Serverless PostgreSQL. This structure supports the separation of concerns principle and allows independent scaling of frontend and backend services.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
