'use client';

import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Box, AlertCircle } from 'lucide-react';
import { MessageActions } from './MessageActions';
import { SourceCitation } from './SourceCitation';
import { markdownComponents } from './markdownComponents';
import { ChatLoadingIndicator } from './ChatLoadingIndicator';
import { formatTimestamp } from '@/lib/chat/chatUtils';
import type { ChatMessage as ChatMessageType } from '@/types/chat';

interface ChatMessageProps {
  message: ChatMessageType;
  conversationId: string;
  isLast: boolean;
  onRegenerate: () => void;
  onFeedback: (messageId: string, value: 'up' | 'down' | null) => void;
}

export function ChatMessage({
  message,
  conversationId,
  isLast,
  onRegenerate,
  onFeedback,
}: ChatMessageProps) {
  const isUser = message.role === 'user';
  const isPending = message.status === 'pending';
  const isError = message.status === 'error';

  if (isUser) {
    return (
      <div className="flex justify-end px-4 py-1.5">
        <div className="max-w-[75%]">
          <div className="rounded-2xl rounded-br-sm bg-[#1B3A58] px-4 py-3 text-sm leading-relaxed text-[#F8FAFC]">
            {message.content}
          </div>
          <p className="mt-1 text-right text-[10px] text-[#94A3B8]/50">
            {formatTimestamp(message.timestamp)}
          </p>
        </div>
      </div>
    );
  }

  // Assistant message
  return (
    <div className="flex gap-3 px-4 py-1.5">
      {/* Avatar */}
      <div className="mt-0.5 flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-lg bg-[#38BDF8] text-[#081426]">
        <Box size={14} strokeWidth={2.5} aria-hidden="true" />
      </div>

      <div className="min-w-0 flex-1">
        {isPending ? (
          <ChatLoadingIndicator />
        ) : isError ? (
          <div className="flex items-center gap-2 rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-400">
            <AlertCircle size={15} className="flex-shrink-0" aria-hidden="true" />
            {message.content}
          </div>
        ) : (
          <>
            {/* Mock badge */}
            {message.isMock && (
              <p className="mb-1.5 text-[10px] font-medium text-[#94A3B8]/50">
                Demo response · Not from real company documentation
              </p>
            )}

            {/* Rendered Markdown */}
            <div
              className="prose-chat text-sm leading-relaxed text-[#F8FAFC]"
              aria-live="polite"
              aria-atomic="false"
            >
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={markdownComponents}
              >
                {message.content}
              </ReactMarkdown>
            </div>

            {/* Sources */}
            {message.sources && message.sources.length > 0 && (
              <SourceCitation sources={message.sources} />
            )}

            {/* Actions row */}
            {isLast && (
              <MessageActions
                content={message.content}
                conversationId={conversationId}
                messageId={message.id}
                feedback={message.feedback}
                onRegenerate={onRegenerate}
                onFeedback={(value) => onFeedback(message.id, value)}
              />
            )}

            {/* Timestamp */}
            <p className="mt-1 text-[10px] text-[#94A3B8]/50">
              {formatTimestamp(message.timestamp)}
            </p>
          </>
        )}
      </div>
    </div>
  );
}
