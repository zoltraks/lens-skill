"""Canonical table formatter implementing the Table Formatting Rules in
process/report-format.md.

Copy this file into the audited repository's `work/` directory (or the
repository root when no `work/` exists) as `format-table.tmp.py`, run it
on the report file, verify that all `|` separators align vertically, then
remove the copy.

The formatter normalizes separator cells that are separator-shaped but
lack hyphens, warns about rows that begin with `||`, and warns about
columns that are empty in every row - those columns are removed only
when `--drop-empty-columns` is passed.

Usage: python format-table.py <report.md> [--check] [--drop-empty-columns]
"""

from __future__ import annotations

import argparse
import sys


def parse_row(line):
    parts = line.split("|")
    cells = parts[1:-1] if parts and parts[-1].strip() == "" else parts[1:]
    return [c.strip() for c in cells]


def is_sep(cells):
    return len(cells) > 0 and all(set(c) <= set("-:") and "-" in c for c in cells)


def sep_like(cells):
    return (
        len(cells) > 0
        and all(set(c) <= set("-:") for c in cells)
        and any("-" in c for c in cells)
    )


def format_block(block, start, warnings, drop_empty):
    """Return the formatted lines for one table block."""
    for offset, line in enumerate(block):
        if line.startswith("||"):
            warnings.append(f"line {start + offset + 1}: row starts with '||'")
    rows = [parse_row(line) for line in block]
    ncols = max(len(r) for r in rows)
    rows = [r + [""] * (ncols - len(r)) for r in rows]
    sep_index = next((i for i, r in enumerate(rows) if sep_like(r)), None)
    if sep_index is not None and not is_sep(rows[sep_index]):
        warnings.append(
            f"line {start + sep_index + 1}: separator cell(s) lack hyphens - normalized"
        )
        rows[sep_index] = ["-" for _ in rows[sep_index]]
    if ncols > 1:
        data = [r for i, r in enumerate(rows) if i != sep_index]
        empty = [j for j in range(ncols) if all(r[j] == "" for r in data)]
        if empty:
            names = ", ".join(str(j + 1) for j in empty)
            if drop_empty and len(empty) < ncols:
                warnings.append(f"line {start + 1}: dropped empty column(s) {names}")
                rows = [
                    [c for j, c in enumerate(r) if j not in empty] for r in rows
                ]
                ncols -= len(empty)
            else:
                warnings.append(
                    f"line {start + 1}: column(s) {names} empty in every row"
                    " (use --drop-empty-columns to remove)"
                )
    widths = [0] * ncols
    for r in rows:
        if is_sep(r):
            continue
        for j, c in enumerate(r):
            widths[j] = max(widths[j], len(c))
    out = []
    for r in rows:
        if is_sep(r):
            out.append("|" + "|".join("-" * (w + 2) for w in widths) + "|")
        else:
            out.append(
                "| " + " | ".join(c.ljust(widths[j]) for j, c in enumerate(r)) + " |"
            )
    return out


def format_text(text, drop_empty=False):
    """Return (formatted lines, warnings, table count)."""
    lines = text.replace("\r\n", "\n").split("\n")
    out, warnings, tables = [], [], 0
    in_fence = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            i += 1
            continue
        if not in_fence and line.startswith("|"):
            block = []
            while i < len(lines) and lines[i].startswith("|"):
                block.append(lines[i])
                i += 1
            out.extend(format_block(block, i - len(block), warnings, drop_empty))
            tables += 1
        else:
            out.append(line)
            i += 1
    return out, warnings, tables


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("path", help="Markdown report to format")
    parser.add_argument(
        "--check",
        action="store_true",
        help="report files that need formatting without writing",
    )
    parser.add_argument(
        "--drop-empty-columns",
        action="store_true",
        help="remove columns that are empty in every row",
    )
    args = parser.parse_args()

    raw = open(args.path, "rb").read()
    crlf = b"\r\n" in raw
    out, warnings, tables = format_text(
        raw.decode("utf-8"), drop_empty=args.drop_empty_columns
    )

    for warning in warnings:
        print(f"warn: {warning}", file=sys.stderr)

    if args.check:
        if out != raw.decode("utf-8").replace("\r\n", "\n").split("\n"):
            print(f"{args.path}: needs formatting")
            return 1
        print(f"{args.path}: {tables} table(s) already formatted")
        return 0

    eol = "\r\n" if crlf else "\n"
    open(args.path, "wb").write(eol.join(out).encode("utf-8"))
    print(f"formatted {tables} tables")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
