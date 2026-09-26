import { LogIn, LayoutDashboard, Rocket } from 'lucide-react';

const steps = [
  {
    number: '01',
    icon: LogIn,
    title: 'Sign in',
    description: 'Sign in using your company email address — no password required during setup.',
  },
  {
    number: '02',
    icon: LayoutDashboard,
    title: 'Your personalized experience',
    description:
      'Access your personalized onboarding dashboard with documents, tasks and resources tailored to your role.',
  },
  {
    number: '03',
    icon: Rocket,
    title: 'Get started with your team',
    description:
      'Meet your team, configure your workspace and complete your onboarding milestones.',
  },
];

export function HowItWorks() {
  return (
    <section className="bg-[#081426] py-24" aria-labelledby="how-it-works-heading">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <div className="mx-auto max-w-2xl text-center">
          <p className="mb-3 text-xs font-semibold uppercase tracking-wider text-[#38BDF8]">
            Getting started
          </p>
          <h2
            id="how-it-works-heading"
            className="text-3xl font-bold tracking-tight text-[#F8FAFC] sm:text-4xl"
          >
            How it works
          </h2>
          <p className="mt-4 text-base leading-relaxed text-[#94A3B8]">
            Three simple steps to begin your ACME journey.
          </p>
        </div>

        {/* Steps */}
        <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-3">
          {steps.map(({ number, icon: Icon, title, description }, index) => (
            <div key={number} className="relative flex flex-col items-center text-center sm:items-start sm:text-left">
              {/* Connector line (desktop) */}
              {index < steps.length - 1 && (
                <div
                  className="absolute left-[calc(50%+3rem)] top-6 hidden h-px w-[calc(100%-6rem)] bg-[#28415D] sm:block"
                  aria-hidden="true"
                />
              )}

              {/* Icon + number */}
              <div className="relative mb-6 flex h-14 w-14 items-center justify-center rounded-2xl border border-[#28415D] bg-[#142B45]">
                <Icon size={24} className="text-[#38BDF8]" />
                <span className="absolute -right-2 -top-2 flex h-5 w-5 items-center justify-center rounded-full bg-[#38BDF8] text-[10px] font-bold text-[#081426]">
                  {index + 1}
                </span>
              </div>

              <h3 className="mb-2 text-base font-semibold text-[#F8FAFC]">{title}</h3>
              <p className="text-sm leading-relaxed text-[#94A3B8]">{description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
