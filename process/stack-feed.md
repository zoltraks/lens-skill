# Stack Feed

## Purpose

> **Scope:** The intake operation that extends or updates the stack baseline corpus from an external
> standards source **Key items:** source resolution, intake classification, constraint extraction,
> gap diff, proposal gate, provenance rules

The feed operation runs when the user asks to feed the skill with a named source - a skill checkout,
a repository, or a directory of standards and engineering documents.

It converts the source's stack-relevant standards into checkable constraints,
diffs them against `references/stacks/`,
and presents proposed digest changes behind an approval gate.

## Source Resolution

The operation takes one argument: the source name or path.

Resolve the argument to a local checkout - a named sibling skill resolves to its checkout directory,
a repository or path argument resolves as given.

Enumerate candidate documents by convention: index files (`README.md`, `SKILL.md`, `AGENTS.md`,
registry or catalog files), then directories that conventionally hold standards - `standards/`,
`conventions/`, `practices/`, `sections/`, `sources/`, `references/`, `requirements/`.

Record the resolved source and enumerated set under `work/` for the session.

## Intake Classification

Classify every enumerated document before extracting constraints:

| Class                   | Meaning                                                                                                 | Disposition                                               |
|-------------------------|---------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| Stack-relevant standard | Checkable rules for a technology stack - versions, APIs, layouts, security baselines, build conventions | Feed input                                                |
| Cross-stack standard    | Rules that apply regardless of stack - naming, licensing, provenance                                    | Feed input for `references/topics/` or flat `references/` |
| Process or governance   | Workflow, maintenance, and review rules for the source's own lifecycle                                  | Skip - recorded as non-input                              |
| Project-specific        | Content bound to one named project or deliverable                                                       | Skip - anonymize or record                                |

A document carries its class in the intake record with a one-line basis.

## Constraint Extraction

From each feed-input document, extract checkable constraints - statements an audit can verify from
repository source: version floors, required or forbidden APIs, layout rules,
configuration baselines, security controls, and build or test discipline.

Keep the constraint's source: document name plus the section it came from.

Prefer the source's own normative phrasing.
Convert prose into imperative checkable form only when the source states a rule
without a checkable shape.

## Gap Diff

Diff extracted constraints against the bundled corpus:

- For each constraint, find the digest under `references/stacks/` (or `topics/` /flat `references/`
  for cross-stack rules) whose scope covers the technology.
- Mark the constraint `covered` when a digest already encodes an equivalent check,
  `extend` when the digest covers the stack but lacks the check,
  or `new-stack` when no digest covers the technology.
- `new-stack` constraints group into a proposed new digest following the Baseline schema of
  the existing corpus.

Optionally run a web-research pass (fetch permitted sources)
to verify freshness-sensitive claims or complete partial rules - record fetched URLs
alongside constraints.

## Proposal Gate

Present the proposed change set before any shipped edit:

- A table of `extend` constraints per digest file.
- The outline of each `new-stack` digest.
- Cross-stack rules targeting `topics/` or flat `references/`.

The gate asks whether to apply - `autonomous` resolves it to apply,
per the member-contract flag semantics.

Applied edits follow `docs/MAINTENANCE.md` - new digests register in `SKILL.md` and `README.md`,
the version joins the open change set, and evals update when behavior changes.

## Provenance Rules

Shipped files never name the intake source - no skill names, repository names, or paths in digests,
the catalog, or the index.

Provenance lives in `work/` only: an intake record naming the source, classified documents,
extracted constraints, and the applied or rejected proposals.

Digests cite external authoritative URLs (vendor docs, standards bodies)
exactly as the existing corpus does - an internal standard extracted from the source is phrased as a
checkable rule and sourced to the document section in the `work/` record, not in the shipped file.

## Validation

After applied edits run the repository validation suite per `AGENTS.md` plus `format-table.py` on
every table touched.

Report the applied set, skipped classes, and validation results.
