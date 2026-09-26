import type { Metadata } from 'next';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { HeroSection } from '@/components/landing/HeroSection';
import { FeatureSection } from '@/components/landing/FeatureSection';
import { HowItWorks } from '@/components/landing/HowItWorks';

export const metadata: Metadata = {
  title: 'ACME Onboard — Employee Onboarding Portal',
  description:
    'One place to access your onboarding documents, set up your workspace, connect with your team and get ready for your first day at ACME Corp.',
};

export default function HomePage() {
  return (
    <>
      <Navbar />
      <main id="main-content">
        <HeroSection />
        <FeatureSection />
        <HowItWorks />
      </main>
      <Footer />
    </>
  );
}
