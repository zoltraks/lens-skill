# Actionable Remediation Roadmap

## Purpose

> **Scope:** Prioritized, traceable remediation plan with Impact vs Effort matrix, complexity
> ratings, and explicit verification steps
> **Key items:** `REC-[001]` indexing, `FND-XXX` traceability, priority tiers, non-prescriptive
> options

This file guides the remediation roadmap section. The goal is to present a prioritized, traceable
plan where every recommendation resolves a specific finding.

Apply `principles/evaluation-rules.md` throughout. Do not issue absolute directives unless the user
explicitly requests them.

## Prioritized Matrix

Present recommendations as a table. One row per recommendation. Use this fixed column order:

| Rec ID | Priority | Finding | Recommendation | Impact | Effort | Complexity | Verification |
|--------|----------|---------|----------------|--------|--------|------------|--------------|

When the report language is not English, apply the column header translations from the matching
`translation/` file.

Column meanings:

- **Rec ID**: `REC-[001]` ascending sequentially.
- **Priority**: `P1` (immediate), `P2` (short-term), `P3` (medium-term), `P4` (long-term).
- **Finding**: the `FND-[PILLAR]-[NNN]` identifier this recommendation resolves.
- **Recommendation**: a concise, actionable technical step.
- **Impact**: the business or technical impact of applying this fix (`High`, `Medium`, `Low`).
- **Effort**: the estimated engineering effort to implement (`High`, `Medium`, `Low`).
- **Complexity**: the architectural or organizational complexity of the change (`High`, `Medium`,
  `Low`).
- **Verification**: a specific test, command, or process to confirm the fix is successful.

## Priority Tiers

Use these tiers to rank recommendations:

- **P1 - Immediate**: Address critical security risks or data-loss scenarios before exposed use.
- **P2 - Short-term**: Address high-severity findings before the relevant readiness gate.
- **P3 - Medium-term**: Plan material maintainability or observability improvements.
- **P4 - Long-term**: Consider architectural or strategic improvements in a planning cycle.

Priority expresses urgency, not a delivery commitment, use only supplied or approved target dates.

## Rules

- Every `REC-XXX` entry must resolve a specific `FND-XXX`.
- Do not introduce new findings in this section. Recommendations must trace back to gaps in the
  Detailed Technical Findings.
- Tie every recommendation to a finding from the assessment or risk register.
- Keep options non-prescriptive. Present them as choices with consequences.
- Do not rank or select a single option unless the user explicitly asks for a recommendation.
- When the user does ask for a single recommendation, state the chosen option, the reason anchored
  to evidence, and the residual risk.
- Keep language neutral and free of blame.
- When a recommendation would require information that was never provided, state the missing
  information rather than assuming it.
- Do not reproduce plaintext secrets, passwords, or cryptographic keys in the Recommendation or
  Verification columns.
- Any recommendation stated in the Trade-off Analysis must also appear as a `REC-XXX` in this
  roadmap, traced to the same `FND-XXX`. Do not allow recommendations to exist only in the trade-off
  table.

## Cost To Reach Readiness

For readiness and due-diligence reports, summarize the work needed to satisfy the stated gates,
including material evidence gaps, not just the most visible code changes.

Use the cost-model rules in `synthesis/debt-register.md` even when no debt register is included.

Retain the compact impact/effort/complexity matrix and add supported cost ranges in recommendation
detail or a supplemental table.

| Work Item        | Source Recommendations | Effort Range   | Basis      | Dependencies    |
|------------------|------------------------|----------------|------------|-----------------|
| <canonical item> | <REC IDs>              | <range or gap> | <evidence> | <prerequisites> |

Sum only non-overlapping work in compatible units, with common work counted once.

Include tests, migration, review, rollout, and re-verification in the stated scope.

If any required work lacks an estimate, show the known subtotal and unestimated items, never label
the subtotal the total cost of production readiness.

Place the resulting range or `INSUFFICIENT INFORMATION` in the Executive Summary, along with its
scope, exclusions, confidence, and dependencies.

Keep infrastructure spend separate from one-time remediation and avoid currency conversions without
supplied rates.

## Verification Quality

Match verification to the actual defect and the chosen remediation option.

Require negative and positive controls, observable side effects, and an explicit success condition
for security-sensitive fixes.

A clean linter cannot close a behavioral authorization finding.

An unused module absent from the build cannot be verified removed merely by a clean build.

Do not recommend copying a read-path canonicalization check into create operations without checking
nonexistent paths and race conditions.

Check proposed library APIs and platform support against the intended versions before naming an
exact replacement call.

If an option only corrects documentation, do not claim it delivers the missing feature.

## Relationship To Other Sections

Recommendations summarize and plan, they do not introduce new findings.

Every recommendation must trace back to a finding in the Detailed Technical Findings or an entry in
the Unified Risk Register.

Trade-off analyses appear both as a standalone Trade-off Analysis section (immediately after the
Architectural Assessment) and embedded into relevant findings. The roadmap references the relevant
`FND-XXX` finding regardless of where the trade-off is presented.
