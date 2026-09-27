#!/usr/bin/env python3
"""Check that Contents tables match actual section headings.

For every Markdown file with a ``## Contents`` table, each row's recorded
line number must point at a real ``##`` heading, rows must stay in heading
order, and no ``##`` section may hide between the Contents table and the
first recorded row.

Row names may describe a single heading or a group of adjacent sections,
so only the recorded line anchor is checked, not the row label.

Usage: python scripts/check-contents.py <skill-directory>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from common import report


TOLERANCE = 3
CONTENTS_HEADING = re.compile(r"^##\s+Contents\s*$")
HEADING = re.compile(r"^##\s+(.+?)\s*$")
ROW = re.compile(r"^\|\s*(.+?)\s*\|\s*(\d+)\s*\|")


def fenced_flags(lines: list[str]) -> list[bool]:
    flags: list[bool] = []
    inside = False
    for line in lines:
        if line.lstrip().startswith("```"):
            inside = not inside
            flags.append(True)
            continue
        flags.append(inside)
    return flags


def check_file(path: Path, root: Path) -> list[str]:
    relative = path.relative_to(root)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return [f"{relative}: file is not readable as UTF-8"]
    fences = fenced_flags(lines)

    contents_at = next(
        (index for index, line in enumerate(lines)
         if not fences[index] and CONTENTS_HEADING.match(line)),
        None,
    )
    if contents_at is None:
        return []

    headings = [
        (index, match.group(1))
        for index, line in enumerate(lines)
        if not fences[index] and (match := HEADING.match(line))
    ]
    issues: list[str] = []

    rows: list[tuple[int, str, int]] = []
    for index, line in enumerate(lines):
        if fences[index] or index <= contents_at:
            continue
        if not line.startswith("|"):
            if rows:
                break
            continue
        if re.match(r"^\|[\s\-|]+\|?$", line):
            continue
        match = ROW.match(line)
        if match:
            rows.append((index, match.group(1), int(match.group(2))))

    if not rows:
        return [f"{relative}: Contents section has no rows"]

    after_contents = [(index, name) for index, name in headings if index > contents_at]

    previous_heading_line = contents_at
    for row_index, name, recorded in rows:
        nearby = [position for position, _ in after_contents
                  if abs(position + 1 - recorded) <= TOLERANCE]
        if not nearby:
            nearest = min(
                ((abs(position + 1 - recorded), heading) for position, heading in after_contents),
                default=None,
            )
            hint = f", nearest heading is '{nearest[1]}' at line {nearest[0] + 1}" if nearest else ""
            issues.append(
                f"{relative}: Contents row '{name}' records line {recorded}"
                f" but no ## section heading exists within {TOLERANCE} lines{hint}"
            )
            continue
        anchor = min(nearby)
        if anchor <= previous_heading_line:
            issues.append(
                f"{relative}: Contents row '{name}' line {recorded} points at a section"
                " that precedes the previous row's section"
            )
        previous_heading_line = max(previous_heading_line, anchor)

    first_recorded = rows[0][2]
    for position, heading in after_contents:
        if position + 1 < first_recorded - TOLERANCE:
            issues.append(
                f"{relative}: section '{heading}' at line {position + 1} is missing"
                " from the Contents table"
            )

    return issues


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else Path.cwd().resolve()
    issues: list[str] = []
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts:
            continue
        issues.extend(check_file(path, root))
    return report(issues, "contents tables match section headings")


if __name__ == "__main__":
    raise SystemExit(main())
