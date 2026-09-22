# Re-audit And Follow-up Plan

## Purpose

> **Scope:** Verification ownership, re-audit triggers, sign-off gates, and evidence to close
> findings
> **Key items:** verification owner, target date, sign-off gate, closure evidence, `FND-XXX`
> traceability

This file defines the Re-audit And Follow-up Plan, which precedes the final References section.

It connects remediation to verified closure and accountable sign-off.

The convention follows ISO 19011 (guidelines for auditing management systems), which treats
follow-up as part of a complete audit, and the monitor step of the NIST Risk Management Framework
(NIST SP 800-37), which treats verification as continuous.

Apply `principles/evaluation-rules.md` throughout. Owners and dates are placeholders to be filled by
the user's organization, mark them `NOT SPECIFIED` where the input does not provide them rather than
inventing names.

## When This Applies

Include this section whenever the report contains a remediation roadmap with a P1 or P2
recommendation.

Otherwise omit this conditional section and explain the omission in Scope Exclusions.

## Table Format

Use this fixed column order. Include one row per P1 and P2 finding at minimum, P3 and P4 findings
may be grouped.

| Finding | Priority | Verification Owner | Closure Evidence | Target Re-audit Trigger |
|---------|----------|--------------------|------------------|-------------------------|

When the report language is not English, apply the column header translations from the matching
`translation/` file.

Column meanings:

- **Finding**: the `FND-XXX` identifier to be verified.
- **Priority**: the priority tier from the remediation roadmap (`P1`-`P4`).
- **Verification Owner**: the role responsible for confirming the fix, or `NOT SPECIFIED`.
- **Closure Evidence**: the specific artifact, test, or check required to close the finding.
- **Target Re-audit Trigger**: the milestone or date that should trigger re-verification, or
  `NOT SPECIFIED`.

## Sign-off Gates

State which findings gate a re-audit sign-off. As a default rule, every `CRITICAL` and `HIGH`
finding must be closed before the system is signed off as production-ready. Tie each gate to its
`RSK-XXX` so the Production Readiness Threshold in the Executive Summary stays consistent.

## Verification And Sign-off Evidence

Before using the report as a go/no-go gate, verify all `CRITICAL` and `HIGH` findings outside
the audit, not just a convenient sample, using checks capable of testing their claims.

For security defects, prefer a targeted regression test of the vulnerable boundary with permitted
and denied operations, supported by the manual trace and relevant scanner output.

Record the fixed revision, setup, command or procedure, result, residual risk, and reviewer role.

When runtime reproduction is unavailable, keep that limitation explicit and do not claim a
runtime-validated closure from a proposed test or unrelated clean scan.

Every gate needs a confirmed verification owner and acceptance evidence.

Leave unknown assignments `NOT SPECIFIED`, and list a suggested role separately as proposed,
awaiting confirmation.

Missing owners or required evidence keep sign-off pending even if the report itself is final.

Document completion and production approval are separate states.

Any authorized risk acceptance needs an accountable role, rationale, scope, expiry, compensating
controls, and re-audit trigger, it is not technical closure and does not imply `Production-ready`.

For multi-project reports, use project-qualified finding and risk references in every shared row.

Recheck advisories, artifact identity, and materially changed deployment assumptions at follow-up,
not just the edited lines.

## Re-audit Schedule

State when a follow-up audit should occur. Use evidenced triggers rather than arbitrary dates:

- A targeted re-audit when all P1 findings report closure evidence.
- A full re-audit before the next major release or on a stated cadence.
- An event-driven re-audit when the architecture, stack, or trust boundary changes materially.
- An SBOM-drift re-audit when a dependency manifest or lockfile changes, re-running the component
  inventory and the license-classification pass.
- A license/IP-evidence re-audit when the project's own license, notices, ownership or assignment
  documents, or vendored-code provenance changes.
- A delivery-practice re-audit when the pipeline, release cadence, or deployment mechanism changes
  materially, recomputing the proxies rather than carrying them forward.
- An exposure re-audit when the network-facing surface changes: new endpoints, listeners, message
  consumers, or externally supplied input parsers invalidate `Theoretical` narratives and the
  threat model.
- A continuity re-audit when ownership or contributor concentration changes materially, or when
  team, support, or cost evidence arrives that was `NOT SPECIFIED`.
- A compliance-evidence re-audit when new control artifacts (policies, committed scan results,
  audit reports) arrive that the previous review lacked.
- A pentest-escalation trigger: when a `HIGH` or `CRITICAL` security finding on a network-facing
  surface remains `Theoretical` after remediation planning, name a scoped live penetration test
  as the confirming engagement rather than leaving the tier unresolved.

When the input provides no cadence or release plan, mark the schedule `NOT SPECIFIED` and state the
recommended trigger neutrally.

## Rules

- Every row must reference a specific `FND-XXX`.
- Do not invent owner names or dates. Use `NOT SPECIFIED` where the input is silent.
- Closure evidence must be a concrete, verifiable artifact, not a vague assurance.
- Keep sign-off gates consistent with the Production Readiness Threshold and the Unified Risk
  Register.
- Phrase triggers and gates as options, not directives, unless the user asked for directives.
