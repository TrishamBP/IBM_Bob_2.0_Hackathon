'use client';

import { FileText, X, CheckCircle, XCircle, Loader } from 'lucide-react';
import type { UploadFile, FileStatus } from '@/types/documents';

interface SelectedFileListProps {
  files: UploadFile[];
  onRemove: (id: string) => void;
  /** When true, the remove buttons are hidden (upload in progress or done). */
  uploading?: boolean;
}

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

const statusIcon: Record<FileStatus, React.ReactNode> = {
  pending: null,
  uploading: <Loader size={16} className="animate-spin text-[#38BDF8]" aria-label="Uploading" />,
  success: <CheckCircle size={16} className="text-green-400" aria-label="Uploaded successfully" />,
  error: <XCircle size={16} className="text-red-400" aria-label="Upload failed" />,
};

const statusLabel: Record<FileStatus, string> = {
  pending: '',
  uploading: 'Uploading…',
  success: 'Uploaded',
  error: 'Failed',
};

export function SelectedFileList({ files, onRemove, uploading = false }: SelectedFileListProps) {
  if (files.length === 0) return null;

  return (
    <div>
      {/* Header row */}
      <div className="mb-3 flex items-center justify-between">
        <h3 className="text-sm font-semibold text-[#F8FAFC]">Selected files</h3>
        <span className="rounded-full border border-[#28415D] bg-[#142B45] px-2.5 py-0.5 text-xs font-medium text-[#94A3B8]">
          {files.length} {files.length === 1 ? 'file' : 'files'}
        </span>
      </div>

      {/* Scrollable list */}
      <ul
        className="max-h-60 overflow-y-auto rounded-xl border border-[#28415D] divide-y divide-[#28415D] bg-[#0F2138]"
        aria-label="Selected files"
      >
        {files.map((uf) => (
          <li
            key={uf.id}
            className={[
              'flex items-center gap-3 px-4 py-3 transition-colors',
              uf.status === 'error' ? 'bg-red-500/5' : '',
              uf.status === 'success' ? 'bg-green-500/5' : '',
            ]
              .filter(Boolean)
              .join(' ')}
          >
            {/* File icon */}
            <span className="flex-shrink-0 text-[#38BDF8]" aria-hidden="true">
              <FileText size={16} />
            </span>

            {/* Name + meta */}
            <div className="min-w-0 flex-1">
              <p
                className="truncate text-sm font-medium text-[#F8FAFC]"
                title={uf.name}
              >
                {uf.name}
              </p>
              <p className="text-xs text-[#94A3B8]">
                {formatSize(uf.size)}&ensp;·&ensp;{uf.extension.toUpperCase().replace('.', '')}
                {uf.status !== 'pending' && (
                  <>
                    &ensp;·&ensp;
                    <span
                      className={
                        uf.status === 'error'
                          ? 'text-red-400'
                          : uf.status === 'success'
                          ? 'text-green-400'
                          : 'text-[#38BDF8]'
                      }
                    >
                      {statusLabel[uf.status]}
                    </span>
                  </>
                )}
              </p>
              {uf.status === 'error' && uf.errorMessage && (
                <p className="mt-0.5 text-xs text-red-400/80">{uf.errorMessage}</p>
              )}
            </div>

            {/* Status icon or remove button */}
            <div className="flex-shrink-0">
              {uf.status !== 'pending' ? (
                <span aria-hidden="true">{statusIcon[uf.status]}</span>
              ) : !uploading ? (
                <button
                  type="button"
                  onClick={() => onRemove(uf.id)}
                  aria-label={`Remove ${uf.name}`}
                  className="rounded p-0.5 text-[#94A3B8] transition-colors hover:bg-red-500/20 hover:text-red-400 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-red-400"
                >
                  <X size={14} />
                </button>
              ) : null}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
