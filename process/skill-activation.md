# Skill Activation

## Purpose

> **Scope:** Standby procedure for a request that names Lens but no operation.

> **Key items:** referent resolution, standby, enablement response

`use lens`, `run lens`, `work on lens-skill`, or host-native invocation without a task names this
procedure.

## When This Applies

A generic phrase ("use skill", "use this skill", "work on this skill") binds to Lens only when the
context identifies it - the lens-skill repository is the target, the session already uses Lens,
or no other skill competes - otherwise ask which skill is meant and wait.

A named target, a purpose qualifier ("for audits"), or a mode without an operation stays standby,
never a mode-selection question.
Activation joined to a task ("run lens, audit this repository") is a task request and skips this
file.

## Procedure

On a bare `use`, follow `process/skill-update.md` when the request names
`improvement`, `development`, or `training`, or makes an explicit update request.
A request naming no mode uses the installed package.
Reuse this session's result for the checkout when available.
Continue with the installed package when the check cannot run.

1. Treat the loaded `SKILL.md` as the enabled state.
2. Print the enablement response in the language of the request.
3. Ask any pending question through the host's question tool, then wait for the named operation.

## Enablement Response

Without a target, one sentence confirms enablement, one names the skill and its `metadata.version`,
then an `Operation` and `What it covers` table lists Audit, Hunt, Review, Re-audit, Focused review,
Skill audit, Audit request, and Maintain the skill, and a line invites the task.

With a target, including `work on lens-skill`, one or two lines confirm enablement on it - no
roster.

A named mode folds into the opening sentence, such as "enabled in timing mode".

## What Does Not Apply

No intake, target scan, or task guessing runs, and no file is written.
No rule file loads beyond the router and this file - a `verbose` or `diagnostic` mode adds
`process/json-exchange.md`, and a `timing`, `context usage`, or `informational` mode adds only
`process/operation-timing.md`.

## Relation To The Modes

Standby precedes audit work and skill maintenance, and the next task-bearing request routes per
`SKILL.md`.
