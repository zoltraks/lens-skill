# Code Quality

## Purpose

> **Scope:** Static analysis, complexity, duplication, dead code, type safety, style enforcement
> **Key items:** linting, formatting, type strictness, cyclomatic complexity, duplication, dead code

This file guides assessment of code-level quality in an existing or production codebase.

Apply `principles/evaluation-rules.md` throughout. This category covers code-level health,
architectural structure is assessed in `assessment/maintainability-review.md`.

## What To Evaluate

- Static analysis: whether linters or analyzers are configured and enforced, and which rules apply.
- Type safety: whether a type system is used and how strict its configuration is.
- Complexity: whether functions and files are bounded in size and branching.
- Duplication: whether logic is repeated rather than shared.
- Dead code: whether unreachable or unused code is present.
- Style consistency: whether formatting is automated and consistent.

## Evidence To Look For

| Signal               | Where It Appears                                         |
|----------------------|----------------------------------------------------------|
| Linter configuration | Lint config files, enabled rule sets                     |
| Type strictness      | Compiler or type-checker strict flags                    |
| Formatter            | Auto-format config, pre-commit formatting                |
| Complexity signals   | Very long functions, deep nesting, large files           |
| Duplication          | Repeated blocks, copy-paste logic                        |
| Dead code            | Unused exports, unreachable branches, commented-out code |

## Validate Static Claims

Treat lint configuration as evidence of configuration, not successful execution or enforcement.

Record the analyzer's declared version, rules, exclusions, and documented output in the evidence
ledger.

Before claiming a panic, trace guards, slice lengths, invariants, and the runtime's panic boundary.

Before claiming dead code affects compilation or runtime, verify module inclusion and reachability.

Line counts and method counts are investigation signals, not automatic severity thresholds.

For Rust unsafe-code claims, distinguish inspected first-party source from dependencies, macros,
generated code, native FFI, and the standard library.

For scoped unsafe-use statistics, rely on inspected source and committed reports such as
[cargo-geiger](https://github.com/geiger-rs/cargo-geiger) output, do not run tools. A clean
report is not proof of soundness or insecurity.

Report "no unsafe found in the reviewed scope", not "memory safe" or "no unsafe anywhere".

## Complexity Measurement

Estimate cyclomatic complexity per method from source parsing alone, never by execution. Count
one per method plus one per decision point: `if`/`else`, loops, `case`/`when` branches, `catch`,
ternaries, and boolean `&&`/`||` chains.

Flag methods above roughly 15-20, naming the file, method, and estimated count. Estimates are
`Inferred` evidence unless a committed metrics report supplies the value.

Before treating the metric as absent, look for a project-local metrics tool configuration and any
committed output or checkpoint history, such as a SourceMonitor `.smproj` file and its checkpoint
data or the equivalent for other stacks. Record committed metric output as `Reported` evidence
with the tool, version, and revision.

## Duplication Scan

Scan for near-duplicate blocks across files, source-only, using a token-based or structural
comparison. When no dedicated tool is configured, compare suspiciously similar regions manually
by structure: the same sequence of operations under renamed identifiers still counts as
duplication.

Flag candidate clusters explicitly, for example several hand-rolled codecs or parsers that share
one shape, and record the files and extent of each cluster.

## Status Criteria

- `PASS`: Linting, formatting, and type checks are configured and strict, with low complexity and
  little duplication, supported by evidence.
- `PARTIAL`: Some tooling exists but rules are loose, unenforced, or complexity and duplication are
  notable.
- `FAIL`: No static analysis or type discipline where the language and scale clearly call for it,
  with evidence.
- `UNKNOWN`: Source and tooling configuration were not provided.

## Common Risks

- Loose or unenforced lint rules let defects and inconsistencies accumulate.
- Weak type configuration permits a class of errors the type system could catch.
- High complexity raises change risk and lowers testability.
- Duplication causes incomplete fixes when only some copies are changed.
- Dead code misleads readers and hides the true behavior of the system.

## What Raises Confidence

- A strict, enforced lint and type configuration.
- Automated formatting applied consistently.
- Bounded function and file sizes with shared abstractions for repeated logic.
- Evidence that dead code is removed rather than accumulated.

Mark each missing signal explicitly rather than inferring its presence.
