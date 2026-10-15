"""Pre-assembly prose linter for Lens report drafts.

Checks the prose rules ``validate-report.py`` enforces on assembled reports
so an author can lint draft text before composing the full document:
heading depth and blank-line spacing, semicolons outside code spans,
sentences split across a line break by a stray period, doubled end marks,
identifier ranges written with ``..``, sentences joined inside one paragraph
(single-sentence paragraphs are the default; a ``Sentence breaks | Off``
Document Information row suppresses it), and the typographic characters the
ASCII convention forbids (em dash, en dash, arrow).

Copy into the audited repository's report-production directory as
``lint-prose.tmp.py`` when linting a draft.

Usage: python lint-prose.py [--no-sentence-breaks] <draft.md> [<draft2.md> ...]
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
    r"(?:e\.g\.|i\.e\.|etc\.|vs\.|cf\.|ca\.|approx\.|U\.S\.|U\.K\.|"
    r"tj\.|np\.|itp\.|itd\.|m\.in\.|tzw\.|n\.bw\.|ang\.|por\.|zw\.|nr\.|"
    r"ok\.|im\.|prof\.|dr\.|inż\.|mgr\.|hab\.|płk\.|św\.)$"
)
SINGLE_INITIAL = re.compile(r"\b[A-ZĄĆĘŁŃÓŚŹŻ]\.$")
SENT_JOIN = re.compile(r"[.?!](?=\s+[A-ZĄĆĘŁŃÓŚŹŻ[(])")
NON_PROSE = re.compile(r"#{1,6}\s|\||[-*+]\s|\d+[.)]\s|>|<!--|\*\*")


def prose_line(line: str, fenced: bool) -> bool:
    # A prose paragraph line is flush-left and carries no markdown block
    # marker - list items, table rows, headings, quotes, comments, bold
    # run headings, and indented continuations are not prose.
    return bool(line.strip()) and not fenced and not (
        line[:1].isspace() or NON_PROSE.match(line)
    )


def sentence_breaks_on(text: str) -> bool:
    match = re.search(
        r"\|\s*Sentence breaks\s*\|\s*([^|]+)", text, re.IGNORECASE
    )
    return not (
        match and re.search(r"off|disabled|wyłącz", match.group(1), re.IGNORECASE)
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


def lint(path: Path, breaks_on: bool | None = None) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        return [f"{path}: not readable as UTF-8 ({error})"]
    if breaks_on is None:
        breaks_on = sentence_breaks_on(text)
    lines = text.replace("\r\n", "\n").split("\n")
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
            ):
                if nxt.lstrip()[:1].islower():
                    failures.append(
                        f"{path}:{index + 1}: sentence split at line break "
                        f"(period then lowercase): {line[:80]}"
                    )
                elif (
                    breaks_on
                    and prose_line(line, fenced)
                    and prose_line(nxt, fences[index + 1])
                ):
                    failures.append(
                        f"{path}:{index + 1}: sentence boundary inside a "
                        f"paragraph (separate sentences with one blank "
                        f"line): {line[:80]}"
                    )
        if breaks_on and prose_line(line, fenced):
            for match in SENT_JOIN.finditer(collapsed):
                prefix = collapsed[: match.start() + 1]
                if ABBREV_TAIL.search(prefix) or SINGLE_INITIAL.search(prefix):
                    continue
                failures.append(
                    f"{path}:{index + 1}: sentences joined in one line "
                    f"(each sentence is its own paragraph): {line[:80]}"
                )
                break
    return failures


def main(argv: list[str]) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="backslashreplace")
        except Exception:
            pass
    names = [arg for arg in argv[1:] if arg != "--no-sentence-breaks"]
    breaks_on = "--no-sentence-breaks" not in argv[1:]
    if not names:
        print(
            "Usage: python lint-prose.py [--no-sentence-breaks] "
            "<draft.md> [<draft2.md> ...]"
        )
        return 1
    failures: list[str] = []
    for name in names:
        failures.extend(lint(Path(name), None if breaks_on else False))
    for message in failures:
        print(f"FAIL {message}")
    if failures:
        print(f"{len(failures)} issue(s) found")
        return 1
    print("PASS prose rules hold")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
