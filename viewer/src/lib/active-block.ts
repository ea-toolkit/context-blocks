import { useEffect, useState } from 'react';

/** The active block name from a `?block=<name>` query param, or null. Pure — testable. */
export function getActiveBlockFromSearch(search: string): string | null {
  return new URLSearchParams(search).get('block');
}

/** React hook: the active block from the URL (client-side). null on the server /
 * first render, so views default to baked data until hydrated. */
export function useActiveBlock(): string | null {
  const [block, setBlock] = useState<string | null>(null);
  useEffect(() => {
    setBlock(getActiveBlockFromSearch(window.location.search));
  }, []);
  return block;
}

/** URL for the current page with a given active block (empty → clears it). */
export function blockHref(pathname: string, block: string): string {
  return block ? `${pathname}?block=${encodeURIComponent(block)}` : pathname;
}
