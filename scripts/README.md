# Lens Tooling

## Purpose

> **Scope:** Report-production and skill-maintenance scripts
> **Key items:** table formatting, report validation, skill validation, reference integrity,
> self-update check

These scripts support deterministic maintenance of Lens and production of audit reports.

They do not build, test, scan, install dependencies for, or execute the audited project.

All scripts require Python 3.8 or later (the walrus operator is used in
`check-contents.py`).

## Tool Classes

### Report-Production Tools

Copy `link-glossary.py`, `format-table.py`, `align-comments.py`, `validate-report.py`, and -
for Polish reports - `lint-polish.py` into the audited repository's `work/` directory under a
`.tmp.` name before use.

If `work/` does not exist, use an existing `temp` or `temporary` directory.

Use the repository root only when none of those directories exists.

Run the copied scripts only against the generated report and report-support artifacts.

The edit-format-validate cycle is: edit the report, run `link-glossary.py` to insert glossary
body links, run `format-table.py`, then `validate-report.py`, repeating until the validator
reports zero issues.

`finalize-report.py` runs that cycle's three steps in one command when copied alongside them
under a `.tmp.` name, locating its siblings by filename. When the copies are absent, pass
`--skill-root <path>` (or set `LENS_SKILL_ROOT`) pointing at the skill repository so the tools
resolve in its `scripts/` directory - running it straight from the skill tree needs no flag at
all.

`new-report.py --style audit|hunt|check [--projects a,b] [--params work/lens-params.json]
[--output file]` emits a structurally valid report skeleton - required sections, table
headers, and one field-labeled template block per register - and runs `format-table.py` on
`--output` when the formatter resolves next to the script or under `LENS_SKILL_ROOT`.
`--params` reads the saved intake values from `work/lens-params.json`, so a second report
style in the same session reuses the locked parameters. For `--style check`, an
`evidence-mode` of `executed-readonly` or `executed-checks` in the params file adds the
Artifact Manifest section to the skeleton.

`validate-report.py --dump-contract` prints the mechanically enforced contract - required
sections, field lists, token sets, hunt- and check-specific rules - as JSON generated from
the live constants, for agents that want the contract without reading the documentation
corpus.

`format-table.py` warns when a row begins with `||` or a column is empty in every row.

`--drop-empty-columns` removes columns that are empty in every row, and separator-shaped
cells lacking hyphens are normalized on every run.

`lint-prose.py` lints draft report text before assembly for the prose rules the validator
enforces: heading depth, heading blank-line spacing, semicolons outside code spans, and the
typographic characters the ASCII convention forbids.

`align-comments.py` aligns trailing `#` comments inside untagged fenced blocks and shell-tagged
blocks to one shared column per block - the established column when most comments already
share one, otherwise the longest entry plus two spaces.

`--compact` moves the column to the minimum - `--check` reports misalignment without writing.

A block whose opening fence is preceded by `<!-- align-comments: off -->` - optionally with one
blank line between the marker and the fence - is skipped entirely, so deliberate examples of
misalignment stay untouched.

Run it on any document that contains directory trees, file listings, or commented plain-text
blocks, including the skill's own files.

`link-glossary.py` never links glossary terms inside the value of a `* **Field:**` bullet
(Pillar, Severity, Type, Security, Status, Change, Absence, Verified, Confidence, Class,
Result, Priority, Likelihood, Residual, Owner, Exploitability), because those positions hold
fixed-vocabulary tokens the validator compares literally.

When the report language is not English,
run `validate-report.py` on an English-mapped working copy that translates the `* **Field:**`
finding-block labels, fixed-vocabulary values, and section headings,
and that remaps the glossary section anchor and the `Parity baseline` row label to English.

Mapping only field labels makes the validator skip the required-sections, glossary,
and final-state checks instead of running them.

Anchor remapping changes cell widths, so run `format-table.py` on the working copy before validating
it.

On Windows consoles, set `PYTHONIOENCODING=utf-8` when running the tools, so non-ASCII report
text prints legibly.

`validate-report.py` also checks the report's location: when the report sits inside a
version-numbered or date-named subdirectory, it flags a mismatch against the dominant sibling
pattern under the same parent.

It mechanically enforces the Observation/Concern tag rule: every `| EVD-` ledger row must carry
a tag cell, and every `### FND-` block's `Type` field must read `Observation` or `Concern`.

Its snapshot-identity check requires `Subject Revision`, `Report Style`, and `Evidence Mode`
rows in Document Information, and its evidence-sections check requires `Operator Verification
Handoff` for source-only reports or `Executed Evidence Log` for executed-readonly reports.

Its summary-verification check rejects a `Verified` or `Confirmed` cell in the findings summary
when the finding block says `Verified: no` or lacks a positive `Runtime confirmed` value.

Its fresh-audit check rejects comparative claims against a previous report whenever the report
has no `Changes Since Previous Audit` section.

Its roadmap check requires a `Breaking` column in every `Actionable Remediation Roadmap` table
whenever finding blocks assess `Breaking change`.

Its scorecard-mean check recomputes each `Scorecard Summary` table's overall from the displayed
dimension scores and compares it to the stated `Overall score` at one decimal place.

Pass `--repo-root <dir>` to also verify that `path:line` citations in finding `Targets` and
`Evidence` fields resolve to real files whose recorded line numbers are within file length.

When the `Report Style` row reads `hunt` or `check`, it applies that style's section
contract from `process/report-format/hunt-style.md` or
`process/report-format/check-style.md` instead of the baseline section list. A `check`
report also validates the Execution Register rows, check statuses, `Evidence level` fields,
and the Retest Register trigger.

`lint-polish.py` lints Polish report output for the calques listed in the
`Calque And Style Replacements` table of `translations/polish-language.md`, plus
comma splices, `tylko, gdy`, bare `per`, the `w.` abbreviation, semicolons, typographic
characters that the ASCII convention forbids, and all-caps renderings of the title-case
fixed vocabulary. Run it on every Polish report before delivery -
a pre-delivery gate, not a Validation Record row. Like the other report tools it is copied
into the audited repository under a `.tmp.` name before use.

`validate-report.py` detects a review report by a canonical `REVIEW`-family or
`PRZEGLĄD`-family filename - a bare stem or a `-<revision>` suffix - or a title ending
in `Review and Amendment Instructions`, and then applies the review contract from
`process/review-report.md` instead of the audit checks.

A canonical review file carrying `## Findings` and `## Action Proposals` but no
`### Findings and Corrections` selects the change-review contract, which checks the
seven canonical sections in order, the identification table, the findings scan table
and its severity scale, and the `F-xx` anchor-and-link discipline.

A `REVIEW`-family filename with a custom suffix is classified `custom` and receives the
shared mechanical checks only, since a user-supplied template overrides the canonical
section contract.

`link-glossary.py` applies to audit reports only: review reports carry no Glossary.

The validator prints at most ten problems per check, so fix, re-run the formatter, and
re-validate until it reports zero issues rather than stopping after the first batch.

Remove every copied script and every validation working copy after validation.

### Skill-Maintenance Tools

Run `validate-skill.py`, `check-references.py`, `check-contents.py`, and `check-update.py` from
the Lens repository.

These tools inspect the skill itself and do not need to be copied into an audited project.

They honor the repository's root `.gitignore`, so the `work/` tree of audit artifacts and
session documents is never scanned.

`validate-skill.py` checks `SKILL.md` frontmatter, router references, file budgets, and
`evals/evals.json`.

It exempts report artifacts from the large-file Contents check: files whose names begin with
`AUDIT`, `AUDYT`, `REVIEW`, or `PRZEGLĄD`, or end in `-REVIEW` or `-PRZEGLĄD`, because
reports follow `process/report-format.md` or `process/review-report.md` instead.

`check-references.py` validates the skill's own `SKILL.md` and `README.md` navigation documents.
It is never run on a report artifact or inside an audited repository.

`check-contents.py` verifies that `## Contents` tables in the skill's own documents still anchor to
real `##` section headings.

Pass `--fix` to rewrite each row's recorded line to its section heading - when rows and headings
pair one-to-one they are re-anchored in order.

Run it whenever a document's sections move.

`check-update.py` reports the git upstream status of the skill repository for the once-per-session
Skill Update Check in `SKILL.md`, and always exits `0` with a `STATUS` verdict line.

Its verdicts after upstream resolution carry `tip_sha` and `tip_date` details identifying the
incoming tip commit.

`scan-standards.py` fingerprints a supplied engineering-standards directory - file names, sizes,
declared versions, and heading skeletons - producing the manifest that scopes a digest refresh
per `docs/MAINTENANCE.md`.

It treats the supplied directory as data: it reads Markdown files as text and never executes,
installs, or sources anything it scans.

`common.py` is a shared helper module imported by the skill-maintenance tools.

It is not a tool, it is never copied, and it must never be imported by report-production tools -
those stay self-contained single files so the `.tmp.` copy contract keeps working.

They use the Python standard library and do not require PyYAML or a package manager.

The `tests/` directory at the repository root holds focused `unittest` contract tests for the
scripts - run them with `python -m unittest discover -s tests` after changing a tool.

## Commands

```text
python scripts/validate-skill.py .
python scripts/check-references.py .
python scripts/check-contents.py .
python scripts/check-update.py
python scripts/scan-standards.py path/to/standards-dir [--json]
python scripts/lint-prose.py path/to/draft.md
python scripts/format-table.py path/to/AUDIT.md [--check] [--drop-empty-columns]
python scripts/align-comments.py path/to/AUDIT.md [--check]
python scripts/validate-report.py path/to/AUDIT.md [--repo-root path/to/repo]
python scripts/validate-report.py --dump-contract
python scripts/new-report.py --style hunt --projects api,cli --output path/to/HUNT.md
python scripts/lint-polish.py path/to/AUDYT.md
python scripts/finalize-report.py [--polish] [--skill-root path/to/lens-skill] path/to/AUDIT.md
python -m unittest discover -s tests
```

Exit code `0` means all checks passed.

Exit code `1` means one or more checks failed.

## Validation Order

Run maintenance checks in this order:

1. Validate skill metadata and file references.
2. Check Contents tables with `check-contents.py` when document sections moved.
3. Format edited tables with `format-table.py`.
4. Validate generated reports with `validate-report.py`.
5. Run `git diff --check`.
6. Remove temporary copies from the audited repository.

## Limitations

The format and report validators are mechanical checks, not behavioral verification.

A passing validator does not prove that a report's technical findings are correct.

A passing skill validator does not prove that an agent will follow the skill instructions.

Use the evaluation prompts in `evals/evals.json` for behavioral regression checks.

Never treat a configured scanner, formatter, test command, or build command as executed evidence
unless the audit scope explicitly records a committed or supplied result as `Reported`.
