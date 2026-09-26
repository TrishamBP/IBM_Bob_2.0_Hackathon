'use client';

import { useState, useRef, useEffect, KeyboardEvent } from 'react';
import { Box, Plus, Search, MoreHorizontal, Pencil, Trash2, LogOut, User, PanelLeftClose, MessageSquare } from 'lucide-react';
import { groupConversations } from '@/lib/chat/chatUtils';
import type { Conversation } from '@/types/chat';

interface ChatSidebarProps {
  conversations: Conversation[];
  activeConversationId: string | null;
  email: string;
  onNewConversation: () => void;
  onSelectConversation: (id: string) => void;
  onRenameConversation: (id: string, title: string) => void;
  onDeleteConversation: (id: string) => void;
  onLogout: () => void;
  onClose?: () => void; // mobile close
}

interface ConversationMenuState {
  id: string;
  mode: 'menu' | 'rename';
}

export function ChatSidebar({
  conversations,
  activeConversationId,
  email,
  onNewConversation,
  onSelectConversation,
  onRenameConversation,
  onDeleteConversation,
  onLogout,
  onClose,
}: ChatSidebarProps) {
  const [search, setSearch] = useState('');
  const [menuState, setMenuState] = useState<ConversationMenuState | null>(null);
  const [renameValue, setRenameValue] = useState('');
  const [deleteConfirmId, setDeleteConfirmId] = useState<string | null>(null);
  const menuRef = useRef<HTMLDivElement>(null);
  const renameInputRef = useRef<HTMLInputElement>(null);

  // Close menu when clicking outside
  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setMenuState(null);
      }
    }
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  // Focus rename input when mode switches
  useEffect(() => {
    if (menuState?.mode === 'rename') {
      setTimeout(() => renameInputRef.current?.focus(), 50);
    }
  }, [menuState]);

  // Filter conversations
  const filtered = conversations.filter((c) =>
    c.title.toLowerCase().includes(search.toLowerCase())
  );
  const groups = groupConversations(filtered);

  function openMenu(id: string) {
    const conv = conversations.find((c) => c.id === id);
    setRenameValue(conv?.title ?? '');
    setMenuState({ id, mode: 'menu' });
  }

  function startRename(id: string) {
    const conv = conversations.find((c) => c.id === id);
    setRenameValue(conv?.title ?? '');
    setMenuState({ id, mode: 'rename' });
  }

  function commitRename() {
    if (!menuState) return;
    onRenameConversation(menuState.id, renameValue);
    setMenuState(null);
  }

  function handleRenameKey(e: KeyboardEvent<HTMLInputElement>) {
    if (e.key === 'Enter') commitRename();
    if (e.key === 'Escape') setMenuState(null);
  }

  function confirmDelete(id: string) {
    setMenuState(null);
    setDeleteConfirmId(id);
  }

  function executeDelete() {
    if (deleteConfirmId) {
      onDeleteConversation(deleteConfirmId);
      setDeleteConfirmId(null);
    }
  }

  return (
    <aside
      className="flex h-full w-full flex-col bg-[#0F2138] select-none"
      aria-label="Conversation sidebar"
    >
      {/* Top section */}
      <div className="flex-shrink-0 px-3 pt-4 pb-2">
        {/* Brand row */}
        <div className="mb-4 flex items-center justify-between px-1">
          <div className="flex items-center gap-2.5">
            <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-[#38BDF8] text-[#081426]">
              <Box size={15} strokeWidth={2.5} aria-hidden="true" />
            </span>
            <span className="text-sm font-bold text-[#F8FAFC]">
              ACME <span className="text-[#38BDF8]">Onboard</span>
            </span>
          </div>
          {/* Mobile close */}
          {onClose && (
            <button
              type="button"
              onClick={onClose}
              aria-label="Close sidebar"
              className="flex h-7 w-7 items-center justify-center rounded-lg text-[#94A3B8] transition-colors hover:bg-[#142B45] hover:text-[#F8FAFC] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#38BDF8] lg:hidden"
            >
              <PanelLeftClose size={16} />
            </button>
          )}
        </div>

        {/* New chat button */}
        <button
          type="button"
          onClick={onNewConversation}
          className="flex w-full items-center gap-2.5 rounded-xl bg-[#142B45] px-3 py-2.5 text-sm font-medium text-[#F8FAFC] transition-colors hover:bg-[#1B3653] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#38BDF8]"
        >
          <Plus size={16} className="text-[#38BDF8]" aria-hidden="true" />
          New Chat
        </button>

        {/* Search */}
        <div className="relative mt-3">
          <Search
            size={14}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-[#94A3B8]/50"
            aria-hidden="true"
          />
          <input
            type="search"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search chats"
            aria-label="Search conversations"
            className="w-full rounded-lg border border-[#28415D] bg-[#142B45] py-2 pl-8 pr-3 text-xs text-[#F8FAFC] placeholder:text-[#94A3B8]/50 focus:border-[#38BDF8]/50 focus:outline-none focus:ring-1 focus:ring-[#38BDF8]/30"
          />
        </div>
      </div>

      {/* Conversation list */}
      <nav
        className="flex-1 overflow-y-auto px-3 py-2"
        aria-label="Conversation history"
      >
        {groups.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <MessageSquare size={28} className="mb-3 text-[#94A3B8]/30" aria-hidden="true" />
            <p className="text-xs text-[#94A3B8]/50">
              {search ? 'No conversations match your search.' : 'No conversations yet. Start a new chat!'}
            </p>
          </div>
        ) : (
          groups.map(({ group, items }) => (
            <div key={group} className="mb-4">
              <p className="mb-1.5 px-2 text-[10px] font-semibold uppercase tracking-wider text-[#94A3B8]/50">
                {group}
              </p>
              <ul className="space-y-0.5">
                {items.map((conv) => (
                  <li key={conv.id} className="relative">
                    {menuState?.id === conv.id && menuState.mode === 'rename' ? (
                      /* Inline rename input */
                      <div className="flex items-center gap-1 rounded-lg bg-[#142B45] px-2 py-1.5">
                        <input
                          ref={renameInputRef}
                          value={renameValue}
                          onChange={(e) => setRenameValue(e.target.value)}
                          onKeyDown={handleRenameKey}
                          onBlur={commitRename}
                          aria-label="Rename conversation"
                          className="flex-1 bg-transparent text-xs text-[#F8FAFC] focus:outline-none"
                        />
                      </div>
                    ) : (
                      <button
                        type="button"
                        onClick={() => onSelectConversation(conv.id)}
                        aria-current={conv.id === activeConversationId ? 'page' : undefined}
                        className={[
                          'group flex w-full items-center gap-2 rounded-lg px-2 py-2 text-left text-xs transition-colors',
                          'focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#38BDF8]',
                          conv.id === activeConversationId
                            ? 'bg-[#142B45] text-[#F8FAFC]'
                            : 'text-[#94A3B8] hover:bg-[#142B45] hover:text-[#F8FAFC]',
                        ].join(' ')}
                      >
                        <span className="flex-1 truncate">{conv.title}</span>

                        {/* Three-dot menu button */}
                        <span
                          role="button"
                          tabIndex={0}
                          aria-label={`Options for "${conv.title}"`}
                          onClick={(e) => {
                            e.stopPropagation();
                            openMenu(conv.id);
                          }}
                          onKeyDown={(e) => {
                            if (e.key === 'Enter' || e.key === ' ') {
                              e.preventDefault();
                              e.stopPropagation();
                              openMenu(conv.id);
                            }
                          }}
                          className="flex-shrink-0 rounded p-0.5 text-[#94A3B8]/0 transition-colors group-hover:text-[#94A3B8]/60 hover:!text-[#94A3B8] focus-visible:text-[#94A3B8]/60 focus-visible:outline-none"
                        >
                          <MoreHorizontal size={14} />
                        </span>
                      </button>
                    )}

                    {/* Dropdown menu */}
                    {menuState?.id === conv.id && menuState.mode === 'menu' && (
                      <div
                        ref={menuRef}
                        role="menu"
                        aria-label={`Options for "${conv.title}"`}
                        className="absolute right-0 top-8 z-20 w-40 rounded-xl border border-[#28415D] bg-[#142B45] py-1 shadow-xl"
                      >
                        <button
                          role="menuitem"
                          type="button"
                          onClick={() => startRename(conv.id)}
                          className="flex w-full items-center gap-2.5 px-3 py-2 text-xs text-[#F8FAFC] transition-colors hover:bg-[#1B3653]"
                        >
                          <Pencil size={13} className="text-[#94A3B8]" />
                          Rename
                        </button>
                        <button
                          role="menuitem"
                          type="button"
                          onClick={() => confirmDelete(conv.id)}
                          className="flex w-full items-center gap-2.5 px-3 py-2 text-xs text-red-400 transition-colors hover:bg-red-500/10"
                        >
                          <Trash2 size={13} />
                          Delete
                        </button>
                      </div>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          ))
        )}
      </nav>

      {/* Bottom profile section */}
      <div className="flex-shrink-0 border-t border-[#28415D] px-3 py-3">
        <div className="flex items-center gap-2.5">
          <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-[#142B45] text-[#94A3B8]">
            <User size={15} aria-hidden="true" />
          </div>
          <div className="min-w-0 flex-1">
            <p className="truncate text-xs font-medium text-[#F8FAFC]" title={email}>
              {email}
            </p>
            <p className="text-[10px] text-[#94A3B8]/60">ACME Corp</p>
          </div>
          <button
            type="button"
            onClick={onLogout}
            aria-label="Sign out"
            className="flex-shrink-0 rounded-lg p-1.5 text-[#94A3B8]/60 transition-colors hover:bg-red-500/10 hover:text-red-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-red-400"
          >
            <LogOut size={15} />
          </button>
        </div>
      </div>

      {/* Delete confirmation dialog */}
      {deleteConfirmId && (
        <div
          className="absolute inset-0 z-30 flex items-center justify-center bg-black/60 backdrop-blur-sm"
          role="dialog"
          aria-modal="true"
          aria-labelledby="delete-dialog-title"
        >
          <div className="mx-4 rounded-2xl border border-[#28415D] bg-[#0F2138] p-6 shadow-2xl">
            <h3
              id="delete-dialog-title"
              className="mb-2 text-sm font-semibold text-[#F8FAFC]"
            >
              Delete conversation?
            </h3>
            <p className="mb-5 text-xs leading-relaxed text-[#94A3B8]">
              This conversation will be permanently deleted and cannot be recovered.
            </p>
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => setDeleteConfirmId(null)}
                className="flex-1 rounded-lg border border-[#28415D] py-2 text-xs text-[#94A3B8] transition-colors hover:bg-[#142B45]"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={executeDelete}
                className="flex-1 rounded-lg bg-red-500 py-2 text-xs font-semibold text-white transition-colors hover:bg-red-600"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </aside>
  );
}
