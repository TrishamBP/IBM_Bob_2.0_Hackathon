'use client';

import { ChevronDown } from 'lucide-react';
import { DEPARTMENTS } from '@/types/documents';
import type { Department } from '@/types/documents';

interface DepartmentSelectProps {
  value: Department | '';
  onChange: (value: Department | '') => void;
  error?: string;
  disabled?: boolean;
}

export function DepartmentSelect({
  value,
  onChange,
  error,
  disabled = false,
}: DepartmentSelectProps) {
  const selectId = 'doc-department';

  return (
    <div className="flex flex-col gap-1.5">
      <label
        htmlFor={selectId}
        className="text-sm font-medium text-[#F8FAFC]"
      >
        Document Department <span className="text-red-400" aria-hidden="true">*</span>
        <span className="sr-only">(required)</span>
      </label>

      <div className="relative">
        <select
          id={selectId}
          value={value}
          onChange={(e) => onChange(e.target.value as Department | '')}
          disabled={disabled}
          aria-describedby={error ? `${selectId}-error` : undefined}
          aria-invalid={!!error}
          aria-required="true"
          className={[
            'w-full appearance-none rounded-lg border bg-[#0F2138] px-4 py-2.5 pr-10',
            'text-sm transition-colors duration-150',
            'focus:outline-none focus:ring-2 focus:ring-[#38BDF8] focus:border-[#38BDF8]',
            'disabled:cursor-not-allowed disabled:opacity-50',
            value === '' ? 'text-[#94A3B8]' : 'text-[#F8FAFC]',
            error
              ? 'border-red-500 focus:ring-red-500 focus:border-red-500'
              : 'border-[#28415D] hover:border-[#38BDF8]/50',
          ]
            .filter(Boolean)
            .join(' ')}
        >
          <option value="" disabled className="text-[#94A3B8]">
            Select a department
          </option>
          {DEPARTMENTS.map((dept) => (
            <option key={dept} value={dept} className="text-[#F8FAFC] bg-[#0F2138]">
              {dept}
            </option>
          ))}
        </select>

        {/* Custom chevron */}
        <span
          className="pointer-events-none absolute inset-y-0 right-3 flex items-center text-[#94A3B8]"
          aria-hidden="true"
        >
          <ChevronDown size={16} />
        </span>
      </div>

      {error && (
        <p id={`${selectId}-error`} role="alert" className="text-xs text-red-400">
          {error}
        </p>
      )}
    </div>
  );
}
