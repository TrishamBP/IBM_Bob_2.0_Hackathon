/**
 * localStorage persistence for chat conversations.
 *
 * Conversations are namespaced by employee email so different demo accounts
 * maintain separate histories.
 *
 * No confidential information is stored — only mock chat messages.
 */

import type { Conversation } from '@/types/chat';

function storageKey(email: string): string {
  // Sanitise the email so it's a safe localStorage key
  return `acme_chat_${email.toLowerCase().replace(/[^a-z0-9@.]/g, '_')}`;
}

export function loadConversations(email: string): Conversation[] {
  if (typeof window === 'undefined') return [];
  try {
    const raw = localStorage.getItem(storageKey(email));
    if (!raw) return [];
    const parsed = JSON.parse(raw) as Conversation[];
    // Basic shape guard
    if (!Array.isArray(parsed)) return [];
    return parsed;
  } catch {
    return [];
  }
}

export function saveConversations(email: string, conversations: Conversation[]): void {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(storageKey(email), JSON.stringify(conversations));
  } catch {
    // Storage quota exceeded or unavailable — silently ignore
  }
}

export function clearConversations(email: string): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(storageKey(email));
}
