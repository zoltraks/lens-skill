# Rust Baseline

## Purpose

> **Scope:** Checkable constraints for Rust crates and binaries
> **Key items:** API guideline subset, Clippy lint posture, RustSec advisories, Cargo semver
> rules, unsafe usage

This file distills the Rust API Guidelines, Clippy lint list, RustSec, and Cargo semver
reference listed in `references/source-catalog.md` into constraints an audit can verify from
repository source.

Snapshot date: 2026-09-30.

Feeds `assessment/best-practices.md`, `assessment/api-compatibility.md`,
`assessment/dependency-review.md`, `assessment/security-review.md`, and
`assessment/baseline-conformance.md` for Rust subjects.

## API Guidelines, Naming, And Layout

From https://rust-lang.github.io/api-guidelines/,
https://rust-lang.github.io/api-guidelines/naming.html, and
https://doc.rust-lang.org/cargo/guide/project-layout.html.

- Naming: `C-CASE` and `C-CONV` - crate names in `Cargo.toml` use `kebab-case` (or
  `snake_case`), module files and directories use `snake_case.rs`, types (`struct`, `enum`,
  `trait`) and enum variants use `UpperCamelCase` (`PascalCase`) with no `I` prefix on traits,
  functions, methods, variables, and struct fields use `snake_case`, constants and statics use
  `SCREAMING_SNAKE_CASE`, and conversions follow `to_`/`as_`/`into_` by cost and ownership
  (`C-CONV-TRAITS`).
- Cargo layout and code division: split `src/lib.rs` (exporting the crate's testable surface
  such as `pub fn build_app()`) from a thin `src/main.rs` binary entry point so integration
  tests in `tests/*.rs` drive the library crate directly, and place domain modules (`api.rs`,
  `domain.rs`, `error.rs`, `repository.rs`, `service.rs`) under `src/`.
- `C-COMMON-TRAITS`: public types implement `Debug`, and `Clone`/`PartialEq`/`Eq`/`Hash` where
  meaningful. `C-SEND-SYNC` types are `Send`/`Sync` where sensible.
- `C-FAILURE`: public functions that can fail return `Result`, never panic on user input.
  `unwrap`/`expect`/`panic!` in library paths are findings.
- `C-DOCUMENTATION`: public API items carry doc comments. `#![warn(missing_docs)]` or docs.rs
  renders are evidence.
- `unsafe` blocks require `// SAFETY:`-style justification comments by convention. Undocumented
  `unsafe` is a review finding.
- `#[must_use]` belongs on results the caller must not drop silently (`C-MUST-USE`).
- Cargo workspaces from https://doc.rust-lang.org/cargo/reference/workspaces.html: member
  crates sit in flat sibling directories (`crates/` or the root `members` globs), the root
  `Cargo.toml` is a manifest or virtual manifest (`[workspace]` with no `[package]`), the
  root `Cargo.lock` and `target/` are shared, and `[workspace.package]`/`[workspace.lints]`
  inheritance is the checkable uniformity mechanism.
- Server-shape role modules from the maintainer's Rust API standard: `src/` groups
  `api/` or `server/` (routes, `*State`, `*Request`/`*Response` types), `domain/` (entities,
  `*Error` enums), `repository/`/`store.rs` (single persistence module), `service/`, and
  `config.rs`/`main.rs` wiring - a `handlers.rs` grab-bag mixing domains is a division
  finding.
- File budgets: a `snake_case.rs` module approaching roughly 300 lines splits along type or
  trait boundaries into a directory module (`foo.rs` plus `foo/bar.rs`, or the 2018-edition
  `foo/mod.rs` form) - the audit checks the split happened, never which edition form the
  project picked.

## Clippy Posture

From https://rust-lang.github.io/rust-clippy/master/.

- `cargo clippy` is the de-facto linter. `-D warnings` in CI makes it a gate.
- `cargo fmt --check` plus `clippy` in CI is the baseline tooling pair.
- `#![allow(...)]` crate-level suppressions of `correctness` or `suspicious` group lints are
  findings. Targeted `#[allow]` on a specific item is a reviewable deviation.
- Workspace-level lint configuration (`[workspace.lints]` in the root manifest) keeps
  `clippy::pedantic`-class strictness shared across crates. `clippy::unwrap_used` denied in
  library code makes the `C-FAILURE` floor mechanical.

## Async And Concurrency

From https://tokio.rs/tokio/tutorial and the `tokio`/`std::sync` API documentation.

- Blocking work (file IO, synchronous drivers, CPU-heavy compute) runs on
  `tokio::task::spawn_blocking` or a dedicated thread, never inline in an async task - a
  blocking call inside `async` stalls the whole executor.
- Code inside `spawn_blocking` must be non-abortable: cancelling the returned `JoinHandle`
  does not stop the blocking work, so state the task mutates needs completion semantics, not
  cancellation assumptions.
- A connection or transaction handle never crosses an `.await` - holding one suspends a scarce
  resource for an unbounded duration. The full contract lives in
  `references/topics/data-persistence.md`.
- Shared mutable state uses a per-resource `Mutex` or a serialized owner task - `static mut`,
  `lazy_static`/`once_cell` singletons with interior mutability, and global registries are the
  reviewable patterns.
- `serde` contracts: `#[serde(deny_unknown_fields)]` on externally-accepted payloads catches
  client typos instead of silently dropping them, and `#[serde(rename_all = "...")]` on the
  wire type, not scattered per-field.
- Errors are typed at the crate boundary (`thiserror` for libraries, `anyhow`/`eyre` for
  binaries): a library that returns `Box<dyn Error>` or panics on failure is a finding.

## Dependencies And Advisories

From https://rustsec.org/ and https://doc.rust-lang.org/cargo/reference/semver.html.

- `Cargo.lock` is committed for binaries and applications. Libraries conventionally leave it
  out or commit it per project policy - the choice must be deliberate, not accidental.
- RustSec advisories (rustsec.org) feed `cargo audit`/`cargo deny`. Their committed report is
  advisory evidence.
- `cargo deny` can also enforce license allowlists and ban duplicate versions - check
  `deny.toml` when present.
- Cargo semver rules define what is breaking: removing items, changing public signatures,
  feature unification changes, and MSRV bumps are the checkable classes. Yankable releases
  mark withdrawn versions.
- Pre-1.0 crates (`0.x`) treat minor bumps as breaking under Cargo rules. Dependency freshness
  on `0.x` lines needs individual review.

## Live Check

When web fetch is available, spot-check one API-guideline rule ID against
rust-lang.github.io/api-guidelines and one advisory format against rustsec.org.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
