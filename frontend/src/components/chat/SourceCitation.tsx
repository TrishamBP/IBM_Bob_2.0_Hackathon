'use client';

import { ExternalLink, FileText } from 'lucide-react';
import { useOpenSource } from './SourceViewerContext';
import type { SourceCitationData } from '@/types/chat';

interface SourceCitationProps {
  sources: SourceCitationData[];
}

export function SourceCitation({ sources }: SourceCitationProps) {
  const openSource = useOpenSource();
  if (sources.length === 0) return null;

  return (
    <div className="mt-3">
      <p className="mb-2 text-[10px] font-semibold uppercase tracking-wider text-[#94A3B8]/70">
        Sources
      </p>
      <div className="flex flex-wrap gap-2">
        {sources.map((src) => {
          // Older saved answers have no document id and cannot be opened
          const viewable = Boolean(openSource && src.documentId);
          const details = (
            <>
              <FileText size={12} className="flex-shrink-0 text-[#38BDF8]/70" aria-hidden="true" />
              <div className="min-w-0 text-left">
                <p className="truncate text-xs font-medium text-[#F8FAFC]" title={src.title}>
                  {src.title}
                </p>
                <p className="text-[10px] text-[#94A3B8]">
                  {src.department} · {src.section ?? src.reference}
                </p>
              </div>
            </>
          );
          return (
            <div
              key={src.id}
              className="flex max-w-full items-center rounded-lg border border-[#28415D] bg-[#0F2138] transition-colors has-[button:hover]:border-[#38BDF8]/50 has-[button:hover]:bg-[#142B45]"
            >
              {viewable ? (
                <button
                  type="button"
                  onClick={() => openSource?.(src)}
                  aria-label={`View source: ${src.title}${src.section ? `, ${src.section}` : ''}`}
                  className="flex min-w-0 items-center gap-2 rounded-lg px-3 py-1.5 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#38BDF8]"
                >
                  {details}
                </button>
              ) : (
                <div className="flex min-w-0 items-center gap-2 px-3 py-1.5">{details}</div>
              )}
              {src.url && (
                <a
                  href={src.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={`Open ${src.title} in a new tab`}
                  className="mr-3 flex-shrink-0 text-[#94A3B8] transition-colors hover:text-[#38BDF8]"
                >
                  <ExternalLink size={11} />
                </a>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
