# Scope Definition

## Purpose

> **Scope:** The Scope Definition phase of the audit workflow - scope statement, domain profile,
> verification scope, and criteria planning **Key items:** scope, domain profile,
> verification scope, criteria planning

This file is a phase of the audit workflow indexed by `process/audit-workflow.md`.

Follow it after Parameter Configuration.

On completion, proceed to `process/audit-workflow/evidence-gathering.md`.

## Scope Definition

State what is in scope and what is not.

List the components, services, or files that were provided.

Record any constraints, goals, or target environment the user stated.

Mark unstated constraints as `Not specified`.

Determine the maturity level claim, if any, so it can be tested against evidence later.

## Domain Profile

Classify each in-scope project's nature and purpose from its manifests, entry points, protocols,
persisted data, and documentation claims, per `references/domain-profiles.md`.

Record the primary nature and any secondary natures, and load the matching probe set:
each activated probe is mandatory Evidence Gathering work,
and a skipped probe needs a recorded reason.

The domain profile also decides which documentation claims count as advertised workflows for the
journey traces in `process/audit-workflow/evidence-gathering.md`.

## Audit Purpose And Verification Scope

Record whether the decision is engineering improvement, production readiness,
or technical due diligence for acquisition, investment, or supplier review.

For due diligence, include continuity, ownership, operating cost, roadmap feasibility,
and IP/data obligations using the existing assessment categories rather than creating a
separate people score.

If business artifacts are unavailable, retain those concerns as `Unknown` and request specific
artifacts, do not present a source-only review as complete business due diligence.

Under the default `source-only` evidence mode the audit executes nothing.

It never compiles, builds, or tests the project and never runs linters, scanners,
or generators against it, tool availability cannot be assumed and executing untrusted
code is out of scope.

Analysis rests on repository contents alone: source files, configuration, build scripts,
pipeline definitions, documentation, and committed artifacts such as coverage or scan reports.

Read-only inspection commands such as file listing, search,
and version control history remain in scope.

The audit never installs tools, uploads source, changes project policies, executes builds or tests,
or accesses live systems.

Under `executed-readonly` evidence mode the agent may additionally run the non-mutating,
read-only analyzers the user explicitly commissioned,
such as dependency advisory or policy scanners.

Under `executed-commands` evidence mode the agent may additionally run the commissioned non-mutating
commands the user named - tests, builds, lint, typecheck, coverage,
isolated reproduction harnesses - while the subject is still never deployed, mutated,
or connected to live systems.

Commissioned commands follow `references/topics/execution-isolation.md`: the environment census,
isolation recipe, bounded inputs, proxy labeling, harness disclosure, failure-output mining,
and result triage apply to every executed record.

The project itself is still never run outside the commissioned set,
no tool is installed or upgraded for the audit unless commissioned,
and every executed command lands in the Executed Evidence - or the Execution Register under
`Report Style: review` - per `process/report-format/report-closing.md`.

Record the scope as `source-only`, `executed-readonly`, or `executed-commands`.

Documented or committed check results are `Reported` evidence, not audit execution.

Also record the audit-type coverage decision here:
read the canonical rows in `references/audit-taxonomy.md` and note which statuses the
engagement supports.

Under the default scope the Penetration Test, ISO/IEC 27001 Certification,
SOC 2 Attestation Examination, and interview-dependent Technical Due Diligence dimensions stay
`Not done` or `Partially`, and any explicitly lifted constraint is recorded so the Coverage Matrix
and Scope Exclusions can match it.

The matrix itself is rendered during Synthesis.

For readiness audits, identify required evidence before judging readiness:
documented build and test results, dependency manifests and lockfiles, committed scan reports,
and operational recovery documentation.

## Inventory And Classification

Enumerate every in-scope source file into the model's `inventory[]` before sampling.

`scripts/scan-structure.py <root>` produces the deterministic census - tracked files via
`git ls-files` when available, a filesystem walk otherwise - classifies each file into the inventory
classes, and emits the per-area module map that seeds `inventory[]`.

Classify each file as production code, unit or integration test, test support, generated code,
vendored code, example, or script, and record excluded and unread files with reasons,
per `references/evidence-schema.md`.

## Criteria Planning

Build the audit's criteria table from `references/criteria-catalogue.md` using the domain profile
and audit purpose, recording each criteria entry's source, applicability, criticality, weight,
method, and sufficiency rule.

Under scoring policy 3 the start point is the fixed catalogue in
`references/criteria-catalogue.json` - ids, dimensions, weights, criticality, level anchors,
and `na_rules` are declared there, so planning assigns each criteria entry its channel, outcome,
and level instead of adapting the records.

Run `scripts/extract-requirements.py <doc.md> ...` over the subject's requirement documents to
inventory requirement ids with obligation and kind hints,
then freeze the confirmed set into the model's `requirements[]` registry - the script proposes the
inventory, the auditor decides the obligations.

The registry carries normative requirement clauses only - rows the extractor classifies
`scenario` (use-case, scenario, example, or walkthrough sections) and statements the auditor
reads as contextual or aspirational are disclosed as coverage notes, never frozen into
`requirements[]` or counted in the mandatory denominator.

Every frozen registry entry records its id, obligation, kind, and spec location -
a row that cannot cite the clause it comes from is not a requirement.

Record the frozen registry's `requirements_baseline` as `check-model.py` computes it - the SHA-256
hex of the newline-joined, sorted `"<id>:<obligation>"` lines - so the scope record recomputes
instead of being transcribed.

Freeze the applicable denominator before reading favorable or unfavorable findings,
and record any later applicability change with its reason.

Render the table in the Auditing Methodology section per
`process/report-format/methodology-scoring.md`.

