# Audit Workflow

## Purpose

> **Scope:** End-to-end audit process from intake to validated report
> **Key items:** intake, scope, evidence gathering, per-category assessment, synthesis, validation

This file defines the order of operations for producing an audit. Follow it for every full audit.

For a single-dimension request, run the same steps but limit the assessment phase to the one
requested category.

## Contents

| Section                 | Line | What it covers                   |
|-------------------------|------|----------------------------------|
| Step Overview           | 24   | Step Overview guidance           |
| Intake Checklist        | 648  | Intake Checklist guidance        |
| Handling Thin Input     | 663  | Handling Thin Input guidance     |
| Single-Dimension Audits | 674  | Single-Dimension Audits guidance |
| Re-Audit                | 684  | Re-Audit guidance                |
| Multi-Project Audits    | 702  | Multi-Project Audits guidance    |

## Step Overview

The workflow has seven phases. Complete each phase before moving to the next.

**Intake**

Read everything the user supplied: description, code, configuration, diagrams, logs, prior reports.

Identify the artifact type: prototype, codebase under development, running production system, or
written proposal.

Note the source format. Findings from a description are weaker than findings from inspected code or
configuration.

Determine the natural language of the user's request. The report language must match the request
language unless the user explicitly states otherwise. When the request language is ambiguous or
cannot be determined, default to English.

**Development standards discovery**

During intake, look for project-internal development standards documents. These are documents that
prescribe how source code should be written for the project's technology stack: language version,
project structure, naming conventions, error handling, testing, formatting, dependency management,
and similar rules.

Search in these locations, in order:

- `docs/standard/` and any file inside it, such as `docs/standard/go-development.md`
- `docs/standards/`
- `docs/guidelines/`
- `STANDARDS.md` at the repository root
- Any file referenced from `README.md`, `AGENTS.md`, or `docs/GUIDELINES.md` as a development
  standard

Record whether standards documents exist, their paths, and which technology stack or software type
each one covers. This determines whether the Standards Conformance assessment applies.

When no standards documents are found, the Standards Conformance assessment is omitted and the
omission is noted in Scope Exclusions.

**Project Identification**

After reading the input, identify whether the repository or directory contains one project or
multiple projects.

A project is a self-contained unit with its own manifest, configuration, or entry point. Signals of
a project boundary include a package manifest (`package.json`, `Cargo.toml`, `composer.json`,
`go.mod`, `pom.xml`, `*.csproj`), a dedicated configuration directory, a `SKILL.md` file (for an
Agent Skill), or a clearly separated component with its own build and entry point.

When multiple project manifests or boundaries exist at the top level or in clearly separated
subdirectories, treat each as an independent project. Record the list of identified projects with
their paths and, if determinable, their version numbers.

When only one project is present, proceed with the standard single-project workflow.

When multiple projects are present, the audit runs independently for each project. Each project
receives its own complete assessment, findings, scorecard, and risk register within a single
combined report. See the Multi-Project Audits section below for the per-project workflow.

**Stack and subject classification**

For each identified project, detect the language and ecosystem from manifest and file signals:
`Cargo.toml` for Rust, `*.csproj` or `*.sln` for .NET, `go.mod` for Go, `package.json` for
Node, `pom.xml` or `build.gradle` for JVM stacks, `pyproject.toml` for Python, and so on.

Record the detected stacks and consult `references/stack-standards.md` for the canonical
references to apply during assessment and cite in the report.

Classify each project as a reusable library or package versus a deployable service or
application. Signals of a library subject include a package manifest with a published name and
version (`*.nuspec`, a `Cargo.toml` or `package.json` naming a published artifact), library
guidance in documentation, or consumption by other projects. This classification controls the
API Compatibility And Versioning Discipline conditional assessment.

**Rerunning an existing audit**

When the user asks to rerun, regenerate, or update an audit report, first check whether a
previous audit report exists. Search the location indicated in the request, the resolved output
directory and its versioned or dated subdirectories, the default locations (`docs/audit/`,
`docs/report/`, `docs/`, repository root), and the rest of the document structure, per
`synthesis/report-comparison.md`.

A previous report may be named `AUDIT.md`, `AUDIT-<version>.md`, or the language-specific
filename. When several exist, use the one with the highest version.

If a previous report is found, recover its detail level, scale, language, delivery mode, and
filename.

Reuse them unless the user asks to change them, then proceed to Scope Definition without repeating
answered questions.

Do not reuse old execution permissions, tool results, or readiness conclusions as current evidence.

Record any missing parameters using defaults and disclose them, rather than claiming they were
specified in the prior report.

The previous report is never overwritten. The new report is written to a new versioned file
and carries a Changes Since Previous Audit section, per `synthesis/report-comparison.md` and
`process/report-format.md`.

If no previous report is found and the conversation context contains no record of previously chosen
parameters, treat the request as a new audit and run the full Parameter Configuration phase.

**Parameter Configuration**

Before beginning the audit, ask the user whether to accept the default parameters or configure the
core parameters. Present the defaults in a compact summary.

Default parameters:

| Parameter               | Default                                                                            |
|-------------------------|------------------------------------------------------------------------------------|
| Report delivery         | File if `docs/audit/` or `docs/report/` exists, otherwise Inline (direct response) |
| Output filename         | `AUDIT.md` or language-specific, `AUDIT-<version>.md` after a previous report      |
| Report language         | Match the language of the user's request                                           |
| Detail level            | Detailed                                                                           |
| Evaluation scale        | 1-10                                                                               |
| Improvement suggestions | Include with priorities (P1-P4 roadmap)                                            |
| Trade-off analysis      | Standalone section + embedded into relevant findings                               |

The agent MUST ask the user and MUST NOT skip this step. The agent MUST wait for user response
before proceeding to Scope Definition.

Output filename is `AUDIT.md` for English reports, or the language-specific filename from the
matching `translation/` file. When a previous report exists, the filename carries the new
version, for example `AUDIT-1.1.md`, per `synthesis/report-comparison.md`. Used only when
delivery is File.

Improvement suggestions and trade-off analysis are advanced parameters. Apply their defaults
unless the user explicitly specifies another setting.

If the user accepts defaults or says "bypass", "defaults", or equivalent, proceed immediately to
Scope Definition using the values above.

If the user chooses to configure, ask only the unresolved core parameter prompts in this order:
delivery and output file, detail level, and evaluation scale.
At each prompt, offer a bypass option to accept the remaining defaults and proceed.

**Parameter prompts**

Present each prompt as a single question with clear options. After each answer, confirm the
choice and move to the next parameter.

Routine prompts are limited to delivery and output file, detail level, and evaluation scale.
Report language follows the request language unless the user explicitly specifies another
language. Advanced parameters use their defaults unless explicitly specified.

**Delivery and output file**

Before asking, resolve the base output directory using the following rules, applied in order
against the root of the repository or directory being audited:

1. If `docs/audit/` exists, use it as the base output directory.
2. Else if `docs/report/` exists, use it as the base output directory.
3. Else if `docs/` exists, use it as the base output directory.
4. Otherwise use the root of the audited repository or directory as the base output directory.

After selecting the base output directory, check whether it contains subdirectories that
indicate an existing structure. Inspect the subdirectory names to determine the pattern:

- **Version-numbered subdirectories**: If the base directory contains subdirectories named with
  version numbers, such as `1.0.1`, `0.5.0`, or `2.3.1`, and the project version can be
  determined from its manifest or configuration, then the resolved output directory becomes
  `<base>/<version>` using the current project version. For example, if `docs/audit/1.0.1`
  exists and the project version is `1.2.3`, the suggested directory is `docs/audit/1.2.3`.

- **Date-named subdirectories**: If the base directory contains subdirectories named with dates
  in ISO `YYYY-MM-DD` format, such as `2026-01-02` or `2026-04-06`, then the resolved output
  directory becomes `<base>/<current-date>` using the current date in the same ISO format. For
  example, if `docs/report/2026-04-06` exists and the current date is `2026-09-15`, the
  suggested directory is `docs/report/2026-09-15`.

- **No subdirectory pattern**: If the base directory has no version-numbered or date-named
  subdirectories, use the base directory directly as the resolved output directory. When the
  base is `docs/audit/` or `docs/report/`, offer the two structured alternatives in the delivery
  question.

The final output location must fit the existing directory structure. Do not mix patterns: if the
existing structure uses version numbers, use a version subdirectory, if it uses dates, use a
date subdirectory.

When multiple projects are present and each has a different version, resolve the output
directory once using the repository root. The single combined report is written to one location.
Do not create per-project subdirectories unless the user explicitly requests separate files per
project.

Resolve the filename before asking. Use `AUDIT.md` for English reports, or the language-specific
filename from the matching `translation/` file for non-English reports. When a previous report
exists, use the incremented filename defined in `synthesis/report-comparison.md`.

Ask: "How should the report be delivered?"

Present each applicable option as a concrete choice:

- `Inline` - return the full report as the direct response. This is the default when neither
  `docs/audit/` nor `docs/report/` exists.
- `File - <resolved-path>` - write the report to the resolved path. This is the default when
  `docs/audit/` or `docs/report/` exists.
- `File - <base>/<version>/<filename>` - file location using the project version. Offer this
  only when the base is `docs/audit/` or `docs/report/`, no existing subdirectory pattern is
  present, and the project version can be determined. For example,
  `docs/report/<version>/AUDIT.md`.
- `File - <base>/<current-date>/<filename>` - file location using the ISO `YYYY-MM-DD` current
  date. Offer this only when the base is `docs/audit/` or `docs/report/` and no existing
  subdirectory pattern is present. For example, `docs/report/<date>/AUDIT-2.0.md` when the next
  report version is `2.0`.
- `Custom report file` - ask the user to specify the location and filename.

For example, when `docs/report/` exists with no subdirectory pattern, the question can offer
`docs/report/AUDIT.md`, `docs/report/<version>/AUDIT.md`, and
`docs/report/<date>/AUDIT-2.0.md` alongside `Inline` and `Custom report file`.

Choosing a subdirectory option creates the subdirectory inside the base directory. Subsequent
audits then follow the established pattern per the rules above.

Always place the file inside the audited repository or directory. Do not write to an absolute
path outside it unless the user explicitly provides one.

If the user already named a file or stated an Inline preference in the original request, honor
it without asking again. Resolve the output directory using the rules above unless a full path
was given.

If the user stated only a File preference without a path, ask the same delivery question with
`Inline` omitted and the applicable file-location and `Custom report file` options retained.

**Previous report files**

When a previous audit report exists (for example, `AUDIT.md`, `AUDIT-1.0.md`, or a
language-specific audit file), do not overwrite it. Write the new report to a separate file
named `<base>-<version>.md`, for example `AUDIT-1.1.md`.

Read the `Version` field from the previous report's Document Information block, increment the
minor component up to 9 (for example, `1.0` becomes `1.1`, `1.9` becomes `2.0`, `9.9` becomes
`10.0`), and write the incremented version into the new report. When the previous report
records no version, treat it as `1.0` and assign `1.1`.

The previous report remains unchanged so that audit history stays comparable. Full rules live
in `synthesis/report-comparison.md`.

**Report language**

The default is the language of the user's request. When the request language is ambiguous, mixed,
or cannot be determined with confidence, default to English and apply the English document style
rules.

When the user explicitly specifies a different report language, apply it without a routine
follow-up question.

When the report language is not English, load the matching `translation/` file and apply every
translation, style rule, and encoding requirement defined there. The default filename changes to
the language-specific filename defined in the translation file, and the report must be written in
UTF-8 encoding with all language-specific diacritics preserved.

**Detail level**

Ask: "What level of detail should the report include?"

- **Detailed** (default) - full report plus extended remediation steps, additional verification
  methods, deeper architectural critique, and expanded impact analysis.
- **Standard** - full report with all fifteen baseline sections, subject to explicit parameter
  exclusions plus any conditional sections whose criteria are met, complete findings, risk
  register, scorecard, and remediation roadmap.
- **Brief** - Executive Summary, Health Dashboard (scorecard summary and risk heat map only),
  top risks only, and key recommendations. Detailed findings are summarized, not itemized.

**Evaluation scale**

Ask: "Which evaluation scale should be used for the scorecard?"

- **1-10** (default) - default scale with band definitions Poor (1-3), Average (4-6), Good
  (7-8), Excellent (9-10).
- **1-5** - compact numeric scale.
- **1-3** - minimal numeric scale.
- **5 stars** - uses the `1-5` rubric and displays filled and empty star bars, such as
  `★★★☆☆`.
- **3 stars** - uses the `1-3` rubric and displays filled and empty star bars, such as `★★☆`.

**Improvement suggestions**

Use **Include with priorities** by default. Do not ask this as a routine prompt.

Apply another option only when the user explicitly specifies it.

- **Include with priorities** (default) - full Actionable Remediation Roadmap with P1-P4 priority
  tiers, impact/effort/complexity matrix, and verification steps.
- **Brief only** - top 5 recommendations without the full matrix or verification steps.
- **None** - omit the Actionable Remediation Roadmap. Include only findings and risks.

**Trade-off analysis**

Use **Standalone and embedded** by default. Do not ask this as a routine prompt.

Apply another option only when the user explicitly specifies it.

- **Standalone and embedded** (default) - a summary section and reasoning in relevant findings.
- **Embed into findings** - reasoning only in relevant finding blocks.
- **Omit** - do not include trade-off reasoning.

**Bypass rule**

At any parameter prompt, if the user responds with "bypass", "skip", "defaults", or equivalent,
immediately accept all remaining defaults and proceed to Scope Definition.

**Scope Definition**

State what is in scope and what is not.

List the components, services, or files that were provided.

Record any constraints, goals, or target environment the user stated. Mark unstated constraints as
`NOT SPECIFIED`.

Determine the maturity level claim, if any, so it can be tested against evidence later.

**Audit Purpose And Verification Scope**

Record whether the decision is engineering improvement, production readiness, or technical due
diligence for acquisition, investment, or supplier review.

For due diligence, include continuity, ownership, operating cost, roadmap feasibility, and IP/data
obligations using the existing assessment categories rather than creating a separate people score.

If business artifacts are unavailable, retain those concerns as `UNKNOWN` and request specific
artifacts, do not present a source-only review as complete business due diligence.

The audit runs source-only. It never compiles, builds, or tests the project and never runs
linters, scanners, or generators against it, tool availability cannot be assumed and executing
untrusted code is out of scope.

Analysis rests on repository contents alone: source files, configuration, build scripts,
pipeline definitions, documentation, and committed artifacts such as coverage or scan reports.
Read-only inspection commands such as file listing, search, and version control history remain
in scope.

The audit never installs tools, uploads source, changes project policies, executes builds or
tests, or accesses live systems.

Record the scope as `source-only`. Documented or committed check results are `Reported`
evidence, not audit execution.

For readiness audits, identify required evidence before judging readiness: documented build and
test results, dependency manifests and lockfiles, committed scan reports, and operational
recovery documentation.

**Evidence Gathering**

For each relevant assessment category, collect concrete anchors: files, config keys, documented
commands, pipeline steps, documented procedures, committed check output, or direct quotes.

When development standards documents were found during intake, collect evidence of conformance and
divergence: for each rule in the standards, find representative source files that follow or violate
it. Also collect the external best practices, style guides, or conventions that the standards
reference or that apply to the stack, for the standards-quality evaluation in
`assessment/standards-conformance.md`.

For dependency analysis, derive the component inventory from manifests and lockfiles as text,
per `references/dependency-manifests.md`. The derived list records components, versions,
relationships, and scopes without running a package manager or an SBOM generator.

Respect `.gitignore` exclusions. Do not inspect files that are excluded by `.gitignore` patterns
(for example, `bin/`, `obj/`, `node_modules/`, `.env` files, or build artifacts). If a
`.gitignore` file is present, use it to filter the file list before analysis. If no `.gitignore` is
present, record the fact, but raise a finding only if relevant exclusions
are required or a concrete exposure is evidenced.

Do not yet form conclusions. Separate collection from judgement to avoid confirmation bias.

Where evidence is absent, record the gap explicitly with the appropriate missing-information token.

**Collected evidence coverage**

Every material observation collected during this pass must surface in the report. Git history
signals such as author concentration, commit cadence, and tag history produce at least a
one-line entry even when no adverse finding results: a Health Dashboard line, a finding, a
strength, or an explicit note. An item is dropped only with a recorded reason. Nothing
collected is silently unused.

**Verification Plan**

Build a small verification matrix per project before assessment.

Select the checks that would verify material claims from the project's documented commands and
the relevant assessment guides: build and test commands, lint and formatting rules, dependency
advisory scans, and license or SBOM checks.

The audit never executes them. For each selected check, record what the repository itself
shows: a documented command, a pipeline step, a committed report, or nothing at all.

Map each check to the ledger as `NOT RUN`, citing where the check is declared or where its
output is documented when such artifacts exist.

A documented or committed result is `Reported` evidence. It supports the claim it covers,
never "verified" status.

If a material claim has no documented result and cannot be resolved from source, record the
gap, its confidence impact, and the exact next step as a recommendation.

Do not mark the absence of tool execution as a product defect. A missing check is missing
evidence, not a missing feature.

**No execution**

The audit never compiles, builds, or tests the project and never runs linters, scanners, or
generators against it.

Read-only inspection of repository contents is still used: file listing, search, and version
control history.

Do not mutate the repository or its configuration, and do not treat inspection findings as
runtime-verified behavior.

**Evidence ledger**

Use globally unique evidence IDs within a report, with a project identifier on each row.

| Evidence ID | Project   | Check / Source      | Execution | Result        | Artifact |
|-------------|-----------|---------------------|-----------|---------------|----------|
| EVD-001     | <project> | <command or source> | <state>   | <observation> | <path>   |

The audit produces only two execution states: `NOT RUN` for a check that is documented or
selected but never executed, and `N/A` for a source observation.

They are separate from category statuses and from what the check discovered.

For a source observation rather than a check, use `N/A` for execution and identify its evidence
basis as Inspected, Reported, or Inferred as appropriate.

Below each row, record the documented command or the file and line range, revision and
dirty-tree state, date, declared tool or report version, and sanitized artifact path.

For committed scanner or coverage reports, record the producing tool, report timestamp or
revision, ruleset, exclusions, suppressions, and coverage.

For supplied or committed CI output, record the run or revision and label it `Reported`
evidence, noting any mismatch with the audited tree.

Preserve complete sanitized logs or machine-readable output when they exist in the repository,
or record a precise excerpt and explain why the original artifact is unavailable.

Tie findings to evidence IDs and explain what each item proves and does not prove.

**Category Assessment**

For each category, open the matching `assessment/` file and apply its checklist. For a full audit,
this includes the two additional categories `assessment/ai-generated-code.md` and
`assessment/copyright-review.md`.

Evaluate the inclusion criterion for each conditional assessment, listed in the Conditional Sections
table of `process/report-format.md`. When the criterion is met, open the matching conditional file
and apply it: `assessment/data-flow.md`, `assessment/design-patterns.md`,
`assessment/threat-model.md`, `assessment/api-contract.md`, `assessment/skill-definition.md`,
`assessment/standards-conformance.md`, and `assessment/api-compatibility.md`. When a criterion is
not met, omit that section and record the deliberate omission for Scope Exclusions. Do not force a
conditional section onto a subject it does not fit.

Assign a status (`PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`, `N/A`) per the rules in
`principles/evaluation-rules.md`.

Record evidence, concrete risks, and neutral notes for each category.

**Synthesis**

Build the unified risk register from the risks surfaced during assessment, using
`synthesis/risk-register.md`. Every risk must reference its source `FND-XXX`.

Build the project scorecard using `synthesis/project-scorecard.md`. Present the scoring rubric
before the scores. Wherever an overall score is stated, report the lowest-scoring applicable
dimension and its score alongside the mean, so a weak pillar is not hidden inside an average.

Draft the High-Level Observations section by selecting the top 5 most important findings from the
Detailed Technical Findings. Keep each observation brief, full detail lives in the finding blocks.

Draft the Strengths & What's Working section by identifying 5-8 evidenced positive baselines from
the codebase.

Surface trade-offs both as a standalone Trade-off Analysis section (using
`synthesis/trade-off-analysis.md`) and embedded into relevant architectural or design findings where
they directly explain a specific finding.

When structural debt distinct from risks was surfaced, build the Technical Debt Register using
`synthesis/debt-register.md`. Every debt item must trace to a finding or a cited direct observation.

Draft the actionable remediation roadmap using `synthesis/remediation-roadmap.md`. Every
recommendation must resolve a specific `FND-XXX`.

When the roadmap contains at least one P1 or P2 recommendation, build the Re-audit and Follow-up
Plan using `synthesis/re-audit-plan.md`, mapping those findings to verification owners and closure
evidence.

When a previous report was found during intake, build the Changes Since Previous Audit section
using `synthesis/report-comparison.md`, comparing findings, risks, scores, and category
statuses against the previous report.

Draft the Executive Summary last, after all findings, the risk register, and the roadmap are
final. It is the first section a reader sees but the last one synthesized, so it summarizes only
completed analysis. Add the Production Readiness Threshold paragraph to it at this stage, tying
conditions to specific `RSK-XXX` IDs.

**Validation**

Re-check every finding against `principles/evaluation-rules.md`.

Confirm no finding rests on an assumption, that every status has evidence or a gap token, and that
no language evaluates people.

Confirm every `FND-XXX` finding uses the correct pillar abbreviation and sequential numbering.

Confirm every `RSK-XXX` references its source `FND-XXX`.

Confirm every `REC-XXX` resolves a specific `FND-XXX`.

Confirm no plaintext secrets, passwords, or cryptographic keys appear in summaries, observations, or
risk descriptions.

Confirm High-Level Observations contains at most five observations in the template's table and
paragraph format, each anchored to a specific `FND-XXX`.

Confirm strengths fit the selected detail level and are evidenced, use fewer than the suggested
count when the input supports fewer, rather than padding the report.

Confirm the Trade-off Analysis section uses the standard table format and frames each trade-off
against a stated constraint.

Confirm every adverse finding in an initial audit has Remediation Status `Open`.

For re-audits, preserve IDs and update closure states only from the required evidence.

When a Changes Since Previous Audit section is present, confirm the previous report file was
left unchanged, the new filename carries the incremented version, every transition cites
current evidence, and no identifier from the previous report was reused for a different
finding.

Confirm each conditional section was evaluated: it is either present because its criterion is met,
or omitted with a deliberate one-line justification in Scope Exclusions. No conditional section may
be present-but-empty, and none relevant to the subject may be silently dropped. Changes Since
Previous Audit is the exception, its absence in a first audit needs no omission note.

When a Threat Model is present, confirm every unmitigated threat traces to a `FND-XXX` and a
`RSK-XXX`, and that no plaintext secret appears in a disclosure threat.

When an API Contract Conformance section is present, confirm each security gap maps to an OWASP API
Security Top 10 (2023) code where one applies.

When a Standards Conformance section is present, confirm every conformance judgement cites a
specific rule in the standards document and a specific file or pattern in the codebase, and that
every standards-quality judgement cites a named external best practice. Confirm the References
section lists every external source consulted during the standards-quality evaluation.

Confirm every material evidence item collected during Evidence Gathering surfaces in the report
as a finding, a risk, a dashboard element, or a strength, or is recorded as deliberately unused
with a reason. Git history signals such as author concentration, commit cadence, and tag
history must appear at least as the Team & Continuity line in the Health Dashboard.

Confirm every CWE-classified security finding names its equivalent static analyzer rule from
`references/cwe-analyzer-map.md` with its enablement evidence, or states that no direct rule
exists for the CWE in that stack. Confirm no finding implies an analyzer ran.

Confirm every place an overall score appears reports the lowest-scoring applicable dimension
and its score alongside the mean, per `synthesis/project-scorecard.md`.

When an API Compatibility And Versioning Discipline section is present, confirm it addresses
gate presence, versioning-scheme consistency, and breaking-change tracking, and that configured
tools are treated as intended checks, not executed ones.

When a Technical Debt Register is present, confirm every `TDR-XXX` traces to a `FND-XXX` or a cited
direct observation, and that no security risk is duplicated from the Unified Risk Register.

When a Re-audit and Follow-up Plan is present, confirm every row references a `FND-XXX` and that
owners or dates absent from the input are marked `NOT SPECIFIED` rather than invented.

Confirm the Auditing Methodology cites only the reference standards actually applied, including the
stack-specific canonical sources from `references/stack-standards.md` that were consulted, and the
Scope Exclusions state the OWASP category coverage.

Confirm the report follows `process/report-format.md` section by section.

Confirm the report follows the Formatting Rules in `process/report-format.md`: headings stop at
`###`, prose lines over 100 characters are wrapped, prose contains no semicolons, and every table
was formatted with an automated script so all `|` separators align vertically in plain text.

Confirm any temporary formatting scripts were removed from the audited repository.

**Evidence and decision checks**

- Reconcile all counts with their source and scope, including tests, findings, risks, and scores.
- Ensure every `CRITICAL` and `HIGH` finding records a counter-check and verification limit.
- Keep build, test, scanner, and runtime claims consistent with the evidence ledger.
- Confirm no build, test, or tool execution was performed or implied by the audit.
- Distinguish observed defects, unverified threats, and missing evidence in every summary.
- Check applicable security findings for CWE mapping and justified CVSS vectors or gap tokens.
- Recompute risk-matrix placements and any totals rather than estimating them in prose.
- Check that shared references use project-qualified IDs, never ambiguous labels such as "both".
- Require applicable readiness evidence and confirmed verification ownership before sign-off.
- Report unknown cost inputs, unmeasured SLOs, and missing business artifacts prominently.
- Preserve evidence limitations even in Brief reports.

**Regression Scenarios For Skill Changes**

When maintaining this skill, exercise these scenarios and check the expected behavior.

These are reasoning checks, not proof of improvement from an independent model benchmark.

| Scenario                                   | Expected Behavior                                    |
|--------------------------------------------|------------------------------------------------------|
| Changelog says tests pass                  | Reported only, readiness evidence incomplete         |
| Committed scan report lists an advisory    | Reported evidence, finding requires triage           |
| Documented build steps, no pipeline        | Inspected only, build outcome unknown                |
| Old crate, no advisory data                | Freshness concern, vulnerability status unknown      |
| Guarded panic or excluded module           | Verify reachability, do not invent failure           |
| Local CLI without hosted runtime           | Assess local safety, omit irrelevant hosted controls |
| Due diligence with no cost or support data | Retain unknowns, request artifacts                   |
| Two projects reuse FND-SEC-001             | Project-qualified shared references                  |
| Clean code with uniform tests              | No authorship inference, assess test behavior        |
| Security fix proposed but not run          | Keep verification pending, no closure claim          |
| Partial cost inputs or no telemetry        | No complete budget or numeric SLO claim              |
| Previous report at version 1.9 exists      | New `AUDIT-2.0.md`, previous kept, comparison added  |
| Previous report has no Version field       | Assume 1.0, new file `AUDIT-1.1.md`                  |
| Reusable library without an API gate       | API Compatibility section included, absence assessed |
| CWE-295 finding in C#                      | Finding names `CA5359` and its enablement state      |
| Git author data collected, no finding      | Team & Continuity dashboard line still present       |
| Mean 5.8 with Security at 4                | Floor named next to the mean                         |
| Lockfile present, no SBOM                  | Source-derived component inventory produced          |

## Intake Checklist

Use this checklist to confirm you understand the input before assessing.

| Question                                     | Record As                                           |
|----------------------------------------------|-----------------------------------------------------|
| What artifact type is this?                  | Prototype / Codebase / Production system / Proposal |
| What is the source format?                   | Running / Inspected code / Description              |
| What components were provided?               | List of components in scope                         |
| What was explicitly excluded?                | Out-of-scope list                                   |
| What constraints did the user state?         | Constraints, or `NOT SPECIFIED`                     |
| What maturity does the user claim, if any?   | Claimed maturity, or none                           |
| What is the natural language of the request? | Language code or name, or English (default)         |
| How many projects are in the directory?      | One / Multiple (list each with path and version)    |

## Handling Thin Input

When the input is sparse, do not compensate by inferring.

Produce the report anyway, with most categories marked `UNKNOWN` or `INSUFFICIENT INFORMATION`.

Add a short list of the specific artifacts that would raise confidence, so the user can supply them
and re-run the audit.

A thin-input audit is still useful: it shows exactly what is missing for a readiness decision.

## Single-Dimension Audits

When the user asks for only one dimension, such as "review observability" or "check for AI-generated
code" or "audit copyrights":

- Still load `principles/evaluation-rules.md` and `principles/output-style.md`.
- Load only the matching `assessment/` file.
- Produce only the matching report subsection plus any risks for that dimension.
- Note that the audit was scoped to a single dimension and is not a full readiness assessment.

## Re-Audit

When re-auditing after changes, keep the same categories, statuses vocabulary, scorecard dimensions,
and finding IDs.

Record what changed since the previous audit and which findings moved status, so progress is
comparable over time.

Update the Remediation Status column for findings that were closed since the previous audit.

Build the Changes Since Previous Audit section using `synthesis/report-comparison.md`, noting
which `FND-XXX` findings changed from `Open` to `Closed`, which `RSK-XXX` risks were mitigated,
and which findings are new.

Do not overwrite the previous report file. Write the new report to a versioned file such as
`AUDIT-1.1.md` and record the previous report in the Document Information `Previous Report`
field.

## Multi-Project Audits

When the Project Identification step in Intake detects more than one project in the repository or
directory, the audit runs independently for each project.

**Per-project independence**

Each project is assessed as a self-contained subject. Findings, risks, scorecard scores, and
recommendations for one project must not reference or depend on another project unless the user
explicitly states that cross-project interactions are in scope.

Finding IDs use the standard pillar abbreviations but are scoped per project. Each project's
findings start at `FND-XXX-001`. Risk IDs and recommendation IDs also reset per project. The project
name or identifier prefixes the finding block heading so the reader can locate the project within
the report. See `process/report-format.md` for the multi-project report structure.

**Workflow for multiple projects**

Run the full workflow (Scope Definition through Validation) once per project, in sequence or in
parallel as the agent's capabilities allow. After all per-project assessments are complete, run a
single Synthesis phase that combines all projects into one report:

1. For each project, run Scope Definition, Evidence Gathering, Category Assessment, and per-project
   Validation.
2. After all projects are assessed, build the combined report per `process/report-format.md`
   Multi-Project Report Structure.
3. Each project gets its own complete set of sections: Executive Summary, System Context (with the
   Technology Stack subsection), Health Dashboard, High-Level Observations, Auditing Methodology,
   Scoring Rubrics, Architectural Assessment, Trade-off Analysis, conditional sections, Strengths,
   Detailed Technical Findings, Unified Risk Register, and Actionable Remediation Roadmap.
4. Finding IDs, risk IDs, and recommendation IDs are scoped per project. Use the project identifier
   as a prefix in the finding heading so the reader can navigate. For example,
   `### FND-ARC-001: [api-service] Missing input validation`.
5. The Document Information section appears once at the top of the report and lists all audited
   projects.
6. A Project Inventory table immediately after Document Information lists each project with its
   path, version, and a one-line description.
7. Scope Exclusions and Re-audit and Follow-up Plan are shared sections at the end of the report,
   covering all projects.

**Parameter Configuration for multiple projects**

The Parameter Configuration phase runs once. The chosen parameters (detail level, evaluation scale,
language, delivery mode, improvement suggestions, trade-off analysis) apply uniformly to all
projects in the report. Do not re-ask parameters per project.

**Output location for multiple projects**

The report is a single file. Resolve the output directory once using the rules in the Delivery
and output file section. When version-numbered subdirectories exist under `docs/audit/` or
`docs/report/`, use the repository's primary version if one can be determined. When date-named
subdirectories exist under `docs/audit/` or `docs/report/`, use the current date in ISO
`YYYY-MM-DD` format. When no single primary version applies and no date pattern exists, use the
root of the resolved directory without a subdirectory.
