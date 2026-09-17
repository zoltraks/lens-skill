# Skill Versioning Policy

This document defines the versioning rules for the `lens-skill` Agent Skill.

## Format

Versions use a two-part decimal format: `<major>.<minor>`.

- `major` - increments when the skill undergoes structural or breaking changes
- `minor` - increments for additive features, new assessment categories, or format refinements

## Increment Rules

1. **Increment minor by 0.1** for each release that adds or refines capability without breaking
   existing behavior.

2. **Minor rolls over at 9**. When minor would reach 10, increment major by 1 and reset minor to 0.

   | Before | After | Reason         |
   |--------|-------|----------------|
   | 0.8    | 0.9   | minor + 1      |
   | 0.9    | 1.0   | minor rollover |
   | 1.9    | 2.0   | minor rollover |
   | 9.9    | 10.0  | minor rollover |

3. **Major may also be incremented directly** for breaking changes that alter the report structure,
   remove mandatory sections, or change scoring semantics.

## When To Bump

Never bump the version automatically. The version is bumped only when the user explicitly asks for
it.

Do not bump the version as a side effect of adding features, fixing issues, or refactoring. Wait for
the user to request a version bump, then apply the increment rules above.

## Terminology

The word `version` in this file always means the skill version recorded in `SKILL.md`
frontmatter.

Audit reports produced by the skill carry a `Report Revision`, not a version. Inside a report,
the word `version` refers to the audited software, a project, a library, or the skill itself,
which is shown as `Skill Version`. Report revision rules live in `process/report-format.md`
and `synthesis/report-comparison.md`.

## Where Version Is Recorded

The version lives in `SKILL.md` frontmatter under `metadata.version`:

```yaml
---
name: lens-skill
metadata:
  version: "X.Y"
---
```

This follows the [Agent Skills specification](https://agentskills.io/specification) `metadata` field
convention, keeping the skill compatible with Anthropic Claude and other spec-compliant agents.
