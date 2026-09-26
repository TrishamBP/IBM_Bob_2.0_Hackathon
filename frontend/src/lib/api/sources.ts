/**
 * API client for the citation source viewer.
 *
 * Backend endpoint:  GET /api/v1/rag/documents/{document_id}
 * Returns the current version of a stored document, rebuilt from its chunks.
 * 404 (string `detail`) when the document was removed.
 */

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, '') ?? 'http://localhost:8000';

export interface SourceDocumentChunk {
  chunk_id: string;
  index: number;
  section: string | null;
  page_start: number | null;
  page_end: number | null;
  /** Original chunk text; headings restored as Markdown. */
  markdown: string;
}

export interface SourceDocument {
  document_id: string;
  title: string;
  department: string;
  version: string | null;
  effective_date: string | null;
  source_filename: string | null;
  file_type: string | null;
  page_count: number | null;
  ingested_at: string | null;
  chunks: SourceDocumentChunk[];
}

// Documents rarely change within a session; reuse fetches across clicks.
const cache = new Map<string, Promise<SourceDocument>>();

async function load(documentId: string): Promise<SourceDocument> {
  let res: Response;
  try {
    res = await fetch(`${API_BASE}/api/v1/rag/documents/${encodeURIComponent(documentId)}`);
  } catch {
    throw new Error(`Could not reach the document service at ${API_BASE}.`);
  }
  if (!res.ok) {
    let detail = `Could not load the document (HTTP ${res.status}).`;
    try {
      const body = await res.json();
      if (typeof body?.detail === 'string') detail = body.detail;
    } catch {
      // keep the generic message
    }
    throw new Error(detail);
  }
  return (await res.json()) as SourceDocument;
}

export function fetchSourceDocument(documentId: string): Promise<SourceDocument> {
  let pending = cache.get(documentId);
  if (!pending) {
    pending = load(documentId);
    // Failed requests are not cached, so the viewer can retry
    pending.catch(() => cache.delete(documentId));
    cache.set(documentId, pending);
  }
  return pending;
}
