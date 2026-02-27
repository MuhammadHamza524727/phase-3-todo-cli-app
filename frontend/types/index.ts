// User interface representing an authenticated individual
export interface User {
  id: string;                // unique identifier from backend
  email: string;             // user's email address
  createdAt: string;         // account creation timestamp
  updatedAt: string;         // last account update timestamp
}

// Task interface representing a user's personal task
export interface Task {
  id: string;                // unique identifier from backend
  title: string;             // task title/description
  description?: string;      // optional detailed description
  completed: boolean;        // completion status
  userId: string;            // foreign key linking to User
  createdAt: string;         // task creation timestamp
  updatedAt: string;         // last task update timestamp
}

// Authentication Token interface
export interface AuthToken {
  accessToken: string;       // JWT token for API authentication
  refreshToken?: string;     // token for refreshing access token
  expiresAt: string;         // expiration timestamp for access token
}

// Auth state interface
export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

// Chat message interface
export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

// Tool call info from AI agent
export interface ToolCall {
  tool: string;
  arguments: Record<string, unknown>;
  result: Record<string, unknown> | null;
}

// Chat API response
export interface ChatResponse {
  success: boolean;
  data: {
    response: string;
    conversation_id: string;
    tool_calls: ToolCall[];
  };
}

// Chat history API response
export interface ChatHistoryResponse {
  success: boolean;
  data: {
    conversation_id: string | null;
    messages: ChatMessage[];
    total: number;
    limit: number;
    offset: number;
  };
}