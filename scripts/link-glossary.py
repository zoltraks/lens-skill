"""Glossary linker for Lens audit reports.

Reads the report's own `## Glossary` index table and `###` descriptions,
then inserts `[TERM](#anchor)` links on every eligible body occurrence,
applying the same exemption rules that `validate-report.py` enforces:
fenced code blocks, inline code, headings, URLs, existing links,
hyphenated or slashed compound identifiers, and capitalized compound
names stay untouched.

Copy this file into the audited repository's `work/` directory (or the
repository root when no `work/` exists) as `link-glossary.tmp.py`, run it
on the report file before `format-table.py`, then remove the copy.

Usage: python link-glossary.py <report.md>
"""

import re
import sys


GLOSSARY_VARIANTS: dict[str, list[str]] = {
    "HTTP(S)": ["HTTP(S)", "HTTPS", "HTTP"],
    "P1-P4": ["P1-P4", "P1", "P2", "P3", "P4"],
    "ISO": ["ISO/IEC", "ISO"],
    "CISQ": ["CISQ/SQALE", "CISQ"],
    "AI": ["AI/ML", "AI"],
}


def glossary_variants(term: str) -> list[str]:
    variants = list(GLOSSARY_VARIANTS.get(term, [term]))
    if re.fullmatch(r"[A-Z]{2,}", term):
        variants.append(term + "s")
    return variants


COMPOUND_NEIGHBOR_STOPWORDS = {
    "The", "A", "An", "This", "That", "These", "Those", "Each", "Every", "All", "Any", "No",
    "Not", "Both", "Same", "Only", "Just", "Even", "Such", "Its", "Our", "Their", "Per", "Via",
    "For", "From", "Into", "On", "In", "At", "By", "As", "To", "Of", "Or", "And", "But", "So",
    "Yet", "If", "When", "While", "Where", "How", "Why", "What", "Which", "Who", "With",
    "Without", "Within", "Is", "Are", "Was", "Were", "Be", "Been", "Do", "Does", "Did", "Has",
    "Have", "Had", "Can", "Could", "Will", "Would", "Shall", "Should", "May", "Might", "Must",
    "Than", "Then", "Thus", "Also", "After", "Before", "During", "Until", "Since", "Over",
    "Under", "Fits", "Use", "Uses", "Used", "Using",
}


def _compound_word(token: str, trailing: bool) -> str:
    link = re.fullmatch(r"\[([^\]]+)\]\([^)]*\)", token)
    if link:
        return link.group(1)
    if trailing:
        return re.sub(r"[^A-Za-z0-9]+$", "", token)
    return re.sub(r"^[^A-Za-z0-9]+", "", token)


def compound_context(line: str, start: int, end: int) -> bool:
    j = start
    while j > 0 and line[j - 1] not in " \t":
        j -= 1
    if not re.search(r"[A-Za-z0-9]", line[j:start]):
        prev = line[:j].rstrip()
        if prev:
            prev_token = _compound_word(prev.split()[-1], trailing=False)
            if (
                prev_token not in COMPOUND_NEIGHBOR_STOPWORDS
                and re.fullmatch(r"[A-Z][A-Za-z0-9]*(?:\.[A-Za-z0-9]+)*", prev_token)
            ):
                return True
    k = end
    while k < len(line) and line[k] not in " \t":
        k += 1
    if re.fullmatch(r"[\"'`)\]}*]*", line[end:k]):
        nxt = line[k:].lstrip()
        if nxt:
            next_token = _compound_word(nxt.split()[0], trailing=True)
            if re.fullmatch(r"[A-Z][A-Za-z0-9]*(?:\.[A-Za-z0-9]+)*", next_token):
                return True
    return False


def slugify(heading: str) -> str:
    return re.sub(r"[^a-z0-9 _-]", "", heading.lower()).replace(" ", "-")


def parse_glossary(lines: list[str]) -> tuple[list[str], dict[str, str], int, int]:
    """Return (index terms, term->anchor map, glossary start line, end line)."""
    heading_at = next(
        (i for i, l in enumerate(lines) if re.match(r"^##\s+Glossary\s*$", l)), None
    )
    if heading_at is None:
        raise SystemExit("report has no ## Glossary section")
    end = next(
        (i for i in range(heading_at + 1, len(lines)) if re.match(r"^##\s+\S", lines[i])),
        len(lines),
    )
    sub_slugs: dict[str, str] = {}
    table: list[str] = []
    for i in range(heading_at + 1, end):
        line = lines[i]
        m = re.match(r"^###\s+(.+?)\s*$", line)
        if m:
            term = re.split(r"\s*\(", m.group(1), 1)[0].strip()
            sub_slugs[term] = slugify(m.group(1))
            break
        if line.startswith("|"):
            table.append(line)
        elif table:
            break
    terms: list[str] = []
    anchors: dict[str, str] = {}
    for row in table[2:]:
        if not row.startswith("|") or re.match(r"^\|[\s\-:|]+\|?$", row):
            continue
        cell = row.split("|")[1].strip()
        link = re.fullmatch(r"\[([^\]]+)\]\(#([^)]+)\)", cell)
        if link:
            terms.append(link.group(1))
            anchors[link.group(1)] = link.group(2)
        elif re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9/().+-]*", cell):
            terms.append(cell)
            anchors[cell] = "glossary"
    return terms, anchors, heading_at, end


def mask_line(line: str) -> str:
    masked = re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line)
    masked = re.sub(r"\[[^\]]*\]\([^)]*\)", lambda m: " " * len(m.group(0)), masked)
    masked = re.sub(r"https?://\S+", lambda m: " " * len(m.group(0)), masked)
    masked = re.sub(r"\[[^\]]*\]", lambda m: " " * len(m.group(0)), masked)
    return masked


def main(path: str) -> int:
    text = open(path, encoding="utf-8").read().replace("\r\n", "\n")
    lines = text.split("\n")
    terms, anchors, g_start, g_end = parse_glossary(lines)
    variant_map: dict[str, str] = {}
    for term in terms:
        for variant in glossary_variants(term):
            variant_map[variant] = term
    pattern = re.compile(
        "|".join(re.escape(v) for v in sorted(variant_map, key=len, reverse=True))
    )
    linked = 0
    skipped = 0
    in_fence = False
    in_glossary = False
    out: list[str] = []
    for lineno, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        if lineno == g_start:
            in_glossary = True
            out.append(line)
            continue
        if in_glossary:
            if lineno == g_end:
                in_glossary = False
            else:
                out.append(line)
                continue
        if re.match(r"^#{1,6}\s", line):
            out.append(line)
            continue
        masked = mask_line(line)
        inserts: list[tuple[int, int, str]] = []
        for match in pattern.finditer(masked):
            start, end_ = match.start(), match.end()
            before = masked[start - 1] if start else " "
            after = masked[end_] if end_ < len(masked) else " "
            if re.match(r"[\w/#.-]", before) or re.match(r"[\w/-]", after):
                continue
            if compound_context(masked, start, end_):
                skipped += 1
                continue
            term = variant_map[match.group(0)]
            inserts.append((start, end_, f"[{match.group(0)}](#{anchors[term]})"))
        for start, end_, replacement in reversed(inserts):
            line = line[:start] + replacement + line[end_:]
            masked = masked[:start] + " " * len(replacement) + masked[end_:]
        linked += len(inserts)
        out.append(line)
    open(path, "w", encoding="utf-8").write("\n".join(out))
    print(f"linked {linked} occurrence(s), skipped {skipped} compound-context occurrence(s)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python link-glossary.py <report.md>")
        raise SystemExit(1)
    raise SystemExit(main(sys.argv[1]))
