# Hunt Report Style

## Purpose

> **Scope:** The `hunt` report genre - a version-specific defect and health register built
> around one canonical record per finding **Key items:** report overview, health assessment,
> canonical findings, finding lifecycle and dispositions, remediation plan, previous findings

This file defines the report produced when `report-style: hunt` is resolved during Parameter
Configuration in `process/audit-workflow/parameter-phase.md`.

The pre-redesign layout - verdict block, domain ratings, journey traces, and remediation phases -
is preserved as the `hunt (legacy)` variant in `process/report-format/hunt-legacy.md`,
selected by an explicit `hunt (legacy)` request or by a recovered previous report carrying
`Report Style: Hunt (legacy)`.

## Contents

| Section              | Line | What it covers                                    |
|----------------------|------|---------------------------------------------------|
| Shared Contract      | 47   | Carried-over rules from the shared format specs   |
| Section Order        | 66   | Required and conditional section sequence         |
| Document Information      | 101   | Metadata table and verdict block                  |
| Contents             | 120  | Generated report navigation                       |
| Health Assessment    | 128  | Readiness and severity distribution               |
| Findings             | 167  | Canonical defect register                         |
| Remediation Plan     | 250  | Prioritized action plan                           |
| Previous Findings    | 267  | Delta against the previous report                 |
| Scope and Limitations| 285  | Boundaries and exclusions                         |
| Detail Levels        | 293  | Compact, standard, and detailed forms             |
| Output Filename      | 301  | Naming and stems                                  |

A report under this contract records `Report Style: Hunt` in its metadata table,
with no variant suffix.

The `audit` style measures conformance against the governed contract.
`hunt` measures fitness for use and answers: how bad is the project at this revision,
which problems remain, which are intentionally tolerated, and what happens next.

All styles share one evidence base: the same evidence gathering, the same completeness rules,
and the same readiness gates.

Style changes presentation, never what must be found.

Read the sections the task needs - grep the `## ` headings for the section map.

## Shared Contract

The following carry over unchanged from `process/report-format.md` and its spec files:

- The metadata table rows per `report-opening.md` - they live inside `## Document Information`
  instead of a separate Document Information section.
- Snapshot identity, read-depth, and claim traceability rules per
  `process/audit-workflow/audit-intake.md` and `process/audit-workflow/evidence-gathering.md`.
- The Contradiction Register per `synthesis/report-triangulation.md` whenever an external report
  was found at intake.
- Identifier, register-link, and formatting rules per `process/report-format.md` and
  `process/report-contract.md`.

The defect report replaces the shared finding block schema with its own canonical record -
the Finding Record below is authoritative for this style.

Hunt never loads the structure assessment in `assessment/structure-review.md`,
and `FND-STR-` findings never appear in a hunt report of either variant.

## Section Order

Produce these top-level sections in this order, with unnumbered headings:

- Document Information
- Contents
- Health Assessment
- Findings
- Remediation Plan
- Previous Findings
- Scope and Limitations

Conditional `##` sections that may follow Scope and Limitations or sit inside it:

- Contradiction Register *(external report found at intake)*
- Journey Traces *(optional diagnostic appendix - the legacy trace contract applies)*
- Methodology And Evidence *(optional companion appendix: read-depth table, evidence ledger)*
- Executed Evidence *(required under `executed-readonly` and `executed-commands`, omitted under
  `source-only`)*
- Artifact Manifest *(optional under executed modes)*
- Reference Sources *(optional - external sources may instead be cited inside finding Evidence)*
- Glossary *(optional - always the last `##` section when rendered)*
- `## Appendix <letter>: <title>` *(optional - logs, census output, journey detail)*

A `Glossary` is a brief reader aid, not the legacy index - one table row per term the report
actually uses that a reader would not already know.
Well-known abbreviations (API, CI, CVE, SQL, TLS, UI) are omitted, and a report that uses no
unfamiliar terms omits the section entirely.

Sections the defect report never carries: Document Information, Audit Coverage, Glossary Index,
Executive Summary, Verdict, Domain Ratings, System Context, Domain Findings, Risk Register,
Remediation Phases, Recommendation Classification, Improvement Plan, Retest,
Scope Exclusions, Known Limitations, Further Verification, Validation Protocol,
and any `RSK-`, `REC-`, or `TDR-` register block.

## Document Information

Opens the report: the metadata table, then a one-paragraph executive summary.

The metadata table keeps the empty-header two-column form and row vocabulary of
`report-opening.md`, with these required rows: `Report Revision`, `Report Date`,
`Report Style` (`Hunt`), `Detail Level`, `Language`, `Evidence Mode`, `Subject Revision`,
`Skill Version`, `Time taken`.

Optional rows: `Assessment Scope` (components covered), `Subject Version` (release or tag),
`Project`, `Previous Report`, `Translations`, `Audit Purpose`, `Target Environment`,
`Verification Scope`, `Evaluation Scale`, `Projects`, `Dirty-Tree State`.

The executive summary covers, in under a minute of reading: the overall condition,
release readiness, the most important defects, whether known risks are accepted or deferred,
and the recommended immediate actions.

It never carries a technology-stack inventory, glossary, or audit-engagement classification.

## Contents

Follows Document Information - the defect report is long enough that navigation earns its place.

The Contents section carries grouped `- [Section](#anchor)` links in the audit report's style:
scope and context entries first, then findings and plan, then evidence and reference material.
Rendered `##` sections appear in order - the Glossary links last when present.

## Health Assessment

Answers "how bad is it" with two independent views - defect severity and project readiness.

State the readiness as a word-led line carrying exactly one bolded token -
`Readiness: **Blocked**` - one of:

- `Ready` - no known unresolved issue prevents the intended use.
- `At Risk` - significant unresolved problems exist, but deployment may be possible under
  explicit conditions.
- `Blocked` - cannot safely proceed with the intended release or deployment.
- `Not Assessed` - insufficient evidence to establish readiness.

Readiness considers mandatory release gates independently of the defect count:
ten `Low` defects do not outweigh one open `High` security defect,
and an open `P0` action always means `Blocked`.

Follow with the severity/class distribution table - one row per severity,
counts reconciling against the finding blocks:

| Severity | Defect | Improvement | Hypothesis | Observation |
|----------|--------|-------------|------------|-------------|

Then the disposition table - one row per disposition in use,
counts reconciling against the finding blocks:

| Disposition | Findings |
|-------------|----------|

When the report frames staged use, add the readiness-gates table
(`Gate | Result | Basis`) with `Met`, `Not met`, or `Not assessable` rows.

State the figures the table implies in prose: confirmed unresolved defects, unverified
hypotheses, accepted risks, deferred findings, release blockers, and findings resolved since
the previous assessment.

The verdict-support sentence names the outcome plainly -
`The production use profile cannot be confirmed while defects and security vulnerabilities exist.`

## Findings

One canonical record per finding - no separate risk or recommendation register exists.

The section opens with a summary table carrying `Finding`, `Severity`, `Class`, `Status`,
`Disposition`, `Priority`, and `Title` columns (plus `Project` when multi-project),
then organizes the `### FND-` blocks under `###` domain headings drawn from the hunt domain set.

Every domain heading opens with a one-line count-and-severity summary of its findings -
`Seven findings - one Medium, six Low.` - so no `###` heading ever stands empty.

Domains follow the shared set: Correctness, Security, Reliability, Performance, Dependencies,
Deployment, Testability, Documentation, Maintainability, Provenance,
plus any domain the domain profile activates.

Every `### FND-<pillar>-NNN` block opens with a description paragraph, then the field list:

```markdown
### FND-SEC-001: Custom provider headers expose secrets in API responses

<what is wrong, where it lives, and why it is a defect>

- **Component:** Backend
- **Class:** Defect
- **Severity:** High
- **Status:** Open
- **Disposition:** Planned
- **Priority:** P1
- **Confidence:** High
- **Impact:** Exposure of credentials to users who can read connection configuration.
- **Evidence:** `backend/src/modules/admin/connections/connection-schemas.ts` - masking covers
  standard fields, not arbitrary custom headers.
- **Recommendation:** Extend secret masking to custom headers and add regression tests.
- **Verification:** Sensitive headers render masked while provider use keeps the raw values.
```

Required fields, in order: `Component`, `Class`, `Severity`, `Status`, `Disposition`, `Priority`,
`Confidence`, `Impact`, `Evidence`, `Recommendation`, `Verification`.

`Verification` carries the closure criteria - the check that establishes resolution,
the role `Method` plays in the shared schema.

Field vocabularies:

- `Class`: `Defect` (a confirmed problem), `Improvement` (an opportunity that is not a defect),
  `Hypothesis` (suspected, not yet confirmed), `Observation` (informational note).
- `Severity`: `Critical`, `High`, `Medium`, `Low`, `Informational` - judged by the consequence
  if the defect manifests, never by code appearance.
- `Status` (technical lifecycle): `Open`, `In Progress`, `Resolved`, `Verified`, `Reopened`,
  `Rejected` (established invalid or a false positive).
- `Disposition` (management decision): `Planned`, `Deferred`, `Accepted Risk`, `Won't Fix`,
  `Out of Scope`, `None`.
- `Priority` (remediation urgency): `P0` immediate blocker, `P1` urgent, `P2` normal, `P3` low.
- `Confidence`: `High`, `Medium`, `Low`.

Status and Disposition answer different questions - `Open + Deferred` is a known defect
intentionally postponed, `Resolved` is a fix awaiting verification, and only `Verified`
closes the lifecycle.

A `Deferred` or `Accepted Risk` finding stays unresolved and stays visible in every count.
A `Rejected` finding keeps its record but leaves the unresolved set.

Optional fields keep the shared schema names and rules - `Targets`, `Basis`, `Criteria`,
`Method`, `Mitigation`, `Scenario`, `Breaking`, `Level`, `Provenance`, `Security`,
`Exploitability`, `Type` - and render only when they carry information,
for example `Security` on a vulnerability finding.

### Decision Fields

When `Disposition` is `Deferred`, `Accepted Risk`, or `Won't Fix`, the block additionally
requires five fields:

- `Reason` - why the defect is not being repaired.
- `Owner` - who approved the decision, or `Not recorded` when no owner is documented.
- `Decided` - the decision date, or `Not recorded`.
- `Review` - the review or expiration date, or `Not recorded`.
- `Conditions` - what would trigger earlier remediation.

`Out of Scope` requires `Reason` only.

A deferred or accepted finding never disappears from the unresolved count,
and an expired decision is reconsidered at the next assessment.

## Remediation Plan

A prioritized action list replacing phases and recommendation registers - no `REC-` identifiers:

| Priority | Finding | Action | Depends | Verification |
|----------|---------|--------|---------|--------------|

Rows order `P0` first, each `Finding` cell cites a defined `FND-`,
`Depends` names blocking findings or `None`, and `Verification` repeats the finding's
closure check in one line.

Every unresolved finding with `Disposition: Planned` appears exactly once.
`Deferred`, `Accepted Risk`, `Won't Fix`, and `Out of Scope` findings need no row -
their disposition and decision fields are the record.

Group actions under `### <phase>` headings only when implementation dependencies justify them.

## Previous Findings

On a re-hunt, a compact change table - one row per prior or newly-tracked finding:

| Finding | Change | Notes |
|---------|--------|-------|

`Change` vocabulary: `New`, `Still Open`, `Resolved`, `Reopened`, `Deferred`, `Accepted`,
`Reclassified`, `Retired`.

Identifiers stay stable across revisions - a finding keeps its `FND-<pillar>-NNN` for life,
and an identifier is never reassigned to a different problem.

A `Resolved` or `Retired` row needs no `### FND-` block - the identifier cites in a code span
when it has no definition in this report, per `process/report-format.md`.

On a first hunt the section states that this is the first assessment.

## Scope and Limitations

One concise closing section covering: assessed components, excluded areas,
the verification environment, important unexecuted checks with the finding or rating each
would settle, evidence limitations, and the unverified hypotheses the report carries.

An environment-related check failure is a limitation, never a product defect.

## Detail Levels

`Standard` and `Detailed` produce the full register and every required section.
`Detailed` adds deeper evidence notes and optional companion appendices.

`Brief` keeps all six sections but carries only the summary table and the top five
priority findings as blocks, with remaining findings listed by identifier in the table.

## Output Filename

The hunt filename stem is `HUNT`, or the language-specific stem from the matching `translations/`
file such as `USTERKI` for Polish.

A first hunt report defaults to the bare stem `HUNT.md`,
with `HUNT-1.0.md` offered as the revisioned alternative at delivery time.

When a previous hunt report exists, the filename carries the new revision,
for example `HUNT-1.1.md`, per `synthesis/report-comparison.md`.
