#!/usr/bin/env python3
"""Canonical comment aligner implementing the Comments In Plain-Text Blocks
rule in `docs/STYLE.md`.

Inside every fenced block that carries trailing `#` comments - untagged
plain-text blocks and shell-tagged blocks - all comments share one column.
When most comments already sit at one column the outliers align to it, otherwise
the column is the longest entry plus a two-space gap. `--compact` forces the
minimum column.

A fenced block is skipped entirely when `<!-- align-comments: off -->` is the
line before its opening fence, optionally separated from the fence by one
blank line - intended for deliberate examples of misalignment.

Copy this file into the working repository's `work/` directory (or the
repository root when no `work/` exists) as `align-comments.tmp.py`, run it
on the document file, verify the block, then remove the copy.

Usage: python align-comments.py <document.md> [--check] [--compact] [--payload-markdown]

  --check              report misaligned comments and exit 1, without
                       writing the file
  --compact            move every block's column to the minimum (longest entry
                       plus two spaces) instead of keeping an established column
  --payload-markdown   also align comments inside fenced blocks nested in
                       ```markdown payload blocks
"""

import argparse
import os
import re
import sys
from collections import Counter

FENCE = re.compile(r"^\s*(`{3,})\s*(\w*)")
COMMENT = re.compile(r"^(.*\S)( +)(#(?: .*)?)$")

SHELL_TAGS = {"bash", "sh", "zsh", "shell", "console", "shellsession"}
DISABLE_COMMENT = "<!-- align-comments: off -->"


def decode(raw):
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16"), "utf-16"
    return raw.decode("utf-8"), "utf-8"


def processable(fences, payload_markdown):
    """True when the innermost fence is untagged or shell-tagged and any
    enclosing fences are markdown payloads allowed by --payload-markdown."""
    if not fences:
        return False
    lang = fences[-1][1]
    if lang != "" and lang not in SHELL_TAGS:
        return False
    outers = fences[:-1]
    return not outers or (payload_markdown and all(
        lang == "markdown" for _, lang in outers))


def align(lines, payload_markdown, compact):
    """Return (new_lines, misaligned) where misaligned lists
    (line_number, actual_column, expected_column)."""
    out = list(lines)
    fences = []
    block = []
    disabled = False
    misaligned = []

    def flush():
        if not block:
            return
        minimum = max(len(prefix) for _, prefix, _, _ in block) + 2
        dominant, count = Counter(
            actual for _, _, _, actual in block).most_common(1)[0]
        target = minimum if compact or count * 2 <= len(block) or \
            dominant < minimum else dominant
        for index, prefix, comment, actual in block:
            if actual != target:
                misaligned.append((index + 1, actual + 1, target + 1))
                out[index] = prefix + " " * (target - len(prefix)) + comment
        block.clear()

    for i, line in enumerate(lines):
        fence = FENCE.match(line)
        if fence:
            flush()
            marker = len(fence.group(1))
            if fences:
                if marker >= fences[-1][0]:
                    fences.pop()
                    if not fences:
                        disabled = False
            else:
                before = i - 1
                if before >= 0 and not lines[before].strip():
                    before -= 1
                disabled = before >= 0 and \
                    lines[before].strip() == DISABLE_COMMENT
                fences.append((marker, fence.group(2)))
            continue
        if disabled or not processable(fences, payload_markdown):
            continue
        stripped = line.rstrip()
        match = COMMENT.match(stripped)
        if not match or not match.group(1):
            continue
        minimum = 2 if fences[-1][1] in SHELL_TAGS else 1
        if len(match.group(2)) < minimum:
            continue
        comment = match.group(3).rstrip() or "#"
        block.append((i, match.group(1), comment, len(stripped) - len(comment)))

    flush()
    return out, misaligned


def main(path, check_only, compact, payload_markdown):
    raw = open(path, "rb").read()
    crlf = b"\r\n" in raw
    try:
        text, encoding = decode(raw)
    except UnicodeDecodeError:
        print(f"FAIL {path}: not decodable as UTF-8 or UTF-16, "
              "check the file encoding first")
        return 1
    lines = text.replace("\r\n", "\n").split("\n")

    out, misaligned = align(lines, payload_markdown, compact)

    if check_only:
        for number, actual, expected in misaligned:
            print(f"line {number}: comment at column {actual}, expected {expected}")
        if misaligned:
            print(f"{len(misaligned)} comment(s) misaligned")
            return 1
        print(f"PASS {path}: comments already aligned")
        return 0

    if out != lines:
        eol = "\r\n" if crlf else "\n"
        tmp = path + ".tmp-write"
        try:
            with open(tmp, "wb") as handle:
                handle.write(eol.join(out).encode(encoding))
            os.replace(tmp, path)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
    print(f"aligned {len(misaligned)} comment(s)")
    return 0


if __name__ == "__main__":
    for _stream in (sys.stdout, sys.stderr):
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(
        description="Align `#` comments inside fenced plain-text and shell blocks."
    )
    parser.add_argument("file")
    parser.add_argument("--check", action="store_true",
                        help="report misaligned comments without writing")
    parser.add_argument("--compact", action="store_true",
                        help="force the minimum column: longest entry plus two spaces")
    parser.add_argument("--payload-markdown", action="store_true",
                        help="also process blocks nested inside ```markdown payloads")
    args = parser.parse_args()
    raise SystemExit(
        main(args.file, args.check, args.compact, args.payload_markdown))
