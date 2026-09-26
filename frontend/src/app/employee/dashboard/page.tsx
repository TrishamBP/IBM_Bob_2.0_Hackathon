'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { getSession } from '@/lib/auth';
import { ChatLayout } from '@/components/chat/ChatLayout';
import type { MockSession } from '@/types/auth';

export default function EmployeeDashboardPage() {
  const router = useRouter();
  // Lazy initializer — read session once on mount
  const [session] = useState<MockSession | null>(() =>
    typeof window !== 'undefined' ? getSession() : null
  );

  // Redirect if unauthenticated or wrong role
  useEffect(() => {
    if (!session || session.role !== 'employee') {
      router.replace(session ? '/hr/dashboard' : '/employee/login');
    }
  }, [session, router]);

  if (!session || session.role !== 'employee') return null;

  return <ChatLayout email={session.email} />;
}
