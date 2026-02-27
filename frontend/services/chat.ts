import apiClient from './api-client';
import { ChatResponse, ChatHistoryResponse, ChatMessage } from '../types';

/**
 * Send a message to the AI chatbot.
 * Returns the assistant's response with any tool call info.
 */
export const sendMessage = async (message: string): Promise<ChatResponse> => {
  const response = await apiClient.post<ChatResponse>('/api/chat', { message });
  return response.data;
};

/**
 * Retrieve conversation history for the authenticated user.
 * Returns messages in chronological order with pagination.
 */
export const getChatHistory = async (
  limit: number = 50,
  offset: number = 0
): Promise<ChatMessage[]> => {
  const response = await apiClient.get<ChatHistoryResponse>('/api/chat/history', {
    params: { limit, offset },
  });
  return response.data.data.messages;
};
