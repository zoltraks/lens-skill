"""Pre-assembly prose linter for Lens report drafts.

Checks the prose rules ``validate-report.py`` enforces on assembled reports
so an author can lint draft text before composing the full document:
heading depth and blank-line spacing, semicolons outside code spans,
sentences split across a line break by a stray period, doubled end marks,
identifier ranges written with ``..``, and the typographic characters the
ASCII convention forbids (em dash, en dash, arrow).

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

ID_RANGE = re.compile(r"\b[A-Z]{2,8}-[A-Z0-9-]*\d+\.\.")
ABBREV_TAIL = re.compile(
    r"(?:e\.g\.|i\.e\.|etc\.|vs\.|cf\.|ca\.|approx\.|U\.S\.|U\.K\.)$"
)


def split_code(lines: list[str]) -> list[bool]:
    flags: list[bool] = []
    inside = False
    # A leading YAML frontmatter block is metadata, not prose.
    frontmatter = 0
    for index, line in enumerate(lines):
        if line == "---" and (index == 0 or frontmatter == 1):
            frontmatter += 1
            flags.append(True)
            continue
        if frontmatter == 1:
            flags.append(True)
            continue
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
            if index > 0 and lines[index - 1].strip() != "":
                failures.append(f"{path}:{index + 1}: heading is not preceded by one blank line")
        value = strip_spans(line)
        if ";" in value:
            failures.append(f"{path}:{index + 1}: semicolon in prose: {line[:80]}")
        for character, name in ((EMDASH, "em dash"), (ENDASH, "en dash"), (ARROW, "arrow")):
            if character in value:
                failures.append(f"{path}:{index + 1}: {name} found: {line[:80]}")
        collapsed = strip_spans(
            re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)
        )
        if ID_RANGE.search(collapsed):
            failures.append(
                f"{path}:{index + 1}: identifier range with '..' "
                f"(cite each identifier): {line[:80]}"
            )
        if re.match(r"^#{1,3} ", line) or line.startswith("|"):
            continue
        # The raw tail decides what the reader sees: a trailing code span or
        # link means the prose did not end at an earlier period - a wrapped
        # quote-subject like `…`. `Option` / continues is a legal break.
        tail = line.rstrip()
        if re.search(r"[,;:]\.$", strip_spans(tail)):
            failures.append(f"{path}:{index + 1}: doubled end mark: {line[:80]}")
        elif (
            tail.endswith(".")
            and not ABBREV_TAIL.search(tail)
            and not re.match(r"^\s*\d+\.$", tail)
            and index + 1 < len(lines)
        ):
            nxt = lines[index + 1]
            if (
                nxt.strip()
                and not fences[index + 1]
                and not re.match(r"^\s*(#{1,6}\s|\||[-*+]\s|>|```|<!--)", nxt)
                and nxt.lstrip()[:1].islower()
            ):
                failures.append(
                    f"{path}:{index + 1}: sentence split at line break "
                    f"(period then lowercase): {line[:80]}"
                )
    return failures


def main(argv: list[str]) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="backslashreplace")
        except Exception:
            pass
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
