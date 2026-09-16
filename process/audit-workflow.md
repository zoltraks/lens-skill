# Audit Workflow

## Purpose

> **Scope:** End-to-end audit process from intake to validated report
> **Key items:** intake, scope, evidence gathering, per-category assessment, synthesis, validation

This file defines the order of operations for producing an audit. Follow it for every full audit.

For a single-dimension request, run the same steps but limit the assessment phase to the one requested category.

## Contents

| Section                 | Line | What it covers                   |
|-------------------------|------|----------------------------------|
| Step Overview           | 23   | Step Overview guidance           |
| Intake Checklist        | 431  | Intake Checklist guidance        |
| Handling Thin Input     | 446  | Handling Thin Input guidance     |
| Single-Dimension Audits | 456  | Single-Dimension Audits guidance |
| Re-Audit                | 465  | Re-Audit guidance                |
| Multi-Project Audits    | 473  | Multi-Project Audits guidance    |

## Step Overview

The workflow has seven phases. Complete each phase before moving to the next.

**Intake**

Read everything the user supplied: description, code, configuration, diagrams, logs, prior reports.

Identify the artifact type: prototype, codebase under development, running production system, or written proposal.

Note the source format. Findings from a description are weaker than findings from inspected code or configuration.

Determine the natural language of the user's request. The report language must match the request language unless the user explicitly states otherwise. When the request language is ambiguous or cannot be determined, default to English.

**Development standards discovery**

During intake, look for project-internal development standards documents. These are documents that prescribe how source code should be written for the project's technology stack: language version, project structure, naming conventions, error handling, testing, formatting, dependency management, and similar rules.

Search in these locations, in order:

- `docs/standard/` and any file inside it, such as `docs/standard/go-development.md`
- `docs/standards/`
- `docs/guidelines/`
- `STANDARDS.md` at the repository root
- Any file referenced from `README.md`, `AGENTS.md`, or `docs/GUIDELINES.md` as a development standard

Record whether standards documents exist, their paths, and which technology stack or software type each one covers. This determines whether the Standards Conformance assessment applies.

When no standards documents are found, the Standards Conformance assessment is omitted and the omission is noted in Scope Exclusions.

**Project Identification**

After reading the input, identify whether the repository or directory contains one project or multiple projects.

A project is a self-contained unit with its own manifest, configuration, or entry point. Signals of a project boundary include a package manifest (`package.json`, `Cargo.toml`, `composer.json`, `go.mod`, `pom.xml`, `*.csproj`), a dedicated configuration directory, a `SKILL.md` file (for an Agent Skill), or a clearly separated component with its own build and entry point.

When multiple project manifests or boundaries exist at the top level or in clearly separated subdirectories, treat each as an independent project. Record the list of identified projects with their paths and, if determinable, their version numbers.

When only one project is present, proceed with the standard single-project workflow.

When multiple projects are present, the audit runs independently for each project. Each project receives its own complete assessment, findings, scorecard, and risk register within a single combined report. See the Multi-Project Audits section below for the per-project workflow.

**Rerunning an existing audit**

When the user asks to rerun, regenerate, or update an audit report, first check whether a previous audit file exists in the target location (for example, `AUDIT.md` or a language-specific filename in the project directory).

If a previous report is found, recover its detail level, scale, language, delivery mode, and
filename.

Reuse them unless the user asks to change them, then proceed to Scope Definition without repeating
answered questions.

Do not reuse old execution permissions, tool results, or readiness conclusions as current evidence.

Record any missing parameters using defaults and disclose them, rather than claiming they were
specified in the prior report.

If no previous report is found and the conversation context contains no record of previously chosen parameters, treat the request as a new audit and run the full Parameter Configuration phase.

**Parameter Configuration**

Before beginning the audit, ask the user whether to accept the default parameters or configure them. Present the defaults in a compact summary.

Default parameters:

| Parameter               | Default                                                                            |
|-------------------------|------------------------------------------------------------------------------------|
| Report delivery         | File if `docs/audit/` or `docs/report/` exists, otherwise Inline (direct response) |
| Output filename         | `AUDIT.md` for English reports, or the language-specific filename                  |
| Report language         | Match the language of the user's request                                           |
| Detail level            | Standard                                                                           |
| Evaluation scale        | 1-10                                                                               |
| Improvement suggestions | Include with priorities (P1-P4 roadmap)                                            |
| Trade-off analysis      | Standalone section + embedded into relevant findings                               |

The agent MUST ask the user and MUST NOT skip this step. The agent MUST wait for user response before proceeding to Scope Definition.

Output filename is `AUDIT.md` for English reports, or the language-specific filename from the matching `translation/` file. Used only when delivery is File.

If the user accepts defaults or says "bypass", "defaults", or equivalent, proceed immediately to Scope Definition using the values above.

If the user chooses to configure, walk through the parameters one at a time. At each prompt, offer a bypass option to accept the remaining defaults and proceed.

**Parameter prompts**

Present each prompt as a single question with clear options. After each answer, confirm the choice and move to the next parameter.

**Report delivery**

The default delivery mode depends on the audited repository or directory structure:

- If `docs/audit/` or `docs/report/` exists, the default is **File** - write the report to a file inside the audited repository or directory.
- If neither `docs/audit/` nor `docs/report/` exists, the default is **Inline** - return the full report as the direct response.

Ask: "How should the report be delivered?"

- File (default when `docs/audit/` or `docs/report/` exists) - write the report to a file inside the audited repository or directory.
- Inline (default when neither `docs/audit/` nor `docs/report/` exists) - return the full report as the direct response.

When File mode is selected (either by default or by user choice), resolve the output location using the following rules, applied in order against the root of the repository or directory being audited:

1. If `docs/audit/` exists, use it as the base output directory.
2. Else if `docs/report/` exists, use it as the base output directory.
3. Else if `docs/` exists, use it as the base output directory.
4. Otherwise use the root of the audited repository or directory as the base output directory.

After selecting the base output directory, check whether it contains subdirectories that indicate an existing structure. Inspect the subdirectory names to determine the pattern:

- **Version-numbered subdirectories**: If the base directory contains subdirectories named with version numbers (for example, `1.0.1`, `0.5.0`, `2.3.1`) and the project version can be determined from its manifest or configuration, then the default output directory becomes `<base>/<version>` using the current project version. For example, if `docs/audit/1.0.1` exists and the project version is `1.2.3`, the suggested directory is `docs/audit/1.2.3`.

- **Date-named subdirectories**: If the base directory contains subdirectories named with dates in ISO `YYYY-MM-DD` format (for example, `2026-01-02`, `2026-04-06`), then the default output directory becomes `<base>/<current-date>` using the current date in the same ISO format. For example, if `docs/report/2026-04-06` exists and the current date is `2026-09-15`, the suggested directory is `docs/report/2026-09-15`.

- **No subdirectories**: If the base directory has no subdirectories, use the base directory directly as the output directory.

The final output location must fit the existing directory structure. Do not mix patterns: if the existing structure uses version numbers, use a version subdirectory, if it uses dates, use a date subdirectory.

When multiple projects are present and each has a different version, resolve the output directory once using the repository root. The single combined report is written to one location. Do not create per-project subdirectories unless the user explicitly requests separate files per project.

Present the resolved default location to the user and ask: "Where should the file be written, and what should it be named?"

- Default location - accept the resolved directory and the language-appropriate default filename (`AUDIT.md` for English reports, or the filename defined in the matching `translation/` file for non-English reports), adjusted for any naming convention found in the resolved directory.
- Custom path - the user may supply a path relative to the audited repository or directory root (e.g. `reports/2026-06-audit.md`).

Always place the file inside the audited repository or directory. Do not write to an absolute path outside it unless the user explicitly provides one.

If the user already named a file or stated a delivery preference in the original request, honor it without asking again, still resolve the output directory using the rules above unless a full path was given.

**Overwriting existing files**

When the target file already exists (for example, a previous `AUDIT.md` or language-specific audit file), overwrite it with the new report. Increment the `Version` field in the Document Information section by reading the existing file, parsing the current version number, and incrementing the minor component up to 9 (for example, `1.0` becomes `1.1`, `1.9` becomes `2.0`, `9.9` becomes `10.0`). Do not prompt the user before overwriting. Do not create backup copies. The audit report is the authoritative artifact for the current assessment.

**Report language**

The default is the language of the user's request. When the request language is ambiguous, mixed, or cannot be determined with confidence, default to English and apply the English document style rules.

Ask only if the user explicitly asks for a different language.

When the report language is not English, load the matching `translation/` file and apply every translation, style rule, and encoding requirement defined there. The default filename changes to the language-specific filename defined in the translation file, and the report must be written in UTF-8 encoding with all language-specific diacritics preserved.

**Detail level**

Ask: "What level of detail should the report include?"

- **Standard** (default) - full report with all sixteen baseline sections, subject to explicit
  parameter exclusions plus any conditional sections whose criteria are met, complete findings, risk
  register, scorecard, and remediation roadmap.
- **Detailed** - full report plus extended remediation steps, additional verification methods, deeper architectural critique, and expanded impact analysis.
- **Brief** - Executive Summary, Health Dashboard (scorecard summary and risk heat map only), top risks only, and key recommendations. Detailed findings are summarized, not itemized.

**Evaluation scale**

Ask: "Which evaluation scale should be used for the scorecard?"

- **1-10** (default) - default scale with band definitions Poor (1-3), Average (4-6), Good (7-8), Excellent (9-10).
- **1-5** - alternative compact scale.

**Improvement suggestions**

Ask: "How should improvement suggestions be presented?"

- **Include with priorities** (default) - full Actionable Remediation Roadmap with P1-P4 priority tiers, impact/effort/complexity matrix, and verification steps.
- **Brief only** - top 5 recommendations without the full matrix or verification steps.
- **None** - omit the Actionable Remediation Roadmap. Include only findings and risks.

**Trade-off analysis**

Ask: "Should architectural trade-offs be analyzed?"

- **Standalone and embedded** (default) - a summary section and reasoning in relevant findings.
- **Embed into findings** - reasoning only in relevant finding blocks.
- **Omit** - do not include trade-off reasoning.

**Bypass rule**

At any parameter prompt, if the user responds with "bypass", "skip", "defaults", or equivalent, immediately accept all remaining defaults and proceed to Scope Definition.

**Scope Definition**

State what is in scope and what is not.

List the components, services, or files that were provided.

Record any constraints, goals, or target environment the user stated. Mark unstated constraints as `NOT SPECIFIED`.

Determine the maturity level claim, if any, so it can be tested against evidence later.

**Audit Purpose And Verification Scope**

Record whether the decision is engineering improvement, production readiness, or technical due
diligence for acquisition, investment, or supplier review.

For due diligence, include continuity, ownership, operating cost, roadmap feasibility, and IP/data
obligations using the existing assessment categories rather than creating a separate people score.

If business artifacts are unavailable, retain those concerns as `UNKNOWN` and request specific
artifacts, do not present a source-only review as complete business due diligence.

During scope definition, agree the permitted execution environment and network access.

Default to source inspection plus safe, available local checks after reviewing their side effects.

Do not treat acceptance of report-format defaults as permission to install tools, upload source,
change project policies, execute untrusted builds, or access live systems.

Record the resulting scope as source-only, tool-assisted, or runtime-validated for the checks
actually completed, not those planned.

For readiness audits, identify required evidence before judging readiness: applicable build and
test results, dependency review, targeted security checks, and operational recovery evidence.

**Evidence Gathering**

For each relevant assessment category, collect concrete anchors: files, config keys, commands, pipeline steps, documented procedures, or direct quotes.

When development standards documents were found during intake, collect evidence of conformance and divergence: for each rule in the standards, find representative source files that follow or violate it. Also collect the external best practices, style guides, or conventions that the standards reference or that apply to the stack, for the standards-quality evaluation in `assessment/standards-conformance.md`.

Respect `.gitignore` exclusions. Do not inspect files that are excluded by `.gitignore` patterns
(for example, `bin/`, `obj/`, `node_modules/`, `.env` files, or build artifacts). If a
`.gitignore` file is present, use it to filter the file list before analysis. If no `.gitignore` is
present, record the fact, but raise a finding only if relevant exclusions
are required or a concrete exposure is evidenced.

Do not yet form conclusions. Separate collection from judgement to avoid confirmation bias.

Where evidence is absent, record the gap explicitly with the appropriate missing-information token.

**Verification Plan And Execution**

Build a small verification matrix per project before assessment.

Select checks from the project's documented commands and the relevant assessment guides.

For executable projects, consider build/type checks, tests, formatting/lint, dependency advisories,
and license/SBOM checks as the baseline, executing applicable checks when safe and permitted.

Add targeted security regression checks for material trust boundaries.

Use coverage, mutation, fuzz, load, and recovery testing proportionately, not as an unconditional
requirement to install every tool.

For documentation-only skills or proposals, substitute reference, format, consistency, and scenario
checks rather than attempting unrelated compiler commands.

Record every selected check, including checks not run, in the ledger.

If a tool is missing or blocked, record the reason, confidence impact, and exact next step.

Do not silently convert the audit to source-only or mark an environment failure as a product defect.

**Execution safety**

Review scripts, build hooks, package-manager configuration, test setup, and tool provenance first.

Builds, procedural macros, dependency resolution, and SBOM generators can execute project code.

Use an approved disposable environment without ambient credentials for untrusted code.

Constrain network access, time, memory, and disk usage, and use synthetic data and local fixtures.

Do not mutate live data, weaken security controls, or alter source, manifests, lockfiles, or policy
exceptions to make verification pass.

Request approval for necessary installation, network use, or configuration changes.

Use pinned, reviewed tool versions rather than auto-installing the newest release.

Record any generated artifacts and keep them in the approved audit/work location.

An explicitly approved verification output may be inspected even if its directory is gitignored,
but this does not authorize inspecting unrelated ignored files or secrets.

**Evidence ledger**

Use globally unique evidence IDs within a report, with a project identifier on each row.

| Evidence ID | Project   | Check / Source      | Execution | Result        | Artifact |
|-------------|-----------|---------------------|-----------|---------------|----------|
| EVD-001     | <project> | <command or source> | <state>   | <observation> | <path>   |

Execution states are `COMPLETED`, `FAILED`, `BLOCKED`, `NOT RUN`, or `N/A`.

They are separate from category statuses and from what the check discovered.

For a source observation rather than a command, use `N/A` for execution and identify its evidence
basis as Inspected, Reported, or Inferred as appropriate.

`COMPLETED` means a check produced interpretable results, even if it found defects and returned
nonzero, while `FAILED` means execution did not produce a usable assessment.

Below each row, record the exact command and working directory or file and line range, revision
and dirty-tree state, date, tool/version, OS/target/features, exit code, and sanitized artifact
path.

For scanners, record database timestamp/revision, ruleset, exclusions, suppressions, and coverage.

For supplied CI output, record the run/revision and label it reported evidence unless independently
reproduced, noting any mismatch with the audited tree.

Preserve complete sanitized logs or machine-readable output when permitted, or record a precise
excerpt and explain why the original artifact is unavailable.

Tie findings to evidence IDs and explain what each item proves and does not prove.

**Category Assessment**

For each category, open the matching `assessment/` file and apply its checklist. For a full audit, this includes the two additional categories `assessment/ai-generated-code.md` and `assessment/copyright-review.md`.

Evaluate the inclusion criterion for each conditional assessment, listed in the Conditional Sections table of `process/report-format.md`. When the criterion is met, open the matching conditional file and apply it: `assessment/data-flow.md`, `assessment/design-patterns.md`, `assessment/threat-model.md`, `assessment/api-contract.md`, `assessment/skill-definition.md`, and `assessment/standards-conformance.md`. When a criterion is not met, omit that section and record the deliberate omission for Scope Exclusions. Do not force a conditional section onto a subject it does not fit.

Assign a status (`PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`, `N/A`) per the rules in
`principles/evaluation-rules.md`.

Record evidence, concrete risks, and neutral notes for each category.

**Synthesis**

Build the unified risk register from the risks surfaced during assessment, using `synthesis/risk-register.md`. Every risk must reference its source `FND-XXX`.

Build the project scorecard using `synthesis/project-scorecard.md`. Present the scoring rubric before the scores.

Draft the High-Level Observations section by selecting the top 5 most important findings from the Detailed Technical Findings. Keep each observation brief, full detail lives in the finding blocks.

Draft the Strengths & What's Working section by identifying 5-8 evidenced positive baselines from the codebase.

Surface trade-offs both as a standalone Trade-off Analysis section (using `synthesis/trade-off-analysis.md`) and embedded into relevant architectural or design findings where they directly explain a specific finding.

When structural debt distinct from risks was surfaced, build the Technical Debt Register using `synthesis/debt-register.md`. Every debt item must trace to a finding or a cited direct observation.

Draft the actionable remediation roadmap using `synthesis/remediation-roadmap.md`. Every recommendation must resolve a specific `FND-XXX`.

When the roadmap contains at least one P1 or P2 recommendation, build the Re-audit and Follow-up Plan using `synthesis/re-audit-plan.md`, mapping those findings to verification owners and closure evidence.

Add the Production Readiness Threshold paragraph to the Executive Summary, tying conditions to specific `RSK-XXX` IDs.

**Validation**

Re-check every finding against `principles/evaluation-rules.md`.

Confirm no finding rests on an assumption, that every status has evidence or a gap token, and that no language evaluates people.

Confirm every `FND-XXX` finding uses the correct pillar abbreviation and sequential numbering.

Confirm every `RSK-XXX` references its source `FND-XXX`.

Confirm every `REC-XXX` resolves a specific `FND-XXX`.

Confirm no plaintext secrets, passwords, or cryptographic keys appear in summaries, observations, or risk descriptions.

Confirm High-Level Observations contains at most five observations in the template's table and
paragraph format, each anchored to a specific `FND-XXX`.

Confirm strengths fit the selected detail level and are evidenced, use fewer than the suggested
count when the input supports fewer, rather than padding the report.

Confirm the Trade-off Analysis section uses the standard table format and frames each trade-off against a stated constraint.

Confirm every adverse finding in an initial audit has Remediation Status `Open`.

For re-audits, preserve IDs and update closure states only from the required evidence.

Confirm each conditional section was evaluated: it is either present because its criterion is met, or omitted with a deliberate one-line justification in Scope Exclusions. No conditional section may be present-but-empty, and none relevant to the subject may be silently dropped.

When a Threat Model is present, confirm every unmitigated threat traces to a `FND-XXX` and a `RSK-XXX`, and that no plaintext secret appears in a disclosure threat.

When an API Contract Conformance section is present, confirm each security gap maps to an OWASP API Security Top 10 (2023) code where one applies.

When a Standards Conformance section is present, confirm every conformance judgement cites a specific rule in the standards document and a specific file or pattern in the codebase, and that every standards-quality judgement cites a named external best practice. Confirm the References section lists every external source consulted during the standards-quality evaluation.

When a Technical Debt Register is present, confirm every `TDR-XXX` traces to a `FND-XXX` or a cited direct observation, and that no security risk is duplicated from the Unified Risk Register.

When a Re-audit and Follow-up Plan is present, confirm every row references a `FND-XXX` and that owners or dates absent from the input are marked `NOT SPECIFIED` rather than invented.

Confirm the Auditing Methodology cites only the reference standards actually applied, and the Scope Exclusions state the OWASP category coverage.

Confirm the report follows `process/report-format.md` section by section.

**Evidence and decision checks**

- Reconcile all counts with their source and scope, including tests, findings, risks, and scores.
- Ensure every `CRITICAL` and `HIGH` finding records a counter-check and verification limit.
- Keep build, test, scanner, and runtime claims consistent with the execution ledger.
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

| Scenario                                     | Expected Behavior                                    |
|----------------------------------------------|------------------------------------------------------|
| Changelog says tests pass, execution blocked | Reported only, readiness evidence incomplete         |
| Scanner exits nonzero with an advisory       | Completed check, finding requires triage             |
| Old crate, no advisory data                  | Freshness concern, vulnerability status unknown      |
| Guarded panic or excluded module             | Verify reachability, do not invent failure           |
| Local CLI without hosted runtime             | Assess local safety, omit irrelevant hosted controls |
| Due diligence with no cost or support data   | Retain unknowns, request artifacts                   |
| Two projects reuse FND-SEC-001               | Project-qualified shared references                  |
| Clean code with uniform tests                | No authorship inference, assess test behavior        |
| Security fix proposed but not run            | Keep verification pending, no closure claim          |
| Partial cost inputs or no telemetry          | No complete budget or numeric SLO claim              |

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

Add a short list of the specific artifacts that would raise confidence, so the user can supply them and re-run the audit.

A thin-input audit is still useful: it shows exactly what is missing for a readiness decision.

## Single-Dimension Audits

When the user asks for only one dimension, such as "review observability" or "check for AI-generated code" or "audit copyrights":

- Still load `principles/evaluation-rules.md` and `principles/output-style.md`.
- Load only the matching `assessment/` file.
- Produce only the matching report subsection plus any risks for that dimension.
- Note that the audit was scoped to a single dimension and is not a full readiness assessment.

## Re-Audit

When re-auditing after changes, keep the same categories, statuses vocabulary, scorecard dimensions, and finding IDs.

Record what changed since the previous audit and which findings moved status, so progress is comparable over time.

Update the Remediation Status column for findings that were closed since the previous audit. Add a "Re-audit Notes" paragraph noting which `FND-XXX` findings changed from `Open` to `Closed` and which `RSK-XXX` risks were mitigated.

## Multi-Project Audits

When the Project Identification step in Intake detects more than one project in the repository or directory, the audit runs independently for each project.

**Per-project independence**

Each project is assessed as a self-contained subject. Findings, risks, scorecard scores, and recommendations for one project must not reference or depend on another project unless the user explicitly states that cross-project interactions are in scope.

Finding IDs use the standard pillar abbreviations but are scoped per project. Each project's findings start at `FND-XXX-001`. Risk IDs and recommendation IDs also reset per project. The project name or identifier prefixes the finding block heading so the reader can locate the project within the report. See `process/report-format.md` for the multi-project report structure.

**Workflow for multiple projects**

Run the full workflow (Scope Definition through Validation) once per project, in sequence or in parallel as the agent's capabilities allow. After all per-project assessments are complete, run a single Synthesis phase that combines all projects into one report:

1. For each project, run Scope Definition, Evidence Gathering, Category Assessment, and per-project Validation.
2. After all projects are assessed, build the combined report per `process/report-format.md` Multi-Project Report Structure.
3. Each project gets its own complete set of sections: Technology Stack, Executive Summary, Health Dashboard, High-Level Observations, Auditing Methodology, Scoring Rubrics, System Context, Architectural Assessment, conditional sections, Strengths, Detailed Technical Findings, Unified Risk Register, Trade-off Analysis, and Actionable Remediation Roadmap.
4. Finding IDs, risk IDs, and recommendation IDs are scoped per project. Use the project identifier as a prefix in the finding heading so the reader can navigate. For example, `### FND-ARC-001: [api-service] Missing input validation`.
5. The Document Information section appears once at the top of the report and lists all audited projects.
6. A Project Inventory table immediately after Document Information lists each project with its path, version, and a one-line description.
7. Scope Exclusions and Re-audit and Follow-up Plan are shared sections at the end of the report, covering all projects.

**Parameter Configuration for multiple projects**

The Parameter Configuration phase runs once. The chosen parameters (detail level, evaluation scale, language, delivery mode, improvement suggestions, trade-off analysis) apply uniformly to all projects in the report. Do not re-ask parameters per project.

**Output location for multiple projects**

The report is a single file. Resolve the output directory once using the rules in the Report delivery section. When version-numbered subdirectories exist under `docs/audit/` or `docs/report/`, use the repository's primary version if one can be determined. When date-named subdirectories exist under `docs/audit/` or `docs/report/`, use the current date in ISO `YYYY-MM-DD` format. When no single primary version applies and no date pattern exists, use the root of the resolved directory without a subdirectory.
