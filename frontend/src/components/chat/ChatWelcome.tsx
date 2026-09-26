import { Box } from 'lucide-react';
import { SuggestedQuestions } from './SuggestedQuestions';

interface ChatWelcomeProps {
  email: string;
  onSelectQuestion: (question: string) => void;
}

export function ChatWelcome({ onSelectQuestion }: ChatWelcomeProps) {
  return (
    <div className="flex flex-1 flex-col items-center justify-center px-4 py-12 sm:px-8">
      <div className="w-full max-w-[850px]">
        {/* Icon */}
        <div className="mb-6 flex justify-center">
          <div className="flex h-16 w-16 items-center justify-center rounded-2xl border border-[#28415D] bg-[#142B45]">
            <Box size={28} className="text-[#38BDF8]" strokeWidth={2} aria-hidden="true" />
          </div>
        </div>

        {/* Heading */}
        <h1 className="text-center text-2xl font-bold text-[#F8FAFC] sm:text-3xl">
          Good to have you here.
        </h1>
        <p className="mt-3 text-center text-sm leading-relaxed text-[#94A3B8] sm:text-base">
          I&apos;m your ACME onboarding assistant. Ask me anything about your workplace,
          tools, company policies or getting started with your team.
        </p>

        {/* Suggested questions */}
        <SuggestedQuestions onSelect={onSelectQuestion} />
      </div>
    </div>
  );
}
