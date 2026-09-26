import type { Metadata } from 'next';
import { AuthLayout } from '@/components/auth/AuthLayout';
import { LoginForm } from '@/components/auth/LoginForm';

export const metadata: Metadata = {
  title: 'HR Login — ACME Onboard',
  description: 'Sign in to the ACME Corp HR Portal.',
};

export default function HRLoginPage() {
  return (
    <AuthLayout>
      <LoginForm
        role="hr"
        heading="Welcome back"
        description="Sign in with your HR email address to access the ACME HR Portal and manage employee onboarding."
        redirectTo="/hr/dashboard"
        switchLink={{ label: 'Employee Login', href: '/employee/login' }}
      />
    </AuthLayout>
  );
}
