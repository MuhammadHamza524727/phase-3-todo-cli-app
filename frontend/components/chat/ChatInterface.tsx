'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { ChatMessage as ChatMessageType, ToolCall } from '../../types';
import { sendMessage, getChatHistory } from '../../services/chat';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';

interface ChatInterfaceProps {
  onToolCall?: (toolCalls: ToolCall[]) => void;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ onToolCall }) => {
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to latest message
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // Load conversation history on mount (US5: T027)
  useEffect(() => {
    const loadHistory = async () => {
      try {
        setHistoryLoading(true);
        const history = await getChatHistory();
        setMessages(history);
      } catch {
        // Silently handle — first-time users won't have history
      } finally {
        setHistoryLoading(false);
      }
    };
    loadHistory();
  }, []);

  const handleSend = async (message: string) => {
    setError(null);

    // Append user message immediately
    const userMessage: ChatMessageType = {
      id: `temp-${Date.now()}`,
      role: 'user',
      content: message,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await sendMessage(message);

      // Append assistant response
      const assistantMessage: ChatMessageType = {
        id: `resp-${Date.now()}`,
        role: 'assistant',
        content: response.data.response,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, assistantMessage]);

      // Notify parent about tool calls for task list refresh (T034)
      if (response.data.tool_calls?.length > 0 && onToolCall) {
        onToolCall(response.data.tool_calls);
      }
    } catch (err: unknown) {
      // Handle specific error types (T029, T032)
      const axiosError = err as { response?: { status?: number } };
      if (axiosError?.response?.status === 401) {
        setError('Session expired. Please log in again.');
        return;
      }

      const errorMessage =
        axiosError?.response?.status === 500
          ? 'Chatbot temporarily unavailable. Please try again.'
          : 'Failed to send message. Please try again.';

      // Show error as assistant message
      const errorMsg: ChatMessageType = {
        id: `err-${Date.now()}`,
        role: 'assistant',
        content: errorMessage,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMsg]);
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center gap-2 px-4 py-3 border-b border-white/10 bg-white/5">
        <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
        <span className="text-sm font-semibold text-indigo-200">Task Assistant</span>
      </div>

      {/* Messages area */}
      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-1">
        {historyLoading ? (
          <div className="flex items-center justify-center h-full">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-violet-400" />
          </div>
        ) : messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-center">
            <div className="space-y-2 text-indigo-300/60">
              <p className="text-lg font-medium">Hi! I'm your task assistant.</p>
              <p className="text-sm">Try saying "Add a task to buy groceries" or "Show my tasks"</p>
            </div>
          </div>
        ) : (
          messages.map((msg) => <ChatMessage key={msg.id} message={msg} />)
        )}

        {isLoading && (
          <div className="flex justify-start mb-3">
            <div className="bg-white/10 border border-white/10 rounded-2xl rounded-bl-md px-4 py-3">
              <div className="flex gap-1">
                <div className="w-2 h-2 rounded-full bg-violet-400 animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-2 h-2 rounded-full bg-violet-400 animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-2 h-2 rounded-full bg-violet-400 animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Error banner */}
      {error && (
        <div className="px-4 py-2 bg-red-900/30 border-t border-red-500/20">
          <p className="text-xs text-red-300">{error}</p>
        </div>
      )}

      {/* Input */}
      <ChatInput onSend={handleSend} isLoading={isLoading} />
    </div>
  );
};

export default ChatInterface;
