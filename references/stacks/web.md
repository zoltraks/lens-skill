# Vanilla Web Baseline

## Purpose

> **Scope:** Checkable constraints for browser subjects built on HTML, CSS, and JavaScript
> without a framework
> **Key items:** WHATWG structure/semantics, DOM contracts, Web Storage trust boundary, Web
> Audio/MIDI lifecycle, MDN security categories

This file distills the WHATWG HTML/DOM, ECMA-262, and MDN sources listed in
`references/source-catalog.md` into constraints an audit can verify from repository source.

Snapshot date: 2026-10-27.

Feeds `assessment/best-practices.md`, `assessment/security-review.md`,
`assessment/nfr-review.md`, `assessment/baseline-conformance.md`, and
`references/topics/accessibility-baseline.md` consumers for vanilla-web subjects.

## HTML Structure

From https://html.spec.whatwg.org/multipage/.

- Documents need `<!DOCTYPE html>`, `<html lang>`, `<head><meta charset>` and a non-empty
  `<title>`. A missing `lang` is an accessibility and correctness finding.
- Landmark elements (`<header>`, `<nav>`, `<main>`, `<footer>`) carry implicit ARIA roles.
  `<main>` appears at most once per document.
- Interactive content must not nest inside interactive content (`<a>` inside `<button>`).
  `button`/`a` misuse (anchors as buttons, divs as buttons) is a checkable class.
- `type="button"` on non-submit buttons inside forms prevents accidental submission.
  Form fields need associated `<label>` (the accessibility file covers the full criteria).
- Elements like `<img>` require `alt`. `<video>`/`<audio>` caption and controls attributes are
  the conformance floor.

## DOM Contracts

From https://dom.spec.whatwg.org/ and https://developer.mozilla.org/en-US/docs/Web/JavaScript.

- `addEventListener` is the canonical event registration. `onclick`-style attributes and
  inline `on*` handler attributes mix markup with behavior and defeat CSP.
- `textContent` (not `innerHTML`) is the safe sink for untrusted strings. `innerHTML`,
  `outerHTML`, `insertAdjacentHTML`, and `document.write` are the injection sinks that
  `references/topics/frontend-security.md` enumerates.
- `querySelector` returns the first match. `id` duplication makes selection and label
  association ambiguous - duplicate ids are a defect.
- ECMA-262 semantics: `===` comparison, `const`/`let` over `var`, no implicit globals
  (`'use strict'` or modules), and `async`/`await` error paths through `try/catch` or
  `.catch()` - unhandled rejections are an error-handling observation.

## Storage And Media

From https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API,
https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API, and
https://developer.mozilla.org/en-US/docs/Web/API/Web_MIDI_API.

- `localStorage`/`sessionStorage` are synchronous, stringly-typed, and readable by any script
  on the origin: tokens or PII there are an exposure finding, and writes need quota/error
  handling (Safari private mode historically throws).
- Storage values are untrusted input on read. Code that `innerHTML`s stored values chains
  persistence to injection.
- `AudioContext` starts `suspended` until a user gesture. Resume must happen inside the
  gesture handler - autoplay-policy violations are console-visible and user-breaking.
- Audio nodes must be disconnected and contexts closed on teardown. Unclosed contexts cap
  the browser's per-document limit.
- Web MIDI `sysex: true` triggers a permission gate and is only justified for actual SysEx
  use. Requesting it casually is a permission-scope finding.

## Security Categories

From https://developer.mozilla.org/en-US/docs/Web/Security.

- Same-origin policy, mixed-content blocking, and CORS are the model: a page loading
  `http://` subresources or widening CORS with `*` on credentialed endpoints is a finding.
- Subresource Integrity (`integrity`/`crossorigin` on CDN `<script>`/`<link>`) is the
  checkable control for third-party static includes.
- `target="_blank"` links need `rel="noopener"`. Missing it exposes `window.opener`.
- Client-side validation is UX, never the boundary. The audit treats it as defense-in-depth.
  only.

## CSS Discipline

From https://developer.mozilla.org/en-US/docs/Web/CSS and
https://www.w3.org/TR/WCAG22/.

- Cascade layers (`@layer`) and design tokens (custom properties) are the modern ordering
  mechanisms - a stylesheet that relies on source order alone is fragile under refactors.
- `!important` outside a declared utility layer is a specificity smell - each use is a
  reviewable exception, and a pattern of it defeats cascade reasoning.
- `:focus-visible` styles are mandatory on interactive elements - removing the outline
  without a replacement is an accessibility defect.
- `prefers-reduced-motion` guards animation, and touch targets meet the WCAG 2.2 AA minimum
  (24 CSS px, or the documented exception).
- Float layouts, fixed pixel heights on text containers, and `position: absolute` page
  scaffolds are the checkable fragility classes.

## Application Surface

- State lives in JavaScript, not in the DOM: reading `.value`/`.checked`/`.innerText` as the
  source of truth for logic couples correctness to rendering and loses data on re-render.
- Native dialogs (`alert`/`confirm`/`prompt`) block the event loop and cannot be styled -
  shipped code uses the project's own modal component.
- One `requestAnimationFrame` loop owns animation - multiple independent `setInterval` timers
  driving visual work drift and double-fire.
- Every event listener and subscription added inside a component needs a matching teardown -
  unpaired listeners on long-lived documents leak and double-deliver.
- User-supplied strings reach the DOM through `textContent` or an explicit sanitizer -
  `innerHTML` concatenation is the injection finding class this file already names.

## Naming And Layout

From the maintainer's HTML, CSS, accessibility, and performance-budget engineering standards.

- A vanilla web project's baseline is `index.html` at the root (or `src/index.html` when the
  deployable artifact is the `src/` directory) with `css/` and `js/` siblings - four layout
  tiers scale by size: single-file document, `index.html` plus one stylesheet and one script
  (`style.css` + `app.js`/`main.js`), split `css/`/`js/` modules, and `src/` separated from
  `runtime/` tooling. The smallest fitting tier is correct, and a layout migration is a
  project decision, never an audit recommendation.
- `kebab-case.css`/`kebab-case.js` filenames name the file's single responsibility
  (`item-list-renderer.js`, `catalog-data.js` for generated data), and `.a11y.test.tsx`,
  `*.perf.test.ts`, and `*.spec.ts` suffixes mark accessibility, performance, and end-to-end
  test files.
- CSS conventions: component classes `kebab-case`, BEM `__`/`--` separators when adopted,
  `is-*`/`has-*` state classes, `u-*` utility prefixes, and `--kebab-case` custom properties
  - one declared convention per project.
- Identifier semantics for inline and vanilla scripts: booleans read as claims (`isVisible`,
  `hasAnswer`), functions are verb phrases (`renderQuestion`), collections take plural nouns,
  and event handlers carry `on*` names - role-based naming over type-encoding (`strTitle`,
  `arrItems` are findings).
- Scratch probes stay in the gitignored workspace (`work/scripts/*.tmp.mjs`) - a committed
  `*.tmp.*` file is a hygiene finding, consistent with `references/stacks/shell.md`.

## Maintainer-Standard Floor

From the maintainer's HTML, CSS, and vanilla-application engineering standards.

- HTML floor: no value reaches `innerHTML` without the escape helper, platform features beat
  hand-rolled code, responsive across viewport dimensions and orientation, keyboard and
  screen-reader parity for every pointer action, and lowest workable complexity. Vanilla apps
  additionally ban native dialogs (`alert`/`confirm`/`prompt` are custom modals) and keep
  state in JavaScript with the DOM as projection.
- CSS floor: no unscoped element selectors on components, no `!important` outside utility
  classes, no raw colour literals where a token exists, no `float` for layout, visible
  `:focus-visible` on interactive elements, `prefers-reduced-motion` respected, and Stylelint
  passes. A component-library theme adds theme tokens over literals and both color schemes
  verified.

## Live Check

When web fetch is available, spot-check one element requirement against the WHATWG standard
and one storage/security claim against MDN.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
