'use client';

import { useState } from 'react';
import { Copy, RefreshCw, ThumbsUp, ThumbsDown, Check } from 'lucide-react';

interface MessageActionsProps {
  content: string;
  conversationId: string;
  messageId: string;
  feedback: 'up' | 'down' | null | undefined;
  onRegenerate: () => void;
  onFeedback: (value: 'up' | 'down' | null) => void;
}

export function MessageActions({
  content,
  feedback,
  onRegenerate,
  onFeedback,
}: MessageActionsProps) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Clipboard API unavailable — silently ignore
    }
  }

  function handleFeedback(value: 'up' | 'down') {
    onFeedback(feedback === value ? null : value);
  }

  const btnBase =
    'inline-flex items-center justify-center rounded-md p-1.5 text-[#94A3B8]/60 transition-colors hover:bg-[#1B3653] hover:text-[#94A3B8] focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#38BDF8]';

  return (
    <div className="mt-2 flex items-center gap-0.5" role="toolbar" aria-label="Message actions">
      {/* Copy */}
      <button
        type="button"
        onClick={handleCopy}
        aria-label={copied ? 'Copied!' : 'Copy response'}
        className={btnBase}
      >
        {copied ? (
          <Check size={14} className="text-green-400" />
        ) : (
          <Copy size={14} />
        )}
      </button>

      {/* Regenerate */}
      <button
        type="button"
        onClick={onRegenerate}
        aria-label="Regenerate response"
        className={btnBase}
      >
        <RefreshCw size={14} />
      </button>

      {/* Separator */}
      <span className="mx-1 h-3.5 w-px bg-[#28415D]" aria-hidden="true" />

      {/* Thumbs up */}
      <button
        type="button"
        onClick={() => handleFeedback('up')}
        aria-label={feedback === 'up' ? 'Remove positive feedback' : 'Mark as helpful'}
        aria-pressed={feedback === 'up'}
        className={[
          btnBase,
          feedback === 'up' ? 'text-green-400 hover:text-green-300' : '',
        ].join(' ')}
      >
        <ThumbsUp size={14} />
      </button>

      {/* Thumbs down */}
      <button
        type="button"
        onClick={() => handleFeedback('down')}
        aria-label={feedback === 'down' ? 'Remove negative feedback' : 'Mark as unhelpful'}
        aria-pressed={feedback === 'down'}
        className={[
          btnBase,
          feedback === 'down' ? 'text-red-400 hover:text-red-300' : '',
        ].join(' ')}
      >
        <ThumbsDown size={14} />
      </button>
    </div>
  );
}
