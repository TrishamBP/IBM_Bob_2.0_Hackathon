import type { Metadata } from 'next';
import { AuthLayout } from '@/components/auth/AuthLayout';
import { LoginForm } from '@/components/auth/LoginForm';

export const metadata: Metadata = {
  title: 'Employee Login — ACME Onboard',
  description: 'Sign in to the ACME Corp Employee Portal.',
};

export default function EmployeeLoginPage() {
  return (
    <AuthLayout>
      <LoginForm
        role="employee"
        heading="Welcome to ACME"
        description="Sign in with your company email address to access your personalized onboarding experience."
        redirectTo="/employee/dashboard"
        switchLink={{ label: 'HR Login', href: '/hr/login' }}
      />
    </AuthLayout>
  );
}
