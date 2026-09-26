import { InputHTMLAttributes, forwardRef } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  id: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, id, className = '', ...props }, ref) => {
    return (
      <div className="flex flex-col gap-1.5">
        {label && (
          <label
            htmlFor={id}
            className="text-sm font-medium text-[#F8FAFC]"
          >
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={id}
          aria-describedby={error ? `${id}-error` : undefined}
          aria-invalid={!!error}
          className={[
            'w-full rounded-lg border bg-[#0F2138] px-4 py-2.5 text-sm text-[#F8FAFC]',
            'placeholder:text-[#94A3B8]',
            'transition-colors duration-150',
            'focus:outline-none focus:ring-2 focus:ring-[#38BDF8] focus:border-[#38BDF8]',
            error
              ? 'border-red-500 focus:ring-red-500 focus:border-red-500'
              : 'border-[#28415D] hover:border-[#38BDF8]/50',
            className,
          ]
            .filter(Boolean)
            .join(' ')}
          {...props}
        />
        {error && (
          <p
            id={`${id}-error`}
            role="alert"
            className="text-xs text-red-400"
          >
            {error}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
