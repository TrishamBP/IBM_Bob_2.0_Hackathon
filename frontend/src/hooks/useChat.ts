'use client';

import { useCallback, useEffect, useReducer, useRef } from 'react';
import type { ChatMessage, ChatState, Conversation } from '@/types/chat';
import {
  createConversation,
  createUserMessage,
  createAssistantPlaceholder,
  titleFromMessage,
} from '@/lib/chat/chatUtils';
import { loadConversations, saveConversations } from '@/lib/chat/chatStorage';
import { streamChat } from '@/lib/api/chat';

// ---------------------------------------------------------------------------
// Reducer
// ---------------------------------------------------------------------------

type Action =
  | { type: 'INIT'; conversations: Conversation[]; activeId: string | null }
  | { type: 'SET_ACTIVE'; id: string }
  | { type: 'ADD_CONVERSATION'; conversation: Conversation }
  | { type: 'UPDATE_CONVERSATION'; conversation: Conversation }
  | { type: 'DELETE_CONVERSATION'; id: string }
  | { type: 'SET_LOADING'; loading: boolean }
  | { type: 'SET_ERROR'; error: string | null };

function reducer(state: ChatState, action: Action): ChatState {
  switch (action.type) {
    case 'INIT':
      return {
        ...state,
        conversations: action.conversations,
        activeConversationId: action.activeId,
      };

    case 'SET_ACTIVE':
      return { ...state, activeConversationId: action.id, error: null };

    case 'ADD_CONVERSATION':
      return {
        ...state,
        conversations: [action.conversation, ...state.conversations],
        activeConversationId: action.conversation.id,
      };

    case 'UPDATE_CONVERSATION':
      return {
        ...state,
        conversations: state.conversations.map((c) =>
          c.id === action.conversation.id ? action.conversation : c
        ),
      };

    case 'DELETE_CONVERSATION': {
      const remaining = state.conversations.filter((c) => c.id !== action.id);
      const nextActive =
        state.activeConversationId === action.id
          ? (remaining[0]?.id ?? null)
          : state.activeConversationId;
      return { ...state, conversations: remaining, activeConversationId: nextActive };
    }

    case 'SET_LOADING':
      return { ...state, isLoading: action.loading };

    case 'SET_ERROR':
      return { ...state, error: action.error, isLoading: false };

    default:
      return state;
  }
}

const INITIAL_STATE: ChatState = {
  conversations: [],
  activeConversationId: null,
  isLoading: false,
  error: null,
};

// ---------------------------------------------------------------------------
// Hook
// ---------------------------------------------------------------------------

export function useChat(email: string) {
  const [state, dispatch] = useReducer(reducer, INITIAL_STATE);

  // Keep a ref to always-fresh state for async callbacks
  const stateRef = useRef(state);
  useEffect(() => {
    stateRef.current = state;
  });

  // Load from localStorage on mount
  useEffect(() => {
    if (!email) return;
    const stored = loadConversations(email);
    const sorted = [...stored].sort((a, b) => b.updatedAt - a.updatedAt);
    dispatch({
      type: 'INIT',
      conversations: sorted,
      activeId: sorted[0]?.id ?? null,
    });
  }, [email]);

  // Persist on every change
  useEffect(() => {
    if (!email) return;
    saveConversations(email, state.conversations);
  }, [email, state.conversations]);

  // ---------------------------------------------------------------------------
  // Derived
  // ---------------------------------------------------------------------------

  const activeConversation =
    state.conversations.find((c) => c.id === state.activeConversationId) ?? null;

  // ---------------------------------------------------------------------------
  // Actions
  // ---------------------------------------------------------------------------

  const newConversation = useCallback((): string => {
    const conv = createConversation();
    dispatch({ type: 'ADD_CONVERSATION', conversation: conv });
    return conv.id;
  }, []);

  const selectConversation = useCallback((id: string) => {
    dispatch({ type: 'SET_ACTIVE', id });
  }, []);

  const renameConversation = useCallback((id: string, title: string) => {
    const conv = stateRef.current.conversations.find((c) => c.id === id);
    if (!conv) return;
    const updated: Conversation = { ...conv, title: title.trim() || conv.title };
    dispatch({ type: 'UPDATE_CONVERSATION', conversation: updated });
  }, []);

  const deleteConversation = useCallback((id: string) => {
    dispatch({ type: 'DELETE_CONVERSATION', id });
  }, []);

  /** Applies `patch` to one message of a conversation, using fresh state. */
  const patchMessage = useCallback(
    (convId: string, messageId: string, patch: Partial<ChatMessage>, convPatch?: Partial<Conversation>) => {
      const conv = stateRef.current.conversations.find((c) => c.id === convId);
      if (!conv) return;
      const updated: Conversation = {
        ...conv,
        ...convPatch,
        messages: conv.messages.map((m) => (m.id === messageId ? { ...m, ...patch } : m)),
      };
      // Keep the ref in sync so rapid token updates don't clobber each other.
      stateRef.current = {
        ...stateRef.current,
        conversations: stateRef.current.conversations.map((c) => (c.id === convId ? updated : c)),
      };
      dispatch({ type: 'UPDATE_CONVERSATION', conversation: updated });
    },
    []
  );

  /** Streams the backend answer for `content` into the placeholder message. */
  const runTurn = useCallback(
    async (convId: string, placeholderId: string, content: string) => {
      dispatch({ type: 'SET_LOADING', loading: true });
      try {
        const conv = stateRef.current.conversations.find((c) => c.id === convId);
        const response = await streamChat({
          email,
          conversationId: conv?.serverId,
          message: content,
          onSession: (serverId) => patchMessage(convId, placeholderId, {}, { serverId }),
          onToken: (text) => patchMessage(convId, placeholderId, { content: text, status: 'streaming' }),
        });
        patchMessage(
          convId,
          placeholderId,
          {
            content: response.content,
            status: 'complete',
            sources: response.sources,
            timestamp: Date.now(),
          },
          { serverId: response.conversationId, updatedAt: Date.now() }
        );
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Something went wrong. Please try again.';
        patchMessage(convId, placeholderId, {
          content: message,
          status: 'error',
          timestamp: Date.now(),
        });
        dispatch({ type: 'SET_ERROR', error: message });
      } finally {
        dispatch({ type: 'SET_LOADING', loading: false });
      }
    },
    [email, patchMessage]
  );

  /**
   * Resolves or creates a conversation, sends the user message,
   * then streams the assistant response into a placeholder.
   */
  const sendMessage = useCallback(
    async (content: string, conversationId?: string) => {
      if (!content.trim() || stateRef.current.isLoading) return;

      const { conversations, activeConversationId } = stateRef.current;

      // Resolve or create the target conversation
      let convId = conversationId ?? activeConversationId;
      let conv = conversations.find((c) => c.id === convId);

      if (!conv) {
        conv = createConversation();
        convId = conv.id;
        dispatch({ type: 'ADD_CONVERSATION', conversation: conv });
      }

      const userMsg = createUserMessage(content.trim());
      const placeholder = createAssistantPlaceholder();
      const isFirstMessage = conv.messages.length === 0;

      const optimisticConv: Conversation = {
        ...conv,
        title: isFirstMessage ? titleFromMessage(content) : conv.title,
        updatedAt: Date.now(),
        messages: [...conv.messages, userMsg, placeholder],
      };

      stateRef.current = {
        ...stateRef.current,
        conversations: stateRef.current.conversations.some((c) => c.id === convId)
          ? stateRef.current.conversations.map((c) => (c.id === convId ? optimisticConv : c))
          : [optimisticConv, ...stateRef.current.conversations],
      };
      dispatch({ type: 'UPDATE_CONVERSATION', conversation: optimisticConv });

      await runTurn(convId!, placeholder.id, content.trim());
    },
    [runTurn]
  );

  /** Regenerate the last assistant message by re-asking the last user question. */
  const regenerateLastResponse = useCallback(
    async (conversationId: string) => {
      if (stateRef.current.isLoading) return;
      const conv = stateRef.current.conversations.find((c) => c.id === conversationId);
      if (!conv || conv.messages.length === 0) return;

      const lastUser = [...conv.messages].reverse().find((m) => m.role === 'user');
      if (!lastUser) return;

      // Drop the last assistant message
      const withoutLast =
        conv.messages[conv.messages.length - 1].role === 'assistant'
          ? conv.messages.slice(0, -1)
          : conv.messages;
      const placeholder = createAssistantPlaceholder();

      const rebuiltConv: Conversation = {
        ...conv,
        updatedAt: Date.now(),
        messages: [...withoutLast, placeholder],
      };
      stateRef.current = {
        ...stateRef.current,
        conversations: stateRef.current.conversations.map((c) =>
          c.id === conversationId ? rebuiltConv : c
        ),
      };
      dispatch({ type: 'UPDATE_CONVERSATION', conversation: rebuiltConv });

      await runTurn(conversationId, placeholder.id, lastUser.content);
    },
    [runTurn]
  );

  /** Set thumbs up/down feedback on a message. */
  const setMessageFeedback = useCallback(
    (conversationId: string, messageId: string, feedback: 'up' | 'down' | null) => {
      const conv = stateRef.current.conversations.find((c) => c.id === conversationId);
      if (!conv) return;
      dispatch({
        type: 'UPDATE_CONVERSATION',
        conversation: {
          ...conv,
          messages: conv.messages.map((m) =>
            m.id === messageId ? { ...m, feedback } : m
          ),
        },
      });
    },
    []
  );

  return {
    state,
    activeConversation,
    newConversation,
    selectConversation,
    renameConversation,
    deleteConversation,
    sendMessage,
    regenerateLastResponse,
    setMessageFeedback,
  };
}
