#!/usr/bin/env python3
"""Check Polish-contract invariants that mapped-copy validation cannot see.

`map-translation.py` + `validate-report.py` verify the Polish report
against the English contract after vocabulary inversion. This tool checks
the Polish text itself:

* Summary-table titles must agree with the `### FND-...`, `### RSK-...`,
  `### REC-...`, and `### TDR-...` block headings they index - the title
  may live in a different column per register, so every cell of the row
  that carries the identifier link is compared after markup is stripped.
* Prose counts such as `22 ustaleń` or `13 ryzyk` must equal the real
  register block/row counts (FND/RSK/REC block headings, EVD ledger rows).
* `* **Label:**` fields inside `### FND-…`, `### RSK-…`, `### REC-…`, and
  `### TDR-…` blocks must come from that register's contract label set -
  a label borrowed from another register (for example `Skutek` in a
  finding block) leaves the English-mapped copy missing a required field.
* Every `](#anchor)` target must resolve to a heading slug - renamed
  translated headings silently orphan links the mapped copy rewrites.
* Prose sentences outside tables stay within a word limit - long chained
  sentences are a known translation defect class. Warn-level only.

Spell checking stays external (a real dictionary), per the polish-language
contract - this tool checks only mechanical agreement.

Copy this file into the audited repository's `work/` directory as
`check-translation.tmp.py` before running it against a report there.

Usage:
    check-translation.py <translated.md> [--max-words N]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ID_HEADING = re.compile(r"^###\s+((?:FND|RSK|REC|TDR)-[A-Z0-9-]+):\s*(.+?)\s*$")
ROW_ID = re.compile(r"^\|\s*\[?((?:FND|RSK|REC|TDR|EVD)-[A-Z0-9-]+)\]?")
LINK = re.compile(r"\[([^\]]+)\]\([^)]*\)")
INTERNAL_LINK = re.compile(r"\]\(#([^)\s]+)\)")
BLOCK_FIELD = re.compile(r"^\*\s+\*\*([^:*]+):\*\*")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$")

# `* **Label:**` fields allowed inside each register's detail blocks,
# taken from the label tables in `translations/polish-language.md` -
# keep in sync when the contract adds or renames a field. Labels unique
# to one register (for example `Środek ograniczający ryzyko`, `Zwłoka`,
# `Zależy od`) must not leak into another register's blocks.
BLOCK_LABELS = {
    "FND": {
        "Filar", "Ważność", "Tytuł", "Wynik", "Status", "Zmiana",
        "Weryfikacja", "Typ", "Bezpieczeństwo", "Obiekty", "Podstawa",
        "Kryterium", "Charakter odstępstwa", "Opis", "Wpływ",
        "Zalecenie", "Metoda", "Zweryfikowane",
        "Potwierdzone uruchomieniem", "Łamanie kompatybilności",
        "Dotyczy", "Pewność oceny", "Czynniki łagodzące",
        "Wykorzystanie podatności", "Dowód", "Podstawa pochodzenia",
    },
    "RSK": {
        "Ryzyko", "Opis", "Źródło", "Wpływ", "Zakres",
        "Prawdopodobieństwo", "Ważność", "Środek ograniczający ryzyko",
        "Pewność oceny", "Wyzwalacz", "Mechanizmy kontrolne",
        "Ryzyko rezydualne", "Status", "Właściciel", "Zamknięcie",
    },
    "TDR": {
        "Dług", "Pozycja", "Kategoria", "Źródło", "Koszt", "Zwłoka",
        "Status", "Opis",
    },
    "REC": {
        "Identyfikator zalecenia", "Priorytet", "Ustalenie",
        "Zalecenie", "Opis", "Wpływ", "Koszt", "Wysiłek", "Złożoność",
        "Weryfikacja", "Łamanie", "Zależy od", "Właściciel",
        "Warunek końcowy", "Rozważane alternatywy",
        "Pewność oceny nakładu", "Ryzyko rezydualne",
        "Kamień milowy akceptacji", "Dowód zamknięcia",
    },
}

# Genitive/paucal/singular forms a Polish count statement can take for
# each register. `ryzyk` bare is the genitive plural of `ryzyko`.
COUNT_NOUNS = {
    "ustalenie": "FND",
    "ustalenia": "FND",
    "ustaleń": "FND",
    "ryzyko": "RSK",
    "ryzyka": "RSK",
    "ryzyk": "RSK",
    "ryzyków": "RSK",
    "zalecenie": "REC",
    "zalecenia": "REC",
    "zaleceń": "REC",
    "rekomendacje": "REC",
    "rekomendacji": "REC",
    "dowód": "EVD",
    "dowody": "EVD",
    "dowodów": "EVD",
}
COUNT_CLAIM = re.compile(
    r"\b(\d+)\s+(" + "|".join(sorted(COUNT_NOUNS, key=len, reverse=True)) + r")\b",
    re.IGNORECASE,
)

WORD = re.compile(r"\w+")


def reconfigure_stdio():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="backslashreplace")
        except Exception:
            pass


def normalize(text):
    """Strip link/code/emphasis markup and fold case + whitespace so a
    table cell and a heading title compare equal."""
    text = LINK.sub(r"\1", text)
    text = text.replace("`", "").replace("*", "")
    return " ".join(text.split()).casefold().rstrip(".")


def fenced_mask(lines):
    """Line numbers that sit inside fenced code blocks."""
    inside = False
    masked = set()
    for index, line in enumerate(lines):
        if line.strip().startswith("```"):
            inside = not inside
            masked.add(index)
            continue
        if inside:
            masked.add(index)
    return masked


def check_summary_titles(lines):
    """Every `### ID: title` block must have a register row whose cells
    include the same title after markup stripping."""
    failures = []
    rows = {}
    for index, line in enumerate(lines):
        match = ROW_ID.match(line)
        if match:
            cells = [cell.strip() for cell in line.split("|")[1:-1]]
            rows.setdefault(match.group(1), []).append(
                (index, [normalize(cell) for cell in cells])
            )
    for index, line in enumerate(lines):
        match = ID_HEADING.match(line)
        if not match:
            continue
        ident, title = match.group(1), match.group(2)
        candidates = rows.get(ident)
        if not candidates:
            failures.append(
                (index, f"{ident}: no register/summary row carries this block")
            )
            continue
        wanted = normalize(title)
        if any(wanted in cells for _row_index, cells in candidates):
            continue
        row_index, _cells = candidates[0]
        failures.append(
            (
                index,
                f"{ident}: block title '{title[:60]}' appears in no cell "
                f"of its summary row (line {row_index + 1})",
            )
        )
    return failures


def check_prose_counts(lines, masked):
    """`N <register noun>` in prose must equal the real register count."""
    actual = {
        family: sum(
            1
            for line in lines
            if re.match(rf"^###\s+{family}-", line)
        )
        for family in ("FND", "RSK", "REC")
    }
    actual["EVD"] = sum(1 for line in lines if re.match(r"^\|\s*\[?EVD-", line))
    failures = []
    for index, line in enumerate(lines):
        if index in masked or line.startswith(("|", "#", ">")):
            continue
        for match in COUNT_CLAIM.finditer(line):
            claimed = int(match.group(1))
            family = COUNT_NOUNS[match.group(2).lower()]
            real = actual.get(family)
            if real is not None and claimed != real:
                failures.append(
                    (
                        index,
                        f"prose claims {claimed} {family} item(s) "
                        f"('{match.group(2)}') but the register holds {real}",
                    )
                )
    return failures


def check_block_labels(lines):
    """`* **Label:**` fields inside register detail blocks must belong
    to that register's contract label set. A label from another
    register's table - `Skutek` under `### FND-…`, `Wpływ` under
    `### TDR-…` - survives mapping unmapped and drops the required
    English field."""
    failures = []
    current = None
    for index, line in enumerate(lines):
        heading = ID_HEADING.match(line)
        if heading:
            current = heading.group(1).split("-", 1)[0]
            continue
        if re.match(r"^#{1,3}\s", line):
            current = None
            continue
        if current is None:
            continue
        field = BLOCK_FIELD.match(line)
        if field:
            label = field.group(1).strip()
            if label not in BLOCK_LABELS[current]:
                failures.append(
                    (
                        index,
                        f"{current} block uses field label '{label}' "
                        f"outside its contract set",
                    )
                )
    return failures


def heading_slug(text):
    """GitHub-style slug: lowercase, drop punctuation except hyphens,
    spaces become hyphens, diacritics stay."""
    return re.sub(r"[^\w -]", "", text.casefold()).replace(" ", "-")


def check_internal_anchors(lines, masked):
    """Every `](#anchor)` target must resolve to a heading slug, with
    duplicate headings numbered `-1`, `-2` the way renderers disambiguate
    them. A translated heading renamed after links were written orphans
    every link the mapper then rewrites to itself."""
    seen = {}
    slugs = set()
    for line in lines:
        heading = HEADING.match(line)
        if not heading:
            continue
        base = heading_slug(heading.group(1))
        count = seen.get(base, 0)
        seen[base] = count + 1
        slugs.add(base if count == 0 else f"{base}-{count}")
    failures = []
    reported = set()
    for index, line in enumerate(lines):
        if index in masked:
            continue
        for match in INTERNAL_LINK.finditer(line):
            target = match.group(1)
            if target not in slugs and (index, target) not in reported:
                reported.add((index, target))
                failures.append(
                    (index, f"internal link `#{target}` resolves to no heading")
                )
    return failures


def check_sentence_length(lines, masked, max_words):
    """Warn on prose sentences over `max_words` words, outside tables,
    headings, and fenced code."""
    warnings = []
    paragraph = []
    paragraph_start = 0

    def flush():
        text = " ".join(paragraph).strip()
        if not text:
            return
        start = 0
        for match in re.finditer(r"[.!?]+(?:\s+|$)", text):
            sentence = text[start : match.start()].strip()
            if sentence:
                count = len(WORD.findall(sentence))
                if count > max_words:
                    warnings.append(
                        (
                            paragraph_start,
                            f"sentence runs {count} words (limit {max_words}): "
                            f"'{sentence[:60]}...'",
                        )
                    )
            start = match.end()
        count = len(WORD.findall(text[start:]))
        if count > max_words:
            warnings.append(
                (
                    paragraph_start,
                    f"sentence runs {count} words (limit {max_words}): "
                    f"'{text[start:start + 60]}...'",
                )
            )

    for index, line in enumerate(lines):
        if index in masked or not line.strip():
            flush()
            paragraph = []
            continue
        if line.startswith(("|", "#", "- ", "* ", ">", "```")):
            flush()
            paragraph = []
            continue
        if not paragraph:
            paragraph_start = index + 1
        paragraph.append(line.strip())
    flush()
    return warnings


def main():
    reconfigure_stdio()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument(
        "--max-words",
        type=int,
        default=40,
        help="warn when a prose sentence exceeds this many words (default 40)",
    )
    args = parser.parse_args()

    lines = args.file.read_text(encoding="utf-8").split("\n")
    masked = fenced_mask(lines)

    failures = (
        check_summary_titles(lines)
        + check_prose_counts(lines, masked)
        + check_block_labels(lines)
        + check_internal_anchors(lines, masked)
    )
    warnings = check_sentence_length(lines, masked, args.max_words)

    for index, message in sorted(failures + warnings):
        level = "FAIL" if (index, message) in failures else "WARN"
        print(f"{level} line {index + 1}: {message}")
    print(
        "%d failure(s), %d warning(s)"
        % (len(failures), len(warnings))
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
