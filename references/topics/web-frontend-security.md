# Web Frontend Security Baseline

## Purpose

> **Scope:** Checkable client-side injection and browser-policy constraints
> **Key items:** DOM sink inventory, CSP directives and delivery, Trusted Types,
> Permissions-Policy, eslint rule cross-refs

This file distills the OWASP DOM-XSS, XSS-prevention, CSP, and web-frontend cheat sheets plus
the MDN header references listed in `references/source-catalog.md` into constraints an audit
can verify from repository source.

Snapshot date: 2026-09-30.

Feeds `assessment/security-review.md` for browser-facing subjects and complements
`references/stacks/web.md`.

## DOM Sinks And Sources

From https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html
and https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html.

- Execution sinks: `eval`, `new Function`, `setTimeout`/`setInterval` with string args,
  `document.write`, `location.href = javascript:`, `script.src` from data.
- Markup sinks: `innerHTML`, `outerHTML`, `insertAdjacentHTML`. The safe alternatives are
  `textContent`, `createElement` + `textContent`, or a sanitizer (`DOMPurify`).
- Attribute/URL sinks: `setAttribute` on `href`/`src`/`formaction` with untrusted data,
  `location.*` assignment, `window.open` with untrusted URLs - `javascript:`/`data:` schemes
  in these positions are findings.
- Untrusted sources include `location.search`/`hash`, `postMessage` payloads (require
  `event.origin` checks - `addEventListener('message')` without origin verification is a
  defect), `document.referrer`, cookies, and storage values.
- Contextual encoding: HTML-entity encode in markup, JS-encode in script context, URL-encode
  in parameters. A single sanitizer applied across contexts is misuse.
- Trusted Types (`trustedTypes`/`require-trusted-types-for 'script'`) is the DOM-XSS
  structural defense when deployed. Its absence is an observation, not a defect.

## Content Security Policy

From https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html
and https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP.

- Delivery order: `Content-Security-Policy-Report-Only` first, then enforced. An enforced
  policy without a report phase is a rollout observation.
- `default-src 'none'` with explicit directives is the strict posture. `default-src *`,
  `unsafe-inline` on `script-src`, and `data:` in `script-src`/`img-src` where unneeded are
  findings.
- `script-src 'nonce-...'`/`'strict-dynamic'` is the modern allowlist. `'unsafe-inline'` in
  `script-src` defeats the policy.
- `frame-ancestors` replaces `X-Frame-Options` (keep both for coverage), `base-uri 'none'`
  blocks base-tag hijacking, `object-src 'none'` kills plugin embedding.
- Meta-element CSPs (`<meta http-equiv>`) can't set `frame-ancestors` or report-uri. Header
  delivery is the checkable form.

## Permissions-Policy And Headers

From https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Permissions-Policy.

- `Permissions-Policy` gates browser features per origin list: `camera=()`, `microphone=()`,
  `geolocation=()`, `midi=()`, `usb=()` are deny-all forms. A feature not in the app's spec
  but left open is an observation.
- Related baseline headers (full list in
  `references/methodology/owasp-baselines.md` Secure Headers): `X-Content-Type-Options:
  nosniff`, `Referrer-Policy`, `Cross-Origin-Opener-Policy`, `Cross-Origin-Resource-Policy`.
- `iframe sandbox=` attributes sandbox embedded contexts. `allow-scripts` without
  `allow-same-origin` avoids origin escape.

## Lint Cross-Reference

From https://github.com/mozilla/eslint-plugin-no-unsanitized.

- `eslint-plugin-no-unsanitized` rules (`no-unsanitized/property`, `no-unsanitized/method`)
  flag `innerHTML`/`outerHTML`/`insertAdjacentHTML`/`document.write` assignments - the CWE-79
  surface cross-referenced in `references/cwe-analyzer.md`.

## Live Check

When web fetch is available, spot-check one sink against the DOM-XSS cheat sheet and one
directive against the CSP cheat sheet.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
