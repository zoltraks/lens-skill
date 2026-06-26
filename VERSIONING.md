# Skill Versioning Policy

This document defines the versioning rules for the `lens-skill` Agent Skill.

## Current Version

**0.5**

## Format

Versions use a two-part decimal format: `<major>.<minor>`.

- `major` - increments when the skill undergoes structural or breaking changes
- `minor` - increments for additive features, new assessment categories, or format refinements

## Increment Rules

1. **Start at 0.5** for this release.

2. **Increment minor by 0.1** for each release that adds or refines capability without breaking existing behavior.

3. **Minor rolls over at 9**. When minor would reach 10, increment major by 1 and reset minor to 0.

   | Before | After | Reason |
   |--------|-------|--------|
   | 0.8    | 0.9   | minor + 1 |
   | 0.9    | 1.0   | minor rollover |
   | 1.9    | 2.0   | minor rollover |
   | 9.9    | 10.0  | minor rollover |

4. **Major may also be incremented directly** for breaking changes that alter the report structure, remove mandatory sections, or change scoring semantics.

## Where Version Is Recorded

The version lives in `SKILL.md` frontmatter under `metadata.version`:

```yaml
---
name: lens-skill
metadata:
  version: "0.5"
---
```

This follows the [Agent Skills specification](https://agentskills.io/specification) `metadata` field convention, keeping the skill compatible with Anthropic Claude and other spec-compliant agents.

## Version Changelog

| Version | Date | Changes |
|---------|------|---------|
| 0.5     | -    | Baseline with 18 assessment categories, conditional sections, and report format templates |
