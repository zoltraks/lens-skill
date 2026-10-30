# Frontend Review

## Purpose

> **Scope:** Rendered-UI subjects - client-side injection surface, storage residue,
> accessibility, dead features, and frontend-backend agreement
> **Key items:** DOM-sink census, client-storage census, accessibility census, dead-feature
> census, coupled-client contract reconciliation

This file guides assessment of subjects that ship a rendered user interface - a browser SPA,
a server-rendered UI, or a desktop shell.

It is conditional: it applies only when the subject's domain profile classifies a project as
`frontend`, per `references/domain-profiles.md`.

Apply `principles/evaluation-rules.md` throughout.

## What To Evaluate

- **Injection surface**: whether untrusted data reaches DOM sinks unsanitized, and whether
  export paths (CSV, clipboard, generated documents) carry formula or markup injection.
- **Storage residue**: what client storage retains after logout - tokens, identifiers, and
  browsing history of sensitive objects.
- **Accessibility**: whether interactive elements are reachable and labelled for keyboard
  and assistive technology, and whether the document language matches the UI language.
- **Dead features**: whether visible affordances lead to real behavior - buttons wired to
  "not available" notices, render branches for formats the backend refuses, and API
  helpers nothing calls.
- **Frontend-backend agreement**: whether the client's expectations match the server -
  status-code set, error-body fields consumed versus produced, and capability matrices
  (formats, features, roles) on each side.

## Evidence To Look For

| Signal              | Where It Appears                                                        |
|---------------------|-------------------------------------------------------------------------|
| DOM sinks           | `innerHTML`, `insertAdjacentHTML`, `dangerouslySetInnerHTML`, template HTML |
| Export builders     | CSV/Excel/document generation from user-controlled values               |
| Storage writes      | `localStorage`/`sessionStorage`/`indexedDB` writes and logout cleanup   |
| A11y markers        | `aria-`, `role=`, `tabIndex`, `htmlFor`, keyboard handlers, `lang`      |
| Dead affordances    | Disabled-forever controls, unimplemented modals, unused API modules     |
| Contract consumers  | Client call sites, error-field reads, expected status codes             |

## Checks

### DOM Sinks And Export Injection

Run the DOM-sink census per `references/census-commands.md` and apply the sink rules in
`references/topics/frontend-security.md`.

Every sink fed by data that crosses a trust boundary gets a sanitization verdict -
`textContent`, a sanitizer, or a finding.

Export builders get a formula-injection verdict: cells starting with `=`, `+`, `-`, or `@`
from user data reach a spreadsheet unchecked unless the builder neutralizes them.

### Client-Storage Residue

Enumerate every storage key the client writes and every key the logout path clears.

Sensitive residue - session tokens, object identifiers with names or numbers, browsed-path
history - surviving logout is a finding on shared workstations.

### Accessibility Census

Count the markers per `references/census-commands.md`: `aria-` attributes, `role=`,
`tabIndex`, `htmlFor`, keyboard handlers, dialog semantics, and the `lang` attribute against
the UI language.

A near-zero count on a rendered UI is a finding of absence, graded against
`references/topics/accessibility-baseline.md`.

### Dead-Feature Census

Visible affordances wired to no-op or "unavailable" behavior are findings - the UI promises
a capability the product does not deliver.

Reconcile rendered formats and features against what the backend actually serves: a preview
branch for a format the API rejects is dead code and a contract drift.

Dead client helpers - API modules, store actions, exported utilities with no call site -
join the dead-code census in `assessment/code-quality.md`.

### Frontend-Backend Agreement

Apply the coupled-client reconciliation in `assessment/api-contract.md`, extended to the
wire contract's semantics:

- Status-code agreement: the codes the client branches on (401/403/404) are the codes the
  server emits for the matching conditions - a client that refreshes on 401 while the
  server answers 403 has a silent failure path.
- Error-body agreement: the fields the client reads from error responses are the fields the
  server writes - a handler reading `errorText` while the server emits `message` shows the
  user a generic failure forever.
- Capability agreement: role-dependent UI visibility matches the server's role matrix, and
  declared format or feature support agrees on both sides.

## Status Criteria

- `PASS`: No unsanitized sinks, storage cleaned at logout, accessibility markers present at
  meaningful density, affordances backed by real behavior, and the wire contract agrees,
  with evidence.
- `PARTIAL`: Coverage exists but censuses show gaps - unguarded sinks in bounded areas,
  partial cleanup, thin a11y coverage, or drift on some pairs.
- `FAIL`: Unguarded injection surface on user data, sensitive residue surviving logout, or
  systematic contract disagreement, with evidence.
- `UNKNOWN`: Client source was not provided or could not be inspected.

## Common Risks

- A single unsanitized sink turns stored user data into script execution in a victim's
  origin.
- Residual storage leaks identity and browsing context on shared machines.
- Dead features mislead users and hide the missing capability from defect tracking.
- Status or field drift between client and server produces silent failure modes the user
  cannot see or report.

## What Raises Confidence

- A censused sink list with a sanitization verdict each, not a sampled impression.
- Enumerated storage keys reconciled against the logout path.
- Accessibility density measured against a baseline, not asserted.
- The contract reconciliation run in both directions per `assessment/api-contract.md`.

Mark each missing signal explicitly rather than inferring its presence.
