# Readiness And Scoring

## Purpose

> **Scope:** Deterministic scorecard aggregation, evidence confidence, maturity, and
> production-readiness gates
> **Key items:** score inputs, score caps, confidence, readiness state, sign-off limits

This file defines how Lens converts criterion outcomes into comparable scores without treating an
average as a production approval.

Apply `principles/evaluation-rules.md` throughout.

## Contents

| Section                   | Line | What it covers                     |
|---------------------------|------|------------------------------------|
| Separate Decision Outputs | 28   | Category status vs dimension score |
| Criterion Inputs          | 49   | Criterion Inputs guidance          |
| Dimension Scoring         | 75   | Dimension Scoring guidance         |
| Overall Score             | 161  | Overall Score guidance             |
| Confidence                | 189  | Confidence guidance                |
| Maturity Levels           | 207  | Maturity Levels guidance           |
| Readiness Gates           | 226  | Readiness Gates guidance           |
| Required Summary Fields   | 279  | Required Summary Fields guidance   |
| Multi-Project Rules       | 292  | Multi-Project Rules guidance       |

## Separate Decision Outputs

Every full audit keeps these outputs separate:

- **Category status:** whether an assessed capability is present, incomplete, absent, unknown, or
  inapplicable.
- **Dimension score:** a bounded summary of weighted criterion mastery and evidence quality.
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

## Criterion Inputs

Start each score from the frozen criterion table declared in Auditing Methodology per
`references/criterion-catalogue.md` - each criterion carries its `dimension`, `weight`, and
`criticality`, and `process`-family criteria never enter the product-quality aggregate.

Each criterion resolves to one outcome state from `references/evidence-schema.md`, and the
state maps to a mastery value:

| Outcome          | Mastery treatment                                         | Evidence interpretation                   |
|------------------|-----------------------------------------------------------|-------------------------------------------|
| `PASS`           | `1.0`                                                     | Criterion satisfied within assessed scope |
| `PARTIAL`        | Recorded fraction `0 < m < 1` naming the satisfied subset | A demonstrated subset satisfies it        |
| `FAIL`           | `0.0`                                                     | Violated, with evidence of violation      |
| `UNKNOWN`        | Unresolved - excluded from the point estimate             | Evidence cannot decide the criterion      |
| `NOT_ASSESSED`   | Unresolved - excluded from the point estimate             | The criterion's method did not run        |
| `NOT_APPLICABLE` | Excluded from the denominator entirely                    | Cannot apply to this deployment model     |

`FAIL` requires an applicable requirement and evidence of absence or defeat.

`UNKNOWN` and `NOT_ASSESSED` are not low mastery and are never converted to `0.0` - they widen
the interval and reduce coverage instead.

`NOT_APPLICABLE` requires a deployment-model justification frozen at planning, and must not be
used for missing evidence.

## Dimension Scoring

A dimension's score derives from weighted mastery over its applicable criteria - it is never
picked from an evidence-pattern range.

Compute each dimension's point mastery over its resolved applicable criteria:

```
mastery = sum(weight_i * mastery_i) / sum(weight_i)
```

Map mastery to the selected scale's integer score:

```
score = max(1, round(mastery * scale_max))
```

`PARTIAL` fractions are recorded in the model with the satisfied subset named, so a re-audit
reproduces the same mastery.

The band definitions in `synthesis/project-scorecard.md` describe what the resulting score
means - they do not substitute for the computation.

**Uncertainty interval**

Every dimension score carries an interval beside the point value:

- `lo` - mastery recomputed with every unresolved (`UNKNOWN`, `NOT_ASSESSED`) applicable
  criterion treated as `FAIL`, mapped to the scale.
- `hi` - mastery recomputed with every unresolved applicable criterion treated as `PASS`,
  mapped to the scale.
- When `lo` equals `hi` - no unresolved applicable criteria - the interval is omitted.

The interval is stated, never hidden: a score with a wide unresolved spread reports
`7/10 [4-9]`, not `7/10`.

**Eligibility gate**

A numeric dimension score publishes only when both hold:

- Resolved criteria carry more than half of the dimension's applicable criterion weight.
- At least one resolved criterion rests on `INSPECTED`, `STATICALLY_DERIVED`, `EXECUTED`, or
  `MEASURED` evidence - a dimension resolved on `DECLARED` material alone is not scored.

A dimension that fails the gate renders `UNKNOWN` with the missing coverage named - it never
publishes a numeric score on thin evidence, and `NOT_APPLICABLE` criteria never count toward
either side of the gate.

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

Severity starts at `MEDIUM`.

An advertised core journey that fails end to end is at least
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

An overall score publishes only when more than half of the applicable dimensions carry numeric
scores - below that the report presents per-dimension results and coverage with no overall.

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
laboratory defect.

An incorrect authorization check or a broken declared invariant is a
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
- Every dimension score recomputes from criterion mastery and frozen weights, and each stated
  interval equals the FAIL/PASS substitution bounds.
- Every numeric dimension passed the eligibility gate, and gated dimensions render `UNKNOWN`
  with their missing coverage named.
- Every overall score reports its formula, denominator, rounding, and floor, and published only
  when more than half of the applicable dimensions scored.
- `UNKNOWN` and `N/A` dimensions are excluded from the mean.
- Blocking findings and readiness state agree.
- Sign-off is pending when required ownership or closure evidence is missing.
- Multi-project shared references are qualified.
