import { ExternalLink, FileText } from 'lucide-react';
import type { SourceCitationData } from '@/types/chat';

interface SourceCitationProps {
  sources: SourceCitationData[];
}

export function SourceCitation({ sources }: SourceCitationProps) {
  if (sources.length === 0) return null;

  return (
    <div className="mt-3">
      <p className="mb-2 text-[10px] font-semibold uppercase tracking-wider text-[#94A3B8]/70">
        Sources
      </p>
      <div className="flex flex-wrap gap-2">
        {sources.map((src) => (
          <div
            key={src.id}
            className="flex items-center gap-2 rounded-lg border border-[#28415D] bg-[#0F2138] px-3 py-1.5"
          >
            <FileText size={12} className="flex-shrink-0 text-[#38BDF8]/70" aria-hidden="true" />
            <div className="min-w-0">
              <p className="truncate text-xs font-medium text-[#F8FAFC]" title={src.title}>
                {src.title}
              </p>
              <p className="text-[10px] text-[#94A3B8]">
                {src.department} · {src.reference}
              </p>
            </div>
            {src.url && (
              <a
                href={src.url}
                target="_blank"
                rel="noopener noreferrer"
                aria-label={`Open ${src.title}`}
                className="ml-1 flex-shrink-0 text-[#94A3B8] transition-colors hover:text-[#38BDF8]"
              >
                <ExternalLink size={11} />
              </a>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
