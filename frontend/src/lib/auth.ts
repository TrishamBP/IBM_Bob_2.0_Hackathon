import type { MockSession, UserRole } from '@/types/auth';

const SESSION_KEY = 'acme_mock_session';

export function setSession(session: MockSession): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem(SESSION_KEY, JSON.stringify(session));
}

export function getSession(): MockSession | null {
  if (typeof window === 'undefined') return null;
  try {
    const raw = localStorage.getItem(SESSION_KEY);
    if (!raw) return null;
    return JSON.parse(raw) as MockSession;
  } catch {
    return null;
  }
}

export function clearSession(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(SESSION_KEY);
}

export function hasRole(role: UserRole): boolean {
  const session = getSession();
  return session?.role === role;
}
