# Contributing

## Purpose

> **Scope:** How changes to the Lens skill repository are proposed, reviewed,
> and released **Key items:** maintainer model, validation before merge, AI-assisted
> contributions, versioning

## Maintainer Model

The repository is maintained by a single maintainer, Filip Golewski.

This single-maintainer model is the intended operating model of the project,
not a transitional state.

All changes go through pull requests and are reviewed and merged by the maintainer.

If the maintainer is unavailable for an extended period,
repository continuity depends on a fork or a maintainer handoff arranged through the repository
owner, which is the accepted continuity mechanism.

## Before Submitting

- Follow `STYLE.md` for prose, tables, and file handling.
- Follow `MAINTENANCE.md` for directory roles, naming,
  and the registration contract - every new or renamed resource is registered in `SKILL.md` and
  mirrored in the `README.md` tree.
- Keep `evals/evals.json` in sync when a change alters skill behavior.

Run the skill-maintenance validators and the script test suite before requesting review:

```
python3 scripts/validate-skill.py .
python3 scripts/check-references.py .
python3 scripts/check-contents.py .
python3 scripts/align-comments.py <file> --check
python3 -m unittest discover -s tests -v
git diff --check
```

The repository runs no CI workflow by deliberate choice:
the checklist above is the standing pre-merge gate,
and the maintainer runs it on every change before merging.

Skipping it leaves regressions in the tools and documents undetected, so treat it as
required, not advisory.

## AI-Assisted Contributions

AI-assisted contributions are welcome.

Disclose meaningful AI involvement in the pull request description,
so code and content provenance stays traceable.

Commit messages carry no AI attribution or `Co-Authored-By` trailers.

## Versioning And Releases

Bump `metadata.version` per `VERSIONING.md`.
Every shipped change set increments the patch component once,
at the point the set is complete and validated.

Releases are anchored by the commit that bumps `metadata.version`.
No git tags are used.

## Commit Messages

Match the repository's own convention - read `git log -10 --format=%s` before proposing.

The subject line is one short, general sentence with no type prefixes
(`feat:`, `fix:`, `docs:`, `chore:`) and no trailing period.

Optional detail goes in the body, separated from the subject by one blank line.
The message itself never ends with a blank line or a trailing newline.

The message carries no author lines, sign-offs, AI attribution,
or other metadata trailers.

## Security Issues

Do not open pull requests or public issues for vulnerabilities - follow `SECURITY.md`.
