# Contributing

## Purpose

> **Scope:** How changes to the Lens skill repository are proposed, reviewed, and released
> **Key items:** maintainer model, validation before merge, AI-assisted contributions, versioning

## Maintainer Model

The repository is maintained by a single maintainer, Filip Golewski.

All changes go through pull requests and are reviewed and merged by the maintainer.

If the maintainer is unavailable for an extended period, repository continuity depends on a fork
or a maintainer handoff arranged through the repository owner.

## Before Submitting

- Follow `STYLE.md` for prose, tables, and file handling.
- Follow `MAINTENANCE.md` for directory roles, naming, and the registration contract - every new
  or renamed resource is registered in `SKILL.md` and mirrored in the `README.md` tree.
- Keep `evals/evals.json` in sync when a change alters skill behavior.

Run the skill-maintenance validators before requesting review:

```text
python scripts/validate-skill.py .
python scripts/check-references.py .
python scripts/check-contents.py .
git diff --check
```

The maintainer runs the same validators before merging.

## AI-Assisted Contributions

AI-assisted contributions are welcome.

Disclose meaningful AI involvement in the pull request description or commit trailer, for
example a `Co-Authored-By` line, so code and content provenance stays traceable.

## Versioning And Releases

Never bump `metadata.version` as a side effect of a change - the skill version moves only on an
explicit request, per `VERSIONING.md`.

Releases are anchored by the commit that bumps `metadata.version` - no git tags are used.

## Security Issues

Do not open pull requests or public issues for vulnerabilities - follow `SECURITY.md`.
