import { HTMLAttributes } from 'react';

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  hover?: boolean;
}

export function Card({ hover = false, className = '', children, ...props }: CardProps) {
  return (
    <div
      className={[
        'rounded-xl border border-[#28415D] bg-[#142B45] p-6',
        hover
          ? 'transition-colors duration-200 hover:border-[#38BDF8]/40 hover:bg-[#142B45]/80'
          : '',
        className,
      ]
        .filter(Boolean)
        .join(' ')}
      {...props}
    >
      {children}
    </div>
  );
}
