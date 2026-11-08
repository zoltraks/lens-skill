# Final Adjustments

## Purpose

> **Scope:** The Final Adjustments phase of the audit workflow - the post-write confirmation and
> correction pass **Key items:** mechanical confirmation, completeness sweep, style confirmation,
> adjustment loop, delivery gate

This file is a phase of the audit workflow indexed by `process/audit-workflow.md`.

Follow it after Validation, once the report file is written.

The phase exists because a report is not finished when its prose is drafted:
style, format, and completeness defects are found and fixed here, before delivery.

## Contents

| Section                 | Line | What it covers          |
|-------------------------|------|-------------------------|
| Mechanical Confirmation | 27   | Mechanical Confirmation |
| Completeness Sweep      | 39   | Completeness Sweep      |
| Style Confirmation      | 54   | Style Confirmation      |
| Adjustment Loop         | 67   | Adjustment Loop         |
| Delivery Gate           | 84   | Delivery Gate           |


## Mechanical Confirmation

Run the finalization chain once more against the written report, in order:

1. `scripts/link-references.py` - repair identifier anchors after any late edits.
2. `scripts/format-table.py` - align every table to source width.
3. `scripts/validate-report.py` with `--model work/audit-model.json` and
   `--state work/audit-state.json` - the report must reach zero issues.
4. `git diff --check` - no whitespace or conflict-marker damage.

`scripts/finalize-report.py` runs the same chain - prefer it over the manual sequence.

## Completeness Sweep

Confirm every contract section the report declares is present and non-empty,
in the order the report style defines.

Confirm every register row has its block, every summary table reconciles with the register counts,
and every score, count, and headline value matches the model it renders from.

Confirm no `<placeholder>` cell, template token, or stale vocabulary survives in the shipped text.

Confirm every artifact declared in `work/audit-state.json` exists on disk.

Confirm the redaction sweep: no plaintext secrets, credentials, keys, internal addresses,
or personal identifiers anywhere in the report.

## Style Confirmation

Confirm no heading descends below level 3.

Confirm one sentence per line and no semicolons in prose - related sentences may share a paragraph
on consecutive lines.

Confirm every table is machine-formatted and every identifier citation resolves to its block anchor.

Confirm the Glossary Index covers every term and acronym used in the body.

Confirm the report follows `docs/STYLE.md` for every shipped surface.

## Adjustment Loop

Snapshot the report to `work/` before any automated transform so a bad pass is recoverable.

Fix every defect the sweeps surface in place - never regenerate a finished section wholesale,
and never drop a required section to silence a check.

Apply fixes at table or block scope - a multi-pattern regex pass across the whole document merges
rows, collapses separators, and corrupts register identifiers faster than it repairs them.

Re-run `scripts/validate-report.py` after each scoped adjustment until it reports zero issues - a
fix that grows the issue count is reverted, not layered over.

A defect that cannot be fixed in place - missing evidence,
an unverifiable claim - is corrected by marking it `Unknown` or `INSUFFICIENT INFORMATION`,
never by asserting it.

## Delivery Gate

The phase ends only when the mechanical chain reports zero issues and every sweep item holds.

Record the adjustments made and the final validator result in `work/audit-state.json`.

Then the report moves to the delivery path the parameters named - delivery is a consequence of a
confirmed report, never a step that can be skipped while defects remain open.
