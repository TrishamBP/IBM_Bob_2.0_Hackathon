/** Departments that match the backend XGBoost router labels exactly. */
export const DEPARTMENTS = [
  'Human Resources',
  'IT Operations',
  'Information Security',
  'Software Engineering',
  'AI and Machine Learning',
  'Cloud Platform and DevOps',
  'Product Management',
  'UX and Design',
  'Quality Engineering',
  'Sales',
  'Customer Support',
  'Finance',
  'Legal and Compliance',
] as const;

export type Department = (typeof DEPARTMENTS)[number];

/** Accepted MIME types and extensions. */
export const ACCEPTED_MIME_TYPES: Record<string, string> = {
  'application/pdf': '.pdf',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
  'text/markdown': '.md',
  'text/plain': '.txt',
};

/** File extension fallback map (for files where MIME may be generic). */
export const ACCEPTED_EXTENSIONS = ['.pdf', '.docx', '.md', '.txt'] as const;

/** Maximum files per batch sent to the backend. */
export const BATCH_SIZE = 10;

/** Maximum individual file size in bytes (configurable; default 50 MB). */
export const MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024;

// ---------------------------------------------------------------------------
// Per-file state
// ---------------------------------------------------------------------------

export type FileStatus =
  | 'pending'     // waiting to be uploaded
  | 'uploading'   // actively transferring
  | 'success'     // backend confirmed receipt
  | 'error';      // network or backend error

export interface UploadFile {
  /** Stable unique identifier for React keys / matching. */
  id: string;
  file: File;
  name: string;
  size: number;
  extension: string;
  status: FileStatus;
  /** Backend error message, if any. */
  errorMessage?: string;
  /** Upload progress 0–100 for the current transfer (per-file within a batch). */
  transferProgress: number;
}

// ---------------------------------------------------------------------------
// Upload operation state
// ---------------------------------------------------------------------------

export type UploadPhase =
  | 'idle'        // not started
  | 'uploading'   // batches in progress
  | 'done';       // all batches finished

export interface UploadState {
  phase: UploadPhase;
  department: Department | '';
  files: UploadFile[];
  currentBatch: number;
  totalBatches: number;
  successCount: number;
  failedCount: number;
  /** Overall progress 0–100 (based on completed files). */
  overallProgress: number;
  /** Human-readable status line shown in the progress section. */
  statusMessage: string;
}

// ---------------------------------------------------------------------------
// API response
// ---------------------------------------------------------------------------

export interface UploadBatchResponse {
  /** Number of documents successfully ingested in this batch. */
  uploaded: number;
  /** Per-file error details if the backend returns them. */
  errors?: Array<{ filename: string; message: string }>;
  /** Any top-level message from the backend. */
  message?: string;
}
