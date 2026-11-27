---
name: lens-skill
description: >-
  Audit software and produce evidence-based engineering reviews, findings, risk registers,
  or remediation roadmaps. Use for code quality, security, dependencies, readiness, standards,
  or project structure. Defaults to source inspection.
license: MIT
compatibility: >-
  Requires access to source files and the ability to write Markdown reports.
  Python 3.10+ is used for bundled tools. External sources and upstream checks require network access.
metadata:
  version: "3.1.4"
  author: Filip Golewski
---

# Software Audit Skill

> **Type:** Root router and taxonomy

> **Purpose:** Route software audit requests to the relevant procedure and require
> evidence for findings.

## Task Entry

| Request                             | First step                                                                                                        |
|-------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| Bare activation                     | Follow [activation](process/skill-activation.md) and wait for a task.                                             |
| List capabilities                   | Read the [operations catalog](process/operation-catalog.md).                                                     |
| Perform a task                      | Choose the operation under [Operations](#operations).                                                             |
| Develop this skill                  | Follow [development](process/skill-development.md) and the [repository instructions](AGENTS.md).                  |
| Improvement mode                    | Apply lessons from the work through this skill's maintenance rules.                                               |
| Training mode                       | Apply on-the-fly adjustments through this skill's maintenance rules.                                              |
| Review a session                    | Follow [session review](process/session-review.md).                                                               |
| Verbose reporting                   | Follow [timing](process/operation-timing.md) and [JSON exchange](process/json-exchange.md) for pending questions. |
| Update this skill or check upstream | Follow [Skill Update Check](#skill-update-check).                                                                 |

Resolve the operation and target first.
Read the selected procedure and its required resources as each phase begins.
Consult directory indexes to locate an unspecified resource.
Use the target repository's instructions for its artifacts.

Run a procedure's documented commands and check the results.
Read script source when reviewing, modifying, or diagnosing the script.
Use the host's question mechanism when available and ask directly if the host has none.

## Operations

| Request                                                              | Read first                                                                                         |
|----------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|
| Audit software, hunt for defects, or review engineering or structure | [Audit workflow](process/audit-workflow.md) and [evaluation rules](principles/evaluation-rules.md) |
| Explain a subject or its observed engineering properties inline      | [Audit intake](process/audit-workflow/audit-intake.md), descriptive route                          |
| Reformat an existing audit report                                    | [Report reformat](process/report-reformat.md)                                                      |
| Compare or benchmark external audit reports                          | [Report benchmark](process/report-benchmark.md)                                                    |
| Prepare an audit prompt for another agent                            | [Audit request](process/audit-request.md)                                                          |
| Produce a project history dataset                                    | [History visualisation](process/history-visualisation.md)                                          |
| Compile a dataset into a single-file history visualisation           | [Visualisation build](process/visualisation-build.md)                                              |
| Feed external standards into this skill                              | [Stack feed](process/stack-feed.md)                                                                |

For an audit, use the workflow's intake and parameter phase before assessing the subject.
Honor supplied parameters and the documented defaults bypass.
Read [report contract](process/report-contract.md) and [navigation](process/navigation-rules.md)
before planning a report, then open the selected style and section rules from
[report format](process/report-format.md).

## Resource Map

### `principles/` - Rules Of Evaluation

- **`principles/evaluation-rules.md`** - Evidence-only reasoning, no assumptions, neutrality,
  status markers, absent-capability assessment.
- **`principles/output-style.md`** - Tone, fixed vocabularies, consistency, determinism.

### `process/` - Audit Process

- **`process/audit-workflow.md`** - Audit workflow index: phase order, checklists, variants.
- **`process/audit-workflow/`** - Phase files mapped in the workflow index.
- **`process/report-reformat.md`** - The `reformat report` operation: mechanical pass,
  tool pipeline, and manual tail for bringing existing reports to the current contract.
- **`process/report-benchmark.md`** - External-report comparison: verification, gap attribution,
  adjustment plan feeding skill improvement.
- **`process/audit-model.md`** - Evidence-to-finding pipeline and the canonical audit model.
- **`process/audit-request.md`** - External-agent audit-request prompt generation.
- **`process/decision-modes.md`** - Interaction-mode matrix: interactive and automated resolution.
- **`process/audit-calibration.md`** - Paired-run reproducibility procedure and tolerances.
- **`process/report-format.md`** - Report format index: rules, parameters, spec-file map.
- **`process/report-contract.md`** - One-page mechanically enforced report contract.
  Use its section map to read only the specifications for included sections.
  The selected hunt, review, or structure-review style supplies its own requirements.
- **`process/json-exchange.md`** - JSON parameter documents for intake question surfaces.
- **`process/operation-timing.md`** - Timing under verbose, informational,
  diagnostic, or timing modes.
- **`process/parameter-configuration.md`** - Parameter surfaces, defaults, and resolution rules.
- **`process/parallel-execution.md`** - Delegated scout and reporter model for evidence gathering
  and per-type report generation.
- **`process/skill-housekeeping.md`** - Self-repository upkeep: registration, coverage,
  workspace, validation.
- **`process/self-healing.md`** - The evidence-gated self-repair loop for this skill.
- **`process/skill-development.md`** - Standby-for-specification mode for developing this skill.
- **`process/navigation-rules.md`** - File-selection and section-placement rules for every report.
- **`process/report-parity.md`** - Mandatory core checklist and consistency gate.
- **`process/readiness-scoring.md`** - Score aggregation, confidence, maturity, readiness gates.
- **`process/run-state.md`** - Run-state artifact: phase and gate record, resume, reconciliation.
- **`process/skill-activation.md`** - Enable-mode intake, enablement response, and standby.
- **`process/operation-catalog.md`** - The catalog procedure for "list all operations" requests.
- **`process/session-review.md`** - Improve-the-skill session review: findings, gate, modes.
- **`process/stack-feed.md`** - External standards intake into `references/` digests, gated.
- **`process/history-visualisation.md`** - The named lifecycle operation: history gathering and
  `history.json` production, run only when requested and never proposed by default.
- **`process/visualisation-build.md`** - The named build operation: packs a `history.json`
  dataset into the bundled viewer shell as one self-contained HTML visualisation,
  run only when requested and never proposed by default.

Timing is armed by default on every operation - `no timing` opts out for that request.

### `assessment/` - Assessment Categories

Open only the assessment files that match the system under audit - the index of core and conditional
files is `assessment/README.md`, and a conditional file loads only when the subject meets its
inclusion criteria in `process/report-format.md`.

### `synthesis/` - Findings And Report Assembly

- **`synthesis/risk-register.md`** - Unified risk register: `RSK-[001]` to `FND-XXX` findings.
- **`synthesis/project-scorecard.md`** - 1-10 scorecard, rubric, scales (1-5, 1-3, star bars).
- **`synthesis/solution-comparison.md`** - Trade-offs as a standalone section and embedded findings.
- **`synthesis/remediation-roadmap.md`** - Prioritized roadmap with impact-vs-effort matrix and
  the Recommended/Optional/Not recommended classification.
- **`synthesis/debt-register.md`** - `TDR-[001]` inventory (CISQ/SQALE), for structural debt.
- **`synthesis/reaudit-plan.md`** - Verification owners, sign-off gates, P1/P2 findings.
- **`synthesis/report-comparison.md`** / **`report-triangulation.md`** - Re-audit discovery and
  second-opinion rules for prior or external reports.

### `translations/` - Report Languages

Load the matching file when the report language is not English.

Analysis runs in English and the report renders into the report language in a single pass,
per `principles/output-style.md`:

- **`translations/polish-language.md`** - Polish rendering: vocabulary, terminology, style rules.
  Large file - read the vocabulary and style sections first,
  then resolve each section block by heading as the report emits it.

### `references/` - Lookup Tables

Load these during intake, assessment, and report writing when the stack or finding type requires.

- **`references/stack-standards.md`** - Canonical standards and advisories per detected stack.
- **`references/cwe-analyzer.md`** - CWE-to-analyzer-rule cross-reference per ecosystem.
- **`references/dependency-manifests.md`** - Text-only manifest readers, source-derived inventory.
- **`references/census-commands.md`** - Reproducible census and counting methods.
- **`references/check-surface.md`** - Declared check-surface census, commission proposal,
  scope-bounded claims, verification passes.
- **`references/audit-taxonomy.md`** - Audit types, coverage statuses, methodology corpus.
- **`references/evidence-schema.md`** - Evidence kinds, outcome states, sufficiency, coverage.
- **`references/criteria-catalogue.md`** - Criteria records, families, applicability freeze.
- **`references/criteria-catalogue.json`** - Fixed scoring-policy-3 criteria catalogue (levels,
  dimension order/tiers, criteria weights, severity anchors).
- **`references/organization-model.md`** - Area map and responsibility inventory method.
- **`references/naming-and-layout.md`** - Naming matrices, code-division rules, 11-stack fixtures
  - load only the matrix matching the detected stack.
- **`references/language-conventions.md`** - Per-ecosystem style yardstick snapshot (T3 tier).
- **`references/sbom-schema.md`** - Source-derived inventory report schema.
- **`references/history-schema.md`** - Canonical `history.json` field contract for lifecycle datasets.
- **`references/license-compliance.md`** - License classes, copyleft, attribution, ownership checks.
- **`references/delivery-checklist.md`** - Authored-side delivery checklist and gate contract.
- **`references/delivery-practice.md`** - DORA proxies, bus-factor rubric.
- **`references/domain-profiles.md`** - Project-nature classification and mandatory probes.
- **`references/exploitability-narrative.md`** - Attack-path narrative format and tiers.
- **`references/agent-skills.md`** - Agent Skills spec corpus and live-check baseline.
- **`references/agent-configuration.md`** - AGENTS.md, rules, plugin, MCP, guidance-set baselines.
- **`references/source-catalog.md`** - Authoritative external-source registry and corpus index -
  grep the catalog row needed rather than loading it whole.
- **`references/stacks/`** / **`methodology/`** / **`topics/`** - digests, see `source-catalog.md`.

### `assets/` - Bundled Applications

- **`assets/visualisation-shell.html`** - The bundled single-file visualisation viewer shell,
  carrying a dataset anchor the visualisation build replaces with the packed
  `window.HISTORY_DATA` payload - data-free viewer code, refreshed wholesale
  per `docs/MAINTENANCE.md`.

### `scripts/` - Canonical Scripts

They are report-production tooling, not analysis of the audited project - run them from the skill
tree via `finalize-report.py --skill-root <path>`,
or copy them into the audited repository's `work/` directory under a `.tmp.` name and remove
the copies when done.

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

Use the verification plan and evidence ledger in `process/audit-workflow/evidence-gathering.md` for
every audit and every review - the audit never builds, tests, or executes the project,
while under the `executed-readonly` evidence mode it may additionally run commissioned non-mutating
analyzers, and under `executed-commands` commissioned non-mutating commands run per
`references/topics/execution-isolation.md` and are recorded in the Executed Evidence.

All evidence comes from inspected repository contents: source, configuration, build scripts,
documentation, and committed artifacts.

Record documented but unrun checks and their effect on confidence rather than treating a source-only
review as verified production readiness, keeping evidence basis, confidence, category status,
vulnerability severity, and business risk distinct.

For security findings, use the CWE/CVSS and control-verification guidance in
`assessment/security-review.md` - for full audits of executable projects,
load `assessment/testing-review.md` and `assessment/dependency-review.md` for stack-aware
verification, SBOM, and license review, and for technical due diligence,
also load `assessment/operational-readiness.md`, `assessment/documentation-review.md`,
`assessment/compliance-review.md`, and `synthesis/remediation-roadmap.md` for continuity, cost,
data lifecycle, and roadmap evidence.

Use `synthesis/project-scorecard.md` for the ISO/IEC 25010:2023 crosswalk without changing Lens
scores into purported ISO ratings, treat unknown authorship as unknown using
`assessment/generated-code.md` rather than style heuristics,
and validate summaries against evidence while running the regression scenarios in
`process/audit-workflow/regression-scenarios.md` when maintaining the skill.

## Navigation Rules

The file-selection, section-placement, and report-construction rules live in
`process/navigation-rules.md` - apply them to every report.

## Skill Update Check

Run the check once per session when the request names `improvement`, `development`, or
`training` as a working mode, or makes an explicit `update` or upstream-check request -
on the bare `use` that carries the mode or on the mode-carrying task.
Reuse a check already attempted for this exact checkout in the session, unless the user
explicitly requests another one. Record the attempted checkout and result in session state.
Catalog queries and requests naming no mode use the installed package.

Use the directory containing this `SKILL.md`. Verify that it is the root of its own Git checkout
before running `python <skill-root>/scripts/check-update.py` with the available Python 3 launcher.
If Git, an upstream, or authorized network access is unavailable, use the installed package.
Report the limitation on an explicit request.

For `UPDATE-AVAILABLE`, report the incoming `tip_sha`, `tip_date`, and working-tree state.
After the user approves the reported update, run `git -C <skill-root> merge --ff-only <tip_sha>`
only if `ahead=0` and `dirty=no`, then re-read this entry point and the active procedures.
If the check or merge cannot run, report it for the requested maintenance operation and use the
installed files. A separately requested merge or push follows repository rules.

The check may update remote-tracking refs but leaves the working tree intact.
Review incoming changes if the upstream is uncertain.
