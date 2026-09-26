// ---------------------------------------------------------------------------
// Message
// ---------------------------------------------------------------------------

export type MessageRole = 'user' | 'assistant';
export type MessageStatus = 'pending' | 'streaming' | 'complete' | 'error';

export interface SourceCitationData {
  id: string;
  title: string;
  department: string;
  /** e.g. "IT Handbook, Section 3.2" */
  reference: string;
  /** Optional URL — will be populated by the RAG pipeline in a future phase. */
  url?: string;
}

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: number; // Unix ms
  status: MessageStatus;
  /** Feedback set by the user locally. */
  feedback?: 'up' | 'down' | null;
  /** Source citations returned by the RAG backend (populated in future phase). */
  sources?: SourceCitationData[];
  /** True when this is a mock / demo response (not yet from the real backend). */
  isMock?: boolean;
}

// ---------------------------------------------------------------------------
// Conversation
// ---------------------------------------------------------------------------

export interface Conversation {
  id: string;
  title: string;
  createdAt: number; // Unix ms
  updatedAt: number; // Unix ms
  messages: ChatMessage[];
}

// ---------------------------------------------------------------------------
// Chat API / service contract
// ---------------------------------------------------------------------------

/** Request sent to the assistant service (mock or real). */
export interface AssistantRequest {
  conversationId: string;
  messages: Pick<ChatMessage, 'role' | 'content'>[];
}

/** Response from the assistant service. */
export interface AssistantResponse {
  content: string;
  sources?: SourceCitationData[];
  isMock?: boolean;
}

// ---------------------------------------------------------------------------
// Chat state (managed by useChat)
// ---------------------------------------------------------------------------

export interface ChatState {
  conversations: Conversation[];
  activeConversationId: string | null;
  isLoading: boolean;
  error: string | null;
}

// ---------------------------------------------------------------------------
// Suggested questions
// ---------------------------------------------------------------------------

export interface SuggestedQuestion {
  id: string;
  text: string;
  /** Lucide icon name string — resolved by the SuggestedQuestions component. */
  icon: string;
}
