<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.1.0
- Modified principles: [PRINCIPLE_1_NAME] → Spec-Driven Development, [PRINCIPLE_2_NAME] → Security-First Design, [PRINCIPLE_3_NAME] → Deterministic Behavior, [PRINCIPLE_4_NAME] → Separation of Concerns, [PRINCIPLE_5_NAME] → Zero Manual Coding
- Added sections: Architecture Standards, Security Standards, Development Constraints, Quality Constraints, Testing & Validation Requirements, Documentation Standards, Success Criteria
- Removed sections: None
- Templates requiring updates: .specify/templates/plan-template.md (⚠ pending), .specify/templates/spec-template.md (⚠ pending), .specify/templates/tasks-template.md (⚠ pending)
- Follow-up TODOs: None
-->
# Todo Full-Stack Web Application Constitution

## Core Principles

### Spec-Driven Development
No implementation without an approved spec. Every feature must trace back to a written spec. All changes must follow: Spec → Plan → Tasks → Implement.

### Security-First Design
Authentication, authorization, and data isolation are paramount. All protected endpoints require a valid JWT. Requests without JWT return 401 Unauthorized. User data isolation is mandatory (no cross-user data access).

### Deterministic Behavior
Predictable, testable API and UI flows. All API behavior must match the defined REST contract exactly. API responses must be consistent and typed. Meaningful HTTP status codes for all API responses.

### Separation of Concerns
Authentication, backend, and frontend clearly isolated. No shared session state between frontend and backend. JWT verification must be stateless and backend-controlled.

### Zero Manual Coding
All implementation via Claude Code. No manual code edits allowed. No feature creep beyond defined requirements.

### JWT-Based Authentication
JWT signature must be verified using shared secret. JWT expiration must be respected. Task ownership must be enforced at query level. Backend must not trust client-provided user IDs blindly.

## Architecture Standards
Frontend: Next.js 16+ (App Router), Backend: Python FastAPI, ORM: SQLModel, Database: Neon Serverless PostgreSQL, Authentication: Better Auth (JWT-based), Communication: RESTful APIs with JSON, Authorization: Bearer JWT via Authorization header.

## Security Standards
All protected endpoints require a valid JWT. Requests without JWT return 401 Unauthorized. JWT signature must be verified using shared secret. JWT expiration must be respected. Task ownership must be enforced at query level. Backend must not trust client-provided user IDs blindly.

## Development Constraints
No manual code edits allowed. All changes must follow: Spec → Plan → Tasks → Implement. No feature creep beyond defined requirements. No shared session state between frontend and backend. All configuration via environment variables. All errors must return structured JSON responses.

## Quality Constraints
API responses must be consistent and typed. Frontend must be responsive (mobile-first). Clear loading, error, and empty states in UI. Meaningful HTTP status codes for all API responses. Database schema must support future extensibility.

## Testing & Validation Requirements
Manual test scenarios must be defined in specs. Auth flow must be tested end-to-end. Multi-user isolation must be validated. Token expiry behavior must be verifiable. CRUD operations must be validated per user.

## Documentation Standards
Specs must be human-readable and unambiguous. API endpoints must be clearly documented. Auth flow must be diagrammable from spec alone. Environment variables must be explicitly listed. Assumptions must be stated explicitly.

## Success Criteria
Users can signup and signin successfully. Authenticated users receive valid JWTs. JWT-secured API accepts only authorized requests. Each user can only access their own tasks. All CRUD task operations function correctly. Data persists in Neon PostgreSQL across sessions. Frontend and backend operate independently but securely. Project passes hackathon review for architecture, security, and process.

## Governance
Constitution supersedes all other practices. Amendments require documentation, approval, and migration plan. All PRs/reviews must verify compliance. Complexity must be justified. Environment-based secrets management (no hardcoded secrets). Use development guidance for runtime development guidance.

**Version**: 1.1.0 | **Ratified**: 2026-01-23 | **Last Amended**: 2026-01-23
