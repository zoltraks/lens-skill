# Service Surface Baseline

## Purpose

> **Scope:** Checkable constraints for projects exposing network listeners - WebSocket handshake
> security, authentication ordering, protocol negotiation, HTTP error shape, stream semantics,
> abuse bounds **Key items:** Origin allowlist, auth-before-upgrade, subprotocol enforcement,
> RFC 9457, idempotency, bounded everything

This file distills the OWASP WebSocket Security Cheat Sheet,
the OWASP Web Security Testing Guide WebSocket chapter,
the OWASP Application Security Verification Standard, and RFC 6455 and RFC 9457,
as listed in `references/source-catalog.md`,
into constraints an audit can verify from repository source.

Snapshot date: 2026-11-05.

Feeds `assessment/security-review.md`, `assessment/api-contract.md`, `assessment/threat-model.md`,
`assessment/nfr-review.md`, and `assessment/baseline-conformance.md` for subjects classified
`service` in `references/domain-profiles.md`.

## WebSocket Handshake

From https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html and
https://wstg.owasp.org/ (WebSockets chapter).

- Every handshake validates the `Origin` header against an explicit allowlist of trusted origins -
  never a denylist, substring match, or wildcard.
  Unvalidated Origin enables Cross-Site WebSocket Hijacking when any ambient credential (cookie,
  token) rides the upgrade request.
  A non-browser channel that refuses `Origin` outright satisfies the same check.
- Authentication and authorization complete before `101 Switching Protocols` - identity, scope,
  subject-path binding, and principal state checks all run while refusal is still a
  normal HTTP response.
  An upgrade that completes before checks is a finding.
- `Sec-WebSocket-Protocol` subprotocols are negotiated from a declared set,
  and the negotiated protocol's security rules apply to the whole channel.
- Production transport is `wss://` only; a `ws://` listener is a finding outside a documented
  loopback or development-only path.
- `permessage-deflate` stays off unless needed - compression over secret-bearing traffic leaks
  content (CRIME/BREACH class).
- Bearer material never travels in the URL - query strings land in proxy and access logs
  tickets or headers carry tokens.
- The handshake authenticates, it does not authorize messages:
  every inbound frame that reads data or acts re-checks permission.

## HTTP Surface

From RFC 9457 and the OWASP API guidance.

- Error responses carry a machine-readable problem shape (`application/problem+json` or the
  subject's documented equivalent) with consistent type, status, and detail fields
  ad-hoc error bodies per endpoint are a consistency finding.
- Mutating operations honor an idempotency mechanism - a key, natural identifiers,
  or conditional headers - so safe retry cannot double-apply.
- Authentication failure responses are uniform across endpoints and leak no oracle about which claim
  or principal failed.
- Correlation identifiers generate at every entry point and propagate to downstream hops
  a surface without request-id plumbing limits incident reconstruction.

## Streaming Surfaces

- Server-Sent Events or equivalent streams support resume (`Last-Event-ID` or a documented cursor)
  where interruption loses acknowledged state, and close cleanly on principal revocation.
- Streams carry per-principal and total quotas the same way connections do.

## Abuse Bounds

- Every listener declares connection caps, frame and message size limits, idle and lifetime bounds,
  and per-principal rate buckets - an unbounded accept loop converts one client into a
  resource-exhaustion path.
- Progressive delay or equivalent throttling follows failed authentication on
  credential-verifying endpoints.
- Unauthenticated endpoints apply rate limits before any cryptographic or durable-write work.

## Live Check

The digested sources are live documents.

When a fetched version is available, fresh rules supersede this snapshot.
