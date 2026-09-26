import type { Conversation, ChatMessage, SuggestedQuestion } from '@/types/chat';

// ---------------------------------------------------------------------------
// ID generation
// ---------------------------------------------------------------------------

let _seq = 0;
export function generateId(prefix: string): string {
  return `${prefix}_${Date.now()}_${++_seq}`;
}

// ---------------------------------------------------------------------------
// Conversation helpers
// ---------------------------------------------------------------------------

/** Derive a short display title from the first user message. */
export function titleFromMessage(content: string): string {
  const trimmed = content.trim().replace(/\s+/g, ' ');
  return trimmed.length > 60 ? `${trimmed.slice(0, 57)}…` : trimmed;
}

/** Create a brand-new empty conversation. */
export function createConversation(): Conversation {
  const now = Date.now();
  return {
    id: generateId('conv'),
    title: 'New conversation',
    createdAt: now,
    updatedAt: now,
    messages: [],
  };
}

// ---------------------------------------------------------------------------
// Date grouping for sidebar
// ---------------------------------------------------------------------------

export type DateGroup = 'Today' | 'Yesterday' | 'Previous 7 Days' | 'Older';

export function getDateGroup(timestamp: number): DateGroup {
  const now = new Date();
  const date = new Date(timestamp);

  const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime();
  const startOfYesterday = startOfToday - 86_400_000;
  const startOf7DaysAgo = startOfToday - 7 * 86_400_000;

  if (date.getTime() >= startOfToday) return 'Today';
  if (date.getTime() >= startOfYesterday) return 'Yesterday';
  if (date.getTime() >= startOf7DaysAgo) return 'Previous 7 Days';
  return 'Older';
}

export function groupConversations(
  conversations: Conversation[]
): Array<{ group: DateGroup; items: Conversation[] }> {
  const order: DateGroup[] = ['Today', 'Yesterday', 'Previous 7 Days', 'Older'];
  const map = new Map<DateGroup, Conversation[]>();

  for (const conv of conversations) {
    const g = getDateGroup(conv.updatedAt);
    const arr = map.get(g) ?? [];
    arr.push(conv);
    map.set(g, arr);
  }

  return order
    .filter((g) => map.has(g))
    .map((g) => ({ group: g, items: map.get(g)! }));
}

// ---------------------------------------------------------------------------
// Time formatting
// ---------------------------------------------------------------------------

export function formatTimestamp(ts: number): string {
  const date = new Date(ts);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60_000);

  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins}m ago`;

  const diffHours = Math.floor(diffMins / 60);
  if (diffHours < 24) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
}

// ---------------------------------------------------------------------------
// Suggested questions
// ---------------------------------------------------------------------------

export const SUGGESTED_QUESTIONS: SuggestedQuestion[] = [
  {
    id: 'sq1',
    text: 'How do I set up my development environment?',
    icon: 'Code2',
  },
  {
    id: 'sq2',
    text: 'What documents do I need for onboarding?',
    icon: 'FileText',
  },
  {
    id: 'sq3',
    text: 'How do I configure my corporate VPN?',
    icon: 'Shield',
  },
  {
    id: 'sq4',
    text: 'Where can I find the leave policy?',
    icon: 'CalendarDays',
  },
  {
    id: 'sq5',
    text: 'How do I request access to a repository?',
    icon: 'GitBranch',
  },
  {
    id: 'sq6',
    text: 'How do I set up GitHub Copilot?',
    icon: 'Bot',
  },
];

// ---------------------------------------------------------------------------
// Message helpers
// ---------------------------------------------------------------------------

export function createUserMessage(content: string): ChatMessage {
  return {
    id: generateId('msg'),
    role: 'user',
    content,
    timestamp: Date.now(),
    status: 'complete',
  };
}

export function createAssistantPlaceholder(): ChatMessage {
  return {
    id: generateId('msg'),
    role: 'assistant',
    content: '',
    timestamp: Date.now(),
    status: 'pending',
  };
}
