# Evidence Gathering

## Purpose

> **Scope:** The Evidence Gathering phase of the audit workflow - evidence anchors, sweeps,
> the Verification Plan, the no-execution rule,
> and the evidence ledger **Key items:** operation matrix, read-depth floor, Verification
> Plan, evidence ledger

This file is a phase of the audit workflow indexed by `process/audit-workflow.md`.

Follow it after Scope Definition.

On completion, proceed to `process/audit-workflow/category-assessment.md`.

## Contents

| Section                                           | Line | What it covers                                    |
|---------------------------------------------------|------|---------------------------------------------------|
| Evidence Gathering                                | 38   | Evidence Gathering                                |
| Organization Model                                | 52   | Organization Model                                |
| Cross-boundary Traces                             | 60   | Cross-boundary Traces                             |
| Per-entry-point Operation Matrix                  | 80   | Per-entry-point Operation Matrix                  |
| Advertised-capability Reality Check               | 95   | Advertised-capability Reality Check               |
| Toolchain Compatibility Check                     | 104  | Toolchain Compatibility Check                     |
| Correctness Defect Census                         | 112  | Correctness Defect Census                         |
| Lifecycle And Defaults Sweep                      | 120  | Lifecycle And Defaults Sweep                      |
| Collected Evidence Coverage                       | 193  | Collected Evidence Coverage                       |
| Read-depth Floor                                  | 209  | Read-depth Floor                                  |
| Check-execution Reconciliation                    | 220  | Check-execution Reconciliation                    |
| Shared Evidence Capture (`work/audit-model.json`) | 236  | Shared Evidence Capture (`work/audit-model.json`) |
| Verification Plan                                 | 261  | Verification Plan                                 |
| No Execution                                      | 304  | No Execution                                      |
| Evidence Ledger                                   | 316  | Evidence Ledger                                   |
| Claim And Evidence Traceability                   | 354  | Claim And Evidence Traceability                   |


## Evidence Gathering

For each relevant assessment category, collect concrete anchors: files, config keys,
documented commands, pipeline steps, documented procedures, committed check
output, or direct quotes.

When development standards documents were found during intake,
collect evidence of conformance and divergence: for each rule in the standards,
find representative source files that follow or violate it.

Also collect the external best practices, style guides,
or conventions that the standards reference or that apply to the stack,
for the standards-quality evaluation in `assessment/standards-conformance.md`.

## Organization Model

Build the area map and responsibility inventory per `references/organization-model.md` - the scan
census supplies the class mix, inspected content supplies declared and observed roles - before
judging structure or architecture.

A populated area with no identifiable responsibility is a finding input, not a skip.

## Cross-boundary Traces

Module-by-module reading is not sufficient evidence for capabilities that span components.

For every identifier or value that crosses a component boundary - document paths,
session or request identifiers, tokens and claims, configuration keys,
error shapes - build a producer/consumer trace: name each producer site,
the representation it emits, every consumer site, and the representation each expects.

A representation mismatch across a boundary is a finding.

Record the trace itself as evidence so conformance or absence claims cite traced
hops, not searched files.

For each advertised workflow named by the domain profile,
trace the declared path through its producer and consumer hops and record
conforming and failing hops.

Advertised workflows come from the documentation and the profile, not only from observed code.

## Per-entry-point Operation Matrix

Enumerate every externally reachable operation - routes, message consumers,
scheduled and background jobs, and public tool or command surfaces - from registration sites,
per the dispatch enumeration recipe in `references/topics/evidence-recipes.md`.

Record one operation row per entry point carrying four verdicts:
the authorization verdict (principal and scope required, or unauthenticated),
the input-to-sink trace for each caller-controlled value, the bounds verdict (size, rate,
and pagination limits and their out-of-range behavior),
and the error-contract verdict (status mapping and what the body exposes).

The matrix lands in the model's `evidence[]` and findings cite its rows - a finding that names one
endpoint without the matrix behind it rests on an anecdote, not a census.

## Advertised-capability Reality Check

For every capability the subject's documentation advertises,
confirm a non-trivial implementation exists:
read the code path and verify it produces real behavior rather than a placeholder,
stub, or uniform default.

A documented capability backed by a stub is a spec violation per `process/readiness-scoring.md`.

## Toolchain Compatibility Check

Compare declared toolchain requirements - manifest `rust-version` and edition,
builder and CI image versions, documented prerequisites - against the language features, APIs,
and dependency minimum requirements the code uses.

Record the comparison as evidence even when everything is compatible.

## Correctness Defect Census

On a code-bearing subject, run the defect-pattern and shipped-surface completeness censuses from
`assessment/correctness-review.md` against the in-scope source.

Candidates are confirmed by reading before they become findings,
and the census patterns and denominators are recorded beside the figures.

## Lifecycle And Defaults Sweep

For identity, session, token, key, and credential objects, trace issuance, expiry, revocation,
rotation, and behavior after identity removal or demotion.

For deployment and configuration, census the shipped defaults - ports, addresses, credentials,
debug endpoints, transport security, and file permissions - against least-privilege expectations.

For dependency analysis, derive the component inventory from manifests and lockfiles as text,
per `references/dependency-manifests.md`.

The derived list records components, versions, relationships,
and scopes without running a package manager or an SBOM generator.

Build the SBOM table for the report from that inventory per `references/sbom-schema.md` before
scoring Dependency Health, so the score has a structured artifact behind it.

Then run the license-classification pass from `references/license-compliance.md` over every SBOM
row, populating the License and Risk cells from inspected declarations only.

For delivery practice, compute the Git-derived proxies and contributor concentration per
`references/delivery-practice.md`: tag cadence, median commit-to-tag interval, top-author share,
and active-contributor count - agent-bot identities are excluded from the contributor counts and
recorded separately per the attribution census.

Fields the repository cannot supply stay `Not specified` with the reason recorded.

For recurring source and history censuses,
apply the canonical counting methods in `references/census-commands.md` and record the counting rule
beside each figure in the ledger, so a re-audit can reproduce the number.

Respect `.gitignore` exclusions for generated, vendored, and build output.

Do not inspect files that are excluded by `.gitignore` patterns when they hold generated or vendored
content (for example, `bin/`, `obj/`, `node_modules/`, or build artifacts).

If a `.gitignore` file is present, use it to filter the file list before analysis.

If no `.gitignore` is present, record the fact,
but raise a finding only if relevant exclusions are required or a concrete exposure is evidenced.

The exclusion targets generated and vendored content,
not project-owned configuration that the project keeps untracked.

When tracked source loads an untracked config or credential file (for example an `access.json` or
`.env` file referenced by auth code), inspect it for security posture.

Record such a file as working-tree evidence, never count it in the tracked file inventory,
and never reproduce secret values per `principles/evaluation-rules.md`.

Before asserting that a file is committed repository content,
verify its tracked status with `git ls-files` and its ignore status with `git check-ignore`,
per the Tracked Artifacts methods in `references/census-commands.md`.

A file present on disk is not committed content until `git ls-files` says so.

Honor read restrictions the project itself declares,
for example rule files that bar reading certain directories.

An untracked rules directory still governs.

Record every honored restriction in Scope Exclusions so the reader knows the coverage bound.

Do not yet form conclusions.

Separate collection from judgement to avoid confirmation bias.

When a search or pattern match is ambiguous - for example a dependency scope or a classification
matched in a different context than the project dependency - confirm the result by reading the
source file before recording it as evidence.

Where evidence is absent, record the gap explicitly with the appropriate missing-information token.

## Collected Evidence Coverage

Every material observation collected during this pass must surface in the report.

Git history signals such as author concentration, commit cadence,
and tag history produce at least a one-line entry even when no adverse finding results:
a Health Dashboard line, a finding, a strength, or an explicit note.

An item is dropped only with a recorded reason.

Nothing collected is silently unused.

Also record the read depth of each source file - full read, sampled,
or listed only - so the Auditing Methodology section can publish the read-depth table per
`process/report-format/methodology-scoring.md`.

## Read-depth Floor

A file that an activated probe, an applicable assessment check,
or a declared criteria-entry method touches must be read in full.

`Sampled` is permitted only on files no activated check reaches,
and `Listed` only for inventory rows whose contents no judgment needs.

Every non-full-read area named in the read-depth table carries a recorded justification,
and the Auditing Methodology section discloses it.

## Check-execution Reconciliation

Before leaving Evidence Gathering, reconcile three frozen denominators:
every probe activated by the domain profile,
every applicable check named in the loaded assessment files,
and every criteria entry's declared `method`.

Each must produce at least one `evidence[]` row,
or a recorded `NOT ASSESSED` or `inapplicable` entry in `audit-model.json` with its reason.

An unreconciled denominator - a probe or check that produced neither evidence nor a recorded skip -
is unfinished work, and the consistency gate in `process/report-parity.md` fails on it.

A check that ran and found nothing adverse is still evidence:
record the clean row so the reader can tell "checked" from "not looked at".

## Shared Evidence Capture (`work/audit-model.json`)

The canonical capture is `work/audit-model.json` per `process/audit-model.md`.

Its `evidence[]`, `inventory[]`, `findings[]`, `risks[]`,
and `recommendations[]` registers are populated during evidence collection and assessment,
and every report section renders from them.

Before generation, `scripts/check-model.py` verifies the model's referential integrity and
recomputes its scoring records. A failing model is repaired in the records, never rendered around,
per Model Quality Checks in `process/audit-model.md`.

When the session plans more than one report - for example an `audit` and a `hunt` over the same
snapshot - the same model registers serve every style: the audit renders its ledger, methodology,
and register sections from `evidence[]`, and the hunt renders the same rows plus the journey traces.

Style changes presentation, never the captured evidence.

Structure Review evidence rows are rendered by the `audit` and `review` styles - a `hunt` report
never consumes them.

A legacy `work/evidence.json` file - `evidence`, `read_depth`, `boundary_traces`, `journeys`,
and `notes` keys - maps onto the model's keys and may be kept beside it for multi-style sessions -
it never replaces the model or the read-depth and traceability rules in this file.

## Verification Plan

Build a small verification matrix per project before assessment.

Select the checks that would verify material claims from the project's documented commands and the
relevant assessment guides: build and test commands, lint and formatting rules,
dependency advisory scans, and license or SBOM checks.

Under `executed-readonly` or `executed-commands` the environment census from
`references/topics/execution-isolation.md` runs first and bounds which checks the matrix can select,
Under it the census also measures capacity - free disk against the expected build and test footprint
- so a check the host cannot complete is recorded before it starts, not after it dies.
and every executed `Fail` or `Error` result carries a triage class in the model.

Under `source-only` the audit never executes them.

The matrix becomes the Further Verification.

Under `executed-readonly` only the commissioned non-mutating analyzers run - builds, tests,
and the project itself still never execute,
and their results are `Executed` evidence in the Executed Evidence Log rather than `Not run` rows.

Under `executed-commands` the commissioned non-mutating commands run - tests and builds included -
and land in the same register, or in the Execution Register under `Report Style: review`,
each with its status token (`Pass` / `Fail` / `Error` / `Blocked` / `Skipped` / `Not run` / `N/A`).

For each selected check, record what the repository itself shows: a documented command,
a pipeline step, a committed report, or nothing at all.

Map each check to the ledger as `Not run`,
citing where the check is declared or where its output is documented when such artifacts exist.

A documented or committed result is `Reported` evidence.

It supports the claim it covers, never "verified" status.

If a material claim has no documented result and cannot be resolved from source, record the gap,
its confidence impact, and the exact next step as a recommendation.

Do not mark the absence of tool execution as a product defect.

A missing check is missing evidence, not a missing feature.

## No Execution

The audit never compiles, builds, or tests the project and never runs linters, scanners,
or generators against it, except the commissioned non-mutating analyzers under `executed-readonly`
and the commissioned non-mutating commands under `executed-commands`.

Read-only inspection of repository contents is still used: file listing, search,
and version control history.

Do not mutate the repository or its configuration,
and do not treat inspection findings as runtime-verified behavior.

## Evidence Ledger

Use globally unique evidence IDs within a report,
with a project identifier on each row in a multi-project report.

| Evidence | Source              | Result        | Type          | Artifact |
|----------|---------------------|---------------|---------------|----------|
| EVD-001  | <command or source> | <observation> | <obs/concern> | <path>   |

A `Project` column follows `Evidence` only in a multi-project report.

Every ledger row carries a `Type`: `Observation` for a fact another auditor could re-derive from the
same artifact, `Concern` for a risk judgment built on observations.

Most ledger rows are `Observation`.

The audit never executes checks, so there is no execution column:
a documented or selected check that was never executed writes `Not run` in `Result` with a note on
what the check would establish, and a source observation writes the observed result directly.

Result markers are separate from category statuses and from what the check discovered.

Identify each row's evidence basis as Inspected, Reported, or Inferred as appropriate.

Below each row, record the documented command or the file and line range,
revision and dirty-tree state, date, declared tool or report version, and sanitized artifact path.

For committed scanner or coverage reports, record the producing tool, report timestamp or revision,
ruleset, exclusions, suppressions, and coverage.

For supplied or committed CI output, record the run or revision and label it `Reported` evidence,
noting any mismatch with the audited tree.

Preserve complete sanitized logs or machine-readable output when they exist in the repository,
or record a precise excerpt and explain why the original artifact is unavailable.

Tie findings to evidence IDs and explain what each item proves and does not prove.

## Claim And Evidence Traceability

Treat every material claim in the Executive Summary, Health Dashboard, High-Level Observations,
scorecard, risk register, roadmap, and readiness decision as a claim that needs a finding
or evidence reference.

A claim reference must preserve the qualification of its source.

Use `Inspected`, `Reported`, or `Inferred` evidence labels and retain `Unknown`, `Not specified`,
or `Insufficient information` when the evidence cannot support a stronger statement.

Do not promote an inspected source observation into a runtime or production claim.

Do not promote a reported result from an older revision into current verification.

If a material claim has no direct reference, add one to the evidence ledger or remove the claim.

