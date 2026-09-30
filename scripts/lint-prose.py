"""Pre-assembly prose linter for Lens report drafts.

Checks the prose rules ``validate-report.py`` enforces on assembled reports
so an author can lint draft text before composing the full document:
heading depth and blank-line spacing, semicolons outside code spans,
and the typographic characters the ASCII convention forbids
(em dash, en dash, arrow).

Copy into the audited repository's report-production directory as
``lint-prose.tmp.py`` when linting a draft.

Usage: python lint-prose.py <draft.md> [<draft2.md> ...]
Exit code 0 means all checks pass, 1 means failures were found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

EMDASH = chr(0x2014)
ENDASH = chr(0x2013)
ARROW = chr(0x2192)


def split_code(lines: list[str]) -> list[bool]:
    flags: list[bool] = []
    inside = False
    for line in lines:
        if line.lstrip().startswith("```"):
            inside = not inside
            flags.append(True)
            continue
        flags.append(inside)
    return flags


def strip_spans(value: str) -> str:
    value = re.sub(r"`[^`]*`", "", value)
    return re.sub(r"\]\([^)]*\)", "]", value)


def lint(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        return [f"{path}: not readable as UTF-8 ({error})"]
    lines = text.split("\n")
    fences = split_code(lines)
    failures: list[str] = []
    for index, (line, fenced) in enumerate(zip(lines, fences)):
        if fenced:
            continue
        if re.match(r"^#{4,} ", line):
            failures.append(f"{path}:{index + 1}: heading is deeper than ###")
            continue
        if re.match(r"^#{1,3} ", line):
            if index + 1 < len(lines) and lines[index + 1].strip() != "":
                failures.append(f"{path}:{index + 1}: heading is not followed by one blank line")
        value = strip_spans(line)
        if ";" in value:
            failures.append(f"{path}:{index + 1}: semicolon in prose: {line[:80]}")
        for character, name in ((EMDASH, "em dash"), (ENDASH, "en dash"), (ARROW, "arrow")):
            if character in value:
                failures.append(f"{path}:{index + 1}: {name} found: {line[:80]}")
    return failures


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python lint-prose.py <draft.md> [<draft2.md> ...]")
        return 1
    failures: list[str] = []
    for name in argv[1:]:
        failures.extend(lint(Path(name)))
    for message in failures:
        print(f"FAIL {message}")
    if failures:
        print(f"{len(failures)} issue(s) found")
        return 1
    print("PASS prose rules hold")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
