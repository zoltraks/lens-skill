"""Canonical table formatter implementing the Table Formatting Rules in
process/report-format.md.

Copy this file into the audited repository's `work/` directory (or the
repository root when no `work/` exists) as `format-table.tmp.py`, run it
on the report file, verify that all `|` separators align vertically, then
remove the copy.

Usage: python format-table.py <report.md>
"""

import sys


def parse_row(line):
    parts = line.split("|")
    cells = parts[1:-1] if parts and parts[-1].strip() == "" else parts[1:]
    return [c.strip() for c in cells]


def is_sep(cells):
    return len(cells) > 0 and all(set(c) <= set("-:") and "-" in c for c in cells)


def main(path):
    raw = open(path, "rb").read()
    crlf = b"\r\n" in raw
    lines = raw.decode("utf-8").replace("\r\n", "\n").split("\n")

    out, i, tables = [], 0, 0
    in_fence = False
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
            rows = [parse_row(l) for l in block]
            ncols = max(len(r) for r in rows)
            rows = [r + [""] * (ncols - len(r)) for r in rows]
            widths = [1] * ncols
            for r in rows:
                if is_sep(r):
                    continue
                for j, c in enumerate(r):
                    widths[j] = max(widths[j], len(c))
            for r in rows:
                if is_sep(r):
                    out.append("|" + "|".join("-" * (w + 2) for w in widths) + "|")
                else:
                    out.append("| " + " | ".join(c.ljust(widths[j]) for j, c in enumerate(r)) + " |")
            tables += 1
        else:
            out.append(line)
            i += 1

    eol = "\r\n" if crlf else "\n"
    open(path, "wb").write(eol.join(out).encode("utf-8"))
    print(f"formatted {tables} tables")


if __name__ == "__main__":
    main(sys.argv[1])
