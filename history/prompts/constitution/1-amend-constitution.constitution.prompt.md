---
id: 1
title: Amend Constitution
stage: constitution
date: 2026-01-23
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: sp.constitution
labels: [constitution, todo-app, full-stack, web-application]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

Project: Todo Full-Stack Web Application

Objective:
Transform a basic console-based todo application into a modern, secure, multi-user full-stack web application using a strictly spec-driven, agentic development workflow.

Core principles:

- Spec-driven development (no implementation without an approved spec)
- Security-first design (authentication, authorization, data isolation)
- Deterministic behavior (predictable, testable API and UI flows)
- Separation of concerns (auth, backend, frontend clearly isolated)
- Zero manual coding (all implementation via Claude Code)

Key standards:

- Every feature must trace back to a written spec
- All API behavior must match the defined REST contract exactly
- Authentication must be enforced on every protected route
- User data isolation is mandatory (no cross-user data access)
- JWT verification must be stateless and backend-controlled
- Environment-based secrets management (no hardcoded secrets)

Architecture standards:

- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT-based)
- Communication: RESTful APIs with JSON
- Authorization: Bearer JWT via Authorization header

Security standards:

- All protected endpoints require a valid JWT
- Requests without JWT return 401 Unauthorized
- JWT signature must be verified using shared secret
- JWT expiration must be respected
- Task ownership must be enforced at query level
- Backend must not trust client-provided user IDs blindly

Development constraints:

- No manual code edits allowed
- All changes must follow: Spec → Plan → Tasks → Implement
- No feature creep beyond defined requirements
- No shared session state between frontend and backend
- All configuration via environment variables
- All errors must return structured JSON responses

Quality constraints:

- API responses must be consistent and typed
- Frontend must be responsive (mobile-first)
- Clear loading, error, and empty states in UI
- Meaningful HTTP status codes for all API responses
- Database schema must support future extensibility

Testing & validation requirements:

- Manual test scenarios must be defined in specs
- Auth flow must be tested end-to-end
- Multi-user isolation must be validated
- Token expiry behavior must be verifiable
- CRUD operations must be validated per user

Documentation standards:

- Specs must be human-readable and unambiguous
- API endpoints must be clearly documented
- Auth flow must be diagrammable from spec alone
- Environment variables must be explicitly listed
- Assumptions must be stated explicitly

Success criteria:

- Users can signup and signin successfully
- Authenticated users receive valid JWTs
- JWT-secured API accepts only authorized requests
- Each user can only access their own tasks
- All CRUD task operations function correctly
- Data persists in Neon PostgreSQL across sessions
- Frontend and backend operate independently but securely
- Project passes hackathon review for architecture, security, and process

## Response snapshot

I've successfully updated the project constitution based on your requirements. The constitution file (.specify/memory/constitution.md) has been updated with the specific details for the Todo Full-Stack Web Application project, including:

1. Core principles:
   - Spec-Driven Development
   - Security-First Design
   - Deterministic Behavior
   - Separation of Concerns
   - Zero Manual Coding
   - JWT-Based Authentication

2. Additional sections:
   - Architecture Standards
   - Security Standards
   - Development Constraints
   - Quality Constraints
   - Testing & Validation Requirements
   - Documentation Standards
   - Success Criteria

3. Governance section with versioning information

The version has been updated from 1.0.0 to 1.1.0 to reflect the addition of new principles and sections. The file now properly represents the requirements for the todo CLI app transformation into a full-stack web application with authentication and authorization.

## Outcome

- ✅ Impact: Updated project constitution with specific principles and standards for the Todo Full-Stack Web Application
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with new principles and requirements
- 🔁 Next prompts: Ready to proceed with spec creation based on the updated constitution
- 🧠 Reflection: The constitution now clearly defines the project's core principles and requirements, providing a solid foundation for spec-driven development.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): Begin spec creation based on the updated constitution