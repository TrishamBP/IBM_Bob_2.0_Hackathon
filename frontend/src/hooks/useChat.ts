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
import { getMockAssistantResponse } from '@/lib/chat/mockAssistant';

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

  /**
   * Resolves or creates a conversation, sends the user message,
   * then appends the assistant response.
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

      dispatch({ type: 'UPDATE_CONVERSATION', conversation: optimisticConv });
      dispatch({ type: 'SET_LOADING', loading: true });

      try {
        const historyForApi = optimisticConv.messages
          .filter((m) => m.status === 'complete' && m.role === 'user')
          .map((m) => ({ role: m.role, content: m.content }));

        const response = await getMockAssistantResponse({
          conversationId: convId!,
          messages: historyForApi,
        });

        // Read fresh state via ref to apply the update
        const freshConv = stateRef.current.conversations.find((c) => c.id === convId);
        if (freshConv) {
          const assistantMsg: ChatMessage = {
            ...placeholder,
            content: response.content,
            status: 'complete',
            sources: response.sources,
            isMock: response.isMock,
            timestamp: Date.now(),
          };
          const finalConv: Conversation = {
            ...freshConv,
            updatedAt: Date.now(),
            messages: freshConv.messages.map((m) =>
              m.id === placeholder.id ? assistantMsg : m
            ),
          };
          dispatch({ type: 'UPDATE_CONVERSATION', conversation: finalConv });
        }
      } catch (err) {
        const freshConv = stateRef.current.conversations.find((c) => c.id === convId);
        if (freshConv) {
          const errMsg: ChatMessage = {
            ...placeholder,
            content: 'Something went wrong. Please try again.',
            status: 'error',
            timestamp: Date.now(),
          };
          dispatch({
            type: 'UPDATE_CONVERSATION',
            conversation: {
              ...freshConv,
              messages: freshConv.messages.map((m) =>
                m.id === placeholder.id ? errMsg : m
              ),
            },
          });
        }
        dispatch({
          type: 'SET_ERROR',
          error: err instanceof Error ? err.message : 'Unknown error',
        });
      } finally {
        dispatch({ type: 'SET_LOADING', loading: false });
      }
    },
    [] // stateRef is always fresh — no deps needed
  );

  /** Regenerate the last assistant message. */
  const regenerateLastResponse = useCallback(async (conversationId: string) => {
    if (stateRef.current.isLoading) return;
    const conv = stateRef.current.conversations.find((c) => c.id === conversationId);
    if (!conv || conv.messages.length === 0) return;

    // Drop the last assistant message
    const withoutLast = conv.messages.slice(0, -1);
    const placeholder = createAssistantPlaceholder();

    const rebuiltConv: Conversation = {
      ...conv,
      updatedAt: Date.now(),
      messages: [...withoutLast, placeholder],
    };
    dispatch({ type: 'UPDATE_CONVERSATION', conversation: rebuiltConv });
    dispatch({ type: 'SET_LOADING', loading: true });

    try {
      const historyForApi = withoutLast
        .filter((m) => m.role === 'user')
        .map((m) => ({ role: m.role, content: m.content }));

      const response = await getMockAssistantResponse({
        conversationId,
        messages: historyForApi,
      });

      const freshConv = stateRef.current.conversations.find((c) => c.id === conversationId);
      if (freshConv) {
        const assistantMsg: ChatMessage = {
          ...placeholder,
          content: response.content,
          status: 'complete',
          sources: response.sources,
          isMock: response.isMock,
          timestamp: Date.now(),
        };
        dispatch({
          type: 'UPDATE_CONVERSATION',
          conversation: {
            ...freshConv,
            updatedAt: Date.now(),
            messages: freshConv.messages.map((m) =>
              m.id === placeholder.id ? assistantMsg : m
            ),
          },
        });
      }
    } catch {
      dispatch({ type: 'SET_ERROR', error: 'Regeneration failed. Please try again.' });
    } finally {
      dispatch({ type: 'SET_LOADING', loading: false });
    }
  }, []);

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
