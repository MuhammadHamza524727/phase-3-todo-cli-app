# Research: Backend API & Data Persistence (Spec 2)

**Feature**: Backend API & Data Persistence (Spec 2)
**Date**: 2026-01-23
**Phase**: Phase 0 - Research & Discovery

## Overview

This research document addresses all unknowns and establishes best practices for implementing the Backend API & Data Persistence feature with secure JWT-based authentication and Neon PostgreSQL data storage.

## Technology Research

### 1. FastAPI Project Structure

**Decision**: Use standard FastAPI project structure with modular organization
**Rationale**: FastAPI's recommended structure promotes separation of concerns and maintainability. Modular organization by functionality (models, api, middleware, database) follows industry best practices.
**Implementation**: Organize code in separate modules for models, API endpoints, middleware, and database connections.

### 2. SQLModel Model Design for Task Entity

**Decision**: Create Task model with proper relationships and constraints for user ownership
**Rationale**: SQLModel provides Pydantic validation with SQLAlchemy ORM capabilities, perfect for FastAPI applications. Proper relationships ensure data integrity and efficient querying.
**Design**: Task.owner_user_id as foreign key to enforce ownership, proper indexing for performance

**Alternatives considered**:
- Pure SQLAlchemy: Missing Pydantic validation benefits
- Pure Pydantic: Missing ORM capabilities

### 3. JWT Verification Middleware Implementation

**Decision**: Use python-jose library with custom middleware for JWT validation
**Rationale**: python-jose is well-maintained, supports all JWT algorithms, and integrates seamlessly with FastAPI. Custom middleware allows fine-grained control over token validation and user identity extraction.
**Implementation**: Create JWTBearer class extending HTTPBearer and custom dependency for token validation

**Alternatives considered**:
- PyJWT: Similar functionality but python-jose has better async support
- Authlib: More comprehensive but overkill for this use case

### 4. Neon PostgreSQL Connection Configuration

**Decision**: Use asyncpg driver with SQLModel for Neon Serverless PostgreSQL
**Rationale**: asyncpg provides asynchronous database operations which align well with FastAPI's async nature. It's the recommended driver for PostgreSQL in async Python applications.
**Configuration**: Set up connection pooling with appropriate settings for serverless environment

### 5. API Endpoint Design for Task Operations

**Decision**: RESTful API design with user-scoped endpoints and proper HTTP status codes
**Rationale**: RESTful design is standard for APIs and provides clear, predictable interfaces. User-scoped endpoints ensure proper authorization patterns.
**Design**: Use path parameters for user_id but enforce authorization via JWT, not client-provided values

## Security Best Practices

### 1. JWT Secret Management

**Decision**: Use environment variable for JWT secret with fallback to generated secret
**Rationale**: Environment variables provide secure external configuration that can be managed separately from code.
**Implementation**: Read from environment, generate random secret if not set

### 2. Input Validation

**Decision**: Leverage Pydantic models for automatic input validation
**Rationale**: FastAPI's integration with Pydantic provides automatic validation and serialization with clear error messages.
**Implementation**: Request/response models defined as Pydantic classes

### 3. Authorization Enforcement

**Decision**: Server-side enforcement of user data ownership using JWT-derived user ID
**Rationale**: Client-provided user IDs can be tampered with; server must always use authenticated user identity from JWT.
**Implementation**: Always use user ID extracted from JWT, not from URL parameters or request body

## Performance Considerations

### 1. Database Connection Pooling

**Decision**: Configure SQLModel with appropriate connection pool settings for Neon
**Rationale**: Connection pooling improves performance by reusing database connections, especially important for serverless environments.
**Settings**: Pool size of 5-10 connections with appropriate timeouts for serverless

### 2. Query Optimization

**Decision**: Index owner_user_id field on Task table for efficient user-based queries
**Rationale**: Proper indexing ensures fast user-scoped queries which are the primary access pattern.
**Implementation**: Add database index on owner_user_id field

## API Design Patterns

### 1. Consistent Error Handling

**Decision**: Use consistent error response format across all endpoints
**Rationale**: Consistent error responses make client-side error handling predictable and reliable.
**Implementation**: Standard error response structure with code, message, and details fields

### 2. HTTP Status Codes

**Decision**: Use appropriate HTTP status codes based on operation outcome
**Rationale**: Standard HTTP status codes communicate operation results clearly to API consumers.
**Codes**: 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 500 (Internal Server Error)

## Key Findings

1. FastAPI + SQLModel is a natural fit for this type of application with great developer experience
2. JWT token validation can be efficiently implemented with custom middleware
3. Neon Serverless PostgreSQL provides automatic scaling and connection management
4. The technology stack supports the security-first design requirements effectively
5. Proper data isolation can be achieved by filtering queries by authenticated user ID

## Next Steps

1. Create data models based on research findings
2. Define API contracts using OpenAPI specification
3. Implement JWT authentication middleware
4. Build database layer with proper isolation
5. Create API endpoints with security middleware
6. Test authentication and authorization flows