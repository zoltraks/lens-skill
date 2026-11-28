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
  version: "3.1.8"
  author: Filip Golewski
---

# Software Audit Skill

> **Type:** Root router and taxonomy

> **Purpose:** Route software audit requests to the relevant procedure and require
> evidence for findings.

## Task Entry

| Request                        | First step                                                                                                        |
|--------------------------------|-------------------------------------------------------------------------------------------------------------------|
| Bare activation                | Follow [activation](process/skill-activation.md) and wait for a task.                                             |
| List capabilities              | Read the [operations catalog](process/operation-catalog.md).                                                      |
| Perform a task                 | Choose the operation under [Operations](#operations).                                                             |
| Develop this skill             | Follow [development](process/skill-development.md) and the [repository instructions](AGENTS.md).                  |
| Improvement mode               | Apply lessons from the work through this skill's maintenance rules.                                               |
| Training mode                  | Apply on-the-fly adjustments through this skill's maintenance rules.                                              |
| Review a session               | Follow [session review](process/session-review.md).                                                               |
| Timing or context usage        | Follow [timing](process/operation-timing.md) only.                                                                |
| Verbose or diagnostic          | Follow [timing](process/operation-timing.md) and [JSON exchange](process/json-exchange.md) for pending questions. |
| Working mode or update request | Run the [update check](process/skill-update.md) once per session.                                                 |

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
| Update a prior history visualisation from its last version           | [History visualisation](process/history-visualisation.md), Continuation section                    |
| Compile a dataset into a single-file history visualisation           | [Visualisation build](process/visualisation-build.md)                                              |
| Feed external standards into this skill                              | [Stack feed](process/stack-feed.md)                                                                |

For an audit, use the workflow's intake and parameter phase before assessing the subject.
Honor supplied parameters and the documented defaults bypass.
Read [report contract](process/report-contract.md) and [navigation](process/navigation-rules.md)
before planning a report, then open the selected style and section rules from
[report format](process/report-format.md).

## Resource Map

Each listed directory carries a `README.md` index naming its files with their load triggers -
open the index when a phase needs a file the routed procedure does not name,
never bulk-read a directory.

| Directory       | Role                         | Load                                                                                                               |
|-----------------|------------------------------|--------------------------------------------------------------------------------------------------------------------|
| `principles/`   | Rules of evaluation          | Every audit, hunt, or review - `principles/README.md`                                                              |
| `process/`      | Audit process                | The routed procedure and the phase files it names - `process/README.md`                                            |
| `assessment/`   | Assessment categories        | Only files matching the system under audit, conditional files on their inclusion criteria - `assessment/README.md` |
| `synthesis/`    | Findings and report assembly | Report assembly - `synthesis/README.md`                                                                            |
| `translations/` | Report languages             | Only when the report language is not English - `translations/README.md`                                            |
| `references/`   | Lookup tables                | Intake, assessment, and report writing when the stack or finding type requires - `references/README.md`            |
| `assets/`       | Bundled applications         | `assets/visualisation-shell.html` for the visualisation build, `assets/history-pipeline/` for the dataset run      |
| `scripts/`      | Report-production tooling    | `scripts/README.md` for tool classes, usage, and validation order                                                  |
| `tests/`        | Tool contract tests          | Skill maintenance only                                                                                             |

Timing is armed by default on every operation - `no timing` opts out for that request.

Scripts are report-production tooling, not analysis of the audited project - run them from the skill
tree via `finalize-report.py --skill-root <path>`,
or copy them into the audited repository's `work/` directory under a `.tmp.` name and remove
the copies when done.

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
