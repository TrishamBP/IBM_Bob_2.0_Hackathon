'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import ReactMarkdown, { type Components } from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { AlertCircle, AlertTriangle, Crosshair, FileText, RotateCw, X } from 'lucide-react';
import { markdownComponents } from './markdownComponents';
import { fetchSourceDocument, type SourceDocument } from '@/lib/api/sources';
import type { SourceCitationData } from '@/types/chat';

interface SourceViewerDrawerProps {
  isOpen: boolean;
  /** Kept while closing so the panel does not empty mid-animation. */
  source: SourceCitationData | null;
  onClose: () => void;
}

type LoadResult = { documentId: string; doc?: SourceDocument; error?: string };

// Documents can nest deeper than chat answers usually do
const documentComponents: Components = {
  ...markdownComponents,
  h4: ({ children }) => (
    <h4 className="mb-1 mt-3 text-sm font-medium text-[#F8FAFC] first:mt-0">{children}</h4>
  ),
  h5: ({ children }) => (
    <h5 className="mb-1 mt-2 text-xs font-semibold uppercase tracking-wide text-[#94A3B8] first:mt-0">
      {children}
    </h5>
  ),
  h6: ({ children }) => (
    <h6 className="mb-1 mt-2 text-xs font-medium text-[#94A3B8] first:mt-0">{children}</h6>
  ),
};

function pages(start: number | null, end: number | null): string | null {
  if (!start) return null;
  return end && end !== start ? `pp. ${start}–${end}` : `p. ${start}`;
}

export function SourceViewerDrawer({ isOpen, source, onClose }: SourceViewerDrawerProps) {
  const documentId = source?.documentId;
  const chunkId = source?.chunkId;
  const [result, setResult] = useState<LoadResult | null>(null);
  const [attempt, setAttempt] = useState(0);
  const bodyRef = useRef<HTMLDivElement>(null);
  const closeRef = useRef<HTMLButtonElement>(null);

  // Load the document whenever a different citation is opened
  useEffect(() => {
    if (!documentId) return;
    let cancelled = false;
    fetchSourceDocument(documentId).then(
      (doc) => !cancelled && setResult({ documentId, doc }),
      (err: unknown) =>
        !cancelled &&
        setResult({
          documentId,
          error: err instanceof Error ? err.message : 'Could not load the document.',
        })
    );
    return () => {
      cancelled = true;
    };
  }, [documentId, attempt]);

  const current = result?.documentId === documentId ? result : null;
  const doc = current?.doc;
  const loading = Boolean(documentId) && !current;
  const citedFound = Boolean(
    doc && source?.chunkId && doc.chunks.some((c) => c.chunk_id === source.chunkId)
  );

  const scrollToCited = useCallback(
    (behavior: ScrollBehavior = 'smooth') => {
      if (!chunkId) return;
      const el = bodyRef.current?.querySelector<HTMLElement>(
        `[data-chunk-id="${CSS.escape(chunkId)}"]`
      );
      el?.scrollIntoView({ block: 'start', behavior });
    },
    [chunkId]
  );

  // Jump to the cited passage once the document is on screen
  useEffect(() => {
    if (!isOpen || !doc) return;
    const frame = requestAnimationFrame(() => scrollToCited('auto'));
    return () => cancelAnimationFrame(frame);
  }, [isOpen, doc, scrollToCited]);

  // Escape closes; focus the close button on open
  useEffect(() => {
    if (!isOpen) return;
    closeRef.current?.focus();
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [isOpen, onClose]);

  const meta = doc
    ? [
        doc.department,
        doc.version && `v${doc.version.replace(/^v/i, '')}`,
        doc.effective_date && `Effective ${doc.effective_date}`,
        doc.source_filename,
      ].filter(Boolean)
    : source
      ? [source.department]
      : [];

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
        aria-labelledby="source-viewer-title"
        inert={!isOpen}
        className={[
          'fixed inset-y-0 right-0 z-50 flex w-full max-w-[680px] flex-col border-l border-[#28415D] bg-[#0F2138] shadow-2xl',
          'transition-transform duration-200 ease-in-out',
          isOpen ? 'translate-x-0' : 'translate-x-full',
        ].join(' ')}
      >
        {/* Header */}
        <div className="flex items-start justify-between gap-3 border-b border-[#28415D] px-5 py-4">
          <div className="flex min-w-0 gap-3">
            <span className="mt-0.5 flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-lg bg-[#38BDF8]/10 text-[#38BDF8]">
              <FileText size={16} aria-hidden="true" />
            </span>
            <div className="min-w-0">
              <h2
                id="source-viewer-title"
                className="truncate text-base font-semibold text-[#F8FAFC]"
                title={doc?.title ?? source?.title}
              >
                {doc?.title ?? source?.title ?? 'Source'}
              </h2>
              {meta.length > 0 && (
                <p className="mt-0.5 truncate text-xs text-[#94A3B8]">{meta.join(' · ')}</p>
              )}
            </div>
          </div>
          <button
            ref={closeRef}
            type="button"
            onClick={onClose}
            aria-label="Close source viewer"
            className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-lg text-[#94A3B8] transition-colors hover:bg-[#142B45] hover:text-[#F8FAFC] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#38BDF8]"
          >
            <X size={18} />
          </button>
        </div>

        {/* Cited section strip */}
        {source && (
          <div className="flex items-center justify-between gap-3 border-b border-[#28415D] bg-[#081426]/60 px-5 py-2.5">
            <p className="min-w-0 truncate text-xs text-[#94A3B8]">
              <span className="mr-2 rounded bg-[#38BDF8]/15 px-1.5 py-0.5 font-mono text-[10px] font-semibold text-[#38BDF8]">
                {source.id}
              </span>
              {source.section ?? source.reference}
            </p>
            {citedFound && (
              <button
                type="button"
                onClick={() => scrollToCited()}
                className="flex flex-shrink-0 items-center gap-1 rounded-md px-2 py-1 text-xs font-medium text-[#38BDF8] transition-colors hover:bg-[#142B45] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#38BDF8]"
              >
                <Crosshair size={12} aria-hidden="true" />
                Cited passage
              </button>
            )}
          </div>
        )}

        {/* Body */}
        <div ref={bodyRef} className="flex-1 overflow-y-auto px-5 py-5">
          {loading && (
            <div className="space-y-3" aria-label="Loading document" role="status">
              {[92, 100, 76, 88, 60].map((w, i) => (
                <div
                  key={i}
                  className="h-3 animate-pulse rounded bg-[#28415D]/60"
                  style={{ width: `${w}%` }}
                />
              ))}
            </div>
          )}

          {current?.error && (
            <div className="flex flex-col items-center gap-3 py-10 text-center">
              <AlertCircle size={22} className="text-[#F87171]" aria-hidden="true" />
              <p className="max-w-sm text-sm text-[#94A3B8]">{current.error}</p>
              <button
                type="button"
                onClick={() => {
                  setResult(null);
                  setAttempt((a) => a + 1);
                }}
                className="flex items-center gap-1.5 rounded-lg border border-[#28415D] px-3 py-1.5 text-xs font-medium text-[#F8FAFC] transition-colors hover:bg-[#142B45] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#38BDF8]"
              >
                <RotateCw size={12} aria-hidden="true" />
                Try again
              </button>
            </div>
          )}

          {doc && (
            <>
              {source?.chunkId && !citedFound && (
                <div className="mb-4 flex gap-2 rounded-lg border border-[#FBBF24]/30 bg-[#FBBF24]/10 px-3 py-2.5 text-xs text-[#FDE68A]">
                  <AlertTriangle size={14} className="mt-0.5 flex-shrink-0" aria-hidden="true" />
                  <p>
                    This document has been updated since this answer was written, so the cited
                    passage can&apos;t be highlighted. Showing the current version.
                  </p>
                </div>
              )}

              <article className="text-sm leading-relaxed text-[#F8FAFC]">
                {doc.chunks.map((chunk, i) => {
                  const cited = chunk.chunk_id === source?.chunkId;
                  // Page numbers only where they change (and on the cited passage)
                  const newPage = chunk.page_start !== doc.chunks[i - 1]?.page_start;
                  const pageLabel =
                    cited || newPage ? pages(chunk.page_start, chunk.page_end) : null;
                  return (
                    <section
                      key={chunk.chunk_id}
                      data-chunk-id={chunk.chunk_id}
                      aria-label={cited ? 'Cited passage' : undefined}
                      className={[
                        'scroll-mt-4 rounded-lg',
                        cited
                          ? 'my-3 border border-[#38BDF8]/40 bg-[#38BDF8]/[0.07] px-4 py-3'
                          : 'px-4 py-1',
                      ].join(' ')}
                    >
                      {(cited || pageLabel) && (
                        <p className="mb-1.5 flex items-center gap-2 text-[10px] font-semibold uppercase tracking-wider">
                          {cited && <span className="text-[#38BDF8]">Cited passage</span>}
                          {pageLabel && <span className="text-[#94A3B8]/60">{pageLabel}</span>}
                        </p>
                      )}
                      <ReactMarkdown remarkPlugins={[remarkGfm]} components={documentComponents}>
                        {chunk.markdown}
                      </ReactMarkdown>
                    </section>
                  );
                })}
              </article>
            </>
          )}
        </div>
      </aside>
    </>
  );
}
