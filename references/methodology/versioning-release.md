# Versioning And Release Baseline

## Purpose

> **Scope:** Checkable rules for version numbers, changelogs, commit conventions, and release
> metadata
> **Key items:** SemVer precedence rules, Keep a Changelog structure, Conventional Commits,
> npm range operators, security-contact convention

This file distills the SemVer, Keep a Changelog, Conventional Commits, npm, and securitytxt
sources listed in `references/source-catalog.md` into constraints an audit can verify from
repository source.

Snapshot date: 2026-09-30.

Feeds `assessment/change-management.md`, `assessment/api-compatibility.md`, and
`synthesis/remediation-roadmap.md`.

## Semantic Versioning

From https://semver.org/spec/v2.0.0.html (bare semver.org URLs are folded into this row).

- `MAJOR.MINOR.PATCH`: breaking API change, backward-compatible feature,
  backward-compatible fix. Everything else (docs, internals) is unversioned by the spec.
- Pre-release labels (`-alpha.1`, `-rc.2`) sort before the release and compare numerically
  per identifier. Build metadata (`+build.5`) is ignored for precedence.
- 0.x.y means the public API is not stable - no compatibility promise. A `0.x` library used
  as a public dependency is a risk observation.
- Version claims must agree across `package.json`, tags, and changelog. A tag ahead of the
  manifest or a changelog behind the tag is a coherence finding.

## Keep A Changelog

From https://keepachangelog.com/en/1.1.0/ (bare URLs are folded into this row).

- Conventional sections: `Unreleased`, then versioned releases newest-first, each grouping
  `Added`/`Changed`/`Deprecated`/`Removed`/`Fixed`/`Security`.
- Every release entry carries a date (`YYYY-MM-DD`). Undated releases and diffs without
  dates are convention findings.
- `CHANGELOG.md` is human-facing and hand-maintained in this convention. A changelog that is
  only git log output or fully generated without review is an observation.

## Conventional Commits

From https://www.conventionalcommits.org/en/v1.0.0/.

- `type(scope): description` where type is `feat`/`fix`/etc.. `feat!:`/`fix!:` or a
  `BREAKING CHANGE:` footer marks breaking changes.
- Adoption is all-or-nothing hygiene: a history mixing conventional and free-form messages
  weakens release automation. The audit records the dominant pattern.

## npm Ranges

From https://docs.npmjs.com/about-semantic-versioning.

- `^` keeps the left-most non-zero component (`^1.2.3` -> `>=1.2.3 <2.0.0`. `^0.2.3` -> 
  `>=0.2.3 <0.3.0`). `~` keeps minor (`~1.2.3` -> `>=1.2.3 <1.3.0`).
- Exact pins (`1.2.3`, no operator) freeze the dependency. Ranges (`*`, `>=`, `latest`)
  create unpinned drift - flag them in lockfile-absent libraries.
- `npm ci` installs lockfile-exactly. `npm install` resolves ranges - the distinction feeds
  `references/dependency-manifests.md`.

## Security Contact

From https://securitytxt.org/.

- `.well-known/security.txt` (or `security.txt` at root) advertises a `Contact`, optional
  `Expires`, `Policy`, `Acknowledgments`. Deployed sites should also serve it under
  `/.well-known/`.
- A repo-level `SECURITY.md` is the GitHub convention feeding
  `references/topics/project-health.md`. The two files coexist - web-facing artifacts use
  `security.txt`, repos use `SECURITY.md`.

## Live Check

When web fetch is available, spot-check the SemVer precedence paragraph against semver.org and
the changelog section names against keepachangelog.com.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
