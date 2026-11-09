#!/usr/bin/env python3
"""Reformat an existing audit or review report to the current report contract.

Applies the mechanical conventions: title form, Document Information rows,
bolded Overall score, bare Projects names, no contents table, conditional
Language row, capitalized descriptive values, natural evidence-mode forms,
omitted Not-collected lines, occupied-band-only Risk Maps, a shared
Evaluation Legend in multi-project reports, and compact register titles.

Non-mechanical content (findings, evidence, prose) is left untouched.

Usage: python reformat-report.py <report.md> [--check]

  --check   report the changes it would make without writing, exit 1 when
            any change is pending.
"""

from __future__ import annotations
import re, sys


def find_title_name(line: str) -> str | None:
    m = re.match(r"^#\s+(.+?)\s*$", line)
    if not m:
        return None
    t = m.group(1).strip()
    for suffix in (" Software Audit Report", " Audit Report", " - Lens audit report",
                   " - Lens Audit Report", " Lens audit report", " Lens Audit Report"):
        if t.endswith(suffix):
            return t[: -len(suffix)]
    return t.split(" - ")[0] if " - " in t else t


def reformat(text: str) -> tuple[str, list[str]]:
    lines = text.split("\n")
    out: list[str] = []
    changes: list[str] = []
    i = 0
    legend_block = None
    first_project_seen = False
    legend_emitted = False

    while i < len(lines):
        line = lines[i]

        # 1. Title -> '# <Name> Audit Report'
        if i == 0 or (not out and line.startswith("# ")):
            name = find_title_name(line)
            if name is not None and line.strip() != f"# {name} Audit Report":
                out.append(f"# {name} Audit Report")
                changes.append("title normalized to '<Name> Audit Report'")
                i += 1
                continue

        # 2. Drop ## Table of Contents block
        if re.match(r"^## Table of Contents\s*$", line.strip()):
            j = i + 1
            while j < len(lines) and (lines[j].startswith("- [") or not lines[j].strip()):
                j += 1
            changes.append("removed '## Table of Contents' section")
            i = j
            continue

        # 3. Drop '| Language | English' row
        if re.match(r"^\|\s*Language\s*\|\s*English\s*\|", line):
            changes.append("removed Language row (English)")
            i += 1
            continue

        # 4. Overall score row -> '**Overall score** | **X/10** (Band)'
        m = re.match(r"^(\|\s*)(\*\*)?Overall score(\*\*)?\s*\|\s*(\*\*)?([\d.]+/10)( \(.*?\))?(\*\*)?\s*\|", line)
        if m:
            band = m.group(6) or ""
            repl = f"{m.group(1)}**Overall score** | **{m.group(5)}**{band} |"
            rest = line[m.end():]
            if rest.strip().startswith("|") or rest.strip() == "":
                pass
            new = repl
            if new != line:
                changes.append("Overall score row bolded")
                out.append(new + line[m.end():])
                i += 1
                continue

        # 5. Projects row: strip 'Project `x`' link text to bare 'x'
        if re.match(r"^\|\s*Projects\s*\|", line):
            new = re.sub(r"\[Project `?([^`\]]+)`?\]\((#project-[^)]*)\)", r"[\1](\2)", line)
            if new != line:
                changes.append("Projects row uses bare project names")
                out.append(new)
                i += 1
                continue

        # 6. Doc Info descriptive values capitalized / naturalized
        if re.match(r"^\|\s*[^|]+\|\s*", line):
            for old, newv in (
                ("executed-commands", "Executed commands"),
                ("executed-readonly", "Executed read-only"),
                ("source-only", "Source-only"),
                ("unversioned working tree", "Unversioned working tree"),
            ):
                nl = line.replace("| " + old, "| " + newv, 1)
                if nl != line:
                    changes.append(f"Document Information value '{old}' normalized")
                    line = nl
            # evidence-mode token in prose/backticks -> natural form
            if "executed-commands" in line and "Evidence Mode" not in line:
                line = line.replace("`executed-commands`", "executed commands").replace(
                    "executed-commands", "executed commands")
                changes.append("evidence-mode token naturalized in prose")

        # 7. Drop '**Team & Continuity** Not collected...' line
        if re.match(r"^\*\*Team & Continuity\*\*\s*Not collected", line.strip()):
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            changes.append("removed Not-collected Team & Continuity line")
            i = j
            continue

        # 8. Capture first **Legend**+table for hoisting (multi-project) or keep
        if line.strip() == "**Legend**":
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            block = []
            while j < len(lines) and lines[j].strip().startswith("|"):
                block.append(lines[j]); j += 1
            if legend_block is None:
                legend_block = ["**Legend**", ""] + block + [""]
            i = j
            continue

        # 9. Empty Risk Map rows - strip rows whose likelihood cells are all empty
        out.append(line)
        i += 1

    text2 = "\n".join(out)

    # Risk Map empty-row removal
    def rm_map(m):
        rows = m.group(0).split("\n")
        kept = [r for r in rows if not (
            r.lstrip().startswith("|") and "Impact" not in r
            and len([c for c in r.split("|")[2:-1] if c.strip()]) == 0
            and len(r.split("|")) > 3)]
        if len(kept) != len(rows):
            changes.append("removed empty Risk Map rows")
        return "\n".join(kept)
    text2 = re.sub(r"\*\*Risk Map\*\*\n\n\| Impact[^\n]*\n(?:\|[^\n]*\n)+", rm_map, text2)

    # Hoist legend to '## Evaluation Legend' before first '## Project' in multi-project
    if re.search(r"^## Project `", text2, re.M):
        text2 = re.sub(r"\*\*Legend\*\*\n\n\| Band[^\n]*\n(?:\|[^\n]*\n)+", "", text2)
        if "## Evaluation Legend" not in text2:
            leg = ("## Evaluation Legend\n\n| Band      | Score |\n"
                   "|-----------|-------|\n| Poor      | 1-3   |\n| Average   | 4-6   |\n"
                   "| Good      | 7-8   |\n| Excellent | 9-10  |\n\n")
            text2 = re.sub(r"(## Project `)", leg + r"\1", text2, count=1)
            changes.append("hoisted shared '## Evaluation Legend'")

    # Register titles: flag overlong (manual review hint)
    for m in re.finditer(r"^### ((?:FND|RSK|REC|TDR)-\d+): (.{60,})", text2, re.M):
        changes.append(f"NOTE {m.group(1)}: long register title '{m.group(2)[:40]}...' - shorten by hand")

    return text2, changes


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__); return 2
    path = sys.argv[1]
    check = "--check" in sys.argv
    text = open(path).read()
    new, changes = reformat(text)
    if not changes:
        print(f"{path}: already conforms")
        return 0
    for c in changes:
        print(f"  {c}")
    if check:
        print(f"{path}: {len(changes)} pending change(s)")
        return 1
    open(path, "w").write(new)
    print(f"{path}: applied {len(changes)} change(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
