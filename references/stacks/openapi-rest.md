# OpenAPI And REST Baseline

## Purpose

> **Scope:** Checkable constraints for OpenAPI-described APIs and REST services
> **Key items:** spec-required fields, schema-object rules, error contract (RFC 9457), lint
> expectations, OWASP REST hardening

This file distills the OpenAPI Specification, Spectral, OWASP REST, and RFC 9457 sources
listed in `references/source-catalog.md` into constraints an audit can verify from repository
source.

Snapshot date: 2026-09-30.

Feeds `assessment/api-contract.md`, `assessment/best-practices.md`, and
`assessment/baseline-conformance.md` for API subjects.

## OpenAPI Structure

From https://spec.openapis.org/oas/v3.1 (canonical text mirror:
https://github.com/OAI/OpenAPI-Specification).

- An OpenAPI document requires `openapi` (version string) and `info` (`title`, `version`).
  `paths` may be empty in 3.1 but a contract with zero paths describes no API.
- Every operation gets `operationId` by convention for tooling and traceability. Operations
  without it generate unstable names.
- `responses` is required on every operation and needs at least one declared response. The
  absence of `4xx`/`5xx` responses on mutating operations is a contract gap.
- `$ref` resolution rules: sibling keys of `$ref` are ignored (3.0) or allowed (3.1 with
  `summary`/`description`). Unresolved `$ref` targets are a contract defect.
- `components.schemas`, `parameters`, `responses`, `securitySchemes` hold reusable objects.
  inline duplication where components exist is a maintainability observation.
- `security` at root sets the global requirement. An operation-level `security: []`
  explicitly marks an endpoint public - that opt-out must be deliberate.
- `required` in schemas lists mandatory fields. A requestBody without `required` or
  `content` schema is unverifiable by consumers.

## Error Contract

From https://datatracker.ietf.org/doc/html/rfc9457.

- RFC 9457 `application/problem+json` is the standard error body: `type` (URI reference,
  `about:blank` default), `title`, `status`, `detail`, `instance`. Extension members are
  permitted.
- `status` in the problem body should match the HTTP status. Divergent values are a defect.
- APIs that document `4xx`/`5xx` responses but return ad-hoc `{"error": "..."}` bodies break
  the documented contract. Either is legal but they must match the spec.
- Deprecation is signaled by the HTTP `Deprecation` header/`deprecation` property on
  operations, not by prose alone.

## Lint Expectations

From https://stoplight.io/open-source/spectral (Spectral has moved homes. The ruleset
semantics below are the stable part).

- Spectral's `oas` ruleset is the de-facto baseline: operation descriptions, `operationId`
  uniqueness, `tags` consistency, schema `type` declarations, `example`/`examples` presence.
- A project claiming OpenAPI conformance without a lint config (`spectral.yaml`/`.spectral.*`)
  has unenforced conformance - an observation, not a defect.
- Custom rulesets extending `oas` inherit the baseline. `extends: []` removes it.

## OWASP REST Hardening

From https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html.

- HTTPS everywhere. HTTP endpoints redirect rather than serve.
- AuthN/Z on every non-public endpoint, with object-level authorization per resource (IDOR
  class).
- Input validation on parameters/body. Allowlist, not denylist, where a schema exists.
- Rate limiting and request-size limits on mutating and expensive routes.
- No sensitive data in URLs (query strings are logged). Credentials and tokens belong in
  headers or bodies.
- `Content-Type`/`Accept` handling with 406/415 responses on unsupported media types.
- CORS allowlists origins for browser-facing APIs. `Access-Control-Allow-Origin: *` with
  credentials is a defect.

## Contract Discipline

- The spec is the contract of record when the project declares contract-first: implementation
  drift from the spec is a finding in whichever direction it goes - an undocumented route is
  as much a gap as an unimplemented documented one.
- Composition keywords are chosen deliberately: `allOf` for extension, `oneOf`/`anyOf` for
  alternation - a `oneOf` where `anyOf` is meant rejects valid payloads.
- Examples are everywhere a consumer copies from: every schema carries `example`/`examples`,
  and every operation shows at least one success and one error body.
- `x-` extensions are the extension mechanism: their use is documented at the root or in a
  companion README so a reader knows which are load-bearing.
- Generated artifacts (clients, server stubs, HTML docs) are either committed with a pinned
  generator version or regenerated in CI - a half-committed generated tree drifts silently.

## Live Check

When web fetch is available, spot-check one required field against the OpenAPI text and one
RFC 9457 member against the RFC.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
