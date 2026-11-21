# History Visualisation

## Purpose

> **Scope:** The named lifecycle operation that produces a `history.json` dataset from
> a project's development record **Key items:** activation contract, workspace layout,
> ref selection, gathering sources, extraction pipeline, schema, verification

This document governs the `history visualisation` and `lifecycle visualisation` operation.

The operation turns a project's development history into a canonical JSON dataset
(`history.json`) that a visualisation user interface consumes, and optionally produces
the prototype interface itself.

It is not an audit and produces no report.

## Activation Contract

The operation runs only when the request names it - phrases such as
"create a history visualisation", "visualise the project lifecycle", or
"generate the development history dataset".

The operation is never proposed by default.

It is never offered as a suggested follow-up to an audit, a review,
or any other completed operation, and it never activates on its own after
another task inside the same session.

## Intake

Resolve these parameters before gathering, asking only for what the request leaves open:

- **Target** - the repository or project location whose history is gathered.
- **Workspace** - the directory receiving all artifacts.
  When the request names a directory, use it.
  Otherwise create `work/history/` inside the target repository,
  or its own `work` or `temporary` convention when one exists.
- **Prototype** - whether the request commissions a visualisation prototype
  in addition to the dataset.
  The dataset is always the primary deliverable.
- **Sources** - confirm that version history and all documentation,
  including archived documentation, are readable.
- **Landing** - where the finished `history.json` and its shim are placed
  when a consuming viewer exists outside the workspace.

## Ref Selection

Gather the fullest reachable history of the target branch.

- When the upstream tracking ref (`@{u}`) exists and strictly contains `HEAD`
  (`git merge-base --is-ancestor HEAD @{u}`), gather at the upstream tip and record
  the local checkout's lag.
- Otherwise gather at `HEAD`.
- The chosen ref, its sha, the local head sha, and the behind-count land in
  `gathering/out/ref.json` and the manifest - the dataset never silently covers
  less history than the repository already fetched.
- Probe for non-git systems once: `.svn`, `git-svn-id` commit markers.
  Absence is recorded; a real SVN checkout uses `svn log` as the commit source.

## Workspace Layout

Establish this tree inside the workspace before gathering:

```
<workspace>/README.md              # workspace identity contract
<workspace>/plan/                  # the recorded plan + steps log
<workspace>/gathering/scripts/     # extraction scripts
<workspace>/gathering/out/         # intermediate JSON per extractor
<workspace>/gathering/notes/       # findings, anomalies, unassigned records
<workspace>/temporary/             # scratch files and downloads
<workspace>/prototype/             # the visualisation, when commissioned
```

The workspace `README.md` marks the directory as a history-gathering workspace:
it states the layout, that contents are derived state reusable for incremental
updates, that evidence passes may exclude the tree, and that deletion loses only
resume capability.

Write the plan under `plan/` first.
The plan names the sources, the extraction stages, the dataset schema,
and the verification steps before any gathering runs.

Keep a steps log (`plan/steps.md`) as the run proceeds: one row per stage -
what ran, how, what it produced, and anomalies hit.
The log feeds session review and the next run's reuse decisions.

## Scout Delegation

Spawn read-only scout agents for the evidence surface when the host supports
delegation, unless the request says otherwise.
Typical roles: document-field inventory, version-boundary facts,
consumer-side contract (what the viewer reads).
Scouts never write; the parent folds their reports into scripts and notes
per `process/parallel-execution.md`.

## Gathering

Collect source families in this order.

1. **Commit history** - the full `git log` with subjects, hashes, dates,
   and insertion/deletion counts, oldest first, at the chosen ref.
   Merge commits stay in the stream; the classifier routes them to a
   neutral type rather than dropping them.
   Every commit that touches a dependency manifest (`Cargo.toml`,
   `package.json`, `pyproject.toml`, `requirements.txt`, `go.mod`,
   `pom.xml`, `*.csproj`, build descriptors) is diffed against its
   first parent - declared dependency additions, removals, and version
   bumps become `dependency` events carrying name, from/to versions,
   manifest path, and channel (prod/dev/build/indirect).
   Manifests are discovered by walking the tree at the chosen ref and
   parsed per format - lockfiles are excluded (resolved versions are
   not declarations), each manifest's own `version` field is a version
   signal, not a dependency, and `FROM image:tag` lines in Dockerfiles
   feed the `build` channel.
   Boundary commits emit them too - dependency changes on the commit
   that bumps the version still belong to the era that contains it.
2. **Version boundaries** - the commit at which each version began and ended:
   version-manifest bumps (package files, build descriptors), tags,
   and changelog headings.
   Versions found only in documentation, without a manifest bump,
   still enter the dataset as boundary-free records.
3. **Development records** - every documentation tree that records decisions,
   lessons, issues, bugs, changes, plans, refactorings, assessments, proposals,
   reviews, audits, hunts, reports, prompts, tests, standards, templates,
   preparations, and discards, including archived trees.
   Each record keeps its path and date so it stays traceable.
   A doc holding several dated entries under its own headings
   (a decision register, a lessons log) splits into one record per entry.
   Record kind resolves from the directory family before the filename, so
   a template-directory file never inherits its filename's apparent family
   (`<x>-assessment-template.md` stays a template, not an assessment).
4. **Local scratch probe** - the subject's `work/` or scratch trees are
   inventoried into `gathering/notes/` only - never turned into events.

## Extraction Pipeline

Run the pipeline as staged scripts under `gathering/scripts/`
with intermediate output under `gathering/out/`:

| Stage        | Script shape       | Output                                            |
|--------------|--------------------|---------------------------------------------------|
| Git extract  | `extract_git.py`   | commits, version boundaries, dependency changes, per-boundary stats, ref record |
| Docs extract | `extract_docs.py`  | categorized + enriched development records        |
| Merge        | `build_history.py` | `history.json`, the bundled shim, `manifest.json` |

Per-version statistics are captured at the version's own boundary commit -
line counts, file counts by category, dependency counts, commit count,
and insertions/deletions - never measured at HEAD for a past version.

### Assessment Metrics

Beyond stats, each era carries a `metrics` block that lets the consumer
assess the development process itself - problems surfaced and how
engineering focus moved between releases:

- `days` - era duration from first to last commit date.
- `testRatio` - `loc.test / loc.src` at the boundary commit.
- `modules` - per top-level directory LOC at the boundary plus the era's
  insertions/deletions against it, so a multi-implementation project
  shows where the effort went.
- `hotspots` - the most-touched files of the era (top ~8 by commit count),
  from per-commit `--numstat`, not only `--shortstat`.
- `authors` - commit counts per author inside the era.
- `commitMix` - the classified commit-type distribution per era; computed
  at merge time from the same classifier that types events, so the
  interface can diff focus between consecutive versions.

Commit extraction therefore records `%an` and `--numstat` per commit,
and the merge folds per-era metrics onto each version record.

### Record Dating And Era Assignment

Each doc record carries two dates:

- `date` - the declared record date: dated path or filename segment,
  then document-comment date (`<!-- ... Date: YYYY-MM-DD -->`),
  then the commit date the file entered history.
- `committed` / `era_date` - the commit-era date used to place the record
  on a version era when it carries no explicit version directory.

A declared date may legitimately predate the repository (preparation
documents); era assignment always uses the commit-era date.

### Record Enrichment

Doc extraction pulls structured fields out of record content when the
family supplies them: audit/hunt/review/report score, verdict or decision,
findings count (unique finding-id occurrences, including prefixed forms
like `FND-SEC-001`), report revision,
the subject version a report assesses, and change-request subtype
(Feature/Fix/Refactor/Chore) which overrides the record's event type.
Verdict extraction accepts only a bounded outcome vocabulary - pass, fail,
verdict words - never arbitrary heading text.
Fields are emitted only when found - never invented.

### Merge

Doc record categories are normalized to the dataset's category registry
at merge time, so `refactoring` records land on the `refactor` category
and every event type has a known id.

Commits are classified into event types by a subject-pattern rule bank -
release markers, merge messages, audit/report additions, fixes,
refactors, docs, tests, features, changes, chores - with an explicit
fallback type, never a dropped commit.

Records that land on no version era are written to
`notes/unassigned.json` - an empty file is the expected result,
a non-empty one is an anomaly to review, not to hide.

The merge emits `gathering/out/manifest.json`: generation timestamp,
chosen ref and sha, local head and behind count, commit/version/record
totals, unassigned count, and landing paths.

## Data Model

Versions are ordered oldest to newest and each carries a `kind`:

| Kind         | Meaning                                                |
|--------------|--------------------------------------------------------|
| `release`    | A released version with a boundary commit              |
| `changelog`  | A version found only in changelog or docs, no boundary |
| `developing` | The current unreleased version, boundary open at HEAD  |
| `planned`    | A future version that has records but no code          |

`gapDays` records quiet days between consecutive versions,
`superseded` marks a version number later reused,
and `eventCounts` precomputes per-category totals for the interface.

The canonical field contract lives in `references/history-schema.md`.

## Bundled Shim

The merge stage emits a second artifact beside `history.json`:
a JavaScript shim that assigns the same object to a global variable,
so the interface can load the dataset from `file://`
where `fetch` is unavailable.

Both artifacts emit from one data object in one build,
so they can never diverge.

The shim's filename must be the path the consumer's own script tag loads
(e.g. `js/history.js`) - a name the consumer does not reference silently
breaks the `file://` fallback.

## Prototype

When a prototype is commissioned it is a static multi-file application
(`index.html`, stylesheet, ordered scripts, no build step) that loads
`history.json` first, falls back to the bundled shim,
and offers a file picker as last resort.

The prototype visual language, layout, and interaction model belong
to the commissioning request, not to this operation.

## Verification

Before delivery, confirm mechanically:

- `history.json` parses and conforms to `references/history-schema.md`.
- The shim exists, carries the identical dataset, and lands at the
  consumer's referenced path.
- Every released version appears once, in order, with stats present.
- Every stats-bearing version also carries its `metrics` block.
- Every event carries a traceable source - a commit hash or a document path.
- No record is fabricated: unknown fields are omitted, never invented.
- `manifest.json` records the covered ref and counts.

## Incremental Reuse

A re-run compares the recorded `manifest.json` ref sha against the
repository's current chosen ref: equal means unchanged stages can be
skipped and only the merge re-runs.
The `out/` intermediates are the resume state - keep them.

## Boundaries

The operation is source-only like the audit:
it reads commit history and documentation, and never builds, tests,
or executes the target project.

Extraction scripts are report-production tools operating on gathered text,
run under the workspace, never against the subject's build.

The dataset may name the target project inside its own workspace output -
shipped skill files never carry real project names or paths.
