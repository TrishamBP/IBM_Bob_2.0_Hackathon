'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Box, LogOut, Users, FileUp, Upload } from 'lucide-react';
import { getSession, clearSession } from '@/lib/auth';
import { DocumentUploadModal } from '@/components/hr/DocumentUploadModal';
import type { MockSession } from '@/types/auth';

export default function HRDashboardPage() {
  const router = useRouter();
  // Lazy initializer — read session once on mount, no setState-in-effect
  const [session] = useState<MockSession | null>(() =>
    typeof window !== 'undefined' ? getSession() : null
  );
  const [modalOpen, setModalOpen] = useState(false);

  // Redirect if unauthenticated or wrong role
  useEffect(() => {
    if (!session || session.role !== 'hr') {
      router.replace(session ? '/employee/dashboard' : '/hr/login');
    }
  }, [session, router]);

  function handleLogout() {
    clearSession();
    router.push('/hr/login');
  }

  // Don't render anything until we know the user is valid
  if (!session || session.role !== 'hr') return null;

  return (
    <div className="flex min-h-screen flex-col bg-[#081426]">
      {/* ------------------------------------------------------------------ */}
      {/* Header                                                               */}
      {/* ------------------------------------------------------------------ */}
      <header className="border-b border-[#28415D] bg-[#0F2138]">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          {/* Logo */}
          <Link
            href="/"
            className="flex items-center gap-2.5 group"
            aria-label="ACME Onboard Home"
          >
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#38BDF8] text-[#081426] transition-colors group-hover:bg-[#7DD3FA]">
              <Box size={18} strokeWidth={2.5} />
            </span>
            <span className="text-base font-bold text-[#F8FAFC]">
              ACME <span className="text-[#38BDF8]">Onboard</span>
            </span>
          </Link>

          {/* Right side */}
          <div className="flex items-center gap-3">
            {/* HR badge */}
            <span className="hidden items-center gap-2 rounded-full border border-[#38BDF8]/30 bg-[#38BDF8]/10 px-3 py-1 sm:inline-flex">
              <span className="h-1.5 w-1.5 rounded-full bg-[#38BDF8]" aria-hidden="true" />
              <span className="text-xs font-medium text-[#38BDF8]">HR Portal</span>
            </span>

            {/* Email */}
            <span className="hidden text-sm text-[#94A3B8] lg:block" title={session.email}>
              {session.email}
            </span>

            {/* Logout */}
            <button
              onClick={handleLogout}
              className="inline-flex items-center gap-2 rounded-lg border border-[#28415D] px-4 py-2 text-sm text-[#94A3B8] transition-colors hover:border-red-500/40 hover:bg-red-500/10 hover:text-red-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-red-400"
            >
              <LogOut size={16} />
              <span className="hidden sm:inline">Sign out</span>
            </button>
          </div>
        </div>
      </header>

      {/* ------------------------------------------------------------------ */}
      {/* Main content                                                         */}
      {/* ------------------------------------------------------------------ */}
      <main className="mx-auto w-full max-w-7xl flex-1 px-4 py-10 sm:px-6 lg:px-8">
        {/* Page title */}
        <div className="mb-8">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-[#28415D] bg-[#142B45]">
              <Users size={20} className="text-[#38BDF8]" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-[#F8FAFC]">HR Dashboard</h1>
              <p className="text-xs text-[#94A3B8]">Signed in as {session.email}</p>
            </div>
          </div>
        </div>

        {/* ---------------------------------------------------------------- */}
        {/* Document Management section                                       */}
        {/* ---------------------------------------------------------------- */}
        <section aria-labelledby="doc-management-heading">
          <div className="rounded-2xl border border-[#28415D] bg-[#0F2138]">
            {/* Section header */}
            <div className="border-b border-[#28415D] px-6 py-5">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div className="flex items-center gap-3">
                  <div className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-lg border border-[#28415D] bg-[#142B45]">
                    <FileUp size={18} className="text-[#38BDF8]" />
                  </div>
                  <div>
                    <h2
                      id="doc-management-heading"
                      className="text-base font-semibold text-[#F8FAFC]"
                    >
                      Document Management
                    </h2>
                    <p className="text-xs text-[#94A3B8]">
                      Upload company onboarding documents for employees across all departments.
                    </p>
                  </div>
                </div>

                {/* Upload button */}
                <button
                  type="button"
                  onClick={() => setModalOpen(true)}
                  className="inline-flex flex-shrink-0 items-center gap-2 rounded-xl bg-[#38BDF8] px-5 py-2.5 text-sm font-semibold text-[#081426] transition-colors hover:bg-[#7DD3FA] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#38BDF8] focus-visible:ring-offset-2 focus-visible:ring-offset-[#081426]"
                >
                  <Upload size={16} />
                  Upload Documents
                </button>
              </div>
            </div>

            {/* Empty state body */}
            <div className="flex flex-col items-center justify-center px-6 py-16 text-center">
              <div className="mb-5 flex h-16 w-16 items-center justify-center rounded-2xl border border-[#28415D] bg-[#142B45]">
                <FileUp size={28} className="text-[#38BDF8]/60" />
              </div>
              <h3 className="mb-2 text-sm font-semibold text-[#F8FAFC]">
                No documents uploaded yet
              </h3>
              <p className="mb-6 max-w-xs text-xs leading-relaxed text-[#94A3B8]">
                Upload PDF, Word, Markdown or plain-text files to make them available to employees
                during onboarding.
              </p>
              <button
                type="button"
                onClick={() => setModalOpen(true)}
                className="inline-flex items-center gap-2 rounded-xl border border-[#38BDF8]/40 px-5 py-2.5 text-sm font-medium text-[#38BDF8] transition-colors hover:bg-[#38BDF8]/10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#38BDF8] focus-visible:ring-offset-2 focus-visible:ring-offset-[#081426]"
              >
                <Upload size={15} />
                Upload your first document
              </button>
            </div>
          </div>
        </section>
      </main>

      {/* ------------------------------------------------------------------ */}
      {/* Upload Modal                                                         */}
      {/* ------------------------------------------------------------------ */}
      <DocumentUploadModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
      />
    </div>
  );
}
