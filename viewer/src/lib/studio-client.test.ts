import { afterEach, describe, expect, it, vi } from 'vitest';

import {
  STUDIO_API_BASE,
  api,
  detailMessage,
  studio,
  validationErrors,
} from './studio-client';

function mockFetch(status: number, jsonBody: unknown, opts: { noJson?: boolean } = {}) {
  const fn = vi.fn().mockResolvedValue({
    ok: status >= 200 && status < 300,
    status,
    json: opts.noJson
      ? () => Promise.reject(new Error('not json'))
      : () => Promise.resolve(jsonBody),
  });
  globalThis.fetch = fn as unknown as typeof fetch;
  return fn;
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe('api()', () => {
  it('returns ok/status/body on success', async () => {
    mockFetch(200, { hello: 'world' });
    const res = await api<{ hello: string }>('/x');
    expect(res.ok).toBe(true);
    expect(res.status).toBe(200);
    expect(res.body).toEqual({ hello: 'world' });
  });

  it('returns ok=false and body on error status', async () => {
    mockFetch(409, { detail: 'exists' });
    const res = await api('/x');
    expect(res.ok).toBe(false);
    expect(res.status).toBe(409);
    expect(res.body).toEqual({ detail: 'exists' });
  });

  it('tolerates a non-JSON body', async () => {
    mockFetch(204, null, { noJson: true });
    const res = await api('/x');
    expect(res.body).toBeNull();
  });

  it('prefixes the studio API base', async () => {
    const fn = mockFetch(200, {});
    await api('/health');
    expect(fn).toHaveBeenCalledWith(`${STUDIO_API_BASE}/health`, expect.any(Object));
  });
});

describe('studio endpoints', () => {
  it('createBlock POSTs the payload to /blocks', async () => {
    const fn = mockFetch(201, {});
    await studio.createBlock({ name: 'cost-control', label: 'Cost Control' });
    const [url, opts] = fn.mock.calls[0];
    expect(url).toBe(`${STUDIO_API_BASE}/blocks`);
    expect(opts.method).toBe('POST');
    expect(JSON.parse(opts.body)).toEqual({ name: 'cost-control', label: 'Cost Control' });
  });

  it('addEntity POSTs {content} to the entities path (name encoded)', async () => {
    const fn = mockFetch(201, {});
    await studio.addEntity('cost control', '---\ntype: x\n---');
    const [url, opts] = fn.mock.calls[0];
    expect(url).toBe(`${STUDIO_API_BASE}/blocks/cost%20control/entities`);
    expect(opts.method).toBe('POST');
    expect(JSON.parse(opts.body)).toEqual({ content: '---\ntype: x\n---' });
  });

  it('listEntities GETs the entities path', async () => {
    const fn = mockFetch(200, []);
    await studio.listEntities('incidents');
    expect(fn.mock.calls[0][0]).toBe(`${STUDIO_API_BASE}/blocks/incidents/entities`);
  });
});

describe('detailMessage()', () => {
  it('reads a string detail', () => {
    expect(detailMessage({ detail: 'Block exists' })).toBe('Block exists');
  });

  it('joins an errors array', () => {
    expect(detailMessage({ detail: { errors: ['type: bad', 'id: bad'] } })).toBe('type: bad; id: bad');
  });

  it('falls back for an unknown shape', () => {
    expect(detailMessage(null)).toBe('Request failed');
    expect(detailMessage({})).toBe('Request failed');
  });
});

describe('validationErrors()', () => {
  it('extracts the errors array', () => {
    expect(validationErrors({ detail: { errors: ['a', 'b'] } })).toEqual(['a', 'b']);
  });

  it('returns [] when absent', () => {
    expect(validationErrors({ detail: 'string' })).toEqual([]);
    expect(validationErrors(null)).toEqual([]);
  });
});
