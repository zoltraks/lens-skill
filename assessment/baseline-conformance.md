# Baseline Conformance

## Purpose

> **Scope:** Whether a code-bearing subject carries the engineering floor that well-governed
> projects of its detected stack and purpose standardize - independent of whether the subject
> documents its own standards
> **Key items:** universal floor rows, stack and purpose baseline digests, applicability
> conditions, baseline selection record

This file guides assessment of whether the project meets the baseline a comparable
well-governed project would carry, even when the subject documents no standards of its own.

Where `assessment/standards-conformance.md` measures the code against the project's own
documented rules, this assessment measures the code against the engineering floor that
projects using similar technology or serving a similar purpose widely adopt.

Apply `principles/evaluation-rules.md` throughout.

This assessment is conditional: it applies when the subject ships or develops executable
source and at least one bundled baseline digest covers its detected stack or nature.

When no bundled baseline covers the subject - for example a documentation-only repository or
a stack with no digest - omit this category and note the omission in Scope Exclusions.

## Baseline Selection

The governing baseline is chosen during Scope Definition and recorded in the Auditing
Methodology section.

Consult the baselines in this order:

1. The subject's own development standards documents, when found during intake - they are the
   project's declared floor and `assessment/standards-conformance.md` measures them.
2. The bundled digests: `references/stacks/` for the detected stack, `references/topics/` for
   the detected nature or purpose, mapped through `references/source-catalog.md`.
3. The live authoritative URL a digest names, only when the bundled material leaves the
   question open and fetching is permitted.

Record which baseline governed each judgement and the digest's snapshot date, so a report can
be re-derived later.

Never apply a baseline outside its applicability signals: an MCP contract applies to a project
that exposes tools over MCP, not to every project that happens to use JSON.

## Universal Floor Rows

These rows apply to every code-bearing subject regardless of stack:

| Baseline                      | Pass signal                                                              |
|-------------------------------|--------------------------------------------------------------------------|
| Runtime/toolchain pinning     | Manifest or toolchain file declares the floor and it matches the code    |
| Dependency reproducibility    | Lockfile committed, no floating versions on the release path             |
| Lint/format gate              | Formatter and linter configured and exercised by CI or a check script    |
| Test floor                    | Tests exist, run in CI or a documented command, and are not empty shells |
| Secrets hygiene               | No credentials in source or config, secret-bearing files are gitignored  |
| Error propagation             | Failures surface to the caller, no swallowed exceptions or ignored codes |
| Bounded work                  | Loops, polls, and external calls carry timeouts or element caps          |
| Documentation discoverability | Entry point (`README`/`AGENTS`) names how to build, test, and contribute |

A row that does not apply because the subject lacks the surface is `N/A`, not a pass.

## Stack And Purpose Rows

Rows drawn from the bundled digests apply only when their applicability signals fire:

| Baseline                                         | Applies when                                                                                     |
|--------------------------------------------------|--------------------------------------------------------------------------------------------------|
| CLI output/exit-code contract                    | Subject is `cli` nature - see `references/topics/cli-contract.md`                                |
| MCP tool schema and transport integrity          | Subject is `agent-tooling` over MCP - `references/topics/mcp-server.md`                          |
| UI-automation read-only contract and calibration | Subject is `automation` nature - `references/topics/ui-automation.md`                            |
| Performance budgets enforced                     | Subject declares budgets or is production-bound - `references/topics/performance-budgets.md`     |
| Inline/glue scripting discipline                 | Repository ships `.bat`/`.cmd`/`.ps1`/embedded scripts - `references/topics/inline-scripting.md` |
| Persistence transaction and migration discipline | Subject persists data - `references/topics/data-persistence.md`                                  |
| Own standards anatomy                            | Subject ships standards docs - `references/topics/standards-anatomy.md`                          |
| Stack-specific floor                             | Detected stack has a digest - `references/stacks/`                                               |

## Status Criteria

- `PASS`: Every applicable baseline row has source evidence of the expected control, and no
  row is a defect.
- `PARTIAL`: Some rows pass but others show the control absent, unenforced, or applied
  inconsistently.
- `FAIL`: Multiple applicable floor rows are absent where the subject's role makes them
  load-bearing.
- `UNKNOWN`: Evidence was not gathered deeply enough to judge the applicable rows.
- `N/A`: No bundled baseline covers the subject's detected stack or nature.

## Evidence To Look For

| Signal                     | Where It Appears                                                       |
|----------------------------|------------------------------------------------------------------------|
| Runtime pin                | `.nvmrc`, `global.json`, `rust-toolchain.toml`, `go.mod`, `engines`    |
| Lockfile                   | `package-lock.json`, `Cargo.lock`, `packages.lock.json`, `poetry.lock` |
| Lint/format config         | `.eslintrc*`/`eslint.config.*`, `.editorconfig`, `clippy` in CI        |
| CI exercise                | Workflow steps that run the linter, formatter check, or tests          |
| Test floor                 | `tests/`, `*test*`, CI `test` step, coverage config                    |
| Purpose baseline signals   | `mcp.json`/`tools/list` shape, UIA/WebDriver imports, `.bat`/`.ps1`    |
| Secrets hygiene            | `.gitignore` coverage, no `secrets.json`/`*.env` committed             |
| Documented-but-unrun check | Config exists but no CI step consumes it - an unenforced floor         |

## Requirement Interpretation

- A documented check that is never executed is weaker than an executed one - record it as
  documented-not-enforced, not as a pass.
- A missing baseline is an observation when the subject's role does not depend on it, and it is a
  finding only where the subject's purpose makes the control load-bearing.
- Cross-feed rows into the other categories: a missing lockfile feeds `dependency-review`, a
  missing test floor feeds `testing-review`, secrets findings feed `security-review`. This
  section reports the aggregate floor, not every individual gap.
- A subject's own documented standard overrides the bundled baseline where they conflict -
  record the override rather than silently applying the stricter external rule.

## Common Risks

- A project that documents no standards can still be well-governed, and this assessment fills the
  floor that `assessment/standards-conformance.md` cannot measure when no project documents
  exist.
- Baseline absence concentrated on one surface (for example, no exit-code contract on a CLI
  whose whole purpose is scripting) is a stronger finding than the same absence spread thin.
- An unenforced floor - a linter configured but never run in CI, a budget file nothing
  consumes - is harder to detect and more honest to report than a clean pass.
