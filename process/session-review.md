# Session Review

## Purpose

> **Scope:** Procedure for improving the skill from the current session's history
> **Key items:** session gather, findings, approval gate, review modes, rule-file
> application, validation

This file defines the session-review path of skill maintenance: the agent reviews what
happened in this conversation, extracts the lessons worth keeping, and lands them in the
rule corpus.

Follow it when the request asks to improve this skill from this session - "improve
lens-skill", "improve the skill from this session", "review the session for lessons".

## Modes

Two optional flags named in the request modify how the review's question surfaces behave -
"improve lens-skill from this session, autonomously".

- **Autonomous** - `autonomous`, `automatic`, `unattended`, or `non-interactive`. Every gate
  in this procedure resolves to its recommended option without waiting, and the completion
  report carries a `Decisions:` list naming each resolved surface and the option taken.
- **Verbose** - `verbose`. Every surface additionally reports the full option list and the
  rationale for the recommended choice, whether the surface was asked or auto-resolved.

The flags may stack. Autonomous plus verbose resolves every gate and reports all options.

Autonomous mode resolves only this procedure's own gates: it never commits, and a session
that yields no findings still reports and stops rather than inventing changes.

## Procedure

### Gather

Read the session's conversation history, across thread boundaries when a summary split
occurred.

List what failed, surprised, or needed a workaround, and every assumption the session made -
validated or broken.

Verify real state before recording a lesson: re-check files, rerun commands, confirm the
reported behavior - no guessed findings.

### Findings

Map each durable lesson to the rule file or files it belongs in.

A lesson about audit process or report structure goes to `process/` or `synthesis/`, a
lesson about assessment coverage goes to `assessment/`, a lesson about evidence or
neutrality goes to `principles/`, a lesson about reference data goes to `references/`, and
a lesson about tool behavior goes to `scripts/` or `tests/`.

A structural proposal larger than a single rule edit lands as a plan in the gitignored
`work/` workspace instead, per `AGENTS.md` - the review record names the plan file.

Drop lessons already covered by existing rules - the findings list names gaps, not
repetitions.

The anonymized-examples rule from `docs/MAINTENANCE.md` applies: findings describe the
lesson with skill-owned examples, never with names or paths of an audited project.

### Approval

Report the findings and the proposed changes per rule file.

Ask for approval before editing. Under JSON exchange the gate emits as the
`session-review-approval` `choice` parameter per `process/json-exchange.md`.

The gate offers `Apply` (recommended), `Adjust`, and `Cancel`.

`Adjust` accepts a free-text correction to the findings or the proposal and re-presents the
report.

Under autonomous mode the gate resolves to `Apply` without asking and the resolution is
recorded in the decisions list, per Modes above.

### Apply

On approval, edit the named rule files per `docs/MAINTENANCE.md` and `docs/STYLE.md`.

Apply the registration contract when the change adds, removes, or renames a resource -
`SKILL.md`, the `README.md` directory tree, `## Contents` tables, and `evals/evals.json`
move together.

### Validate

Run the skill-maintenance suite from `docs/CONTRIBUTING.md` after the edits and report every
check that ran, failed, or was skipped.

## What Does Not Apply

- No audit machinery runs. Parameter resolution, evidence modes, and report contracts do
  not apply to the skill's own files.
- No separate findings log is kept - findings land directly in the rule files they correct,
  except structural proposals recorded as `work/` plans.
- The session's audit output is not part of the review - the review extracts transferable
  rules, not a report of the audit itself.

## Relation To Maintenance

This file is the session-review path inside skill maintenance.

The `Maintain the skill` operation routes to it when the request asks to improve the skill
from the session, and `docs/MAINTENANCE.md` governs the edits it produces.
