# Audit Model

## Purpose

> **Scope:** The canonical intermediate model every audit builds and the stage pipeline that
> separates collection, interpretation, scoring,
> and presentation **Key items:** `work/audit-model.json`, stage table, derivation rule,
> counter-evidence pass, publication stops

This file defines the machine-readable intermediate model that makes the audit reproducible.

The model is the single structured record an audit's tables, registers, scores,
and summaries render from - the report writer never invents facts, counts,
or scores while composing prose.

Apply `principles/evaluation-rules.md` throughout.

Evidence kinds and record fields live in `references/evidence-schema.md`,
and criteria records live in `references/criteria-catalogue.md`.

## Contents

| Section                 | Line | What it covers                                   |
|-------------------------|------|--------------------------------------------------|
| Pipeline Stages         | 31   | The nine stages and their publication conditions |
| The Model Artifact      | 49   | `work/audit-model.json` schema and lifecycle     |
| Derivation Rule         | 209  | Rendering every surface from the model           |
| Counter-Evidence Review | 267  | The second-pass challenge discipline             |
| Publication Stops       | 282  | Errors that block final publication              |

## Pipeline Stages

| Stage                 | Inputs                                        | Required output                                                   | Publication condition                    |
|-----------------------|-----------------------------------------------|-------------------------------------------------------------------|------------------------------------------|
| Scope resolver        | User purpose, source availability, deployment | Audit contract and revision identity                              | Scope and evidence mode explicit         |
| Inventory collector   | Repository files, manifests, module roots     | File inventory and exclusion record                               | Every in-scope source file accounted for |
| Criteria planner      | Product context, criteria catalogue           | Applicability and method matrix                                   | `N/A` decisions justified                |
| Evidence collectors   | Source, config, supplied artifacts, execution | Typed evidence records                                            | Provenance and limitations recorded      |
| Architecture analyzer | File roles, modules, imports, history         | Organization model, responsibility inventory, dependency findings | Unresolved graph edges disclosed         |
| Finding evaluator     | Criteria and evidence                         | Findings, counter-evidence, contextual risk                       | Each claim has an adequate basis         |
| Scoring engine        | Criteria results and fixed policy             | Scores, intervals, coverage, caps, gates                          | Computation reproducible                 |
| Report generator      | Validated structured records                  | Human-readable report                                             | No independent recalculation in prose    |
| Validator             | Structured model and generated report         | Validation results                                                | Material errors block final publication  |

Complete each stage before the next.

A stage's publication condition unmet keeps the downstream record out of the model.

## The Model Artifact

The audit maintains `work/audit-model.json` inside the audited repository's `work/` tree (or its
`temp` / `temporary` convention), gitignored scratch per `docs/MAINTENANCE.md` retention rules.

Top-level shape:

```json
{
 "model_version": 2,
 "scope": {
  "subject": "<name>", "revision": "<full identity>", "purpose": "<audit purpose>",
  "evidence_mode": "source-only", "scoring_policy": 3, "catalogue_version": 4,
  "history": "present|absent|out-of-scope", "detail_level": "Detailed|Standard|Brief",
  "requirements_baseline": "<sha256 hex>|null", "product_profile": {"natures": ["service"]},
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
  {"id": "SEC-AUTHZ", "catalogue_id": "SEC-AUTHZ", "channel": "score|conformance",
   "source": "...", "applicability": "applicable",
   "criticality": "high", "weight": 1.0, "expected": "...", "method": "...",
   "sufficiency": "...", "dimension": "security",
   "outcome": "PASS", "level": "PASS", "mastery": 1.0, "na_basis": null, "shortfall": null}
 ],
 "requirements": [
  {"id": "A-01", "source": {"path": "...", "line": 1}, "statement": "...",
   "obligation": "mandatory|recommended|optional|future",
   "status": "PASS|PARTIAL|FAIL|UNKNOWN", "evidence": ["EVD-001"],
   "finding": "FND-SEC-001|null"}
 ],
 "evidence": [
  {"id": "EVD-001", "kind": "INSPECTED", "collector": "...", "method": "...",
   "timestamp": "...", "tool": null, "locator": {"path": "...", "lines": [1, 40]},
   "procedure": null, "result": "...", "claims": ["SEC-AUTHZ"],
   "limits": "...", "sampling": "full", "counter": "...", "redaction": "none",
   "unavailable": null}
 ],
 "findings": [
  {"id": "FND-SEC-001", "criteria": "SEC-AUTHZ", "type": "Concern",
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
 "readiness": {"state": "READY|NOT READY|PENDING EVIDENCE|NOT ASSESSED",
               "blocking": ["FND-SEC-001"]},
 "scores": {
  "scale_max": 10,
  "dimensions": {
   "security": {"mastery": 0.7, "uncapped": 7, "score": 5, "interval": [4, 5],
                "coverage": 0.9, "eligible": true,
                "caps": [{"rule": "severity-high", "limit": 5,
                          "source": ["FND-SEC-001"]}]}
  },
  "product": {"score": 7.0, "interval": null, "published": true,
              "eligible_weight": 29, "applicable_weight": 29,
              "lowest": ["testability"]},
  "process": {"score": null, "interval": null, "published": false,
              "scored": 1, "applicable": 2, "lowest": []},
  "single": {"score": 6.0, "raw": 7.0, "interval": null, "flag": "product-only",
             "ceiling": {"limit": 6, "reasons": ["readiness:NOT READY"]},
             "band": "Average"}
 },
 "coverage": {"families": {}, "labels": {}},
 "exclusions": ["..."]
}
```

`model_version` is `2` for this schema.

Criteria `dimension` values are the canonical ids in `process/readiness-scoring.md` (scoring policy
3) - snake_case keys like `security` and `delivery_continuity`,
never the legacy `process` bucket or kebab-case.
a process-family criteria entry names its own dimension (`delivery_continuity`,
`originality_licensing`, `skill_definition`).
Multi-project models prefix each dimension key with the project `name` (`<project>.security`)
and publish the three headline records under `scores.per_project[<name>]` while `scores.product`,
`scores.process`, and `scores.single` stay absent,
and `readiness` becomes `{"per_project": {<name>: {"state", "blocking"}}}`.

Score-channel criteria carry `catalogue_id` naming their entry in the fixed catalogue of
`references/criteria-catalogue.json` - in a single-project model `id` equals `catalogue_id` - and a
resolved criteria entry's `level` comes from that entry's declared anchors.

`scope.scoring_policy` records which policy produced the scores,
so a model written under policy 2 is not a policy-3 model - it fails the check until regenerated
under the fixed catalogue, and `scores.overall` is removed rather than migrated.

`NOT_APPLICABLE` criteria carry `na_basis` (`deployment-model`, `census-none`,
or `history-out-of-scope`), and `PARTIAL` / `FAIL` criteria carry either an open finding or a
recorded `shortfall` with evidence per the deduction-traceability rule in
`process/readiness-scoring.md`.

Criteria-to-evidence linkage runs through `evidence[].claims` - each evidence record names the
criteria ids its result supports, and a criteria entry is scored-relevant only when at least one
resolved criteria entry carries `INSPECTED`, `STATICALLY_DERIVED`, `EXECUTED`,
or `MEASURED` evidence per the eligibility gate in `process/readiness-scoring.md`.
A dimension that fails the gate omits its `score` and `eligible` fields entirely rather
than recording a zero.

Each scored dimension's `interval` records the substitution bounds:
`lo` recomputes mastery with every unresolved applicable criteria entry treated as `FAIL`,
`hi` treats them as `PASS`, and a degenerate interval (`lo` equals `hi`) is omitted.

The `projects[]` scope record carries the intake discovery: each project's provenance, fetch state,
pin state, and automation signal census outcome,
recorded before criteria planning so applicability decisions cite the census.

Scope-model determinations are contracted so two auditors reach the same partition:

- A project's `name` is the basename of its `path` - never an abbreviation or display name,
  so paired audits pair projects mechanically.
- A subject is multi-project when its root manifest aggregates member packages that each ship an
  independently buildable or deliverable artifact - two auditors must reach the same decomposition,
  so the rule is the manifest, not judgment.
  A subject whose root is itself the deliverable is single-project even when it
  carries internal modules.
- A directory that only aggregates sub-projects is not itself a project.
  It becomes one only when it ships first-party code at its own root outside the member trees.
- `automation_census` is mechanical: `none` when no build, CI, packaging,
  or deployment automation files exist under the project root,
  `signals` when in-tree automation exists,
  `external` when automation is declared but lives outside the tree.
  Member crates inherit the workspace root's census when they ship no automation of their own.
- `product_profile.natures` follows the delivered artifact kind - a member crate inherits the
  workspace's natures unless it is independently published as a reusable package,
  in which case `library` applies to that crate alone.
- A criteria entry resolves `UNKNOWN` only when the evidence its `sufficiency` names cannot be
  located or cannot distinguish adjacent levels.
  When partial evidence exists the criteria entry grades at the level that evidence supports -
  `UNKNOWN` is never a shortcut for a hard grading call.

The artifact lives until validation passes,
then follows the `work/` retention rule for report parts - deleted before delivery unless the
user asks to keep it.

The sibling `work/audit-state.json` tracks the run itself - phases, gate resolutions,
and declared artifacts - per `process/run-state.md`.
The model holds audit data, the state file holds run progress,
and neither duplicates a field the other owns.
Both keep a single writer: the parent agent writes them, delegated scouts never do.

## Derivation Rule

Every findings summary row, register entry, score cell, count, coverage label,
and executive claim renders from the model.

No prose recalculates, restates, or invents a number the model does not already hold - a count
mentioned in a description equals the count in the classified records that produced it.

When a summary and a detail disagree, the model is wrong or the prose drifted.
Both are resolved against the records, never edited independently.

Finding, evidence, risk, recommendation, debt,
and checklist IDs stay stable between the model and every rendering of it - a ledger row cites the
model's `EVD` identifier verbatim, it is never renumbered in prose.

## Generation Contract

The report-generator stage renders only what the model holds:

- Identifiers allocate in model order - findings first, then risks, recommendations,
  and PAR rows - and no rendering renumbers them.
- Every number in the report - counts, scores, intervals, aggregates - equals a model value,
  and prose never recalculates.
- A final report carries no unfilled placeholder:
  any `<...>` skeleton token still present is a publication stop.
- An incomplete model renders an explicitly incomplete report with the missing stages named in the
  Validation Protocol - never a silent gap.
- The PAR budget stays at 20 rows regardless of recommendation count.

## Model Quality Checks

Before generation, `scripts/check-model.py <work/audit-model.json>` verifies the
artifact mechanically.

`scripts/check-model.py --fix <work/audit-model.json>` recomputes the mechanically derived records
in place - criteria mastery from declared levels,
mechanical criteria from the requirements coverage, `scope.requirements_baseline`,
`scores.dimensions` records with caps and intervals,
and the `product` / `process` / `single` or `per_project` headline - so model authoring declares
outcomes and the fixer computes the records, then re-runs the check.


- Referential integrity: finding criteria and evidence, risk and recommendation findings,
  and evidence claims all resolve to declared identifiers.
- Outcome validity: criteria outcomes come from the declared state set,
  `PARTIAL` carries a recorded mastery fraction,
  and `CRITICAL` / `HIGH` findings carry counter-evidence.
- Catalogue conformance: score-channel criteria match the fixed catalogue on id, dimension, weight,
  criticality, declared `level` anchors, and `na_rules`, completeness holds per project,
  and the `requirements[]` registry matches `scope.requirements_baseline`.
- Scoring reproducibility: each dimension's score, interval bounds, coverage,
  and eligibility recompute from criteria outcomes, weights, and backing evidence kinds,
  and the `product`, `process`, and `single` headline records recompute from the dimension set under
  the catalogue's tier weights, publish gates, blend, and ceilings.

A model that fails these checks is not generated from.
The failures are resolved in the records first, per the Derivation Rule.

## Counter-Evidence Review

After the deterministic validation pass, run a separate counter-evidence review before finalizing.

Challenge both inflated praise and unsupported defect claims.

For every `CRITICAL` / `HIGH` finding and every favorable `PASS` that gates a score,
ask what observation would refute it and record the answer in the finding's `counter` field.

Retain disagreements and their disposition reasons in the model.
A resolved disagreement is recorded, never erased.

This pass is a second sequential evaluation by the same auditor.
Parallel agents are not required.

## Publication Stops

The generator stops final publication on:

- Arithmetic errors: a score, interval, count, or aggregate that does not recompute.
- Unsupported headline readiness: a readiness or eligibility claim whose gates are not met.
- Material evidence/claim mismatch: a claim citing a record that cannot establish it.
- Broken semantic references: an identifier that resolves to the wrong problem,
  not merely a missing one.

A stopped publication may still emit the report as a clearly labeled incomplete artifact.
It names the unresolved errors in the Validation Protocol.
