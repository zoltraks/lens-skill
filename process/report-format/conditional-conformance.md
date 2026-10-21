# Conformance Sections

## Purpose

> **Scope:** The conditional conformance sections of the report
> **Key items:** API contract, skill definition, agent guidance, AI system, standards,
> engineering baseline, naming and layout, API compatibility

## Contents

| Section                                   | Line | What it covers                             |
|-------------------------------------------|------|--------------------------------------------|
| API Contract Conformance                  | 22   | API specification and security conformance |
| Skill Definition Conformance              | 49   | Agent Skill and artifact spec conformance  |
| Agent Guidance Conformance                | 116  | Guidance-set topology and ownership        |
| AI System Assessment                      | 146  | AI model, dataset, and safety assessment   |
| Standards Conformance                     | 165  | Project development standards conformance  |
| Engineering Baseline Conformance          | 228  | Bundled stack and purpose baseline floor   |
| Structure Conformance                     | 255  | Directory, file, and code-division rules   |
| API Compatibility & Versioning Discipline | 306  | Library API surface and SemVer discipline  |

## API Contract Conformance

Include this section only when the system exposes an API, per `assessment/api-contract.md`.

Omit it entirely for a system with no API surface, and note the omission in Scope Exclusions.

Present a conformance table across the evaluated dimensions,
then describe each gap with evidence and its linked `FND-XXX`.

Map each API security gap to its OWASP API Security Top 10 (2023) code where one applies.

A deviation from the declared contract is not automatically API8 `Security
Misconfiguration` - classify by the deviation's character (missing controls, unsafe
defaults, excessive exposure) or map to a CWE instead, and leave the mapping empty when
no category genuinely fits.

| Dimension                  | Status  | Evidence                                        |
|----------------------------|---------|-------------------------------------------------|
| Specification present      | PASS    | `openapi/openapi.yaml`                          |
| Schema validation enforced | PARTIAL | typed deserialization, no rejection tests       |
| Adopted error contract     | FAIL    | observed response contradicts declared schema   |
| Versioning strategy        | UNKNOWN | compatibility policy not supplied               |
| Spec-to-code agreement     | PARTIAL | `/health` marked `security: []` but behind auth |

When the report language is not English, apply the column header translations from the matching
`translations/` file.

## Skill Definition Conformance

Include this section only when the subject is an Agent Skill, a skill collection,
or contains agent-facing artifacts such as `SKILL.md` files, `AGENTS.md`, `CLAUDE.md`, rules
directories, plugin manifests, subagent definitions, instruction files, or MCP configuration,
per `assessment/skill-definition.md`.

Omit it entirely for a project with no in-scope agent-facing artifacts,
and note the omission in Scope Exclusions.

Record the spec baseline used for each format: the `references/agent-skills.md`
and `references/agent-configuration.md` snapshot dates or the live-fetch results when
the optional check ran.

Present a conformance table across the evaluated dimensions, then describe each gap with evidence
and its linked `FND-XXX`.

| Dimension                | Status  | Evidence                                               |
|--------------------------|---------|--------------------------------------------------------|
| Frontmatter present      | PASS    | `SKILL.md` has YAML frontmatter with required fields   |
| Name field conformance   | PASS    | `name` is lowercase, matches directory, under 64 chars |
| Description conformance  | PARTIAL | Description is 1200 chars, exceeds 1024-char limit     |
| Optional field validity  | PASS    | `license`, `compatibility`, `metadata` all valid       |
| Directory structure      | PASS    | `scripts/`, `references/` directories present          |
| Progressive disclosure   | PASS    | `SKILL.md` is 180 lines, references split out          |
| File reference integrity | FAIL    | `references/missing.md` referenced but does not exist  |
| Description triggering   | PARTIAL | Description lacks specific trigger keywords            |
| Body content quality     | PASS    | Instructions, examples, and edge cases present         |

When the subject contains more than one skill - a collection, or embedded skills assessed as
components - precede the dimension table with a Skills Inventory matrix listing every discovered
`SKILL.md`:

| Skill         | Path                          | Name Match | Status       | Key Gaps                        |
|---------------|-------------------------------|------------|--------------|---------------------------------|
| pdf-toolkit   | `skills/pdf-toolkit/`         | YES        | PASS         | None                            |
| code-reviewer | `.claude/skills/code-review/` | NO         | PARTIAL      | `name` does not match directory |
| legacy-bot    | `plugins/legacy/`             | YES        | FAIL         | Missing `description` field     |
| helper-bot    | `.claude/skills/helper/`      | YES        | OUT OF SCOPE | Installed, excluded at intake   |

Every discovered `SKILL.md` appears in the matrix, including ones excluded as installed,
unfetched, or unchecked at intake, which carry `OUT OF SCOPE` as their status and the exclusion
reason as the gap note.

When non-skill agent-facing artifacts exist, follow the Skills Inventory with an Agent Artifacts
table listing every discovered memory file, rules directory, subagent definition, plugin
manifest, instruction file, or MCP configuration:

| Artifact        | Type        | Path               | Status       | Notes                         |
|-----------------|-------------|--------------------|--------------|-------------------------------|
| Project memory  | `AGENTS.md` | `AGENTS.md`        | PASS         | Covers build and test         |
| Cursor rules    | Rules dir   | `.cursor/rules/`   | PARTIAL      | One rule has a dead `globs`   |
| Greeting plugin | Plugin      | `plugins/greeter/` | PASS         | Manifest `name` present       |
| Vendor rules    | Rules dir   | `.windsurf/rules/` | OUT OF SCOPE | Installed, excluded at intake |

Follow the matrix with the dimension table per skill that warrants detail - at minimum every
non-`PASS` skill and every skill in a collection - then describe each gap with evidence and its
linked `FND-XXX`.

Apply the same per-artifact detail rule to every non-`PASS`, non-excluded row
of the Agent Artifacts table.

The aggregate status follows the weakest in-scope item.

When the report language is not English, apply the column header translations from the matching
`translations/` file.

## Agent Guidance Conformance

Include this section only when the subject carries a structured agent-guidance documentation
set, per `assessment/agent-guidance.md`.

Omit it entirely for a project whose agent-facing material is a lone thin entry file or less,
and note the omission in Scope Exclusions.

Record the baseline used: the `references/agent-configuration.md` Guidance Set Baselines
snapshot date, or the live-fetch result when the optional check ran.

Present a conformance table across the evaluated dimensions, then describe each gap with
evidence and its linked `FND-XXX`.

| Dimension              | Status  | Evidence                                                       |
|------------------------|---------|----------------------------------------------------------------|
| Guidance inventory     | PASS    | every discovered guidance document listed, in or out of scope  |
| Entry route            | PASS    | `AGENTS.md` read order resolves to `docs/standard/` files      |
| Index of record        | FAIL    | rules restated in `README.md` and `docs/GUIDELINES.md`         |
| Consolidated topology  | PASS    | `AGENTS.md` recorded as the central rules document             |
| Owner selection        | PARTIAL | workflow and testing owned, style and versioning unrecorded    |
| Role resolution        | PASS    | declared roles resolve to `docs/changes/` and `docs/plans/`    |
| Restricted directories | UNKNOWN | no read-boundary statements found                              |
| Vendored documents     | PARTIAL | vendored `PREPARATION.md` marker older than the canonical file |

The aggregate status follows the weakest evaluated dimension.

When the report language is not English, apply the column header translations from the matching
`translations/` file.

## AI System Assessment

Include this section only when the project trains, serves, or materially depends on an AI or
machine-learning system, per `assessment/ai-system.md`.

Keep this section distinct from AI-generated-code provenance.

A project can have AI-assisted source without having an AI system,
and an AI system can contain no evidence about how its source was authored.

An `AI Governance Audit` row omitted from the coverage table as `NOT APPLICABLE` never
suppresses AI-provenance findings in the `AIP` pillar - the row answers whether
governance of an AI system was assessed, the pillar answers how the source was authored.

Present the evaluated lifecycle, model and data provenance, evaluation evidence, safety boundaries,
operational controls, and unresolved limitations.

Use NIST AI RMF or ISO/IEC 42001 only when the selected practices were actually assessed.

## Standards Conformance

Include this section only when the project contains documented development standards,
per `assessment/standards-conformance.md`.

Omit it entirely for a project with no development standards documents,
and note the omission in Scope Exclusions.

This section evaluates two dimensions: whether the codebase conforms to the project's documented
development standards, and whether those standards are themselves consistent with established good
practices for the technology stack, programming language, and software type.

**Standards inventory**

List the development standards documents found in the project:

| Document | Path   | Stack Coverage                         |
|----------|--------|----------------------------------------|
| <title>  | <path> | <languages, frameworks, software type> |

When the report language is not English, apply the column header translations from the matching
`translations/` file.

**Code conformance**

Present a conformance table across the areas the standards cover, then describe each gap with
evidence and its linked `FND-XXX`:

| Area                  | Standard Rule         | Status  | Evidence                                  |
|-----------------------|-----------------------|---------|-------------------------------------------|
| Language version      | <rule from standards> | PASS    | <file or config matching the rule>        |
| Project structure     | <rule from standards> | PARTIAL | <file or pattern diverging from the rule> |
| Naming conventions    | <rule from standards> | FAIL    | <file or pattern violating the rule>      |
| Error handling        | <rule from standards> | UNKNOWN | <not enough evidence to judge>            |
| Testing               | <rule from standards> | PASS    | <test files matching the rule>            |
| Formatting and lint   | <rule from standards> | PARTIAL | <CI config present, not enforced>         |
| Dependency management | <rule from standards> | PASS    | <manifest and lockfile matching the rule> |
| Security              | <rule from standards> | FAIL    | <file or pattern violating the rule>      |

When the report language is not English, apply the column header translations from the matching
`translations/` file.

**Standards quality**

Evaluate whether the documented standards are consistent with established good practices for the
stack.

Anchor every judgement to a named external best practice, style guide, or convention:

| Area   | Standards Position             | External Best Practice  | Alignment                      |
|--------|--------------------------------|-------------------------|--------------------------------|
| <area> | <what the standards prescribe> | <named external source> | ALIGNED / PARTIALLY / DIVERGES |

When the report language is not English, apply the column header translations from the matching
`translations/` file.

After the table, describe each divergence with evidence.

Name the external source and explain how the standards position differs from the established
practice.

Cross-reference any conformance gap that also produces a `FND-XXX` finding.

## Engineering Baseline Conformance

Include this section when the subject ships or develops executable source and at least one
bundled baseline digest covers its detected stack or nature,
per `assessment/baseline-conformance.md`.

Omit it entirely for a subject with no code or no covering baseline,
and note the omission in Scope Exclusions.

Record which baselines governed the judgement - the digest files and their snapshot dates, or
the subject's own standards where they overrode - in the Auditing Methodology section.

Present a conformance table across the evaluated baseline rows, then describe each gap with
evidence and its linked `FND-XXX`.

| Baseline                   | Status  | Evidence                                          |
|----------------------------|---------|---------------------------------------------------|
| Runtime/toolchain pinning  | PASS    | `.nvmrc` and `engines.node` agree                 |
| Dependency reproducibility | PASS    | `package-lock.json` committed, `npm ci` in CI     |
| Lint/format gate           | PARTIAL | `eslint.config.*` present, no CI step consumes it |
| Test floor                 | PASS    | `tests/` exercised by the CI workflow             |
| Secrets hygiene            | PASS    | no secrets in source, `.env` gitignored           |
| CLI output contract        | N/A     | subject is not a `cli` nature                     |

When the report language is not English, apply the column header translations from the matching
`translations/` file.

## Structure Conformance

Include this section when the subject contains source code files or a structured documentation
tree, per `assessment/structure-review.md` and `references/naming-and-layout.md`.

Omit it only for a subject with neither source files nor a structured documentation tree (such
as a single-file prose proposal), and note the omission in Scope Exclusions.

Evaluate each component (`src/<Component>`, `tests/<Component>`, `scripts/`, `docs/`)
independently against its component role (`library`, `service`, `application`, `cli`,
`test-suite`, `documentation`) and the governing stack or documentation conventions from
`references/naming-and-layout.md` and `references/stacks/`.

Cite the consulted authoritative external sources in `Auditing Methodology` and include their
links in `References` so the governing rules can be retrieved on demand.

**Directory and file naming**

Present a per-component conformance table covering directory organization, directory naming
(full words versus abbreviations such as `App`/`Config`/`Auth`/`Docs`, singular/plural
consistency, absence of `Misc`/`Util` catch-alls), source-file naming, and test-file naming:

| Component          | Surface       | Convention                     | Observed                           | Status  | Evidence                 |
|--------------------|---------------|--------------------------------|------------------------------------|---------|--------------------------|
| `src/OrderApp.Api` | Directories   | Full `PascalCase` role nouns   | `App/`, `Config/`, `Auth/`         | PARTIAL | `EVD-036`, `FND-STR-001` |
| `src/OrderApp.Api` | Source files  | `PascalCase.cs` matching type  | 40/40 `.cs` files `PascalCase`     | PASS    | `EVD-036`                |
| `tests/OrderTests` | Test files    | `<Subject>Tests.cs`            | 13 `*Tests.cs` + `ModuleInit.cs`   | PASS    | `EVD-036`                |
| `docs/`            | Documentation | `kebab-case.md` or role naming | Mixed `Snake_Case.md` and `Pascal` | PARTIAL | `EVD-036`                |

**Code division**

Present a conformance table evaluating how types, interfaces, abstract classes, and
implementations are divided across files and modules according to idioms natural for the
language and component role:

| Component          | Division Rule                             | Observed                                          | Status  | Evidence                 |
|--------------------|-------------------------------------------|---------------------------------------------------|---------|--------------------------|
| `src/OrderApp.Api` | One public top-level type per `.cs` file  | 9 files co-locate 2-4 public types                | PARTIAL | `EVD-037`, `FND-STR-002` |
| `src/OrderApp.Api` | Interface separated from implementation   | `IRevocationStore` + `NullRevocationStore` paired | PARTIAL | `EVD-037`, `FND-STR-002` |
| `src/OrderApp.Api` | Single-responsibility component placement | `App/Misc.cs` catch-all, `App/RedisMain.cs`       | FAIL    | `EVD-038`, `FND-STR-002` |

When the report language is not English, apply the column header translations from the matching
`translations/` file.

After the tables, describe each non-`PASS` row in single-sentence paragraphs with concrete file
and line evidence and link to the corresponding `FND-STR-NNN` finding.

In-code identifier naming - classes, methods, fields, constants, and variables - is assessed by
`assessment/code-style.md` and reported in the `Code Style` section per
`process/report-format/code-style.md`, not in this section.

## API Compatibility & Versioning Discipline

Include this section only when the subject is a reusable library or package,
per `assessment/api-compatibility.md`.

Omit it entirely for a deployable service or application, and note the omission in Scope Exclusions.

Present a conformance table across the evaluated dimensions, then describe each gap with evidence
and its linked `FND-XXX`.

| Dimension                  | Status  | Evidence                                          |
|----------------------------|---------|---------------------------------------------------|
| Public surface tracked     | PARTIAL | API baseline or exports list, or none found       |
| Compatibility gate present | FAIL    | No ApiCompat or semver-checks configuration found |
| Versioning scheme declared | PASS    | `VERSIONING.md` names the scheme                  |
| Versioning practice        | PARTIAL | Tag and changelog history vs the declared scheme  |
| Deprecation policy         | UNKNOWN | Deprecation markers and removal timeline          |
| Breaking changes tracked   | FAIL    | Known items bound to a named future major version |

When the report language is not English, apply the column header translations from the matching
`translations/` file.

After the table, list each known future-breaking item and the version it is bound to.

An item with no target version is open-ended and must be named as such.

Configured tooling is evidence of intent, not proof of execution.

Treat a configured gate as `REPORTED` unless the audit can verify it ran.
