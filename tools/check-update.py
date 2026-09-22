#!/usr/bin/env python3
"""Check whether the skill's own git repository has incoming updates.

Runs against the skill repository itself - never against the audited or
edited subject. Prints a STATUS verdict line plus key=value detail lines
and always exits 0.

Verdicts:

- NO-REPO          the skill directory is not inside a git work tree
- GIT-MISSING      the git executable is not available
- NO-UPSTREAM      the current branch has no upstream configured
- FETCH-FAILED     the fetch could not complete (offline, auth, timeout)
- CHECK-FAILED     an unexpected git query failed after a successful fetch
- UP-TO-DATE       no incoming commits on the upstream branch
- UPDATE-AVAILABLE incoming commits exist, with behind/ahead/dirty details

Usage: python tools/check-update.py [skill-directory]
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

FETCH_TIMEOUT = 20
GIT_TIMEOUT = 15


def git(root: Path, *args: str, timeout: int = GIT_TIMEOUT) -> subprocess.CompletedProcess | None:
    env = dict(os.environ)
    env.setdefault("GIT_TERMINAL_PROMPT", "0")
    env.setdefault("GIT_SSH_COMMAND", "ssh -o BatchMode=yes")
    try:
        return subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
    except subprocess.TimeoutExpired:
        return None


def verdict(status: str, **details: str) -> int:
    print(f"STATUS {status}")
    for key, value in details.items():
        print(f"{key}={value}")
    return 0


def main() -> int:
    if len(sys.argv) > 2:
        print(__doc__.strip().splitlines()[-1])
        return 0

    if len(sys.argv) == 2:
        root = Path(sys.argv[1]).resolve()
    else:
        root = Path(__file__).resolve().parent.parent

    try:
        inside = git(root, "rev-parse", "--is-inside-work-tree")
    except FileNotFoundError:
        return verdict("GIT-MISSING")
    if inside is None or inside.returncode != 0 or inside.stdout.strip() != "true":
        return verdict("NO-REPO")

    upstream = git(root, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    if upstream is None or upstream.returncode != 0:
        return verdict("NO-UPSTREAM")
    upstream_ref = upstream.stdout.strip()

    fetch = git(root, "fetch", "--quiet", timeout=FETCH_TIMEOUT)
    if fetch is None or fetch.returncode != 0:
        return verdict("FETCH-FAILED", upstream=upstream_ref)

    counts = git(root, "rev-list", "--left-right", "--count", "HEAD...@{u}")
    if counts is None or counts.returncode != 0:
        return verdict("CHECK-FAILED", upstream=upstream_ref)
    parts = counts.stdout.split()
    if len(parts) != 2:
        return verdict("CHECK-FAILED", upstream=upstream_ref)
    ahead, behind = parts

    if behind == "0":
        return verdict("UP-TO-DATE", upstream=upstream_ref)

    status = git(root, "status", "--porcelain")
    dirty = "yes" if status is not None and status.stdout.strip() else "no"
    return verdict(
        "UPDATE-AVAILABLE",
        upstream=upstream_ref,
        behind=behind,
        ahead=ahead,
        dirty=dirty,
    )


if __name__ == "__main__":
    raise SystemExit(main())
