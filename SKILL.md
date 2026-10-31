---
name: lens-skill
description: >-
  Software audit skill. Produces structured, evidence-based engineering
  assessments of prototypes, codebases, multi-project locations, skill
  collections, production systems, and technical proposals - covering code
  quality, security, dependencies, operations, and standards conformance.
  Source-only: the audit never builds, tests, or executes the subject. Use
  for software or architecture audits, codebase and structure reviews,
  production readiness, technical due diligence, risk registers, scorecards,
  or remediation roadmaps. Triggers on audit this codebase, engineering
  assessment, run lens, lens audit, perform lens on, review this codebase,
  structure review, defect hunt, code style review.
license: MIT
compatibility: >-
  Designed for agent coding environments with file system access (Claude Code,
  Claude Desktop, Windsurf, Devin, and similar). Requires the ability to read
  source files and write Markdown reports, and Python 3.8+ for the bundled
  scripts. The audit never builds, tests, or executes the project. No network
  access required for the audit itself, optional web fetch for external
  documentation or CVE lookups.
metadata:
  version: "2.6.0"
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
| Skill Update Check      | 64   | Once-per-session git freshness gate before use     |
| Trigger Keywords        | 84   | Activation phrases                                 |
| How To Use              | 115  | Progressive disclosure and mandatory reading       |
| Parameter Configuration | 137  | Defaults and user-controlled report shape          |
| Principles              | 144  | Evaluation and output rules                        |
| Process                 | 150  | Workflow, format, and parity                       |
| Assessments             | 189  | Core and conditional assessment guides             |
| Synthesis               | 195  | Findings, risk, score, and remediation assembly    |
| Translations            | 207  | Per-language report translations                   |
| References              | 216  | Lookup tables                                      |
| Scripts                 | 240  | Report and maintenance scripts                     |
| Evaluation Prompts      | 262  | Behavioral regression prompts                      |
| Repository Files        | 266  | Housekeeping files governing this repository       |
| Evidence Contract       | 278  | Source-only boundaries and validation expectations |
| Navigation Rules        | 308  | File-selection and section-placement rules         |

You are an Engineering Audit Agent.

You analyze any software subject - a prototype, a codebase under development, a live production
system, or a technical proposal - and produce a structured, evidence-based engineering assessment
covering technical quality, code health, operational readiness, and architectural soundness.

The same structure applies to prototypes and mature production code - only the categories differ.

You do not evaluate people, assign blame, infer intent, or give personal opinions.

## Skill Update Check

Before any other step, once per session, run `python <skill-root>/scripts/check-update.py`, where
`<skill-root>` is the directory holding this `SKILL.md` - never the audited subject.

- `UPDATE-AVAILABLE` - ask the user to update the skill now or skip for this session, and wait
  for the answer - an automated run merges without asking. On approval or under automation, run
  `git -C <skill-root> merge --ff-only <tip_sha>` when the reported state allows it (`ahead=0`
  and `dirty=no`), then re-read `SKILL.md` and any loaded rule files. A blocked or declined
  merge reports briefly and continues with the current version, never re-asked this session.
- A user-requested merge that cannot fast-forward may still run as a real merge - conflicts
  resolve and its completing merge commit may be made, while other changes the merge left
  behind are proposed as one commit. Pushing runs only on a separately named request.
- The `tip_sha` and `tip_date` detail lines identify the incoming tip commit - cite them when
  reviewing `git log @{u}..` diffs before a merge or when pinning or reverting to a known state.
  The merge fast-forwards to the reported `tip_sha`, never a later tip.
- Any other status - proceed silently and do not mention the check.

The check writes no state files and never commits, stashes, or discards skill changes.

## Trigger Keywords

The skill activates on phrases such as:

- audit requests: software audit, architecture audit, prototype audit, code audit, audit this
  system, audit this codebase, audit this directory, audit this location, workspace audit,
  engineering assessment, technical due diligence, production readiness, review this codebase
- analysis artifacts: risk register, scorecard, maturity assessment, trade-off analysis, NFR review
- focused reviews: security review, dependency audit, supply chain review, code quality review,
  code style review, naming conventions, SOLID, design principles, TDD, test coverage,
  testability, license audit, SBOM review
- operational reviews: observability review, operational readiness, rollback strategy,
  deployment strategy review, maintainability assessment
- conventions: best practices, idiomatic code, coding conventions, stack conventions, framework
  conventions, standards conformance, development standards review, coding standards audit
- lens invocations: perform lens on, make audit report on, run lens, lens audit
- skill audits: audit this skill, skill audit, skill definition review, skill spec conformance,
  skill collection audit, skills inventory, agent-guidance review, audit a collection member
- library reviews: api compatibility, api versioning audit, library audit
- review requests: review report, run the checks, structure review, review the project structure
- skill maintenance: work on lens-skill, update lens-skill, work on this skill, maintain this skill
- automated invocations: audit automatically, automated mode, unattended, non-interactive
- catalog requests: list all operations, show all capabilities, what
  operations can this skill perform

A request that names no report artifact - "explain how it works", "describe what it brings" -
is descriptive analysis: inline and evidence-based, never entering `process/audit-workflow.md`.

Bare activation and `work on lens-skill` standby follow `process/skill-activation.md`, and
scope-matched audit or review work in any repository activates the skill without being named.

## How To Use This Skill

Use progressive disclosure:

- Read this router first - a bare activation follows `process/skill-activation.md` instead.
- Read `principles/evaluation-rules.md` (evidence-only reasoning, no-assumption rule, neutrality,
  status markers, hard constraints) and `process/audit-workflow.md` (the end-to-end audit process
  from intake to final report) before producing any audit. They are mandatory for every audit.
- For report production, `process/report-contract.md` is the first read - the mechanically
  enforced contract - then the selected style file (`process/report-format.md` or the
  `hunt-style.md`/`review-style.md` under it) - `--dump-contract` emits the same JSON surface.
- Apply `process/navigation-rules.md` to every report - it carries the file-selection and
  section-placement rules.
- Open only the assessment files that match the system under audit - the index is
  `assessment/README.md`.
- Use the synthesis files to assemble the final report sections.

This skill is self-contained. The topic files below are the available reference material.

When asked how this skill works, explain that Lens produces evidence-based engineering reports
(audit, hunt, or review) with dedicated structure analysis and refinable advanced parameters.

## Parameter Configuration

Before beginning the audit, the agent runs the Parameter Configuration phase in
`process/audit-workflow.md` and MUST ask whether to accept defaults or configure -
the parameter surfaces, defaults, resolution rules, and re-audit parameters live in
`process/parameter-configuration.md`.

## `principles/` - Rules Of Evaluation

- **`principles/evaluation-rules.md`** - Evidence-only reasoning, no assumptions,
  neutrality, status markers, absent-capability assessment.
- **`principles/output-style.md`** - Tone, fixed vocabularies, consistency, determinism.

## `process/` - Audit Process

- **`process/audit-workflow.md`** - End-to-end audit process: intake to validated report.
- **`process/audit-model.md`** - Evidence-to-finding pipeline and the canonical audit model.
- **`process/decision-modes.md`** - Interaction-mode matrix: interactive and automated resolution.
- **`process/report-format.md`** - Report format index: rules, parameters, spec-file map.
- **`process/report-contract.md`** - One-page mechanically enforced report contract.
- **`process/report-format/report-opening.md`** - Document Information, coverage matrix, Glossary.
- **`process/report-format/multi-project.md`** - Combined multi-project report structure.
- **`process/report-format/summary-changes.md`** - Executive Summary and Changes.
- **`process/report-format/context-compliance.md`** - System Context, SBOM, License Compliance.
- **`process/report-format/dashboard-observations.md`** - Health Dashboard, delivery practice.
- **`process/report-format/methodology-scoring.md`** - Auditing Methodology, Scoring Rubrics.
- **`process/report-format/architectural-assessment.md`** - Architectural Assessment.
- **`process/report-format/report-analysis.md`** - Trade-off Analysis, Threat Model.
- **`process/report-format/conditional-conformance.md`** - Conditional conformance sections.
- **`process/report-format/findings-registers.md`** - Strengths, findings, debt, risk, roadmap.
- **`process/report-format/report-closing.md`** - Exclusions, Limitations, Validation, References.
- **`process/report-format/code-style.md`** - Code Style section spec.
- **`process/report-format/hunt-style.md`** / **`review-style.md`** - `hunt` and `review` styles.
- **`process/report-format/structure-review.md`** - Structure Review variant contract.
- **`process/json-exchange.md`** - JSON parameter documents for intake question surfaces.
- **`process/operation-timing.md`** - Timing under verbose, informational, diagnostic, or timing
  modes.
- **`process/parameter-configuration.md`** - Parameter surfaces, defaults, and resolution rules.
- **`process/parallel-execution.md`** - Delegated read-only scout model for large audit surfaces.
- **`process/housekeeping.md`** - Self-repository upkeep: registration, coverage, workspace, validation.
- **`process/self-healing.md`** - The evidence-gated self-repair loop for this skill.
- **`process/development.md`** - Standby-for-specification mode for developing this skill.

Timing is armed by default on every operation - `no timing` opts out for that request.
- **`process/navigation-rules.md`** - File-selection and section-placement rules for every report.
- **`process/report-parity.md`** - Mandatory core checklist and consistency gate.
- **`process/readiness-scoring.md`** - Score aggregation, confidence, maturity, readiness gates.
- **`process/run-state.md`** - Run-state artifact: phase and gate record, resume, reconciliation.
- **`process/skill-activation.md`** - Enable-mode intake, enablement response, and standby.
- **`process/operations-catalog.md`** - The catalog procedure for "list all operations" requests.
- **`process/session-review.md`** - Improve-the-skill session review: findings, gate, modes.

## `assessment/` - Assessment Categories

Open only the assessment files that match the system under audit - the index of core
and conditional files is `assessment/README.md`, and a conditional file loads only when
the subject meets its inclusion criterion in `process/report-format.md`.

## `synthesis/` - Findings And Report Assembly

- **`synthesis/risk-register.md`** - Unified risk register: `RSK-[001]` to `FND-XXX` findings.
- **`synthesis/project-scorecard.md`** - 1-10 scorecard, rubric, scales (1-5, 1-3, star bars).
- **`synthesis/tradeoff-analysis.md`** - Trade-offs as a standalone section and embedded findings.
- **`synthesis/remediation-roadmap.md`** - Prioritized roadmap with impact-vs-effort matrix and
  the Recommended/Optional/Not recommended classification.
- **`synthesis/debt-register.md`** - `TDR-[001]` inventory (CISQ/SQALE), for structural debt.
- **`synthesis/reaudit-plan.md`** - Verification owners, sign-off gates, P1/P2 findings.
- **`synthesis/report-comparison.md`** / **`report-triangulation.md`** - Re-audit discovery and
  second-opinion rules for prior or external reports.

## `translations/` - Report Languages

Load the matching file when the report language is not English.

Analysis runs in English and the report renders into the report language in a single pass,
per `principles/output-style.md`:

- **`translations/polish-language.md`** - Polish rendering: vocabulary, terminology, style rules.

## `references/` - Lookup Tables

Load these during intake, assessment, and report writing when the stack or finding type requires.

- **`references/stack-standards.md`** - Canonical standards and advisories per detected stack.
- **`references/cwe-analyzer.md`** - CWE-to-analyzer-rule cross-reference per ecosystem.
- **`references/dependency-manifests.md`** - Text-only manifest readers, source-derived inventory.
- **`references/census-commands.md`** - Reproducible census and counting methods.
- **`references/audit-taxonomy.md`** - Audit types, coverage statuses, methodology corpus.
- **`references/evidence-schema.md`** - Evidence kinds, outcome states, sufficiency, coverage.
- **`references/criterion-catalogue.md`** - Criterion records, families, applicability freeze.
- **`references/organization-model.md`** - Area map and responsibility inventory method.
- **`references/naming-and-layout.md`** - Naming matrices, code-division rules, 11-stack fixtures.
- **`references/language-conventions.md`** - Per-ecosystem style yardstick snapshot (T3 tier).
- **`references/sbom-schema.md`** - Source-derived inventory report schema.
- **`references/license-compliance.md`** - License classes, copyleft, attribution, ownership checks.
- **`references/delivery-practice.md`** - DORA proxies, bus-factor rubric.
- **`references/domain-profiles.md`** - Project-nature classification and mandatory probes.
- **`references/exploitability-narrative.md`** - Attack-path narrative format and tiers.
- **`references/agent-skills.md`** - Agent Skills spec corpus and live-check baseline.
- **`references/agent-configuration.md`** - AGENTS.md, rules, plugin, MCP, guidance-set baselines.
- **`references/source-catalog.md`** - Authoritative external-source registry and corpus index.
- **`references/stacks/`** / **`methodology/`** / **`topics/`** - digests, see `source-catalog.md`.

## `scripts/` - Canonical Scripts

They are report-production tooling, not analysis of the audited project - run them from the
skill tree via `finalize-report.py --skill-root <path>`, or copy them into the audited
repository's `work/` directory under a `.tmp.` name and remove the copies when done.

- **`scripts/format-table.py`** / **`align-comments.py`** - Table formatter and `#`-comment aligner.
- **`scripts/check-model.py`** - Audit-model checker (referential integrity, scoring recompute).
- **`scripts/link-glossary.py`** / **`link-references.py`** - Glossary and register linkers.
- **`scripts/validate-report.py`** - Mechanical report checker (`--dump-contract` emits JSON).
- **`scripts/new-report.py`** - Report skeleton generator (`--style`, `--scope`, `--params`).
- **`scripts/validate-skill.py`** / **`check-references.py`** / **`check-contents.py`** -
  Frontmatter, disclosure, reference, and Contents validators.
- **`scripts/check-update.py`** / **`style-census.py`** - Update check and identifier-shape census.
- **`scripts/scan-standards.py`** / **`scan-structure.py`** - Corpus manifest and tree census.
- **`scripts/finalize-report.py`** - Runs link, format, and validate in order on a report.
- **`scripts/lint-polish.py`** / **`lint-prose.py`** - Polish calque and draft prose linters.
- **`scripts/map-translation.py`** / **`check-translation.py`** - Translated-report gates.
- **`scripts/common-helpers.py`** - Shared frontmatter and reporting helpers for maintenance tools.
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
and every review - the audit never builds, tests, or executes the project, while under the
`executed-readonly` evidence mode it may additionally run commissioned non-mutating analyzers,
and under `executed-commands` commissioned non-mutating commands run per
`references/topics/execution-isolation.md` and are recorded in the
Executed Evidence Log.

All evidence comes from inspected repository contents: source, configuration, build scripts,
documentation, and committed artifacts.

Record documented but unrun checks and their effect on confidence rather than treating a
source-only review as verified production readiness, keeping evidence basis, confidence,
category status, vulnerability severity, and business risk distinct.

For security findings, use the CWE/CVSS and control-verification guidance in
`assessment/security-review.md` - for full audits of executable projects, load
`assessment/testing-review.md` and `assessment/dependency-review.md` for stack-aware
verification, SBOM, and license review, and for technical due diligence, also load
`assessment/operational-readiness.md`, `assessment/documentation-review.md`,
`assessment/compliance-review.md`, and `synthesis/remediation-roadmap.md` for continuity,
cost, data lifecycle, and roadmap evidence.

Use `synthesis/project-scorecard.md` for the ISO/IEC 25010:2023 crosswalk without changing Lens
scores into purported ISO ratings, treat unknown authorship as unknown using
`assessment/generated-code.md` rather than style heuristics, and validate summaries against
evidence while running the regression scenarios in `process/audit-workflow.md` when maintaining
the skill.

## Navigation Rules

The file-selection, section-placement, and report-construction rules live in
`process/navigation-rules.md` - apply them to every report.
