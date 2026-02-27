'use client';

import React from 'react';
import { ChatMessage as ChatMessageType } from '../../types';

interface ChatMessageProps {
  message: ChatMessageType;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-3`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap ${
          isUser
            ? 'bg-gradient-to-r from-violet-600 to-purple-600 text-white rounded-br-md'
            : 'bg-white/10 text-indigo-100 border border-white/10 rounded-bl-md'
        }`}
      >
        {message.content}
      </div>
    </div>
  );
};

export default ChatMessage;
