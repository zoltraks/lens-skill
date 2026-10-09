# Review Report Style

## Purpose

> **Scope:** The `review` report genre - an execution-oriented technical assessment built
> around a run register of commissioned checks
> **Key items:** execution register, check statuses, evidence levels, verdict and gates,
> retest register, artifact manifest, structure review variant

This file defines the report produced when `report-style: review` is resolved during
Parameter Configuration in `process/audit-workflow.md`.

The `audit` style measures conformance against the governed contract and `hunt` measures
fitness for use. `review` answers a narrower question: what do the commissioned checks
actually show, and what do the findings drawn from them mean.

All three styles share one evidence base: the same finding schema, the same completeness
rules, and the same readiness gates.

Style changes presentation, never what must be found.

A review report is only as strong as what ran. Its distinguishing content is the Execution
Register - one row per commissioned check - and its honesty rules: an unexecuted check is
never a pass, a runner failure is never a product failure, and a model reproduction never
upgrades an application-level claim.

## Shared Contract

The following carry over unchanged from `process/report-format.md` and its spec files:

- Document Information per `report-opening.md`, including `Report Style: review` and the
  `Evidence Mode` row that decides which checks may run.
- Audit Type Coverage per `report-opening.md`.
- The finding block schema per `findings-registers.md`, with the same field vocabulary.
- The risk register schema per `synthesis/risk-register.md`, the roadmap priority and
  phasing rules per `synthesis/remediation-roadmap.md`, and scoring semantics per
  `process/readiness-scoring.md` wherever gates or confidence apply.
- Snapshot identity, read-depth table, evidence ledger, and claim traceability rules per
  `process/audit-workflow.md`.
- The Contradiction Register per `synthesis/report-triangulation.md` whenever an external
  report was found at intake.
- Scope Exclusions, Limitations and Unknowns, Validation Record, and References per
  `report-closing.md`.

Review adds one mandatory finding field everywhere the shared schema applies: `Evidence
level` per this file.

The review style includes the structure assessment from `assessment/structure-review.md`
in its evidence base - structure findings render in Domain Findings under the
Maintainability domain with `FND-STR-` identifiers. A `hunt` report never loads that
assessment.

When the resolved scope is structure-only, the report renders the Structure Review Variant
at the end of this file instead of the section order below.

## Evidence Mode

The style works under every evidence mode - the mode decides what may run, never what may
be claimed:

- `source-only` - nothing executes. Every register row is `NOT RUN` with the command that
  would run it, and findings rest on source evidence alone.
- `executed-readonly` - the commissioned non-mutating analyzers run (linters,
  typecheckers, format checkers, dependency advisory or policy scanners, contract
  diffing). The project itself is still never built, tested, or run.
- `executed-commands` - the explicitly commissioned non-mutating commands run, including
  test suites, builds, coverage runs, and isolated reproduction harnesses. The subject is
  still never deployed, mutated, or connected to live systems, and no tool is installed
  or upgraded for the audit unless the user commissioned it.

## Section Order

Produce these top-level sections in this order, with unnumbered headings:

- Document Information
- Audit Type Coverage
- Glossary *(when Descriptive mode is enabled)*
- Verdict
- System Context
- Check Plan And Methodology
- Execution Register
- Domain Findings
- Risk Register
- Improvement Plan
- Retest Register *(required when the Execution Register carries `FAIL`, `ERROR`, or
  `BLOCKED` rows)*
- Metrics Snapshot *(when the register produced metrics)*
- Artifact Manifest *(required under `executed-readonly` and `executed-commands`)*
- Contradiction Register *(conditional - external report found at intake)*
- Operator Verification Handoff *(source-only mode)* - under an executed mode the
  section lists only the checks outside the commissioned set
- Scope Exclusions
- Limitations and Unknowns
- Validation Record
- References
- `## Appendix <letter>: <title>` appendices *(optional - logs, coverage detail,
  reproduction harnesses, advisory dumps)*

## Verdict

The Verdict section replaces the Executive Summary and is the first content a reader sees.

It carries, in order:

1. A purpose statement - what the subject is, what was checked, at which snapshot.
2. A one-paragraph plain verdict: `Ready`, `Conditionally ready`, or `Not ready`, plus one
   sentence on what the verdict does not mean.
3. The domain ratings table per `hunt-style.md` (fixed domains, `Red`/`Amber`/`Green`/
   `Not assessed`, `FND-` basis for degraded ratings).
4. The hard readiness gates: every gate listed with `Met`, `Not met`, or `Not
   assessable`. State which permitted-use profile each gate belongs to - laboratory,
   controlled sharing, or production - when the report frames a staged rollout.
5. A top-five action list naming the first remediation steps with their finding IDs.
6. A strengths list of at most five evidenced positives.

A verdict never upgrades a `NOT RUN` or `BLOCKED` check into evidence of health, and a
gate that could not run is `Not assessable`, never `Met`.

## System Context

A condensed context block: purpose statement, technology stack with locked versions, the
component inventory table, and the runtime environment identity relevant to the register
(OS, toolchain versions, container base) when execution occurred.

## Check Plan And Methodology

States what was checked and under what authority:

- The check plan - the checks selected, the criterion each evaluates, and the evidence
  level each can reach.
- Execution permissions - exactly which commands the user commissioned, so the register
  cannot imply authority it never had.
- Deliberate omissions - checks considered and not commissioned.
- The read-depth table and evidence ledger per the shared rules.

## Execution Register

One row per check. The register is the report's spine - findings cite it, the retest
register replays it, and a later report can rerun it verbatim.

| Check | Command | Cwd | Tool & Version | Timestamp | Input revision | Exit status | Result | Interpretation | Artifact |
|-------|---------|-----|----------------|-----------|----------------|-------------|--------|----------------|----------|

Required columns are `Check`, `Command`, and `Result` - carry the remaining columns
whenever the mode permits them. A field the run did not record renders `NOT SPECIFIED`,
never an invented value.

`Result` takes exactly one token:

- `PASS` - the check ran and its criterion held.
- `FAIL` - the check ran and its criterion broke.
- `ERROR` - the runner or tool failed before producing a verdict. An `ERROR` row is an
  execution-environment failure, never a product failure.
- `BLOCKED` - the check could not start because a precondition was absent.
- `SKIPPED` - the check was deliberately omitted, and the Interpretation states why.
- `NOT RUN` - the check was never executed. `NOT RUN` contributes nothing toward a pass.
- `N/A` - the check does not apply to this subject.

Every non-`PASS` row carries its reason or outcome meaning in `Interpretation`.
Every row under an executed mode names its retained output in `Artifact` or records
`None retained`.

Scope labels stay distinct: a typecheck pass is not a test pass, a coverage figure is not
a correctness claim, a scanner count is not a vulnerability count, and advisory presence
in a manifest is not reachability.

## Domain Findings

One findings register organized under `###` domain headings (the domain ratings set),
each finding keeping its shared `FND-<pillar>-NNN` identifier and full block schema.

The section opens with a summary table carrying the shared columns (`Finding`, `Result`,
`Status`, `Change`, `Verification`, plus `Project` when multi-project), and the validator
reconciles its row count against the `### FND-` blocks.

Review adds a mandatory field to every finding block:

- `* **Evidence level:**` - the strongest level the cited evidence reaches:
  `Source` (read in code or config), `Model` (an isolated reproduction or harness),
  `App` (the real application running locally), `Deployed` (a deployed environment),
  or `Unknown` when the level cannot be established.

A `Model` reproduction demonstrates a mechanism - it never upgrades application-wide
reachability claims, which stay `Source`-derived until exercised against the real routes.
`Evidence level` is independent of `Confidence` - a claim can be confidently inferred
from source without any execution.

Structure findings render under the `### Maintainability` domain heading with
`FND-STR-` identifiers.

## Risk Register

The shared schema applies unchanged.

## Improvement Plan

Recommendations grouped into phases ordered by dependency, in the manner of the hunt
Remediation Phases: each phase lists its recommendations, acceptance criteria,
verification steps, and the findings each closes.

Every finding maps to a phase or to an explicit `Accepted - no action` disposition.
`Deferred` and `Unresolved` dispositions are permitted with their blocking condition
named.

A review report has no Recommendation Classification section - the plan records the
disposition judgment, and the validator flags the section when it appears under
`Report Style: review`.

## Retest Register

Required when the Execution Register carries any `FAIL`, `ERROR`, or `BLOCKED` row -
one row per failed check:

| Check | Register result | Blocking condition | Retest command | Closes |
|-------|-----------------|--------------------|----------------|--------|

`Closes` names the finding or gate the retest resolves.

## Metrics Snapshot

Present only when the register produced metrics. State each figure with its scope:
`backend tests: 241 passed` is a different claim from `tests pass`, and `42% statement
coverage` is a different claim from `42% coverage`.

## Artifact Manifest

Required under `executed-readonly` and `executed-commands`, omitted otherwise with the
omission noted in Scope Exclusions.

One row per retained output - logs, coverage reports, audit JSON, reproduction PoCs,
advisory dumps:

| Artifact | Check | Location / Digest | Notes |
|----------|-------|-------------------|-------|

When nothing was retained, state `None retained` explicitly.

## Detail Levels

`Standard` and `Detailed` produce the full register and findings. `Detailed` adds
extended verification methods and appendix material.

`Brief` keeps Document Information, Verdict, the Execution Register summary, the top
findings, the plan summary, the handoff or manifest, and the closing sections.

## Output Filename

The review filename stem is `REVIEW`, or the language-specific stem from the matching
`translations/` file such as `PRZEGLĄD` for Polish.

A first review report defaults to the bare stem `REVIEW.md`, with `REVIEW-1.0.md` offered
as the revisioned alternative at delivery time.

When a previous review report exists, the filename carries the new revision, for example
`REVIEW-1.1.md`, per `synthesis/report-comparison.md`.

## Structure Review Variant

When intake resolves a structure-only scope - wording such as "make a structure review"
or "review the project structure" - the report still uses the `REVIEW` filename family and
`Report Style: review`, but renders the bespoke contract defined in
`process/report-format/structure-review.md`: Document Information carrying
`Review Scope: Structure`, then Project Context, Structural Overview, Findings, Positive
Practices, Recommendations, Prioritization, and Limitations and Assumptions.

The variant baselines only against prior `REVIEW`-family files carrying the same
`Review Scope: Structure` row, per `synthesis/report-comparison.md`.
