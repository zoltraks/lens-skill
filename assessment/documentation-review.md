# Documentation

## Purpose

> **Scope:** Code, API, and user documentation, onboarding, knowledge transfer
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

## Architecture Documentation Coverage

Use [arc42](https://arc42.org/overview) as a coverage aid, not a required document format.

Map existing material to goals, constraints, context, solution strategy, building blocks, runtime,
deployment, crosscutting concepts, decisions, quality scenarios, risks/debt, and glossary.

Reference existing documents rather than requiring twelve new sections for a small system.

Use the [C4 model](https://c4model.com/) for appropriate context, container, and component views.

A C4 container is a deployable or executable unit, not necessarily a Docker container.

C4 diagrams supplement the security DFD and do not replace trust-boundary or data-flow analysis.

Check diagrams against actual routing and storage access, not a generic template.

Review significant decisions using `assessment/change-management.md`.

## Support Continuity

For production readiness or technical due diligence, assess knowledge concentration and handover
artifacts as system continuity risks, not individual performance.

Inspect ownership files, support procedures, reviewer coverage, onboarding evidence, and maintenance
of critical subsystems.

A bounded Git summary such as `git shortlog -sn --no-merges HEAD` can inform contributor
concentration when history is in scope.

Record revision range, observation window, merge handling, bots, aliases, and any shallow history.

Commit concentration is only a proxy, it does not measure operational access, expertise, review
work, or the number of people able to restore service.

Request evidence of backup ownership, access handover, and a second operator's build/restore drill
before asserting a bus-factor number.

Report aggregate or role-level information, not personal rankings or contributor email addresses.

Whatever this pass collects must surface in the report, per the collected-evidence rule in
`process/audit-workflow.md`. Contributor concentration, commit cadence, and tag history appear
at minimum as the Team & Continuity line in the Health Dashboard, even when they produce no
adverse finding.

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
