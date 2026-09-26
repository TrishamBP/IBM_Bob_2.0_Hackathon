import Link from 'next/link';
import { Box } from 'lucide-react';
import { ReactNode } from 'react';

interface AuthLayoutProps {
  children: ReactNode;
}

export function AuthLayout({ children }: AuthLayoutProps) {
  return (
    <div className="flex min-h-screen flex-col bg-[#081426]">
      {/* Top bar */}
      <header className="border-b border-[#28415D] bg-[#081426]/95 backdrop-blur-sm">
        <div className="mx-auto flex max-w-7xl items-center px-4 py-4 sm:px-6 lg:px-8">
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
        </div>
      </header>

      {/* Content */}
      <main className="flex flex-1 items-center justify-center px-4 py-16 sm:px-6 lg:px-8">
        <div className="w-full max-w-md">{children}</div>
      </main>

      {/* Footer */}
      <footer className="border-t border-[#28415D] py-5 text-center">
        <p className="text-xs text-[#94A3B8]">
          &copy; {new Date().getFullYear()} ACME Corp &mdash; Internal use only
        </p>
      </footer>
    </div>
  );
}
