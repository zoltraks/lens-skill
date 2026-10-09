# Data Persistence Baseline

## Purpose

> **Scope:** Checkable constraints for projects that persist data: query construction,
> transaction and async boundaries, schema evolution, connection lifecycle, engine fidelity in
> tests
> **Key items:** bound parameters, migration discipline, short transactions, pragma/practice
> floors, engine-match testing

This file distills the SQLite documentation, the OWASP SQL Injection cheat sheet, and the
Jakarta Persistence specification sources listed in `references/source-catalog.md` into
constraints an audit can verify from repository source.

Snapshot date: 2026-10-09.

Feeds `assessment/baseline-conformance.md`, `assessment/security-review.md`, and
`assessment/nfr-review.md` for subjects classified `database` in
`references/domain-profiles.md`.

## Query Construction

From https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html.

- Every value reaching a query is bound - never string-concatenated or formatted into SQL.
  Identifier quoting is the narrow documented exception, not a license to build statements.
- Credentials never sit in source or configuration: the environment or a secret store
  supplies them, and connection strings in the repository are a finding regardless of
  environment targeting.
- Query errors propagate to the caller. Swallowing an error and returning an empty or default
  value hides corruption as missing data.

## Schema Evolution

- Schema changes are versioned migrations: immutable once released, applied in order at
  startup, and transactional (DDL rolled back on failure). A modified released migration is a
  finding - environment state can no longer be trusted.
- ORM auto-DDL is forbidden outside disposable environments: `ddl-auto: validate` at most in
  configuration, with real changes going through the migration path.
- Migration tests run against the real engine through containers or the project's declared
  equivalent - an embedded substitute accepts DDL the target rejects.

## Transactions And Async Boundaries

- Transactions live at the service boundary and stay short. A transaction never spans a
  network call, file IO, or an `.await` - each widens the lock window into contention the
  caller cannot see.
- A connection or transaction handle never crosses an `.await`: holding one suspends a scarce
  resource for an unbounded duration.
- Read-only report methods are explicitly non-transactional where the stack supports it, so a
  read cannot outlive its need.
- Optimistic concurrency (a `@Version`-style column) is the default answer to concurrent
  writes - destructive concurrent updates are a finding.

## Connection And Engine Floor

- The connection path is single-sourced: one constructor applies every pragma or session
  setting, so a connection that misses `foreign_keys`, journal mode, `synchronous`, or
  `busy_timeout` cannot exist in the codebase.
- Pools are sized to real concurrency. For embedded engines the pool serializes correctly
  (SQLite write concurrency is one) - a pool larger than the engine's honest ceiling is
  configuration noise, and blocking call sites that must serialize use an explicit per-resource
  lock.
- Embedded-engine tests prefer a temp file over in-memory: `:memory:` skips the WAL and
  locking paths the production file exercises.

## Derived Data

- Secondary indexes - full-text search, vector or derived stores - are owned beside their base
  data, updated in the same transaction where practical, and carry a single reindex entry point
  so rebuilding cannot be improvised per call site.
- A derived index with no rebuild path, or one built lazily on a hot request path, is a
  finding.

## Live Check

When web fetch is available, spot-check one pragma or session-setting default against the
target engine's documentation before citing the floor above.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
