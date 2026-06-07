# Code Quality

## Purpose

> **Scope:** Static analysis, complexity, duplication, dead code, type safety, style enforcement
> **Key items:** linting, formatting, type strictness, cyclomatic complexity, duplication, dead code

This file guides assessment of code-level quality in an existing or production codebase.

Apply `principles/evaluation-rules.md` throughout. This category covers code-level health; architectural structure is assessed in `assessment/maintainability.md`.

## What To Evaluate

- Static analysis: whether linters or analyzers run and what rule sets are enforced.
- Type safety: whether a type system is used and how strict its configuration is.
- Complexity: whether functions and files are bounded in size and branching.
- Duplication: whether logic is repeated rather than shared.
- Dead code: whether unreachable or unused code is present.
- Style consistency: whether formatting is automated and consistent.

## Evidence To Look For

| Signal                       | Where It Appears                                   |
|------------------------------|----------------------------------------------------|
| Linter configuration         | Lint config files, enabled rule sets               |
| Type strictness              | Compiler or type-checker strict flags              |
| Formatter                    | Auto-format config, pre-commit formatting          |
| Complexity signals           | Very long functions, deep nesting, large files     |
| Duplication                  | Repeated blocks, copy-paste logic                  |
| Dead code                    | Unused exports, unreachable branches, commented-out code |

## Status Criteria

- `PASS`: Linting, formatting, and type checks are configured and strict, with low complexity and little duplication, supported by evidence.
- `PARTIAL`: Some tooling exists but rules are loose, unenforced, or complexity and duplication are notable.
- `FAIL`: No static analysis or type discipline where the language and scale clearly call for it, with evidence.
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
