import Link from 'next/link';
import { Box } from 'lucide-react';

const currentYear = new Date().getFullYear();

export function Footer() {
  return (
    <footer className="border-t border-[#28415D] bg-[#0F2138]">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-4">
          {/* Brand */}
          <div className="col-span-1 sm:col-span-2 lg:col-span-1">
            <div className="flex items-center gap-2.5">
              <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#38BDF8] text-[#081426]">
                <Box size={18} strokeWidth={2.5} />
              </span>
              <span className="text-base font-bold text-[#F8FAFC]">
                ACME <span className="text-[#38BDF8]">Onboard</span>
              </span>
            </div>
            <p className="mt-4 text-sm leading-relaxed text-[#94A3B8]">
              The internal employee onboarding portal for ACME Corp. Streamlining every step of
              your journey from day one.
            </p>
          </div>

          {/* Product */}
          <div>
            <h3 className="mb-4 text-xs font-semibold uppercase tracking-wider text-[#94A3B8]">
              Product
            </h3>
            <ul className="space-y-2.5">
              <li>
                <Link href="/" className="text-sm text-[#94A3B8] transition-colors hover:text-[#F8FAFC]">
                  ACME Onboard
                </Link>
              </li>
              <li>
                <span className="text-sm text-[#94A3B8]/50 cursor-not-allowed">Employee Portal</span>
              </li>
              <li>
                <span className="text-sm text-[#94A3B8]/50 cursor-not-allowed">HR Portal</span>
              </li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="mb-4 text-xs font-semibold uppercase tracking-wider text-[#94A3B8]">
              Company
            </h3>
            <ul className="space-y-2.5">
              <li>
                <span className="text-sm text-[#94A3B8]/50 cursor-not-allowed">About ACME Corp</span>
              </li>
              <li>
                <span className="text-sm text-[#94A3B8]/50 cursor-not-allowed">Careers</span>
              </li>
              <li>
                <span className="text-sm text-[#94A3B8]/50 cursor-not-allowed">Blog</span>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="mb-4 text-xs font-semibold uppercase tracking-wider text-[#94A3B8]">
              Support
            </h3>
            <ul className="space-y-2.5">
              <li>
                <span className="text-sm text-[#94A3B8]/50 cursor-not-allowed">Help &amp; Support</span>
              </li>
              <li>
                <span className="text-sm text-[#94A3B8]/50 cursor-not-allowed">Privacy Policy</span>
              </li>
              <li>
                <span className="text-sm text-[#94A3B8]/50 cursor-not-allowed">Terms of Service</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-10 flex flex-col items-center justify-between gap-3 border-t border-[#28415D] pt-8 sm:flex-row">
          <p className="text-xs text-[#94A3B8]">
            &copy; {currentYear} ACME Corp. All rights reserved.
          </p>
          <p className="text-xs text-[#94A3B8]/60">
            Internal use only &mdash; ACME Onboarding Portal
          </p>
        </div>
      </div>
    </footer>
  );
}
