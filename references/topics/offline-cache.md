# Offline Cache And Service Worker Baseline

## Purpose

> **Scope:** Checkable constraints for service-worker caching and offline behavior
> **Key items:** lifecycle semantics, cache-version cleanup, strategy recipes, HTTP-cache
> interaction, stale-cache finding class

This file distills the web.dev service-worker articles and MDN Using Service Workers source
listed in `references/source-catalog.md` into constraints an audit can verify from repository
source.

Snapshot date: 2026-09-30.

Feeds `references/stacks/spa.md` PWA checks and `assessment/nfr-review.md` offline claims.

## Lifecycle Semantics

From https://web.dev/articles/service-worker-lifecycle and
https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers.

- Registration (`navigator.serviceWorker.register`) happens on load, needs HTTPS or
  localhost, and is feature-detected (`'serviceWorker' in navigator`). Unguarded
  registration on unsupported contexts throws.
- `install` -> `activate` -> idle/fetch: a new worker waits for old tabs unless
  `self.skipWaiting()` runs in `install` and `clients.claim()` in `activate`. An update that
  never activates leaves the old worker serving forever - the stale-cache finding class.
- `activate` should delete old cache versions (`caches.keys()` + `delete` of non-current
  names). Caches not versioned or never purged leak storage and serve stale code.
- `self.addEventListener('fetch', ...)` intercepts everything in scope. Responses must come
  from `respondWith` or fall through - a handler that swallows errors without a fallback
  offline response breaks the app.

## Caching Strategies

From https://web.dev/articles/offline-cookbook and
https://web.dev/articles/service-worker-caching-and-http-caching.

- Cache-first suits immutable assets (hashed filenames). Network-first suits fresh-content
  API/HTML. Stale-while-revalidate serves cache then updates.
- Mixing strategies without a route split (`url.pathname`/`request.destination` matching) is
  a consistency defect: API responses cached under cache-first defeat freshness.
- Precaching (install-time `cache.addAll`) must list everything needed for the offline shell.
  a missing asset fails `addAll` atomically and leaves the worker uninstalled.
- Cache keys and opaque responses (`no-cors` third-party fetches) can't be inspected.
  caching `no-cors` responses silently stores opaque failures.

## HTTP Interaction

- A service worker overrides HTTP caching but does not replace it: `Cache-Control` still
  governs what the network fetch returned. `cache-control: no-store` responses must not be
  cached.
- `updateViaCache` on registration controls HTTP-cache use for the worker script itself.
  `importScripts`/`import` inside the worker is the module boundary.
- `Credentials: 'include'`/`'same-origin'` on `fetch` controls cookie forwarding. A cache
  serving responses that skipped credential checks is a data-leak finding.

## Checkable Surface

- Service-worker file present at the expected scope path (usually `/sw.js`), registration
  guarded, `activate` cleans old cache names, `fetch` handler has an offline fallback,
  strategy per route is declared (not ad-hoc).
- `manifest.json` presence and service-worker registration together make the PWA claim. One
  without the other is partial.

## Live Check

When web fetch is available, spot-check one lifecycle claim against web.dev and one strategy
name against the offline cookbook.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
