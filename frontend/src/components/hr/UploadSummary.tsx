'use client';

import { CheckCircle, XCircle, RefreshCw, FolderOpen } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import type { Department, UploadFile } from '@/types/documents';

interface UploadSummaryProps {
  department: Department | '';
  files: UploadFile[];
  onRetryFailed: () => void;
  onClose: () => void;
}

export function UploadSummary({ department, files, onRetryFailed, onClose }: UploadSummaryProps) {
  const total = files.length;
  const succeeded = files.filter((f) => f.status === 'success').length;
  const failed = files.filter((f) => f.status === 'error').length;
  const allSuccess = failed === 0;

  return (
    <div className="flex flex-col gap-6">
      {/* Status banner */}
      <div
        className={[
          'flex items-start gap-4 rounded-xl border p-5',
          allSuccess
            ? 'border-green-500/30 bg-green-500/10'
            : 'border-red-500/30 bg-red-500/10',
        ].join(' ')}
        role="status"
        aria-live="polite"
      >
        <span className="mt-0.5 flex-shrink-0" aria-hidden="true">
          {allSuccess ? (
            <CheckCircle size={22} className="text-green-400" />
          ) : (
            <XCircle size={22} className="text-red-400" />
          )}
        </span>
        <div>
          <p
            className={[
              'font-semibold text-sm',
              allSuccess ? 'text-green-300' : 'text-red-300',
            ].join(' ')}
          >
            {allSuccess
              ? 'All documents uploaded successfully'
              : `${failed} document${failed !== 1 ? 's' : ''} failed to upload`}
          </p>
          <p className="mt-1 text-xs text-[#94A3B8]">
            {allSuccess
              ? 'Documents have been sent to the backend for processing.'
              : 'Successfully uploaded files have been processed. You can retry only the failed files.'}
          </p>
        </div>
      </div>

      {/* Summary stats */}
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        {[
          { label: 'Total selected', value: total, color: 'text-[#F8FAFC]' },
          { label: 'Succeeded', value: succeeded, color: 'text-green-400' },
          { label: 'Failed', value: failed, color: failed > 0 ? 'text-red-400' : 'text-[#94A3B8]' },
          { label: 'Department', value: department || '—', color: 'text-[#38BDF8]' },
        ].map(({ label, value, color }) => (
          <div
            key={label}
            className="rounded-lg border border-[#28415D] bg-[#142B45] p-3 text-center"
          >
            <p className={`text-base font-bold truncate ${color}`}>{value}</p>
            <p className="mt-0.5 text-xs text-[#94A3B8]">{label}</p>
          </div>
        ))}
      </div>

      {/* Failed file list */}
      {failed > 0 && (
        <div>
          <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-[#94A3B8]">
            Failed files
          </h4>
          <ul className="max-h-40 overflow-y-auto rounded-xl border border-[#28415D] divide-y divide-[#28415D] bg-[#0F2138]">
            {files
              .filter((f) => f.status === 'error')
              .map((f) => (
                <li key={f.id} className="flex items-start gap-3 px-4 py-2.5">
                  <FolderOpen size={14} className="mt-0.5 flex-shrink-0 text-red-400" aria-hidden="true" />
                  <div className="min-w-0">
                    <p className="truncate text-xs font-medium text-[#F8FAFC]">{f.name}</p>
                    {f.errorMessage && (
                      <p className="text-xs text-red-400/80">{f.errorMessage}</p>
                    )}
                  </div>
                </li>
              ))}
          </ul>
        </div>
      )}

      {/* Actions */}
      <div className="flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
        <Button variant="ghost" size="md" onClick={onClose}>
          Close
        </Button>
        {failed > 0 && (
          <Button variant="secondary" size="md" onClick={onRetryFailed}>
            <RefreshCw size={15} />
            Retry Failed ({failed})
          </Button>
        )}
        {allSuccess && (
          <Button variant="primary" size="md" onClick={onClose}>
            Done
          </Button>
        )}
      </div>
    </div>
  );
}
