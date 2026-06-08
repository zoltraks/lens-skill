# Actionable Remediation Roadmap

## Purpose

> **Scope:** Prioritized, traceable remediation plan with Impact vs Effort matrix, complexity ratings, and explicit verification steps
> **Key items:** `REC-[001]` indexing, `FND-XXX` traceability, priority tiers, non-prescriptive options

This file guides the remediation roadmap section. The goal is to present a prioritized, traceable plan where every recommendation resolves a specific finding.

Apply `principles/evaluation-rules.md` throughout. Do not issue absolute directives unless the user explicitly requests them.

## Prioritized Matrix

Present recommendations as a table. One row per recommendation. Use this fixed column order:

| Rec ID | Priority | Finding | Recommendation | Impact | Effort | Complexity | Verification |
|--------|----------|---------|----------------|--------|--------|------------|--------------|

Column meanings:

- **Rec ID**: `REC-[001]` ascending sequentially.
- **Priority**: `P1` (immediate), `P2` (short-term), `P3` (medium-term), `P4` (long-term).
- **Finding**: the `FND-[PILLAR]-[NNN]` identifier this recommendation resolves.
- **Recommendation**: a concise, actionable technical step.
- **Impact**: the business or technical impact of applying this fix (`High`, `Medium`, `Low`).
- **Effort**: the estimated engineering effort to implement (`High`, `Medium`, `Low`).
- **Complexity**: the architectural or organizational complexity of the change (`High`, `Medium`, `Low`).
- **Verification**: a specific test, command, or process to confirm the fix is successful.

## Priority Tiers

Use these tiers to rank recommendations:

- **P1 - Immediate**: Address critical security risks or data-loss scenarios. Implement within days.
- **P2 - Short-term**: Address high-severity findings that degrade reliability or compliance. Implement within weeks.
- **P3 - Medium-term**: Address average findings that affect maintainability or observability. Implement within months.
- **P4 - Long-term**: Address architectural or strategic improvements. Schedule for the next planning cycle.

## Rules

- Every `REC-XXX` entry must resolve a specific `FND-XXX`.
- Do not introduce new findings in this section. Recommendations must trace back to gaps in the Detailed Technical Findings & Assessment.
- Tie every recommendation to a finding from the assessment or risk register.
- Keep options non-prescriptive. Present them as choices with consequences.
- Do not rank or select a single option unless the user explicitly asks for a recommendation.
- When the user does ask for a single recommendation, state the chosen option, the reason anchored to evidence, and the residual risk.
- Keep language neutral and free of blame.
- When a recommendation would require information that was never provided, state the missing information rather than assuming it.
- Do not reproduce plaintext secrets, passwords, or cryptographic keys in the Recommendation or Verification columns.

## Relationship To Other Sections

Recommendations summarize and plan, they do not introduce new findings.

Every recommendation must trace back to a finding in the Detailed Technical Findings & Assessment or an entry in the Unified Risk Register.

Trade-off analyses appear both as a standalone Trade-off Analysis section (before the Remediation Roadmap) and embedded into relevant findings. The roadmap references the relevant `FND-XXX` finding regardless of where the trade-off is presented.
