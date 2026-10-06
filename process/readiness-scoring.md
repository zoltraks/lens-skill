# Readiness And Scoring

## Purpose

> **Scope:** Deterministic scorecard aggregation, evidence confidence, maturity, and
> production-readiness gates
> **Key items:** score inputs, score caps, confidence, readiness state, sign-off limits

This file defines how Lens converts category evidence into comparable scores without treating an
average as a production approval.

Apply `principles/evaluation-rules.md` throughout.

## Separate Decision Outputs

Every full audit keeps these outputs separate:

- **Category status:** whether an assessed capability is present, incomplete, absent, unknown, or
  inapplicable.
- **Dimension score:** a bounded summary of applicable category statuses and evidence quality.
- **Evidence confidence:** how strongly the inspected or reported evidence supports the conclusion.
- **Maturity level:** the development state supported by the evidence.
- **Readiness state:** whether the stated decision gate is met.
- **Production sign-off:** an authorized decision outside the audit, with confirmed owners and
  closure evidence.

A final report - one without a `State` row - means the scoped report passed its report-quality
gates.

It does not mean the subject is production-approved.

This distinction is audit-internal semantics - the report itself never carries a sentence
disclaiming production acceptance.

## Category Inputs

Start each score from the applicable source categories in `synthesis/project-scorecard.md`.

Use the following status interpretation:

| Status    | Numeric treatment                         | Evidence interpretation                 |
|-----------|-------------------------------------------|-----------------------------------------|
| `PASS`    | Positive capability evidence              | Present and supported within scope      |
| `PARTIAL` | Partial capability or incomplete evidence | Some capability or controls are present |
| `FAIL`    | Required capability is absent             | Absence is evidenced and applicable     |
| `UNKNOWN` | Excluded from the numeric mean            | Evidence is insufficient to decide      |
| `N/A`     | Excluded from the numeric mean            | Capability cannot apply to the model    |

`FAIL` requires an applicable requirement and evidence of absence or defeat.

`UNKNOWN` is not a low score and must not be converted to the minimum numeric value.

`N/A` requires a deployment-model justification and must not be used for missing evidence.

## Dimension Scoring

Use the selected numeric scale and the following default mapping as a starting point:

| Evidence pattern                               | 1-10 range | 1-5 range | 1-3 range |
|------------------------------------------------|------------|-----------|-----------|
| All applicable categories `PASS`               | 8-10       | 4-5       | 3         |
| Mostly `PASS` with localized `PARTIAL` results | 7-8        | 4         | 2-3       |
| Mixed `PASS` and `PARTIAL` results             | 4-7        | 3-4       | 2         |
| Material `FAIL` result                         | 1-5        | 1-3       | 1-2       |
| No scoreable evidence                          | `UNKNOWN`  | `UNKNOWN` | `UNKNOWN` |

The exact score must be justified by the affected findings, evidence IDs, scope, and confidence.

Do not choose a score from the table without explaining the selected point in the range.

Apply these caps unless a stronger project-specific rule is explicitly stated:

- An unresolved `CRITICAL` finding caps its affected dimension at `3/10`.
- An unresolved `HIGH` finding caps its affected dimension at `5/10`.
- A dimension with only reported historical execution results cannot exceed `7/10` without
  current inspected evidence that supports the same capability.
- A dimension with material unresolved unknowns cannot exceed `8/10`.
- A dimension with no scoreable category evidence is `UNKNOWN`, not `1/10`.

Convert caps proportionally for other numeric scales.

A cap is a reporting rule, not a severity assignment.

Severity and conformance anchor two further rules:

- A control the subject's own documentation, specification, or contract promises but the code
  does not implement is a spec violation - its severity grades against the documented promise,
  not against generic best practice.
- A deviation from the subject's own development standards is a conformance finding even when
  the deviation is otherwise defensible - governance evidence weighs on its own.

**Functional-defect gates**

A documented or advertised capability that the code does not implement - a supported workflow
that fails end to end, a stub behind an advertised feature, a builder image that cannot
compile the code - is a spec violation and a hard readiness gate.

While such a gate stays open the readiness state is `NOT READY` or `PENDING EVIDENCE`
regardless of dimension scores, and its dimension is capped per the finding's severity.

Severity starts at `MEDIUM`. An advertised core journey that fails end to end is at least
`HIGH`.

An overall mean never hides a broken advertised capability - every readiness statement and
verdict names it explicitly.

## Overall Score

Use the unweighted arithmetic mean of numeric dimension scores.

Exclude `UNKNOWN` and `N/A` dimensions from the denominator.

When the scale is ordinal - `5 stars`, `3 stars`, or a rubric whose levels are ordered
labels rather than measured intervals - report the per-dimension distribution beside any
mean (for example `11 dimensions: good, 3: average`), or prefer the distribution alone.

A decimal mean such as `3.8/5` implies interval precision the rubric does not supply.

Report the formula, scored dimension count, rounding rule, mean, and lowest-scoring applicable
dimension together.

If several dimensions tie for the lowest score, name all of them.

Do not report an overall score when no dimension has a numeric score.

Do not compare means across reports when the scale, dimension set, or evidence scope differs without
stating the comparability limit.

An overall mean never overrides a material risk, an unresolved readiness gate, or missing closure
ownership.

## Confidence

Assign confidence separately from the numeric score:

| Confidence | Minimum basis                                                  |
|------------|----------------------------------------------------------------|
| `HIGH`     | Complete trace, current revision, and corroborating evidence   |
| `MEDIUM`   | Partial corroboration or a bounded inspected sample            |
| `LOW`      | Material unknowns, historical evidence, or broad extrapolation |

A high score with low confidence must remain visible as a high-uncertainty result.

A low score with high confidence describes a strongly evidenced gap.

Runtime claims require runtime evidence or a clearly labeled `REPORTED` artifact.

Source inspection alone does not verify runtime behavior.

## Maturity Levels

Use the first level whose evidence conditions are satisfied:

| Level               | Minimum evidence pattern                                     |
|---------------------|--------------------------------------------------------------|
| `Prototype`         | Core intent or partial implementation is present             |
| `Early development` | Main implementation exists, but major capability gaps remain |
| `Pre-production`    | Deployable shape exists, but readiness gates remain open     |
| `Production-ready`  | Required gates are evidenced, verified, and owned            |
| `Undetermined`      | The supplied evidence cannot distinguish a maturity level    |

Maturity is descriptive and must be anchored to findings and evidence.

A production-ready claim requires a deployment model and stakeholder-approved acceptance criteria.

When those inputs are missing, retain the most defensible descriptive maturity and mark the
readiness decision as pending.

## Readiness Gates

For a readiness or due-diligence audit, define the gates before the final summary.

At minimum, assess:

- Applicable `CRITICAL` and `HIGH` findings.
- Advertised-workflow integrity: every documented capability traces to working implementation.
- Required build, test, scan, recovery, and deployment evidence.
- Confirmed verification ownership.
- Operational objectives and recovery evidence for operated systems.
- Dependency and artifact identity for shipped software.
- Business, legal, support, cost, and data artifacts for due diligence.

When the project defines no gates of its own, reconstruct the minimum set above from the
subject's deployment model and stated purpose.

**Permitted-use profiles**

When the subject is pre-production, the report states which use profile each gate guards:

- `Laboratory` - the defect exists and matters, but isolated experiments may proceed.
- `Controlled sharing` - the defect must be closed before the artifact reaches a bounded
  group of users or another team.
- `Production` - the defect must be closed before real data or untrusted users.

A gate scoped to a later profile stays open for that profile without blocking the current
one - a missing SLO is a conditional production requirement, not automatically a present
laboratory defect. An incorrect authorization check or a broken declared invariant is a
defect under every profile: laboratory status never legitimizes it.

A gate the evidence cannot satisfy stays open - silence never waives a reconstructed gate.

Use these readiness states:

| State              | Meaning                                                 |
|--------------------|---------------------------------------------------------|
| `READY`            | Stated gates are evidenced and no blocking item remains |
| `NOT READY`        | One or more applicable blocking gates remain open       |
| `PENDING EVIDENCE` | Decision depends on missing or unrun evidence           |
| `NOT ASSESSED`     | Readiness was outside the requested audit purpose       |

When the report language is not English, the readiness state is rendered per the matching
`translations/` file.

`READY` requires current closure evidence for every blocking gate.

A proposed gate is not an approved requirement until the responsible stakeholder confirms it.

Missing owners or missing closure evidence keep sign-off pending even when the report is final.

## Required Summary Fields

The Executive Summary should state:

- Overall score and lowest dimension.
- Score confidence and major evidence limits.
- Maturity level with a supporting finding or evidence reference.
- Readiness state and blocking finding or risk IDs.
- Whether production sign-off is pending.
- Known and unestimated remediation cost.

The Health Dashboard repeats the score floor and evidence limitations where the score appears.

## Multi-Project Rules

Compute scores and readiness independently per project.

Do not collapse unrelated projects into one mean.

Shared work may be counted once in cost rollups, but every affected project remains identified.

Shared gates and trade-offs use project-qualified IDs.

## Validation

The Validation Record must confirm:

- Every numeric score has supporting evidence and confidence.
- Every overall score reports its formula, denominator, rounding, and floor.
- `UNKNOWN` and `N/A` dimensions are excluded from the mean.
- Blocking findings and readiness state agree.
- Sign-off is pending when required ownership or closure evidence is missing.
- Multi-project shared references are qualified.
