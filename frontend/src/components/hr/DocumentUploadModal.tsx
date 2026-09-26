'use client';

import {
  useState,
  useEffect,
  useCallback,
  useRef,
  KeyboardEvent,
} from 'react';
import { X, Upload } from 'lucide-react';
import { DepartmentSelect } from './DepartmentSelect';
import { FileDropzone } from './FileDropzone';
import { SelectedFileList } from './SelectedFileList';
import { UploadProgress } from './UploadProgress';
import { UploadSummary } from './UploadSummary';
import { Button } from '@/components/ui/Button';
import { uploadBatch } from '@/lib/api/documents';
import { createBatches, overallProgress } from '@/lib/upload/batching';
import type { Department, UploadFile, UploadPhase } from '@/types/documents';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

let _idCounter = 0;
function nextId(): string {
  return `uf-${++_idCounter}`;
}

function getExtension(name: string): string {
  const parts = name.split('.');
  return parts.length > 1 ? `.${parts[parts.length - 1].toLowerCase()}` : '';
}

function fileToUploadFile(file: File): UploadFile {
  return {
    id: nextId(),
    file,
    name: file.name,
    size: file.size,
    extension: getExtension(file.name),
    status: 'pending',
    transferProgress: 0,
  };
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

interface DocumentUploadModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function DocumentUploadModal({ isOpen, onClose }: DocumentUploadModalProps) {
  // Form state
  const [department, setDepartment] = useState<Department | ''>('');
  const [files, setFiles] = useState<UploadFile[]>([]);

  // Validation errors
  const [deptError, setDeptError] = useState('');
  const [filesError, setFilesError] = useState('');

  // Upload state
  const [phase, setPhase] = useState<UploadPhase>('idle');
  const [currentBatch, setCurrentBatch] = useState(0);
  const [totalBatches, setTotalBatches] = useState(0);
  const [statusMessage, setStatusMessage] = useState('');
  const [batchTransferProgress, setBatchTransferProgress] = useState(0);
  const [currentBatchSize, setCurrentBatchSize] = useState(0);

  // Abort controller ref
  const abortRef = useRef<AbortController | null>(null);

  // Close button / first focusable element
  const closeBtnRef = useRef<HTMLButtonElement>(null);
  const modalRef = useRef<HTMLDivElement>(null);

  // ---------------------------------------------------------------------------
  // Derived values
  // ---------------------------------------------------------------------------

  const isUploading = phase === 'uploading';
  const isDone = phase === 'done';
  const successCount = files.filter((f) => f.status === 'success').length;
  const failedCount = files.filter((f) => f.status === 'error').length;
  const processedCount = successCount + failedCount;

  const progress = overallProgress(
    processedCount,
    files.length,
    batchTransferProgress,
    currentBatchSize
  );

  // ---------------------------------------------------------------------------
  // File management
  // ---------------------------------------------------------------------------

  const handleFilesSelected = useCallback(
    (newFiles: File[]) => {
      setFilesError('');
      setFiles((prev) => {
        // Deduplicate by name + size
        const existingKeys = new Set(prev.map((f) => `${f.name}:${f.size}`));
        const deduplicated: UploadFile[] = [];
        const duplicates: string[] = [];

        for (const f of newFiles) {
          const key = `${f.name}:${f.size}`;
          if (existingKeys.has(key)) {
            duplicates.push(f.name);
          } else {
            existingKeys.add(key);
            deduplicated.push(fileToUploadFile(f));
          }
        }

        if (duplicates.length) {
          setFilesError(
            `Duplicate${duplicates.length > 1 ? 's' : ''} skipped: ${duplicates.join(', ')}`
          );
        }

        return [...prev, ...deduplicated];
      });
    },
    []
  );

  const handleRemoveFile = useCallback((id: string) => {
    setFiles((prev) => prev.filter((f) => f.id !== id));
    setFilesError('');
  }, []);

  // ---------------------------------------------------------------------------
  // Validate before upload
  // ---------------------------------------------------------------------------

  function validate(): boolean {
    let ok = true;
    if (!department) {
      setDeptError('Please select a department before uploading.');
      ok = false;
    }
    const pendingFiles = files.filter((f) => f.status === 'pending' || f.status === 'error');
    if (pendingFiles.length === 0) {
      setFilesError('Please add at least one file.');
      ok = false;
    }
    return ok;
  }

  // ---------------------------------------------------------------------------
  // Upload orchestration
  // ---------------------------------------------------------------------------

  async function startUpload(filesToUpload: UploadFile[]) {
    const batches = createBatches(filesToUpload);
    const nBatches = batches.length;

    setPhase('uploading');
    setTotalBatches(nBatches);
    setCurrentBatch(0);
    setStatusMessage('Preparing upload…');
    setBatchTransferProgress(0);

    abortRef.current = new AbortController();
    const { signal } = abortRef.current;

    // Mark all queued files as pending (re-try scenario: failed → pending)
    const idsToUpload = new Set(filesToUpload.map((f) => f.id));
    setFiles((prev) =>
      prev.map((f) => (idsToUpload.has(f.id) ? { ...f, status: 'pending', errorMessage: undefined, transferProgress: 0 } : f))
    );

    for (let bIdx = 0; bIdx < batches.length; bIdx++) {
      if (signal.aborted) break;

      const batch = batches[bIdx];
      const batchNum = bIdx + 1;

      setCurrentBatch(batchNum);
      setCurrentBatchSize(batch.length);
      setBatchTransferProgress(0);
      setStatusMessage(
        `Uploading batch ${batchNum} of ${nBatches} (${batch.length} file${batch.length !== 1 ? 's' : ''})`
      );

      // Mark batch files as uploading
      const batchIds = new Set(batch.map((f) => f.id));
      setFiles((prev) =>
        prev.map((f) => (batchIds.has(f.id) ? { ...f, status: 'uploading' } : f))
      );

      try {
        const result = await uploadBatch({
          department: department as Department,
          files: batch.map((f) => f.file),
          onTransferProgress: (pct) => setBatchTransferProgress(pct),
          signal,
        });

        // Build per-file error map from backend response
        const errorMap = new Map<string, string>();
        if (result.errors) {
          for (const e of result.errors) {
            errorMap.set(e.filename, e.message);
          }
        }

        setFiles((prev) =>
          prev.map((f) => {
            if (!batchIds.has(f.id)) return f;
            const errMsg = errorMap.get(f.name);
            return errMsg
              ? { ...f, status: 'error' as const, errorMessage: errMsg, transferProgress: 100 }
              : { ...f, status: 'success' as const, transferProgress: 100 };
          })
        );
      } catch (err) {
        if (signal.aborted) {
          // Mark remaining files in this batch as pending (not failed)
          setFiles((prev) =>
            prev.map((f) =>
              batchIds.has(f.id) && f.status === 'uploading'
                ? { ...f, status: 'pending' }
                : f
            )
          );
          break;
        }

        const message =
          err instanceof Error ? err.message : 'Upload failed — unknown error.';

        setFiles((prev) =>
          prev.map((f) =>
            batchIds.has(f.id)
              ? { ...f, status: 'error' as const, errorMessage: message }
              : f
          )
        );
      }

      setBatchTransferProgress(0);
    }

    setStatusMessage('');
    setPhase('done');
  }

  function handleUploadClick() {
    if (!validate()) return;
    const toUpload = files.filter((f) => f.status === 'pending');
    startUpload(toUpload);
  }

  function handleRetryFailed() {
    const failed = files.filter((f) => f.status === 'error');
    if (failed.length === 0) return;
    startUpload(failed);
  }

  // ---------------------------------------------------------------------------
  // Cancel / close guards
  // ---------------------------------------------------------------------------

  function handleCancelUpload() {
    abortRef.current?.abort();
  }

  function handleCloseAttempt() {
    if (isUploading) {
      if (window.confirm('An upload is in progress. Cancel and close?')) {
        handleCancelUpload();
        resetAndClose();
      }
      return;
    }
    resetAndClose();
  }

  function resetAndClose() {
    setDepartment('');
    setFiles([]);
    setDeptError('');
    setFilesError('');
    setPhase('idle');
    setCurrentBatch(0);
    setTotalBatches(0);
    setStatusMessage('');
    setBatchTransferProgress(0);
    setCurrentBatchSize(0);
    onClose();
  }

  // ---------------------------------------------------------------------------
  // Accessibility: focus trap & ESC key
  // ---------------------------------------------------------------------------

  useEffect(() => {
    if (!isOpen) return;
    // Focus the close button when the modal opens
    const timer = setTimeout(() => closeBtnRef.current?.focus(), 50);
    return () => clearTimeout(timer);
  }, [isOpen]);

  function handleKeyDown(e: KeyboardEvent<HTMLDivElement>) {
    if (e.key === 'Escape') handleCloseAttempt();
  }

  // Trap focus inside the modal
  function handleFocusTrap(e: KeyboardEvent<HTMLDivElement>) {
    if (e.key !== 'Tab' || !modalRef.current) return;
    const focusable = modalRef.current.querySelectorAll<HTMLElement>(
      'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
    );
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (e.shiftKey) {
      if (document.activeElement === first) {
        e.preventDefault();
        last?.focus();
      }
    } else {
      if (document.activeElement === last) {
        e.preventDefault();
        first?.focus();
      }
    }
  }

  // ---------------------------------------------------------------------------
  // Render
  // ---------------------------------------------------------------------------

  if (!isOpen) return null;

  return (
    /* Backdrop */
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6"
      role="dialog"
      aria-modal="true"
      aria-labelledby="upload-modal-title"
      onKeyDown={(e) => {
        handleKeyDown(e);
        handleFocusTrap(e);
      }}
    >
      {/* Overlay */}
      <div
        className="absolute inset-0 bg-black/70 backdrop-blur-sm"
        aria-hidden="true"
        onClick={handleCloseAttempt}
      />

      {/* Panel */}
      <div
        ref={modalRef}
        className="relative z-10 flex w-full max-w-2xl flex-col max-h-[90vh] overflow-hidden rounded-2xl border border-[#28415D] bg-[#0F2138] shadow-2xl"
      >
        {/* Modal header */}
        <div className="flex flex-shrink-0 items-center justify-between border-b border-[#28415D] px-6 py-5">
          <div>
            <h2
              id="upload-modal-title"
              className="text-xl font-bold text-[#F8FAFC]"
            >
              Upload Documents
            </h2>
            <p className="mt-0.5 text-xs text-[#94A3B8]">
              Select a department and upload onboarding documents.
            </p>
          </div>
          <button
            ref={closeBtnRef}
            type="button"
            onClick={handleCloseAttempt}
            aria-label="Close upload modal"
            className="ml-4 flex-shrink-0 rounded-lg p-2 text-[#94A3B8] transition-colors hover:bg-[#142B45] hover:text-[#F8FAFC] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#38BDF8]"
          >
            <X size={20} />
          </button>
        </div>

        {/* Scrollable body */}
        <div className="flex-1 overflow-y-auto px-6 py-6">
          {isDone ? (
            /* Summary view */
            <UploadSummary
              department={department}
              files={files}
              onRetryFailed={handleRetryFailed}
              onClose={resetAndClose}
            />
          ) : (
            /* Upload form */
            <div className="flex flex-col gap-6">
              {/* Department selector */}
              <DepartmentSelect
                value={department}
                onChange={(v) => {
                  setDepartment(v);
                  if (deptError) setDeptError('');
                }}
                error={deptError}
                disabled={isUploading}
              />

              {/* Dropzone */}
              <FileDropzone
                onFilesSelected={handleFilesSelected}
                disabled={isUploading}
                error={filesError}
              />

              {/* File list */}
              {files.length > 0 && (
                <SelectedFileList
                  files={files}
                  onRemove={handleRemoveFile}
                  uploading={isUploading}
                />
              )}

              {/* Upload progress */}
              {isUploading && (
                <UploadProgress
                  overallProgress={progress}
                  currentBatch={currentBatch}
                  totalBatches={totalBatches}
                  successCount={successCount}
                  failedCount={failedCount}
                  totalFiles={files.length}
                  statusMessage={statusMessage}
                />
              )}
            </div>
          )}
        </div>

        {/* Footer actions — hidden when showing the summary (it has its own actions) */}
        {!isDone && (
          <div className="flex flex-shrink-0 items-center justify-end gap-3 border-t border-[#28415D] px-6 py-4">
            {isUploading ? (
              <Button
                variant="ghost"
                size="md"
                onClick={handleCancelUpload}
              >
                Cancel Upload
              </Button>
            ) : (
              <>
                <Button variant="ghost" size="md" onClick={handleCloseAttempt}>
                  Cancel
                </Button>
                <Button
                  variant="primary"
                  size="md"
                  onClick={handleUploadClick}
                  disabled={isUploading}
                >
                  <Upload size={16} />
                  Upload Documents
                </Button>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
