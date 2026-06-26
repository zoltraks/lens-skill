# Change Management

## Purpose

> **Scope:** Feature flags, ADR usage, release governance
> **Key items:** controlled rollout, recorded decisions, change approval, traceability

This file guides assessment of how changes are introduced, recorded, and governed.

Apply `principles/evaluation-rules.md` throughout. Assess processes and artifacts, not the people who run them.

## What To Evaluate

- Feature flags: whether changes can be enabled and disabled without redeploying.
- Architecture decision records: whether significant decisions are recorded with context and consequences.
- Release governance: how changes are reviewed, approved, and traced to requirements.

## Evidence To Look For

| Signal              | Where It Appears                                 |
|---------------------|--------------------------------------------------|
| Feature flag system | Flag configuration, flag libraries, toggles      |
| Decision records    | ADR directory, design docs, recorded rationale   |
| Change review       | Pull request templates, review rules, approvals  |
| Traceability        | Links between changes and requirements or issues |
| Changelog           | Maintained changelog or release notes            |

## Status Criteria

- `PASS`: Changes are controlled by flags where useful, significant decisions are recorded, and a governed review path exists, with evidence.
- `PARTIAL`: Some governance exists but decisions are undocumented, flags are absent, or review is inconsistent.
- `FAIL`: No change control where it is clearly required, with evidence of absence.
- `UNKNOWN`: Change-management artifacts were not provided.

## Common Risks

- Without flags, risky changes require full redeploys to enable or disable.
- Undocumented decisions are re-litigated and lost as staff changes.
- Unreviewed changes raise the rate of defects reaching production.
- Lack of traceability makes it hard to tie a defect to its originating change.

## What Raises Confidence

- A feature flag mechanism with clear ownership and cleanup.
- Decision records that capture context, options, and consequences.
- A consistent, evidenced review and approval path.
- Changes traceable to requirements or tracked work items.

Mark each missing signal explicitly rather than inferring its presence.

## Architecture Decision Record Gap Assessment

For production-bound systems, the absence of Architecture Decision Records (ADRs) is a governance gap. Industry practice (the MADR standard and Michael Nygard's original ADR format) treats significant, hard-to-reverse decisions as artifacts that should be recorded.

A standard ADR records, at minimum: Title, Status (`Proposed`, `Accepted`, `Deprecated`, `Superseded`), Context, Decision, Consequences, and the Alternatives considered.

**What to evaluate**

- Whether a decisions directory exists (for example, `docs/decisions/`, `docs/adr/`) and contains ADRs.
- Which significant decisions lack a recorded rationale. List the decisions that should have been recorded, for example: choice of data store, choice of web framework, state management model, key algorithm weightings, and the authentication model.
- Whether the recorded decisions match the implemented system.

**Render as**

Render the ADR gap as a subsection of the Architectural Assessment per `process/report-format.md`. Present a table of decisions that should have an ADR, each marked `Recorded` or `Missing`, anchored to the file or code that embodies the decision.

**Interaction with AI provenance**

When the codebase shows AI-generated-code signals (see `assessment/ai-generated-code.md`), the absence of ADRs is more serious: without recorded rationale it is impossible to distinguish a deliberate decision from an AI default. Cross-reference the relevant `FND-AIP-XXX` finding.

**Status**

Use `PASS` when significant decisions are recorded and current, `PARTIAL` when some are recorded but key ones are missing, `FAIL` when no decisions are recorded for a production system with clearly significant choices, and `N/A` for a trivial system where no architectural decision rises to the level of an ADR.
