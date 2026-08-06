import { describe, expect, it } from 'vitest';

import { blockHref, getActiveBlockFromSearch } from './active-block';

describe('getActiveBlockFromSearch', () => {
  it('reads the ?block= param', () => {
    expect(getActiveBlockFromSearch('?block=incidents')).toBe('incidents');
    expect(getActiveBlockFromSearch('?x=1&block=cost-control')).toBe('cost-control');
  });
  it('is null when absent', () => {
    expect(getActiveBlockFromSearch('')).toBeNull();
    expect(getActiveBlockFromSearch('?other=1')).toBeNull();
  });
});

describe('blockHref', () => {
  it('appends the block param', () => {
    expect(blockHref('/map', 'incidents')).toBe('/map?block=incidents');
  });
  it('clears back to the bare path when empty', () => {
    expect(blockHref('/map', '')).toBe('/map');
  });
});
