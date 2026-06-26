# Error Handling

## Purpose

> **Scope:** Exception handling strategy, retries, fallbacks, user-facing error handling
> **Key items:** consistent error strategy, retry safety, graceful degradation, clear failures

This file guides assessment of how the system behaves when operations fail.

Apply `principles/evaluation-rules.md` throughout. System-wide resilience patterns are also touched in `assessment/nfr.md`; here the focus is the code-level handling of failures.

## What To Evaluate

- Exception handling strategy: whether errors are handled consistently and at the right boundaries.
- Retries: whether transient failures are retried safely, with limits and backoff.
- Fallbacks: whether the system degrades gracefully when a dependency fails.
- User-facing error handling: whether failures produce clear, safe messages without leaking internals.

## Evidence To Look For

| Signal           | Where It Appears                                 |
|------------------|--------------------------------------------------|
| Error boundaries | Centralized handlers, middleware, error types    |
| Retry logic      | Retry helpers, backoff, idempotency handling     |
| Fallbacks        | Default values, circuit breakers, degraded modes |
| User messaging   | Error responses, status codes, message templates |
| Leak prevention  | Stack traces or internals hidden from users      |

## Status Criteria

- `PASS`: Errors are handled consistently at clear boundaries, retries are safe, fallbacks exist where needed, and user-facing failures are clear and safe, with evidence.
- `PARTIAL`: Handling exists but is inconsistent, retries are unsafe, or some paths swallow or leak errors.
- `FAIL`: Errors are unhandled or hidden where handling is clearly required, with evidence.
- `UNKNOWN`: Error-handling code was not provided.

## Common Risks

- Swallowed exceptions hide failures until they cause larger incidents.
- Unbounded or non-idempotent retries amplify load and cause duplicate effects.
- A failed dependency takes the whole system down for lack of a fallback.
- Internal details leaked in error messages aid attackers and confuse users.

## What Raises Confidence

- A consistent error strategy applied at well-defined boundaries.
- Retries with limits, backoff, and idempotency where side effects occur.
- Graceful degradation when non-critical dependencies fail.
- Clear, safe user-facing messages that do not expose internals.

Mark each missing signal explicitly rather than inferring its presence.
