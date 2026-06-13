# Re-audit and Follow-up Plan

## Purpose

> **Scope:** Verification ownership, re-audit triggers, sign-off gates, and evidence to close findings
> **Key items:** verification owner, target date, sign-off gate, closure evidence, `FND-XXX` traceability

This file defines the Re-audit and Follow-up Plan, the final section of the report. It makes the audit actionable in a governance sense, not just a technical one.

The convention follows ISO 19011 (guidelines for auditing management systems), which treats follow-up as part of a complete audit, and the monitor step of the NIST Risk Management Framework (NIST SP 800-37), which treats verification as continuous.

Apply `principles/evaluation-rules.md` throughout. Owners and dates are placeholders to be filled by the user's organization; mark them `NOT SPECIFIED` where the input does not provide them rather than inventing names.

## When This Applies

Include this section whenever the report contains a remediation roadmap with at least one P1 or P2 recommendation. For a report with no actionable findings, mark the section `N/A`.

## Table Format

Use this fixed column order. Include one row per P1 and P2 finding at minimum; P3 and P4 findings may be grouped.

| Finding | Priority | Verification Owner | Closure Evidence | Target Re-audit Trigger |
|---------|----------|--------------------|------------------|-------------------------|

When the report language is Polish, translate the column headers into Polish: `Znalezisko`, `Priorytet`, `Właściciel weryfikacji`, `Dowód zamknięcia`, `Wyzwalacz ponownego audytu`.

Column meanings:

- **Finding**: the `FND-XXX` identifier to be verified.
- **Priority**: the priority tier from the remediation roadmap (`P1`-`P4`).
- **Verification Owner**: the role responsible for confirming the fix, or `NOT SPECIFIED`.
- **Closure Evidence**: the specific artifact, test, or check required to close the finding.
- **Target Re-audit Trigger**: the milestone or date that should trigger re-verification, or `NOT SPECIFIED`.

## Sign-off Gates

State which findings gate a re-audit sign-off. As a default rule, every `CRITICAL` and `HIGH` finding must be closed before the system is signed off as production-ready. Tie each gate to its `RSK-XXX` so the Production Readiness Threshold in the Executive Summary stays consistent.

## Re-audit Schedule

State when a follow-up audit should occur. Use evidenced triggers rather than arbitrary dates:

- A targeted re-audit when all P1 findings report closure evidence.
- A full re-audit before the next major release or on a stated cadence.
- An event-driven re-audit when the architecture, stack, or trust boundary changes materially.

When the input provides no cadence or release plan, mark the schedule `NOT SPECIFIED` and state the recommended trigger neutrally.

## Rules

- Every row must reference a specific `FND-XXX`.
- Do not invent owner names or dates. Use `NOT SPECIFIED` where the input is silent.
- Closure evidence must be a concrete, verifiable artifact, not a vague assurance.
- Keep sign-off gates consistent with the Production Readiness Threshold and the Unified Risk Register.
- Phrase triggers and gates as options, not directives, unless the user asked for directives.
