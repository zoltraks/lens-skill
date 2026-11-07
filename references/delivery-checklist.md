# Delivery Checklist

## Purpose

> **Scope:** The authored-side checklist run before report assembly and the delivery gate run before
> the completion message **Key items:** register shapes, link semantics, ordering, parity, timing

The checklist consolidates what the validator enforces so authoring lands it on the first pass - run
it against the assembled report before the delivery gate,
and run the gate before the completion message.

Field-level register shapes are owned by `process/report-format/findings-registers.md` - this
checklist names the contract, never re-lists it.

## Authoring

Confirm each item while composing sections, not after assembly.

- Every `### FND-` block carries a description paragraph plus the field set in
  `findings-registers.md`, and `High` findings carry `Defect scenario` and a counter-check.
- `### RSK-`, `### REC-`, and `### TDR-` blocks exist for every register row,
  and each identifier family runs contiguously from `001`.
- Register summary rows carry the block's title text verbatim - the risk register's `Title` column
  copies its `### RSK-` heading.
- `EVD` and `PAR` identifiers are row-defined in tables under a single section,
  so their links point at the family section slug; `FND`, `RSK`, `REC`,
  and `TDR` links point at their `###` block slugs, never a section anchor.
- Every finding identifier appears inside the Remediation Roadmap or Recommendation Classification
  region, or carries an `Accepted - no action` disposition on its block.
- Debt-register `Category` values come from the CISQ set - Reliability, Performance Efficiency,
  Security, Maintainability.
- Structure Review verdicts use `Passed` / `Partially` / `Failed`,
  and findings-summary `Verification` cells use the qualifier vocabulary or the column is omitted.
- Requirements Conformance tables carry one row per declared requirement - merged range rows are a
  summary, not a grade - and the row count reconciles with the model registry.
- The Glossary Index holds a term table with linked entries plus the triplets table plus `###`
  definitions - prose-format glossaries yield zero parseable terms.
- Scorecard cells carry the point score only - uncertainty intervals disclose below the table per
  `process/readiness-scoring.md`.
- Remediation Roadmap sits penultimate, immediately before Reference Sources.
- No semicolons in prose, one sentence per paragraph, and ` - ` marks qualifiers only.

## Assembly

Apply these while building the report file.

- Author sections as part files under `work/`, assemble once,
  then let `finalize-report.py` own the pass order - glossary links, register links,
  table formatting, validation. Link insertion changes cell widths,
  so formatting always follows linking.
- Never splice tables by substring match - a cell-prefix match on shared vocabulary such as
  `Requirement` has swallowed an entire section's rows into the wrong table.
  Match on section boundaries and verify row counts after every structural edit.
- Multi-table edits in one pass run in reverse document order,
  or recompute offsets after each replacement - earlier positions go stale on insertion.
- Re-run the formatter and validator after each structural splice, not at the end of a batch.

## Delivery

Run the gate as the last operation before the completion message.

- `finalize-report.py --gate --model work/audit-model.json --state work/audit-state.json` must print
  `DELIVERY READY` - a `SKIPPED` model check means the reduced-scope caveat is
  disclosed, never silent.
- The git-status delta against intake is reported, never silently left.
- `Time taken` is written last, after the gate passes - the `TT:TT` placeholder never ships.
- The secrets sweep and redaction check complete before the completion message.
