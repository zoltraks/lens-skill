# Brief Report Style

## Purpose

> **Scope:** The `brief` report genre - a compact, status-driven decision brief for one project
> revision **Key items:** report overview, current state and gates, canonical findings,
> governed statuses, plan, known and deferred, evidence and trust, single report file

This file defines the report produced when `report-style: brief` is resolved during Parameter
Configuration in `process/audit-workflow/parameter-phase.md`.

The brief is the default review-oriented format - it replaces the `review` genre.

The former execution-register layout - verdict block, execution register, domain findings,
improvement plan, and retest register - is preserved as the `review (legacy)` variant in
`process/report-format/review-legacy.md`, selected by an explicit `review` or `review (legacy)`
request or by a recovered previous report carrying `Report Style: Review`.

A report under this contract records `Report Style: Brief` in its metadata table,
with no variant suffix.

The brief answers four questions in under five minutes of reading: what is defective,
what the plan is, what is known and deliberately not fixed, and how far the result can be trusted.

It judges the current revision - it never re-audits history.

All styles share one evidence base: the same evidence gathering, the same completeness rules,
and the same readiness gates.

Style changes presentation, never what must be found.

Read the sections the task needs - grep the `## ` headings for the section map.

## Contents

| Section                     | Line | What it covers                                    |
|-----------------------------|------|---------------------------------------------------|
| Shared Contract             | 52   | Carried-over rules from the shared format specs   |
| Deliverables                | 70   | One self-contained report file                    |
| Section Order               | 81   | Required and conditional section sequence         |
| Document Information             | 101  | Metadata table and executive summary              |
| Current State               | 115  | Status-driven readiness and gate block            |
| Findings                    | 152  | Canonical defect register                         |
| Plan                        | 222  | Prioritized action plan                           |
| Known And Deferred          | 236  | Accepted and deferred items                       |
| Evidence And Trust          | 250  | Evidence mode and confidence statement            |
| Changes Since Previous Report | 267 | Revision comparison block                        |
| Detail Levels               | 302  | Standard, detailed, and brief depth               |
| Polish Edition              | 310  | Polish rendering notes                            |
| Output Filename             | 316  | Brief filename convention                         |

## Shared Contract

The following carry over unchanged from `process/report-format.md` and its spec files:

- The metadata table row vocabulary per `report-opening.md` - it lives inside
  `## Document Information` instead of a separate Document Information section.
- Snapshot identity, read-depth, and claim traceability rules per
  `process/audit-workflow/audit-intake.md` and `process/audit-workflow/evidence-gathering.md`.
- The Contradiction Register per `synthesis/report-triangulation.md` whenever an external report
  was found at intake - it renders inside Evidence And Trust.
- Identifier, register-link, and formatting rules per `process/report-format.md` and
  `process/report-contract.md`.

The brief replaces the shared finding block schema with its own canonical record -
the Finding Record below is authoritative for this style.

`FND-STR-` structure findings load and render like any other finding.

## Deliverables

The brief produces exactly one artifact:

- `<STEM>-<rev>-<lang>.md` - the brief report itself, no more than 250 lines and 20 KB for a
  single-project subject.

Working artifacts - an evidence extraction or a findings JSON holding one record per finding
with every field from the analysis - may be kept in a temporary or working directory for the
run's own diffing needs. They are never delivered beside the report.

## Section Order

Produce these top-level sections in this order, with unnumbered headings:

- Document Information
- Current State
- Findings
- Plan
- Known And Deferred
- Evidence And Trust
- Changes Since Previous Report *(only when a previous brief report exists)*
- Glossary *(optional - always last when rendered)*

Sections the brief never carries: Document Information, Audit Coverage, Glossary Index,
Executive Summary, Verdict, Domain Ratings, System Context, Check Plan And Methodology,
Execution Register, Domain Findings, Risk Register, Improvement Plan, Remediation Phases,
Retest Register, Metrics Snapshot, Artifact Manifest, Further Verification, Scope Exclusions,
Known Limitations, Validation Protocol, Reference Sources, Recommendation Classification,
and any `RSK-`, `REC-`, `TDR-`, `EVD-`, or `PAR-` register row or block.

## Document Information

Opens the report with the metadata table alone - no executive summary paragraph.

Required rows, in order: `Report Revision`, `Report Date`, `Report Style` (`Brief`),
`Language`, `Evidence Mode`, `Subject Revision`, `Previous Report`, `Skill Version`,
`Time taken`.

`Previous Report` records `None` on a first brief or the prior report's filename.

Optional rows follow `report-opening.md` vocabulary: `Subject Version`, `Project`,
`Gate Profile`, `Known Horizon`, `Audit Purpose`, `Target Environment`, `Verification Scope`,
`Dirty-Tree State`.

## Current State

Answers "where are we now" - the state of the revision, not the method.

Open with a verdict sentence led by a plain word and carrying exactly one bolded token -
`The platform verdict reads **Not ready**` - one of:

- `Ready` - no open gate-blocker and no unaccepted Critical or High defect.
- `Conditionally ready` - release is possible once the named conditions are met.
- `Not ready` - a gate fails or a blocking defect is open.
- `Not assessable` - the evidence cannot support a verdict.

Follow with the gates table - one row per gate in the resolved profile:

| Gate | Result | Basis |
|------|--------|-------|

`Result` vocabulary: `Met`, `Met (provisional)`, `Not met`, `Not assessable`.

The default profile is `Laboratory`, `Controlled Sharing`, `Production` -
a project-defined profile from intake replaces it.

A provisional result labels the evidence gap in `Basis`,
and no gate claim exceeds what the evidence mode actually executed.

Then the status count table - one row per status in use,
counts reconciling exactly against the Findings summary table:

| Status | Findings |
|--------|----------|

Then at most five `## Immediate Actions` bullets - the P1 fixes and the items whose
closure changes the verdict - and at most three `## What Works` lines.

An optional compact domain table (`Area | Rating` with `Green`, `Amber`, `Red`,
`Not assessed`) closes the section when the project profile asks for domain ratings.

## Findings

One canonical record per finding - no risk or recommendation register exists.

The section opens with one summary table carrying every finding - a single row per finding
with a short summary in the `Fix` cell, no prose between rows:

| Finding | Area | Title | Severity | Priority | Status | Verification | Fix |
|---------|------|-------|----------|----------|--------|--------------|-----|

Every `### FND-<pillar>-NNN` block carries the description paragraph, then the field list:

```markdown
### FND-SEC-001: Custom provider headers expose secrets in API responses

<what is wrong, where it lives, and why it is a defect>

- **Area:** Backend
- **Severity:** High
- **Priority:** P1
- **Status:** Open
- **Verification:** Src
- **Blocks:** Controlled Sharing
- **Observation:** Masking covers standard fields, not arbitrary custom headers.
- **Impact:** Exposure of credentials to users who can read connection configuration.
- **Fix:** Extend secret masking to custom headers and add regression tests.
- **Effort:** Medium
- **Closure:** Sensitive headers render masked while provider use keeps the raw values.
```

Required fields, in order: `Area`, `Severity`, `Priority`, `Status`, `Verification`,
`Observation`, `Impact`, `Fix`, `Closure`.

`Blocks` renders only when the finding blocks a named gate.

Field vocabularies:

- `Severity`: `Critical`, `High`, `Medium`, `Low`, `Informational`.
- `Priority`: `P1` (blocks a gate or the release - mandatory on every gate-blocker),
  `P2`, `P3`.
- `Status`: `Open`, `Planned`, `In Progress`, `Known`, `Investigating`, `Fixed`,
  `Not a defect` - exactly one per finding, with the obligations below.
- `Verification`: `Exec` (observed in execution), `Src` (established from source),
  `Hyp` (hypothesis awaiting a check).
- `Effort`: a short token such as `Small`, `Medium`, `Large`.

`Critical` and `High` findings carry a `### FND-` block.

`Medium` and `Low` findings may render as one summary-table row plus a single
`- **FND-XXX-NNN:** <title> - <one-line statement>` line instead of a block,
and `Informational` findings always render as the one-line form.

### Status Obligations

The status carries its own obligations:

- `Open` - a confirmed defect not yet scheduled; `Fix` is required.
- `Planned` - assigned to the plan; `Fix` names the phase from the Plan table.
- `In Progress` - actively being worked.
- `Investigating` - a hypothesis awaiting the check named in `Closure`.
- `Fixed` - closed during this review or since the previous report;
  `Closure` cites the evidence that establishes it.
- `Not a defect` - rejected, with `Observation` carrying the justification.
- `Known` - deliberately not fixed now; four additional fields are required:
  `Reason` (why), `Owner` (who approved or `Not recorded`), `Review` (the review-by date
  or milestone), `Control` (the compensating control, or `None`).

The `Review` date resolves against the `Known Horizon` parameter - `Next milestone` by
default, a `90-day cap`, or a project-set horizon.

## Plan

The remediation plan as one table - phases replace the recommendation register:

| Phase | Target | Findings | Action |
|-------|--------|----------|--------|

`Phase` orders the work (`Immediate`, `Next release`, `Later`),
`Target` names the version or milestone when known and may stay a phase name,
`Findings` cites the covered `FND-` identifiers,
and `Action` states the work in one line.

Every `Planned` and `In Progress` finding appears exactly once.

## Known And Deferred

One table holding every `Known` finding - the governed record of what is deliberately
not fixed:

| Finding | Reason | Owner | Control | Review |
|---------|--------|-------|---------|--------|

The row mirrors the finding's decision fields verbatim.

An expired `Review` date is reconsidered at the next assessment.

When no finding carries `Known`, the section states `None recorded` once.

## Evidence And Trust

How far the result can be trusted - the honesty section replacing the validation protocol.

Cover, in compact prose or a small table:

- The evidence mode actually executed - `source-only`, `executed-readonly`,
  or `executed-commands` - and what that mode can and cannot establish.
- Coverage: components assessed, check categories run, deliberate omissions.
- Environment failures - every check that failed for environment reasons,
  separated from product defects and never counted as one.
- Unverified items: every `Hyp` finding and every claim carried on weaker evidence.
- Contradictions with external reports, when intake found one.

A gate or verdict never claims evidence beyond what ran -
an unrun or blocked check is `Not assessable`, never a pass.

## Changes Since Previous Report

Renders only when a previous brief report exists - it reconciles against that report's
finding records, never re-analyzed from prose.

One table, one row per prior or newly-tracked finding:

| Finding | Change | Notes |
|---------|--------|-------|

`Change` vocabulary: `New`, `Still Open`, `Resolved`, `Reopened`, `Deferred`, `Accepted`,
`Reclassified`, `Retired`.

Identifiers stay stable across revisions - a finding keeps its `FND-<pillar>-NNN` for life.

The counts reconcile: the previous report's statuses plus the change table equal the
current status count table.

## Glossary

Optional, and always the last section when rendered - a brief report carries no opening
Glossary Index.

One compact table, only the terms a decision reader needs to parse this report's findings:

| Term | Meaning |
|------|---------|

Include only project-specific or report-specific terms - omit well-known industry
vocabulary the audience already knows. Skip the section entirely when nothing qualifies.

Each glossary term's first occurrence in the report links to the glossary anchor -
`[Term](#glossary)` - and `link-glossary.py` counts table header cells and table body
cells as occurrences, so a term used as a column header links its header cell.

## Detail Levels

`Standard` and `Detailed` produce the full contract - `Detailed` permits longer `Observation`
text, the brief file budget still applies.

`Brief` keeps all sections but renders `Critical` and `High` findings only as blocks and
every other finding as a summary-table row.

## Polish Edition

A Polish brief pair carries identical identifiers, counts, statuses, and dispositions -
the Polish file is a translation, never a different assessment, and shares the report stem
with a `-PL` suffix.

## Output Filename

The brief filename stem is `BRIEF`, or the language-specific stem from the matching
`translations/` file such as `SKRÓT` for Polish.

A first brief defaults to the bare stem `BRIEF.md`,
with `BRIEF-1.0.md` offered as the revisioned alternative at delivery time.

When a previous brief exists, the filename carries the new revision,
for example `BRIEF-1.1.md`, per `synthesis/report-comparison.md`.
