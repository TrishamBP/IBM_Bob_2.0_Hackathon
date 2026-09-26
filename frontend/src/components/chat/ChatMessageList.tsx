'use client';

import { useEffect, useRef } from 'react';
import { ChatMessage } from './ChatMessage';
import type { Conversation } from '@/types/chat';

interface ChatMessageListProps {
  conversation: Conversation;
  isLoading: boolean;
  onRegenerate: () => void;
  onFeedback: (messageId: string, value: 'up' | 'down' | null) => void;
}

export function ChatMessageList({
  conversation,
  onRegenerate,
  onFeedback,
}: ChatMessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom whenever messages change
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [conversation.messages]);

  const lastAssistantIdx = conversation.messages
    .map((m, i) => (m.role === 'assistant' ? i : -1))
    .filter((i) => i !== -1)
    .at(-1) ?? -1;

  return (
    <div
      className="flex flex-col gap-2 py-6"
      role="log"
      aria-label="Conversation messages"
      aria-live="polite"
      aria-relevant="additions"
    >
      {conversation.messages.map((message, idx) => (
        <ChatMessage
          key={message.id}
          message={message}
          conversationId={conversation.id}
          isLast={idx === lastAssistantIdx}
          onRegenerate={onRegenerate}
          onFeedback={onFeedback}
        />
      ))}
      {/* Scroll anchor */}
      <div ref={bottomRef} aria-hidden="true" />
    </div>
  );
}
