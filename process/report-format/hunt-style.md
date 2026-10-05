# Hunt Report Style

## Purpose

> **Scope:** The `hunt` report genre - a verdict-first, domain-organized defect-hunt report
> **Key items:** verdict block, domain register, journey traces, phase roadmap, ratings,
> operator handoff

This file defines the report produced when `report-style: hunt` is resolved during Parameter
Configuration in `process/audit-workflow.md`.

The `audit` style measures conformance against the governed contract. `hunt` measures fitness
for use and orients every section toward what is broken, why it matters, and what to do first.

Both styles share one evidence base: the same evidence gathering, the same finding schema, the
same completeness rules, and the same readiness gates.

Style changes presentation, never what must be found.

## Shared Contract

The following carry over unchanged from `process/report-format.md` and its spec files:

- Document Information per `report-opening.md`, including `Report Style: hunt`.
- Audit Type Coverage per `report-opening.md`.
- The finding block schema per `findings-registers.md`, with the same field vocabulary.
- The risk register schema per `synthesis/risk-register.md`, the roadmap priority and phasing
  rules per `synthesis/remediation-roadmap.md`, and scoring semantics per
  `process/readiness-scoring.md` wherever gates or confidence apply.
- Snapshot identity, read-depth table, evidence ledger, and claim traceability rules per
  `process/audit-workflow.md`.
- The Contradiction Register per `synthesis/report-triangulation.md` whenever an external
  report was found at intake.
- Scope Exclusions, Limitations and Unknowns, Validation Record, and References per
  `report-closing.md`.

Hunt adds two mandatory finding fields everywhere the shared schema applies: `Breaking
change` and `Runtime confirmed` per `findings-registers.md`.

## Section Order

Produce these top-level sections in this order, with unnumbered headings:

- Document Information
- Audit Type Coverage
- Glossary *(when Descriptive mode is enabled)*
- Verdict
- System Context
- Methodology And Evidence
- Journey Traces
- Domain Findings
- Risk Register
- Remediation Phases
- Contradiction Register *(conditional - external report found at intake)*
- Operator Verification Handoff *(source-only mode)* or Executed Evidence Log
  *(executed-readonly mode)*
- Scope Exclusions
- Limitations and Unknowns
- Validation Record
- References

## Verdict

The Verdict section replaces the Executive Summary and is the first content a reader sees.

It carries, in order:

1. A purpose statement - what the subject is, what was audited, at which snapshot.
2. A one-paragraph plain verdict: `Ready`, `Conditionally ready`, or `Not ready`, plus one
   sentence on what the verdict does not mean.
3. The domain ratings table below.
4. The hard readiness gates: every gate listed with `Met`, `Not met`, or `Not assessable`.
5. A top-five action list naming the first remediation steps with their finding IDs.
6. A strengths list of at most five evidenced positives.

The verdict never hides a broken advertised workflow behind an average: any open hard-fail
gate makes the verdict `Not ready` regardless of other ratings, per
`process/readiness-scoring.md`.

## Domain Ratings

Hunt replaces the numeric dimension scorecard with a per-domain rating table:

| Domain | Rating | Basis |
|--------|--------|-------|

Domains are fixed: Correctness, Security, Reliability, Performance, Dependencies,
Deployment, Testability, Documentation, Maintainability, and Provenance, plus any
domain the domain profile activates.

Ratings use a defined scale, not judgment:

- `Red` - an advertised capability is broken or a `CRITICAL` finding is open in the domain.
- `Amber` - open `HIGH` or material `MEDIUM` findings exist without a broken capability.
- `Green` - no `HIGH` or `CRITICAL` finding is open and capabilities trace clean.
- `Not assessed` - no scoreable evidence, never folded into a positive rating.

The Basis cell names the finding IDs that set the rating.

An external quality model such as ISO/IEC 25010 may be mapped beside the domain table when
the audit applies it, citing the edition and the mapping per
`references/source-catalog.md` - `Not assessed` characteristics are never rated Green.

## System Context

A condensed context block: purpose statement, technology stack with locked versions from the
lockfiles, and a component inventory table with per-module size and role.

| Component | Lines | Role |
|-----------|-------|------|

## Methodology And Evidence

States the evidence basis declaration (tiers used and their mix), the read-depth table, and
the evidence ledger, all per the shared rules.

Under `executed-readonly` it also references the Executed Evidence Log.

## Journey Traces

A mandatory section carrying the cross-boundary evidence gathered per
`process/audit-workflow.md`:

- A producer/consumer matrix for every identifier or value crossing a component boundary,
  naming each site and the representation it emits or expects. Its `Representation match`
  column takes `Conforming`, `Partially conforming`, `Failing`, or `Not assessable`.
- A per-workflow trace for each advertised workflow in `Hop | Status | Evidence` tables,
  marking every hop `conforming`, `failing`, or `not assessable` with its evidence ID.

A failing hop must trace to a `FND-XXX` defined in the report - the validator rejects a
failing hop that cites no finding or an undefined one. A conforming hop is recorded, not
celebrated.

## Domain Findings

One findings register organized under `###` domain headings (the Domain Ratings set), each
finding keeping its shared `FND-<pillar>-NNN` identifier and full block schema.

The section opens with a summary table carrying the shared columns (`Finding`, `Result`,
`Status`, `Change`, `Verification`, plus `Project` when multi-project), and the validator
reconciles its row count against the `### FND-` blocks - the `###` domain headings do not
close the section, only the next `##` does.

Every finding cites `path:line` evidence and carries `Breaking change` and `Runtime
confirmed` fields.

In a multi-project report the register stays single and unified. Each finding records its
project in `Targets` and the summary table carries a `Project` column.

## Remediation Phases

The roadmap groups recommendations into phases ordered by dependency - for example
`Stabilize`, `Harden`, `Improve` - where each phase lists its recommendations, acceptance
criteria, verification steps, and the findings each closes.

Every finding maps to a phase or to an explicit `Accepted - no action` disposition.

A hunt report has no Recommendation Classification section - the phases themselves record the
disposition judgment, and the validator flags the section when it appears under
`Report Style: hunt`.

## Operator Verification Handoff

Under `source-only` this mandatory section lists every material claim the audit could not
resolve from source: the exact command or procedure, its pass criteria, and the finding or
rating it would confirm or close, per `report-closing.md`.

Under `executed-readonly` the section is replaced by the Executed Evidence Log plus any
remaining handoff entries for checks outside the commissioned set.

## Detail Levels

`Standard` and `Detailed` produce the full register. `Detailed` adds extended verification
methods and deeper journey analysis.

`Brief` keeps Document Information, Verdict, the top five findings, the phase summary, the
handoff or executed log, and the closing sections.

## Output Filename

The hunt filename stem is `HUNT`, or the language-specific stem from the matching
`translations/` file such as `POLOWANIE` for Polish.

A first hunt report defaults to the bare stem `HUNT.md`, with `HUNT-1.0.md` offered as the
revisioned alternative at delivery time.

When a previous hunt report exists, the filename carries the new revision, for example
`HUNT-1.1.md`, per `synthesis/report-comparison.md`.
