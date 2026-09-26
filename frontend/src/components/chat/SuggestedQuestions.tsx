import {
  Code2,
  FileText,
  Shield,
  CalendarDays,
  GitBranch,
  Bot,
  type LucideIcon,
} from 'lucide-react';
import { SUGGESTED_QUESTIONS } from '@/lib/chat/chatUtils';

const ICON_MAP: Record<string, LucideIcon> = {
  Code2,
  FileText,
  Shield,
  CalendarDays,
  GitBranch,
  Bot,
};

interface SuggestedQuestionsProps {
  onSelect: (question: string) => void;
}

export function SuggestedQuestions({ onSelect }: SuggestedQuestionsProps) {
  return (
    <div
      className="mt-8 grid grid-cols-1 gap-3 sm:grid-cols-2"
      role="list"
      aria-label="Suggested questions"
    >
      {SUGGESTED_QUESTIONS.map((q) => {
        const Icon = ICON_MAP[q.icon] ?? FileText;
        return (
          <button
            key={q.id}
            type="button"
            role="listitem"
            onClick={() => onSelect(q.text)}
            className={[
              'flex items-center gap-3 rounded-xl border border-[#28415D] bg-[#0F2138] px-4 py-3.5',
              'text-left text-sm font-medium text-[#F8FAFC] transition-colors',
              'hover:border-[#38BDF8]/40 hover:bg-[#142B45]',
              'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#38BDF8] focus-visible:ring-offset-2 focus-visible:ring-offset-[#081426]',
            ].join(' ')}
          >
            <span
              className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-lg border border-[#28415D] bg-[#142B45] text-[#38BDF8]"
              aria-hidden="true"
            >
              <Icon size={16} />
            </span>
            <span className="leading-snug">{q.text}</span>
          </button>
        );
      })}
    </div>
  );
}
