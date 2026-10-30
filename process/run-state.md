# Run State

## Purpose

> **Scope:** The `work/audit-state.json` run-state artifact - schema, lifecycle, resume,
> and malformed-state handling
> **Key items:** state file contract, phase and gate recording, timestamp discipline,
> resume protocol, single-writer rule

This file defines the run-state record an audit maintains next to the canonical model.

`work/audit-model.json` holds audit data - evidence, criteria, findings, scores.

`work/audit-state.json` holds run progress - phases, gate resolutions, declared artifacts,
and timestamps - so an interrupted audit resumes and a finished one reconciles what it
declared against what is on disk.

Apply this file inside `process/audit-workflow.md`; phases, gates, and the report contract
are unchanged.

## Contents

| Section            | Line | What it covers                            |
|--------------------|------|-------------------------------------------|
| The State Artifact | 32   | `work/audit-state.json` schema            |
| Lifecycle          | 74   | Creation, updates, single-writer rule     |
| Timestamps         | 94   | Clock discipline for every recorded time  |
| Resume Protocol    | 104  | Restarting an interrupted run             |
| Malformed State    | 123  | Stop-and-report rule for a damaged file   |
| Reconciliation     | 137  | Declared-artifact check at finalization   |

## The State Artifact

The audit maintains `work/audit-state.json` inside the audited repository's `work/` tree,
beside `work/audit-model.json` and under the same retention rule - gitignored scratch that
survives until report delivery, then follows the `work/` retention rule for
report-evidence artifacts.

Top-level shape:

```json
{
 "state_version": 1,
 "run": {
  "phase": "<phase name>",
  "started": "<ISO 8601 timestamp or null>",
  "completed_phases": [],
  "failed_phases": []
 },
 "gates": {
  "<surface>": {
   "resolution": "<answer or token>",
   "tier": "explicit|convention|discovered|default|automated|unknown"
  }
 },
 "artifacts": [
  {"path": "<relative path>", "kind": "params|model|part|report|translation",
   "declared_phase": "<phase name>"}
 ],
 "timestamps": {
  "created": "<ISO 8601>",
  "updated": "<ISO 8601>"
 }
}
```

`state_version` is `1` for this schema.

The `gates` map records one entry per resolved question surface - the surface name from
`process/audit-workflow.md` (`audit-mode`, `project-inclusion`, `parameters-acceptance`,
`report-delivery`, and so on), the resolution reached, and the precedence tier that
supplied it per `process/decision-modes.md`.

## Lifecycle

The state file is created at the same moment the audit start timestamp is captured - when
the last parameter question resolves, before the remaining rule documents load.

Early gates that already resolved (audit mode, project inclusion) are recorded into
`gates` at creation with their resolution tier.

Every later phase boundary and gate resolution updates the file: `run.phase` moves to the
current phase, `completed_phases` appends a phase only after that phase's exit surface has
resolved, and `artifacts` gains an entry each time the run declares an output file.

The state file has a single writer - the audit's parent agent.

Delegated scouts under `process/parallel-execution.md` never write it, exactly as they
never write the model.

`run.started` is set once at creation and never rewritten - it is the same timestamp the
`Time taken` computation uses, and a resumed or re-done run keeps the original value.

## Timestamps

Every timestamp written to the state file is read from the system clock in the same turn -
`date` or the host's equivalent - never a date-only guess, never a reconstructed value.

When a real value was not captured - for example a phase whose start predates the state
file - write `null` rather than a plausible time.

A `null` is visibly incomplete; a reconstructed time is silently wrong.

## Resume Protocol

A run interrupted after `work/audit-state.json` exists resumes from the recorded state
instead of restarting.

On resume:

1. Read and validate the state file before any phase work - a malformed file follows the
   Malformed State rule below.
2. Verify each artifact already declared in `artifacts` still exists on disk; absent files
   drop from the declaration and the owning phase reruns.
3. Announce the resume point before continuing - the phase named in `run.phase`, the gates
   already resolved, and the next pending surface.
4. Keep `run.started` unchanged so `Time taken` reports the whole effort, not the resumed
   slice.

A state file that shows the run reached delivery - the report artifact exists and
validation passed - never resumes; the next request starts a fresh run and a fresh file.

## Malformed State

A state file that fails to parse, or whose shape violates the schema above, stops the
workflow.

Report what is wrong - key, line, or shape - and offer the user `Repair` (rewrite the file
from the intended values, then re-validate) or `Let me investigate` (pause the run).

Never repair silently, and never continue a run on a state file that could not be read -
a corrupted record that gets overwritten destroys the resume evidence it existed to keep.

Under an automated run the malformed file is recorded in the completion report and the
run continues without state tracking, rather than fabricating a file.

## Reconciliation

Before the completion message, reconcile the `artifacts` declarations against disk.

Every declared path is checked; a missing artifact produces a `Missing artifacts` block in
the completion report naming the path, its `kind`, and the phase that declared it.

Reconciliation reports, it never repairs - do not regenerate the artifact, re-run the
phase, or silently drop the declaration.

Part files already consumed by report assembly are expected absent and do not report.
