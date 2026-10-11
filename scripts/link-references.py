"""Register-reference linker for Lens audit reports.

Reads the report's own register definitions - the ``###`` block headings
of the finding, risk, recommendation, and technical-debt registers plus
the Evidence Ledger and Validation Record table rows - and rewrites every
register identifier cited outside its defining location into a
``[<ID>](#anchor)`` link, per the Register Reference Links rules in
``process/report-format.md``.

Block registers (``FND``, ``RSK``, ``REC``, ``TDR``) link to their
``### <ID>: <title>`` heading anchor. Row-defined registers (``EVD``,
``PAR``) link to the anchor of the section holding their register table.
Project-qualified references such as ``api-service::FND-SEC-001`` resolve
to the block heading carrying the matching ``(<project>)`` suffix.

Exempt locations: fenced code blocks, inline code, headings, existing
links, URLs, and the defining location itself - the ``### <ID>:`` heading
or the register row whose first cell carries the identifier.

Copy this file into the audited repository's `work/` directory (or the
repository root when no `work/` exists) as ``link-references.tmp.py``, run
it on the report file after ``link-glossary.py`` and before
``format-table.py``, then remove the copy.

Usage: python link-references.py <report.md>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


FND_PILLARS = r"ARC|CQY|SEC|INF|AIP|CPR|API|STR"
BLOCK_FAMILY = r"(?:FND-(?:" + FND_PILLARS + r")|RSK|REC|TDR)-\d{3}"
ROW_FAMILY = r"(?:EVD-\d{3}|PAR-\d+)"
ID_TOKEN = r"(?:" + BLOCK_FAMILY + r"|" + ROW_FAMILY + r")"
QUALIFIED = r"(?:[\w][\w.-]*::)?"

REF = re.compile(QUALIFIED + ID_TOKEN)
BLOCK_HEADING = re.compile(r"^#{3,6}\s+(" + BLOCK_FAMILY + r")\s*:")
ROW_ID = re.compile(r"^(" + QUALIFIED + ROW_FAMILY + r")$")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
H2 = re.compile(r"^##\s+(.+?)\s*$")
PROJECT_SUFFIX = re.compile(r"\(([^()]+)\)\s*$")
LINK_MARKUP = re.compile(r"!?\[[^\]]*\]\([^)]*\)")


def slugify(heading: str) -> str:
    return re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-")


def mask_line(line: str) -> str:
    masked = re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line)
    masked = LINK_MARKUP.sub(lambda m: " " * len(m.group(0)), masked)
    masked = re.sub(r"https?://\S+", lambda m: " " * len(m.group(0)), masked)
    masked = re.sub(r"\[[^\]]*\]", lambda m: " " * len(m.group(0)), masked)
    return masked


def first_cell_token(line: str) -> tuple[str, int]:
    """Return (bare identifier, second-pipe index) when the row's first
    cell is exactly one row-defined register identifier (EVD or PAR),
    else ("", -1). Block-register cells are references, not definitions."""
    second_pipe = line.find("|", 1)
    if second_pipe < 0:
        return "", -1
    cell = line[1:second_pipe]
    link = re.fullmatch(r"\s*\[([^\]]+)\]\([^)]*\)\s*", cell)
    text = link.group(1) if link else cell.strip()
    if not re.fullmatch(QUALIFIED + ROW_FAMILY, text):
        return "", -1
    return text.rsplit("::", 1)[-1], second_pipe


def collect(lines: list[str]) -> tuple[
    dict[str, list[tuple[str, str | None]]], dict[str, str], list[str]
]:
    """Return (block ID -> [(slug, project)], row family -> section slug,
    warnings)."""
    blocks: dict[str, list[tuple[str, str | None]]] = {}
    section: dict[str, str] = {}
    warnings: list[str] = []
    counts: dict[str, int] = {}
    last_slug = ""
    in_fence = False
    for index, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        heading = HEADING.match(line)
        if heading:
            base = slugify(heading.group(2))
            seen = counts.get(base, 0)
            counts[base] = seen + 1
            last_slug = base if seen == 0 else f"{base}-{seen}"
            block = BLOCK_HEADING.match(line)
            if block:
                suffix = PROJECT_SUFFIX.search(heading.group(2))
                blocks.setdefault(block.group(1), []).append(
                    (last_slug, suffix.group(1) if suffix else None)
                )
            continue
        if line.startswith("|"):
            first, _ = first_cell_token(line)
            family = next(
                (f for f in ("EVD", "PAR") if first.startswith(f + "-")), None
            )
            if family and family not in section:
                if last_slug:
                    section[family] = last_slug
                else:
                    warnings.append(
                        f"line {index + 1}: {family} register row has no "
                        "preceding heading to anchor"
                    )
    return blocks, section, warnings


def resolve(
    token: str,
    bare: str,
    qualifier: str | None,
    line_no: int,
    current_h2: str,
    blocks: dict[str, list[tuple[str, str | None]]],
    section: dict[str, str],
    warnings: list[str],
) -> str | None:
    if bare.startswith(("EVD-", "PAR-")):
        family = "EVD" if bare.startswith("EVD-") else "PAR"
        anchor = section.get(family)
        if anchor is None:
            warnings.append(f"line {line_no}: {token} has no {family} register section")
        return anchor
    candidates = blocks.get(bare, [])
    if qualifier is not None:
        matched = [
            slug
            for slug, project in candidates
            if project is not None and project.lower() == qualifier.lower()
        ]
        if len(matched) == 1:
            return matched[0]
        warnings.append(
            f"line {line_no}: {token} resolves to {len(matched)} "
            f"{qualifier}:: blocks"
        )
        return None
    if len(candidates) == 1:
        return candidates[0][0]
    if len(candidates) > 1:
        matched = [
            slug
            for slug, project in candidates
            if project is not None and slugify(project) == current_h2
        ]
        if len(matched) == 1:
            return matched[0]
        warnings.append(
            f"line {line_no}: {token} is ambiguous across projects - qualify it"
        )
        return None
    warnings.append(f"line {line_no}: {token} cites an undefined identifier")
    return None


def main(path: str) -> int:
    raw = Path(path).read_bytes()
    crlf = b"\r\n" in raw
    lines = raw.decode("utf-8").replace("\r\n", "\n").split("\n")
    blocks, section, warnings = collect(lines)
    linked = 0
    in_fence = False
    current_h2 = ""
    out: list[str] = []
    for index, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        h2 = H2.match(line)
        if h2:
            current_h2 = slugify(h2.group(1))
        if HEADING.match(line):
            out.append(line)
            continue
        masked = mask_line(line)
        first, cell_end = first_cell_token(line) if line.startswith("|") else ("", -1)
        inserts: list[tuple[int, int, str]] = []
        for match in REF.finditer(masked):
            start, end_ = match.start(), match.end()
            before = masked[start - 1] if start else " "
            after = masked[end_] if end_ < len(masked) else " "
            if re.match(r"[\w/#.:-]", before) or re.match(r"[\w/-]", after):
                continue
            token = match.group(0)
            qualifier, _, bare = token.partition("::")
            if not bare:
                qualifier, bare = None, qualifier
            if first and bare == first and start < cell_end:
                continue
            anchor = resolve(
                token, bare, qualifier, index + 1, current_h2,
                blocks, section, warnings,
            )
            if anchor is not None:
                inserts.append((start, end_, f"[{token}](#{anchor})"))
        for start, end_, replacement in reversed(inserts):
            line = line[:start] + replacement + line[end_:]
            masked = masked[:start] + " " * len(replacement) + masked[end_:]
        linked += len(inserts)
        out.append(line)
    for warning in warnings:
        print(f"warn: {warning}", file=sys.stderr)
    eol = "\r\n" if crlf else "\n"
    Path(path).write_bytes(eol.join(out).encode("utf-8"))
    print(f"linked {linked} register reference(s)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python link-references.py <report.md>")
        raise SystemExit(1)
    raise SystemExit(main(sys.argv[1]))
