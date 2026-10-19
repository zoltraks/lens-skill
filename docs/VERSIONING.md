# Skill Versioning Policy

## Purpose

> **Scope:** Version numbering, rollover rules, release anchoring, and terminology for the Lens
> skill
> **Key items:** three-part decimal format, rollover at 9, commit-anchored releases, skill version
> versus report revision

This document defines the versioning rules for the `lens-skill` Agent Skill.

## Format

Versions use a three-part decimal format: `<major>.<minor>.<patch>`.

- `patch` - the least significant component, which every release increments
- `minor` - advances only when `patch` rolls over at 9
- `major` - advances only when `minor` rolls over at 9

There is no qualitative weight classification: the kind of change never selects the
incremented component.

## Increment Rules

1. **Increment patch by 1** for every release, whatever the change contains -
   corrections, refinements, additive features, or structural changes.

2. **Patch rolls over at 9**. When patch would reach 10, increment minor by 1 and
   reset patch to 0.

3. **Minor rolls over at 9**. When minor would reach 10, increment major by 1 and
   reset minor and patch to 0.

   | Before  | After   | Reason         |
   |---------|---------|----------------|
   | 0.8.0   | 0.8.1   | patch + 1      |
   | 0.8.9   | 0.9.0   | patch rollover |
   | 0.9.9   | 1.0.0   | minor rollover |
   | 1.9.9   | 2.0.0   | minor rollover |
   | 9.9.9   | 10.0.0  | minor rollover |

4. **Components advance only through rollover**. Minor and major numbers are never
   incremented directly and never skipped: each digit moves only when the digit below
   it rolls over at 9.

## When To Bump

Bump the version with every shipped change set. A set of edits that will be committed or
delivered together increments `patch` by 1, whatever the change contains.

Apply the increment rules above once per change set, at the point the set is complete and
validated - not once per edit and not once per file.

The version moves at most once between two commits. While the tree carries uncommitted
changes, every further edit joins the open set and keeps its already-bumped version, no
matter how many requests or edits arrive.

A second bump before the commit is always wrong, even when the new edits feel like a
separate change set - the set lands only when it is committed.

## Release Anchors

Lens does not tag releases.

The commit that bumps `metadata.version` is the release anchor. Its hash is the named state
consumers pin or revert to, since the version alone lives only in frontmatter text.

Record the bump commit's short hash in release notes or issues when a consumer needs to pin a
specific release.

## Terminology

The word `version` in this file always means the skill version recorded in `SKILL.md`
frontmatter.

Audit reports produced by the skill carry a `Report Revision`, not a version.

Inside a report, the word `version` refers to the audited software, a project, a library,
or the skill itself, which is shown as `Skill Version`.

Report revision rules live in `process/report-format/report-opening.md` and
`synthesis/report-comparison.md`.

## Where Version Is Recorded

The version lives in `SKILL.md` frontmatter under `metadata.version`:

```yaml
---
name: lens-skill
metadata:
  version: "X.Y.Z"
---
```

This follows the [Agent Skills specification](https://agentskills.io/specification) `metadata` field
convention, keeping the skill compatible with Anthropic Claude and other spec-compliant agents.
