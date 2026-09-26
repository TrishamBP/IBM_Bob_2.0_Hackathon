'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Menu, X, Box } from 'lucide-react';

const navLinks = [
  { label: 'Home', href: '/' },
  { label: 'About', href: '/#about' },
];

export function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b border-[#28415D] bg-[#081426]/95 backdrop-blur-sm">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2.5 group" aria-label="ACME Onboard Home">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#38BDF8] text-[#081426] transition-colors group-hover:bg-[#7DD3FA]">
            <Box size={18} strokeWidth={2.5} />
          </span>
          <span className="text-base font-bold text-[#F8FAFC]">
            <span className="text-[#F8FAFC]">ACME</span>{' '}
            <span className="text-[#38BDF8]">Onboard</span>
          </span>
        </Link>

        {/* Desktop nav */}
        <nav className="hidden items-center gap-1 md:flex" aria-label="Main navigation">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="rounded-lg px-3 py-2 text-sm text-[#94A3B8] transition-colors hover:bg-[#142B45] hover:text-[#F8FAFC]"
            >
              {link.label}
            </Link>
          ))}
          <div className="mx-2 h-5 w-px bg-[#28415D]" aria-hidden="true" />
          <Link
            href="/hr/login"
            className="rounded-lg border border-[#28415D] px-4 py-2 text-sm text-[#94A3B8] transition-colors hover:border-[#38BDF8]/50 hover:bg-[#142B45] hover:text-[#F8FAFC]"
          >
            HR Login
          </Link>
          <Link
            href="/employee/login"
            className="ml-1 rounded-lg bg-[#38BDF8] px-4 py-2 text-sm font-semibold text-[#081426] transition-colors hover:bg-[#7DD3FA]"
          >
            Employee Login
          </Link>
        </nav>

        {/* Mobile toggle */}
        <button
          className="flex items-center justify-center rounded-lg p-2 text-[#94A3B8] transition-colors hover:bg-[#142B45] hover:text-[#F8FAFC] md:hidden"
          onClick={() => setMobileOpen((v) => !v)}
          aria-label={mobileOpen ? 'Close menu' : 'Open menu'}
          aria-expanded={mobileOpen}
        >
          {mobileOpen ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="border-t border-[#28415D] bg-[#0F2138] px-4 py-4 md:hidden">
          <nav className="flex flex-col gap-1" aria-label="Mobile navigation">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMobileOpen(false)}
                className="rounded-lg px-3 py-2.5 text-sm text-[#94A3B8] transition-colors hover:bg-[#142B45] hover:text-[#F8FAFC]"
              >
                {link.label}
              </Link>
            ))}
            <div className="my-2 border-t border-[#28415D]" />
            <Link
              href="/hr/login"
              onClick={() => setMobileOpen(false)}
              className="rounded-lg border border-[#28415D] px-3 py-2.5 text-center text-sm text-[#94A3B8] transition-colors hover:border-[#38BDF8]/50 hover:bg-[#142B45] hover:text-[#F8FAFC]"
            >
              HR Login
            </Link>
            <Link
              href="/employee/login"
              onClick={() => setMobileOpen(false)}
              className="mt-1 rounded-lg bg-[#38BDF8] px-3 py-2.5 text-center text-sm font-semibold text-[#081426] transition-colors hover:bg-[#7DD3FA]"
            >
              Employee Login
            </Link>
          </nav>
        </div>
      )}
    </header>
  );
}
