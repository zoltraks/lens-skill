# Engineering Standards Anatomy

## Purpose

> **Scope:** How to judge whether a project's own development-standard documents are scoped,
> detectable, verifiable, and enforceable - the meta-level structure that makes a standard an
> audit instrument rather than a style essay
> **Key items:** scope and precedence, detection-first intake, non-negotiables, verification
> section, definition of done, versioned snapshots, source attribution

This file is distilled from engineering-standard corpora supplied to the maintainer during
skill upkeep. It carries no external source links because it describes the anatomy of a
standard, not a technology.

Snapshot date: 2026-10-09.

Feeds `assessment/standards-conformance.md` and `assessment/baseline-conformance.md` when a
subject ships its own standards documents.

## Scope And Precedence

- A checkable standard opens with what it covers and what it excludes: subject technology,
  project shape, and maturity level are declared up front.
- It states its precedence against other rules: user instruction, project-local convention,
  this standard, then general practice - a standard that does not say when it loses is
  unenforceable in a conflict.
- Applicability signals are named: file globs, directories, project types, or manifest markers
  that tell a reader whether the standard applies to the code at hand.
- A paired family of standards (general plus per-purpose) documents which overrides which -
  a specialized document that does not say "builds on" or "replaces" its parent leaves the
  layering undefined.

## Detection-First Intake

- A detection table maps observable repository signals to the standard's applicability and
  the inference confidence: `eslint.config.*` means JavaScript tooling, `*.csproj` means C#.
- Signals carry confidence levels (high/medium/low) so a single ambiguous marker does not
  trigger the whole rule set.
- Detection precedes evaluation: the audit first decides which standard applies, then checks
  the rules - the order matters because irrelevant rules applied anyway produce noise
  findings.

## Non-Negotiables

- A short list names the defect classes the standard treats as unconditional findings -
  never-allowed constructs, always-required controls - separate from the bulk of
  context-dependent guidance.
- Each non-negotiable is stated as a defect, not a preference: "secrets in source are a
  defect" is checkable, "prefer to avoid secrets" is not.
- The list stays short enough to memorize - a non-negotiable list longer than a screen signals
  the standard is a wishlist, not a floor.

## Verification Section

- A checkable standard closes with a verification table: what to run (or inspect), what the
  pass signal is, and which applicability condition governs the row.
- Commands in the verification table are real - they appear in the project's own build scripts
  or tooling - so "run this" can be tested without inventing a command.
- Rows carry applicability conditions so a verification step that needs a live service does
  not fail a repository-only audit.

## Definition Of Done

- A Definition-of-Done checklist enumerates what counts as finished for a change: build, test,
  format, document, verify - stated as checkable rows, not aspirations.
- DoD rows map to the verification table: "tests pass" links to the row that names the test
  command, so done-ness is a lookup, not an opinion.
- The checklist is ordered so cheaper checks run first - a DoD that demands the expensive
  check first teaches readers to skip it.

## Versioning And Sources

- The document carries a version header or snapshot date so a reader can tell whether two
  copies of the standard describe the same rules.
- Normative claims point at authoritative external sources - the tool's own documentation,
  the specification, a standards body's publication - so a rule can be checked against its
  source rather than the author's memory.
- Reasoning is annotated where the rule is surprising ("because ..."), which lets a maintainer
  tell load-bearing rules from cargo-culted ones.
- Deviations require a recorded reason: the standard names where an exception is documented
  (an ADR, a per-rule allowlist, a suppression comment) so silence is distinguishable from a
  permitted exception.

## Assessment Use

- When a subject ships its own standards, the audit checks the standards' own anatomy before
  checking the code against them - a standard with no detection table, no verification
  section, or no DoD is a finding about the project's governance, not about its code.
- A standards document that cannot produce a checkable row (no signals, no commands, no
  observable pass condition) is reported as governance-without-enforcement, distinct from
  absent governance.
- The anatomy applies to the subject's standards only - it is never turned on Lens's own
  digest files, which follow a different contract (`docs/MAINTENANCE.md`).
