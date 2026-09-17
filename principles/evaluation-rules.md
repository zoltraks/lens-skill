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

## Evidence Strength And Claim Control

Assign an evidence ID (`EVD-001` onward) to each material observation or tool execution.

Record its source, revision, scope, collection method, and limitations in the evidence ledger
specified in `process/audit-workflow.md`.

Distinguish these evidence bases in finding detail:

- **Inspected**: directly observed in source, configuration, or documentation, not executed.
- **Reported**: supplied by documentation, a stakeholder, a prior report, or a committed artifact
  such as CI output, a coverage report, or a scan result.
- **Inferred**: reasoned from cited evidence, with prerequisites and uncertainty stated.

The audit never executes checks itself. Results produced outside the audit are `Reported`
evidence, regardless of who ran them.

These labels describe evidence, not replacement category statuses.

Record confidence as `HIGH`, `MEDIUM`, or `LOW`, with a reason independent of severity.

High confidence requires a complete supporting trace or reproducible observation within scope.

Medium confidence indicates partial corroboration, and low confidence indicates material unknowns.

An inspected defect can be high confidence without a scanner alert, but it is not runtime-verified.

Keep qualifications intact in summaries, strengths, scores, and roadmaps.

A changelog saying tests passed supports "reported passing", never "verified passing".

A command listed as a verification recommendation is not evidence that it ran.

A committed scanner report supports only its covered checks, not "no vulnerabilities".

**Counter-check material claims**

Before finalizing every `CRITICAL` or `HIGH` finding, look for evidence that could refute it.

- Trace inputs, callers, guards, configuration, and the actual effect across relevant boundaries.
- Check whether the code is compiled, registered, reachable, and enabled for the assessed target.
- Verify library semantics and control-flow invariants before claiming a panic or data loss.
- Identify actor access, deployment prerequisites, blast radius, and compensating controls.
- Record the counter-check and remaining uncertainty, the audit never performs execution.

A guarded `unwrap()` is not a demonstrated panic, and an unregistered module does not necessarily
add compile time.

A Docker builder-stage exposure does not prove inclusion in the published runtime image.

A policy requiring documentation before implementation cannot be disproved by missing doc comments.

Treat these as examples of claim validation, not exceptions limited to a particular stack.

**Requirements and advice**

Separate mandatory requirements, adopted recommendations, and optional improvements.

Cite the requirement and its applicability before recording nonconformance.

A standard's popularity does not make its adoption mandatory, and a recommendation does not
become a requirement merely because the report lists it.

Do not infer code originality, authorship, review history, or organizational practices from
source style or absence of contrary evidence.

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

Use plain-text markers by default, add glyphs only when explicitly requested.

Reserve `FAIL` for cases where the capability is both absent and required by a stated or clearly implied requirement. If the requirement itself is not stated, prefer `UNKNOWN` and note the missing requirement.

## Contextual Applicability

Some categories do not apply to every system.

A local binary may not need hosted telemetry or on-call, but can still need safe updates, rollback,
file-operation safeguards, and recovery from corruption.

Use `N/A` only when the capability cannot apply given the system's stated or clearly evident deployment model.

Every `N/A` must carry a one-line justification anchored to the deployment model, for example "single-user desktop binary, no hosted runtime".

`N/A` is not an escape hatch. Do not use it to avoid reporting a real gap in a system where the capability could apply. When in doubt between `N/A` and `UNKNOWN`, prefer `UNKNOWN`.

Distinguish the three non-positive markers carefully:

- `FAIL`: the capability is needed and is absent, with evidence.
- `UNKNOWN`: the capability may be needed but evidence is missing.
- `N/A`: the capability cannot be needed given the deployment model.

A category marked `N/A` is excluded from scoring, not scored zero. See `synthesis/project-scorecard.md`.

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
  - `CQY` - Code Quality
  - `SEC` - Security & Compliance
  - `INF` - Infrastructure & CI/CD
  - `AIP` - AI Provenance & Code Origin
  - `CPR` - Copyrights & Originality
  - `API` - API Compatibility & Versioning Discipline (conditional, reusable libraries and
    packages only, per `assessment/api-compatibility.md`)
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
- Never compile, build, test, or execute the audited project, and never run linters, scanners,
  or generators against it. Tool availability cannot be assumed. Analysis rests on repository
  contents alone: source files, configuration, build scripts, pipeline definitions,
  documentation, and committed artifacts. Read-only inspection commands such as file listing,
  search, and version control history remain in scope.
