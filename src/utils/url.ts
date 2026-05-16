/**
 * Build a URL path that respects the Astro `base` config.
 *
 * GitHub Pages project sites live under a base path (e.g. /helios-site/).
 * Astro doesn't auto-prefix <a href> values with that base, so every
 * internal link in the site goes through this helper.
 *
 *   import { path } from '../utils/url';
 *   <a href={path('/consumer')}> ... </a>
 *
 * In dev: import.meta.env.BASE_URL is '/', so path('/consumer') => '/consumer'
 * In prod: BASE_URL is '/helios-site/', so path('/consumer') => '/helios-site/consumer'
 */
export function path(p: string): string {
  const base = import.meta.env.BASE_URL;
  const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base;
  const cleanPath = p.startsWith('/') ? p : `/${p}`;
  return `${cleanBase}${cleanPath}` || '/';
}
