# Lens Tooling

## Purpose

> **Scope:** Report-production and skill-maintenance scripts
> **Key items:** table formatting, report validation, skill validation, reference integrity,
> self-update check

These scripts support deterministic maintenance of Lens and production of audit reports.

They do not build, test, scan, install dependencies for, or execute the audited project.

## Tool Classes

### Report-Production Tools

Copy `format-table.py` and `validate-report.py` into the audited repository's `work/` directory
under a `.tmp.` name before use.

If `work/` does not exist, use an existing `temp` or `temporary` directory.

Use the repository root only when none of those directories exists.

Run the copied scripts only against the generated report and report-support artifacts.

Run `format-table.py` before `validate-report.py`, so table-width noise does not drown the
validator's structural findings.

When the report language is not English, run `validate-report.py` on an English-mapped working
copy that translates the `* **Field:**` finding-block labels, fixed-vocabulary values, and
section headings, and that remaps the glossary section anchor and the `Parity baseline` row
label to English. Mapping only field labels makes the validator skip the required-sections,
glossary, and final-state checks instead of running them. Anchor remapping changes cell widths,
so run `format-table.py` on the working copy before validating it.

On Windows consoles, set `PYTHONIOENCODING=utf-8` when running the tools, so non-ASCII report
text prints legibly.

`validate-report.py` also checks the report's location: when the report sits inside a
version-numbered or date-named subdirectory, it flags a mismatch against the dominant sibling
pattern under the same parent.

It mechanically enforces the Observation/Concern tag rule: every `| EVD-` ledger row must carry
a tag cell, and every `### FND-` block's `Type` field must read `Observation` or `Concern`.

The validator prints at most ten problems per check, so fix, re-run the formatter, and
re-validate until it reports zero issues rather than stopping after the first batch.

Remove every copied script and every validation working copy after validation.

### Skill-Maintenance Tools

Run `validate-skill.py`, `check-references.py`, and `check-update.py` from the Lens repository.

These tools inspect the skill itself and do not need to be copied into an audited project.

`check-references.py` validates the skill's own `SKILL.md` and `README.md` navigation documents.
It is never run on a report artifact or inside an audited repository.

`check-update.py` reports the git upstream status of the skill repository for the once-per-session
Skill Update Check in `SKILL.md`, and always exits `0` with a `STATUS` verdict line.

They use the Python standard library and do not require PyYAML or a package manager.

## Commands

```text
python tools/validate-skill.py .
python tools/check-references.py .
python tools/check-update.py
python tools/format-table.py path/to/AUDIT.md
python tools/validate-report.py path/to/AUDIT.md
```

Exit code `0` means all checks passed.

Exit code `1` means one or more checks failed.

## Validation Order

Run maintenance checks in this order:

1. Validate skill metadata and file references.
2. Review changed documents and Contents tables.
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
