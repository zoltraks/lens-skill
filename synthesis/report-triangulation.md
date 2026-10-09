# Report Triangulation

## Purpose

> **Scope:** Reconciling the audit's claims against prior or external audit reports of the
> same subject
> **Key items:** second-opinion input, contradiction register, snapshot binding,
> merge-versus-triangulate rule

This file defines how an audit treats another report about the same subject.

Apply `principles/evaluation-rules.md` throughout.

An external report is triangulation input, never adopted truth and never noise.

Two reports that name the same product version do not describe the same tree until their
snapshots match.

## When This Applies

Triangulation activates when intake finds either:

- A previous report produced by this workflow for the same subject (`Audit mode` handles
  its own reuse rules in `synthesis/report-comparison.md`, while triangulation governs the
  contradictions).
- Any external audit, review, or assessment of the same subject, found in the documentation
  roots, the repository root, or supplied with the request.

## Snapshot Binding

Before comparing claims, record each report's snapshot: commit SHA, branch, working-tree
state, and report date.

A report without a commit anchor cannot be proven to describe the audited tree.

When snapshots differ or are unknown, every conflicting claim is a candidate against the
current snapshot, not an established fact and not a refutation.

## Contradiction Register

When an external report exists, the audit report carries a `### Contradiction Register`
block inside Limitations And Unknowns, or inside the triangulation appendix at Detailed
level, listing every point where the reports assert incompatible facts:

| # | Topic | This audit | External claim | Evidence pointers | Status |
|---|-------|------------|----------------|-------------------|--------|

Status values: `Confirmed` - external claim verified at the audited snapshot. `Refuted` -
current evidence contradicts it. `Not reproducible` - snapshots or evidence differ beyond
resolution. `Pending` - requires evidence outside this audit's mode.

A `Pending` row names the check that resolves it in the Operator Verification Handoff.

No row is silently dropped.

## Rules

- Never interleave two reports' finding sets. Contradicting facts, different ID schemes,
  and different severity scales make concatenation misleading.
- Never import an external finding as an established fact. Re-inspect the cited location at
  the audited snapshot, then record the outcome. Until then the claim stays `Reported`
  evidence and its citation names the source report and its snapshot - a result from a
  different commit is never presented as this run's measurement.
- When a finding is retained on the external report's authority alone, name that provenance
  in the finding's Evidence field (for example `Reported - REVIEW-1.1 S-4`) so the claim
  chain stays reconstructable.
- Never discard a recorded control merely because an external report contradicts it. Keep
  it provisional until the register resolves the row.
- Distinguish report defects (errors provable from a document alone, such as arithmetic)
  from software defects (claims requiring repository evidence).
- Record which external claims were confirmed, refuted, or left pending. The register is
  the audit trail for why two reports disagree.
- A fresh audit still performs triangulation: the register concerns the snapshot, not the
  report lineage.

## Re-audit Trigger

When a report is found with a publication date later than the last audit's snapshot, treat
each of its claims as a priority triangulation input for the next audit cycle.
