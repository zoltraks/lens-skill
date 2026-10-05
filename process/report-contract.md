# Report Contract

## Purpose

> **Scope:** The mechanically enforced surface of every Lens report
> **Key items:** required sections, field syntax, token vocabularies, hunt-specific rules

This file lists only what `scripts/validate-report.py` enforces - nothing more.

The same contract is available as JSON through `python scripts/validate-report.py
--dump-contract`, generated from the live constants, so an agent can load it without
reading this file.

Rationale and detail live in the section specs under `process/report-format/` and
`synthesis/` - this page is the fast check, not the specification.

## Every Report

- Headings never go deeper than `###`, and every heading is followed by exactly one blank
  line.
- No semicolons in prose outside code spans and link targets - use a comma or split the
  sentence.
- No em dash, en dash, or Unicode arrow outside code spans - use `-` and `->`.
- Every table's separator widths match its header cell widths and all pipes align
  vertically - run `scripts/format-table.py` rather than aligning by hand.
- No trailing whitespace, and the closing line `End of audit report` is never written.
- Document Information carries `Report Style`, `Evidence Mode`, and a `Subject Revision`
  snapshot anchor.
- A report under `Evidence Mode: source-only` carries an `Operator Verification Handoff` -
  under `executed-readonly` an `Executed Evidence Log` replaces it.
- The Audit Type Coverage table keeps only `Covered`, `Partially`, and `Not done` status
  cells - `Not Applicable` rows are omitted entirely.
- The Validation Record carries rows `PAR-1` through `PAR-18` in fixed order.
- `FND`, `RSK`, and `REC` references must resolve to defined entries - a `REC-XXX` or
  `RSK-XXX` cite of a nonexistent `FND-` fails.
- A `State | Draft` row marks a report in progress and skips the final-state gate, and a
  final report omits the row.

## Field Blocks

- The only parsed field syntax is `* **Field:** value` - an asterisk bullet, a bold field
  name, a colon outside the bold.
- Finding blocks require, in order: `Pillar`, `Severity`, `Type`, `Status`, `Change`,
  `Targets`, `Basis`, `Description`, `Impact`, `Recommendation`, `Method`, `Verified`,
  `Runtime confirmed`, `Confidence`, `Mitigating factors`, `Evidence`.
- Risk blocks require: `Severity`, `Likelihood`, `Residual`, `Status`, `Description`,
  `Impact`, `Trigger`, `Controls`, `Mitigation`, `Closure`, `Source`, `Confidence`.
- Finding identifiers match `FND-<pillar>-NNN` with pillar `ARC`, `CQY`, `SEC`, `INF`,
  `AIP`, `CPR`, or `API`.
- `Type` is `Observation` or `Concern`. `Verified` starts with `yes` or `no`.
  `Runtime confirmed` starts with `yes`, `no`, or `not applicable`. `Breaking change`
  starts with `None`, `Internal`, or `Public API`. `Applicability` starts with
  `applicable`, `conditional`, `inapplicable`, or `unverified`.
- A field whose value would be `N/A` or empty is omitted, never rendered blank.
- Legacy field names such as `Verification State` or `Remediation Status` are rejected -
  the current names are the ones above.

## Token Casing

English renders title case where the vocabulary lists give canonical uppercase names.

- Finding `Status`: `Open`, `Closed`, `PASS`. Finding `Change`: `New`, `Unchanged`,
  `Reopened`, `Closed`. Summary `Verification`: `Verified`, `Confirmed`, `Reported`, or
  empty for `New`.
- Risk `Status`: `Open`, `Accepted`, `Transferred`, `Monitoring`, `Closed`.
- Classification `Class`: `Recommended`, `Optional`, `Not recommended`.
- `Absence`: `No documented rationale`, `Deliberate - recorded decision`, `Undetermined`.
- A summary row's `Verified`/`Confirmed` claim must agree with the block's `Verified` and
  `Runtime confirmed` fields.

## Scorecard And Overall Score

- `**Scorecard Summary**` rows carry numeric `n/m` Score cells - the validator recomputes
  the mean and compares it to every stated `Overall score` row, and they must agree.
- `Overall score` never appears inside the scorecard table - it lives in the Executive
  Summary key-value table.
- Every line stating an overall `x.y/n` score needs the word `lowest` within six lines.
- `N/A` scorecard rows are omitted, never rendered.

## Multi-Project

- A report with a `Project Inventory` never uses `both`, `either`, or `the projects` as a
  table cell - rows name each project explicitly.
- Shared-register identifiers qualify as `<project>::FND-SEC-001`.
- The `Project` column appears only in shared tables - a single-project evidence ledger
  must not carry one.

## Hunt Style

Under `Report Style: hunt` the required sections are Document Information, Audit Type
Coverage, Verdict, System Context, Methodology And Evidence, Journey Traces, Domain
Findings, Risk Register, Remediation Phases, Scope Exclusions, Limitations and Unknowns,
Validation Record, References - plus Glossary, Contradiction Register, and the handoff or
executed-log section when conditional.

- The Verdict section carries a `Verdict:` token (`Ready`, `Conditionally ready`,
  `Not ready`), a domain ratings table, a gates table, a top-five actions list citing
  `REC-`/`FND-` identifiers, and at most five strengths.
- Domain ratings cover the fixed set Correctness, Security, Reliability, Performance,
  Dependencies, Deployment, Testability, Documentation, Maintainability, Provenance with
  values `Red`, `Amber`, `Green`, `Not assessed` - a `Red` or `Amber` row cites an `FND-`
  in its Basis.
- Journey hop tables use `Hop | Status | Evidence` with `conforming`, `failing`, or
  `not assessable` - a `failing` hop cites a defined `FND-`.
- The producer/consumer `Representation match` column takes `conforming`,
  `partially conforming`, `failing`, or `not assessable`.
- Domain Findings replaces Detailed Technical Findings for the summary-table and count
  checks - `###` domain headings sit inside the section and end only at the next `##`.
- Every `### FND-` block maps to a remediation phase or an `Accepted - no action` row, and
  multi-project findings match by `<project>::FND-` qualification.
- A `Recommendation Classification` section is forbidden under hunt - phases carry the
  disposition.
