# History Schema

## Purpose

> **Scope:** The canonical `history.json` dataset schema consumed by lifecycle
> visualisation interfaces **Key items:** top-level fields, project, categories,
> version records, stats, events, nullability, producer contract

This document is the field contract for the dataset produced by
`process/history-visualisation.md`.

The producer emits one `history.json` file plus an identical JavaScript shim -
both serialize the same object.

Example values below use generic placeholder versions such as `2.1.0` and
invented hashes.

## Top Level

| Field        | Type     | Contents                                   |
|--------------|----------|--------------------------------------------|
| `schema`     | integer  | Schema version, currently `1`              |
| `project`    | object   | Project identity and coverage, see Project |
| `categories` | object[] | Event category registry, see Categories    |
| `versions`   | object[] | Version records ordered oldest to newest   |

## Project

| Field         | Type         | Contents                                 |
|---------------|--------------|------------------------------------------|
| `name`        | string       | Project name                             |
| `description` | string, opt. | Short description, omitted when unknown  |
| `repository`  | string       | Source path or remote name               |
| `generated`   | string       | Build timestamp                          |
| `head`        | string       | HEAD commit hash at generation time      |
| `commits`     | int          | Total commit count covered               |
| `span`        | object       | `{"from": ISO, "to": ISO}` date coverage |

## Categories

Each category is `{"id", "label", "color", "order"}`.

- `id` - machine key every event `type` resolves to.
- `label` - display name.
- `color` - `#rrggbb` interface accent.
- `order` - sort position, spacing of tens leaves room for insertion.

The registry carries one entry per event family - features, changes, refactors,
fixes, plans, releases, reports, tests, decisions, lessons, discards,
and similar - plus a `release` entry used by version-tower styling.

## Version Record

| Field             | Type           | Contents                                                |
|-------------------|----------------|---------------------------------------------------------|
| `version`         | string         | Semantic version string                                 |
| `kind`            | enum           | `release` `changelog` `developing` `planned`            |
| `range`           | object, opt.   | `{"from": sha, "to": sha}` commit boundaries            |
| `dates`           | object, opt.   | `{"from": ISO, "to": ISO}` activity span                |
| `stats`           | object, opt.   | Measured at the boundary commit, see Stats              |
| `metrics`         | object, opt.   | Process-assessment measures, see Metrics                |
| `commit_span`     | int[], opt.    | `[first, last]` commit indices into the commit list     |
| `events`          | object[]       | Development events inside the era, see Events           |
| `summary`         | string, opt.   | Prose rollup of the era's work                          |
| `changelog_items` | object[], opt. | `{"subject", "text"}` entries found in changelog docs   |
| `eventCounts`     | object         | `{category-id: count}` totals for interface rendering   |
| `gapDays`         | int            | Quiet days between this version and the previous        |
| `superseded`      | bool, optional | True when a later record reuses the same version number |
| `planned`         | bool, optional | True on `planned` records                               |

Kinds differ by provenance: `release` has a manifest or tag boundary,
`changelog` exists only in documents, `developing` is open at HEAD,
and `planned` has records but no code.

`dates` is absent on `planned` records - date arithmetic must skip them,
because an empty or missing bound would hijack range resolution.

## Stats

| Field     | Type   | Contents                                                 |
|-----------|--------|----------------------------------------------------------|
| `loc`     | object | `{"src", "test", "docs", "other", "total"}` line counts  |
| `files`   | object | `{"src", "test", "docs", "other", "total"}` file counts  |
| `deps`    | object | `{"prod", "dev"}` dependency counts                      |
| `delta`   | object | `{"ins", "del"}` insertions and deletions across the era |
| `commits` | int    | Commit count inside the era                              |

All stats are measured at the version's own boundary commit,
never at HEAD.

`stats` is absent on `planned` records, and `delta` is absent when no
insertion/deletion measurement exists for the era.

## Metrics

The `metrics` block carries process-assessment measures that let the
interface compare eras and surface problems, not only display events:

| Field       | Type   | Contents                                                       |
|-------------|--------|----------------------------------------------------------------|
| `days`      | int    | Era duration in days (first to last commit date)               |
| `testRatio` | float  | `loc.test / loc.src` at the boundary commit                    |
| `modules`   | object | `{module: {src,test,docs,other,total,ins,del}}` - per top-level |
|             |        | directory LOC at the boundary plus era churn                    |
| `hotspots`  | array  | `[{"file", "commits"}]` most-touched files of the era           |
| `authors`   | object | `{name: commits}` author activity inside the era               |
| `commitMix` | object | `{type: count}` classified commit-type distribution, e.g.      |
|             |        | `{"feature": 8, "fix": 3, "docs": 2}`                          |

`commitMix` counts only commit events (those carrying `ins`/`del`), never
documentation or dependency events, so it describes engineering focus.
Module keys are the repository's own top-level directories - the producer
derives them from the tree, never from a fixed list.
`metrics` is absent on `planned` and `changelog` records.

## Events

| Field      | Type           | Contents                                       |
|------------|----------------|------------------------------------------------|
| `type`     | string         | A category `id` from the registry              |
| `title`    | string         | Human-readable description                     |
| `date`     | string         | ISO timestamp                                  |
| `sha`      | string, opt.   | Commit hash for commit-sourced events          |
| `ins`      | int, optional  | Insertions for commit events                   |
| `del`      | int, optional  | Deletions for commit events                    |
| `ref`      | string, opt.   | Document path for documentation-sourced events |
| `archived` | bool, optional | True when `ref` lives in an archived tree      |

Report-family records (audits, hunts, reviews, assessments, proposals,
reports) may additionally carry extracted fields:

| Field             | Type          | Contents                                          |
|-------------------|---------------|---------------------------------------------------|
| `score`           | string, opt.  | Overall score as printed, e.g. `"7.3/10"`         |
| `verdict`         | string, opt.  | Outcome word or phrase (Pass, REQUEST CHANGES, Red) |
| `findings`        | int, opt.     | Unique finding-id count found in the record       |
| `revision`        | string, opt.  | Report revision, e.g. `"1.8"`                     |
| `subject_version` | string, opt.  | Project version the record assesses               |

A change-request record may carry `subtype` (`feature`, `fix`, `refactor`,
`chore`) which the producer folds into the event `type` at merge time.

Dependency-change events use the `dependency` category and carry a `dep`
object:

| Field      | Type           | Contents                                    |
|------------|----------------|---------------------------------------------|
| `name`     | string         | Package or image name                       |
| `manifest` | string         | Manifest path, e.g. `server/Cargo.toml`     |
| `kind`     | string         | Channel: `prod`, `dev`, `build`, `indirect` |
| `action`   | string         | `added`, `bumped`, or `removed`             |
| `from`     | string, opt.   | Previous declared version (absent on added) |
| `to`       | string, opt.   | New declared version (absent on removed)    |

Every event carries a traceable source: `sha` for commit events,
`ref` for documentation events.

An event with neither is a fabrication and fails verification.

## Nullability

- No field serializes as `null`: a key with no value is omitted entirely.
- `range`, `dates`, `stats`, `commit_span`, `summary`, `changelog_items`
  appear only when a source supplies them.
- `events` and `eventCounts` are always present, empty when nothing matched.
- `superseded`, `planned`, `archived`, `ins`, `del`, `sha`, `ref`
  are likewise omitted rather than `false` or `0`.
- Consumers must treat a missing key as "unknown" - `undefined` and `null`
  reads are equivalent, so loose checks (`v.dates &&`, `s.delta || {}`)
  stay correct.

## Producer Contract

- One data object emits both `history.json` and the JavaScript shim
  (`prototype/js/history-data.js` shape) - the shim assigns the object
  to a global the interface reads when `fetch` is unavailable.
- Versions serialize oldest to newest.
- Events serialize in chronological order inside each version.
- Numbers are integers, dates are ISO strings, no trailing metadata.
