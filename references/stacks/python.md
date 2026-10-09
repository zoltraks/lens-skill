# Python Baseline

## Purpose

> **Scope:** Checkable constraints for Python services, libraries, and scripts
> **Key items:** version floor, syntax-feature minimums, packaging metadata, style, testing,
> security lint rules

This file distills the Python documentation, PEPs, PyPA packaging guides, pytest, unittest, and
Bandit sources listed in `references/source-catalog.md` into constraints an audit can verify
from repository source.

Snapshot date: 2026-09-30.

Feeds `assessment/best-practices.md`, `assessment/code-quality.md`,
`assessment/testing-review.md`, `assessment/skill-definition.md`, and
`assessment/baseline-conformance.md` for the declared-runtime floor check.

## Version Floor

From https://devguide.python.org/versions/ and
https://docs.python.org/3/whatsnew/index.html.

- At snapshot time, Python 3.9 reached end-of-life in October 2025, Python 3.10 is the oldest
  branch in security support, and 3.13/3.14 are the current feature branches.
- A `requires-python` or runtime floor below the oldest security-supported branch is a
  finding. A floor stated only in README is documentation, not enforcement.
- The effective floor is the minimum of `pyproject.toml` `requires-python`, `setup.cfg`
  `python_requires`, CI matrix minimums, and Dockerfile base images. Conflicting floors are
  a coherence finding.

## Syntax-Feature Minimums

From https://peps.python.org/pep-0585/, https://peps.python.org/pep-0563/, and
https://peps.python.org/pep-0604/.

- PEP 585 builtin generics (`list[str]`, `dict[str, int]`) in annotations evaluate at runtime
  and require Python 3.9+. On 3.8 they raise `TypeError` unless `from __future__ import
  annotations` postpones evaluation.
- PEP 604 union syntax (`X | Y`) requires Python 3.10 at runtime, or 3.7+ under
  `from __future__ import annotations` in annotation positions only.
- PEP 563 `from __future__ import annotations` makes annotations strings. It does not fix
  PEP 585/604 syntax used outside annotations (casts, aliases, `isinstance`).
- A codebase using PEP 585/604 forms without the future import and claiming a 3.8/3.9 floor
  has a verifiable runtime-floor defect - the audit checks imports against the declared floor.

## Style And Layout

From https://peps.python.org/pep-0008/ and https://packaging.python.org/en/latest/.

- PEP 8 remains the style floor: 4-space indent, `snake_case` functions/modules,
  `CapWords` classes, two blank lines around top-level definitions, imports grouped
  stdlib/third-party/local.
- `pyproject.toml` is the canonical build configuration. `setup.py` with imperative logic is
  legacy, `setup.cfg`-only or `requirements.txt`-as-metadata layouts are observations.
- `src/` layout prevents accidental imports of the working tree. Flat layouts that shadow the
  installed package are a common defect.
- `dependencies` in `pyproject.toml` and a committed lockfile (uv.lock, poetry.lock,
  requirements with hashes) serve different roles. A library should not pin exact versions in
  `dependencies`.

## Testing

From https://docs.python.org/3/library/unittest.html and https://docs.pytest.org/en/stable/.

- `unittest` is the stdlib floor. `pytest` is the de-facto harness and discovers
  `test_*.py`/`*_test.py` modules and `test_*` functions/methods by default.
- A `pytest.ini`/`pyproject.toml [tool.pytest.ini_options]` `testpaths` setting that points
  at an empty directory produces a silent zero-test pass - census collected tests.
- `python -m pytest` (not bare `pytest`) guarantees the interpreter under test. CI using a
  bare binary is a portability observation.
- Coverage measurement uses `coverage.py`/`pytest-cov`. `fail_under` makes it a gate.

## Security Lint

From https://bandit.readthedocs.io/en/latest/plugins/index.html - the rule IDs below feed
`references/cwe-analyzer.md`.

- B101 `assert_used`: `assert` on request paths is stripped under `-O` and is not validation.
- B102 `exec_used`, B301-B302 `pickle`/`marshal` loads, B304 `ciphers` weak primitives.
- B307 `eval`, B310 `urllib.urlopen` audit hook, B311 `random` for security purposes.
- B403 `import pickle`, B404 `import subprocess`, B602-B609 shell/`subprocess` injection
  surfaces including `shell=True` and partial-path executables.
- B105-B107 hardcoded password/string secret patterns, B108 `/tmp` usage, B506 `yaml.load`
  without `Loader`, B602+ subprocess wrappers.
- `# nosec` comments suppress findings and are themselves auditable: each one should carry a
  justification.

## Live Check

When web fetch is available, compare the version floor against
https://devguide.python.org/versions/ and spot-check one PEP minimum against the PEP text.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
