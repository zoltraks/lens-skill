# Organization Model And Responsibility Inventory

## Purpose

> **Scope:** The organization model an audit builds from the structure scan, and the
> responsibility inventory that maps what each area actually does
> **Key items:** area map, declared versus observed responsibility, responsibility
> inventory, producer-consumer edges, ownership findings

This file defines the two intermediate artifacts the architecture-analyzer stage of
`process/audit-model.md` builds before structural findings are evaluated.

They answer two questions: what does the tree claim to be, and what does each part of it
actually do.

Apply `principles/evaluation-rules.md` throughout.

## Contents

| Section                  | Line | What it covers                                 |
|--------------------------|------|------------------------------------------------|
| Organization Model       | 27   | Area map from scan census plus declared roles  |
| Responsibility Inventory | 51   | What each area implements, with evidence       |
| Producer-Consumer Edges  | 83   | Cross-boundary edges inside the inventory      |
| Findings The Model Feeds | 95   | Which structural findings the artifacts ground |

## Organization Model

The organization model is the audit's record of how the subject organizes itself - built
from the `scripts/scan-structure.py` census and named documentation, never from a universal
directory template.

Build it once per project, in `work/audit-model.json` or the audit's notes:

| Field           | Content                                                           |
|-----------------|-------------------------------------------------------------------|
| `area`          | Top-level directory, module root, or `.` for loose root files     |
| `files`         | File count from the scan                                          |
| `class_mix`     | Production/test/doc/config/etc. split from the scan               |
| `declared_role` | Role a README, manifest, package doc, or convention assigns, null |
| `observed_role` | Role the auditor assigns from inspected content, null until read  |
| `entry_points`  | Located executables, handlers, exported surfaces                  |
| `depth_fanout`  | Maximum depth and widest fan-out inside the area                  |

A `declared_role` comes only from an inspected statement - a folder convention guess is
recorded in `observed_role` with its basis, never as a declared role.

Record every area, including empty, generated, vendored, and excluded ones - exclusions
name their reason per `references/evidence-schema.md` coverage rules.

## Responsibility Inventory

The responsibility inventory lists what each area actually implements, one row per
responsibility:

| Field            | Content                                                         |
|------------------|-----------------------------------------------------------------|
| `responsibility` | What the component does, in its own terms                       |
| `area`           | Where it lives                                                  |
| `evidence`       | `EVD-NNN` records or `path:line` anchors that establish it      |
| `consumers`      | Areas that call, import, or configure it, when traced           |
| `producers`      | Areas it calls or depends on, when traced                       |
| `state`          | `active`, `dead`, `stub`, `generated`, `dormant`, `unresolved`  |
| `notes`          | Ambiguity, competing copies, or naming-versus-behavior mismatch |

Every non-trivial production area earns at least one row - a populated directory with no
identifiable responsibility is itself a finding input, not a skip.

`state` values:

- `active` - reachable from an entry point or consumer.
- `dead` - present but unreachable by any traced path.
- `stub` - a placeholder body standing for the declared capability.
- `generated` - produced by tooling, recorded once and excluded from manual-quality
  judgments.
- `dormant` - present and coherent but exercised only by optional paths.
- `unresolved` - responsibility could not be determined from inspected evidence, recorded
  with what would resolve it.

A responsibility claimed by two areas is recorded under both with the overlap noted -
competing ownership is evidence, not an error in the inventory.

## Producer-Consumer Edges

Cross-boundary edges come from import, route, interface, or configuration traces - the same
evidence the boundary-trace probes in `process/audit-workflow.md` gather.

Each edge names producer area, consumer area, and the mechanism (import, DI registration,
route mount, event channel, shared file).

Unresolved edges - dynamic imports, string-built paths, reflection - are listed as
`unresolved` with their mechanism, per the architecture-analyzer stage's disclosure
condition.

## Findings The Model Feeds

The organization model and responsibility inventory ground these judgments:

- Catch-all directories: areas whose observed responsibilities span unrelated domains.
- Misplaced or dead components: rows in `dead` or `unresolved` state, or observed roles
  contradicting the declared role.
- Competing organizational models: adjacent areas organized on different principles with
  no recorded rationale.
- Structural duplication: parallel areas implementing the same responsibility.
- Naming-versus-behavior drift: an observed role that contradicts the area's name or
  declared role.
- Unread coverage: areas with no `observed_role` and no read-depth record - a coverage
  gap, never silently treated as `PASS`.

A finding about structure cites the inventory row and the evidence behind it - the
inventory is the intermediate record, the finding is the conclusion.
