# History Visualisation

## Purpose

> **Scope:** The named lifecycle operation that produces a `history.json` dataset from
> a project's development record **Key items:** activation contract, workspace layout,
> gathering sources, extraction pipeline, schema, verification

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
- **Sources** - confirm that git history and all documentation,
  including archived documentation, are readable.

## Workspace Layout

Establish this tree inside the workspace before gathering:

```
<workspace>/plan/                  # the recorded plan, written before work begins
<workspace>/gathering/scripts/     # extraction scripts
<workspace>/gathering/out/         # intermediate JSON per extractor
<workspace>/gathering/notes/       # findings and anomalies worth keeping
<workspace>/temporary/             # scratch files and downloads
<workspace>/prototype/             # the visualisation, when commissioned
```

Write the plan under `plan/` first.
The plan names the sources, the extraction stages, the dataset schema,
and the verification steps before any gathering runs.

## Gathering

Collect three source families, in this order.

1. **Commit history** - the full `git log` with subjects, hashes, dates,
   and insertion/deletion counts, oldest first.
2. **Version boundaries** - the commit at which each version began and ended:
   version-manifest bumps (package files, build descriptors), tags,
   and changelog headings.
   Versions found only in documentation, without a manifest bump,
   still enter the dataset as boundary-free records.
3. **Development records** - every documentation tree that records decisions,
   lessons, issues, bugs, changes, plans, refactorings, reviews, reports,
   prompts, tests, and discards, including archived trees.
   Each record keeps its path and date so it stays traceable.

## Extraction Pipeline

Run the pipeline as staged scripts under `gathering/scripts/`
with intermediate output under `gathering/out/`:

| Stage        | Script shape       | Output                                          |
|--------------|--------------------|-------------------------------------------------|
| Git extract  | `extract_git.py`   | commits, version boundaries, per-boundary stats |
| Docs extract | `extract_docs.py`  | categorized development records                 |
| Merge        | `build_history.py` | `history.json` plus a bundled JavaScript shim   |

Per-version statistics are captured at the version's own boundary commit -
line counts, file counts by category, dependency counts, commit count,
and insertions/deletions - never measured at HEAD for a past version.

Doc record categories are normalized to the dataset's category registry
at merge time, so `refactoring` records land on the `refactor` category
and every event type has a known id.

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
a JavaScript shim that assigns the same object to a global variable
under `prototype/js/`, so the interface can load the dataset from `file://`
where `fetch` is unavailable.

Both artifacts emit from one data object in one build,
so they can never diverge.

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
- Every released version appears once, in order, with stats present.
- Every event carries a traceable source - a commit hash or a document path.
- No record is fabricated: unknown fields are omitted, never invented.
- The shim exists and carries the identical dataset.

## Boundaries

The operation is source-only like the audit:
it reads commit history and documentation, and never builds, tests,
or executes the target project.

Extraction scripts are report-production tools operating on gathered text,
run under the workspace, never against the subject's build.

The dataset may name the target project inside its own workspace output -
shipped skill files never carry real project names or paths.
