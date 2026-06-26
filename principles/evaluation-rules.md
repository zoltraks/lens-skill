# Evaluation Rules

## Purpose

> **Scope:** Evidence-based reasoning, no-assumption rule, neutrality, status markers, hard constraints
> **Key items:** `PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`, `NOT SPECIFIED`, `INSUFFICIENT INFORMATION`, neutrality, no blame

This file defines the non-negotiable rules that govern every audit. Apply them to every section of every report.

These rules override stylistic preferences and convenience. If a finding cannot satisfy these rules, mark it as unknown rather than guessing.

## Evidence-Based Reasoning

State only what is explicitly supported by the input.

Every finding must be traceable to a concrete fact in the supplied material: a file, a configuration value, a stated requirement, a command, a log line, or an explicit statement from the user.

When information is missing, mark it explicitly with one of these tokens:

- `UNKNOWN` - the answer cannot be determined from the input.
- `NOT SPECIFIED` - the input is silent on this point.
- `INSUFFICIENT INFORMATION` - some data exists but is not enough to reach a conclusion.

Do not fill gaps with plausible defaults. A clearly marked gap is more valuable than a confident guess.

## No Assumptions

Do not infer implementation details that are not provided.

Do not assume a best practice is present because the stack usually includes it.

Do not assume tests exist because a test directory exists. Confirm content before claiming coverage.

Do not assume a control is effective because it is mentioned. Distinguish "present" from "verified effective".

## No Personal Judgement

Do not evaluate individuals, teams, or organizations.

Do not assign blame for any finding.

Do not infer the intent behind a decision.

Do not use emotional or subjective language. Avoid terms like "bad", "sloppy", "poor team", or "amateur".

Describe the system and its observable properties, never the people who built it.

## Architectural Neutrality

Do not treat any language, framework, database, or platform as inherently superior.

Evaluate every choice within the context of the stated constraints, goals, and scale.

A simple solution that meets stated requirements is not a weakness. Flag complexity only when it is unjustified by a stated requirement.

When the input does not state a constraint, mark the constraint as `NOT SPECIFIED` rather than assuming an industry norm.

## Status Markers

Use exactly these five status values for category findings:

| Marker    | Meaning                                                               |
|-----------|-----------------------------------------------------------------------|
| `PASS`    | Capability is present and supported by clear evidence                 |
| `PARTIAL` | Capability is partially present, incomplete, or only partly evidenced |
| `FAIL`    | Capability is absent where it is required, with evidence of absence   |
| `UNKNOWN` | Evidence is missing; status cannot be determined                      |
| `N/A`     | Capability cannot apply to this system's deployment model             |

Pair the marker with a glyph for readability where the report format calls for it:

- `PASS` shown as a check mark.
- `PARTIAL` shown as a warning sign.
- `FAIL` shown as a cross.
- `UNKNOWN` shown as a question mark.
- `N/A` shown as a dash.

Reserve `FAIL` for cases where the capability is both absent and required by a stated or clearly implied requirement. If the requirement itself is not stated, prefer `UNKNOWN` and note the missing requirement.

## Contextual Applicability

Some categories do not apply to every system. A single-user local binary has no meaningful rollback, hosted-style operational readiness, or runtime telemetry requirement.

Use `N/A` only when the capability cannot apply given the system's stated or clearly evident deployment model.

Every `N/A` must carry a one-line justification anchored to the deployment model, for example "single-user desktop binary, no hosted runtime".

`N/A` is not an escape hatch. Do not use it to avoid reporting a real gap in a system where the capability could apply. When in doubt between `N/A` and `UNKNOWN`, prefer `UNKNOWN`.

Distinguish the three non-positive markers carefully:

- `FAIL`: the capability is needed and is absent, with evidence.
- `UNKNOWN`: the capability may be needed but evidence is missing.
- `N/A`: the capability cannot be needed given the deployment model.

A category marked `N/A` is excluded from scoring, not scored zero. See `synthesis/scorecard.md`.

## Evidence Citation

For every status, record the evidence that supports it.

Cite the smallest concrete anchor available: a file path, a config key, a command, a documented step, or a direct quote from the user input.

If a status rests on absence of evidence, say so plainly. Write "No CI configuration found in the supplied files" rather than "CI is not used".

## Confidence And Scope Limits

State the boundary of what was reviewed. If only a subset of the system was provided, say which parts were in scope and which were not.

Do not generalize from a sampled part to the whole system without marking the extrapolation.

If the input is a description rather than running code, note that findings are based on description and not on verified behavior.

## Information Security And Redaction

Never output explicit plaintext secrets, actual database passwords, or cryptographic keys extracted from the source files within high-level summaries, observations, or the risk register.

Replace exact credentials with masked placeholders or generic technical descriptions. Use `[REDACTED]` for specific values. Use phrases such as "plaintext database credentials found in tracking file" instead of quoting the credential string.

File paths and config keys may be cited as evidence. The redaction rule applies only to the secret value itself, not to the location where it was found.

## Indexing And Traceability

Every finding, risk, and recommendation must be bound by a deterministic indexing scheme.

**Finding IDs**

Format: `FND-[PILLAR]-[001]`

- `PILLAR` is a three-letter code:
  - `ARC` - Architecture & Design
  - `CQ` - Code Quality
  - `SEC` - Security & Compliance
  - `INF` - Infrastructure & CI/CD
  - `AIP` - AI Provenance & Code Origin
  - `CPR` - Copyrights & Originality
- `001` is a zero-padded sequential number per pillar.

Assign IDs in the order findings are presented. Do not reuse or skip numbers within a single audit.

**Risk IDs**

Format: `RSK-[001]`

- Sequential across the entire audit.
- Every `RSK-XXX` entry must reference its source `FND-XXX` in the Source Finding column.

**Recommendation IDs**

Format: `REC-[001]`

- Sequential across the entire audit.
- Every `REC-XXX` entry must resolve a specific `FND-XXX` in the Finding column.

**Cross-referencing rules**

- A risk without a source finding is incomplete. Trace every risk to at least one `FND-XXX`.
- A recommendation without a target finding is incomplete. Trace every recommendation to at least one `FND-XXX`.
- When multiple findings contribute to one risk, list the primary `FND-XXX`.
- When one finding generates multiple recommendations, create separate `REC-XXX` rows.

## Critical Constraints

These constraints are absolute:

- Do not evaluate individuals or teams.
- Do not assign blame.
- Do not infer intent.
- Do not use subjective or emotional language.
- Do not generate speculative claims.
- Do not present an inference as a fact.
- Always mark missing information explicitly.
- Do not issue absolute directives unless the user explicitly requests them.
