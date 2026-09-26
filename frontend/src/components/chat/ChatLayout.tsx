'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { ChatSidebar } from './ChatSidebar';
import { ChatHeader } from './ChatHeader';
import { ChatWelcome } from './ChatWelcome';
import { ChatMessageList } from './ChatMessageList';
import { ChatComposer } from './ChatComposer';
import { useChat } from '@/hooks/useChat';
import { clearSession } from '@/lib/auth';

interface ChatLayoutProps {
  email: string;
}

export function ChatLayout({ email }: ChatLayoutProps) {
  const router = useRouter();
  // Initialise sidebar: open on desktop, closed on mobile — lazy so no setState in effect
  const [sidebarOpen, setSidebarOpen] = useState<boolean>(() => {
    if (typeof window === 'undefined') return true;
    return !window.matchMedia('(max-width: 1023px)').matches;
  });

  // Keep sidebar state in sync as the viewport is resized
  useEffect(() => {
    const mq = window.matchMedia('(max-width: 1023px)');
    const handler = (e: MediaQueryListEvent) => setSidebarOpen(!e.matches);
    mq.addEventListener('change', handler);
    return () => mq.removeEventListener('change', handler);
  }, []);

  const {
    state,
    activeConversation,
    newConversation,
    selectConversation,
    renameConversation,
    deleteConversation,
    sendMessage,
    regenerateLastResponse,
    setMessageFeedback,
  } = useChat(email);

  function handleLogout() {
    clearSession();
    router.push('/employee/login');
  }

  function handleSendMessage(content: string) {
    sendMessage(content, activeConversation?.id ?? undefined);
  }

  function handleNewConversation() {
    newConversation();
    // Close sidebar on mobile after starting a new chat
    if (window.matchMedia('(max-width: 1023px)').matches) {
      setSidebarOpen(false);
    }
  }

  function handleSelectConversation(id: string) {
    selectConversation(id);
    // Close sidebar on mobile after selecting
    if (window.matchMedia('(max-width: 1023px)').matches) {
      setSidebarOpen(false);
    }
  }

  const hasMessages =
    activeConversation !== null && activeConversation.messages.length > 0;

  return (
    /* Full-viewport container — flex row */
    <div className="flex h-screen overflow-hidden bg-[#081426]">
      {/* ------------------------------------------------------------------ */}
      {/* Sidebar overlay (mobile)                                             */}
      {/* ------------------------------------------------------------------ */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-30 bg-black/50 lg:hidden"
          aria-hidden="true"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* ------------------------------------------------------------------ */}
      {/* Sidebar                                                              */}
      {/* ------------------------------------------------------------------ */}
      <div
        className={[
          'fixed inset-y-0 left-0 z-40 w-[270px] transition-transform duration-200 ease-in-out',
          'lg:relative lg:translate-x-0 lg:z-auto',
          sidebarOpen ? 'translate-x-0' : '-translate-x-full',
        ].join(' ')}
        aria-hidden={!sidebarOpen}
      >
        <ChatSidebar
          conversations={state.conversations}
          activeConversationId={state.activeConversationId}
          email={email}
          onNewConversation={handleNewConversation}
          onSelectConversation={handleSelectConversation}
          onRenameConversation={renameConversation}
          onDeleteConversation={deleteConversation}
          onLogout={handleLogout}
          onClose={() => setSidebarOpen(false)}
        />
      </div>

      {/* ------------------------------------------------------------------ */}
      {/* Main area                                                            */}
      {/* ------------------------------------------------------------------ */}
      <div className="flex min-w-0 flex-1 flex-col">
        {/* Header */}
        <ChatHeader
          conversationTitle={activeConversation?.title ?? null}
          sidebarOpen={sidebarOpen}
          onToggleSidebar={() => setSidebarOpen((v) => !v)}
        />

        {/* Message area */}
        <div className="flex flex-1 flex-col overflow-hidden">
          {hasMessages ? (
            /* Message list — scrollable */
            <div className="flex-1 overflow-y-auto">
              <div className="mx-auto max-w-[850px]">
                <ChatMessageList
                  conversation={activeConversation!}
                  isLoading={state.isLoading}
                  onRegenerate={() =>
                    activeConversation && regenerateLastResponse(activeConversation.id)
                  }
                  onFeedback={(msgId, value) =>
                    activeConversation &&
                    setMessageFeedback(activeConversation.id, msgId, value)
                  }
                />
              </div>
            </div>
          ) : (
            /* Welcome screen — scrollable */
            <div className="flex-1 overflow-y-auto">
              <ChatWelcome
                email={email}
                onSelectQuestion={(q) => sendMessage(q, activeConversation?.id ?? undefined)}
              />
            </div>
          )}

          {/* Composer — always at bottom, never overlaps messages */}
          <ChatComposer
            onSend={handleSendMessage}
            disabled={state.isLoading}
          />
        </div>
      </div>
    </div>
  );
}
