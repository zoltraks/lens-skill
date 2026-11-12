# Audit Request

## Purpose

> **Scope:** Generation of a self-contained agent prompt that commissions an audit elsewhere
>
> **Key items:** triggers, prompt shapes, canonical skeleton, delivery, guardrails

This file defines the operation that writes an audit-request prompt for an external agent.

Follow it when the request says "generate an audit prompt", "write an audit request",
"prompt an external agent to audit this", "produce a delegation prompt",
"create an agent prompt for an audit", or an equivalent that asks for the request itself
rather than the audit.

## When This Applies

The request asks for a prompt that commissions an audit by another agent - the deliverable is
the prompt text, not a report.

The generated prompt targets an agent that does not carry this skill.
It describes the audit's nature and quality bar without relying on any file in this repository.

A request that asks for the audit itself enters `process/audit-workflow.md` instead.

When this operation is the session's first action,
the once-per-session Skill Update Check from `SKILL.md` runs first.

## Parameters

Two surfaces resolve before emission.

| Parameter         | Type     | Options                               | Default           |
|-------------------|----------|---------------------------------------|-------------------|
| `prompt-shape`    | `choice` | Generic (recommended), Configured     | Generic           |
| `prompt-delivery` | `choice` | Inline blockquote (recommended), File | Inline blockquote |

- `Generic` emits the canonical skeleton verbatim - the prompt stays valid for any software
  project and carries no parameter lines.
- `Configured` adds a `**Parameters**` clause listing the resolved audit parameters - report
  style, detail level, evaluation scale, evidence mode, report language, and delivery path -
  resolved with the vocabulary of `process/parameter-configuration.md`,
  so the external report lands comparable to a Lens report on the same subject.
- `Inline blockquote` delivers the prompt as a quoted block for copy-paste.
- `File` writes the prompt to a named path - a `work/` scratch path or the target repository's
  own scratch convention, never a shipped location of this repository.

## Procedure

1. Resolve the prompt target - the repository or subject the external agent will audit,
   defaulting to the working repository.
2. Resolve `prompt-shape` and `prompt-delivery`,
   asking once through the host's question mechanism when the request does not name them.
3. Emit the canonical skeleton below,
   filling the parameters clause for the configured shape.
4. Deliver per `prompt-delivery` and stop - no intake classification, subject discovery,
   or audit phase runs.

## The Canonical Prompt

Emit this skeleton, keeping clause order and one requirement per bullet.

```
You are a senior software auditor. Perform a fresh, evidence-based engineering audit of the
software repository named below, and produce a written audit report as a file at the repository's
conventional location for reports. Do not modify the project's source code.

**Approach**

- Read the repository's own rule, guideline, and documentation files first, and follow any
  conventions they declare - output location, naming, versioning, language.
- Extract the project's declared requirements from its documentation and freeze them as a
  numbered requirements registry.
- Inventory the codebase mechanically - file counts by role, size hotspots,
  test-to-source ratios, dependency surface, configuration.
- Gather evidence before judging. Every claim in the report must trace to evidence - a file and
  line reference, a measured value, an executed check, or an explicit project declaration.
  Distinguish what you inspected from what you executed, measured, or inferred,
  and mark genuinely unverifiable items as unknown rather than guessing.
- If the project has runnable verification and you are permitted to run commands,
  execute them in an isolated copy of the tree, never in the working tree.
  Record each command, its exit status, and its interpretation.
  Distinguish defects of your harness from defects of the subject.

**Report nature**

- A document-information block recording the audit's identity - subject revision, date,
  toolset, scope, and evidence mode.
- An executive summary with an overall readiness verdict, explicit conditions or blockers,
  and headline scores.
- A system context and bill-of-materials section covering architecture, dependencies,
  and license compliance at census level.
- A scored assessment against a fixed set of quality dimensions - functional suitability,
  architecture, structure, code quality, testing, security, dependencies, documentation,
  delivery, and comparable categories. Use a consistent numeric scale,
  justify every score with cited evidence, and show the aggregation method.
- A requirements conformance table with exactly one row per requirement and a graded status each.
- Register sections for findings, technical debt, risks, and remediation recommendations.
  Give every entry a unique, stable, cross-referenceable identifier, a severity or priority,
  cited evidence, and concrete remediation guidance with a verification method.
  Findings and risks must map to recommendations, or carry an explicit accepted-no-action
  disposition.
- A remediation roadmap ordered by priority, and a limitations or exclusions section listing
  what the audit did not verify and why.
- A validation section or appendix showing that the report itself was checked - every register
  identifier resolves, every evidence path exists, tables and cross-references are consistent,
  and scores are internally consistent.

**Quality bar**

- The report must stand on its own for a reader who has never seen the project.
- Prefer verified claims over impressive prose. One measured fact outweighs three adjectives.
- Surface real risks honestly, including uncomfortable ones,
  with the same rigor applied to strengths.
- Before delivering, mechanically self-check the report - identifiers contiguous and defined
  once, references resolve, tables well-formed, no contradictions between summary and detail -
  and iterate until clean.

Begin now.
```

## Configured Parameters Clause

For the configured shape, insert the clause directly after the opening paragraph.

```
**Parameters**

- Report style: <audit, hunt, or review>.
- Detail level: <Brief, Standard, or Detailed>.
- Evaluation scale: <1-10, 1-5, 1-3, or Stars>.
- Evidence mode: <source-only, executed-readonly, or executed-commands as commissioned>.
- Report language: <language>.
- Target: <repository or subject name>.
- Delivery: file at <conventional report path>.
```

## Guardrails

- The generic shape never names a real project, path, stack, or identifier - session examples
  generalize the same way `docs/MAINTENANCE.md` anonymizes shipped examples.
- The prompt never instructs the external agent to commit, push, deploy,
  or modify the subject's source.
- Command execution is offered conditionally - "if permitted" - so the same prompt stays valid
  under source-only policies.
- The prompt asks for self-validation mechanics by nature,
  never naming this skill's validators, register identifiers, or contract vocabulary.
- The emitted prompt must be self-contained - an agent reading only the prompt can perform
  the work.

## What Does Not Apply

- No intake classification, subject discovery,
  or audit phase runs - the request named a generation task.
- No scan of the target runs - the prompt describes a procedure the target's reader executes.
- No parameter document emits while no surface is pending -
  under verbose the two surfaces emit per `process/json-exchange.md`.
- An emitted file is a working artifact - keep it under the target's scratch convention,
  never inside this skill's shipped tree.
