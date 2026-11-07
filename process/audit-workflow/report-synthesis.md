# Report Synthesis

## Purpose

> **Scope:** The Synthesis phase of the audit workflow - style dispatch, report part assembly,
> reconciliations, and the counter-evidence review **Key items:** style dispatch, part assembly,
> counter-evidence review

This file is a phase of the audit workflow indexed by `process/audit-workflow.md`.

Follow it after Category Assessment.

On completion, proceed to `process/audit-workflow/report-validation.md`.

## Synthesis

When the report style is `hunt`, synthesize per `process/report-format/hunt-style.md`.

That style reuses the finding, risk, and roadmap schemas below with its own section order and adds
the journey-trace matrix, per-domain ratings, and the phase-mapped roadmap.

When the report style is `review`, synthesize per `process/report-format/review-style.md` - or
`process/report-format/structure-review.md` when the resolved scope is structure-only.

That style reuses the same schemas and adds the execution register, evidence levels,
and the retest register.

Render the Audit Coverage table first, from the fixed row set in `references/audit-taxonomy.md`.

It is the report's coverage declaration,
so it is assembled before any other section content and checked against Scope
Exclusions during Validation.

Tag every finding `Observation` or `Concern` per `principles/evaluation-rules.md`,
and attach an `Exploitability` narrative at an explicit tier to every `High` or `Critical` Security
& Compliance finding on a network-facing surface, per `references/exploitability-narrative.md`.

Under the default scope the tier is `Theoretical` or `Static-Confirmed`.

Build the unified risk register from the risks surfaced during assessment,
using `synthesis/risk-register.md`.

Every risk must reference its source `FND-XXX`.

Build the project scorecard using `synthesis/project-scorecard.md` and
`process/readiness-scoring.md`.

Render the score-bearing tables - Scorecard Summary, the headline score rows,
the frozen criteria table, and the Requirements Conformance table - with `scripts/render-tables.py`
(`--part scorecard|headline|criteria|requirements|all`, plus `--project` on multi-project models),
so the report never retypes a model value.

Render the register tables - the findings summary, risk register, remediation roadmap,
and evidence ledger - with `scripts/render-tables.py`
(`--part findings|risks|roadmap|evidence|registers`).

Hand-authoring register tables is the largest mechanical error surface:
every row the model already carries must come from the renderer, never be retyped.

Present the scoring rubric before the scores.

Wherever an overall score is stated, report the lowest-scoring applicable dimension and its score
alongside the mean, so a weak pillar is not hidden inside an average.

Record confidence, score caps, and readiness gates separately from the mean.

Draft the High-Level Observations section by selecting the top 5 most important findings from
the Technical Findings.

Keep each observation brief, full detail lives in the finding blocks.

Draft the Strengths & What's Working section by identifying 5-8 evidenced positive
baselines from the codebase.

Surface trade-offs both as a standalone Solution Comparison section (using
`synthesis/solution-comparison.md`) and embedded into relevant architectural or design findings
where they directly explain a specific finding.

When structural debt distinct from risks was surfaced,
build the Technical Debt Register using `synthesis/debt-register.md`.

Every debt item must trace to a finding or a cited direct observation.

Draft the actionable remediation roadmap using `synthesis/remediation-roadmap.md`.

Every recommendation must resolve a specific `FND-XXX`.

At `Standard` and `Detailed` detail levels, classify every `REC-XXX` as `Recommended`, `Optional`,
or `Not recommended` for the Recommendation Classification subsection of the roadmap per
`synthesis/remediation-roadmap.md`.

When the roadmap contains at least one P1 or P2 recommendation,
build the Follow-up Plan subsection at the bottom of the roadmap using `synthesis/reaudit-plan.md`,
mapping those findings to verification owners and closure evidence.

A fresh audit is always generated from the current report-format specification - never composed by
transforming a previous report file. A previous report may be an older contract revision - cloning
it imports stale sections, field vocabularies,
and table shapes that the current spec removed or renamed.
Use it only to recover parameters and to seed a verification checklist.

When applying scripted or mechanical edits to a draft,
assert each substitution matched before continuing - a pattern that matched zero lines is a failed
edit, not a completed one.

When a re-audit was confirmed during intake,
build the Changes Since Previous Audit section using `synthesis/report-comparison.md`,
comparing findings, risks, scores, and category statuses against the previous report.

Draft the Executive Summary last, after all findings, the risk register, and the roadmap are final.

It is the first section a reader sees but the last one synthesized,
so it summarizes only completed analysis.

Add the Production Readiness Threshold paragraph to it at this stage,
tying conditions to specific `RSK-XXX` IDs.

## Report Part Assembly

Before composing the report body, run a tooling probe against the report-production scripts:

copy `scripts/link-glossary.py`, `scripts/link-references.py`, `scripts/format-table.py`,
and `scripts/validate-report.py` (or `scripts/finalize-report.py`, which orchestrates all four)
into the audited repository under `.tmp.` names,
run them on a stub report carrying one canonical populated instance of every fixed field token
(`* **Absence:**`, `* **Exploitability:**`, `* **Status:**`, and so on),
and confirm the tools behave as specified.

Before drafting registers, read `validate-report.py --dump-contract` output for the mechanically
enforced contract - required sections, field lists,
token vocabularies - so blocks are composed to the enforced shape rather than corrected into it.

Scaffold the report with `scripts/new-report.py` (with `--projects` for multi-project subjects)
instead of hand-authoring the skeleton, so every required heading, table header,
and register block shape starts conformant.
When `work/audit-model.json` holds registers, `--model` also seeds the scorecard,
register rows and blocks, evidence ledger, and requirements table from the model,
so population is generated rather than transcribed.

Run `scripts/finalize-report.py` early and repeatedly while composing,
then continue editing on the formatted, linked text - link and format passes rewrite identifiers and
column widths, so exact-match edits against unformatted content miss.

A probe failure means the toolchain, not the report, needs attention first.

Produce the report in this order so each mechanical pass is effective:

1. Finish all section content first. Every later cell-text edit changes column widths.
2. Run `scripts/link-glossary.py` on the report to insert glossary body links.
3. Run `scripts/link-references.py` to link every register-identifier reference to its definition
   or register section.
4. Run `scripts/format-table.py` once content is stable,
   so table alignment is computed once - it measures the full source cell, link markup included.
5. Run `scripts/validate-report.py` and fix whole issue classes per run, not one problem at a time.
6. Re-run the linking passes and formatter whenever report prose changes, then re-validate.


Compose every File-mode report as ordered parts, never as a single write.

A report delivered as Inline text is exempt,
and a Brief report delivered to a file may be written in one pass.

Parts are checkpoints: a lost or deleted output file, or a session that ends mid-synthesis,
resumes from the last written part instead of regenerating the whole report from context,
which also bounds the memory any single step can consume.

Write one part per file-writing call, each holding one or a few `##` sections,
so no call approaches the tool's input limit.

Never author report content through a shell heredoc or shell redirection:
long heredocs are truncated by input limits and leave silently partial files behind.

Joining existing part files into the output file is a mechanical copy, not authoring.

Name each part `.tmp.<stem>-part-NN.md` so it reads as scratch wherever it appears,
and write parts inside the audited repository's `work/` directory,
an existing `temp` or `temporary` directory when `work/` is unavailable,
and the repository root only when none exists.

When the scratch directory exists but the file-writing tool cannot write it - for example when the
tooling refuses a gitignored path - place the `.tmp.` part files beside the output file.

They follow the retention rule below like any other parts and must never survive delivery as visible
litter in the output tree.

When a baseline-integrity record exists,
re-verify that the previous report file still matches the recorded checksum before concatenating,
and stop and surface the discrepancy on a mismatch.

Concatenate the parts in the fixed section order into the final file with a mechanical file join,
never by rewriting the document from context.

Finalize with `finalize-report.py`, never by hand-ordering passes - glossary links, register links,
table formatting, then validation, in that order,
because link insertion changes cell widths and formatting must follow linking.

Structural edits land on section boundaries,
never on substring matches inside cells - a cell prefix shared with table vocabulary has swallowed
whole row blocks into the wrong table.
Multi-table edits run in reverse document order or recompute offsets after each replacement,
and every structural splice re-runs the formatter and validator immediately rather than
at the end of a batch.

The full authored-side checklist lives in `references/delivery-checklist.md`.

Parts may be written directly in the report language.

A second render pass over the whole document is not required and can itself exceed the write limit.

The English-mapped validation copy described in Validation still covers the mechanical checks for
a non-English report.

Keep the part files until the assembled report passes the formatting script,
`validate-report.py` with zero issues, the Pre-Delivery Mechanical Checklist, and the parity gate,
then remove them before the completion message.

Run the Pre-Delivery Mechanical Checklist and the formatting script on the assembled
file, not on the parts.

## Register-and-block Reconciliation

After any emission path - part assembly, in-place edit,
or chunked append - verify every `FND` row in each Technical Findings summary table pairs with
exactly one `### FND-<id>:` block and the file ends on a complete line.

A row without a block or a block without a row is truncated emission, not a valid report.

## Forced-compression Disclosure

When output constraints - context budget, write limits,
tooling - force the report below the declared detail level or register layout,
the Document Information table records the effective detail level and the Limitations section names
the compressed element.

A report silently smaller than its contract is a defect - the disclosure is the fix.

## Inherited-ledger Reconciliation

When a report extends, rebuilds, or derives from an existing report file,
evidence references in added or carried content resolve to the report's one evidence ledger - remap
numbering to the inherited `EVD` sequence instead of starting a second sequence.

When the audit edits an existing report file instead of composing parts,
for example on a re-audit that upgrades a prior revision, apply these mechanical-edit rules:

- Anchor every insertion, move, or replacement on a complete heading line including its `#` level,
  for example `^## frontend$`. A bare substring such as `## frontend` also matches the deeper
  heading `### frontend` and lands edits inside the wrong block.
- Scope block-relative searches to the enclosing section's start and end offsets,
  for example the `## backend` to `## frontend` span.
  A document-wide `find` returns the first occurrence,
  which is not necessarily the occurrence inside the intended block.
- Never edit table separator rows or splice cells by regular expression.
  A pattern such as `[-\s|]+` can cross a line boundary and merge the next data row into the
  separator. Rewrite the whole table block,
  then run `scripts/format-table.py` to rebuild padding and separators.
- After every scripted edit, re-run `scripts/format-table.py` and then `scripts/validate-report.py`.
  The validator prints at most ten problems per check,
  so iterate until it reports zero rather than assuming the first fix pass cleared everything -
  bounded by the three-iteration fix loop defined in `process/audit-workflow/report-validation.md`.
- Preserve the report's existing line-ending style when a script writes the file.
- Run `scripts/validate-report.py` once against an early partial assembly,
  for example after the first composed parts are concatenated,
  so systematic style violations surface before they replicate across the full report.

## Counter-evidence Review

During the Validation phase, run the second-pass review defined in `process/audit-model.md` once the
mechanical validation in `process/audit-workflow/report-validation.md` reports zero issues.

Challenge both inflated praise and unsupported defect claims,
and record retained disagreements and their dispositions in the model.

