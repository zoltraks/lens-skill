# Visualisation Build

## Purpose

> **Scope:** The named operation that compiles a `history.json` dataset into one
> self-contained HTML visualisation.

> **Key items:** activation contract, dataset requirement, view resolution, pack
> procedure, verification, boundaries.

This document governs the `visualisation build` and `history visualisation build`
operation.

The operation takes a canonical `history.json` dataset - produced by
`process/history-visualisation.md` or supplied directly - and emits a single
HTML file that carries the viewer and the dataset together, so the visualisation
opens over `file://` with no server and no sibling files.

It is not an audit and produces no report.

## Activation Contract

The operation runs only when the request names it - phrases such as "create the
visualisation", "build the history visualisation", "pack the history into one
HTML", or "compile the dataset into a single file".

The operation is never proposed by default and never offered as a suggested
follow-up to another completed operation.

A bare dataset request stays inside `process/history-visualisation.md` - this
operation runs when the deliverable is the compiled HTML file, named directly or
implied by phrasing such as "the visualisation app" or "the single-file build".

## Dataset Requirement

The operation requires a `history.json` before it packs - resolve the dataset in
this order:

1. A dataset the request names or the conversation already established.
2. A dataset waiting in the workspace `out/` of a completed dataset run.
3. A fresh dataset run under `process/history-visualisation.md` when none of the
   above exists or the existing dataset is stale against the target's current
   history - the dataset build is a prerequisite stage of this operation, never
   a separate ask.

Every dataset packed here conforms to `references/history-schema.md` and carries
the verification marks of the dataset operation - `scripts/validate-history.py`
clean is the entry gate, not a repeat step.

## Intake

Each parameter resolves per `process/decision-modes.md`, explicit request
statements first, unresolved parameters surfacing one question surface under
the interactive default and resolving to their defaults under the automated
mode.

| Parameter      | Default                                                                   |
|----------------|---------------------------------------------------------------------------|
| **Dataset**    | Resolved per Dataset Requirement - named, workspace `out/`, or fresh run  |
| **Output**     | `<project>-<version>.html` beside the dataset or in the workspace `out/`  |
| **Shell**      | The bundled `assets/visualisation-shell.html`                             |
| **View**       | Resolved per View Resolution - layout, theme, and palette together        |
| **Shim**       | Not emitted unless the request or the landing contract asks for a twin    |

Notes on the parameters:

- **View** resolves as a set - layout, theme, and palette move together per the
  resolution ladder below, and the resolved values stamp into the embedded copy
  of the dataset so the artifact and the dataset never disagree.
- **Shim** names an optional sibling `history.js` emitted beside the output for
  shells that load a dataset file rather than an embedded payload - the packed
  single file needs no sibling.

## View Resolution

The viewer reads a `view` block (`layout`, `theme`, `palette`) from the dataset
and applies it whenever the user holds no stored preference - the packed
artifact's `view` is the default presentation, never a lock.

Resolve each view parameter in this order:

1. **The request** - an explicit layout, theme, or palette statement wins.
2. **Prior artifacts** - a previously generated visualisation HTML, an existing
   `history.json` or `history.js` for the same subject, or a project
   documentation scheme the subject declares - the recorded `view` values carry
   forward so a rebuild keeps the established presentation.
3. **A question** - unresolved parameters surface with the defaults `square`
   layout, `dark` theme, and `blue` palette, offering the viewer's layout and
   palette families for a non-default pick; under the automated mode the
   defaults resolve silently.

Proposing alternatives is part of the surface - a request for a visualisation
without a stated scheme is offered the other layouts, the light theme, and the
named accent palettes rather than silently accepting the defaults.

## Pack Procedure

1. Resolve the dataset per Dataset Requirement and verify it parses and
   conforms to `references/history-schema.md`.
2. Resolve every intake parameter, reporting the resolved set once before
   packing.
3. Run `scripts/pack-visualisation.py --history <dataset> --out <output>`
   from the skill tree, adding `--layout`, `--theme`, or `--palette` for each
   resolved override and `--shell` when the request names a different shell.
4. Add `--shim <path>` when the landing contract asks for the file:// twin.
5. Verify per Verification below and deliver the output path with the resolved
   view values.

The packer reads the shipped single-file viewer shell, replaces its dataset
anchor - the placeholder comment and `history.js` script tag - with the
embedded `window.HISTORY_DATA` payload, and writes one artifact.

It never mutates the source dataset or the bundled shell.

A target-side run copies the script into the subject's workspace under a
`.tmp.` name per the report-production copy contract, with `--shell` pointing
back at the skill's asset when the copy cannot resolve it.

## Verification

Before delivery, confirm mechanically:

- The output is one file: no `<link>` stylesheet references and no
  `<script src>` tags survive - the anchor is the only external reference the
  shell carried, and the file picker is a DOM element, not a script.
- `window.HISTORY_DATA` parses and carries the identical dataset -
  `scripts/pack-visualisation.py --check` reports the anchor and the resolved
  view before any write.
- The embedded `view` block equals the resolved intake values.
- The emitted shim, when produced, assigns the identical object - twin of the
  same build, never a divergent copy.
- The output filename follows `<project>-<version>.html` from the dataset's
  own identity.

## Boundaries

The bundled shell ships without a dataset - it is viewer code only, and a
shipped skill file never carries real project names, paths, or identifiers.

The operation is source-only like the dataset operation: it reads the dataset
and the shell as data and never builds, tests, or executes the target project.

The shell refresh contract lives in `docs/MAINTENANCE.md` - the bundled asset
is replaced wholesale from a newer upstream build, never edited by hand.
