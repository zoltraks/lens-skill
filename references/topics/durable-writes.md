# Durable Writes Baseline

## Purpose

> **Scope:** Checkable constraints for projects that must survive crashes and restarts - flush
> discipline, atomic replacement, journal/WAL ordering, torn-write handling,
> fencing **Key items:** fdatasync, directory fsync, tmp+rename, commit ordering, fencing tokens

This file distills the filesystem-durability literature - the Evan Jones durability survey,
"Files are hard", the PostgreSQL fsyncgate discussion,
and crash-consistency research - as listed in `references/source-catalog.md`,
into constraints an audit can verify from repository source.

Snapshot date: 2026-11-05.

Feeds `assessment/nfr-review.md`, `assessment/operational-readiness.md`, `assessment/data-flow.md`,
and `assessment/baseline-conformance.md` for subjects that persist state - any project classified
`service`, `cli`, or `library` in `references/domain-profiles.md` with an on-disk data directory.

This file covers filesystem-level durability.
`references/topics/data-persistence.md` covers the database-engine layer - query construction,
migrations, and connection lifecycle - and the two are complementary scopes, not overlapping rules.

## Flush Discipline

From https://www.evanjones.ca/durability-filesystem.html.

- Durable writes end in a flush primitive: `fdatasync` for data-only concerns,
  `fsync` when metadata (timestamps, size) must also persist, `O_DSYNC` / `O_SYNC`,
  or an equivalent synchronized-I/O flag.
  A write that returns without a flush is volatile, not durable.
- Creating a file durably requires flushing the containing directory - the file data and the
  directory entry are separate writes, and a crash can lose one without the other.
- Every flush and rename call's return value is checked and acted on:
  kernels before ~4.16 could swallow writeback errors,
  and retrying a failed fsync is not guaranteed to rewrite data already marked clean.
  An ignored persist error is a finding.

## Atomic Replacement

- File replacement follows the durable dance: write temp file on the same filesystem,
  `fsync` the temp, `rename` over the target, `fsync` the parent directory.
  Each skipped step names a real failure mode - torn content, zero-length targets, or lost renames.
- `rename` is atomic at the namespace level only: same filesystem, no implied durability,
  no implied ordering relative to earlier data writes.
  It never substitutes for the flush sequence.
- In-place overwrite of live state files is a finding unless the format tolerates torn content by
  design (checksummed records, append-only).

## Journal And Commit Ordering

- Commit order is data-before-metadata: the payload reaches stable storage before the record that
  publishes it (commit marker, checkpoint, index).
  Recovery must never observe the pointer without the payload.
- A journal or WAL carries its own integrity - per-entry checksum or length framing - so replay can
  stop at a torn tail instead of applying it.
- Restart replay is deterministic: the same log produces the same recovered state regardless of
  crash point, and recovery code has fault-injection coverage for boundary cases (mid-commit,
  mid-record, torn tail).
- A "never fsync" or relaxed-durability mode is acceptable only behind an explicit non-production
  gate - silently selectable lossy defaults are a finding.

## Ownership And Fencing

- One writer owns a data directory or shard at a time - enforced by lockfile, exclusive open,
  or documented process discipline.
- Distributed or failover writers carry fencing (monotonic tokens checked at write time,
  leases with expiry) so a stale or partitioned writer cannot commit after losing authority.

## Live Check

The digested sources are live documents and papers.

When a fetched version is available, fresh rules supersede this snapshot.
