# Agent Guidance Conformance

## Purpose

> **Scope:** Topology and authority of a repository's agent-guidance documentation set -
> entry routes, index of record, topic ownership, role resolution, restricted directories,
> and vendored-document currency
> **Key items:** entry route, index of record, consolidated topology, owner selection,
> role resolution, restricted directories, vendored documents, execution policy

This file guides assessment of whether a repository's agent-facing guidance documents form a
coherent set: whether an agent entering at a documented entry point reaches authoritative
rules, whether exactly one document declares which documents are authoritative, and whether
declared documentation roles resolve to real paths.

`references/agent-configuration.md` Guidance Set Baselines is the conformance baseline.

This file covers set-level topology and authority only.

Per-artifact format conformance - `SKILL.md` frontmatter, `AGENTS.md` mechanics,
rules-directory frontmatter, MCP configuration shape - stays with
`assessment/skill-definition.md`.

It complements `assessment/documentation-review.md`, which owns documentation quality and
documented-claim verification for the human-facing docs.

Apply `principles/evaluation-rules.md` throughout.

Assess only what the files show.

## When This Applies

This assessment applies when the subject carries a structured agent-guidance set: a central
rules document (`GUIDELINES.md`, `RULES.md`, or an `AGENTS.md` declared in that role), a
Sources-of-Truth-style index, multiple layered instruction files routed from an entry point,
governance workflow directories (change records, plans, decision records), or a vendored
preparation or instruction document.

A lone thin `AGENTS.md` with no routed rules documents does not trigger this assessment - its
format checks belong to `assessment/skill-definition.md`.

When the subject carries no guidance set, mark the section `N/A` with a one-line justification
and note the omission in Scope Exclusions.

The baseline is a convention the repository declares, never an imposed template: absence of a
guidance structure is an observation only where repository scale makes the gap material, and
never a conformance verdict by itself.

## What To Evaluate

- **Guidance inventory**: enumerate the set - entry files, central rules documents, routed
  standards or guidelines, workflow directories, decision records, vendored documents. Every
  discovered document lands in the inventory, included or marked out of scope.
- **Entry route**: whether each documented entry file carries an explicit read-and-follow
  instruction toward authoritative rules, and whether the chain resolves without broken links,
  circular imports, or conflicting copies of the same rule.
- **Index of record**: whether exactly one document declares which documents are authoritative
  (a Sources of Truth table or equivalent). A second authority declaration - a README block
  restating rules, a parallel guidelines root - is a finding.
- **Consolidated topology**: whether a single entry file doubling as the central rules
  document records that role. Consolidation recorded as a convention conforms; unrecognized
  consolidation must not be reported as drift.
- **Owner selection**: whether workflow, testing or verification, document style, and
  versioning each resolve to exactly one recorded owning document or an explicit `N/A`. The
  same rule text duplicated across two owners is drift; an unowned topic is a gap only where
  the repository's scale warrants one.
- **Role resolution**: whether declared documentation roles - change records, plans, decision
  records, standards, references, reports, archive, templates, disposable workspace - resolve
  to paths that exist, and whether a layout map or equivalent records the mapping.
- **Restricted directories**: whether historical, report, or reference directories that must
  not be scanned for unrelated work carry an explicit read-boundary statement.
- **Content sufficiency**: whether guidance documents hold real repository-derived content.
  Boilerplate-only documents presented as authoritative are findings; documents naming
  commands or paths that do not exist are drift - the existence check itself belongs to
  `assessment/documentation-review.md`, so record the cross-reference rather than duplicating
  it.
- **Vendored-document currency**: whether a vendored instruction or preparation document
  carries a version marker, and whether that marker is older than the canonical source, making
  it a stale record.
- **Execution and approval posture**: whether the set records who may commit, integrate, bump
  versions, or select release baselines. Decisions reserved for a human are recorded as
  reserved; an implied or absent policy is a governance observation.
- **Self-improvement mechanism**: whether the set routes durable lessons somewhere - a
  memorization convention, session-review protocol, or findings appendix. Absence is a
  confidence gap, not a finding, except in large long-lived repositories.
- **Secrets indirection**: whether agent-facing documents reference secrets indirectly -
  environment variables, `secrets:`-style indirection, gitignored files - rather than
  embedding values.

## Evidence To Look For

| Signal                        | Where It Appears                                                         |
|-------------------------------|--------------------------------------------------------------------------|
| Entry files                   | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, tool-specific entry points        |
| Central rules documents       | `GUIDELINES.md`, `RULES.md`, `CONTRIBUTING.md`, consolidated `AGENTS.md` |
| Authority index               | Sources-of-Truth section, governing-documents table, read-order list     |
| Routed rules documents        | `docs/standard/`, `docs/guidelines/`, rules directories                  |
| Workflow directories          | `changes/` or `change/`, `plans/` or `plan/`, `decisions/`               |
| Layout map                    | Recorded role-to-path mapping in the central document or README          |
| Restricted-directory rules    | Read-boundary statements on archive, report, or reference directories    |
| Vendored documents            | Preparation or instruction documents carrying a `Version:` marker        |
| Disposable-workspace contract | Workspace markers, wipe scripts, resolution rules in the guidance set    |
| Execution policy              | Commit, integration, version authority statements, reserved decisions    |
| Secrets handling              | Indirection conventions - `env` references, `secrets:` keys, gitignored  |

## Status Criteria

- `PASS`: The set has a resolvable entry route, a single index of record, recorded topic
  owners, roles that resolve to real paths, and no conflicting or stale guidance.
- `PARTIAL`: The set functions but carries gaps - a second authority declaration, duplicated
  rules across owners, unrecorded consolidation, a stale vendored document, or undeclared
  restricted directories.
- `FAIL`: The entry route is broken, two documents conflict over the same rules with no
  recorded precedence, or guidance documents present boilerplate or nonexistent paths as
  authoritative.
- `UNKNOWN`: The set exists but key documents were not provided or not inspected deeply enough
  to judge.
- `N/A`: The subject carries no structured agent-guidance set - a lone thin entry file at
  most. Omit the section and note the omission in Scope Exclusions.

## Common Risks

- Parallel authority declarations let agents follow whichever copy they load first, so a rule
  change fixes one copy and leaves the other stale.
- A broken or circular entry route leaves agents without the authoritative rules while the
  repository appears documented.
- Unrecorded consolidated topology reads as drift to auditors and invites a duplicate central
  rules document that forks the conventions.
- Duplicated rule text across owners diverges silently - each copy is documented but the
  copies disagree.
- Boilerplate-only guidance documents pass file-existence checks while carrying no real
  convention.
- Vendored preparation documents age into stale instructions nobody owns.
- An unrecorded execution policy lets automation infer commit or release authority the
  maintainers never granted.

## What Raises Confidence

- A recorded layout map or Sources-of-Truth table resolving every declared role to a path.
- A single index of record referenced by every entry file.
- Explicit owner selection including recorded `N/A` entries rather than silence.
- Reserved human decisions recorded as such - commit authorship, version bumps, baseline
  selection.
- Findings-appendix or session-review conventions routing durable lessons back into the rules.
- A documented disposable-workspace convention separating scratch artifacts from durable
  records.
- Restricted directories carrying explicit read-boundary statements.

Mark each missing signal explicitly rather than inferring its presence.

Anchor every topology judgement to a specific document and a specific declared rule - a verdict
about "the documentation" without a path is not anchored.
