# Skill Definition Conformance

## Purpose

> **Scope:** Agent Skills specification conformance, skill structure, progressive disclosure, triggering description quality, file reference integrity
> **Key items:** SKILL.md frontmatter, directory structure, description triggering, progressive disclosure, file references, body content quality

This file guides assessment of whether a project that is an Agent Skill conforms to the [Agent Skills specification](https://agentskills.io/specification) and follows the quality practices defined by the skill-creator skill.

It complements `assessment/documentation.md` for the docs dimension and `assessment/best-practices.md` for stack-convention conformance. This file covers skill-specification-specific conformance only.

Apply `principles/evaluation-rules.md` throughout. Assess only what the files show. Treat a frontmatter field that contradicts the spec as a conformance finding.

## When This Applies

This assessment applies when the subject is an Agent Skill: a directory containing a `SKILL.md` file with YAML frontmatter.

It does not apply to a conventional codebase, library, or service that has no `SKILL.md`. In that case, mark the section `N/A` with a one-line justification. Do not invent skill-conformance findings for a project that is not a skill.

## What To Evaluate

- **Frontmatter presence and validity**: whether `SKILL.md` contains YAML frontmatter with the required `name` and `description` fields.
- **Name field conformance**: whether `name` is 1-64 characters, lowercase alphanumeric and hyphens only, does not start or end with a hyphen, contains no consecutive hyphens, and matches the parent directory name.
- **Description field conformance**: whether `description` is 1-1024 characters, describes both what the skill does and when to use it, and includes trigger keywords or contexts.
- **Optional field validity**: whether `license`, `compatibility` (max 500 characters), `metadata` (string-to-string map), and `allowed-tools` fields, when present, conform to the spec constraints.
- **Directory structure**: whether the skill uses the conventional optional directories (`scripts/`, `references/`, `assets/`) where appropriate, or places files in non-standard locations.
- **Progressive disclosure**: whether `SKILL.md` body stays under 500 lines, whether large reference material is split into separate files, and whether the body points to those files with clear guidance on when to read them.
- **File reference integrity**: whether every file path referenced in `SKILL.md` resolves to an existing file on disk.
- **Description triggering quality**: whether the description includes specific keywords and contexts that help agents identify relevant tasks, and whether it is pushy enough to combat undertriggering.
- **Body content quality**: whether the body contains actionable instructions, examples of inputs and outputs, and coverage of common edge cases.
- **Reference depth**: whether file references stay one level deep from `SKILL.md`, avoiding deeply nested reference chains.

## Agent Skills Specification Reference

Use these constraints when evaluating frontmatter conformance:

| Field           | Required | Constraints                                                    |
|-----------------|----------|----------------------------------------------------------------|
| `name`          | Yes      | Max 64 chars, lowercase alphanumeric and hyphens, matches directory |
| `description`   | Yes      | Max 1024 chars, non-empty, describes what and when            |
| `license`       | No       | License name or reference to a bundled license file            |
| `compatibility` | No       | Max 500 chars, environment requirements                        |
| `metadata`      | No       | Map of string keys to string values                            |
| `allowed-tools` | No       | Space-separated string of pre-approved tools (experimental)   |

## Evidence To Look For

| Signal                        | Where It Appears                                          |
|-------------------------------|-----------------------------------------------------------|
| Frontmatter                   | YAML block at top of `SKILL.md`                           |
| Name conformance              | `name` field value vs directory name                       |
| Description quality           | `description` field content and length                    |
| Optional fields               | `license`, `compatibility`, `metadata`, `allowed-tools`   |
| Directory structure           | `scripts/`, `references/`, `assets/` directories           |
| Progressive disclosure        | `SKILL.md` line count, referenced files                    |
| File reference integrity      | Paths in `SKILL.md` body resolving to existing files       |
| Body content                  | Instructions, examples, edge cases in `SKILL.md`          |

## Status Criteria

- `PASS`: Frontmatter is fully spec-compliant, the description includes trigger keywords, the body is under 500 lines with clear file references, and all referenced files exist, with evidence.
- `PARTIAL`: The skill is functional but has conformance gaps, such as a description over the limit, a name that does not match the directory, missing trigger keywords, or broken file references.
- `FAIL`: The skill has critical spec violations, such as missing required fields, a name that is invalid, or a `SKILL.md` that is absent or unreadable, with evidence.
- `UNKNOWN`: The `SKILL.md` file was not provided for review.
- `N/A`: The subject is not an Agent Skill, with justification.

## Common Risks

- A description exceeding 1024 characters may be silently truncated by spec-compliant agents, losing trigger keywords.
- A name that does not match the directory may cause the skill to fail validation.
- A `SKILL.md` over 500 lines loads excessive context, degrading agent performance.
- Broken file references cause the agent to fail when following instructions.
- A description without trigger keywords causes the skill to undertrigger, never activating when it should.
- Missing optional fields like `license` reduce discoverability and legal clarity.
- Deeply nested reference chains make it hard for the agent to locate the right file.

## What Raises Confidence

- A `name` field that is fully compliant and matches the directory name.
- A `description` under 1024 characters that clearly states what the skill does and when to use it, with specific trigger keywords.
- A `SKILL.md` body under 500 lines that acts as a router, pointing to well-organized reference files.
- All file references in `SKILL.md` resolve to existing files.
- Optional fields like `license` and `compatibility` are present and conform to spec constraints.
- The body includes examples, edge cases, and clear step-by-step instructions.
- Reference files are focused and loaded on demand, not bundled into `SKILL.md`.

Mark each missing signal explicitly rather than inferring its presence. Treat a frontmatter field that violates a spec constraint as a conformance finding, not a style preference.
