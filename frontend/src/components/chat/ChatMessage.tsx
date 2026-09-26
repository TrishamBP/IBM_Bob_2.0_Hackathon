'use client';

import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Box, AlertCircle } from 'lucide-react';
import { MessageActions } from './MessageActions';
import { SourceCitation } from './SourceCitation';
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
                components={{
                  // Headings
                  h1: ({ children }) => (
                    <h1 className="mb-3 mt-4 text-lg font-bold text-[#F8FAFC] first:mt-0">{children}</h1>
                  ),
                  h2: ({ children }) => (
                    <h2 className="mb-2 mt-4 text-base font-semibold text-[#F8FAFC] first:mt-0">{children}</h2>
                  ),
                  h3: ({ children }) => (
                    <h3 className="mb-1.5 mt-3 text-sm font-semibold text-[#F8FAFC] first:mt-0">{children}</h3>
                  ),
                  // Paragraph
                  p: ({ children }) => (
                    <p className="mb-2 last:mb-0">{children}</p>
                  ),
                  // Lists
                  ul: ({ children }) => (
                    <ul className="mb-2 ml-4 list-disc space-y-1">{children}</ul>
                  ),
                  ol: ({ children }) => (
                    <ol className="mb-2 ml-4 list-decimal space-y-1">{children}</ol>
                  ),
                  li: ({ children }) => (
                    <li className="text-[#F8FAFC]">{children}</li>
                  ),
                  // Blockquote
                  blockquote: ({ children }) => (
                    <blockquote className="my-2 border-l-2 border-[#38BDF8]/40 pl-3 text-[#94A3B8] italic">
                      {children}
                    </blockquote>
                  ),
                  // Inline code
                  code: ({ children, className }) => {
                    const isBlock = className?.includes('language-');
                    if (isBlock) {
                      return (
                        <code className={className}>
                          {children}
                        </code>
                      );
                    }
                    return (
                      <code className="rounded bg-[#0F2138] px-1.5 py-0.5 font-mono text-xs text-[#38BDF8]">
                        {children}
                      </code>
                    );
                  },
                  // Code block wrapper
                  pre: ({ children }) => (
                    <pre className="my-3 overflow-x-auto rounded-xl border border-[#28415D] bg-[#081426] p-4 font-mono text-xs leading-relaxed text-[#94A3B8]">
                      {children}
                    </pre>
                  ),
                  // Table
                  table: ({ children }) => (
                    <div className="my-3 overflow-x-auto rounded-xl border border-[#28415D]">
                      <table className="w-full text-xs">{children}</table>
                    </div>
                  ),
                  thead: ({ children }) => (
                    <thead className="border-b border-[#28415D] bg-[#0F2138]">{children}</thead>
                  ),
                  tbody: ({ children }) => <tbody>{children}</tbody>,
                  tr: ({ children }) => (
                    <tr className="border-b border-[#28415D]/50 last:border-0">{children}</tr>
                  ),
                  th: ({ children }) => (
                    <th className="px-3 py-2 text-left font-semibold text-[#94A3B8]">{children}</th>
                  ),
                  td: ({ children }) => (
                    <td className="px-3 py-2 text-[#F8FAFC]">{children}</td>
                  ),
                  // Links — open in new tab, sanitised by no javascript: hrefs
                  a: ({ href, children }) => {
                    const safe = href?.startsWith('http') || href?.startsWith('/') || href?.startsWith('mailto:');
                    return safe ? (
                      <a
                        href={href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-[#38BDF8] underline decoration-[#38BDF8]/40 hover:decoration-[#38BDF8]"
                      >
                        {children}
                      </a>
                    ) : (
                      <span className="text-[#38BDF8]">{children}</span>
                    );
                  },
                  // Strong / em
                  strong: ({ children }) => (
                    <strong className="font-semibold text-[#F8FAFC]">{children}</strong>
                  ),
                  em: ({ children }) => (
                    <em className="italic text-[#94A3B8]">{children}</em>
                  ),
                  // HR separator
                  hr: () => <hr className="my-4 border-[#28415D]" />,
                }}
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
