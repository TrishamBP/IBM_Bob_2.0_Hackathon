'use client';

import { useRef, useState, KeyboardEvent } from 'react';
import { ArrowUp } from 'lucide-react';

interface ChatComposerProps {
  onSend: (content: string) => void;
  disabled?: boolean;
}

export function ChatComposer({ onSend, disabled = false }: ChatComposerProps) {
  const [value, setValue] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const canSend = value.trim().length > 0 && !disabled;

  function submit() {
    if (!canSend) return;
    const trimmed = value.trim();
    setValue('');
    // Reset textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
    onSend(trimmed);
  }

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  }

  function handleInput() {
    const el = textareaRef.current;
    if (!el) return;
    // Auto-resize: shrink then grow
    el.style.height = 'auto';
    const maxHeight = 200;
    el.style.height = `${Math.min(el.scrollHeight, maxHeight)}px`;
  }

  return (
    <div className="border-t border-[#28415D] bg-[#081426] px-4 pb-4 pt-3 sm:px-6">
      <div className="mx-auto max-w-[850px]">
        <div
          className={[
            'flex items-end gap-3 rounded-2xl border bg-[#0F2138] px-4 py-3 transition-colors',
            disabled
              ? 'border-[#28415D] opacity-60'
              : 'border-[#28415D] focus-within:border-[#38BDF8]/60',
          ].join(' ')}
        >
          {/* Textarea */}
          <textarea
            ref={textareaRef}
            rows={1}
            value={value}
            onChange={(e) => {
              setValue(e.target.value);
              handleInput();
            }}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            placeholder="Ask anything about ACME Corp..."
            aria-label="Message composer"
            aria-multiline="true"
            className={[
              'flex-1 resize-none bg-transparent text-sm leading-relaxed text-[#F8FAFC]',
              'placeholder:text-[#94A3B8]/60',
              'focus:outline-none',
              'disabled:cursor-not-allowed',
              'max-h-[200px] overflow-y-auto',
            ].join(' ')}
            style={{ height: 'auto' }}
          />

          {/* Send button */}
          <button
            type="button"
            onClick={submit}
            disabled={!canSend}
            aria-label="Send message"
            className={[
              'mb-0.5 flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-xl transition-colors',
              'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#38BDF8] focus-visible:ring-offset-2 focus-visible:ring-offset-[#081426]',
              canSend
                ? 'bg-[#38BDF8] text-[#081426] hover:bg-[#7DD3FA]'
                : 'bg-[#28415D] text-[#94A3B8]/40 cursor-not-allowed',
            ].join(' ')}
          >
            <ArrowUp size={16} />
          </button>
        </div>

        <p className="mt-2 text-center text-[10px] text-[#94A3B8]/40">
          AI-generated answers should be verified against company documentation.
        </p>
      </div>
    </div>
  );
}
