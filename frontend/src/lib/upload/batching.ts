import { BATCH_SIZE } from '@/types/documents';
import type { UploadFile } from '@/types/documents';

/**
 * Splits an array of UploadFile items into sequential batches of at most
 * BATCH_SIZE (10) files each.
 *
 * Examples:
 *   7  files → [[f0…f6]]
 *   10 files → [[f0…f9]]
 *   23 files → [[f0…f9], [f10…f19], [f20…f22]]
 */
export function createBatches(files: UploadFile[]): UploadFile[][] {
  const batches: UploadFile[][] = [];
  for (let i = 0; i < files.length; i += BATCH_SIZE) {
    batches.push(files.slice(i, i + BATCH_SIZE));
  }
  return batches;
}

/** Returns the total number of batches required for the given file count. */
export function batchCount(fileCount: number): number {
  return Math.ceil(fileCount / BATCH_SIZE);
}

/**
 * Calculates overall upload progress (0–100) based on how many files have
 * been fully processed (success or error) out of the total.
 */
export function overallProgress(
  processed: number,
  total: number,
  currentBatchTransferProgress: number,
  currentBatchSize: number
): number {
  if (total === 0) return 0;
  // Weight of each file in overall progress
  const fileWeight = 100 / total;
  // Contribution of already-completed files
  const completedContrib = processed * fileWeight;
  // Fractional contribution of the currently-transferring batch
  const batchContrib = (currentBatchTransferProgress / 100) * currentBatchSize * fileWeight;
  return Math.min(100, Math.round(completedContrib + batchContrib));
}
