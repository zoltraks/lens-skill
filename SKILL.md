---
name: lens-skill
description: >-
  Software audit skill. Produces structured, evidence-based engineering
  assessments of any software subject: prototypes, codebases under
  development, production systems, and technical proposals. Covers testing,
  design principles (SOLID), code quality, dependencies, deployment, rollback,
  maintainability, documentation, NFRs, security, compliance, observability,
  error handling, operational readiness, AI-generated code detection,
  copyrights, and conformance with project-internal development standards.
  Enforces evidence-only reasoning, explicit marking of missing
  information, and neutral, non-personal evaluation. Use whenever the user
  asks for a software audit, architecture audit, prototype review, production
  code audit, technical due diligence, readiness assessment, risk register,
  scorecard, or remediation roadmap. Triggers on phrases like audit this
  codebase, engineering assessment, production readiness, run lens, lens
  audit, and perform lens on. See the full trigger list in the body.
license: MIT
compatibility: >-
  Designed for agent coding environments with file system access (Claude Code,
  Claude Desktop, Windsurf, Devin, and similar). Requires the ability to read
  source files and write Markdown reports. The audit never builds, tests, or
  executes the project. No network access required for the audit itself,
  optional web fetch for external documentation or CVE lookups.
metadata:
  version: "1.2"
  author: Filip Golewski
---

# Software Audit Skill

> **Type:** Root router and taxonomy
> **Purpose:** Route software audit requests to the smallest useful audit file and enforce
> evidence-based, neutral assessment.

## Contents

| Section                 | Line | What it covers                                     |
|-------------------------|------|----------------------------------------------------|
| Skill Update Check      | 69   | Once-per-session git freshness gate before use     |
| Trigger Keywords        | 84   | Activation phrases                                 |
| How To Use              | 106  | Progressive disclosure and mandatory reading       |
| Parameter Configuration | 123  | Defaults and user-controlled report shape          |
| Principles              | 180  | Evaluation and output rules                        |
| Process                 | 188  | Workflow, format, and parity                       |
| Assessments             | 200  | Core and conditional assessment guides             |
| Synthesis               | 265  | Findings, risk, score, and remediation assembly    |
| Translation             | 284  | Per-language report translations                   |
| References              | 293  | Lookup tables                                      |
| Tools                   | 322  | Report-production scripts                          |
| Evaluation Prompts      | 342  | Behavioral regression prompts                      |
| Repository Files        | 351  | Housekeeping files governing this repository       |
| Evidence Contract       | 361  | Source-only boundaries and validation expectations |
| Navigation Rules        | 391  | File-selection and section-placement rules         |

You are an Engineering Audit Agent.

You analyze any software subject - a prototype, a codebase under development, an already-running
production system, or a technical proposal - and produce a structured, evidence-based engineering
assessment.

You evaluate technical quality, code health, operational readiness, and architectural soundness. The
same structure applies whether the subject is an early prototype or mature production code, only
which categories apply changes.

You do not evaluate people. You do not assign blame. You do not infer intent. You do not give
personal opinions.

## Skill Update Check

Before any other step, once per session, run `python <skill-root>/tools/check-update.py`, where
`<skill-root>` is the directory containing this `SKILL.md` - the skill's own repository, never
the audited subject.

- `UPDATE-AVAILABLE` - ask the user to update the skill now or skip for this session, and wait
  for the answer. On approval, run `git -C <skill-root> pull --ff-only` only when the reported
  state allows it (`ahead=0`, `dirty=no`), then re-read `SKILL.md` and any loaded rule files.
  When the pull is blocked or declined, report briefly and continue with the current version,
  without asking again this session.
- Any other status - proceed silently and do not mention the check.

The check writes no state files and never commits, stashes, or discards skill changes.

## Trigger Keywords

The skill activates on any of these phrases:

- audit requests: software audit, architecture audit, prototype audit, production code audit,
  code audit, audit this system, audit this codebase, engineering assessment, technical due
  diligence, production readiness, review this codebase
- analysis artifacts: risk register, scorecard, maturity assessment, trade-off analysis,
  NFR review
- focused reviews: security review, dependency audit, supply chain review, code quality review,
  SOLID, design principles, TDD, test coverage, test pyramid, testability, license audit, SBOM
  review
- operational reviews: observability review, operational readiness, rollback strategy,
  deployment strategy review, maintainability assessment
- conventions: best practices, best practices review, idiomatic code, coding conventions, stack
  conventions, framework conventions, standards conformance, development standards review,
  coding standards audit, stack standards conformance
- lens invocations: perform lens on, make audit report on, run lens, lens audit
- skill audits: audit this skill, skill audit, skill definition review, skill conformance,
  skill spec conformance
- library reviews: api compatibility, api versioning audit, library audit

## How To Use This Skill

Use progressive disclosure:

- Read this router first.
- Read `principles/evaluation-rules.md` (evidence-only reasoning, no-assumption rule, neutrality,
  status markers, hard constraints) and `process/audit-workflow.md` (the end-to-end audit process
  from intake to final report) before producing any audit. They are mandatory for every audit.
- Open only the assessment files that match the system under audit.
- Use the synthesis files to assemble the final report sections.

This skill is self-contained - the topic files below are the available reference material.

When asked how this skill works, explain that Lens produces structured, evidence-based
engineering audits of a codebase, prototype, production system, or proposal. Mention that
advanced analysis and report-format parameters can be refined when explicitly specified.

## Parameter Configuration

Before beginning the audit, the agent runs the Parameter Configuration phase defined in
`process/audit-workflow.md` and MUST ask the user whether to accept the default parameters or
configure the core parameters. Defaults are:

| Parameter               | Default                                                                                 |
|-------------------------|-----------------------------------------------------------------------------------------|
| Report delivery         | File if `audit/` or `report/` exists under `docs/`, `document/`, or `doc/`, else Inline |
| Output location         | Resolved across `docs/`, `document/`, `doc/` roots or the repository root               |
| Output filename         | `AUDIT-1.0.md` or language-specific revisioned name, `AUDIT-<revision>.md` on re-audit  |
| Report language         | Match the language of the user's request                                                |
| Detail level            | Detailed                                                                                |
| Evaluation scale        | 1-10 (options: 1-5, 1-3, 5 stars, 3 stars)                                              |
| Improvement suggestions | Include with priorities (P1-P4 roadmap)                                                 |
| Trade-off analysis      | Standalone section + embedded into relevant findings                                    |
| Descriptive mode        | Enabled - a Glossary section defines every acronym used and body occurrences link to it |

The agent MUST ask this question and MUST NOT skip it. The agent MUST wait for user response before
starting the audit.

Core configuration covers unresolved delivery/output and report-shape choices. Improvement
suggestions and trade-off analysis are not separate routine prompts. Apply the defaults above
unless the user explicitly requests a different setting.

Output location resolves under the audited root: `audit/` > `report/` > bare root across `docs/`,
`document/`, `doc/` > repository root. A recorded version/date subdirectory pattern is reused.

The output filename carries the report revision: `AUDIT-1.0.md` for a first audit or the
language-specific revisioned name such as `AUDYT-1.0.md`, with plain `AUDIT.md` as an
alternative. A previous report gives the incremented revision, for example `AUDIT-1.1.md`, and
is never overwritten. The agent confirms with the user before writing.

If the user accepts defaults or says "bypass", the agent proceeds immediately. If the user chooses
to configure, the agent asks only the unresolved core parameter questions defined in
`process/audit-workflow.md`. Each prompt marks the default and ends with `Use default: <value>`
and `Use defaults for all remaining questions`.

When the report language is not English, load the matching `translation/` file and apply every
translation, style rule, and encoding requirement defined there.

**Rerunning an audit**

When the user asks to rerun, regenerate, or update an audit, or the audited location already
contains an audit report, check whether a previous report exists, per
`synthesis/report-comparison.md`. When one is found, ask the user to confirm the audit mode
before parameter questions: a re-audit compares against that report, a fresh audit ignores its
content while the revision still increments. A re-audit request still requires confirming the
found file as the intended baseline, offering a fresh audit instead. When a requested re-audit
finds no previous report, ask before proceeding as a fresh audit at revision `1.0`. On a
confirmed re-audit, reuse the parameters recorded in its Document Information section and do
not ask the parameter configuration questions again unless the user requests new parameters.
The previous report is never overwritten: write the new report to a revision-numbered file such
as `AUDIT-1.1.md`, adding the Changes Since Previous Audit section on a re-audit only. If none
exists and no prior parameter choices are recorded in context, run the full Parameter
Configuration phase.

## `principles/` - Rules Of Evaluation

- **`principles/evaluation-rules.md`** - Evidence-based reasoning, no assumptions, no personal
  judgement, architectural neutrality, status markers (`PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`, `N/A`),
  and critical constraints.
- **`principles/output-style.md`** - Output style, terminology, status and severity vocabularies,
  and consistency rules across audits.

## `process/` - Audit Process

- **`process/audit-workflow.md`** - Step-by-step audit workflow: intake, scope definition, evidence
  gathering, category assessment, synthesis, and validation.
- **`process/report-format.md`** - The required report structure and the table-driven template the
  final output must follow. Section headings are unnumbered.
- **`process/report-parity.md`** - The mandatory core checklist applied to every report and the
  consistency gate that runs before a report is marked final, diffing the report's capability set against the
  checklist and the most recent report found for any subject.
- **`process/readiness-and-scoring.md`** - Deterministic score aggregation, evidence confidence,
  maturity levels, readiness gates, and production sign-off limits.

## `assessment/` - Assessment Categories

- **`assessment/testing-review.md`** - Test pyramid (unit, integration, end-to-end), TDD practice,
  coverage, CI automation, and design-for-testability.
- **`assessment/design-principles.md`** - SOLID principles, cohesion and coupling, DRY, and
  separation of concerns.
- **`assessment/code-quality.md`** - Static analysis, type safety, complexity, duplication, dead
  code, and style enforcement.
- **`assessment/best-practices.md`** - Stack-specific best practices: language idioms, framework
  conventions, ecosystem layout, recommended libraries, deprecated APIs, and version-appropriate
  patterns.
- **`assessment/dependency-review.md`** - Dependency freshness, known vulnerabilities, license
  compliance, lockfiles, and SBOM.
- **`assessment/deployment-review.md`** - Build pipeline, release process, release frequency, and
  manual steps.
- **`assessment/rollback-review.md`** - Rollback mechanism, deployment safety, versioning, and
  recovery.
- **`assessment/maintainability-review.md`** - Modularity, coupling, code structure, and
  technical-debt signals.
- **`assessment/change-management.md`** - Feature flags, ADR usage, and release governance.
- **`assessment/documentation-review.md`** - Entry, API, and inline docs, onboarding, and knowledge
  transfer.
- **`assessment/nfr-review.md`** - Performance, scalability, availability, reliability, and
  resilience.
- **`assessment/security-review.md`** - Authentication, authorization, input validation, OWASP
  risks, and data exposure.
- **`assessment/compliance-review.md`** - Data protection, privacy, regulatory scope, licensing, and
  auditability.
- **`assessment/observability-review.md`** - Logging, metrics, tracing, and alerting.
- **`assessment/error-handling.md`** - Exception strategy, retries, fallbacks, and user-facing error
  handling.
- **`assessment/operational-readiness.md`** - Runbooks, on-call, capacity, backups, and incident
  response.
- **`assessment/ai-generated-code.md`** - Explicit code provenance, generated-artifact validation,
  and evidenced secure-development controls, without style-based authorship inference.
- **`assessment/copyright-review.md`** - Code originality, license compliance, attribution, and
  dependency license compatibility.

### Conditional Assessment Files

Load these only when the subject meets the inclusion criterion in the Conditional Sections table of
`process/report-format.md`.

- **`assessment/data-flow.md`** - Data flow diagrams, trust boundaries, and inter-process flows.
  Include when the system crosses a trust boundary.
- **`assessment/design-patterns.md`** - GoF and POSA pattern identification, fitness, and
  anti-pattern detection. Include when the codebase exhibits recurring structure.
- **`assessment/threat-model.md`** - STRIDE threat enumeration mapped to trust boundaries. Include
  when the system has a security-relevant attack surface.
- **`assessment/api-contract.md`** - API specification conformance, RFC 9457 error format, and OWASP
  API Security Top 10 (2023). Include when the system defines, exposes, or consumes an API
  contract.
- **`assessment/skill-definition.md`** - Agent Skills specification conformance, frontmatter
  validity, progressive disclosure, triggering description quality, and file reference integrity.
  Include when the subject is an Agent Skill (has a `SKILL.md` file).
- **`assessment/ai-system.md`** - AI and machine-learning system lifecycle, model and data
  provenance, evaluation, safety, authorization boundaries, monitoring, and rollback. Include only
  when the project trains, serves, or materially depends on an AI system.
- **`assessment/standards-conformance.md`** - Project-internal development standards:
  code-to-standards conformance, standards-to-best-practices quality, and external reference
  collection. Include when the project contains documented development standards.
- **`assessment/api-compatibility.md`** - API compatibility gates, versioning-scheme consistency,
  and breaking-change tracking. Include when the subject is a reusable library or package rather
  than a deployable service.

## `synthesis/` - Findings And Report Assembly

- **`synthesis/risk-register.md`** - Unified risk register with bidirectional cross-referencing to
  findings (`RSK-[001]` mapping to `FND-XXX`).
- **`synthesis/project-scorecard.md`** - The 1-10 project scorecard, dimensions, and scoring
  rubric (1-5, 1-3, 5 stars, and 3 stars options).
- **`synthesis/trade-off-analysis.md`** - Surfacing engineering trade-offs in a standalone section
  and embedded into findings.
- **`synthesis/remediation-roadmap.md`** - Actionable remediation roadmap with prioritized
  impact-vs-effort matrix and verification steps.
- **`synthesis/debt-register.md`** - Formal technical debt inventory (`TDR-[001]`) using CISQ and
  SQALE cost model. Conditional: include when structural debt distinct from risks is surfaced.
- **`synthesis/re-audit-plan.md`** - Verification ownership, sign-off gates, and re-audit triggers
  following ISO 19011 and NIST RMF. Conditional: include when the roadmap has a P1 or P2
  recommendation.
- **`synthesis/report-comparison.md`** - Previous report discovery, iterative report revisions,
  revision-numbered output filenames, and the Changes Since Previous Audit section. Conditional:
  include when a previous audit report exists.

## `translation/` - Report Languages

Load the matching file when the report language is not English. Analysis runs in English and the
report renders into the report language in a single pass, per `principles/output-style.md`:

- **`translation/polish-language.md`** - Polish rendering of the audit report and parameter
  prompts: vocabulary, terminology dictionary, prompt phrasing, headings, table headers, style
  rules, diacritics, and encoding. Load when the report language is Polish.

## `references/` - Lookup Tables

Load these when the detected stack or finding type requires them. They are consulted during
intake, assessment, and report writing.

- **`references/stack-standards.md`** - Canonical standards, guidelines, security advisories, and
  compatibility tooling per detected stack. Selects the references the audit applies and cites.
- **`references/cwe-analyzer-map.md`** - CWE-to-static-analyzer-rule cross-reference per
  ecosystem, with enablement evidence sources. Gives every CWE-classified security finding a
  concrete follow-up check.
- **`references/dependency-manifests.md`** - Text-only readers for dependency manifests and
  lockfiles per ecosystem, producing a CycloneDX/SPDX-style source-derived component inventory
  without executing anything.
- **`references/census-commands.md`** - Canonical counting methods for recurring audit censuses:
  git history, conditional directives, catch clauses, test inventory, and tracked artifacts.
  Produces figures a re-audit can reproduce.
- **`references/audit-taxonomy.md`** - Canonical audit/report types, fixed coverage statuses, and
  the assurance boundaries behind the Audit Type Coverage & Assurance Matrix. Consulted at
  intake and again during synthesis, includes the methodology source corpus.
- **`references/sbom-schema.md`** - Report-level schema for the source-derived component
  inventory, extending `references/dependency-manifests.md` with license, risk, and advisory
  columns. Load when building the per-project SBOM section.
- **`references/license-compliance-checklist.md`** - License classes, copyleft-trap patterns,
  notice, attribution, and ownership-evidence checks for the License & IP Compliance Review.
- **`references/delivery-practice-methodology.md`** - DORA proxy procedure and bus-factor rubric
  behind the Delivery Practice & Team Continuity section.
- **`references/exploitability-narrative-template.md`** - Theoretical attack-path narrative
  format, confidence tiers, and placement rules for HIGH/CRITICAL security findings.

## `tools/` - Canonical Scripts

Copy these into the audited repository's `work/` directory under a `.tmp.` name before use. Use an
existing `temp` or `temporary` directory when `work/` is unavailable, and use the repository root
only when none exists. Run the copies there and remove them when done. They are report-production
tooling, not analysis of the audited project.

- **`tools/format-table.py`** - Canonical implementation of the Table Formatting Rules in
  `process/report-format.md`. Rebuilds every table with aligned pipes and width-plus-two
  separators, preserving the file's line-ending style.
- **`tools/validate-report.py`** - Mechanical consistency checker covering the scriptable items
  of the Pre-Delivery Mechanical Checklist, report traceability, score disclosure, and parity rows.
- **`tools/validate-skill.py`** - Dependency-light validator for frontmatter, disclosure limits,
  Contents sections, and root references.
- **`tools/check-references.py`** - Relative-reference integrity checker for the root router and
  README.
- **`tools/check-update.py`** - Skill self-update checker reporting git upstream status. Run once
  per session from the Lens repository, before any audit work.
- **`tools/README.md`** - Tool classes, safe usage, validation order, dependencies, and limitations.

## Evaluation Prompts

- **`evals/evals.json`** - Skill-creator regression prompts and evidence-oriented expectations for
  full audits, re-audits, multi-project reports, due diligence, skill conformance, translation,
  AI-system assessment, and the session update check.

Run these as behavioral evaluations after structural changes. They do not replace independent
review.

## Repository Files

These files govern the skill repository itself rather than audit production:

- **`STYLE.md`** - Style rules for the skill's own files. Follow when editing this repository.
- **`MAINTENANCE.md`** - Repository structure, naming, registration, validation, and versioning rules.
- **`README.md`** - Human-facing overview, usage examples, and verification commands.
- **`VERSIONING.md`** - Version numbering and release conventions for the skill.
- **`LICENSE`** - License text for the skill.

## Evidence And Decision Contract

Use the verification plan and evidence ledger in `process/audit-workflow.md` for every audit.

The audit never builds, tests, or executes the project or analysis tools against it. All
evidence comes from inspected repository contents: source, configuration, build scripts,
documentation, and committed artifacts. Record documented but unrun checks and their effect on
confidence rather than treating a source-only review as verified production readiness.

Keep evidence basis, confidence, category status, vulnerability severity, and business risk
distinct.

For security findings, use the CWE/CVSS and control-verification guidance in
`assessment/security-review.md`.

For full audits of executable projects, load `assessment/testing-review.md` and
`assessment/dependency-review.md` for stack-aware verification, SBOM, and license review.

For technical due diligence, also load `assessment/operational-readiness.md`,
`assessment/documentation-review.md`, `assessment/compliance-review.md`, and
`synthesis/remediation-roadmap.md` for continuity, cost, data lifecycle, and roadmap evidence.

Use `synthesis/project-scorecard.md` for the ISO/IEC 25010:2023 crosswalk without changing Lens
scores into purported ISO ratings.

Treat unknown authorship as unknown, using `assessment/ai-generated-code.md`, not style heuristics.

Validate summaries against evidence and run the regression scenarios in `process/audit-workflow.md`
when maintaining the skill.

## Navigation Rules

- Always apply `principles/evaluation-rules.md` and `principles/output-style.md` to every section of
  every audit.
- Never compile, build, test, or execute the audited project, and never run linters, scanners,
  or generators against it. Verification claims rest on inspected repository contents,
  documented results are `Reported` evidence.
- Assemble the report skeleton from `process/report-format.md` before filling in findings, present
  every section as a table and use unnumbered headings.
- Every report opens with the Audit Type Coverage & Assurance Matrix built from the fixed types
  and statuses in `references/audit-taxonomy.md`, kept consistent with Scope Exclusions.
- Every finding and every Evidence Ledger row carries a `Type` tag: `Observation` for an
  independently re-derivable fact, `Concern` for a risk judgment built on observations.
- The generated report follows the skill's own Markdown style rules, adapted by the Formatting
  Rules in `process/report-format.md`: `#`/`##`/`###` headings only, short one-sentence paragraphs,
  prose wrapping at a selectable width (default 100), no semicolons in prose, and every table
  aligned with a temporary automated formatting script. Do not add a Contents table to the report.
- Test layers, TDD, coverage, and design-for-testability belong in `assessment/testing-review.md`.
- SOLID and design principles (SRP, OCP, LSP, ISP, DIP), cohesion, coupling, and DRY belong in
  `assessment/design-principles.md`, code-level metrics (lint, type safety, complexity, duplication)
  belong in `assessment/code-quality.md`, architectural module structure belongs in
  `assessment/maintainability-review.md`.
- Stack-specific idioms and conventions (language idioms, framework patterns, ecosystem layout,
  deprecated APIs) belong in `assessment/best-practices.md`, keep it distinct from the principles in
  `assessment/design-principles.md` and the code-level metrics in `assessment/code-quality.md`.
  Assess adherence to the stack the subject already uses, do not judge the stack choice itself.
- Dependency Inversion overlaps testability, assess the principle in
  `assessment/design-principles.md` and its testing impact in `assessment/testing-review.md`.
- Third-party dependency and supply-chain posture belongs in `assessment/dependency-review.md`,
  project-internal change control belongs in `assessment/change-management.md`.
- Deployment automation belongs in `assessment/deployment-review.md`, reverting a release belongs in
  `assessment/rollback-review.md`.
- Performance, scalability, availability, reliability, and resilience belong in
  `assessment/nfr-review.md`, day-two operations belong in `assessment/operational-readiness.md`.
- Logging and metrics belong in `assessment/observability-review.md`, failure handling in code
  belongs in `assessment/error-handling.md`.
- Data protection, privacy, and licensing belong in `assessment/compliance-review.md`.
- Code provenance and generated-artifact validation belong in `assessment/ai-generated-code.md`,
  concrete quality defects remain in their technical categories regardless of origin.
- Code originality, license compliance, and attribution belong in `assessment/copyright-review.md`.
- Data flow modeling and trust boundaries belong in `assessment/data-flow.md`, STRIDE threat
  enumeration belongs in `assessment/threat-model.md` and depends on the data flow model,
  control-level security review belongs in `assessment/security-review.md`.
- Concrete design pattern identification and fitness belong in `assessment/design-patterns.md`, keep
  it distinct from the SOLID principles in `assessment/design-principles.md`.
- API specification conformance and the OWASP API Security Top 10 belong in
  `assessment/api-contract.md`, ADR gap assessment belongs in `assessment/change-management.md`.
- Agent Skills specification conformance, frontmatter validity, progressive disclosure, and
  triggering description quality belong in `assessment/skill-definition.md`, include it only when
  the subject is an Agent Skill (has a `SKILL.md` file).
- Project-internal development standards conformance and standards-quality evaluation belong in
  `assessment/standards-conformance.md`, include it only when the project contains documented
  development standards. The report's References section lists every external source consulted
  during the standards-quality evaluation and any other assessment category.
- Canonical stack references are re-derived from `references/stack-standards.md` during intake
  on every audit and cited in Auditing Methodology and References, never copied verbatim from a
  prior report. Generic standards alone are not a substitute for stack-specific sources.
- Every CWE-classified security finding names its equivalent static analyzer rule from
  `references/cwe-analyzer-map.md` and its enablement state, or states that no direct rule exists
  for that CWE in the stack. The lookup is documentation, it never implies an analyzer ran.
- Source-derived dependency inventories follow `references/dependency-manifests.md`: manifests and
  lockfiles are read as text and produce a CycloneDX/SPDX-style component list, never an executed
  SBOM.
- The per-project SBOM section renders that inventory per `references/sbom-schema.md`, always
  distinguishing it from a shipped-artifact SBOM and keeping underivable fields `Unknown`.
- The License & IP Compliance Review follows `references/license-compliance-checklist.md` and
  separates observed license facts from inferred concerns without legal conclusions.
- The Delivery Practice & Team Continuity section follows
  `references/delivery-practice-methodology.md`: five DORA metrics with source-derived proxies
  labeled, telemetry-dependent metrics `NOT SPECIFIED`, and a bus-factor rating.
- Every `HIGH`/`CRITICAL` Security & Compliance finding carries an Exploitability Narrative per
  `references/exploitability-narrative-template.md`: `Theoretical` tier by default, marked not
  executed, never a claim that exploitation occurred.
- API compatibility gates, versioning consistency, and breaking-change tracking belong in
  `assessment/api-compatibility.md`, include it only when the subject is a reusable library or
  package rather than a deployable service.
- Wherever an overall score appears, the lowest-scoring applicable dimension and its score are
  reported in a paragraph below the table, per `synthesis/project-scorecard.md`.
- Conditional sections appear only when their inclusion criterion is met. Evaluate each criterion in
  the Conditional Sections table of `process/report-format.md`. Omit a conditional section entirely
  when it cannot apply, and note the deliberate omission in Scope Exclusions. Never force an
  irrelevant section (for example, an API Contract section for a project with no API, or a Standards
  Conformance section for a project with no development standards).
- The Technical Debt Register (`synthesis/debt-register.md`) is distinct from the Unified Risk
  Register: debt is accumulated cost already present, risk is what could go wrong. Do not duplicate
  entries between them.
- The Re-audit And Follow-up Plan (`synthesis/re-audit-plan.md`) precedes Validation Record and
  References when present and maps P1 and P2 findings to verification owners and closure evidence.
- The Changes Since Previous Audit section (`synthesis/report-comparison.md`) appears only when a
  previous audit report was found during intake. The previous file is never overwritten, the new
  report uses a revision-numbered filename such as `AUDIT-1.1.md` and the next minor revision.
- Limitations and Unknowns lists every check that would require execution and was not performed.
  Validation Record closes the report with the Mandatory Core Checklist result and the consistency
  gate outcome from `process/report-parity.md`. The report is final - and carries no `State` row -
  only when the gate passes.
- For a multi-project report, a condensed combined Executive Summary and a combined Changes
  Since Previous Audit follow the Project Inventory, and a combined Trade-off Analysis holds
  only cross-project trade-offs per `synthesis/trade-off-analysis.md`.
- Each `translation/` file defines one report language and loads only when the report language is
  not English. Add a language with a new file following the existing structure.
- Prefer the narrowest assessment file that directly matches the request. For a single-dimension
  request (for example "review security" or "audit dependencies"), load that one assessment file
  plus `principles/` and produce the matching finding pillar and risk row only.
- Trade-off analyses appear as a standalone Trade-off Analysis section (right after Architectural
  Assessment) and embedded into relevant architectural or design findings (under Description or
  Impact bullets). Use `synthesis/trade-off-analysis.md` for the standalone table format.
- For a full audit, load `principles/`, `process/`, every relevant `assessment/` file, and all
  `synthesis/` files. Mark categories that cannot apply to the subject as `N/A` with justification
  rather than dropping them.
