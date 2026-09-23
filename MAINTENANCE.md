# Skill Maintenance

## Purpose

> **Scope:** Rules for extending, restructuring, and maintaining the Lens skill repository
> **Key items:** directory roles, file naming, registration, extension procedures, validation,
> versioning

These rules govern Lens's own files, not the audit reports it produces.

Use `SKILL.md` as the resource router and follow it when deciding which files to update.

`STYLE.md` governs prose, Markdown formatting, and file handling for the skill's own documents.

`VERSIONING.md` governs skill-version changes.

`tools/README.md` governs tool usage, safety, and validation order.

## Directory Roles

| Directory      | Role                                                      |
|----------------|-----------------------------------------------------------|
| `assessment/`  | Core and conditional engineering-audit categories         |
| `principles/`  | Evidence rules, neutrality, and report-output conventions |
| `process/`     | Audit workflow, report structure, parity, and scoring     |
| `synthesis/`   | Report sections for findings, risks, scoring, and actions |
| `references/`  | Taxonomies, schemas, and lookup guidance                  |
| `translation/` | Per-language report rendering and terminology             |
| `tools/`       | Report-production and skill-maintenance scripts           |
| `evals/`       | Behavioral regression prompts and expectations            |

Root files govern the repository itself: `SKILL.md`, `README.md`, `STYLE.md`,
`MAINTENANCE.md`, `VERSIONING.md`, and `LICENSE`.

Keep resource files one level deep under their directory.

Do not add nested resource directories unless a documented format requires them.

When a new resource directory is justified, register it in `SKILL.md` and mirror it in the
`README.md` tree.

## File Naming

Use lowercase kebab-case for assessment, process, principle, synthesis, and reference files.

Follow the naming pattern of the target directory and choose a name that describes the file's
responsibility, such as `security-review.md` or `report-parity.md`.

Name translation files `translation/<language>-language.md`, following the existing
`polish-language.md` pattern.

Name tools `tools/<verb>-<object>.py` and use the Python standard library unless an additional
dependency is documented.

Keep conventional uppercase names for root files, including `README.md`, `STYLE.md`,
`MAINTENANCE.md`, `VERSIONING.md`, and `LICENSE`.

Keep evaluation prompts in `evals/evals.json`.

## Registration Contract

Register every new or renamed resource in `SKILL.md` under the section for its directory.

Each router entry states what the file covers and when to load it.

Mirror root-level and resource-layout changes in the `README.md` directory tree.

Update `## Contents` line numbers in `SKILL.md` and `README.md` when section locations change.

Update all references when a file moves or is renamed, including references in assessment,
workflow, synthesis, and translation files.

When audit behavior or report coverage changes, update the applicable workflow, report-format,
parity, navigation, and evaluation material together.

Keep `evals/evals.json` aligned with supported behaviors and regression expectations.

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

When adding or changing a report section, update `process/report-format.md` and
`process/report-parity.md`, plus the relevant `synthesis/` or `assessment/` guide.

Keep report section order, conditional criteria, checklist coverage, and router guidance consistent.

### Adding References

Add reference material under `references/` and register it in `SKILL.md` with its use conditions.

Update the assessment or synthesis guide that consumes it.

Distinguish consulted reference material from evidence that a tool or external check was executed.

## Adding A Report Language

Create `translation/<language>-language.md` following the structure of the existing
`translation/polish-language.md` file.

Define report terminology, translated section labels, prompt phrasing, style requirements, and
expected diacritics or encoding requirements as applicable.

Register the translation in `SKILL.md` and update the `README.md` tree.

Add or update regression prompts that exercise the translated report output.

## Adding Tools And Evaluations

Create tools with a descriptive verb-object filename and standard-library dependencies unless
additional dependencies are documented.

Classify each tool in `tools/README.md` as report-production or skill-maintenance.

Report-production tools are copied into the audited repository under a `.tmp.` name and run only
against report artifacts and report-support files.

Skill-maintenance tools run from the Lens repository.

Register each tool in `SKILL.md` and in the workflow or validation order where it is used.

Lens audits are source-only, so never add a tool that builds, tests, scans, or executes the
audited project.

Keep evaluation JSON valid, with a matching `skill_name`, unique integer IDs, non-empty prompts,
and non-empty expectation lists.

Update or add evaluation prompts when a change alters activation, assessment, reporting, or tool
behavior.

## Validation After Changes

Run the skill-maintenance validators after structural changes:

```text
python tools/validate-skill.py .
python tools/check-references.py .
```

Run `git diff --check` before delivery.

Format tables in edited skill documents with a temporary source-width formatter per `STYLE.md`.

Preserve the encoding and line-ending style of existing files.

For report-format changes, use `tools/validate-report.py` only on a report artifact, not on a rule
or maintenance document.

Exercise relevant regression scenarios from `evals/evals.json` and `process/audit-workflow.md`
when behavior changes.

A passing validator checks structure, not the audit's technical correctness or future agent
behavior.

## Versioning

The skill version is recorded in `SKILL.md` frontmatter under `metadata.version`.

Follow `VERSIONING.md` for increments and bump the version only when the user explicitly requests
it.

## File Encoding

Preserve the encoding and line-ending style of each existing file that is edited.

Create new files in UTF-8 without a BOM and use LF line endings.
