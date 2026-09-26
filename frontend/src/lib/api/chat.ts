/**
 * API client for the chat streaming endpoint.
 *
 * Backend endpoint:  POST /api/v1/chat/stream
 * Transport:         JSON request, Server-Sent Events response
 * Events:
 *   session    { conversation_id, title, ... }   — first frame; the server conversation id
 *   status     { stage, message, ... }           — pipeline progress (ignored here)
 *   token      { text }                          — answer fragment
 *   sources    { sources: SourceRef[] }
 *   completed  { conversation_id, content, sources }
 *   error      { code, message }
 */

import type { SourceCitationData } from '@/types/chat';

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, '') ?? 'http://localhost:8000';

export const CHAT_STREAM_ENDPOINT = `${API_BASE}/api/v1/chat/stream`;

interface SourceRef {
  id: string;
  chunk_id?: string;
  document_id?: string;
  title: string;
  department: string;
  section?: string | null;
  reference: string;
  version?: string | null;
  url?: string | null;
}

export interface StreamChatOptions {
  email: string;
  /** Server-side conversation id; omit to let the backend create one. */
  conversationId?: string;
  message: string;
  /** Called with the full answer text accumulated so far. */
  onToken: (content: string) => void;
  /** Called once the backend reports the conversation id for this turn. */
  onSession?: (conversationId: string) => void;
  signal?: AbortSignal;
}

export interface StreamChatResult {
  conversationId: string;
  content: string;
  sources: SourceCitationData[];
}

function toCitation(src: SourceRef): SourceCitationData {
  return {
    id: src.id,
    title: src.title,
    department: src.department,
    reference: src.reference,
    url: src.url ?? undefined,
    documentId: src.document_id,
    chunkId: src.chunk_id,
    section: src.section ?? undefined,
    version: src.version ?? undefined,
  };
}

async function errorDetail(res: Response): Promise<string> {
  try {
    const body = await res.json();
    if (typeof body?.detail === 'string') return body.detail;
  } catch {
    // fall through
  }
  return `Request failed (HTTP ${res.status})`;
}

/**
 * Sends one message and consumes the SSE stream until `completed` or `error`.
 * Rejects with an Error carrying a user-safe message on failure.
 */
export async function streamChat({
  email,
  conversationId,
  message,
  onToken,
  onSession,
  signal,
}: StreamChatOptions): Promise<StreamChatResult> {
  let res: Response;
  try {
    res = await fetch(CHAT_STREAM_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'text/event-stream' },
      body: JSON.stringify({
        conversation_id: conversationId ?? null,
        employee_email: email,
        message,
      }),
      signal,
    });
  } catch (err) {
    if (err instanceof DOMException && err.name === 'AbortError') throw err;
    throw new Error(`Could not reach the assistant service at ${API_BASE}.`);
  }

  if (!res.ok) throw new Error(await errorDetail(res));
  if (!res.body) throw new Error('The assistant returned an empty response.');

  const reader = res.body.pipeThrough(new TextDecoderStream()).getReader();
  let buffer = '';
  let serverId = conversationId ?? '';
  let content = '';
  let sources: SourceCitationData[] = [];

  const handle = (event: string, data: string): StreamChatResult | null => {
    const payload = JSON.parse(data);
    switch (event) {
      case 'session':
        serverId = payload.conversation_id;
        onSession?.(serverId);
        return null;
      case 'token':
        content += payload.text;
        onToken(content);
        return null;
      case 'sources':
        sources = (payload.sources as SourceRef[]).map(toCitation);
        return null;
      case 'completed':
        return {
          conversationId: payload.conversation_id ?? serverId,
          // The final content has invalid citation markers stripped.
          content: payload.content ?? content,
          sources: payload.sources ? (payload.sources as SourceRef[]).map(toCitation) : sources,
        };
      case 'error':
        throw new Error(payload.message ?? 'The assistant could not generate a response.');
      default:
        return null;
    }
  };

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += value.replace(/\r\n/g, '\n');

    let sep: number;
    while ((sep = buffer.indexOf('\n\n')) !== -1) {
      const frame = buffer.slice(0, sep);
      buffer = buffer.slice(sep + 2);

      let event = 'message';
      const dataLines: string[] = [];
      for (const line of frame.split('\n')) {
        if (line.startsWith('event:')) event = line.slice(6).trim();
        else if (line.startsWith('data:')) dataLines.push(line.slice(5).trimStart());
      }
      if (dataLines.length === 0) continue;

      const result = handle(event, dataLines.join('\n'));
      if (result) {
        reader.cancel().catch(() => {});
        return result;
      }
    }
  }

  throw new Error('The connection to the assistant closed before the answer finished.');
}
