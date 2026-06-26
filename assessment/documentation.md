# Documentation

## Purpose

> **Scope:** Code, API, and user documentation; onboarding; knowledge transfer
> **Key items:** README accuracy, API docs, inline docs, setup/onboarding, decision records

This file guides assessment of whether the system is documented well enough to be understood, operated, and extended.

Apply `principles/evaluation-rules.md` throughout. Assess whether documentation exists and matches the code, not its prose style.

## What To Evaluate

- Entry documentation: whether a README or equivalent explains purpose, setup, and usage.
- API documentation: whether public interfaces are documented.
- Inline documentation: whether non-obvious code carries explanatory comments.
- Onboarding: whether a new contributor can build and run the system from the docs.
- Knowledge transfer: whether key decisions and operational facts are recorded rather than tacit.

## Evidence To Look For

| Signal             | Where It Appears                               |
|--------------------|------------------------------------------------|
| Entry docs         | README, getting-started, usage guide           |
| API docs           | Generated API reference, interface docs        |
| Setup instructions | Build and run steps, environment requirements  |
| Inline docs        | Comments on non-obvious logic, doc comments    |
| Decision records   | ADRs, design docs, recorded rationale          |
| Doc-code agreement | Docs that match current commands and structure |

## Status Criteria

- `PASS`: Entry, setup, and interface documentation exist and match the code, with evidence.
- `PARTIAL`: Some documentation exists but is incomplete, outdated, or drifts from the code.
- `FAIL`: No usable documentation where the system's scale clearly requires it, with evidence.
- `UNKNOWN`: Documentation was not provided for review.

## Common Risks

- Missing setup docs block onboarding and raise the bus-factor risk.
- Documentation that drifts from the code misleads contributors and operators.
- Undocumented public interfaces force readers to infer behavior from source.
- Tacit knowledge is lost when contributors leave.

## What Raises Confidence

- An accurate README covering purpose, setup, and usage.
- Documented public interfaces and non-obvious logic.
- Setup instructions that match the actual build and run commands.
- Recorded decisions that explain why the system is built as it is.

Mark each missing signal explicitly rather than inferring its presence. Treat documentation that contradicts the code as a drift finding, not as present documentation.
