/**
 * Thin typed client for the Studio API (block authoring). Mirrors the fetch
 * idiom of AskView (PUBLIC_-prefixed base URL) and the api()/detailMessage
 * helpers ported from the standalone studio/app.js.
 *
 * All writes go client-side to the Studio API — the viewer is static (SSG), so
 * there is no server route to mutate through (same model as the Ask page).
 */

import type {
  AddEntityResponse,
  BlockDetail,
  BlockSummary,
  CreateBlockPayload,
  EntityListItem,
  StudioHealth,
} from './studio-types';

export const STUDIO_API_BASE =
  import.meta.env.PUBLIC_CB_STUDIO_API_BASE || 'http://localhost:8322';

export interface ApiResult<T> {
  ok: boolean;
  status: number;
  body: T | null;
}

/** Low-level fetch wrapper: returns {ok, status, body} and never throws on HTTP errors. */
export async function api<T>(path: string, options?: RequestInit): Promise<ApiResult<T>> {
  const res = await fetch(`${STUDIO_API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  let body: T | null = null;
  try {
    body = (await res.json()) as T;
  } catch {
    body = null;
  }
  return { ok: res.ok, status: res.status, body };
}

/** Best-effort human message from a FastAPI error body ({detail: string | {errors: [...]}}). */
export function detailMessage(body: unknown): string {
  if (!body || typeof body !== 'object') return 'Request failed';
  const detail = (body as { detail?: unknown }).detail;
  if (detail == null) return 'Request failed';
  if (typeof detail === 'string') return detail;
  if (typeof detail === 'object' && detail !== null && 'errors' in detail) {
    const errs = (detail as { errors?: unknown }).errors;
    if (Array.isArray(errs)) return errs.join('; ');
  }
  return JSON.stringify(detail);
}

/** Per-field validation errors from a 422 add-entity response ({detail: {errors: [...]}}). */
export function validationErrors(body: unknown): string[] {
  if (body && typeof body === 'object') {
    const detail = (body as { detail?: { errors?: unknown } }).detail;
    if (detail && Array.isArray(detail.errors)) {
      return detail.errors.filter((e): e is string => typeof e === 'string');
    }
  }
  return [];
}

/** Typed endpoint methods. */
export const studio = {
  health: () => api<StudioHealth>('/health'),
  listBlocks: () => api<BlockSummary[]>('/blocks'),
  getBlock: (name: string) => api<BlockDetail>(`/blocks/${encodeURIComponent(name)}`),
  listEntities: (name: string) =>
    api<EntityListItem[]>(`/blocks/${encodeURIComponent(name)}/entities`),
  createBlock: (payload: CreateBlockPayload) =>
    api<BlockDetail>('/blocks', { method: 'POST', body: JSON.stringify(payload) }),
  addEntity: (name: string, content: string) =>
    api<AddEntityResponse>(`/blocks/${encodeURIComponent(name)}/entities`, {
      method: 'POST',
      body: JSON.stringify({ content }),
    }),
};
