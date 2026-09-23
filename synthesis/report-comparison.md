# Report Comparison

## Purpose

> **Scope:** Locating a previously created audit report, assigning and naming the new report
> revision, and building the Changes Since Previous Audit section
> **Key items:** previous report discovery, iterative revisions, revisioned filenames, status
> transitions, `FND-XXX` continuity, fresh audit

This file defines how an audit incorporates a previously created audit report.

Apply `principles/evaluation-rules.md` throughout. A comparison claim follows the same evidence
rules as any finding. A status transition is asserted only from evidence in the current audit,
never assumed from the previous report alone.

## When This Applies

Apply this file when a previously created audit report exists in the audited repository or
directory and the user confirmed it as the re-audit baseline in the audit-mode question of
`process/audit-workflow.md`.

A previous report is identified by the audit report Document Information section, a
`Software Audit Report` title with `Report Revision`, `Report Date`, `State`, and
`Detail Level` rows, or by the audit filename convention: `AUDIT.md`, `AUDIT-<revision>.md`,
or the language-specific filename defined in `translation/`.

A file that shares the report directory but lacks these identification markers is not a previous
audit report. Status snapshots, state documents such as `current-state.md`, coverage or scan
output, and stakeholder documents are `Reported` evidence or context, never comparison baselines.

Older reports may record the metadata differently: a bold-label block with a `Version` field,
or a `Field`/`Value` table with a `Version` row. Read any of these forms as the report
revision.

Search for previous reports in this order:

- The path or file indicated in the audit request, when the user named one.
- The resolved output directory, including its version-numbered or date-named subdirectories.
- The default designated locations: `audit/` and `report/` directories and the bare roots under
  `docs/`, `document/`, and `doc/`, then the repository or directory root.
- Any other location in the document structure where an audit report file is found.

When several previous reports exist, compare against the one with the highest revision. When
revisions cannot be compared, use the report with the most recent `Report Date`. When neither
can be determined, use the most recently modified file and record the choice.

When no previous report exists, or the user confirmed a fresh audit, omit the Changes Since
Previous Audit section. Both cases need no omission note in Scope Exclusions.

When the section is present, place it immediately after the Executive Summary, per
`process/report-format.md`. For a multi-project report, place the combined section after the
condensed combined Executive Summary and give each compared project its own level-3 subsection.

## Fresh Audit

When the user chose a fresh audit over an existing report, this file's comparison rules do not
apply: the previous report's content is ignored entirely.

What still applies:

- The previous report file is never overwritten, renamed, or deleted.
- The report revision still increments from the highest revision found, per Report Revision,
  and the filename carries the new revision, per Output Filename.
- The cross-subject parity baseline below still applies, it diffs capability sets, not content.

What does not apply:

- No Changes Since Previous Audit section.
- No `Previous Report` row in Document Information.
- No parameter recovery from the previous report.
- No `FND-XXX`, `RSK-XXX`, or `REC-XXX` identifier continuity, sequences restart at `-001`.
- No Remediation Status carryover, comparison tables, or score deltas.

## Cross-Subject Parity Baseline

During the same discovery search, also record the most recent audit report found for ANY
subject, not only this subject's prior revisions, with its path and revision.

The consistency gate in `process/report-parity.md` diffs the new report's capability set against
that baseline before the report is marked final. Extract the baseline's capability set from its Validation
Record when present, otherwise from its section headings.

## Report Revision

The first audit of a subject is revision `1.0`.

Each subsequent report increments the minor component by one. When the minor component would
reach 10, increment the major component and reset the minor to 0.

| Previous | New  |
|----------|------|
| 1.0      | 1.1  |
| 1.9      | 2.0  |
| 9.9      | 10.0 |

When the previous report records no revision, treat it as `1.0` and assign the new report `1.1`.

Record the new revision in the `Report Revision` row of the Document Information section and
the previous report's path and revision in the `Previous Report` row.

## Output Filename

Never overwrite a previous report file. Each revision is a separate file so that audit history
stays comparable.

The default filename is `<base>-<revision>.md`, where `<base>` is the language-specific default
stem (`AUDIT` for English, the stem defined in `translation/` otherwise) and `<revision>` is the
new report revision. For example, `AUDIT-1.1.md` or `AUDYT-1.1.md`. A first audit uses revision
`1.0`, producing `AUDIT-1.0.md` or `AUDYT-1.0.md`, with the plain stem `AUDIT.md` offered as an
alternative at delivery time.

When the resolved output directory uses an existing naming convention, adjust the pattern to
fit it while keeping the revision distinguishable in the name.

When the user supplies an explicit output filename, honor it. If the supplied name collides
with an existing report file, do not overwrite it. Append the revision suffix or ask the user
for a different name.

Place each revision under the resolved output directory for the current audit date, for
example `docs/report/<audit-date>/` or the equivalent under `document/` or `doc/`. When the
previous report sits in the same date-named directory, the new revision lands beside it. Never
write a revision into a different report's directory and never modify directories of prior
audits.

## Comparison Content

Build the comparison from the previous report's Document Information, category assessments,
Detailed Technical Findings, Unified Risk Register, and Scorecard Summary.

Compare at least:

- Finding transitions: findings that moved between remediation states, keyed by `FND-XXX`.
- New findings: findings in the current audit with no counterpart in the previous report.
- Retired findings: previous findings that no longer reproduce, carried forward as `Closed`
  with the closing evidence rather than silently dropped.
- Risk delta: `RSK-XXX` entries added, mitigated, or unchanged.
- Score delta: per-dimension score movement and direction.
- Category status changes: categories that moved between `PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`,
  and `N/A`.

When a previous report element cannot be parsed well enough to compare, mark that element
`UNKNOWN` and state why.

When parameters differ between reports, for example a different evaluation scale or detail
level, note the difference before comparing, since it affects comparability.

## Evidence Transitions

Distinguish three kinds of delta in the Changes Since Previous Audit section.

- **Finding transition** - a finding moved remediation state, for example `Open` to `Closed`.
- **Evidence correction** - a figure or anchor was re-derived and differs from the previous
  report while the finding it supports is unchanged. List corrections in their own subsection,
  never as finding transitions.
- **Capability change** - the report structure differs because the skill version or parameters
  changed, not the audited product.

A refined figure does not change a finding's status by itself.

State the corrected value, name the counting method when the difference is methodological, and
keep the finding status it supports.

## Observation Folding

When a re-audit surfaces a defect not named in any previous finding, first check whether an
existing finding's description already covers that defect class.

Attach the observation to the covering finding as an evidence extension and record it in the
finding's evidence rows.

Mint a new `FND-XXX` identifier only when no existing finding covers the defect class,
continuing the per-pillar sequence per the Identifier Continuity rules.

## Identifier Continuity

Preserve `FND-XXX`, `RSK-XXX`, and `REC-XXX` identifiers across audits.

New findings continue the per-pillar sequence of the previous report. Retired identifiers are
not reused.

A finding is marked `Closed` only when the current audit holds the evidence that closes it.
A finding that still reproduces stays `Open` even when the previous report claimed progress.

When the report structure itself forces renumbering, for example when registers move from a
combined layout to per-project scope, re-scope the identifiers to the current structure and
publish the complete old-to-new mapping in the Changes Since Previous Audit section. The
mapping is mandatory, it is what keeps a renumbered register comparable across revisions.

When a previous recommendation references a source that is not an `FND-XXX` identifier, for
example "Dependencies (both)" or "API Contract", create the covering finding under the current
pillar sequence and mark it `New` in the finding transitions, do not carry a dangling
reference forward.

## Remediation Status

Use this fixed vocabulary in the Remediation Status column during a re-audit.

| Status              | Meaning                                                                |
|---------------------|------------------------------------------------------------------------|
| `Open - Confirmed`  | The finding's anchor was re-inspected and still reproduces             |
| `Open - Reported`   | Only historical executed evidence supports it, nothing was re-verified |
| `Closed - Verified` | Current-audit evidence closes it, cite the closing evidence            |
| `New`               | Minted in this revision                                                |
| `PASS`              | A passing control, re-verified                                         |

Carry the evidence qualification inside the status rather than inventing new markers.

## Rules

- Do not overwrite, rename, or delete the previous report file.
- Do not present a parameter difference as a product change. A score that moved because the
  scale changed is not an improvement.
- Do not copy conclusions, tool results, or readiness claims from the previous report into the
  current findings. Re-derive them from current evidence.
- Mark comparisons that cannot be completed `UNKNOWN` rather than guessing the previous state.
- Keep the fixed vocabularies. Describe direction with plain words such as `New`, `Closed`,
  `Up`, `Down`, or `Unchanged`, not new status markers.
- For multi-project reports, produce the comparison in the combined Changes Since Previous
  Audit section, one level-3 subsection per project, and qualify every identifier with the
  project identifier.
- Previous reports are comparison inputs, not audited source. Read them for transitions and
  parity, never count them in the file inventory or cite them as product evidence.
- A score that moved because the formula or presentation changed is a capability change.
  Record it outside the score-delta table, the table covers dimension changes only.
