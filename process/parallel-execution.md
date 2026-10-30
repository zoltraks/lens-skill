# Parallel Execution

## Purpose

> **Scope:** Delegation model for running audit evidence gathering through parallel
> read-only scout agents when the host environment supports subagents
> **Key items:** applicability, scout roles, scout contract, merge discipline,
> provenance, sequential fallback

This file defines how a full audit's Evidence Gathering phase splits work across parallel
read-only agents for wall-clock efficiency on large audit surfaces.

It applies inside `process/audit-workflow.md` - the phase order, canonical model, and report
contract are unchanged.

## Applicability

Use parallel execution when two conditions hold.

- The audit surface is large - a multi-module repository, more than roughly 150 source
  files, or a multi-project location.
- The host agent supports delegating bounded tasks to subagents or equivalent parallel
  workers.

When either condition fails, the audit runs the sequential workflow unchanged.

Parallelism never changes what is audited - it changes only who reads the evidence.

## Scout Roles

Choose roles from the pool per audit shape, merging roles when the surface is small.

State which roles ran and why in the Auditing Methodology section.

| Role              | Focus                                                                 |
|-------------------|-----------------------------------------------------------------------|
| `file-inventory`  | Module map, entry points, generated vs hand-written code, key files   |
| `architecture`    | Layering, patterns, execution flows, data layer, module coupling      |
| `context`         | Tests and coverage, manifests, consumers, integrations, doc drift     |
| `security-trace`  | Auth paths, trust boundaries, every input-to-filesystem path          |
| `delivery`        | Git history, versioning, CI and release automation, contributor shape |

File-inventory output ranks key files with a confidence note and a one-line reason each.

Every scout reports structured text the parent can fold into `work/audit-model.json`.

## Scout Contract

Every scout prompt carries the same invariants.

- Read-only against the subject - scouts never create, write, modify, or execute
  anything, including `work/` artifacts and `work/audit-model.json`.
- The scout returns findings as text in its reply, with `file:line` evidence references
  for every claim.
- The brief scopes the search to the audit root and names the generated trees to skip -
  `target/`, `node_modules/`, build output, vendored dependencies.
- The brief repeats every active `evidence-exclusions` entry so excluded material is
  never opened, quoted, or summarized.
- The brief names the role's output shape - file lists, flows, inventories - so merges
  stay mechanical.
- The brief carries the context already resolved upstream - the frozen parameter record
  (evidence mode, scope record, exclusions), the scout role's expected focus from the
  phase table, and the canonical model path its output lands in - so a scout never
  re-derives decisions the parent already locked.

A scout that cannot finish reports partial coverage and the gap it hit - the parent
covers the gap itself rather than treating the area as audited.

## Merge Discipline

The parent agent owns synthesis.

Deduplicate file lists across scouts, ranking files mentioned by more than one scout
higher.

Keep conflicting readings as both readings with their evidence - never silently pick one.

The parent writes scout results into `work/audit-model.json` itself - the canonical
model keeps a single writer even under delegation.

When two scouts surface the same defect, the findings register carries one row with the
merged evidence references per `process/report-format/findings-registers.md`.

## Provenance

The Auditing Methodology section records that parallel scouts ran - roles used, scout
count, and any uncovered gap the parent filled directly.

A finding never cites "the scout" as evidence - the `file:line` reference is the
evidence.

## Sequential Fallback

Without subagent capability the parent performs every scout role itself in the order
the evidence demands - the role list becomes a reading checklist, not a skip list.

A partially delegated run that loses a worker mid-flight continues sequentially for the
remaining roles and records the mix in Auditing Methodology.
