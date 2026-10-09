# Agent Instructions

## Purpose

> **Scope:** Agent-facing entry point for authoring and maintaining this skill repository.
> **Key items:** governing documents, boundaries, local workspace, validation, improvement.

This repository is the Lens skill, an Agent Skills package for source-only engineering audits
and review reports.

`SKILL.md` is the runtime router read by agents that use the skill.

This file is the entry point for agents that modify the skill.

## Governing Documents

| Document               | Owns                                                               |
|------------------------|--------------------------------------------------------------------|
| `docs/CONTRIBUTING.md` | Maintainer model, pre-merge validation, commit convention          |
| `docs/STYLE.md`        | Prose, tables, headings, and encoding for shipped documents        |
| `docs/MAINTENANCE.md`  | Directory roles, file naming, registration, validation, versioning |
| `docs/VERSIONING.md`   | Version format, bump rules, and the release procedure              |
| `docs/SECURITY.md`     | Vulnerability reporting path and covered risks                     |
| `docs/README.md`       | Index of the governance documents under `docs/`                    |

Keep each rule in its owning document and link to it instead of duplicating it.

## Boundaries

- The skill is a routed instruction set: Markdown content becomes agent instructions, so
  content integrity issues are security issues - follow `docs/SECURITY.md` for them.
- Audits are source-only by default: never add instructions that build, test, or execute the
  audited project without an opt-in evidence mode. `executed-readonly` permits only
  non-mutating, read-only analyzers (such as dependency advisory or policy scanners) the
  user explicitly commissions - the project itself is still never built, tested, or run.
  `executed-commands` additionally permits explicitly commissioned non-mutating commands
  such as test suites, builds, and isolated reproduction harnesses - the subject is still
  never deployed, mutated, or connected to live systems.
- Keep `SKILL.md` lean: it routes to resources and must stay below 500 lines.
- Register every new or renamed resource in `SKILL.md` and mirror it in the `README.md` tree,
  per `docs/MAINTENANCE.md`.
- Follow `docs/STYLE.md` for every shipped document: H1 plus Purpose, one sentence per
  paragraph, wrap width per `docs/STYLE.md`, tables aligned by source width.
- Never embed real names, paths, or identifiers of audited projects in shipped files -
  generalize examples per `docs/MAINTENANCE.md`.
- Keep `evals/evals.json` in sync when a change alters skill behavior.
- Bump `metadata.version` by one patch with every shipped change set - a set of edits that
  will be committed or delivered together, per `docs/VERSIONING.md`.
- Do not claim validation that did not run.
- Never commit automatically - propose a one-sentence commit message per `docs/CONTRIBUTING.md`.
- A bare `work on lens-skill` request that names no operation is standby - read this file and
  `SKILL.md`, follow the router's usage notes, confirm readiness, and wait for the named
  operation without loading further files, resuming plans, or editing on assumption.
- On a named operation, decide which additional skill documents the task needs and read them
  first, loading the smallest useful set per the router.

## Local Workspace

Audit reports, session reviews, and other local working artifacts live in the gitignored
`work/` directory.

Shipped skill files never depend on workspace content - temporary validation scripts carry a
`.tmp.` infix and are removed after use, per `README.md`.

## Validation

Run the skill-maintenance checklist from `docs/CONTRIBUTING.md` before proposing a change:

```text
python scripts/validate-skill.py .
python scripts/check-references.py .
python scripts/check-contents.py .
python scripts/align-comments.py <file> --check
python -m unittest discover -s tests -v
git diff --check
```

Format edited tables with an automated source-width formatter and re-anchor Contents tables
with `python scripts/check-contents.py --fix .` when headings move, per `scripts/README.md`.

Changes to audit workflow, report format, or skill behavior also exercise the regression
scenarios in `evals/evals.json` and `process/audit-workflow.md`.

## Skill Improvement

Structural, routing, or gate changes follow the procedures in `docs/MAINTENANCE.md`.

Session and program-level improvement planning lives in the gitignored `work/` workspace and
never ships as part of the skill payload.
