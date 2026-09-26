'use client';

import { useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { getSession } from '@/lib/auth';
import type { UserRole } from '@/types/auth';

interface ProtectedRouteProps {
  requiredRole: UserRole;
  children: ReactNode;
}

export function ProtectedRoute({ requiredRole, children }: ProtectedRouteProps) {
  const router = useRouter();

  useEffect(() => {
    const session = getSession();

    if (!session) {
      router.replace(requiredRole === 'hr' ? '/hr/login' : '/employee/login');
      return;
    }

    if (session.role !== requiredRole) {
      // Wrong role — send them to their own dashboard
      router.replace(session.role === 'hr' ? '/hr/dashboard' : '/employee/dashboard');
    }
  }, [requiredRole, router]);

  const session = getSession();

  // Render nothing (and let the redirect fire) if there's no valid session
  if (!session || session.role !== requiredRole) {
    return null;
  }

  return <>{children}</>;
}
