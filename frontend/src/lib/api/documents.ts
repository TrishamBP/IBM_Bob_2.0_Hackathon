/**
 * API client for the document upload endpoint.
 *
 * Backend endpoint (provisional):  POST /api/v1/rag/upload
 * Transport:                        multipart/form-data
 * Fields:
 *   department  string   — selected department label
 *   files       File[]   — up to BATCH_SIZE files per request
 *
 * Uses XMLHttpRequest so the browser fires real upload progress events.
 * The Content-Type boundary is set automatically by the browser — never set
 * it manually on multipart requests.
 */

import { API_BASE } from './config';
import type { Department, UploadBatchResponse } from '@/types/documents';

export const UPLOAD_ENDPOINT = `${API_BASE}/api/v1/rag/upload`;

export interface BatchUploadOptions {
  department: Department;
  files: File[];
  /** Called repeatedly with 0–100 as bytes are transferred over the wire. */
  onTransferProgress: (percent: number) => void;
  /** AbortSignal — abort() cancels the in-flight XHR. */
  signal?: AbortSignal;
}

/**
 * Uploads a single batch of files to the backend.
 *
 * Resolves with the parsed UploadBatchResponse on HTTP 2xx.
 * Rejects with an Error on network failure, abort, or non-2xx status.
 *
 * NOTE: Transfer progress reaching 100 % only means bytes left the browser.
 *       A successful upload is only confirmed when the server responds 2xx.
 */
export function uploadBatch({
  department,
  files,
  onTransferProgress,
  signal,
}: BatchUploadOptions): Promise<UploadBatchResponse> {
  return new Promise((resolve, reject) => {
    const form = new FormData();
    form.append('department', department);
    for (const file of files) {
      form.append('files', file, file.name);
    }

    const xhr = new XMLHttpRequest();

    // Wire up abort signal
    const onAbort = () => xhr.abort();
    if (signal) {
      if (signal.aborted) {
        reject(new DOMException('Upload aborted', 'AbortError'));
        return;
      }
      signal.addEventListener('abort', onAbort, { once: true });
    }

    xhr.upload.addEventListener('progress', (evt) => {
      if (evt.lengthComputable) {
        const pct = Math.round((evt.loaded / evt.total) * 100);
        onTransferProgress(pct);
      }
    });

    xhr.addEventListener('load', () => {
      if (signal) signal.removeEventListener('abort', onAbort);

      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          const data = JSON.parse(xhr.responseText) as UploadBatchResponse;
          resolve(data);
        } catch {
          // Backend returned 2xx but non-JSON — treat as full success
          resolve({ uploaded: files.length });
        }
      } else {
        let message = `Server returned ${xhr.status}`;
        try {
          const body = JSON.parse(xhr.responseText) as { detail?: string; message?: string };
          message = body.detail ?? body.message ?? message;
        } catch {
          // ignore parse failure
        }
        reject(new Error(message));
      }
    });

    xhr.addEventListener('error', () => {
      if (signal) signal.removeEventListener('abort', onAbort);
      reject(new Error('Network error — could not reach the server.'));
    });

    xhr.addEventListener('abort', () => {
      if (signal) signal.removeEventListener('abort', onAbort);
      reject(new DOMException('Upload aborted', 'AbortError'));
    });

    xhr.addEventListener('timeout', () => {
      if (signal) signal.removeEventListener('abort', onAbort);
      reject(new Error('Upload timed out.'));
    });

    xhr.open('POST', UPLOAD_ENDPOINT);
    // Do NOT set Content-Type — the browser sets the multipart boundary.
    xhr.send(form);
  });
}
