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
* Every heading must come from a translation table row - a heading kept
  verbatim in English (for example `## Threat Model`) fails - unless the
  file is the translation sibling of a language pair and the heading
  matches its English sibling verbatim: the pair-skeleton convention
  keeps headings and field labels English so `](#anchor)` targets stay
  stable. The sibling resolves from `--en`, or from a `<stem>-EN.md`
  file beside a `<stem>-<LANG>` report.
* `* **Label:**` field values start uppercase, and a governed vocabulary
  token inside a code span is translated like the unspanned form
  (`Teoretyczne`, never `Theoretical`).
* `TDD` never appears - the contract spells out `due diligence
  techniczne` in full.
* Prose sentences outside tables stay within a word limit - long chained
  sentences are a known translation defect class. Warn-level only.

Spell checking stays external (a real dictionary), per the polish-language
contract - this tool checks only mechanical agreement.

Copy this file into the audited repository's `work/` directory as
`check-translation.tmp.py` before running it against a report there.

Usage:
    check-translation.py <translated.md> [--max-words N] [--rules <rulefile.md> ...]

When --rules is omitted, translations/polish-language.md is loaded relative to
this script; the heading check is skipped only when no rules file resolves.
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
        "Kryterium", "Charakter odstępstwa", "Wpływ",
        "Zalecenie", "Metoda", "Zweryfikowane",
        "Uruchomienie", "Łamanie kompatybilności",
        "Dotyczy", "Pewność oceny", "Czynniki łagodzące",
        "Wykorzystanie podatności", "Dowód", "Podstawa pochodzenia",
    },
    "RSK": {
        "Ryzyko", "Źródło", "Wpływ", "Zakres",
        "Prawdopodobieństwo", "Ważność", "Środek ograniczający ryzyko",
        "Pewność oceny", "Wyzwalacz", "Mechanizmy kontrolne",
        "Ryzyko rezydualne", "Status", "Właściciel", "Zamknięcie",
    },
    "TDR": {
        "Dług", "Pozycja", "Kategoria", "Źródło", "Koszt", "Zwłoka",
        "Status",
    },
    "REC": {
        "Identyfikator zalecenia", "Priorytet", "Ustalenie",
        "Zalecenie", "Wpływ", "Koszt", "Wysiłek", "Złożoność",
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

# Governed English vocabulary tokens (status, severity, confidence, maturity,
# verdict words) that must be translated even when written inside a code span.
# Kept as a curated set rather than every first-column cell of the rules
# tables so generic vocabulary (`Boundary`, `Control`) cannot collide with
# subject identifiers quoted verbatim.
GOVERNED_TOKENS = {
    "theoretical", "confirmed", "verified", "reported", "open", "closed",
    "reopened", "accepted", "mitigated", "covered", "partially", "unchanged",
    "low", "medium", "high", "critical", "planned", "deferred", "unresolved",
    "recommended", "optional", "deliberate", "undetermined", "indicated",
    "declared", "attested", "supplied", "inspected", "inferred",
    "early development", "pre-production", "production-ready", "prototype",
    "red", "amber", "green", "unknown", "stale", "resolved", "outstanding",
    "complete", "partial", "not met", "not assessable", "not ready",
    "conditionally ready", "not assessed", "not done", "not run",
}

# Subset of governed tokens that never name subject identifiers, so a code
# span holding one is a missed translation wherever it appears - not only in
# `* **Label:**` field values.
GOVERNED_ANYWHERE = {
    "theoretical", "undetermined", "deliberate", "early development",
    "pre-production", "production-ready", "conditionally ready",
    "not assessable", "not assessed", "not run",
}


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


def check_block_labels(lines, extra_labels=None):
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
            if label not in BLOCK_LABELS[current] and not (
                extra_labels and label.casefold() in extra_labels
            ):
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


def load_english_keys(rules_paths):
    """First-column cells of `English | Polish` tables whose Polish form
    differs - the set of headings and labels a Polish report must not keep
    verbatim. Self-mapping rows (`STRIDE` -> `STRIDE`) are excluded so a
    legitimately untranslated heading does not flag."""
    keys = {}
    for rules in rules_paths:
        if not rules.exists():
            continue
        in_table = False
        for line in rules.read_text(encoding="utf-8").split("\n"):
            if not line.startswith("|"):
                in_table = False
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if not cells or set("".join(cells)) <= set("-: "):
                continue
            if not in_table:
                in_table = cells[0].casefold() == "english"
                continue
            if len(cells) >= 2 and cells[0].casefold() != cells[1].casefold():
                keys[cells[0].casefold()] = cells[1]
    return keys


def check_untranslated_headings(lines, masked, keys, en_headings=None):
    """A `##`/`###` heading kept verbatim in English breaks PAR-16 - the
    Polish form is the rules-file mapping for that heading - unless the
    pair-skeleton convention applies and the heading matches its English
    sibling verbatim."""
    failures = []
    for index, line in enumerate(lines):
        if index in masked:
            continue
        match = HEADING.match(line)
        if not match:
            continue
        norm = normalize(match.group(1))
        if norm in keys and not (en_headings and norm in en_headings):
            failures.append(
                (
                    index,
                    f"heading stays English: '{match.group(1)}' - "
                    f"expected '{keys[norm]}'",
                )
            )
    return failures


def check_field_values(lines, masked):
    """`* **Label:**` field values start uppercase per the style rules, and
    a code span holding a governed English token (`Theoretical`, `Open`,
    `Critical`) keeps it untranslated through the mapping - both defects
    leave the Polish contract unmet."""
    failures = []
    for index, line in enumerate(lines):
        if index in masked:
            continue
        match = BLOCK_FIELD.match(line)
        if not match:
            continue
        value = line[match.end() :].strip()
        if not value:
            continue
        for span in re.findall(r"`([^`]*)`", value):
            token = span.strip().casefold()
            if token in GOVERNED_TOKENS and token not in GOVERNED_ANYWHERE:
                failures.append(
                    (
                        index,
                        f"governed token `{span.strip()}` stays English inside a "
                        "code span - translate it like the unspanned form",
                    )
                )
        first = value[:1]
        if first.islower():
            failures.append(
                (
                    index,
                    f"field value starts lowercase: '{value[:50]}'",
                )
            )
    for index, line in enumerate(lines):
        if index in masked:
            continue
        for span in re.findall(r"`([^`]*)`", line):
            if span.strip().casefold() in GOVERNED_ANYWHERE:
                failures.append(
                    (
                        index,
                        f"governed token `{span.strip()}` stays English inside a "
                        "code span - translate it like the unspanned form",
                    )
                )
    return failures


def check_tdd_token(lines, masked):
    """`TDD` is never sanctioned in a Polish report - `due diligence
    techniczne` and `test-driven development` are both spelled out."""
    failures = []
    for index, line in enumerate(lines):
        if index in masked:
            continue
        plain = re.sub(r"`[^`]*`", "", line)
        # The Słownik term cell records the acronym being defined - the ban
        # covers its use as an abbreviation elsewhere.
        if line.startswith("|"):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            plain = " | ".join(cells[1:]) if len(cells) > 1 else ""
        if re.search(r"\bTDD\b", plain):
            failures.append(
                (
                    index,
                    "ambiguous TDD token - spell out 'due diligence techniczne' "
                    "or 'test-driven development' in full",
                )
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


def english_sibling(path, explicit):
    """Resolve the English sibling of a pair-skeleton translation file:
    `--en` when given, else `<stem>-EN.md` beside a `<stem>-<LANG>` file."""
    if explicit:
        return explicit if explicit.exists() else None
    match = re.match(r"^(.*)-[A-Z]{2}$", path.stem)
    if not match:
        return None
    candidate = path.with_name(f"{match.group(1)}-EN{path.suffix}")
    return candidate if candidate.exists() else None


def sibling_surface(en_path):
    """Normalized headings and `* **Label:**` field labels of the English
    sibling. The pair-skeleton convention keeps both verbatim English in
    the translation file, so a match is not a defect."""
    en_lines = en_path.read_text(encoding="utf-8").split("\n")
    en_mask = fenced_mask(en_lines)
    headings, labels = set(), set()
    for index, line in enumerate(en_lines):
        if index in en_mask:
            continue
        heading = HEADING.match(line)
        if heading:
            headings.add(normalize(heading.group(1)))
        label = BLOCK_FIELD.match(line)
        if label:
            labels.add(label.group(1).strip().casefold())
    return headings, labels


def main():
    reconfigure_stdio()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument(
        "--en",
        type=Path,
        default=None,
        help="English sibling of a language pair - headings and field "
        "labels matching it stay English per the pair-skeleton convention "
        "(default: auto-detect a <stem>-EN file beside <stem>-<LANG>)",
    )
    parser.add_argument(
        "--max-words",
        type=int,
        default=40,
        help="warn when a prose sentence exceeds this many words (default 40)",
    )
    parser.add_argument(
        "--rules",
        type=Path,
        action="append",
        default=[],
        help="polish-language rules file(s) for the untranslated-heading check "
        "(default: translations/polish-language.md beside this script)",
    )
    args = parser.parse_args()

    lines = args.file.read_text(encoding="utf-8").split("\n")
    masked = fenced_mask(lines)

    rules = args.rules
    if not rules:
        root = Path(__file__).resolve().parent.parent
        candidate = root / "translations" / "polish-language.md"
        if candidate.exists():
            rules = [candidate]
    keys = load_english_keys(rules)

    sibling = english_sibling(args.file, args.en)
    en_headings, en_labels = (
        sibling_surface(sibling) if sibling else (None, None)
    )

    failures = (
        check_summary_titles(lines)
        + check_prose_counts(lines, masked)
        + check_block_labels(lines, en_labels)
        + check_internal_anchors(lines, masked)
        + check_untranslated_headings(lines, masked, keys, en_headings)
        + check_field_values(lines, masked)
        + check_tdd_token(lines, masked)
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
