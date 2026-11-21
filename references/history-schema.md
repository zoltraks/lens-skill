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

Read the sections the task needs - grep the `## ` headings for the section map.

## Top Level

| Field        | Type     | Contents                                   |
|--------------|----------|--------------------------------------------|
| `schema`     | integer  | Schema version, currently `2`              |
| `project`    | object   | Project identity and coverage, see Project |
| `view`       | object   | Interface defaults, see View, optional     |
| `categories` | object[] | Event category registry, see Categories    |
| `versions`   | object[] | Version records ordered oldest to newest   |

## Project

| Field         | Type         | Contents                                                      |
|---------------|--------------|---------------------------------------------------------------|
| `name`        | string       | Project name                                                  |
| `description` | string, opt. | Short description, omitted when unknown                       |
| `repository`  | string       | Source path or remote name                                    |
| `generated`   | string       | Build timestamp                                               |
| `head`        | string       | HEAD commit hash at generation time                           |
| `commits`     | int          | Total commit count covered                                    |
| `span`        | object       | `{"from": ISO, "to": ISO}` date coverage                      |
| `grouping`    | string       | Era strategy: `version`, `month`, `quarter`, `year`, or `gap` |

`grouping` records how commits grouped into eras - `version` when
manifest, tag, or changelog boundaries exist (the best choice whenever
present), a calendar period or activity-gap strategy otherwise or when the
intake asked for one.

## Categories

Each category is `{"id", "label", "color", "order"}`.

- `id` - machine key every event `type` resolves to.
- `label` - display name.
- `color` - `#rrggbb` interface accent.
- `order` - sort position, spacing of tens leaves room for insertion.

The registry carries one entry per event family - features, changes, refactors,
fixes, plans, releases, reports, tests, decisions, lessons, discards,
and similar - plus a `release` entry used by version-tower styling.

## View

Optional presentation defaults the dataset declares for the interface:

| Field     | Type         | Contents                                 |
|-----------|--------------|------------------------------------------|
| `layout`  | string, opt. | Default scene layout id the viewer opens |
| `theme`   | string, opt. | Default theme (`dark` or `day`)          |
| `palette` | string, opt. | Default accent palette id                |

A consumer applies `view` only when the user has no stored preference -
persisted choices always win, and a reset falls back to these values
rather than to hardcoded constants.

## Version Record

| Field             | Type           | Contents                                                |
|-------------------|----------------|---------------------------------------------------------|
| `version`         | string         | Era label - a semantic version or a date-period label   |
| `kind`            | enum           | `release` `changelog` `developing` `planned` `era`      |
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
| `categoryDetail`  | object, opt.   | Per-category era evidence, see Category Detail          |
| `planned`         | bool, optional | True on `planned` records                               |

Kinds differ by provenance: `release` has a manifest or tag boundary,
`changelog` exists only in documents, `developing` is open at HEAD,
`era` is a date-grouped activity period produced when the project has no
version boundaries or a date strategy was asked for, and `planned` has
records but no code.

Date-era labels are `YYYY-MM` for `month`, `YYYY-Qn` for `quarter`,
`YYYY` for `year`, and the era's first commit date `YYYY-MM-DD` for `gap`.

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

| Field       | Type   | Contents                                                        |
|-------------|--------|-----------------------------------------------------------------|
| `days`      | int    | Era duration in days (first to last commit date)                |
| `testRatio` | float  | `loc.test / loc.src` at the boundary commit                     |
| `modules`   | object | `{module: {src,test,docs,other,total,ins,del}}` - per top-level |
|             |        | directory LOC at the boundary plus era churn                    |
| `hotspots`  | array  | `[{"file", "commits"}]` most-touched files of the era           |
| `authors`   | object | `{name: commits}` author activity inside the era                |
| `commitMix` | object | `{type: count}` classified commit-type distribution, e.g.       |
|             |        | `{"feature": 8, "fix": 3, "docs": 2}`                           |
| `files`     | array  | `[{"path","loc","module"}]` top ~12 largest src/test files      |
| `aspects`   | object | Quality-aspect telemetry, see Aspects                           |

`commitMix` counts only commit events (those carrying `ins`/`del`), never
documentation or dependency events, so it describes engineering focus.
Module keys are the repository's own top-level directories - the producer
derives them from the tree, never from a fixed list.
A `src/` root splits
one level deeper (`src/components`) so a monorepo's real components surface.
Module entries may also carry `files`, `deps` (`{prod,dev}` from the
module's own manifest), and `added` when the module first appears this era.
`metrics` is absent on `planned` and `changelog` records.

### Aspects

`metrics.aspects` carries quality-aspect measures that let a zoomed
single-version scope render the release as a city of concerns -
every key is omitted when its evidence does not exist:

| Key               | Contents                                                        |
|-------------------|-----------------------------------------------------------------|
| `testability`     | `{ratio, files, cases}` - test/source LOC, test files, case ids |
| `maintainability` | `{avgFile, maxFile, godFiles}` - file-size distribution         |
| `security`        | `{schemes, authDeps}` - security schemes + auth-family deps     |
| `api`             | `{paths, operations}` - declared API surface (e.g. OpenAPI)     |
| `documentation`   | `{ratio, loc, records}` - docs share + doc events of the era    |
| `problems`        | `{findings, fixes}` - finding counts + fix commits of the era   |

## Category Detail

`categoryDetail` maps each category id with era activity to the evidence a
per-category sidebar needs - the category's own measures, never the full
version dump.
Keys appear in registry `order`; a category with no era events and no
relevant churn is omitted, and so is the whole block on a silent era.

| Field     | Type         | Contents                                                  |
|-----------|--------------|-----------------------------------------------------------|
| `events`  | int          | Event count for the category this era                     |
| `ins`     | int, opt.    | Insertions summed over the category's own events          |
| `del`     | int, opt.    | Deletions summed over the category's own events           |
| `churn`   | object, opt. | `{"ins", "del"}` era churn restricted to relevant buckets |
| `modules` | object, opt. | `{module: {"ins","del","loc"}}` per-module churn of the   |
|           |              | relevant buckets plus the module's boundary LOC in them   |
| `loc`     | object, opt. | `{bucket: lines}` boundary LOC of the relevant buckets    |
| `facts`   | object, opt. | Category-specific structured detail, see below            |
| `summary` | string, opt. | One generated sentence from the gathered evidence         |

Relevant buckets: `docs` and `test` map to their own buckets; `feature`,
`change`, `fix`, `refactor`, `chore`, and `release` map to `src` and
`test`; `dependency` and record-driven categories (plans, specs, audits,
and similar) carry no `churn`, `modules`, or `loc` slice - their evidence
is the record itself.
`docs` and `test` may also appear without era events when their own
bucket churned - file-level activity is attributable to them alone,
while code-category churn cannot be attributed to an eventless category.

`facts` is the extension point: producers add keys without a schema
change. Known shapes: `dependency` carries `added`, `bumped`, `removed`
counts, `names` per action, and `prod`/`dev` totals; `test` carries
`cases`, `files`, `ratio`; report-family categories carry `records`,
`archived`, `scores`, `verdicts`, `findings`, `subjects`; `spec` and
`contract` carry `requirements`; changelog carries `items`.

`summary` is generated by deterministic templates over the gathered
evidence - counts, churn, module hotspots, names - and never fabricates
content the gatherers did not find.

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

| Field             | Type         | Contents                                            |
|-------------------|--------------|-----------------------------------------------------|
| `score`           | string, opt. | Overall score as printed, e.g. `"7.3/10"`           |
| `verdict`         | string, opt. | Outcome word or phrase (Pass, REQUEST CHANGES, Red) |
| `findings`        | int, opt.    | Unique finding-id count found in the record         |
| `revision`        | string, opt. | Report revision, e.g. `"1.8"`                       |
| `subject_version` | string, opt. | Project version the record assesses                 |
| `requirements`    | int, opt.    | Count of requirement/use-case ids in a spec record  |

A change-request record may carry `subtype` (`feature`, `fix`, `refactor`,
`chore`) which the producer folds into the event `type` at merge time.

Dependency-change events use the `dependency` category and carry a `dep`
object:

| Field      | Type         | Contents                                    |
|------------|--------------|---------------------------------------------|
| `name`     | string       | Package or image name                       |
| `manifest` | string       | Manifest path, e.g. `server/Cargo.toml`     |
| `kind`     | string       | Channel: `prod`, `dev`, `build`, `indirect` |
| `action`   | string       | `added`, `bumped`, or `removed`             |
| `from`     | string, opt. | Previous declared version (absent on added) |
| `to`       | string, opt. | New declared version (absent on removed)    |

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
- `categoryDetail` keys serialize in registry `order`.
- Numbers are integers, dates are ISO strings, no trailing metadata.
- The dataset is reproducible: a re-run at the same ref emits identical
  content apart from `project.generated`.
