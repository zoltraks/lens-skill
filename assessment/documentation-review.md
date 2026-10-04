# Documentation

## Purpose

> **Scope:** Code, API, and user documentation, onboarding, knowledge transfer
> **Key items:** README accuracy, API docs, inline docs, setup/onboarding, decision records,
> contract references, calibration captures

This file guides assessment of whether the system is documented well enough to be understood,
operated, and extended.

Apply `principles/evaluation-rules.md` throughout.

Assess whether documentation exists and matches the code, not its prose style.

## What To Evaluate

- Entry documentation: whether a README or equivalent explains purpose, setup, and usage.
- API documentation: whether public interfaces are documented.
- Inline documentation: whether non-obvious code carries explanatory comments.
- Onboarding: whether a new contributor can build and run the system from the docs.
- Knowledge transfer: whether key decisions and operational facts are recorded rather than tacit.
- Contract and usage references: whether interface-contract or per-surface usage documents are
  maintained in lockstep with the implemented surface.
- Environment calibration: whether captured environment or target-application quirks are
  recorded separately from normative rules, so behavior-specific facts stay out of portable
  standards.
- Community health files: whether `SECURITY.md`, `CONTRIBUTING.md`, and `CODE_OF_CONDUCT.md`, or the
  stack's equivalents, exist.

## Evidence To Look For

| Signal             | Where It Appears                                       |
|--------------------|--------------------------------------------------------|
| Entry docs         | README, getting-started, usage guide                   |
| API docs           | Generated API reference, interface docs                |
| Setup instructions | Build and run steps, environment requirements          |
| Inline docs        | Comments on non-obvious logic, doc comments            |
| Decision records   | ADRs, design docs, recorded rationale                  |
| Doc-code agreement | Docs that match current commands and structure         |
| Contract docs      | Usage or interface references tracking the surface     |
| Calibration docs   | Quirk captures stored apart from normative rules       |
| Workspace contract | Disposable-workspace rules - location, marker, cleanup |
| Health files       | `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` |

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

A dedicated maintainer-onboarding document (a `HANDOVER.md`-style walkthrough for the next
maintainer) is continuity evidence distinct from contributor-facing `CONTRIBUTING.md` material.

A bounded Git summary such as `git shortlog -sn --no-merges HEAD` can inform contributor
concentration when history is in scope.

Record revision range, observation window, merge handling, bots, aliases, and any shallow history.

Commit concentration is only a proxy, it does not measure operational access, expertise, review
work, or the number of people able to restore service.

Request evidence of backup ownership, access handover, and a second operator's build/restore drill
before asserting a bus-factor number.

Report aggregate or role-level information, not personal rankings or contributor email addresses.

Whatever this pass collects must surface in the report,
per the collected-evidence rule in `process/audit-workflow.md`.

Contributor concentration, commit cadence,
and tag history appear at minimum as the Team & Continuity line in the Health Dashboard,
even when they produce no adverse finding.

## Community Health Files

Check for `SECURITY.md`, `CONTRIBUTING.md`, and `CODE_OF_CONDUCT.md`, or the stack's
equivalents.

The absence of `SECURITY.md` is a named finding, not a silent gap, whenever the audited subject
has any security-relevant surface and is published for external consumption.

The file conventions and `SECURITY.md` semantics are baselined in
`references/topics/project-health.md`.

## Documented-Claim Verification

Two mechanical drift checks apply to every documented surface.

The documented-figure check recalculates every quantitative claim in the docs - file counts,
test counts, coverage percentages, version numbers, supported-platform lists - against the
measured repository.

A documented figure that no census reproduces is a drift finding, and the measured figure is
recorded beside the claim.

The docs-to-code check diffs documented commands, options, environment variables, and file
paths against the implemented surface - every documented `npm run` script, CLI flag, env var,
and config key must resolve to the code.

A documented-but-unimplemented item is `NOT SPECIFIED` coverage drift. An implemented-but-
undocumented surface is a documentation gap.

Both directions are findings, never prose generalizations.

The embedded-code check diffs normative and reference code blocks inside documentation
against the implementation.

Classify each passage as normative design, illustrative pseudocode, or a
current-implementation excerpt before proposing correction: an excerpt that drifted is a
documentation defect, while a normative requirement the code violates is an implementation
defect.

## Agent-Facing Documentation

Agent-facing guidance documents are assessed elsewhere and cross-referenced here, not
duplicated: per-artifact format conformance belongs to `assessment/skill-definition.md`,
set-level topology and authority to `assessment/agent-guidance.md`.

When those assessments report drift in agent-facing documents, record it there and keep this
file's findings to the human-facing surface.

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

Mark each missing signal explicitly rather than inferring its presence.

Treat documentation that contradicts the code as a drift finding, not as present documentation.
