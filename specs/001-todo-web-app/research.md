# Research: Todo Full-Stack Web Application

**Feature**: Todo Full-Stack Web Application
**Date**: 2026-01-23
**Phase**: Phase 0 - Research & Discovery

## Overview

This research document addresses all unknowns and establishes best practices for implementing the Todo Full-Stack Web Application with secure JWT-based authentication.

## Technology Research

### 1. Better Auth Integration with Next.js 16+ App Router

**Decision**: Use Better Auth client-side session management with Next.js App Router
**Rationale**: Better Auth provides seamless integration with Next.js App Router through its React hooks and middleware. It handles JWT token storage securely and provides automatic session refresh mechanisms.
**Implementation**: Use `@better-auth/react` for client-side session management and `@better-auth/next-js` for server-side middleware if needed.

**Alternatives considered**:
- Custom JWT implementation: More complex and error-prone
- NextAuth.js: Good alternative but Better Auth offers more direct JWT support

### 2. JWT Configuration for Better Auth

**Decision**: Configure Better Auth to issue JWT tokens with 24-hour expiration
**Rationale**: 24-hour expiration provides a good balance between security (short-lived tokens) and user experience (not requiring frequent re-authentication).
**Configuration**: Set `session.expiresIn: 24 * 60 * 60` (24 hours in seconds) and enable JWT plugin

**Alternatives considered**:
- Longer expiration (7 days): Less secure but better UX
- Shorter expiration (1 hour): More secure but requires frequent re-auth

### 3. FastAPI JWT Middleware Implementation

**Decision**: Use python-jose library with custom middleware for JWT validation
**Rationale**: python-jose is well-maintained, supports all JWT algorithms, and integrates seamlessly with FastAPI. Custom middleware allows fine-grained control over token validation and user identity extraction.
**Implementation**: Create JWTBearer class extending HTTPBearer and custom dependency for token validation

**Alternatives considered**:
- PyJWT: Similar functionality but python-jose has better async support
- Authlib: More comprehensive but overkill for this use case

### 4. SQLModel Model Design for User and Task

**Decision**: Create User and Task models with proper relationships and constraints
**Rationale**: SQLModel provides Pydantic validation with SQLAlchemy ORM capabilities, perfect for FastAPI applications. Proper relationships ensure data integrity and efficient querying.
**Design**: User.id as foreign key in Task model with proper indexing for performance

**Alternatives considered**:
- Pure SQLAlchemy: Missing Pydantic validation benefits
- Pure Pydantic: Missing ORM capabilities
- Tortoise ORM: Good for async but SQLModel better fits FastAPI ecosystem

### 5. Frontend API Client Implementation

**Decision**: Create centralized API client service that automatically attaches JWT tokens
**Rationale**: Centralized service ensures consistent authentication header handling across all API calls and simplifies error handling.
**Implementation**: Axios interceptors or fetch wrapper that reads JWT from Better Auth session and attaches to Authorization header

**Alternatives considered**:
- Manual header attachment: Error-prone and inconsistent
- React Query / SWR providers: More complex for simple use case

## Security Best Practices

### 1. JWT Secret Management

**Decision**: Use environment variable for JWT secret with fallback to generated secret
**Rationale**: Environment variables provide secure external configuration that can be managed separately from code.
**Implementation**: Read `BETTER_AUTH_SECRET` from environment, generate random secret if not set

### 2. Rate Limiting

**Decision**: Implement basic rate limiting for authentication endpoints
**Rationale**: Prevents brute-force attacks on login endpoints while keeping implementation simple.
**Implementation**: Use slowapi library with FastAPI

### 3. Input Validation

**Decision**: Leverage Pydantic models for automatic input validation
**Rationale**: FastAPI's integration with Pydantic provides automatic validation and serialization with clear error messages.
**Implementation**: Request/response models defined as Pydantic classes

## Performance Considerations

### 1. Database Connection Pooling

**Decision**: Configure SQLModel with appropriate connection pool settings
**Rationale**: Connection pooling improves performance by reusing database connections.
**Settings**: Pool size of 5-10 connections with appropriate timeouts

### 2. API Response Optimization

**Decision**: Implement pagination for task listing endpoints
**Rationale**: Prevents performance issues with large numbers of tasks per user.
**Implementation**: Limit to 50 tasks per page by default with offset/limit parameters

## Deployment Architecture

### 1. Separate Services

**Decision**: Deploy frontend and backend as separate services
**Rationale**: Enables independent scaling, easier maintenance, and aligns with separation of concerns principle.
**Implementation**: Backend deployed with containerization, frontend to static hosting or Node.js server

### 2. Environment Configuration

**Decision**: Use environment variables for all configuration
**Rationale**: Provides flexibility across environments while keeping secrets secure.
**Variables**: DATABASE_URL, BETTER_AUTH_SECRET, FRONTEND_URL, BACKEND_URL

## Key Findings

1. Better Auth has excellent Next.js 16+ App Router support with minimal configuration
2. FastAPI + SQLModel is a natural fit for this type of application with great developer experience
3. JWT token validation can be efficiently implemented with custom middleware
4. Neon Serverless PostgreSQL provides automatic scaling and connection pooling
5. The technology stack supports the security-first design requirements effectively

## Next Steps

1. Create data models based on research findings
2. Define API contracts using OpenAPI specification
3. Implement authentication flow
4. Build database layer with proper isolation
5. Create API endpoints with security middleware
6. Integrate frontend with backend services