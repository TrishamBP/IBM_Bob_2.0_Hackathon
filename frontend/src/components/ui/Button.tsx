import { ButtonHTMLAttributes, forwardRef } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  fullWidth?: boolean;
}

const variantClasses: Record<NonNullable<ButtonProps['variant']>, string> = {
  primary:
    'bg-[#38BDF8] text-[#081426] font-semibold hover:bg-[#7DD3FA] focus-visible:ring-[#38BDF8]',
  secondary:
    'bg-transparent text-[#38BDF8] font-semibold border border-[#38BDF8] hover:bg-[#38BDF8]/10 focus-visible:ring-[#38BDF8]',
  ghost:
    'bg-transparent text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-[#142B45] focus-visible:ring-[#38BDF8]',
};

const sizeClasses: Record<NonNullable<ButtonProps['size']>, string> = {
  sm: 'px-4 py-2 text-sm rounded-lg',
  md: 'px-6 py-2.5 text-sm rounded-lg',
  lg: 'px-8 py-3 text-base rounded-xl',
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    { variant = 'primary', size = 'md', fullWidth = false, className = '', children, ...props },
    ref
  ) => {
    return (
      <button
        ref={ref}
        className={[
          'inline-flex items-center justify-center gap-2 transition-colors duration-150',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-[#081426]',
          'disabled:opacity-50 disabled:cursor-not-allowed',
          variantClasses[variant],
          sizeClasses[size],
          fullWidth ? 'w-full' : '',
          className,
        ]
          .filter(Boolean)
          .join(' ')}
        {...props}
      >
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';
