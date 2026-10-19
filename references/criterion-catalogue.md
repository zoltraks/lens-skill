# Criterion Catalogue

## Purpose

> **Scope:** The criterion record schema, minimum criterion families, applicability rules, and
> the freeze discipline that anchors every audit score and verdict
> **Key items:** criterion records, families, applicability freeze, crosswalk integrity,
> criticality and weight

This file defines how an audit declares the criteria it evaluates before it reads the evidence.

A criterion is an evaluable requirement with an identifier, a method, and a sufficiency rule -
not a folder name, a section heading, or a checklist of presence.

Apply `principles/evaluation-rules.md` throughout.

The catalogue is per-audit: the criterion planner stage of `process/audit-model.md` selects,
adapts, and freezes it for the subject, and `references/evidence-schema.md` defines the outcome
states each criterion resolves to.

## Contents

| Section                | Line | What it covers                              |
|------------------------|------|---------------------------------------------|
| Criterion Records      | 31   | The fields every criterion carries          |
| Applicability Freeze   | 66   | Denominator locking and change rules        |
| Criterion Families     | 81   | Minimum family set and per-family notes     |
| Criticality And Weight | 130  | How criteria earn weight inside a dimension |
| Crosswalk Integrity    | 141  | Mapping to external quality models honestly |

## Criterion Records

Every criterion in `audit-model.json` `criteria[]` carries these fields:

| Field           | Required content                                                          |
|-----------------|---------------------------------------------------------------------------|
| `id`            | Three-letter family-prefixed identifier, for example `SEC-AUTHZ`          |
| `source`        | Requirement origin: stakeholder requirement, adopted standard with        |
|                 | version, auditor-proposed criterion, or reconstructed assumption          |
| `applicability` | `applicable`, `conditional`, or `not applicable` with a one-line reason   |
| `criticality`   | `critical`, `high`, `medium`, or `low` - a `critical` criterion gates the |
|                 | headline score                                                            |
| `weight`        | Relative weight inside its dimension                                      |
| `expected`      | The outcome that satisfies the criterion                                  |
| `method`        | The collection and analysis method required                               |
| `sufficiency`   | What evidence suffices, per `references/evidence-schema.md`               |
| `dimension`     | The product dimension it feeds, or `process` for a non-product family     |

Criterion identifier rules:

- Every criterion `id` starts with a **three-letter uppercase prefix** (`<FAM>-<SUBJ>`, such as
  `TST-UNIT`, `MNT-COHES`, `DEP-BUILD`, `SCA-POOL`, `COM-DATA`, `DLY-HIST`, `SKL-PRES`) - never
  a four-or-more-letter prefix (`TEST-`, `MAINT-`, `DEPLOY-`, `SCALE-`, `COMP-`, `DELIV-`,
  `SKILL-`).
- Omit numeric suffixes (`-01`, `-1`) when only one criterion uses a given `<FAM>-<SUBJ>`
  stem, and append `-01`, `-02` only when multiple distinct criteria in the same report share
  the same `<FAM>-<SUBJ>` stem.

Distinguish stakeholder requirements from auditor-proposed criteria and reconstructed
assumptions in `source` - the reader must see which requirements the subject actually made.

Record the product profile the catalogue was tuned to: product type, intended users, deployment
topology, data sensitivity, operating scale, critical functions, external contracts, and the
release purpose, distinguishing supplied facts from auditor reconstructions.

## Applicability Freeze

Freeze the applicable criterion set - the denominator - before reading favorable or unfavorable
findings.

Deciding a criterion is inapplicable after its evidence turned out unfavorable is denominator
gaming.

Every post-freeze applicability change carries a recorded reason in `audit-model.json` and a
visible justification in the report.

`NOT_APPLICABLE` means the criterion cannot apply to the deployment model, with the
contextual-applicability justification from `principles/evaluation-rules.md` - never "not
checked" or "evidence was missing".

## Criterion Families

These families are the minimum set the planner starts from.

Add or adapt families when the product profile justifies it, and record the adaptation.

| Prefix | Family / Dimension                                                               |
|--------|----------------------------------------------------------------------------------|
| `FNC`  | Functional completeness and correctness, including negative and boundary cases   |
| `TST`  | Testing, test isolation, pipeline coverage, and suite execution                  |
| `ARC`  | Architecture, layering, abstractions, session/state isolation, dependency edges  |
| `CQY`  | Code quality, static analysis, dead code, duplication, error-path hygiene        |
| `STK`  | Stack alignment, idiomatic framework and runtime conventions                     |
| `DEP`  | Dependencies, supply chain, build, container, and deployment pipeline signals    |
| `MNT`  | Maintainability, cohesion, readability, change management, documentation sync    |
| `STR`  | Physical directory layout, file naming, code division, in-code identifier naming |
| `SCA`  | Scalability, resource bounds, state scaling, and non-functional targets          |
| `SEC`  | Authorization paths, secret lifecycle, configuration exposure, misuse resistance |
| `COM`  | Compliance, data retention, audit trail, and governance documentation            |
| `REL`  | Data integrity, transaction consistency, recovery, failure handling              |
| `PRF`  | Performance and latency under the stated intended workload                       |
| `OBS`  | Observability, logging, correlation, health checks, metrics, and alerting        |
| `OPS`  | Operational readiness, rollback, backup, monitoring, and failure recovery        |
| `CMP`  | Interface and version compatibility across contracts and stored data             |
| `INT`  | Product-appropriate interaction: CLI scripting, errors, or UI behavior           |
| `DLY`  | Process: delivery practice, commit history, bus factor, release cadence          |
| `AIP`  | Process: AI-generated code provenance and review controls                        |
| `CPR`  | Process: copyright, originality, and license declarations                        |
| `SKL`  | Process/conformance: Agent Skill and agent-guidance artifacts                    |
| `SAF`  | Conditional: hazards, fail-safe behavior where consequences warrant              |
| `MDL`  | Conditional: model/retrieval quality where the product depends on it             |

Compatibility criteria cover every external contract the subject exposes - service protocols,
CLI flags and exit behavior, configuration schemas, persisted data, and supported version
combinations - not only libraries.

Deployable binaries carry breaking-change surface the same as packages.

Deployment-pipeline criteria inside `DEP` resolve `not applicable` at planning when the intake
automation signal census records `none` for the project, with the census cited as the recorded
reason - the census precedes the applicability freeze, so this is not denominator gaming.

Under an `external` census the pipeline criteria stay applicable only for what the external
pointer establishes.

Assess delivery practice, team continuity, provenance, and license obligations in separate
process families marked `process` - their results remain release gates where applicable but
never enter the product-quality aggregate.

## Criticality And Weight

A `critical` criterion is one whose `FAIL` state prevents safe release, operation, or
maintenance of the subject as scoped - a non-compensatory gate.

Weight reflects the criterion's contribution inside its dimension and is frozen with the
catalogue.

New weights, criteria, or applicability decisions after publication require a scoring-policy
version bump recorded in the audit model.

## Crosswalk Integrity

A standards crosswalk - such as the ISO/IEC 25010:2023 map in
`synthesis/project-scorecard.md` - points at actual evaluated criteria and names unresolved
gaps.

Listing nine characteristic names does not demonstrate nine-characteristic coverage.

Each mapped row cites the criteria that produced its evidence, and unmapped or unresolved
characteristics are named, not implied.
