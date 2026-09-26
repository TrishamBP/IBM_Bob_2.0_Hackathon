'use client';

interface UploadProgressProps {
  overallProgress: number;
  currentBatch: number;
  totalBatches: number;
  successCount: number;
  failedCount: number;
  totalFiles: number;
  statusMessage: string;
}

export function UploadProgress({
  overallProgress,
  currentBatch,
  totalBatches,
  successCount,
  failedCount,
  totalFiles,
  statusMessage,
}: UploadProgressProps) {
  const processed = successCount + failedCount;

  return (
    <div
      className="rounded-xl border border-[#28415D] bg-[#0F2138] p-5"
      role="region"
      aria-label="Upload progress"
      aria-live="polite"
      aria-atomic="false"
    >
      {/* Row: label + percentage */}
      <div className="mb-2 flex items-center justify-between">
        <span className="text-sm font-semibold text-[#F8FAFC]">Upload progress</span>
        <span
          className="text-sm font-bold text-[#38BDF8]"
          aria-label={`${overallProgress} percent`}
        >
          {overallProgress}%
        </span>
      </div>

      {/* Progress bar */}
      <div
        className="h-2 w-full overflow-hidden rounded-full bg-[#28415D]"
        role="progressbar"
        aria-valuenow={overallProgress}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label="Overall upload progress"
      >
        <div
          className="h-2 rounded-full bg-[#38BDF8] transition-all duration-300"
          style={{ width: `${overallProgress}%` }}
        />
      </div>

      {/* Status message */}
      <p className="mt-2.5 text-xs text-[#94A3B8]">{statusMessage}</p>

      {/* Stats row */}
      <div className="mt-3 flex flex-wrap gap-x-5 gap-y-1.5 text-xs">
        <span className="text-[#94A3B8]">
          Batch{' '}
          <span className="font-semibold text-[#F8FAFC]">{currentBatch}</span>
          {' '}of{' '}
          <span className="font-semibold text-[#F8FAFC]">{totalBatches}</span>
        </span>
        <span className="text-[#94A3B8]">
          <span className="font-semibold text-green-400">{successCount}</span>
          {' '}of{' '}
          <span className="font-semibold text-[#F8FAFC]">{totalFiles}</span>
          {' '}files uploaded
        </span>
        {failedCount > 0 && (
          <span className="font-semibold text-red-400">
            {failedCount} failed
          </span>
        )}
        {processed < totalFiles && (
          <span className="text-[#94A3B8]">
            <span className="font-semibold text-[#F8FAFC]">{totalFiles - processed}</span>
            {' '}remaining
          </span>
        )}
      </div>
    </div>
  );
}
