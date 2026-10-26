# Evidence Schema

## Purpose

> **Scope:** The canonical evidence kinds, outcome states, record fields, sufficiency rules,
> advisory states, and coverage labels used by the audit model
> **Key items:** `DECLARED`, `INSPECTED`, `STATICALLY_DERIVED`, `EXECUTED`, `MEASURED`,
> `CORROBORATED`, outcome vocabulary, claim sufficiency, advisory states, coverage labels

This file defines the evidence vocabulary the audit model uses, per `process/audit-model.md`.

It answers two questions for every claim: what kind of observation supports it, and what that
kind can and cannot establish.

Apply `principles/evaluation-rules.md` throughout.

The report-level `Basis` vocabulary (`inspected`, `reported`, `inferred`, `executed`) and the
ledger `Observation`/`Concern` tags stay unchanged - the kinds below are the analytic layer
recorded in the audit model and cited in finding `Evidence` fields, with the mapping defined
here.

## Contents

| Section                          | Line | What it covers                                     |
|----------------------------------|------|----------------------------------------------------|
| Evidence Kinds                   | 36   | What each kind can and cannot establish            |
| Outcome States                   | 71   | Per-criterion result vocabulary                    |
| Evidence Records                 | 96   | Required fields and redaction rules                |
| Supplied And Historical Evidence | 136  | Reuse rules for prior artifacts                    |
| Coverage And Collection          | 146  | Inventory, classification, and sampling discipline |
| Claim Sufficiency                | 163  | What verification each claim type requires         |
| Closure Rules                    | 180  | What may close a criterion and what may not        |
| Advisory States                  | 195  | Dependency-advisory vocabulary                     |
| Coverage Labels                  | 216  | Criterion-coverage label vocabulary                |

## Evidence Kinds

| Kind                 | What it can establish                                              | What it cannot establish by itself           |
|----------------------|--------------------------------------------------------------------|----------------------------------------------|
| `DECLARED`           | A document, maintainer, or artifact states an intention or result  | Implementation or successful operation       |
| `INSPECTED`          | A specific source or configuration property was observed           | Runtime behavior outside the traced scope    |
| `STATICALLY_DERIVED` | A property derived from a sufficiently resolved graph or code path | Behavior involving unresolved dynamic paths  |
| `EXECUTED`           | A commissioned procedure produced a recorded result                | Properties not exercised by that procedure   |
| `MEASURED`           | A property measured under stated conditions                        | Performance outside those conditions         |
| `CORROBORATED`       | Multiple relevant, sufficiently independent observations agree     | Universal correctness or exhaustive coverage |

The kinds are not one universal ranking.

Full source and module inspection may satisfy a structural claim, while a performance claim
normally needs measurement.

Two statements copied from one source are not independent corroboration.

### Mapping To The Report Vocabulary

| Kind                 | Report `Basis` | Report tag  | Notes                                              |
|----------------------|----------------|-------------|----------------------------------------------------|
| `DECLARED`           | `reported`     | Observation | Intent or stated result, never the current control |
| `INSPECTED`          | `inspected`    | Observation | Direct source/config observation                   |
| `STATICALLY_DERIVED` | `inferred`     | Observation | Derivation path and unresolved edges recorded      |
| `EXECUTED`           | `executed`     | Observation | Commissioned run under an executed evidence mode   |
| `MEASURED`           | `executed`     | Observation | `EXECUTED` with workload and condition fields      |
| `CORROBORATED`       | `inferred`     | Concern     | Names the independent observations combined        |

Under `source-only` evidence mode only `DECLARED`, `INSPECTED`, `STATICALLY_DERIVED`, and
`CORROBORATED` may appear.

`EXECUTED` and `MEASURED` require `executed-readonly` or `executed-commands` per the evidence
mode rules, or they arrive as `DECLARED`/`Reported` artifacts produced outside the audit.

## Outcome States

Every criterion result uses exactly one of these states:

| State            | Meaning                                                             |
|------------------|---------------------------------------------------------------------|
| `PASS`           | The criterion is satisfied within the assessed scope, with evidence |
| `FAIL`           | The criterion applies and is violated, with evidence of violation   |
| `PARTIAL`        | A known, demonstrated subset satisfies the criterion                |
| `UNKNOWN`        | Evidence exists but cannot decide the criterion                     |
| `NOT_ASSESSED`   | The criterion applies but no method ran against it                  |
| `NOT_APPLICABLE` | The criterion cannot apply to this subject's deployment model       |

`PARTIAL` always names the demonstrated subset - it never means "a test was not executed".

`NOT_ASSESSED` and `NOT_APPLICABLE` both require a recorded reason.

The mapping to report markers is `PASS`/`FAIL`/`PARTIAL`/`UNKNOWN`/`N/A` unchanged, with
`NOT_ASSESSED` rendered as `Not assessed` and `NOT_APPLICABLE` rendered as `N/A` where the
report vocabulary requires it.

Executed-procedure rows keep their own runner vocabulary (`PASS`, `FAIL`, `ERROR`, `BLOCKED`,
`SKIPPED`, `NOT RUN`) per `principles/evaluation-rules.md` - a runner status is not a criterion
outcome, and `NOT RUN` never counts toward `PASS`.

## Evidence Records

Every material observation or procedure in `audit-model.json` carries a record with these
fields:

| Field         | Required content                                                      |
|---------------|-----------------------------------------------------------------------|
| `id`          | `EVD-NNN`, unique within the audit                                    |
| `audit`       | The audit identity and report revision                                |
| `subject`     | Full subject revision or content identity                             |
| `kind`        | One of the six evidence kinds                                         |
| `collector`   | The stage or agent that produced the record                           |
| `method`      | How the observation was produced                                      |
| `timestamp`   | Collection time, ISO 8601                                             |
| `tool`        | Tool and version where applicable, `null` for manual inspection       |
| `locator`     | For `INSPECTED`: path, symbol, and line range plus a content digest   |
| `procedure`   | For `EXECUTED`/`MEASURED`: command or procedure, working directory,   |
|               | environment profile, features/target, exit status, artifact digest    |
| `result`      | What was observed                                                     |
| `claims`      | Claim or criterion IDs the record supports                            |
| `limits`      | What the record cannot establish                                      |
| `sampling`    | Sampling depth and selection rule, `full` for complete review         |
| `counter`     | Counter-evidence examined                                             |
| `redaction`   | `none`, `redacted`, or `withheld` with reason                         |
| `unavailable` | Reason when expected evidence could not be produced, `null` otherwise |

Method is recorded separately from outcome - a recorded command is not a passed check.

A repository-relative path without an excerpt, symbol, or recorded observation is a locator,
not sufficient evidence.

Favorable claims carry the same record discipline as unfavorable ones.

### Redaction

Never retain raw credentials, tokens, passwords, or keys in records, snippets, or logs.

A redacted example still demonstrates the mechanism - record `[REDACTED]` in place of the
value per `principles/evaluation-rules.md`.

## Supplied And Historical Evidence

A committed or supplied artifact (CI output, scan result, prior report, coverage export) keeps
its original revision and environment in the record.

Reuse it only after checking it remains relevant to the current claim.

It is `DECLARED`/`Reported` evidence regardless of who produced it, and it is never relabeled
as executed during the current audit.

## Coverage And Collection

Inventory all in-scope source files before sampling.

Classify each file as production code, unit or integration test, test support, generated code,
vendored code, example, or script - `scripts/scan-structure.py` additionally separates the
non-code classes doc, config, asset, and other inside the same `inventory[]` records.

Record excluded and unread files explicitly in `inventory[]` and the Scope Exclusions section.

Security-critical and data-integrity paths target full path review.

Lower-risk areas may use risk-directed sampling, which records its limits in `sampling`.

A failed parse or unavailable tool creates a collection limitation recorded in `limits`,
never a silent hole in coverage figures.

## Claim Sufficiency

Each claim class names the verification that is sufficient and the substitutes that are not.

| Claim or risk                  | Sufficient verification                                                          | Insufficient substitute                          |
|--------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------|
| No secret in process arguments | All supported invocation paths avoid secret-bearing argv, inspected or executed  | A warning while the secret path remains accepted |
| Automated merge verification   | Configured enforcement plus a recorded run on the applicable branch and targets  | One local test run                               |
| License-policy conformance     | Complete applicable inventory plus scan or manual obligation review              | Policy file presence                             |
| Native dependency provisioning | Recorded acquisition, version, integrity, and successful provisioning or build   | A dependency-policy check passing                |
| Concurrency or latency target  | Defined workload, environment, warmup, duration, error budget, percentile target | A mechanism description with no defined load     |
| Authorization isolation        | Per-entry-point negative cases over permitted and denied resources               | Existence of one permission helper               |
| Test adequacy                  | Exercised critical behaviors and failure paths, with results                     | Counted test functions                           |
| Deployability                  | Recorded build or provisioning on the intended target                            | A Dockerfile or compose file being present       |
| Feature shipped on a branch    | Marker greps and path reads at the target ref (`git grep`, `git show`, `git ls-tree`) | The change-record or spec document existing on that ref |

Extend this table in the criterion catalogue when a subject needs a claim class it lacks.

## Closure Rules

A criterion closes only on evidence that establishes its intended postcondition.

A warning can close a visibility criterion, such as "the risk is disclosed to the operator".

A warning cannot close a prevention criterion, such as "no secret reaches the process argument
list", unless an authorized owner explicitly accepts it as a compensating control - and the
residual exposure is then recorded, not erased.

A "not run" control never appears as successful verification.

Formal acceptance changes a risk's disposition, not its technical effectiveness, and never
earns remediation credit.

## Advisory States

Dependency-advisory cells and records use exactly these states:

| State                              | Meaning                                                          |
|------------------------------------|------------------------------------------------------------------|
| `KNOWN_APPLICABLE`                 | An advisory covers the component and the vulnerable path applies |
| `KNOWN_MITIGATED`                  | An advisory applies but a recorded control removes the exposure  |
| `KNOWN_NOT_APPLICABLE`             | An advisory exists but the vulnerable path is disabled or absent |
| `NONE_IDENTIFIED_BY_RECORDED_SCAN` | A recorded scan or check found no advisory for the component     |
| `NOT_CHECKED`                      | No advisory source was consulted for the component               |

The SBOM `Advisory` column renders the compact forms `Applicable`, `Mitigated`,
`Not applicable`, `None identified`, and `Not checked`.

Every non-`NOT_CHECKED` state records its provenance - which scan, advisory artifact, or
inspection established it - and `KNOWN_MITIGATED`/`KNOWN_NOT_APPLICABLE` carry the mitigation or
disabling evidence.

`NOT_CHECKED` is a disclosed gap, never silently upgraded to `NONE_IDENTIFIED_BY_RECORDED_SCAN`.

## Coverage Labels

Criterion-coverage reporting uses exactly these labels:

| Label                         | Meaning                                              |
|-------------------------------|------------------------------------------------------|
| `COMPLETE_FOR_DECLARED_SCOPE` | Every applicable criterion has a resolved outcome    |
| `PARTIAL`                     | Some applicable criteria are resolved, gaps recorded |
| `NOT_ASSESSED`                | The criterion family or method was not exercised     |
| `NOT_APPLICABLE`              | The family cannot apply to this subject              |

Broad engagement labels always disclose the evidence mode beside them.

A static source review is not a penetration test, and an embedding-component review is not an
organizational AI-governance assessment.

The Audit Type Coverage matrix keeps its own type-level vocabulary per
`references/audit-taxonomy.md` - these labels describe criterion coverage, not engagement
coverage.
