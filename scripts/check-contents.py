#!/usr/bin/env python3
"""Check that Contents tables match actual section headings.

For every Markdown file with a ``## Contents`` table, each row's recorded
line number must point at a real ``##`` heading, rows must stay in heading
order, and no ``##`` section may hide between the Contents table and the
first recorded row.

Row names may describe a single heading or a group of adjacent sections,
so only the recorded line anchor is checked, not the row label.

Pass ``--fix`` to rewrite each row's recorded line to the nearest section
heading that still follows the previous row's anchor.

Usage: python scripts/check-contents.py [--fix] <skill-directory>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from common import markdown_files, report


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


def fix_rows(lines: list[str], rows: list[tuple[int, str, int]],
             headings: list[tuple[int, str]], contents_at: int) -> list[str]:
    """Return lines with each row's recorded line snapped to a section heading.

    When rows and headings pair one-to-one they are zipped in order; otherwise
    each row snaps to the nearest heading that still follows the previous row's
    anchor.
    """
    anchors = sorted(position + 1 for position, _ in headings if position > contents_at)
    out = list(lines)
    one_to_one = len(rows) == len(anchors)
    previous = contents_at
    for position, (row_index, _name, recorded) in enumerate(rows):
        if one_to_one:
            nearest = anchors[position]
        else:
            candidates = [anchor for anchor in anchors if anchor > previous]
            if not candidates:
                break
            nearest = min(candidates, key=lambda anchor: abs(anchor - recorded))
        previous = nearest - 1
        if nearest != recorded:
            match = ROW.match(out[row_index])
            if match:
                replacement = str(nearest).ljust(match.end(2) - match.start(2))
                out[row_index] = (
                    out[row_index][: match.start(2)] + replacement + out[row_index][match.end(2) :]
                )
    return out


def collect_rows(lines: list[str], fences: list[bool],
                 contents_at: int) -> list[tuple[int, str, int]]:
    """Return the contents-table rows that follow the Contents heading.

    Fenced lines are skipped so example tables inside code blocks stay
    opaque, and collection stops at the first non-table line after rows
    begin.
    """
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
    return rows


def check_file(path: Path, root: Path, fix: bool = False) -> list[str]:
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

    rows = collect_rows(lines, fences, contents_at)

    if not rows:
        return [f"{relative}: Contents section has no rows"]

    after_contents = [(index, name) for index, name in headings if index > contents_at]

    if fix:
        out = fix_rows(lines, rows, headings, contents_at)
        if out != lines:
            path.write_text("\n".join(out) + "\n", encoding="utf-8")
            lines = out
            rows = collect_rows(lines, fences, contents_at)

    previous_heading_line = contents_at
    for row_index, name, recorded in rows:
        nearby = [position for position, _ in after_contents
                  if abs(position + 1 - recorded) <= TOLERANCE]
        if not nearby:
            nearest = min(
                after_contents,
                key=lambda item: abs(item[0] + 1 - recorded),
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
    arguments = [argument for argument in sys.argv[1:] if argument != "--fix"]
    fix = "--fix" in sys.argv[1:]
    root = Path(arguments[0]).resolve() if arguments else Path.cwd().resolve()
    issues: list[str] = []
    for path in markdown_files(root):
        issues.extend(check_file(path, root, fix))
    return report(issues, "contents tables match section headings")


if __name__ == "__main__":
    raise SystemExit(main())
