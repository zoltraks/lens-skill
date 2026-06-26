# Audit Workflow

## Purpose

> **Scope:** End-to-end audit process from intake to validated report
> **Key items:** intake, scope, evidence gathering, per-category assessment, synthesis, validation

This file defines the order of operations for producing an audit. Follow it for every full audit.

For a single-dimension request, run the same steps but limit the assessment phase to the one requested category.

## Step Overview

The workflow has seven phases. Complete each phase before moving to the next.

**Intake**

Read everything the user supplied: description, code, configuration, diagrams, logs, prior reports.

Identify the artifact type: prototype, codebase under development, running production system, or written proposal.

Note the source format. Findings from a description are weaker than findings from inspected code or configuration.

Determine the natural language of the user's request. The report language must match the request language unless the user explicitly states otherwise.

**Parameter Configuration**

Before beginning the audit, ask the user whether to accept the default parameters or configure them. Present the defaults in a compact summary.

Default parameters:

| Parameter | Default Value |
|-----------|---------------|
| Report delivery | Inline (direct response) |
| Output filename | `AUDIT.md` for non-Polish reports, `AUDYT.md` for Polish reports (only used if delivery is File) |
| Report language | Match the language of the user's request |
| Detail level | Standard |
| Evaluation scale | 1-10 |
| Improvement suggestions | Include with priorities (P1-P4 roadmap) |
| Trade-off analysis | Standalone section + embedded into relevant findings |

The agent MUST ask the user and MUST NOT skip this step. The agent MUST wait for user response before proceeding to Scope Definition.

If the user accepts defaults or says "bypass", "defaults", or equivalent, proceed immediately to Scope Definition using the values above.

If the user chooses to configure, walk through the parameters one at a time. At each prompt, offer a bypass option to accept the remaining defaults and proceed.

**Parameter prompts**

Present each prompt as a single question with clear options. After each answer, confirm the choice and move to the next parameter.

**Report delivery**

Ask: "How should the report be delivered?"

- Inline (default) - return the full report as the direct response.
- File - write the report to a file inside the audited repository or directory.

If File is chosen, resolve the output location using the following rules, applied in order against the root of the repository or directory being audited:

1. If `docs/audit/` exists, inspect its contents and match the naming convention already in use there (e.g. `AUDIT.md`, `audit.md`, date-prefixed names). Use that directory and that convention as the default.
2. If `docs/audit/` does not exist but `docs/` exists, use `docs/` as the default output directory.
3. Otherwise use the root of the audited repository or directory as the default output directory.

Present the resolved default location to the user and ask: "Where should the file be written, and what should it be named?"

- Default location - accept the resolved directory and the language-appropriate default filename (`AUDIT.md` for non-Polish reports, `AUDYT.md` for Polish reports), adjusted for any naming convention found in step 1.
- Custom path - the user may supply a path relative to the audited repository or directory root (e.g. `reports/2026-06-audit.md`).

Always place the file inside the audited repository or directory. Do not write to an absolute path outside it unless the user explicitly provides one.

If the user already named a file or stated a delivery preference in the original request, honor it without asking again; still resolve the output directory using the rules above unless a full path was given.

**Report language**

The default is the language of the user's request. Ask only if the user explicitly asks for a different language.

When the report language is Polish, the default filename changes to `AUDYT.md`, all Polish diacritics must be preserved, and the report must be written in UTF-8 encoding.

**Detail level**

Ask: "What level of detail should the report include?"

- **Standard** (default) - full report with all eleven sections, complete findings, risk register, scorecard, and remediation roadmap.
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

- **Embed into findings** (default) - trade-offs are embedded into the relevant `FND-ARC-XXX` or `FND-CQ-XXX` finding blocks.
- **Omit** - do not include trade-off reasoning.

**Bypass rule**

At any parameter prompt, if the user responds with "bypass", "skip", "defaults", or equivalent, immediately accept all remaining defaults and proceed to Scope Definition.

**Scope Definition**

State what is in scope and what is not.

List the components, services, or files that were provided.

Record any constraints, goals, or target environment the user stated. Mark unstated constraints as `NOT SPECIFIED`.

Determine the maturity level claim, if any, so it can be tested against evidence later.

**Evidence Gathering**

For each relevant assessment category, collect concrete anchors: files, config keys, commands, pipeline steps, documented procedures, or direct quotes.

Respect `.gitignore` exclusions. Do not inspect files that are excluded by `.gitignore` patterns (for example, `bin/`, `obj/`, `node_modules/`, `.env` files, or build artifacts). If a `.gitignore` file is present, use it to filter the file list before analysis. If no `.gitignore` is present, explicitly note this as a gap.

Do not yet form conclusions. Separate collection from judgement to avoid confirmation bias.

Where evidence is absent, record the gap explicitly with the appropriate missing-information token.

**Category Assessment**

For each category, open the matching `assessment/` file and apply its checklist. For a full audit, this includes the two additional categories `assessment/ai-generated-code.md` and `assessment/copyrights.md`.

Assign a status (`PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`) per the rules in `principles/evaluation-rules.md`.

Record evidence, concrete risks, and neutral notes for each category.

**Synthesis**

Build the unified risk register from the risks surfaced during assessment, using `synthesis/risk-register.md`. Every risk must reference its source `FND-XXX`.

Build the project scorecard using `synthesis/scorecard.md`. Present the scoring rubric before the scores.

Draft the High-Level Observations section by selecting the top 5 most important findings from the Detailed Technical Findings. Keep each observation brief; full detail lives in the finding blocks.

Draft the Strengths & What's Working section by identifying 5-8 evidenced positive baselines from the codebase.

Surface trade-offs both as a standalone Trade-off Analysis section (using `synthesis/trade-off-analysis.md`) and embedded into relevant architectural or design findings where they directly explain a specific finding.

Draft the actionable remediation roadmap using `synthesis/recommendations.md`. Every recommendation must resolve a specific `FND-XXX`.

Add the Production Readiness Threshold paragraph to the Executive Summary, tying conditions to specific `RSK-XXX` IDs.

**Validation**

Re-check every finding against `principles/evaluation-rules.md`.

Confirm no finding rests on an assumption, that every status has evidence or a gap token, and that no language evaluates people.

Confirm every `FND-XXX` finding uses the correct pillar abbreviation and sequential numbering.

Confirm every `RSK-XXX` references its source `FND-XXX`.

Confirm every `REC-XXX` resolves a specific `FND-XXX`.

Confirm no plaintext secrets, passwords, or cryptographic keys appear in summaries, observations, or risk descriptions.

Confirm the High-Level Observations section contains at most 5 bullets and anchors each to a specific `FND-XXX`.

Confirm the Strengths & What's Working section contains 5-8 evidenced bullet points.

Confirm the Trade-off Analysis section uses the standard table format and frames each trade-off against a stated constraint.

Confirm every finding in the index table has a Remediation Status column with value `Open`.

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
| What is the natural language of the request? | Language code or name              |

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
