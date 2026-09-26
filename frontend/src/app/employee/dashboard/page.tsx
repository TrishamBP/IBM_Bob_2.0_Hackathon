'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { ChatLayout } from '@/components/chat/ChatLayout';
import { useSession } from '@/hooks/useSession';

export default function EmployeeDashboardPage() {
  const router = useRouter();
  // undefined while hydrating, then the stored session (or null)
  const session = useSession();

  // Redirect if unauthenticated or wrong role
  useEffect(() => {
    if (session === undefined) return;
    if (!session || session.role !== 'employee') {
      router.replace(session ? '/hr/dashboard' : '/employee/login');
    }
  }, [session, router]);

  if (!session || session.role !== 'employee') return null;

  return <ChatLayout email={session.email} />;
}
