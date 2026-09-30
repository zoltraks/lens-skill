# Vanilla Web Baseline

## Purpose

> **Scope:** Checkable constraints for browser subjects built on HTML, CSS, and JavaScript
> without a framework
> **Key items:** WHATWG structure/semantics, DOM contracts, Web Storage trust boundary, Web
> Audio/MIDI lifecycle, MDN security categories

This file distills the WHATWG HTML/DOM, ECMA-262, and MDN sources listed in
`references/source-catalog.md` into constraints an audit can verify from repository source.

Snapshot date: 2026-09-30.

Feeds `assessment/best-practices.md`, `assessment/security-review.md`,
`assessment/nfr-review.md`, and `references/topics/accessibility.md` consumers for vanilla-web
subjects.

## HTML Structure

From https://html.spec.whatwg.org/multipage/.

- Documents need `<!DOCTYPE html>`, `<html lang>`, `<head><meta charset>` and a non-empty
  `<title>`. A missing `lang` is an accessibility and correctness finding.
- Landmark elements (`<header>`, `<nav>`, `<main>`, `<footer>`) carry implicit ARIA roles.
  `<main>` appears at most once per document.
- Interactive content must not nest inside interactive content (`<a>` inside `<button>`).
  `button`/`a` misuse (anchors as buttons, divs as buttons) is a checkable class.
- `type="button"` on non-submit buttons inside forms prevents accidental submission.
  form fields need associated `<label>` (the accessibility file covers the full criteria).
- Elements like `<img>` require `alt`. `<video>`/`<audio>` caption and controls attributes are
  the conformance floor.

## DOM Contracts

From https://dom.spec.whatwg.org/ and https://developer.mozilla.org/en-US/docs/Web/JavaScript.

- `addEventListener` is the canonical event registration. `onclick`-style attributes and
  inline `on*` handler attributes mix markup with behavior and defeat CSP.
- `textContent` (not `innerHTML`) is the safe sink for untrusted strings. `innerHTML`,
  `outerHTML`, `insertAdjacentHTML`, and `document.write` are the injection sinks that
  `references/topics/web-frontend-security.md` enumerates.
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
- Client-side validation is UX, never the boundary. The audit treats it as defense-in-depth
  only.

## Live Check

When web fetch is available, spot-check one element requirement against the WHATWG standard
and one storage/security claim against MDN.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
