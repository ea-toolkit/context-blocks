/**
 * Base-path helper for multi-block builds.
 *
 * Each block is built into its own subfolder (dist/<block>/) with Astro's
 * `base` set to `/<block>/`. Absolute in-app links written as `/explorer`
 * are NOT auto-prefixed by Astro, so wrap them with withBase() so they
 * resolve correctly under the block's base path. In a normal single-block
 * build (base `/`) this is a no-op.
 */
const BASE = (import.meta.env.BASE_URL || '/').replace(/\/$/, '');

export function withBase(path: string): string {
  const p = path.startsWith('/') ? path : `/${path}`;
  return `${BASE}${p}`;
}
