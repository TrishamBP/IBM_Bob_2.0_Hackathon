'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import { Check, ChevronDown, Copy, CornerDownLeft, Search, X } from 'lucide-react';
import { EXAMPLE_SECTIONS, type ExampleSection } from '@/lib/chat/exampleQuestions';

interface ExampleQuestionsDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  /** Places the question in the composer (does not send it). */
  onInsert: (text: string) => void;
}

function matches(text: string, query: string) {
  return text.toLowerCase().includes(query);
}

/** Filter sections down to the questions/turns matching the search query. */
function filterSections(sections: ExampleSection[], query: string): ExampleSection[] {
  if (!query) return sections;
  return sections
    .map((section) => ({
      ...section,
      questions: section.questions?.filter(
        (item) => matches(item.text, query) || (item.note && matches(item.note, query))
      ),
      conversations: section.conversations?.filter(
        (c) => matches(c.title, query) || c.turns.some((t) => matches(t, query))
      ),
    }))
    .filter((s) => (s.questions?.length ?? 0) + (s.conversations?.length ?? 0) > 0);
}

// ---------------------------------------------------------------------------
// Single question row — copy + insert actions
// ---------------------------------------------------------------------------

function QuestionRow({
  text,
  note,
  prefix,
  onInsert,
}: {
  text: string;
  note?: string;
  prefix?: string;
  onInsert: (text: string) => void;
}) {
  const [copied, setCopied] = useState(false);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => () => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
  }, []);

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
      timeoutRef.current = setTimeout(() => setCopied(false), 1500);
    } catch {
      // Clipboard unavailable (e.g. insecure context) — insert still works
    }
  }

  const actionClass =
    'flex h-7 w-7 items-center justify-center rounded-md text-[#94A3B8] transition-colors hover:bg-[#28415D] hover:text-[#F8FAFC] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#38BDF8]';

  return (
    <li className="group flex items-start gap-2 rounded-lg px-2 py-2 transition-colors hover:bg-[#142B45]">
      {prefix && (
        <span className="mt-0.5 flex-shrink-0 text-[11px] font-semibold text-[#38BDF8]">
          {prefix}
        </span>
      )}
      <button
        type="button"
        onClick={() => onInsert(text)}
        className="min-w-0 flex-1 text-left text-sm leading-relaxed text-[#E2E8F0] focus-visible:outline-none focus-visible:underline"
        title="Insert into chat"
      >
        {text}
        {note && <span className="mt-0.5 block text-[11px] text-[#94A3B8]">{note}</span>}
      </button>
      <div className="flex flex-shrink-0 items-center gap-0.5 opacity-100 sm:opacity-0 sm:transition-opacity sm:group-hover:opacity-100 sm:group-focus-within:opacity-100">
        <button
          type="button"
          onClick={handleCopy}
          aria-label={copied ? 'Copied' : 'Copy question'}
          title={copied ? 'Copied' : 'Copy'}
          className={actionClass}
        >
          {copied ? <Check size={14} className="text-[#38BDF8]" /> : <Copy size={14} />}
        </button>
        <button
          type="button"
          onClick={() => onInsert(text)}
          aria-label="Insert question into chat"
          title="Insert into chat"
          className={actionClass}
        >
          <CornerDownLeft size={14} />
        </button>
      </div>
    </li>
  );
}

// ---------------------------------------------------------------------------
// Drawer
// ---------------------------------------------------------------------------

export function ExampleQuestionsDrawer({ isOpen, onClose, onInsert }: ExampleQuestionsDrawerProps) {
  const [query, setQuery] = useState('');
  const searchRef = useRef<HTMLInputElement>(null);

  const normalized = query.trim().toLowerCase();
  const sections = useMemo(() => filterSections(EXAMPLE_SECTIONS, normalized), [normalized]);

  // Close on Escape, focus search on open
  useEffect(() => {
    if (!isOpen) return;
    searchRef.current?.focus();
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [isOpen, onClose]);

  return (
    <>
      {/* Backdrop */}
      <div
        className={[
          'fixed inset-0 z-40 bg-black/50 transition-opacity duration-200',
          isOpen ? 'opacity-100' : 'pointer-events-none opacity-0',
        ].join(' ')}
        aria-hidden="true"
        onClick={onClose}
      />

      {/* Panel */}
      <aside
        role="dialog"
        aria-modal="true"
        aria-labelledby="example-questions-title"
        inert={!isOpen}
        className={[
          'fixed inset-y-0 right-0 z-50 flex w-full max-w-[440px] flex-col border-l border-[#28415D] bg-[#0F2138] shadow-2xl',
          'transition-transform duration-200 ease-in-out',
          isOpen ? 'translate-x-0' : 'translate-x-full',
        ].join(' ')}
      >
        {/* Header */}
        <div className="flex items-start justify-between gap-3 border-b border-[#28415D] px-5 py-4">
          <div>
            <h2 id="example-questions-title" className="text-base font-semibold text-[#F8FAFC]">
              Example questions
            </h2>
            <p className="mt-0.5 text-xs text-[#94A3B8]">
              Click a question to add it to the chat, or copy it.
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close example questions"
            className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-lg text-[#94A3B8] transition-colors hover:bg-[#142B45] hover:text-[#F8FAFC] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#38BDF8]"
          >
            <X size={18} />
          </button>
        </div>

        {/* Search */}
        <div className="border-b border-[#28415D] px-5 py-3">
          <label className="flex items-center gap-2 rounded-lg border border-[#28415D] bg-[#081426] px-3 py-2 focus-within:border-[#38BDF8]/60">
            <Search size={14} className="text-[#94A3B8]" aria-hidden="true" />
            <input
              ref={searchRef}
              type="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search questions..."
              aria-label="Search example questions"
              className="flex-1 bg-transparent text-sm text-[#F8FAFC] placeholder:text-[#94A3B8]/60 focus:outline-none"
            />
          </label>
        </div>

        {/* Sections */}
        <div className="flex-1 overflow-y-auto px-3 py-3">
          {sections.length === 0 && (
            <p className="px-2 py-6 text-center text-sm text-[#94A3B8]">
              No questions match &ldquo;{query}&rdquo;.
            </p>
          )}

          {sections.map((section, index) => (
            <details
              key={section.id}
              // Expand everything while searching; otherwise only the first section
              open={normalized ? true : index === 0}
              className="group/section mb-2 rounded-xl border border-[#28415D] bg-[#081426]/40"
            >
              <summary className="flex cursor-pointer list-none items-center justify-between gap-2 rounded-xl px-3 py-2.5 text-sm font-semibold text-[#F8FAFC] hover:bg-[#142B45] [&::-webkit-details-marker]:hidden">
                <span>
                  {section.title}
                  <span className="ml-2 text-xs font-normal text-[#94A3B8]">
                    {(section.questions?.length ?? 0) + (section.conversations?.length ?? 0)}
                  </span>
                </span>
                <ChevronDown
                  size={16}
                  className="text-[#94A3B8] transition-transform group-open/section:rotate-180"
                  aria-hidden="true"
                />
              </summary>

              <div className="px-1 pb-2">
                {section.description && (
                  <p className="px-2 pb-1 text-xs text-[#94A3B8]">{section.description}</p>
                )}

                {section.questions && (
                  <ul>
                    {section.questions.map((item) => (
                      <QuestionRow
                        key={item.text}
                        text={item.text}
                        note={item.note}
                        onInsert={onInsert}
                      />
                    ))}
                  </ul>
                )}

                {section.conversations?.map((conversation) => (
                  <div key={conversation.title} className="mt-1 px-1">
                    <p className="px-2 pt-2 text-xs font-medium uppercase tracking-wide text-[#94A3B8]">
                      {conversation.title}
                    </p>
                    <ul>
                      {conversation.turns.map((turn, i) => (
                        <QuestionRow
                          key={turn}
                          text={turn}
                          prefix={`${i + 1}.`}
                          onInsert={onInsert}
                        />
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            </details>
          ))}
        </div>
      </aside>
    </>
  );
}
