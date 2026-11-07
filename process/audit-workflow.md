# Audit Workflow

## Purpose

> **Scope:** End-to-end audit process from intake to validated report **Key items:** intake, scope,
> evidence gathering, per-category assessment, synthesis, validation

This file defines the order of operations for producing an audit.

Follow it for every full audit.

For a single-dimension request, run the same steps but limit the assessment phase to the
one requested category.

The `hunt` and `review` report styles apply the same phases with the section-order deltas defined in
`process/report-format/hunt-style.md` and `process/report-format/review-style.md`.

## Contents

| Section                 | Line | What it covers                   |
|-------------------------|------|----------------------------------|
| Step Overview           | 29   | Step Overview guidance           |
| Intake Checklist        | 56   | Intake Checklist guidance        |
| Handling Thin Input     | 81   | Handling Thin Input guidance     |
| Single-Dimension Audits | 94   | Single-Dimension Audits guidance |
| Re-Audit                | 109  | Re-Audit guidance                |
| Multi-Project Audits    | 176  | Multi-Project Audits guidance    |

## Step Overview

The workflow has eight phases.

Complete each phase before moving to the next.

Each phase lives in its own file under `process/audit-workflow/` - read the file for the phase the
audit is entering and keep it loaded while that phase runs.

| Phase                   | File                                            | Coverage                                       |
|-------------------------|-------------------------------------------------|------------------------------------------------|
| Intake                  | `process/audit-workflow/audit-intake.md`        | input reading, project census, audit mode      |
| Parameter Configuration | `process/audit-workflow/parameter-phase.md`     | acceptance gate, delivery, language, modes     |
| Scope Definition        | `process/audit-workflow/scope-definition.md`    | scope, domain profile, criteria planning       |
| Evidence Gathering      | `process/audit-workflow/evidence-gathering.md`  | sweeps, Verification Plan, evidence ledger     |
| Category Assessment     | `process/audit-workflow/category-assessment.md` | per-category checklists                        |
| Synthesis               | `process/audit-workflow/report-synthesis.md`    | section drafting, part assembly, review        |
| Validation              | `process/audit-workflow/report-validation.md`   | mechanical gates, evidence and decision checks |
| Final Adjustments       | `process/audit-workflow/final-adjustments.md`   | post-write confirmation, corrections, delivery |

`process/audit-workflow/regression-scenarios.md` holds the regression table exercised when
maintaining this skill.

Throughout the run the audit maintains `work/audit-model.json` - the canonical intermediate model
defined in `process/audit-model.md` - and every register, score, count,
and summary in the report renders from that model, never from prose composed during assembly.

## Intake Checklist

Use this checklist to confirm you understand the input before assessing.

| Question                                        | Record As                                            |
|-------------------------------------------------|------------------------------------------------------|
| What report style was resolved?                 | `audit` / `hunt` / `review`                          |
| What review scope was resolved?                 | `full` / `structure`, or `N/A` outside `review`      |
| What artifact type is this?                     | Prototype / Codebase / Production system / Proposal  |
| What is the source format?                      | Running / Inspected code / Description               |
| What components were provided?                  | List of components in scope                          |
| What was explicitly excluded?                   | Out-of-scope list                                    |
| What constraints did the user state?            | Constraints, or `Not specified`                      |
| What maturity does the user claim, if any?      | Claimed maturity, or none                            |
| What is the natural language of the request?    | Language code or name, or English (default)          |
| What language output was resolved?              | `single` / `pair`                                    |
| How many projects are in the directory?         | One / Multiple (list each with path and version)     |
| Is the audited root itself a project?           | `project` / `container`                              |
| Which held members were found?                  | List with provenance and fetch state                 |
| Which projects are included after the question? | Included list / excluded list with reasons           |
| What automation signal census resulted?         | `signals` / `external` / `none` per project          |
| What output subdirectory pattern exists?        | `version-numbered` / `date-named` / `mixed` / `none` |
| Was a previous report found, and which mode?    | none / re-audit / re-audit + changed params / fresh  |
| Was the run automated?                          | `automated` / `interactive`                          |

## Handling Thin Input

When the input is sparse, do not compensate by inferring.

An automated run asks no clarifying questions and produces the bounded report on what was supplied.

Produce the report anyway, with most categories marked `Unknown` or `Insufficient information`.

Add a short list of the specific artifacts that would raise confidence,
so the user can supply them and re-run the audit.

A thin-input audit is still useful: it shows exactly what is missing for a readiness decision.

## Single-Dimension Audits

When the user asks for only one dimension,
such as "review observability" or "check for AI-generated code" or "audit copyrights":

- Still load `principles/evaluation-rules.md` and `principles/output-style.md`.
- Load only the matching `assessment/` file.
- Produce only the matching report subsection plus any risks for that dimension.
- Note that the audit was scoped to a single dimension and is not a full readiness assessment.

A structure-scoped request resolves by wording:
"audit only the structure" is a single-dimension audit,
while "structure review" and "review the structure" route to the `review` style variant per
`process/report-format/structure-review.md`.

## Re-Audit

This section applies only after the user confirmed a re-audit in the audit-mode question of
`process/audit-workflow/audit-intake.md`.

When re-auditing after changes, keep the same categories, statuses vocabulary, scorecard
dimensions, and finding IDs.

Re-read the governing contract files before composing: `process/report-format.md` and its sub-files,
`synthesis/report-comparison.md`, and `process/report-parity.md`.

The baseline report encodes the format of the skill version that wrote it, not the current one.

Record what changed since the previous audit and which findings moved status,
so progress is comparable over time.

Build a prior-finding mapping table in the working notes before synthesis:
one row per prior `FND-XXX` recording its current disposition (`carried`, `closed`, `superseded`,
`dropped`), the evidence that justifies it, and the current identifier it maps to.

The Changes Since Previous Audit section is assembled from this table,
not improvised from memory of the baseline.

Verify remediation claims from current-tree evidence, never from changelogs, commit messages,
or issue trackers alone.

A finding marked `Closed` requires inspected evidence that the remediation landed.

A claimed fix without current evidence keeps `Open` and records the unverified claim.

Every evidence anchor is re-derived from the current tree.

When a previous report's anchor does not resolve and the tree is unchanged,
record the correct anchor and flag the prior citation as an evidence correction per
`synthesis/report-comparison.md`, never silently substitute it.

When the baseline's `Skill Version` row predates the running skill version,
enumerate the capability delta before writing: new mandatory sections, new finding or ledger fields,
new PAR rows, and new scorecard dimensions added between the two versions.

Apply the delta so the new report satisfies the current format,
and classify every structural addition as a capability change in the Changes Since Previous Audit
section and the Validation Protocol, not a product change.

When the scorecard dimension set differs between revisions, restate the mean formula:
an added or removed dimension changes the denominator,
and the resulting score movement is a capability change recorded outside the score-delta table per
`synthesis/report-comparison.md`.

Update the `Status` and `Verification` columns for findings that were closed
since the previous audit.

Build the Changes Since Previous Audit section using `synthesis/report-comparison.md`,
noting which `FND-XXX` findings changed from `Open` to `Closed`,
which `RSK-XXX` risks were mitigated, and which findings are new.

Do not overwrite the previous report file.

Write the new report to a revision-numbered file such as `AUDIT-1.1.md` and record the previous
report in the Document Information `Previous Report` row.

When `git diff` or the file inventory shows no source delta since the previous report,
the mandatory reading narrows: format, comparison, parity, style,
and evaluation files plus the synthesis files for sections the report carries.

Category assessment files load only for categories with new or changed findings.

## Multi-Project Audits

When the Project Identification step in `process/audit-workflow/audit-intake.md` detects more than
one project in the repository or directory,
the project-inclusion question confirms which ones are in scope,
and the audit runs independently for each included project.

**Per-project independence**

Each project is assessed as a self-contained subject.

Findings, risks, scorecard scores, and recommendations for one project must not reference or depend
on another project unless the user explicitly states that cross-project interactions are in scope.

Finding IDs use the standard pillar abbreviations and number globally across the whole report -
`FND` runs contiguously within each pillar, and `EVD`, `RSK`, `REC`, `TDR`,
and `PAR` each run as a single report-wide sequence.

No register resets per project: `FND-SEC-001` occurs once,
and the next SEC finding in any project continues the sequence.

Inside a project block, the short identifier is sufficient.

In shared sections, qualify every finding heading with the stable project identifier as a trailing
parenthetical, so the reader can locate the project within the report.
Register cells keep the bare identifier - `FND-SEC-001`, `RSK-001`,
`REC-001` number report-globally, so they are unambiguous on their own.

Never use ambiguous labels such as `both`, `either`, or `the projects` as an identifier.

See `process/report-format/multi-project.md` for the multi-project report structure.

**Workflow for multiple projects**

Run the assessment workflow (Scope Definition through Category Assessment) once per project,
in sequence or in parallel as the agent's capabilities allow - delegated evidence gathering follows
`process/parallel-execution.md`.

After all per-project assessments are complete,
run a single Synthesis phase that combines all projects into one report:

1. For each project, run Scope Definition, Evidence Gathering, and Category Assessment.
2. After all projects are assessed, build the combined report per
   `process/report-format/multi-project.md`.
3. Each project gets its own complete set of sections: Executive Summary,
   System Context (with the Technology Stack subsection), Health Dashboard, High-Level Observations,
   Auditing Methodology, Scoring Rubrics, Architectural Assessment, Solution Comparison,
   conditional sections, Strengths, Technical Findings, and Unified Risk Register.
4. Finding IDs, risk IDs, and recommendation IDs number globally across the whole report.
   Use the project identifier as a trailing parenthetical in the finding heading so the reader can
   navigate. For example, `### FND-ARC-001: Missing input validation (api-service)`.
5. The Document Information section appears once at the top of the report and lists
   all audited projects.
6. A Project Inventory table immediately after Document Information lists each project with its
   path, version, and a one-line description.
7. A condensed combined Executive Summary and, when a previous report exists,
   a combined Changes Since Previous Audit follow the Project Inventory,
   before the per-project blocks.
8. The combined Solution Comparison, Scope Exclusions, Known Limitations, Further Verification,
   Validation Protocol, consolidated Remediation Roadmap,
   and Reference Sources are shared sections at the end of the report, covering all projects.
   The combined Solution Comparison holds only cross-project trade-offs per
   `synthesis/solution-comparison.md`, and the consolidated Remediation Roadmap merges every
   project's recommendations, classification rows,
   and follow-up rows into one shared section immediately before Reference Sources per
   `process/report-format/multi-project.md`.

Then run the Validation phase once on the combined report per
`process/audit-workflow/report-validation.md`.

**Parameter Configuration for multiple projects**

The Parameter Configuration phase (`process/audit-workflow/parameter-phase.md`) runs once.

The chosen parameters (detail level, evaluation scale, language, delivery mode,
improvement suggestions, trade-off analysis) apply uniformly to all projects in the report.

Do not re-ask parameters per project.

**Output location for multiple projects**

The report is a single file.

Resolve the output directory once using the rules in the Delivery And Output File section of
`process/audit-workflow/parameter-phase.md`.

When version-numbered subdirectories exist under an `audit/` or `report/` documentation directory,
use the repository's primary version if one can be determined.

The primary version is the deployable service or application project's version.

When several projects qualify, prefer the project whose version sequence continues the existing
subdirectory names, and disclose the choice.

When date-named subdirectories exist under an `audit/` or `report/` documentation directory,
use the current date in ISO `YYYY-MM-DD` format.

When no single primary version applies and no date pattern exists,
use the root of the resolved directory without a subdirectory.
