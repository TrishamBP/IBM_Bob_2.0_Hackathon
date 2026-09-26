import { FileText, Monitor, Link2 } from 'lucide-react';

const features = [
  {
    icon: FileText,
    title: 'Seamless Onboarding',
    description:
      'Access essential documents, onboarding activities and company resources — all organized and ready from day one.',
  },
  {
    icon: Monitor,
    title: 'Your Digital Workspace',
    description:
      'Discover your tools, development environment and team-specific resources to hit the ground running.',
  },
  {
    icon: Link2,
    title: 'One Connected Experience',
    description:
      'Connect with HR, IT and your team throughout your onboarding journey in one unified platform.',
  },
];

export function FeatureSection() {
  return (
    <section
      id="about"
      className="bg-[#0F2138] py-24"
      aria-labelledby="features-heading"
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <div className="mx-auto max-w-2xl text-center">
          <p className="mb-3 text-xs font-semibold uppercase tracking-wider text-[#38BDF8]">
            Why ACME Onboard
          </p>
          <h2
            id="features-heading"
            className="text-3xl font-bold tracking-tight text-[#F8FAFC] sm:text-4xl"
          >
            Everything you need to get started
          </h2>
          <p className="mt-4 text-base leading-relaxed text-[#94A3B8]">
            A purpose-built portal designed to make your first weeks at ACME productive,
            connected and stress-free.
          </p>
        </div>

        {/* Feature cards */}
        <div className="mt-16 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {features.map(({ icon: Icon, title, description }) => (
            <div
              key={title}
              className="group rounded-xl border border-[#28415D] bg-[#142B45] p-8 transition-colors duration-200 hover:border-[#38BDF8]/40"
            >
              <div className="mb-5 inline-flex h-12 w-12 items-center justify-center rounded-xl border border-[#28415D] bg-[#0F2138] transition-colors group-hover:border-[#38BDF8]/40 group-hover:bg-[#38BDF8]/10">
                <Icon size={22} className="text-[#38BDF8]" />
              </div>
              <h3 className="mb-3 text-base font-semibold text-[#F8FAFC]">{title}</h3>
              <p className="text-sm leading-relaxed text-[#94A3B8]">{description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
