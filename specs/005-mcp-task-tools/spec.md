# Feature Specification: MCP Server Tools for Task Management

**Feature Branch**: `005-mcp-task-tools`
**Created**: 2026-02-21
**Status**: Draft
**Input**: User description: "Generate Spec-Kit Plus SPEC for Spec-5: api/mcp-tools.md — MCP server tools: add_task, list_tasks, complete_task, delete_task, update_task. Input/Output JSON structure for each tool. Stateless API behavior. Reference Phase 2 task table."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - AI Agent Creates a Task via MCP Tool (Priority: P1)

An AI agent receives a user's natural language request to create a task. The agent invokes the `add_task` MCP tool with the extracted title and optional description. The tool creates the task in the database scoped to the authenticated user and returns a structured JSON confirmation with the new task's details.

**Why this priority**: Task creation is the most fundamental operation. Without it, the AI agent cannot add any tasks for the user.

**Independent Test**: Can be fully tested by invoking the `add_task` tool with a title string and verifying the tool returns a success JSON with the created task's ID, title, and confirmation message.

**Acceptance Scenarios**:

1. **Given** a valid user context and title "Buy groceries", **When** the `add_task` tool is invoked, **Then** it returns a success JSON containing the new task ID, title "Buy groceries", and a confirmation message
2. **Given** a valid user context and title with optional description, **When** the `add_task` tool is invoked, **Then** both title and description are persisted and returned in the response
3. **Given** an empty title, **When** the `add_task` tool is invoked, **Then** it returns an error JSON indicating the title is required

---

### User Story 2 - AI Agent Lists User's Tasks via MCP Tool (Priority: P1)

An AI agent invokes the `list_tasks` MCP tool to retrieve the authenticated user's tasks. The tool returns a structured JSON list of tasks with their titles, completion status, and IDs. The tool supports optional filtering by completion status.

**Why this priority**: Listing tasks is essential for the agent to identify specific tasks before performing update, complete, or delete operations.

**Independent Test**: Can be fully tested by creating several tasks, invoking `list_tasks`, and verifying the response contains all user-owned tasks in a structured JSON format.

**Acceptance Scenarios**:

1. **Given** user has 3 tasks, **When** `list_tasks` is invoked with no filter, **Then** it returns a JSON array of all 3 tasks with ID, title, and completion status
2. **Given** user has both completed and pending tasks, **When** `list_tasks` is invoked with a completed filter, **Then** it returns only tasks matching the filter
3. **Given** user has no tasks, **When** `list_tasks` is invoked, **Then** it returns an empty result with a count of 0 and a helpful message

---

### User Story 3 - AI Agent Completes a Task via MCP Tool (Priority: P2)

An AI agent invokes the `complete_task` MCP tool to mark a specific task as completed. The tool accepts a task ID, toggles the completion status, and returns a structured JSON confirmation showing the updated task state.

**Why this priority**: Completing tasks is a core lifecycle operation that users expect from natural language task management.

**Independent Test**: Can be fully tested by creating a pending task, invoking `complete_task` with its ID, and verifying the response confirms the task is now marked as completed.

**Acceptance Scenarios**:

1. **Given** a pending task exists, **When** `complete_task` is invoked with its ID, **Then** it returns a success JSON confirming the task is now completed
2. **Given** a task ID that does not belong to the user, **When** `complete_task` is invoked, **Then** it returns an error JSON indicating the task was not found
3. **Given** a task that is already completed, **When** `complete_task` is invoked, **Then** it toggles the task back to pending and returns the updated status

---

### User Story 4 - AI Agent Updates a Task via MCP Tool (Priority: P2)

An AI agent invokes the `update_task` MCP tool to modify a task's title, description, or completion status. The tool accepts a task ID and the fields to update, then returns a structured JSON confirmation showing the changes made.

**Why this priority**: Updating tasks allows users to refine their task descriptions and correct mistakes through natural language.

**Independent Test**: Can be fully tested by creating a task, invoking `update_task` with a new title, and verifying the response confirms the title change.

**Acceptance Scenarios**:

1. **Given** a task exists, **When** `update_task` is invoked with a new title, **Then** it returns a success JSON confirming the title was changed with old and new values
2. **Given** a task exists, **When** `update_task` is invoked with multiple fields (title + description), **Then** all specified fields are updated and confirmed
3. **Given** a nonexistent task ID, **When** `update_task` is invoked, **Then** it returns an error JSON indicating the task was not found

---

### User Story 5 - AI Agent Deletes a Task via MCP Tool (Priority: P2)

An AI agent invokes the `delete_task` MCP tool to permanently remove a task. The tool accepts a task ID, deletes the task from the database, and returns a structured JSON confirmation including the deleted task's title.

**Why this priority**: Deletion completes the full CRUD lifecycle, allowing users to clean up their task list.

**Independent Test**: Can be fully tested by creating a task, invoking `delete_task` with its ID, and verifying the response confirms deletion with the specific task title.

**Acceptance Scenarios**:

1. **Given** a task exists, **When** `delete_task` is invoked with its ID, **Then** it returns a success JSON confirming deletion and including the deleted task's title
2. **Given** a nonexistent task ID, **When** `delete_task` is invoked, **Then** it returns an error JSON indicating the task was not found
3. **Given** a task belonging to another user, **When** `delete_task` is invoked, **Then** it returns a "not found" error (does not reveal existence of other users' tasks)

---

### Edge Cases

- What happens when a tool receives a malformed task ID? The tool should return a clear error JSON indicating the ID format is invalid.
- How does the system handle concurrent modifications to the same task? The tool should use the latest database state; no optimistic locking required.
- What happens when the database is temporarily unavailable? The tool should return a structured error JSON indicating a service failure.
- How does the system handle very long title strings (>200 characters)? The tool should reject and return a validation error.
- What happens when `update_task` is called with no fields to change? The tool should return a success response indicating no changes were needed.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST define exactly 5 MCP tools: `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`
- **FR-002**: Each tool MUST accept a user context (authenticated user identity) that is injected by the calling service, not provided by the AI agent
- **FR-003**: Each tool MUST scope all database operations to the authenticated user only — no cross-user data access
- **FR-004**: Each tool MUST return a structured JSON response containing a `status` field ("success" or "error") and a human-readable `message` field
- **FR-005**: The `add_task` tool MUST accept a required `title` (1-200 characters) and optional `description` (max 1000 characters), create the task, and return the created task's ID, title, and confirmation message
- **FR-006**: The `list_tasks` tool MUST accept an optional `completed` filter (boolean) and return an array of tasks with index, ID, title, status, and description
- **FR-007**: The `complete_task` tool MUST accept a `task_id`, toggle the task's completion status, and return the updated task state with a confirmation message
- **FR-008**: The `update_task` tool MUST accept a `task_id` and optional fields (`title`, `description`, `completed`) and return a confirmation listing the specific changes made
- **FR-009**: The `delete_task` tool MUST accept a `task_id`, permanently remove the task, and return a confirmation including the deleted task's title
- **FR-010**: All tools MUST validate input parameters and return descriptive error messages for invalid inputs (missing required fields, invalid IDs, values exceeding limits)
- **FR-011**: All tools MUST return a "Task not found" error when the task ID does not exist or does not belong to the authenticated user
- **FR-012**: All tool operations MUST be stateless — no shared state between invocations; each call operates independently against the database
- **FR-013**: All tools MUST operate against the existing task table defined in Spec 002 (Phase 2) — no new task tables or schema changes
- **FR-014**: Each tool MUST include a clear, descriptive docstring that the AI agent can use to determine when to invoke it

### Tool Input/Output Contracts

**`add_task`**:
- Input: `title` (string, required), `description` (string, optional)
- Success output: `{ "status": "success", "task_id": "<uuid>", "title": "<title>", "message": "Task '<title>' created successfully." }`
- Error output: `{ "status": "error", "message": "<error description>" }`

**`list_tasks`**:
- Input: `completed` (boolean, optional)
- Success output: `{ "status": "success", "count": <int>, "tasks": [{"index": <int>, "id": "<uuid>", "title": "<title>", "status": "pending|completed", "description": "<desc>"}] }`
- Empty output: `{ "status": "empty", "count": 0, "message": "You don't have any tasks yet. Try saying 'Add a task to...'" }`

**`complete_task`**:
- Input: `task_id` (string, required)
- Success output: `{ "status": "success", "task_id": "<uuid>", "title": "<title>", "completed": true|false, "message": "Task '<title>' marked as completed|pending." }`
- Error output: `{ "status": "error", "message": "Task not found." }`

**`update_task`**:
- Input: `task_id` (string, required), `title` (string, optional), `description` (string, optional), `completed` (boolean, optional)
- Success output: `{ "status": "success", "task_id": "<uuid>", "title": "<title>", "changes": ["<change1>", "<change2>"], "message": "Task '<title>' updated: <changes>." }`
- Error output: `{ "status": "error", "message": "Task not found." }`

**`delete_task`**:
- Input: `task_id` (string, required)
- Success output: `{ "status": "success", "deleted_title": "<title>", "message": "Task '<title>' has been deleted." }`
- Error output: `{ "status": "error", "message": "Task not found." }`

### Key Entities

- **Task** *(reference — defined in Spec 002)*: The target entity for all tool operations. Fields: id (UUID), title (string 1-200), description (string optional, max 1000), completed (boolean), owner_user_id (UUID FK→User), due_date (datetime optional), created_at, updated_at
- **User Context**: The authenticated user identity injected into each tool invocation by the chat service. Contains user_id and a database session. Not provided by the AI agent.
- **MCP Tool**: A structured function callable by the AI agent framework. Each tool has a name, description (docstring), typed input parameters, and a JSON string output.

## Assumptions

- The existing Task model and database table from Spec 002 are operational and unchanged
- Tools are invoked by the chat service (Spec 004) which handles JWT authentication and provides the user context
- Tools do not handle authentication directly — the calling service ensures the user is authenticated before invoking any tool
- Tools return JSON strings (not dictionaries) because the AI agent framework expects string outputs from function tools
- The `complete_task` tool toggles completion (if completed, sets to pending; if pending, sets to completed)
- The AI agent determines which tool to call based on the tool docstrings — tools must have clear, descriptive documentation
- One user context is shared across all tool calls within a single chat request

## Dependencies

- **Spec 002 (Backend API & Data Persistence)**: Provides the Task model, database schema, and SQLModel ORM layer
- **Spec 004 (AI Chatbot)**: Provides the chat service that invokes these tools with authenticated user context
- **OpenAI Agents SDK**: Provides the `@function_tool` decorator and `RunContextWrapper` for context injection

## Out of Scope

- Tool authentication (handled by the calling chat service in Spec 004)
- Tool discovery or registration protocol (tools are statically defined and registered with the agent)
- Batch operations (creating, updating, or deleting multiple tasks in one tool call)
- Task filtering beyond completion status (no search by title, date range, or priority)
- Task subtasks, tags, or categories
- Undo/redo operations
- Tool versioning or backward compatibility

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 5 tools (add_task, list_tasks, complete_task, delete_task, update_task) are callable by the AI agent and return valid JSON responses for 100% of valid inputs
- **SC-002**: All tools enforce user data isolation — 100% of operations are scoped to the authenticated user
- **SC-003**: All tools return descriptive error messages for invalid inputs — no silent failures or unstructured errors
- **SC-004**: The `add_task` tool creates a task and returns confirmation within 2 seconds
- **SC-005**: The `list_tasks` tool returns up to 100 tasks within 2 seconds
- **SC-006**: All tool responses follow the documented JSON contract structure with `status` and `message` fields
- **SC-007**: The `delete_task` tool returns the deleted task's title in the confirmation (not a generic success message)
- **SC-008**: The `update_task` tool lists specific changes made (not a generic "task updated" message)
- **SC-009**: All tools operate statelessly — no shared in-memory state between invocations
- **SC-010**: All tools operate against the existing Phase 2 task table — no new database tables required for tool operations
