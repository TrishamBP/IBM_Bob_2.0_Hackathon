import Link from 'next/link';
import { ArrowRight, Users, Layers, Network } from 'lucide-react';

export function HeroSection() {
  return (
    <section className="relative overflow-hidden bg-[#081426] py-24 sm:py-32" aria-label="Hero">
      {/* Subtle background grid */}
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage:
            'linear-gradient(#38BDF8 1px, transparent 1px), linear-gradient(90deg, #38BDF8 1px, transparent 1px)',
          backgroundSize: '60px 60px',
        }}
        aria-hidden="true"
      />

      {/* Soft radial glow */}
      <div
        className="pointer-events-none absolute left-1/2 top-0 -translate-x-1/2 h-[600px] w-[900px] rounded-full opacity-10"
        style={{
          background: 'radial-gradient(ellipse at center, #38BDF8 0%, transparent 70%)',
        }}
        aria-hidden="true"
      />

      <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl text-center">
          {/* Badge */}
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-[#38BDF8]/30 bg-[#38BDF8]/10 px-4 py-1.5">
            <span className="h-1.5 w-1.5 rounded-full bg-[#38BDF8]" aria-hidden="true" />
            <span className="text-xs font-medium uppercase tracking-wider text-[#38BDF8]">
              Welcome to ACME Corp
            </span>
          </div>

          {/* Headline */}
          <h1 className="text-4xl font-bold leading-tight tracking-tight text-[#F8FAFC] sm:text-5xl lg:text-6xl">
            Your journey at{' '}
            <span className="text-[#38BDF8]">ACME</span>{' '}
            starts here.
          </h1>

          {/* Supporting text */}
          <p className="mx-auto mt-6 max-w-xl text-base leading-relaxed text-[#94A3B8] sm:text-lg">
            One place to access your onboarding documents, set up your workspace, connect with
            your team and get ready for your first day.
          </p>

          {/* CTAs */}
          <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link
              href="/employee/login"
              className="inline-flex items-center gap-2 rounded-xl bg-[#38BDF8] px-8 py-3.5 text-base font-semibold text-[#081426] transition-colors hover:bg-[#7DD3FA] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#38BDF8] focus-visible:ring-offset-2 focus-visible:ring-offset-[#081426]"
            >
              Employee Portal
              <ArrowRight size={18} />
            </Link>
            <Link
              href="/hr/login"
              className="inline-flex items-center gap-2 rounded-xl border border-[#38BDF8] px-8 py-3.5 text-base font-semibold text-[#38BDF8] transition-colors hover:bg-[#38BDF8]/10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#38BDF8] focus-visible:ring-offset-2 focus-visible:ring-offset-[#081426]"
            >
              HR Portal
              <ArrowRight size={18} />
            </Link>
          </div>
        </div>

        {/* Abstract visual */}
        <div className="mx-auto mt-20 max-w-4xl" aria-hidden="true">
          <div className="relative rounded-2xl border border-[#28415D] bg-[#0F2138] p-8">
            {/* Top bar */}
            <div className="mb-6 flex items-center gap-2">
              <span className="h-3 w-3 rounded-full bg-red-500/60" />
              <span className="h-3 w-3 rounded-full bg-yellow-500/60" />
              <span className="h-3 w-3 rounded-full bg-green-500/60" />
              <span className="ml-3 text-xs text-[#94A3B8]/60">acme-onboard — dashboard</span>
            </div>

            {/* Mock dashboard grid */}
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
              <div className="rounded-xl border border-[#28415D] bg-[#142B45] p-5">
                <div className="flex items-center gap-3 mb-3">
                  <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#38BDF8]/20">
                    <Users size={18} className="text-[#38BDF8]" />
                  </div>
                  <span className="text-sm font-medium text-[#94A3B8]">Onboarding</span>
                </div>
                <div className="space-y-2">
                  <div className="h-2 w-3/4 rounded-full bg-[#28415D]" />
                  <div className="h-2 w-1/2 rounded-full bg-[#28415D]" />
                </div>
              </div>
              <div className="rounded-xl border border-[#28415D] bg-[#142B45] p-5">
                <div className="flex items-center gap-3 mb-3">
                  <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#38BDF8]/20">
                    <Layers size={18} className="text-[#38BDF8]" />
                  </div>
                  <span className="text-sm font-medium text-[#94A3B8]">Workspace</span>
                </div>
                <div className="space-y-2">
                  <div className="h-2 w-4/5 rounded-full bg-[#28415D]" />
                  <div className="h-2 w-2/3 rounded-full bg-[#28415D]" />
                </div>
              </div>
              <div className="rounded-xl border border-[#28415D] bg-[#142B45] p-5">
                <div className="flex items-center gap-3 mb-3">
                  <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#38BDF8]/20">
                    <Network size={18} className="text-[#38BDF8]" />
                  </div>
                  <span className="text-sm font-medium text-[#94A3B8]">Your Team</span>
                </div>
                <div className="space-y-2">
                  <div className="h-2 w-2/3 rounded-full bg-[#28415D]" />
                  <div className="h-2 w-1/2 rounded-full bg-[#28415D]" />
                </div>
              </div>
            </div>

            {/* Progress bar */}
            <div className="mt-6 rounded-xl border border-[#28415D] bg-[#142B45] p-5">
              <div className="mb-3 flex items-center justify-between">
                <span className="text-xs font-medium text-[#94A3B8]">Onboarding Progress</span>
                <span className="text-xs font-semibold text-[#38BDF8]">Day 1</span>
              </div>
              <div className="h-2 w-full rounded-full bg-[#28415D]">
                <div className="h-2 w-1/4 rounded-full bg-[#38BDF8]" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
