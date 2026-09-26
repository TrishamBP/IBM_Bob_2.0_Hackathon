'use client';

import { Box, Lightbulb, PanelLeftOpen } from 'lucide-react';

interface ChatHeaderProps {
  conversationTitle: string | null;
  sidebarOpen: boolean;
  onToggleSidebar: () => void;
  onOpenExamples: () => void;
}

export function ChatHeader({
  conversationTitle,
  sidebarOpen,
  onToggleSidebar,
  onOpenExamples,
}: ChatHeaderProps) {
  return (
    <header className="flex h-14 flex-shrink-0 items-center gap-3 border-b border-[#28415D] bg-[#0F2138] px-4">
      {/* Mobile sidebar toggle */}
      {!sidebarOpen && (
        <button
          type="button"
          onClick={onToggleSidebar}
          aria-label="Open sidebar"
          className="flex h-8 w-8 items-center justify-center rounded-lg text-[#94A3B8] transition-colors hover:bg-[#142B45] hover:text-[#F8FAFC] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#38BDF8] lg:hidden"
        >
          <PanelLeftOpen size={18} />
        </button>
      )}

      {/* Brand — only shown on mobile when sidebar is closed */}
      <div className="flex items-center gap-2 lg:hidden">
        <span className="flex h-6 w-6 items-center justify-center rounded-md bg-[#38BDF8] text-[#081426]">
          <Box size={13} strokeWidth={2.5} aria-hidden="true" />
        </span>
        <span className="text-sm font-bold text-[#F8FAFC]">
          ACME <span className="text-[#38BDF8]">Onboard</span>
        </span>
      </div>

      {/* Conversation title — desktop */}
      {conversationTitle && (
        <h2 className="hidden flex-1 truncate text-sm font-medium text-[#94A3B8] lg:block">
          {conversationTitle}
        </h2>
      )}

      {/* Example questions drawer toggle */}
      <button
        type="button"
        onClick={onOpenExamples}
        className="ml-auto flex h-8 items-center gap-1.5 rounded-lg border border-[#28415D] px-3 text-xs font-medium text-[#94A3B8] transition-colors hover:border-[#38BDF8]/40 hover:bg-[#142B45] hover:text-[#F8FAFC] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#38BDF8]"
      >
        <Lightbulb size={14} aria-hidden="true" />
        <span className="hidden sm:inline">Example questions</span>
        <span className="sm:hidden">Examples</span>
      </button>

      {/* Demo badge */}
      <div className="flex items-center gap-2 rounded-full border border-[#38BDF8]/30 bg-[#38BDF8]/10 px-3 py-1">
        <span className="h-1.5 w-1.5 rounded-full bg-[#38BDF8]" aria-hidden="true" />
        <span className="text-xs font-medium text-[#38BDF8]">Demo</span>
      </div>
    </header>
  );
}
