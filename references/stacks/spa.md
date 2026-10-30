# React And SPA Baseline

## Purpose

> **Scope:** Checkable constraints for React-class single-page applications and PWAs
> **Key items:** rules of hooks, effect-misuse checklist, key discipline, PWA/service-worker
> surface

This file distills the React documentation and MDN Service Worker source listed in
`references/source-catalog.md` into constraints an audit can verify from repository source.

Snapshot date: 2026-10-27.

Feeds `assessment/best-practices.md`, `assessment/code-quality.md`, and
`assessment/security-review.md`, and `assessment/baseline-conformance.md` for SPA subjects.

`references/topics/offline-cache.md` covers service-worker caching strategy.

## Rules Of Hooks

From https://react.dev/reference/rules/rules-of-hooks.

- Hooks run only at the top level of a component or custom hook - never inside conditions,
  loops, nested functions, or after an early `return`. Conditional hooks are a defect the
  `rules-of-hooks` ESLint rule catches mechanically.
- Hook names start with `use`. Non-`use` functions calling hooks are indistinguishable to the
  linter and are a convention finding.
- `useEffect` dependency arrays must be complete. A missing dep is a stale-closure defect,
  and `eslint-plugin-react-hooks` `exhaustive-deps` is the enforcing rule.
- `useState` never appears inside conditions either. State shape changes belong in reducers
  or multiple state variables.

## Effect Discipline

From https://react.dev/learn/you-might-not-need-an-effect.

- Effects exist for synchronizing with external systems (network subscriptions, DOM APIs,
  timers). Derived values should be computed during render or memoized with `useMemo`, not
  stored via `useEffect` + `setState` chains.
- Fetch-in-`useEffect` without an abort/`ignore` cleanup flag races and warns. The cleanup
  function is the checkable shape.
- An effect that "resets state on prop change" is usually a `key` prop or derived-state
  candidate instead.
- Event-handler logic in effects (`useEffect` that only calls a callback) belongs in the
  handler or `useEffectEvent`/`useEvent` where available.
- `URL.createObjectURL` results must be revoked with `URL.revokeObjectURL` when the URL is
  no longer needed - an un-revoked object URL pins the blob in memory for the session.

## Rendering And State

- `key` props must be stable and unique among siblings. Array-index keys on reorderable lists
  corrupt component state - a classic finding.
- Lifting state, context for deep trees, and external stores (see
  `references/stacks/typescript.md` for Zustand conventions) are the state-placement choices.
  Prop-drilling past two levels is a maintainability observation.
- `<StrictMode>` double-invocation in development exposes impure renders. Side effects inside
  render bodies are findings regardless.

## PWA And Service Workers

From https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API.

- A service worker intercepts every fetch in its scope. It requires HTTPS (or localhost) and
  a valid registration (`navigator.serviceWorker.register`) guarded by feature detection.
- Caching strategy and update lifecycle are covered by `references/topics/offline-cache.md`.
  The audit checks `install`/`activate`/`fetch` handler presence and cache-version cleanup.
- `manifest.json` with `name`, `icons`, `start_url`, `display` defines the installable
  surface. A PWA claim without a linked manifest is a gap.
- Serving user-supplied SVG with `Content-Disposition: inline` needs
  `Content-Security-Policy: sandbox` on the response - an inline SVG can execute script in
  the serving origin.

## Naming And Layout

From https://legacy.reactjs.org/docs/faq-structure.html,
https://vite.dev/guide/#index-html-and-project-root, and the maintainer's TypeScript/React
engineering standard.

- React is deliberately unopinionated about structure: grouping by feature/route and grouping
  by file type are both legitimate, and the audit checks consistency and depth, not the
  chosen model. Nesting beyond roughly three to four levels inside `src/` is the documented
  pain point.
- Role-directory conventions for a `src/` SPA: `components/` (React components),
  `hooks/` (`useCamelCase.ts` custom hooks), `stores/` (state stores, plural), `types/`,
  `constants/` or `constants.ts`, `services/` or `api/`, `utils/` or `logic/` for pure
  modules, `assets/`, `workers/`, `i18n/` - each directory holds one responsibility.
- File naming follows the exported unit: `PascalCase.tsx` for component files (`DataGrid.tsx`),
  `useCamelCase.ts` for hooks, `camelCase.ts` or `kebab-case.ts` for utilities per the
  project's dominant shape, and `*.test.tsx`/`*.test.ts` test files mirroring their subject.
- Vite's convention puts `index.html` at the project root (not under `public/`), source
  modules under `src/` imported through the entry script, and static assets served verbatim
  from `public/` - placing importable source in `public/` breaks the build model.
- Barrel files (`index.ts` re-export aggregates) are acceptable in `types/` or as a
  deliberate public surface. Blanket barrels in component directories hide dependencies and
  slow bundlers - flag the pattern, not the file.
- Pure logic modules carry no React imports. A `logic/` or `utils/` file importing
  `react`/`react-dom` breaks the independent-testability boundary the directory exists for.

## Maintainer-Standard Floor

From the maintainer's TypeScript/React engineering standards.

- Component and hook discipline extends the rules of hooks: effects declare dependencies
  honestly (an omitted dependency to silence the linter is a finding), state lives at the
  lowest shared owner, and derived values are computed rather than stored.
- One file-name casing per project, one barrel policy, and colocated tests - consistency binds
  harder than any single choice.

## Live Check

When web fetch is available, spot-check one hook rule against react.dev and one service-worker
lifecycle claim against MDN.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
