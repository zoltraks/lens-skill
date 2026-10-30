# Decision Modes

## Purpose

> **Scope:** The interaction-mode contract for every Lens operation - how question
> surfaces, gates, and gated actions resolve in each mode
> **Key items:** mode selection, the automated run, resolution precedence, reporting
> flags, permission boundary

This file is the authoritative definition of the interaction modes named in
`SKILL.md` and `process/audit-workflow.md`.

Every procedure resolves its question surfaces through this matrix.

The session review keeps the shared two-flag review contract of
`process/session-review.md` - the `autonomous` and `verbose` semantics there and here
are the same.

## Mode Selection

Classify the request first, then record the interaction mode once at intake and carry
it through the run, including a re-audit.

- `automated`, `autonomous`, `unattended`, `non-interactive`, `fully autonomous`, or
  "without asking" wording records the run as `automated` before any gate resolves.
  The canonical name in shared text is `autonomous` - `automated` is this
skill's recorded alias for the same tier. Lens keeps a single no-questions tier - `fully autonomous` resolves to the same
  `automated` mode, no stronger mode exists.
- `verbose`, `informational`, `diagnostic`, and `timing` are reporting flags that
  change what the run emits, never what it decides or is permitted to do, per
  `process/json-exchange.md` and `process/operation-timing.md`.
- Explicit parameter statements in the request outrank every detected or default
  resolution.
- A bare activation with no task stays informational standby in every mode - no
  question surfaces exist to resolve.

## The Matrix

| Mode                  | Blocking gates and routine prompts                         | Missing inputs                       | Separately gated actions            |
|-----------------------|------------------------------------------------------------|--------------------------------------|-------------------------------------|
| Interactive (default) | Ask at every gate per `process/audit-workflow.md`.         | Ask before dependent work.           | Seek the required permission.       |
| Automated             | Resolve to the discovered or default answer, no questions. | Record `UNKNOWN` or `NOT SPECIFIED`. | Seek permission or skip and report. |

A gate is a point where the run cannot proceed without an answer - audit mode,
project inclusion, parameter acceptance, report delivery - not every routine
sub-step.

## Gate Semantics

The interaction mode is classified once at intake and never re-litigated at a later gate.

Host signals urging fewer questions apply to the agent's own discretionary prompts, never
to the workflow's blocking gates, and a user who answered several gates in a row was being
patient, not setting policy - each gate is a fresh surface.

A gate or phase is recorded as resolved only after the answer arrives - `run.phase` and
`completed_phases` in `work/audit-state.json` never advance ahead of the response, per
`process/run-state.md`.

Every pending surface is presented - before a gate fires, the agent confirms no pending
surface was omitted, because a gate that skips a surface is a protocol defect, not a
shortcut.

Each decision is its own question with its own option set - flattening several decisions'
options into one list lets an answer select conflicting options or none at all.

Anti-patterns:

| Anti-pattern                                      | Why it is wrong                                                                             |
|---------------------------------------------------|---------------------------------------------------------------------------------------------|
| Proceeding past a gate without an answer          | The run loses the recorded decision downstream steps depend on                              |
| Announcing a pause without a blocking wait        | Words are not pauses - the surface must actually await the response                         |
| Marking a phase resolved before its gate answers  | State records a false completion and later phases act on it                                 |
| Re-classifying the mode at each gate              | Intake decided it once; re-opening it lets a "minimize questions" hint swallow a checkpoint |
| Flattening several decisions into one option list | The answer can select conflicting options or none at all                                    |
| Skipping the `gates` record under automated mode  | Automated resolutions record exactly like answered questions                                |

## Resolution Precedence

Resolve each surface in this order, and record which tier supplied the answer:

1. An explicit user choice or parameter statement.
2. The target's own rules and conventions.
3. Discovered evidence from the audited repository.
4. A documented Lens default.
5. `UNKNOWN` or `NOT SPECIFIED`.

Never manufacture a missing input or claim a verified state a source-only inspection
cannot show.

## Automated Recording

Every automated resolution is recorded exactly like an answered question - the same
working notes, the same `work/lens-params.json`, and the same completion-message
disclosure, per `process/audit-workflow.md`.

The skill update check applies its merge without asking when the reported state
allows it, and the run continues with a brief note when it does not.

## Reporting Flags

`verbose` adds the offered options and rationale to every resolved surface and never
changes a selection or a gate.

`informational` arms the timing report alone, while `diagnostic` and `timing` also
emit the `process/json-exchange.md` parameter document for every pending surface.

## Permission Boundary

No mode builds, tests, or executes the audited project, and no mode commits, pushes,
or publishes.

An automated run still produces the bounded report on what the evidence shows rather
than claiming the surfaces it skipped.
