# Skill Maintenance

## Purpose

> **Scope:** Rules for extending, restructuring, and maintaining the Lens skill repository
> **Key items:** directory roles, file naming, registration, extension procedures, validation,
> versioning

These rules govern Lens's own files, not the audit reports it produces.

Use `SKILL.md` as the resource router and follow it when deciding which files to update.

`STYLE.md` governs prose, Markdown formatting, and file handling for the skill's own documents.

`VERSIONING.md` governs skill-version changes.

`scripts/README.md` governs tool usage, safety, and validation order.

## Directory Roles

| Directory       | Role                                                         |
|-----------------|--------------------------------------------------------------|
| `assessment/`   | Core and conditional engineering-audit categories            |
| `principles/`   | Evidence rules, neutrality, and report-output conventions    |
| `process/`      | Audit workflow, report structure, parity, and scoring        |
| `synthesis/`    | Report sections for findings, risks, scoring, and actions    |
| `references/`   | Taxonomies, schemas, and lookup guidance                     |
| `translations/` | Per-language report rendering and terminology                |
| `scripts/`      | Report-production and skill-maintenance scripts              |
| `tests/`        | Focused `unittest` contract tests for the scripts            |
| `evals/`        | Behavioral regression prompts and expectations               |
| `docs/`         | Repository-governance documents, indexed by `docs/README.md` |

Root files govern the repository itself: `SKILL.md`, `README.md`, `AGENTS.md`, and `LICENSE`.

The `docs/` directory holds the governance documents (`README.md`, `STYLE.md`,
`MAINTENANCE.md`, `VERSIONING.md`, `CONTRIBUTING.md`, `SECURITY.md`).

Root `docs/` is repository governance; it is unrelated to the `docs/audit/` report-location
convention in audited projects.

Keep resource files one level deep under their directory.

Do not add nested resource directories unless a documented format requires them.

The corpus directories `references/stacks/`, `references/methodology/`, and
`references/topics/` are the sanctioned exception: they hold distilled external-source
digests indexed by `references/source-catalog.md`.

When a new resource directory is justified, register it in `SKILL.md` and mirror it in the
`README.md` tree.

## File Naming

Use lowercase kebab-case for assessment, process, principle, synthesis, and reference files.

Name each resource file with exactly two words joined by a hyphen, `<word>-<word>.md`.

Stack digests under `references/stacks/` named after a single technology keep one-word names,
such as `go.md` or `php.md`.

Follow the naming pattern of the target directory and choose a name that describes the file's
responsibility, such as `security-review.md` or `report-parity.md`.

Name translation files `translations/<language>-language.md`, following the existing
`polish-language.md` pattern.

Name tools `scripts/<verb>-<object>.py` and use the Python standard library unless an additional
dependency is documented.

Keep conventional uppercase names for root and governance files, including `README.md`,
`AGENTS.md`, `LICENSE`, and the documents under `docs/`.

Keep evaluation prompts in `evals/evals.json`.

## Anonymized Examples

Shipped files never mention real names, paths, or identifiers of projects the skill has
audited or been applied to - no project names, repository paths, hostnames, author names,
or report filenames drawn from a real engagement.

Examples and eval prompts use skill-owned generic subjects: a placeholder project such as
`the project` or `example-service`, placeholder filenames such as `AUDIT-1.1.md`, and
invented finding identifiers.

When a shipped document needs an illustration taken from real work, generalize it first -
strip the subject to its archetype, rename files and identifiers, and drop any detail that
would re-identify the source.

Working artifacts that name real projects live only in the gitignored `work/` directory
and are never shipped.

## Registration Contract

Register every new or renamed resource in `SKILL.md` under the section for its directory.

Each router entry states what the file covers and when to load it.

A resource counts as registered in a document when its filename appears there, or when an
ancestor directory appears as a backticked `path/` token; `scripts/validate-skill.py` enforces
both cases.

Files inside a directory registered by token, such as the corpus directories, are indexed by
`references/source-catalog.md` rather than listed individually in `SKILL.md`.

Mirror root-level and resource-layout changes in the `README.md` directory tree.

Update `## Contents` line numbers in `SKILL.md` and `README.md` when section locations change,
or run `python scripts/check-contents.py --fix .` to re-anchor them mechanically.

Update all references when a file moves or is renamed, including references in assessment,
workflow, synthesis, and translation files.

When audit behavior or report coverage changes, update the applicable workflow, report-format,
parity, navigation, and evaluation material together.

Keep `evals/evals.json` aligned with supported behaviors and regression expectations.

When a rule is mechanically enforced, state it in the document the validator mirrors.

Bounds such as baseline section counts, `PAR` row counts, and required glossary terms must be
identical in the prose contract and in `scripts/validate-report.py`, update both in the same
change so the written rule and the check never drift apart.

The same rule applies to logic mirrored between tools.

The glossary variant, compound-name exemption, and fixed-field-label helpers shared verbatim
between `scripts/link-glossary.py` and `scripts/validate-report.py` must be updated together in
the same change, since a copied implementation drifts the same way a written rule does.

## Extending Assessment And Report Resources

### Adding An Assessment Category

Create the new guide in `assessment/` and follow the structure and evidence requirements of
neighboring assessment files.

State whether the category is mandatory or conditional and define the evidence that makes it
applicable.

Register the guide in the matching `SKILL.md` section and update the `README.md` tree.

For a conditional report section, add its inclusion criterion and position to
`process/report-format.md`.

Update `process/report-parity.md` when the mandatory checklist or report-consistency gate changes.

Update `SKILL.md` Navigation Rules and add evaluation prompts when the behavior changes.

### Changing Process Or Synthesis

When changing audit phases, update `process/audit-workflow.md` and the corresponding intake,
assessment, synthesis, or validation guidance.

When adding or changing a report section, update the matching section file under
`process/report-format/` (or `process/report-format.md` for index-level rules) and
`process/report-parity.md`, plus the relevant `synthesis/` or `assessment/` guide.

Keep report section order, conditional criteria, checklist coverage, and router guidance consistent.

### Adding References

Add reference material under `references/` and register it in `SKILL.md` with its use
conditions; digests distilled from external sources go under the corpus directories and are
indexed by `references/source-catalog.md` instead of `SKILL.md`.

Update the assessment or synthesis guide that consumes it.

Distinguish consulted reference material from evidence that a tool or external check was executed.

### Refreshing The Source Corpus

The corpus under `references/stacks/`, `references/methodology/`, and `references/topics/` is
maintainer-refreshed, never fetched at audit time.

To refresh a digest, fetch the URLs its `references/source-catalog.md` rows name, update the
distilled rules where the source changed, advance the digest's snapshot date, and mark the
catalog rows `distilled`.

When a canonical URL fails, record the working alternate in the catalog's Unresolved And
Alternate Addresses table and mark the row `alternate`; paywalled or bot-blocked sources keep
their canonical URL and a `paywalled` or `restricted` status.

Distill checkable rules and conclusions, never copy a source's full normative text into the
repository.

### Report Workspace Retention

Report parts, copied `.tmp.` tool files, and validation working copies live in the audited
repository's `work/` tree (or its `temp`/`temporary` convention) during assembly, and report
parts carry a `.tmp.` infix so they read as scratch anywhere they appear.

When the scratch tree exists but file tools cannot write it, `.tmp.` parts may sit beside the
output file during assembly under the same retention rule.

Parts are checkpoints, so they are retained until the assembled report passes the formatting,
validation, checklist, and parity gates, then deleted before delivery - `work/` is a scratch
area, not a retention location, and the validation phase confirms the cleanup.

## Adding A Report Language

Create `translations/<language>-language.md` following the structure of the existing
`translations/polish-language.md` file.

Define report terminology, translated section labels, prompt phrasing, style requirements, and
expected diacritics or encoding requirements as applicable.

Register the translation in `SKILL.md` and update the `README.md` tree.

Add or update regression prompts that exercise the translated report output.

## Adding Tools And Evaluations

Create tools with a descriptive verb-object filename and standard-library dependencies unless
additional dependencies are documented.

Classify each tool in `scripts/README.md` as report-production or skill-maintenance.

Report-production tools are copied into the audited repository under a `.tmp.` name and run only
against report artifacts and report-support files.

Skill-maintenance tools run from the Lens repository and may import shared helpers from
`scripts/common.py`.

Report-production tools stay self-contained single files, because they are copied under `.tmp.`
names where `common.py` is not available.

Register each tool in `SKILL.md` and in the workflow or validation order where it is used.

Lens audits are source-only, so never add a tool that builds, tests, scans, or executes the
audited project.

Keep evaluation JSON valid, with a matching `skill_name`, unique integer IDs, non-empty prompts,
and non-empty expectation lists.

Update or add evaluation prompts when a change alters activation, assessment, reporting, or tool
behavior.

## Validation After Changes

Run the skill-maintenance validators and script tests after structural changes:

```text
python scripts/validate-skill.py .
python scripts/check-references.py .
python scripts/check-contents.py .
python -m unittest discover -s tests
```

Run `git diff --check` before delivery.

Format tables in edited skill documents with a temporary source-width formatter per `STYLE.md`.

Check comment alignment in edited plain-text blocks with
`python scripts/align-comments.py <file> --check`.

Generic document checkers flag several sanctioned patterns in this repository. Treat these as
expected noise, not defects:

- Star-bar glyphs `★` and `☆` inside code spans, allowed by `STYLE.md` for documented output
  formats.
- Missing blank lines before a list or table that starts a `markdown` payload block.
- Compact `|  |` and `|--|` leading icon columns, the canonical output of `scripts/format-table.py`
  that stricter formatters would pad further.
- The deliberately incorrect separator-format example in `process/report-format.md`.
- `XXX` inside `FND-XXX`, `RSK-XXX`, and `REC-XXX` template identifiers.
- Polish diacritics in `translations/polish-language.md`.
- A `[text](url)` literal inside a code span, counted as a link by census tools.

Preserve the encoding and line-ending style of existing files.

For report-format changes, use `scripts/validate-report.py` only on a report artifact, not on a rule
or maintenance document.

Exercise relevant regression scenarios from `evals/evals.json` and `process/audit-workflow.md`
when behavior changes.

A passing validator checks structure, not the audit's technical correctness or future agent
behavior.

## Versioning

The skill version is recorded in `SKILL.md` frontmatter under `metadata.version`.

Follow `VERSIONING.md` for increments: every shipped change set bumps the patch component once,
at the point the set is complete and validated.

## File Encoding

Preserve the encoding and line-ending style of each existing file that is edited.

Create new files in UTF-8 without a BOM and use LF line endings.
