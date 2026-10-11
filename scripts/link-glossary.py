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

from __future__ import annotations

import re
import sys
from pathlib import Path


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

# Polish function words that legitimately neighbour a linked term - they
# carry no compound-name meaning even when a sentence start capitalizes
# them.
COMPOUND_NEIGHBOR_STOPWORDS_PL = COMPOUND_NEIGHBOR_STOPWORDS | {
    "I", "A", "O", "W", "We", "Z", "Ze", "Na", "Do", "Dla", "Od", "Po",
    "Przez", "Przy", "Pod", "Nad", "Przed", "Za", "Ku", "U", "Bez",
    "Nie", "To", "Ten", "Ta", "Te", "Tych", "Tym", "Tego", "Tej",
    "Jest", "Są", "Był", "Była", "Było", "Będzie", "Oraz", "Lub",
    "Albo", "Ale", "Więc", "Gdy", "Gdzie", "Jak", "Co", "Czy",
    "Który", "Która", "Które", "Którego", "Której", "Każdy", "Każda",
    "Każde", "Wszystkie", "Wszystko", "Jego", "Jej", "Ich", "Sam",
    "Sama", "Tak", "Także", "Również", "Ma", "Mają", "Może", "Mogą",
    "Musi", "Stanowi", "Między", "Obok", "Poza", "Wraz", "Jako",
}


def _compound_word(token: str, trailing: bool) -> str:
    link = re.fullmatch(r"\[([^\]]+)\]\([^)]*\)", token)
    if link:
        return link.group(1)
    if trailing:
        return re.sub(r"[^\w]+$", "", token)
    return re.sub(r"^[^\w]+", "", token)


def _capitalized_word(token: str) -> bool:
    """Unicode-aware `[A-Z][A-Za-z0-9]*` - Polish diacritics must count as
    letters so `Zgodność API` reads as a compound name."""
    return bool(
        re.fullmatch(r"[^\W\d_][^\W_]*(?:\.[^\W_]+)*", token)
        and token[0].isupper()
    )


def compound_context(line: str, start: int, end: int, stopwords=None) -> bool:
    if stopwords is None:
        stopwords = COMPOUND_NEIGHBOR_STOPWORDS
    j = start
    while j > 0 and line[j - 1] not in " \t":
        j -= 1
    if not re.search(r"[A-Za-z0-9]", line[j:start]):
        prev = line[:j].rstrip()
        if prev:
            prev_token = _compound_word(prev.split()[-1], trailing=False)
            if (
                prev_token not in stopwords
                and _capitalized_word(prev_token)
            ):
                return True
    k = end
    while k < len(line) and line[k] not in " \t":
        k += 1
    if re.fullmatch(r"[\"'`)\]}*]*", line[end:k]):
        nxt = line[k:].lstrip()
        if nxt:
            next_token = _compound_word(nxt.split()[0], trailing=True)
            if _capitalized_word(next_token):
                return True
    return False


FIELD_VALUE_LABELS = (
    "Pillar",
    "Severity",
    "Type",
    "Security",
    "Status",
    "Change",
    "Absence",
    "Verified",
    "Confidence",
    "Class",
    "Result",
    "Priority",
    "Likelihood",
    "Residual",
    "Owner",
    "Exploitability",
)

FIELD_VALUE_LABELS_PL = (
    "Filar",
    "Ważność",
    "Typ",
    "Bezpieczeństwo",
    "Status",
    "Zmiana",
    "Charakter odstępstwa",
    "Zweryfikowane",
    "Potwierdzone uruchomieniem",
    "Pewność oceny",
    "Klasa",
    "Wynik",
    "Priorytet",
    "Prawdopodobieństwo",
    "Ryzyko rezydualne",
    "Właściciel",
    "Wykorzystanie podatności",
    "Środek ograniczający ryzyko",
)

LANGUAGES = {
    "en": {
        "glossary_heading": "Glossary",
        "default_anchor": "glossary",
        "field_labels": FIELD_VALUE_LABELS,
        "stopwords": COMPOUND_NEIGHBOR_STOPWORDS,
    },
    "pl": {
        "glossary_heading": "Słownik",
        "default_anchor": "słownik",
        "field_labels": FIELD_VALUE_LABELS_PL,
        "stopwords": COMPOUND_NEIGHBOR_STOPWORDS_PL,
    },
}


def slugify(heading: str) -> str:
    return re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-")


def parse_glossary(
    lines: list[str], lang: dict
) -> tuple[list[str], dict[str, str], int, int]:
    """Return (index terms, term->anchor map, glossary start line, end line)."""
    heading_re = re.compile(r"^##\s+" + lang["glossary_heading"] + r"\s*$")
    heading_at = next(
        (i for i, l in enumerate(lines) if heading_re.match(l)), None
    )
    if heading_at is None:
        raise SystemExit(
            "report has no ## %s section" % lang["glossary_heading"]
        )
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
        if not cell:
            continue
        link = re.fullmatch(r"\[([^\]]+)\]\(#([^)]+)\)", cell)
        if link:
            terms.append(link.group(1))
            anchors[link.group(1)] = link.group(2)
        elif re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9/().+-]*", cell):
            terms.append(cell)
            anchors[cell] = lang["default_anchor"]
    return terms, anchors, heading_at, end


def mask_line(line: str, field_line) -> str:
    masked = re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line)
    masked = re.sub(r"\[[^\]]*\]\([^)]*\)", lambda m: " " * len(m.group(0)), masked)
    masked = re.sub(r"https?://\S+", lambda m: " " * len(m.group(0)), masked)
    masked = re.sub(r"\[[^\]]*\]", lambda m: " " * len(m.group(0)), masked)
    field = field_line.match(masked)
    if field:
        masked = masked[: field.end()] + " " * (len(masked) - field.end())
    return masked


def reconfigure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="backslashreplace")
        except Exception:
            pass


def main(path: str, lang_name: str = "en", check: bool = False) -> int:
    reconfigure_stdio()
    lang = LANGUAGES[lang_name]
    field_line = re.compile(
        r"^\s*[*-]\s+\*\*(?:" + "|".join(lang["field_labels"]) + r"):\*\*"
    )
    raw = Path(path).read_bytes()
    crlf = b"\r\n" in raw
    lines = raw.decode("utf-8").replace("\r\n", "\n").split("\n")
    terms, anchors, g_start, g_end = parse_glossary(lines, lang)
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
    out: list[str] = []
    for index, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        if g_start <= index < g_end:
            out.append(line)
            continue
        if re.match(r"^#{1,6}\s", line):
            out.append(line)
            continue
        masked = mask_line(line, field_line)
        inserts: list[tuple[int, int, str]] = []
        for match in pattern.finditer(masked):
            start, end_ = match.start(), match.end()
            before = masked[start - 1] if start else " "
            after = masked[end_] if end_ < len(masked) else " "
            if re.match(r"[\w/#.-]", before) or re.match(r"[\w/-]", after):
                continue
            if compound_context(masked, start, end_, lang["stopwords"]):
                skipped += 1
                continue
            term = variant_map[match.group(0)]
            if check:
                print(
                    "line %d: '%s' is not linked to #%s"
                    % (index + 1, match.group(0), anchors[term])
                )
            inserts.append((start, end_, f"[{match.group(0)}](#{anchors[term]})"))
        if check:
            linked += len(inserts)
            out.append(line)
            continue
        for start, end_, replacement in reversed(inserts):
            line = line[:start] + replacement + line[end_:]
            masked = masked[:start] + " " * len(replacement) + masked[end_:]
        linked += len(inserts)
        out.append(line)
    if check:
        print("%d unlinked occurrence(s)" % linked)
        return 1 if linked else 0
    eol = "\r\n" if crlf else "\n"
    Path(path).write_bytes(eol.join(out).encode("utf-8"))
    print(f"linked {linked} occurrence(s), skipped {skipped} compound-context occurrence(s)")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or "-h" in args or "--help" in args:
        print(
            "Usage: python link-glossary.py <report.md> "
            "[--lang en|pl] [--check]"
        )
        raise SystemExit(0 if args else 1)
    path = args[0]
    lang_name = "en"
    check = "--check" in args
    if "--lang" in args:
        lang_at = args.index("--lang")
        if lang_at + 1 >= len(args) or args[lang_at + 1] not in LANGUAGES:
            print("Usage: --lang en|pl")
            raise SystemExit(1)
        lang_name = args[lang_at + 1]
    raise SystemExit(main(path, lang_name, check))
