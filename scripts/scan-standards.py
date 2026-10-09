#!/usr/bin/env python3
"""Fingerprint a supplied engineering-standards corpus for digest refresh.

Enumerates a directory of Markdown standard documents and emits a
deterministic manifest: file name, byte size, line count, declared version
marker, and the H2 heading skeleton. The manifest is maintainer input for the
supplied-corpus refresh procedure in ``docs/MAINTENANCE.md`` - save it under
``work/`` and diff it against a previous manifest to scope what changed.

The corpus is data, never code. This tool reads files as UTF-8 text and never
executes, installs, or evaluates anything it scans.

Usage: python scripts/scan-standards.py <corpus-directory> [--json]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

VERSION_MARKERS = (
    re.compile(r"\bversion\b[:\s*`*]+([0-9]+(?:\.[0-9]+)*)", re.IGNORECASE),
    re.compile(r"\brevision\b[:\s*`*]+([0-9]+(?:\.[0-9]+)*)", re.IGNORECASE),
)
HEADING = re.compile(r"^##\s+(.+?)\s*$")
TITLE = re.compile(r"^#\s+(.+?)\s*$")
FRONTMATTER_BOUNDARY = re.compile(r"^---\s*$")


def declared_version(text: str) -> str:
    """Return the version marker from a frontmatter field or a header line."""
    for line in text.splitlines()[:30]:
        for marker in VERSION_MARKERS:
            match = marker.search(line)
            if match:
                return match.group(1)
    return "-"


def skeleton(path: Path) -> dict:
    """Return the manifest row for one standards document."""
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    headings = [match.group(1) for match in (HEADING.match(line) for line in lines) if match]
    title_match = next((TITLE.match(line) for line in lines if TITLE.match(line)), None)
    return {
        "file": path.name,
        "title": title_match.group(1) if title_match else "-",
        "bytes": path.stat().st_size,
        "lines": len(lines),
        "version": declared_version(text),
        "headings": headings,
    }


def scan(root: Path) -> list[dict]:
    """Return manifest rows for every Markdown file under root, sorted by name."""
    return [skeleton(path) for path in sorted(root.rglob("*.md"))]


def emit_text(rows: list[dict]) -> None:
    for row in rows:
        print(f"## {row['file']}  ({row['lines']} lines, {row['bytes']} bytes, "
              f"version {row['version']})")
        print(f"   title: {row['title']}")
        for heading in row["headings"]:
            print(f"   - {heading}")
        print()


def main(argv: list[str]) -> int:
    args = [arg for arg in argv if not arg.startswith("--")]
    if len(args) != 1:
        print("usage: scan-standards.py <corpus-directory> [--json]", file=sys.stderr)
        return 2
    root = Path(args[0])
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2
    rows = scan(root)
    if "--json" in argv:
        print(json.dumps(rows, indent=2))
    else:
        emit_text(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
