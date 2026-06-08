# Audit Workflow

## Purpose

> **Scope:** End-to-end audit process from intake to validated report
> **Key items:** intake, scope, evidence gathering, per-category assessment, synthesis, validation

This file defines the order of operations for producing an audit. Follow it for every full audit.

For a single-dimension request, run the same steps but limit the assessment phase to the one requested category.

## Step Overview

The workflow has six phases. Complete each phase before moving to the next.

**Intake**

Read everything the user supplied: description, code, configuration, diagrams, logs, prior reports.

Identify the artifact type: prototype, codebase under development, running production system, or written proposal.

Note the source format. Findings from a description are weaker than findings from inspected code or configuration.

Confirm the report destination. If the user named an output file, use it. If the user invoked an audit such as "perform lens on..." or "make audit report on..." without naming a file, ask once whether to return the report inline or write it to a file the user names, per the delivery rule in `process/report-format.md`.

**Scope Definition**

State what is in scope and what is not.

List the components, services, or files that were provided.

Record any constraints, goals, or target environment the user stated. Mark unstated constraints as `NOT SPECIFIED`.

Determine the maturity level claim, if any, so it can be tested against evidence later.

**Evidence Gathering**

For each relevant assessment category, collect concrete anchors: files, config keys, commands, pipeline steps, documented procedures, or direct quotes.

Do not yet form conclusions. Separate collection from judgement to avoid confirmation bias.

Where evidence is absent, record the gap explicitly with the appropriate missing-information token.

**Category Assessment**

For each category, open the matching `assessment/` file and apply its checklist.

Assign a status (`PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`) per the rules in `principles/evaluation-rules.md`.

Record evidence, concrete risks, and neutral notes for each category.

**Synthesis**

Build the unified risk register from the risks surfaced during assessment, using `synthesis/risk-register.md`. Every risk must reference its source `FND-XXX`.

Build the project scorecard using `synthesis/scorecard.md`. Present the scoring rubric before the scores.

Embed trade-off analyses directly into the relevant architectural or design findings. Do not produce a standalone trade-off section.

Draft the actionable remediation roadmap using `synthesis/recommendations.md`. Every recommendation must resolve a specific `FND-XXX`.

**Validation**

Re-check every finding against `principles/evaluation-rules.md`.

Confirm no finding rests on an assumption, that every status has evidence or a gap token, and that no language evaluates people.

Confirm every `FND-XXX` finding uses the correct pillar abbreviation and sequential numbering.

Confirm every `RSK-XXX` references its source `FND-XXX`.

Confirm every `REC-XXX` resolves a specific `FND-XXX`.

Confirm no plaintext secrets, passwords, or cryptographic keys appear in summaries, observations, or risk descriptions.

Confirm the report follows `process/report-format.md` section by section.

## Intake Checklist

Use this checklist to confirm you understand the input before assessing.

| Question                                   | Record As                          |
|--------------------------------------------|------------------------------------|
| What artifact type is this?                | Prototype / Codebase / Production system / Proposal |
| What is the source format?                 | Running / Inspected code / Description |
| What components were provided?             | List of components in scope        |
| What was explicitly excluded?              | Out-of-scope list                  |
| What constraints did the user state?       | Constraints, or `NOT SPECIFIED`    |
| What maturity does the user claim, if any? | Claimed maturity, or none          |
| Where should the report be delivered?      | Inline / named file, ask if unstated |

## Handling Thin Input

When the input is sparse, do not compensate by inferring.

Produce the report anyway, with most categories marked `UNKNOWN` or `INSUFFICIENT INFORMATION`.

Add a short list of the specific artifacts that would raise confidence, so the user can supply them and re-run the audit.

A thin-input audit is still useful: it shows exactly what is missing for a readiness decision.

## Single-Dimension Audits

When the user asks for only one dimension, such as "review observability":

- Still load `principles/evaluation-rules.md` and `principles/output-style.md`.
- Load only the matching `assessment/` file.
- Produce only the matching report subsection plus any risks for that dimension.
- Note that the audit was scoped to a single dimension and is not a full readiness assessment.

## Re-Audit

When re-auditing after changes, keep the same categories, statuses vocabulary, and scorecard dimensions.

Record what changed since the previous audit and which findings moved status, so progress is comparable over time.
