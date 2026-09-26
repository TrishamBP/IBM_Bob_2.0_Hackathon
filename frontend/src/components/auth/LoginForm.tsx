'use client';

import { useState, FormEvent } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { ArrowLeft } from 'lucide-react';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { setSession } from '@/lib/auth';
import { validateHREmail, validateEmployeeEmail } from '@/lib/validation';
import type { UserRole } from '@/types/auth';

interface LoginFormProps {
  role: UserRole;
  /** Page heading, e.g. "HR Portal" */
  heading: string;
  /** Short description shown beneath the heading */
  description: string;
  /** Route to redirect to on success */
  redirectTo: string;
  /** Label and href for the "switch portal" link */
  switchLink: { label: string; href: string };
}

export function LoginForm({
  role,
  heading,
  description,
  redirectTo,
  switchLink,
}: LoginFormProps) {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Validation is resolved inside the client component — no function prop crossing the boundary
  const validateEmail = role === 'hr' ? validateHREmail : validateEmployeeEmail;

  function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError('');

    const result = validateEmail(email);
    if (!result.valid) {
      setError(result.error ?? 'Invalid email address.');
      return;
    }

    setLoading(true);
    // Simulate a brief network delay for UX
    setTimeout(() => {
      setSession({ email: email.trim(), role });
      router.push(redirectTo);
    }, 400);
  }

  return (
    <div>
      {/* Back link */}
      <Link
        href="/"
        className="mb-8 inline-flex items-center gap-1.5 text-sm text-[#94A3B8] transition-colors hover:text-[#F8FAFC]"
      >
        <ArrowLeft size={16} />
        Back to Home
      </Link>

      {/* Card */}
      <div className="rounded-2xl border border-[#28415D] bg-[#0F2138] p-8">
        {/* Role badge */}
        <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-[#38BDF8]/30 bg-[#38BDF8]/10 px-3 py-1">
          <span className="h-1.5 w-1.5 rounded-full bg-[#38BDF8]" aria-hidden="true" />
          <span className="text-xs font-medium uppercase tracking-wider text-[#38BDF8]">
            {role === 'hr' ? 'HR Portal' : 'Employee Portal'}
          </span>
        </div>

        <h1 className="mb-2 text-2xl font-bold text-[#F8FAFC]">{heading}</h1>
        <p className="mb-8 text-sm leading-relaxed text-[#94A3B8]">{description}</p>

        <form onSubmit={handleSubmit} noValidate>
          <div className="mb-6">
            <Input
              id="email"
              label="Work Email"
              type="email"
              placeholder={role === 'hr' ? 'you@hr.com' : 'you@acmecorp.com'}
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                if (error) setError('');
              }}
              error={error}
              autoComplete="email"
              autoFocus
              required
            />
          </div>

          <Button
            type="submit"
            variant="primary"
            size="lg"
            fullWidth
            disabled={loading}
          >
            {loading ? 'Signing in…' : 'Continue'}
          </Button>
        </form>

        {/* Switch portal */}
        <p className="mt-6 text-center text-sm text-[#94A3B8]">
          {role === 'hr' ? 'Not an HR member?' : 'Looking for the HR portal?'}{' '}
          <Link
            href={switchLink.href}
            className="font-medium text-[#38BDF8] transition-colors hover:text-[#7DD3FA]"
          >
            {switchLink.label}
          </Link>
        </p>
      </div>

      {/* Disclaimer */}
      <p className="mt-6 text-center text-xs leading-relaxed text-[#94A3B8]/60">
        This is a demonstration-only authentication system.
        <br />
        Do not enter real or sensitive credentials.
      </p>
    </div>
  );
}
