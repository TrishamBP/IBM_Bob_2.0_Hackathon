'use client';

import { useSyncExternalStore } from 'react';
import { getSession, SESSION_KEY } from '@/lib/auth';
import type { MockSession } from '@/types/auth';

// Cache the parsed session by its raw value so getSnapshot returns a stable
// reference (useSyncExternalStore requires this to avoid infinite re-renders).
let cachedRaw: string | null = null;
let cachedSession: MockSession | null = null;

function getSnapshot(): MockSession | null {
  const raw = localStorage.getItem(SESSION_KEY);
  if (raw !== cachedRaw) {
    cachedRaw = raw;
    cachedSession = getSession();
  }
  return cachedSession;
}

// `undefined` = not yet known (SSR + hydration pass); `null` = no session.
function getServerSnapshot(): MockSession | null | undefined {
  return undefined;
}

function subscribe(onChange: () => void): () => void {
  window.addEventListener('storage', onChange);
  return () => window.removeEventListener('storage', onChange);
}

/**
 * Hydration-safe session reader. Returns `undefined` on the server and during
 * hydration so the server and client markup match, then the real session.
 */
export function useSession(): MockSession | null | undefined {
  return useSyncExternalStore<MockSession | null | undefined>(
    subscribe,
    getSnapshot,
    getServerSnapshot
  );
}
