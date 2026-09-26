'use client';

import { useRef, useState, DragEvent, ChangeEvent } from 'react';
import { UploadCloud } from 'lucide-react';
import {
  ACCEPTED_MIME_TYPES,
  ACCEPTED_EXTENSIONS,
  MAX_FILE_SIZE_BYTES,
} from '@/types/documents';

interface FileDropzoneProps {
  onFilesSelected: (files: File[]) => void;
  disabled?: boolean;
  /** Validation error passed from the parent (e.g. "No files selected"). */
  error?: string;
}

/** Human-readable label for the accept attribute. */
const ACCEPT_LABEL = 'PDF, DOCX, MD or TXT';

/** Build the <input accept="…"> string. */
const ACCEPT_ATTR = [
  ...Object.keys(ACCEPTED_MIME_TYPES),
  ...ACCEPTED_EXTENSIONS,
].join(',');

function getExtension(file: File): string {
  const parts = file.name.split('.');
  return parts.length > 1 ? `.${parts[parts.length - 1].toLowerCase()}` : '';
}

function isAccepted(file: File): boolean {
  if (ACCEPTED_MIME_TYPES[file.type]) return true;
  const ext = getExtension(file);
  return (ACCEPTED_EXTENSIONS as readonly string[]).includes(ext);
}

export function FileDropzone({ onFilesSelected, disabled = false, error }: FileDropzoneProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const [dropError, setDropError] = useState('');

  function processFiles(rawFiles: FileList | File[]) {
    setDropError('');
    const fileArr = Array.from(rawFiles);

    const rejected: string[] = [];
    const tooLarge: string[] = [];
    const accepted: File[] = [];

    for (const f of fileArr) {
      if (!isAccepted(f)) {
        rejected.push(f.name);
      } else if (f.size > MAX_FILE_SIZE_BYTES) {
        tooLarge.push(f.name);
      } else {
        accepted.push(f);
      }
    }

    const msgs: string[] = [];
    if (rejected.length) {
      msgs.push(
        `Unsupported file type${rejected.length > 1 ? 's' : ''}: ${rejected.join(', ')}`
      );
    }
    if (tooLarge.length) {
      const mb = MAX_FILE_SIZE_BYTES / (1024 * 1024);
      msgs.push(
        `File${tooLarge.length > 1 ? 's' : ''} exceed ${mb} MB limit: ${tooLarge.join(', ')}`
      );
    }
    if (msgs.length) setDropError(msgs.join(' • '));
    if (accepted.length) onFilesSelected(accepted);
  }

  function handleDragOver(e: DragEvent<HTMLDivElement>) {
    e.preventDefault();
    if (!disabled) setDragging(true);
  }

  function handleDragLeave(e: DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setDragging(false);
  }

  function handleDrop(e: DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setDragging(false);
    if (disabled) return;
    processFiles(e.dataTransfer.files);
  }

  function handleInputChange(e: ChangeEvent<HTMLInputElement>) {
    if (e.target.files) processFiles(e.target.files);
    // Reset so the same file can be re-selected after removal
    e.target.value = '';
  }

  const displayError = dropError || error;

  return (
    <div className="flex flex-col gap-1.5">
      {/* Drop zone */}
      <div
        role="button"
        tabIndex={disabled ? -1 : 0}
        aria-label="Drop files here or click to browse"
        aria-disabled={disabled}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !disabled && inputRef.current?.click()}
        onKeyDown={(e) => {
          if (!disabled && (e.key === 'Enter' || e.key === ' ')) {
            e.preventDefault();
            inputRef.current?.click();
          }
        }}
        className={[
          'flex flex-col items-center justify-center gap-3 rounded-xl border-2 border-dashed px-6 py-10',
          'cursor-pointer select-none transition-colors duration-150',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#38BDF8] focus-visible:ring-offset-2 focus-visible:ring-offset-[#081426]',
          disabled
            ? 'cursor-not-allowed opacity-50 border-[#28415D]'
            : dragging
            ? 'border-[#38BDF8] bg-[#38BDF8]/10'
            : displayError
            ? 'border-red-500/60 bg-[#0F2138]'
            : 'border-[#28415D] bg-[#0F2138] hover:border-[#38BDF8]/60 hover:bg-[#38BDF8]/5',
        ]
          .filter(Boolean)
          .join(' ')}
      >
        <UploadCloud
          size={36}
          className={dragging ? 'text-[#38BDF8]' : 'text-[#38BDF8]/70'}
          aria-hidden="true"
        />
        <div className="text-center">
          <p className="text-sm font-semibold text-[#F8FAFC]">
            Drag and drop your files here
          </p>
          <p className="mt-1 text-xs text-[#94A3B8]">{ACCEPT_LABEL}</p>
        </div>
        <button
          type="button"
          tabIndex={-1}
          disabled={disabled}
          onClick={(e) => {
            e.stopPropagation();
            if (!disabled) inputRef.current?.click();
          }}
          className="rounded-lg border border-[#28415D] bg-[#142B45] px-4 py-2 text-xs font-medium text-[#F8FAFC] transition-colors hover:border-[#38BDF8]/50 hover:bg-[#142B45]/80 disabled:cursor-not-allowed disabled:opacity-50"
        >
          Browse Files
        </button>
      </div>

      {/* Hidden file input */}
      <input
        ref={inputRef}
        type="file"
        multiple
        accept={ACCEPT_ATTR}
        className="sr-only"
        aria-hidden="true"
        tabIndex={-1}
        onChange={handleInputChange}
      />

      {/* Error */}
      {displayError && (
        <p role="alert" className="text-xs text-red-400">
          {displayError}
        </p>
      )}
    </div>
  );
}
