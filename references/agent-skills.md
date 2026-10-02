# Agent Skills Specification Corpus

## Purpose

> **Scope:** Checkable requirements of the Agent Skills specification used as the conformance
> baseline for the Skill Definition Conformance assessment
> **Key items:** frontmatter field constraints, platform constraints, directory conventions,
> progressive disclosure, file-reference rules, skill security surface, live-check drift
> procedure

This file distills the [Agent Skills specification](https://agentskills.io/specification)
into the constraints an audit can check mechanically.

The specification site is the authoritative source.

Snapshot date: 2026-10-02.

`assessment/skill-definition.md` consumes this file.

`references/agent-configuration.md` holds the baselines for every other agent-facing
format discovered alongside `SKILL.md`, such as `AGENTS.md`, rules directories, and plugin
manifests.

When the live-check clause below applies,
record the fetched result as the baseline instead of this snapshot.

## Required Structure

A skill is a directory containing, at minimum, a `SKILL.md` file.

`SKILL.md` must contain YAML frontmatter delimited by `---` lines, followed by Markdown content.

## Frontmatter Fields

| Field           | Required | Constraints                                                            |
|-----------------|----------|------------------------------------------------------------------------|
| `name`          | Yes      | 1-64 chars, unicode lowercase alphanumerics and hyphens, no            |
|                 |          | leading/trailing or consecutive hyphens, must match the parent         |
|                 |          | directory name                                                         |
| `description`   | Yes      | 1-1024 chars, non-empty, states what the skill does and when to use it |
| `license`       | No       | License name or reference to a bundled license file                    |
| `compatibility` | No       | 1-500 chars, environment requirements                                  |
| `metadata`      | No       | Map of string keys to string values                                    |
| `allowed-tools` | No       | Space-separated string of pre-approved tools, experimental             |

## Platform Constraints

Anthropic's skill documentation at
`https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview` adds constraints
that are not in the agentskills.io specification but apply to skills targeting its products:

- `name` must not contain the reserved substrings `anthropic` or `claude`.
- `name` and `description` must not contain XML tags.
- `description` is injected into the system prompt, so it must be written in third person -
  first- or second-person phrasing disrupts skill discovery.

An audit records these as platform-constraint findings distinct from spec violations.

## Progressive Disclosure

Agents load skills in three stages: `name` and `description` at startup, the full `SKILL.md` body
on activation, and resource files on demand.

The specification recommends keeping `SKILL.md` under 500 lines and under 5,000 tokens.

Detailed material belongs in separate files that `SKILL.md` points to with when-to-load guidance.

## Directory Conventions

The specification names three conventional optional directories:

- `scripts/` - executable code the agent can run.
- `references/` - documentation loaded into context as needed.
- `assets/` - static resources such as templates, images, and data files.

A skill may contain any additional files or directories,
so a non-conventional name is a convention deviation, not a violation.

Record it and evaluate whether the layout still supports progressive disclosure.

## File References

References to other skill files use relative paths from the skill root.

Keep references one level deep from `SKILL.md` and avoid nested reference chains.

Every referenced path must resolve to an existing file.

## Description Quality

The description drives activation.

A conforming description states what the skill does and when to use it,
and carries the trigger keywords an agent would match against user requests.

A description near the 1024-character limit risks truncation in spec-compliant agents.

## Best-Practice Signals

The skill-creation guides add quality signals beyond the required format.

The Anthropic best-practices document at
`https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices` is the
authoritative source for these signals:

- Each bundled file gets explicit when-to-load guidance, not a generic "see the directory" note.
- `scripts/` entries are self-contained or document their dependencies.
- `metadata` key names are reasonably unique to avoid conflicts.
- `allowed-tools` lists only the tools the skill's procedures actually invoke.
- Skill names prefer gerund form (`processing-pdfs`, `analyzing-spreadsheets`) and avoid vague or
  generic names (`helper`, `utils`, `documents`, `data`).
- Instruction specificity matches task fragility: exact scripts for fragile low-freedom steps,
  goal-level guidance for tolerant high-freedom steps.
- Every paragraph is expected to justify its token cost - content the agent already knows is
  waste, not completeness.
- The quality floor is at least three evaluation prompts exercised against real usage, across
  the model tiers the skill targets.
- Anti-patterns the guide names: Windows-style paths, offering too many near-duplicate options,
  and unjustified "voodoo" constants in scripts.

## Skill Security Surface

The overview's security considerations define the checkable surface for an audited skill,
treating an untrusted skill like installing third-party software:

- Every bundled file is reviewed - `SKILL.md`, scripts, and resources - for unexpected network
  calls, file access outside the skill's declared scope, and operations that do not match its
  stated purpose.
- Instructions or scripts that fetch content from external URLs are a distinct risk class: the
  fetched content is mutable and unpinnable, so a trustworthy skill can turn malicious when its
  dependencies change.
- Tool invocations exceeding the `allowed-tools` declaration, and reads or writes of sensitive
  data with no stated need, are exposure findings.
- The OWASP Agentic Skills Top 10 vocabulary in `references/methodology/owasp-baselines.md`
  (AST01-AST10) anchors these finding classes; update-drift findings (AST07) pair with the
  integrity rules in `references/topics/git-integrity.md`.

## Live Check

When web fetch is available, retrieve `https://agentskills.io/specification` during the audit and
compare its headline constraints - required fields, character limits, directory conventions, and
disclosure budgets - against this snapshot.

When the fetched spec differs, record the live constraints as the conformance baseline and note
the drift in the report's Limitations and Unknowns.

When the fetch is unavailable, run the assessment against this snapshot and record the snapshot
date as the baseline in the audit's evidence.

The check is best-effort.

It must never block the audit and never executes anything against the audited subject.

## External Validation

The `skills-ref` reference library validates `SKILL.md` frontmatter and naming conventions.

A `skills-ref validate` run is execution evidence.

Record it only when a committed or supplied result exists in the repository,
and mark it `Reported` rather than `Verified`.
