#!/usr/bin/env python3
"""Extract candidate requirement ids from Markdown documents.

A candidate id is one that appears in a defining position: as the first
non-empty cell of a Markdown table row, at the start of a heading text, or at
the start of a list item followed by `:` or `-`. Ids that appear only in prose
are reported separately as referenced-only.

Usage:
    python3 scripts/extract-requirements.py <doc.md> [<doc.md> ...] [--pattern REGEX] [--json]

Exit code 0 means the extraction ran, 2 means usage or read errors.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_PATTERN = r"\b(?:[A-Z]{1,4}-\d{1,3}|REQ-\d+|FR-\d+|NFR-\d+)\b"

HEADING = re.compile(r"^\s*#{1,6}\s+(.*)$")
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(.*)$")
FENCE = re.compile(r"^\s*```")
TRAILER = re.compile(r"\s*:| +-")

OBLIGATION_HINTS = (
    (re.compile(r"future|deferred|post-mvp|out of scope", re.IGNORECASE), "future"),
    (re.compile(r"proposed|optional|may\b", re.IGNORECASE), "optional"),
    (re.compile(r"should|recommended", re.IGNORECASE), "recommended"),
)


def obligation_hint(text: str) -> str:
    for pattern, hint in OBLIGATION_HINTS:
        if pattern.search(text):
            return hint
    return "mandatory"


def defining_site(line: str, pattern: re.Pattern) -> tuple[str, str] | None:
    """(id, text) when the line defines an id in a candidate position."""
    if line.lstrip().startswith("|"):
        cells = [c.strip() for c in line.strip().split("|")]
        first = next((c for c in cells if c), "")
        match = pattern.match(first)
        if match:
            return match.group(0), line.strip()
    heading = HEADING.match(line)
    if heading:
        text = heading.group(1).strip()
        match = pattern.match(text)
        if match:
            return match.group(0), text
    item = LIST_ITEM.match(line)
    if item:
        text = item.group(1).strip()
        match = pattern.match(text)
        if match and TRAILER.match(text[match.end():]):
            return match.group(0), text
    return None


def extract(docs: list[tuple[str, str]], pattern: re.Pattern) -> dict:
    """Extract requirement records from `(path, text)` documents."""
    requirements: dict[str, dict] = {}
    occurrences: dict[str, int] = {}
    for path, text in docs:
        in_fence = False
        for number, line in enumerate(text.splitlines(), 1):
            if FENCE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for ident in pattern.findall(line):
                occurrences[ident] = occurrences.get(ident, 0) + 1
            site = defining_site(line, pattern)
            if site and site[0] not in requirements:
                ident, row_text = site
                requirements[ident] = {
                    "id": ident,
                    "path": path,
                    "line": number,
                    "text": row_text[:160],
                    "obligation_hint": obligation_hint(row_text),
                    "occurrences": occurrences[ident],
                }
    referenced_only = [
        ident for ident in occurrences if ident not in requirements
    ]
    for record in requirements.values():
        record["occurrences"] = occurrences[record["id"]]
    return {
        "requirements": list(requirements.values()),
        "referenced_only": referenced_only,
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Extract candidate requirement ids from Markdown documents"
    )
    parser.add_argument("docs", nargs="+", help="Markdown documents to scan")
    parser.add_argument(
        "--pattern", default=DEFAULT_PATTERN,
        help="requirement id regex (default: %(default)s)",
    )
    parser.add_argument(
        "--json", action="store_true", help="emit the result as JSON"
    )
    args = parser.parse_args(argv)

    try:
        pattern = re.compile(args.pattern)
    except re.error as exc:
        print(f"extract-requirements: invalid --pattern: {exc}", file=sys.stderr)
        return 2

    docs = []
    for name in args.docs:
        path = Path(name)
        if not path.is_file():
            print(f"extract-requirements: no such file: {name}", file=sys.stderr)
            return 2
        try:
            docs.append((name, path.read_text(encoding="utf-8")))
        except OSError as exc:
            print(
                f"extract-requirements: cannot read {name}: {exc}",
                file=sys.stderr,
            )
            return 2

    result = extract(docs, pattern)
    if args.json:
        print(
            json.dumps(
                {
                    "requirements": result["requirements"],
                    "referenced_only": result["referenced_only"],
                    "documents": args.docs,
                    "pattern": args.pattern,
                },
                indent=1,
            )
        )
    else:
        for record in result["requirements"]:
            print(
                f"{record['id']}  {record['path']}:{record['line']}  "
                f"{record['obligation_hint']}  ({record['occurrences']} "
                f"occurrence(s))  {record['text']}"
            )
        for ident in result["referenced_only"]:
            print(f"{ident}  (referenced only)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
