# Zig Baseline

## Purpose

> **Scope:** Checkable constraints for Zig toolchains and codebases
> **Key items:** build.zig conventions, allocator discipline, comptime idioms, version pinning

This file distills the Zig language documentation listed in `references/source-catalog.md`
into constraints an audit can verify from repository source.

Snapshot date: 2026-09-30.

Zig is pre-1.0: the toolchain version is part of the contract and language semantics shift
between releases.

Feeds `assessment/best-practices.md`, `assessment/code-quality.md`, and
`assessment/baseline-conformance.md` for Zig subjects.

## Toolchain And Build

From https://ziglang.org/documentation/master/.

- `build.zig` is the build program: `b.addExecutable`/`addStaticLibrary`/`addTest`, standard
  `target`/`optimize` options. Projects should record the Zig version they target
  (`.zigversion`, README, or CI matrix) because master and stable diverge.
- `zig build test` is the canonical test entry. `test` blocks inline in source files are the
  unit-test convention.
- `zig fmt` is the mechanical formatter. Unformatted source signals missing tooling.
- Release modes `Debug`/`ReleaseSafe`/`ReleaseFast`/`ReleaseSmall` trade checks for speed.
  `ReleaseSafe` keeps bounds/overflow checks - shipping `Debug` binaries is a finding.

## Language Discipline

- Allocators are explicit: functions take `std.mem.Allocator`. A function allocating without
  accepting an allocator hides ownership - a design finding.
- `defer`/`errdefer` handle cleanup. `defer` after resource acquisition is the leak-proof
  idiom.
- `unreachable` asserts the impossible. Reaching it in `Debug`/`ReleaseSafe` panics - its use
  on user-controlled paths is a finding.
- `undefined` marks uninitialized values. Reading `undefined` is UB - grep for it in
  security-relevant paths.
- `@cImport`/C interop discards Zig's safety at the boundary. `translate-c` output is
  generated code and is reviewed differently.
- Errors are values in error unions (`!T`). `try` propagates, `catch` handles -
  `catch unreachable` on fallible user-input paths is a defect.

## Live Check

When web fetch is available, verify the toolchain version this snapshot targets against
ziglang.org and record the drift window.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
