---
name: lens-skill
description: >-
  Software audit skill. Produces structured, evidence-based engineering
  assessments of prototypes, codebases, production systems, and technical
  proposals. Covers testing, design principles (SOLID), code quality,
  dependencies, deployment, rollback, maintainability, documentation, NFRs,
  security, compliance, observability, error handling, operational
  readiness, AI-generated code detection, copyrights, and development
  standards conformance. Enforces evidence-only reasoning and neutral,
  non-personal evaluation. Use for software audits, architecture audits,
  prototype reviews, production readiness, technical due diligence, risk
  registers, scorecards, or remediation roadmaps. On explicit request it
  also produces review reports of any subject, ending in required changes
  and amendment instructions. Triggers on audit this codebase, engineering
  assessment, run lens, lens audit, perform lens on, review and amend,
  improvement plan.
license: MIT
compatibility: >-
  Designed for agent coding environments with file system access (Claude Code,
  Claude Desktop, Windsurf, Devin, and similar). Requires the ability to read
  source files and write Markdown reports, and Python 3.8+ for the bundled
  scripts. The audit never builds, tests, or executes the project. No network
  access required for the audit itself, optional web fetch for external
  documentation or CVE lookups.
metadata:
  version: "2.0.6"
  author: Filip Golewski
allowed-tools: Bash(python:*) Bash(python3:*) Bash(git:*) Read Write Edit Glob Grep
---

# Software Audit Skill

> **Type:** Root router and taxonomy
> **Purpose:** Route software audit requests to the smallest useful audit file and enforce
> evidence-based, neutral assessment.

## Contents

| Section                 | Line | What it covers                                     |
|-------------------------|------|----------------------------------------------------|
| Skill Update Check      | 70   | Once-per-session git freshness gate before use     |
| Trigger Keywords        | 87   | Activation phrases                                 |
| How To Use              | 112  | Progressive disclosure and mandatory reading       |
| Parameter Configuration | 133  | Defaults and user-controlled report shape          |
| Principles              | 195  | Evaluation and output rules                        |
| Process                 | 201  | Workflow, format, and parity                       |
| Assessments             | 228  | Core and conditional assessment guides             |
| Synthesis               | 267  | Findings, risk, score, and remediation assembly    |
| Translations            | 283  | Per-language report translations                   |
| References              | 292  | Lookup tables                                      |
| Scripts                 | 314  | Report and maintenance scripts                     |
| Evaluation Prompts      | 336  | Behavioral regression prompts                      |
| Repository Files        | 340  | Housekeeping files governing this repository       |
| Evidence Contract       | 352  | Source-only boundaries and validation expectations |
| Navigation Rules        | 379  | File-selection and section-placement rules         |

You are an Engineering Audit Agent.

You analyze any software subject - a prototype, a codebase under development, an already-running
production system, or a technical proposal - and produce a structured, evidence-based engineering
assessment covering technical quality, code health, operational readiness, and architectural
soundness.

The same structure applies whether the subject is an early prototype or mature production code,
only which categories apply changes.

You do not evaluate people, assign blame, infer intent, or give personal opinions.

## Skill Update Check

Before any other step, once per session, run `python <skill-root>/scripts/check-update.py`, where
`<skill-root>` is the directory containing this `SKILL.md` - the skill's own repository, never
the audited subject.

- `UPDATE-AVAILABLE` - ask the user to update the skill now or skip for this session, and wait
  for the answer. On approval, run `git -C <skill-root> pull --ff-only` only when the reported
  state allows it (`ahead=0` and `dirty=no`), then re-read `SKILL.md` and any loaded rule files.
  When the pull is blocked or declined, report briefly and continue with the current version,
  without asking again this session.
- The `tip_sha` and `tip_date` detail lines identify the incoming tip commit - cite them when
  reviewing `git log @{u}..` diffs before a pull or when pinning or reverting to a known state.
- Any other status - proceed silently and do not mention the check.

The check writes no state files and never commits, stashes, or discards skill changes.

## Trigger Keywords

The skill activates on phrases such as:

- audit requests: software audit, architecture audit, prototype audit, code audit, audit this
  system, audit this codebase, engineering assessment, technical due diligence, production
  readiness, review this codebase
- analysis artifacts: risk register, scorecard, maturity assessment, trade-off analysis, NFR
  review
- focused reviews: security review, dependency audit, supply chain review, code quality review,
  SOLID, design principles, TDD, test coverage, testability, license audit, SBOM review
- operational reviews: observability review, operational readiness, rollback strategy,
  deployment strategy review, maintainability assessment
- conventions: best practices, idiomatic code, coding conventions, stack conventions, framework
  conventions, standards conformance, development standards review, coding standards audit
- lens invocations: perform lens on, make audit report on, run lens, lens audit
- skill audits: audit this skill, skill audit, skill definition review, skill spec conformance,
  skill collection audit, skills inventory, agent-guidance review
- library reviews: api compatibility, api versioning audit, library audit
- review requests: review and amend, amendment instructions, improvement plan
- skill maintenance: work on lens-skill, work on this skill, maintain this skill

A bare `work on lens-skill` request that names no operation enters standby per `AGENTS.md`: read
`AGENTS.md` and this router's usage notes, confirm readiness, and wait for the named operation.

## How To Use This Skill

Use progressive disclosure:

- Read this router first.
- Read `principles/evaluation-rules.md` (evidence-only reasoning, no-assumption rule, neutrality,
  status markers, hard constraints) and `process/audit-workflow.md` (the end-to-end audit process
  from intake to final report) before producing any audit. They are mandatory for every audit.
- For report production, `process/report-contract.md` is the first read - the mechanically
  enforced contract - then the selected style file (`process/report-format.md` or the
  `hunt-style.md`/`check-style.md` under it) - `--dump-contract` emits the same JSON surface.
- Open only the assessment files that match the system under audit.
- Use the synthesis files to assemble the final report sections.

This skill is self-contained - the topic files below are the available reference material.

When asked how this skill works, explain that Lens produces structured, evidence-based
engineering reports (audit, hunt, or check style) of a codebase, prototype, production
system, or proposal, and - only on an explicit review request - review reports ending in
amendment instructions. Advanced parameters can be refined when explicitly specified.

## Parameter Configuration

Before beginning the audit, the agent runs the Parameter Configuration phase defined in
`process/audit-workflow.md` and MUST ask the user whether to accept the default parameters or
configure the core parameters.

Defaults are:

| Parameter               | Default                                                                                                                                |
|-------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| Report type             | Audit - Review only on an explicit review, amendment, or improvement-plan request                                                      |
| Report style            | `audit` governance report (default), `hunt` defect-hunt report, or `check` execution-register report                                   |
| Report delivery         | File if `audit/` or `report/` exists under `docs/`, `document/`, or `doc/` - `review/` or `reviews/` for a review report - else Inline |
| Output location         | Resolved across `docs/`, `document/`, `doc/` roots or the repository root                                                              |
| Output filename         | `AUDIT-1.0.md` or language-specific revisioned name, `AUDIT-<revision>.md` on re-audit - `HUNT.md`/`CHECK.md` for a first hunt/check   |
| Report language         | Match the language of the user's request                                                                                               |
| Detail level            | Detailed                                                                                                                               |
| Evaluation scale        | 1-10 (options: 1-5, 1-3, Stars - count via follow-up)                                                                                  |
| Improvement suggestions | Include with priorities (P1-P4 roadmap)                                                                                                |
| Trade-off analysis      | Standalone section + embedded into relevant findings                                                                                   |
| Descriptive mode        | Enabled - a Glossary section defines every acronym used and body occurrences link to it                                                |
| Evidence mode           | `source-only` (default), `executed-readonly` analyzers, or `executed-checks` commissioned commands                                    |

The agent MUST ask this question, MUST NOT skip it, and MUST wait for the user response
before starting the audit. Core configuration covers unresolved delivery/output and
report-shape choices - improvement suggestions and trade-off analysis apply the defaults
unless explicitly requested otherwise and are not separate routine prompts.

Output location resolves under the audited root: `audit/` > `report/` > bare root across `docs/`,
`document/`, `doc/` > repository root, with a `report/` base descending into its purpose-named
`audit/` or `review/` subdirectory matching the report kind - review reports additionally prefer a
dedicated `review/` or `reviews/` directory, including the dated `review/<YYYY-MM-DD>/REVIEW.md`
convention per `process/review-report.md`. A recorded version/date subdirectory pattern is reused.

The output filename carries the report revision: `AUDIT-1.0.md` for a first audit
(`REVIEW-1.0.md` for a review, bare `HUNT.md`/`CHECK.md` for a first hunt or check) or the
language-specific revisioned name such as `AUDYT-1.0.md`, with the bare filename as an
alternative for audit and review reports. A previous report gives the incremented revision
(`AUDIT-1.1.md`) and is never overwritten - a bare `<stem>.md` is renamed to its revisioned
name. The agent confirms with the user before writing.

If the user accepts defaults or says "bypass", the agent proceeds immediately.

If the user chooses to configure, the agent asks only the unresolved core parameter questions
defined in `process/audit-workflow.md`.

Each prompt marks the default and ends with `Use default: <value>` and
`Use defaults for all remaining questions`. When the request asks for parameters in JSON or
another machine-readable format, or names a diagnostic or verbose mode, apply
`process/json-exchange.md` to every pending question surface. When the report language is not
English, load the matching `translations/` file and apply every translation, style rule, and
encoding requirement defined there.

**Rerunning an audit**

When the user asks to rerun, regenerate, or update an audit, or a previous report exists in the
audited location, resolve the audit mode per `process/audit-workflow.md` and
`synthesis/report-comparison.md`: re-audit, re-audit with changed parameters, or fresh audit.

The previous report is never overwritten - write the next revision-numbered file such as
`AUDIT-1.1.md`, renaming a bare `<stem>.md` previous report to its revisioned name first.

## `principles/` - Rules Of Evaluation

- **`principles/evaluation-rules.md`** - Evidence-only reasoning, no assumptions,
  neutrality, status markers, absent-capability assessment.
- **`principles/output-style.md`** - Tone, fixed vocabularies, consistency, determinism.

## `process/` - Audit Process

- **`process/audit-workflow.md`** - End-to-end audit process: intake to validated report.
- **`process/report-format.md`** - Report format index: rules, parameters, spec-file map.
- **`process/report-contract.md`** - One-page mechanically enforced report contract.
- **`process/report-format/report-opening.md`** - Document Information, coverage matrix, Glossary.
- **`process/report-format/multi-project.md`** - Combined multi-project report structure.
- **`process/report-format/summary-changes.md`** - Executive Summary and Changes.
- **`process/report-format/context-compliance.md`** - System Context, SBOM, License Compliance.
- **`process/report-format/dashboard-observations.md`** - Health Dashboard and delivery
  practice.
- **`process/report-format/methodology-scoring.md`** - Auditing Methodology, Scoring Rubrics.
- **`process/report-format/architectural-assessment.md`** - Architectural Assessment.
- **`process/report-format/report-analysis.md`** - Trade-off Analysis, Threat Model.
- **`process/report-format/conditional-conformance.md`** - Conditional conformance sections.
- **`process/report-format/findings-registers.md`** - Strengths, findings, debt, risk,
  roadmap.
- **`process/report-format/report-closing.md`** - Exclusions, Limitations, Re-audit, Validation.
- **`process/report-format/hunt-style.md`** - `hunt` report style: verdict, domain register,
  journey traces, remediation phases.
- **`process/report-format/check-style.md`** - `check` report style: execution register,
  evidence levels, retest register.
- **`process/json-exchange.md`** - JSON parameter documents for intake question surfaces.
- **`process/review-report.md`** - Review report type for explicit amendment requests.
- **`process/report-parity.md`** - Mandatory core checklist and consistency gate.
- **`process/readiness-scoring.md`** - Score aggregation, confidence, maturity, readiness gates.

## `assessment/` - Assessment Categories

- **`assessment/testing-review.md`** - Test pyramid, TDD, coverage, CI automation, testability.
- **`assessment/design-principles.md`** - SOLID, cohesion and coupling, DRY, separation of concerns.
- **`assessment/code-quality.md`** - Static analysis, type safety, complexity,
  duplication, dead code.
- **`assessment/best-practices.md`** - Stack idioms, framework conventions, deprecated APIs.
- **`assessment/dependency-review.md`** - Freshness, vulnerabilities, licenses, lockfiles, SBOM.
- **`assessment/deployment-review.md`** - Build pipeline, release process and frequency,
  manual steps, absent-automation assessment.
- **`assessment/rollback-review.md`** - Rollback mechanism, deploy safety, versioning, recovery.
- **`assessment/maintainability-review.md`** - Modularity, coupling, code structure, technical debt.
- **`assessment/change-management.md`** - Feature flags, ADR usage, release governance.
- **`assessment/documentation-review.md`** - Documentation coverage, onboarding, transfer.
- **`assessment/nfr-review.md`** - Performance, scalability, availability, reliability, resilience.
- **`assessment/security-review.md`** - Authentication, authorization, input validation,
  OWASP risks.
- **`assessment/compliance-review.md`** - Data protection, privacy, regulatory scope, licensing.
- **`assessment/observability-review.md`** - Logging, metrics, tracing, alerting.
- **`assessment/error-handling.md`** - Exception strategy, retries, fallbacks, user-facing errors.
- **`assessment/operational-readiness.md`** - Runbooks, on-call, capacity, backups.
- **`assessment/generated-code.md`** - Code provenance, generated-artifact validation.
- **`assessment/copyright-review.md`** - Originality, license compliance, attribution.

### Conditional Assessment Files

Load these only when the subject meets the inclusion criterion in the Conditional Sections table of
`process/report-format.md`.

- **`assessment/data-flow.md`** - Data flows, trust boundaries. Include for cross-boundary systems.
- **`assessment/design-patterns.md`** - GoF/POSA pattern fitness. Include for recurring structure.
- **`assessment/threat-model.md`** - STRIDE threats. Include for a security-relevant attack surface.
- **`assessment/api-contract.md`** - API contract conformance. Include when the system has an API.
- **`assessment/skill-definition.md`** - Agent Skill spec conformance, collections, embedded skills.
- **`assessment/agent-guidance.md`** - Agent-guidance set topology. Include for guidance sets.
- **`assessment/ai-system.md`** - AI system lifecycle. Include for AI-dependent projects.
- **`assessment/standards-conformance.md`** - Project development standards conformance.
- **`assessment/api-compatibility.md`** - API compatibility. Include for libraries and packages.

## `synthesis/` - Findings And Report Assembly

- **`synthesis/risk-register.md`** - Unified risk register: `RSK-[001]` mapped to
  `FND-XXX` findings.
- **`synthesis/project-scorecard.md`** - 1-10 scorecard, rubric, scales (1-5, 1-3, star bars).
- **`synthesis/tradeoff-analysis.md`** - Trade-offs as a standalone section and embedded findings.
- **`synthesis/remediation-roadmap.md`** - Prioritized roadmap with impact-vs-effort matrix and
  the Recommended/Optional/Not recommended classification.
- **`synthesis/debt-register.md`** - `TDR-[001]` inventory (CISQ/SQALE). Include for
  structural debt.
- **`synthesis/reaudit-plan.md`** - Verification owners, sign-off gates. Include for
  P1/P2 findings.
- **`synthesis/report-comparison.md`** - Re-audit discovery, revisions, Changes, legacy names.
- **`synthesis/report-triangulation.md`** - Contradiction register and second-opinion rules
  for prior or external reports of the same subject.

## `translations/` - Report Languages

Load the matching file when the report language is not English.

Analysis runs in English and the report renders into the report language in a single pass,
per `principles/output-style.md`:

- **`translations/polish-language.md`** - Polish rendering: vocabulary, terminology, style rules.

## `references/` - Lookup Tables

Load these during intake, assessment, and report writing when the detected stack or finding
type requires them.

- **`references/stack-standards.md`** - Canonical standards and advisories per detected stack.
- **`references/cwe-analyzer.md`** - CWE-to-analyzer-rule cross-reference per ecosystem.
- **`references/dependency-manifests.md`** - Text-only manifest readers, source-derived inventory.
- **`references/census-commands.md`** - Reproducible census and counting methods.
- **`references/audit-taxonomy.md`** - Audit types, coverage statuses, methodology corpus.
- **`references/sbom-schema.md`** - Source-derived inventory report schema.
- **`references/license-compliance.md`** - License classes, copyleft, attribution, ownership checks.
- **`references/delivery-practice.md`** - DORA proxies, bus-factor rubric.
- **`references/domain-profiles.md`** - Project-nature classification and mandatory probes.
- **`references/exploitability-narrative.md`** - Attack-path narrative format and tiers.
- **`references/agent-skills.md`** - Agent Skills spec corpus and live-check baseline.
- **`references/agent-configuration.md`** - AGENTS.md, rules, plugin, MCP, guidance-set baselines.
- **`references/source-catalog.md`** - Authoritative external-source registry and corpus index.
- **`references/stacks/`** - Per-stack offline baselines, indexed in `source-catalog.md`.
- **`references/methodology/`** - Methodology digests, indexed in `source-catalog.md`.
- **`references/topics/`** - Domain digests indexed in `source-catalog.md`.

## `scripts/` - Canonical Scripts

They are report-production tooling, not analysis of the audited project. Run them from the
skill tree via `finalize-report.py --skill-root <path>`, or copy them into the audited
repository's `work/` directory under a `.tmp.` name and remove the copies when done.

- **`scripts/format-table.py`** - Canonical table formatter (Table Formatting Rules).
- **`scripts/align-comments.py`** - Plain-text `#` comment column aligner.
- **`scripts/link-glossary.py`** - Glossary body-link inserter, run before the formatter.
- **`scripts/validate-report.py`** - Mechanical report checker, `--dump-contract` emits the contract.
- **`scripts/new-report.py`** - Report skeleton generator (`--style`, `--projects`, `--params`).
- **`scripts/validate-skill.py`** - Frontmatter, disclosure, and references validator.
- **`scripts/check-references.py`** - Relative-reference integrity checker.
- **`scripts/check-contents.py`** - Contents-table versus section-heading drift checker.
- **`scripts/check-update.py`** - Skill self-update checker (git upstream).
- **`scripts/finalize-report.py`** - Runs link, format, and validate in order on a report.
- **`scripts/lint-polish.py`** - Polish report linter for calques and typography.
- **`scripts/lint-prose.py`** - Pre-assembly prose linter for report drafts.
- **`scripts/common.py`** - Shared frontmatter and reporting helpers for maintenance tools.
- **`scripts/README.md`** - Tool classes, usage, validation order, limitations.
- **`tests/`** - Focused `unittest` contract tests for the report and maintenance tools.

## Evaluation Prompts

- **`evals/evals.json`** - Behavioral regression prompts and expectations.

## Repository Files

These files govern the skill repository itself rather than audit production:

- **`AGENTS.md`** - Agent-facing entry point for repository authoring and maintenance.
- **`README.md`** - Human-facing overview, usage examples, and verification commands.
- **`docs/STYLE.md`** - Style rules for the skill's own documents.
- **`docs/MAINTENANCE.md`** - Repository structure, registration, and validation rules.
- **`docs/VERSIONING.md`** - Version numbering and release conventions.
- **`docs/CONTRIBUTING.md`** - Maintainer model and pre-merge validation expectations.
- **`docs/SECURITY.md`** - Private vulnerability reporting path and covered risks.

## Evidence And Decision Contract

Use the verification plan and evidence ledger in `process/audit-workflow.md` for every audit
and every review. The audit never builds, tests, or executes the project; under the
`executed-readonly` evidence mode it may additionally run commissioned non-mutating analyzers,
recorded in the Executed Evidence Log.

All evidence comes from inspected repository contents: source, configuration, build scripts,
documentation, and committed artifacts.

Record documented but unrun checks and their effect on confidence rather than treating a
source-only review as verified production readiness. Keep evidence basis, confidence, category
status, vulnerability severity, and business risk distinct.

For security findings, use the CWE/CVSS and control-verification guidance in
`assessment/security-review.md`. For full audits of executable projects, load
`assessment/testing-review.md` and `assessment/dependency-review.md` for stack-aware
verification, SBOM, and license review. For technical due diligence, also load
`assessment/operational-readiness.md`, `assessment/documentation-review.md`,
`assessment/compliance-review.md`, and `synthesis/remediation-roadmap.md` for continuity,
cost, data lifecycle, and roadmap evidence.

Use `synthesis/project-scorecard.md` for the ISO/IEC 25010:2023 crosswalk without changing Lens
scores into purported ISO ratings. Treat unknown authorship as unknown, using
`assessment/generated-code.md`, not style heuristics. Validate summaries against evidence and
run the regression scenarios in `process/audit-workflow.md` when maintaining the skill.

## Navigation Rules

- Always apply `principles/evaluation-rules.md` and `principles/output-style.md` to every report.
- The audit report is the default deliverable. Produce the review report per
  `process/review-report.md` only on an explicit review, amendment, or improvement-plan request.
- Never compile, build, test, or execute the audited project, and never run linters, scanners,
  or generators against it. Under `executed-readonly` only the commissioned non-mutating
  analyzers run. Verification claims rest on inspected repository contents,
  documented results are `Reported` evidence.
- Assemble the audit report skeleton from `process/report-format.md` and its section files before
  filling in findings, present every section as a table and use unnumbered headings.
- Every audit report opens with the Audit Type Coverage table built from the fixed
  types and statuses in `references/audit-taxonomy.md`, kept consistent with Scope Exclusions.
- Every finding and every Evidence Ledger row carries a `Type` tag: `Observation` for an
  independently re-derivable fact, `Concern` for a risk judgment built on observations.
- The generated report follows the skill's Markdown rules adapted by `process/report-format.md`:
  `#`/`##`/`###` headings only, one-sentence paragraphs, wrap at a selectable width (default 100),
  no semicolons, tables aligned by a formatting script, no Contents table.
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
- Code provenance and generated-artifact validation belong in `assessment/generated-code.md`,
  concrete quality defects remain in their technical categories regardless of origin.
- Code originality, license compliance, and attribution belong in `assessment/copyright-review.md`.
- Data flow modeling and trust boundaries belong in `assessment/data-flow.md`, STRIDE threat
  enumeration belongs in `assessment/threat-model.md` and depends on the data flow model,
  control-level security review belongs in `assessment/security-review.md`.
- Concrete design pattern identification and fitness belong in `assessment/design-patterns.md`, keep
  it distinct from the SOLID principles in `assessment/design-principles.md`.
- API specification conformance and the OWASP API Security Top 10 belong in
  `assessment/api-contract.md`, ADR gap assessment belongs in `assessment/change-management.md`.
- Agent Skills specification conformance belongs in `assessment/skill-definition.md` when the
  subject holds `SKILL.md` files or agent-facing artifacts, with `references/agent-skills.md`
  and `references/agent-configuration.md` as baselines. Intake classifies each discovered
  skill as authored, installed, or undetermined. Installed skills are not audit subjects.
- Agent-guidance set topology - entry routes, index of record, topic owners, role resolution -
  belongs in `assessment/agent-guidance.md` for a structured guidance set. Per-artifact format
  conformance stays with `assessment/skill-definition.md`.
- Standards conformance belongs in `assessment/standards-conformance.md`, only for documented
  development standards. References lists every external source consulted.
- Canonical stack references are re-derived from `references/stack-standards.md` during intake
  and cited in Auditing Methodology and References, never copied verbatim from a prior report.
- Every CWE-classified security finding names its equivalent static analyzer rule from
  `references/cwe-analyzer.md` or states none exists. The lookup never implies an analyzer ran.
- Source-derived dependency inventories follow `references/dependency-manifests.md` (manifests
  and lockfiles read as text) and render per `references/sbom-schema.md` with underivable
  fields `Unknown`, never an executed or shipped-artifact SBOM.
- The License Compliance Review follows `references/license-compliance.md` and
  separates observed license facts from inferred concerns without legal conclusions.
- The Delivery Practice & Team Continuity section follows `references/delivery-practice.md`:
  five DORA metrics with labeled source-derived proxies, telemetry-dependent metrics
  `NOT SPECIFIED`, and a bus-factor rating.
- Every `HIGH`/`CRITICAL` Security & Compliance finding carries an `Exploitability` field per
  `references/exploitability-narrative.md`: `Theoretical` tier by default, never a claim that
  exploitation occurred.
- API compatibility gates, versioning consistency, and breaking-change tracking belong in
  `assessment/api-compatibility.md`, only for a reusable library or package.
- An overall score always reports the lowest-scoring applicable dimension beside it, per
  `synthesis/project-scorecard.md`.
- Conditional sections appear only when their inclusion criterion is met per the table in
  `process/report-format.md`, with omissions noted in Scope Exclusions - never force one.
- The Technical Debt Register (`synthesis/debt-register.md`) is distinct from the Unified Risk
  Register: debt is cost already present, risk is what could go wrong. Never duplicate entries.
- The Re-audit And Follow-up Plan (`synthesis/reaudit-plan.md`) precedes Validation Record and
  maps P1/P2 findings to verification owners and closure evidence.
- Every absent-capability finding carries an `Absence` field built from repository signals per
  `principles/evaluation-rules.md`, never a claim about the authors' motives.
- Recommendation Classification (`synthesis/remediation-roadmap.md`) classes every `REC-XXX`,
  omitted at Brief with a Scope Exclusions note.
- The Changes Since Previous Audit section (`synthesis/report-comparison.md`) appears only
  when a previous report exists - never overwritten, the new file carries the next revision.
- `report-style: hunt` or `check` renders the same evidence base per
  `process/report-format/hunt-style.md`/`check-style.md` - intake records the snapshot,
  external reports reconcile per `synthesis/report-triangulation.md`.
- Limitations and Unknowns lists every unperformed check. Validation Record closes the report
  with the Mandatory Core Checklist result and the `process/report-parity.md` gate outcome.
- Multi-project reports: a condensed combined Executive Summary and Changes follow the
  Project Inventory, combined Trade-off Analysis holds only cross-project trade-offs.
- Each `translations/` file defines one report language, loaded only when needed.
- Prefer the narrowest assessment file matching the request: a single-dimension request loads
  that one file plus `principles/` and produces the matching finding pillar and risk row only.
- Trade-offs appear in Trade-off Analysis after Architectural Assessment and embedded in
  findings, per `synthesis/tradeoff-analysis.md`.
- For a full audit, load `principles/`, `process/`, every relevant `assessment/` file, and all
  `synthesis/` files. Mark inapplicable categories `N/A` with justification rather than dropping
  them.
