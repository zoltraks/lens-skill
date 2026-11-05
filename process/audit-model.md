# Audit Model

## Purpose

> **Scope:** The canonical intermediate model every audit builds and the stage pipeline that
> separates collection, interpretation, scoring, and presentation
> **Key items:** `work/audit-model.json`, stage table, derivation rule, counter-evidence pass,
> publication stops

This file defines the machine-readable intermediate model that makes the audit reproducible.

The model is the single structured record an audit's tables, registers, scores, and summaries
render from - the report writer never invents facts, counts, or scores while composing prose.

Apply `principles/evaluation-rules.md` throughout.

Evidence kinds and record fields live in `references/evidence-schema.md`, and criterion
records live in `references/criterion-catalogue.md`.

## Contents

| Section                 | Line | What it covers                                   |
|-------------------------|------|--------------------------------------------------|
| Pipeline Stages         | 30   | The nine stages and their publication conditions |
| The Model Artifact      | 48   | `work/audit-model.json` schema and lifecycle     |
| Derivation Rule         | 154  | Rendering every surface from the model           |
| Counter-Evidence Review | 199  | The second-pass challenge discipline             |
| Publication Stops       | 215  | Errors that block final publication              |

## Pipeline Stages

| Stage                 | Inputs                                        | Required output                                                   | Publication condition                    |
|-----------------------|-----------------------------------------------|-------------------------------------------------------------------|------------------------------------------|
| Scope resolver        | User purpose, source availability, deployment | Audit contract and revision identity                              | Scope and evidence mode explicit         |
| Inventory collector   | Repository files, manifests, module roots     | File inventory and exclusion record                               | Every in-scope source file accounted for |
| Criterion planner     | Product context, criterion catalogue          | Applicability and method matrix                                   | `N/A` decisions justified                |
| Evidence collectors   | Source, config, supplied artifacts, execution | Typed evidence records                                            | Provenance and limitations recorded      |
| Architecture analyzer | File roles, modules, imports, history         | Organization model, responsibility inventory, dependency findings | Unresolved graph edges disclosed         |
| Finding evaluator     | Criteria and evidence                         | Findings, counter-evidence, contextual risk                       | Each claim has an adequate basis         |
| Scoring engine        | Criterion results and fixed policy            | Scores, intervals, coverage, caps, gates                          | Computation reproducible                 |
| Report generator      | Validated structured records                  | Human-readable report                                             | No independent recalculation in prose    |
| Validator             | Structured model and generated report         | Validation results                                                | Material errors block final publication  |

Complete each stage before the next.

A stage's publication condition unmet keeps the downstream record out of the model.

## The Model Artifact

The audit maintains `work/audit-model.json` inside the audited repository's `work/` tree (or its
`temp`/`temporary` convention), gitignored scratch per `docs/MAINTENANCE.md` retention rules.

Top-level shape:

```json
{
 "model_version": 1,
 "scope": {
  "subject": "<name>", "revision": "<full identity>", "purpose": "<audit purpose>",
  "evidence_mode": "source-only", "scoring_policy": 2,
  "history": "present|absent|out-of-scope", "product_profile": {},
  "projects": [
   {"path": "...", "name": "<project name>", "provenance": "in-tree|submodule|embedded",
    "fetch_state": "fetched|unfetched|n/a", "pin_state": "pinned|ahead|n/a",
    "automation_census": "signals|external|none"}
  ]
 },
 "inventory": [
  {"path": "...", "class": "production|test|test-support|generated|vendored|example|script",
   "module": "...", "read": true, "excluded_reason": null}
 ],
 "criteria": [
  {"id": "SEC-AUTHZ", "source": "...", "applicability": "applicable",
   "criticality": "high", "weight": 1.0, "expected": "...", "method": "...",
   "sufficiency": "...", "dimension": "security",
   "outcome": "PASS", "mastery": null, "na_basis": null, "shortfall": null}
 ],
 "evidence": [
  {"id": "EVD-001", "kind": "INSPECTED", "collector": "...", "method": "...",
   "timestamp": "...", "tool": null, "locator": {"path": "...", "lines": [1, 40]},
   "procedure": null, "result": "...", "claims": ["SEC-AUTHZ"],
   "limits": "...", "sampling": "full", "counter": "...", "redaction": "none",
   "unavailable": null}
 ],
 "findings": [
  {"id": "FND-SEC-001", "criterion": "SEC-AUTHZ", "type": "Concern",
   "severity": "HIGH", "claim_class": "confirmed defect", "observation": "...",
   "property": "...", "evidence": ["EVD-001"], "counter": "...",
   "consequence": "...", "scope": "...", "confidence": "HIGH",
   "status": "Open", "absence": null, "next_verification": "..."}
 ],
 "risks": [
  {"id": "RSK-001", "finding": "FND-SEC-001", "impact": "...", "likelihood": "...",
   "scope": "...", "prerequisites": "...", "controls": "...", "uncertainty": "...",
   "rule": "impact x likelihood matrix", "severity": "HIGH"}
 ],
 "recommendations": [
  {"id": "REC-001", "finding": "FND-SEC-001", "postcondition": "...",
   "options": "...", "owner": "...", "effort": "...", "verification": "...",
   "residual": "...", "priority": "P1"}
 ],
 "scores": {
  "scale_max": 10,
  "dimensions": {
   "security": {"mastery": 0.7, "uncapped": 7, "score": 5, "interval": [4, 5],
                "coverage": 0.9, "eligible": true,
                "caps": [{"rule": "severity-high", "limit": 5,
                          "source": ["FND-SEC-001"]}]}
  },
  "overall": {"score": null, "scored": 0, "applicable": 0},
  "per_project": {}
 },
 "coverage": {"families": {}, "labels": {}},
 "exclusions": ["..."]
}
```

`model_version` is `1` for this schema.

Criterion `dimension` values are the canonical ids in `process/readiness-scoring.md`
(scoring policy 2) - snake_case keys like `security` and `delivery_continuity`, never the
legacy `process` bucket or kebab-case; a process-family criterion names its own dimension
(`delivery_continuity`, `ai_provenance`, `originality_licensing`, `skill_definition`).
Multi-project models prefix each dimension key with the project `name` (`<project>.security`)
and publish `scores.per_project` while `overall.score` stays null.

`NOT_APPLICABLE` criteria carry `na_basis` (`deployment-model`, `census-none`, or
`history-out-of-scope`), and `PARTIAL`/`FAIL` criteria carry either an open finding or a
recorded `shortfall` with evidence per the deduction-traceability rule in
`process/readiness-scoring.md`.

Criterion-to-evidence linkage runs through `evidence[].claims` - each evidence record names
the criterion ids its result supports, and a criterion is scored-relevant only when at least
one resolved criterion carries `INSPECTED`, `STATICALLY_DERIVED`, `EXECUTED`, or `MEASURED`
evidence per the eligibility gate in `process/readiness-scoring.md`. A dimension that fails
the gate omits its `score` and `eligible` fields entirely rather than recording a zero.

Each scored dimension's `interval` records the substitution bounds: `lo` recomputes mastery
with every unresolved applicable criterion treated as `FAIL`, `hi` treats them as `PASS`,
and a degenerate interval (`lo` equals `hi`) is omitted.

The `projects[]` scope record carries the intake discovery: each project's provenance, fetch
state, pin state, and automation signal census outcome, recorded before criterion planning so
applicability decisions cite the census.

The artifact lives until validation passes, then follows the `work/` retention rule for report
parts - deleted before delivery unless the user asks to keep it.

The sibling `work/audit-state.json` tracks the run itself - phases, gate resolutions, and
declared artifacts - per `process/run-state.md`. The model holds audit data, the state file
holds run progress, and neither duplicates a field the other owns. Both keep a single writer:
the parent agent writes them, delegated scouts never do.

## Derivation Rule

Every findings summary row, register entry, score cell, count, coverage label, and executive
claim renders from the model.

No prose recalculates, restates, or invents a number the model does not already hold - a count
mentioned in a description equals the count in the classified records that produced it.

When a summary and a detail disagree, the model is wrong or the prose drifted. Both are
resolved against the records, never edited independently.

Finding, evidence, risk, recommendation, debt, and checklist IDs stay stable between the model
and every rendering of it - a ledger row cites the model's `EVD` identifier verbatim, it is
never renumbered in prose.

## Generation Contract

The report-generator stage renders only what the model holds:

- Identifiers allocate in model order - findings first, then risks, recommendations, and PAR
  rows - and no rendering renumbers them.
- Every number in the report - counts, scores, intervals, aggregates - equals a model value,
  and prose never recalculates.
- A final report carries no unfilled placeholder: any `<...>` skeleton token still present is a
  publication stop.
- An incomplete model renders an explicitly incomplete report with the missing stages named
  in the Validation Protocol - never a silent gap.
- The PAR budget stays at 20 rows regardless of recommendation count.

## Model Quality Checks

Before generation, `scripts/check-model.py <work/audit-model.json>` verifies the artifact
mechanically:

- Referential integrity: finding criteria and evidence, risk and recommendation findings, and
  evidence claims all resolve to declared identifiers.
- Outcome validity: criterion outcomes come from the declared state set, `PARTIAL` carries a
  recorded mastery fraction, and `CRITICAL`/`HIGH` findings carry counter-evidence.
- Scoring reproducibility: each dimension's score, interval bounds, coverage, and eligibility
  recompute from criterion outcomes, weights, and backing evidence kinds, and the overall row
  matches the eligible dimension set and its mean.

A model that fails these checks is not generated from. The failures are resolved in the
records first, per the Derivation Rule.

## Counter-Evidence Review

After the deterministic validation pass, run a separate counter-evidence review before
finalizing.

Challenge both inflated praise and unsupported defect claims.

For every `CRITICAL`/`HIGH` finding and every favorable `PASS` that gates a score, ask what
observation would refute it and record the answer in the finding's `counter` field.

Retain disagreements and their disposition reasons in the model. A resolved disagreement is
recorded, never erased.

This pass is a second sequential evaluation by the same auditor. Parallel agents are not
required.

## Publication Stops

The generator stops final publication on:

- Arithmetic errors: a score, interval, count, or aggregate that does not recompute.
- Unsupported headline readiness: a readiness or eligibility claim whose gates are not met.
- Material evidence/claim mismatch: a claim citing a record that cannot establish it.
- Broken semantic references: an identifier that resolves to the wrong problem, not merely a
  missing one.

A stopped publication may still emit the report as a clearly labeled incomplete artifact. It
names the unresolved errors in the Validation Protocol.
