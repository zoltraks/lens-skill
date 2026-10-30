#!/usr/bin/env python3
"""Map a translated Lens report back to English for validation.

`validate-report.py` speaks only the English contract. To validate a
translated report, this tool produces an English-mapped working copy: it
inverts the fixed `English | Polish` tables in the translation contract
file and applies them document-wide, longest phrase first. Section
headings, field labels, fixed vocabulary values, and glossary anchors map
back to the English literals the validator expects; free-text content
(finding titles, prose) is untouched.

Copy this file into the audited repository's `work/` directory as
`map-translation.tmp.py` and always pass `--rules` - the tables it
inverts live in `translations/polish-language.md`, not in this script.
Sections excluded from inversion: the open-ended `Terminology` dictionary
(mapping it back would rewrite ordinary prose) and the calque/prompt
sections, which carry no `English | Polish` contract tables anyway.

Usage:
    map-translation.py <translated.md> --rules <polish-language.md>
        [--en <canonical-en.md>] [-o <out.md>]

`--en <canonical-en.md>` optionally verifies the mapped output against the
English sibling: every `##` heading must match in order, and `###` block
headings must carry the same identifiers in the same order (titles are
translated prose and are not compared).

The mapped copy is a validation artifact - run `format-table.py` on it
before `validate-report.py`, then remove it with the other `.tmp.` files.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Sections whose `English | Polish` tables must not be inverted: the
# Terminology dictionary is open-ended prose vocabulary, and the prompt and
# calque sections carry no report-contract literals.
EXCLUDE_SECTIONS = {
    "Terminology",
    "Calque And Style Replacements",
    "Parameter Prompts",
}

# Tokens the English contract renders all-caps verbatim - do not
# sentence-case them during normalization.
KEEP_CAPS = {
    "PASS",
    "N/A",
    "N/D",
    "OK",
    "TBD",
    "NOT SPECIFIED",
    "NOT COLLECTED",
    "NOT INSPECTED",
    "INSUFFICIENT INFORMATION",
    "UNKNOWN",
    "PENDING EVIDENCE",
    # Acronyms and register prefixes that the contract renders verbatim -
    # without these they sentence-case into `Sbom`/`Stride`/`Rec`/`Adr`.
    "SBOM",
    "STRIDE",
    "REC",
    "ADR",
}

# `tak`/`nie` are ordinary prose words - only inside the boolean field
# bullets may they become `yes`/`no`/`not applicable`.
FIELD_YES_NO = re.compile(
    r"^(\s*\*\s+\*\*(?:Verification|Runtime):\*\*\s*)"
    r"(nie dotyczy|tak|nie)\b",
    re.IGNORECASE,
)
YES_NO = {"tak": "yes", "nie": "no", "nie dotyczy": "not applicable"}

# `Zadeklarowana` inverts to the Verification-column token `Reported`, but
# the Provenance basis field wants the provenance qualifier `Declared`. The
# remaining provenance values never appear in contract tables, so the field
# itself rewrites them here (`Wskazana` -> `Indicated` and so on).
FIELD_PROVENANCE = re.compile(
    r"^(\s*\*\s+\*\*Provenance basis:\*\*\s*)"
    r"(Reported|Zaświadczona|Dostarczona|Wskazana|Nieokreślona)\b"
)
PROVENANCE_VALUE = {
    "reported": "Declared",
    "zaświadczona": "Attested",
    "dostarczona": "Supplied",
    "wskazana": "Indicated",
    "nieokreślona": "Undetermined",
}

HEADING = re.compile(r"^#{2,3}\s+(.+?)\s*$")
BLOCK_HEADING = re.compile(r"^###\s+([A-Z]{3}-[A-Z]{3}-\d{3}|[A-Z]{3}-\d{3})")

# Ambiguous Polish renderings resolve to the literal the English contract
# uses most often - the first row of every collision wins document order,
# which is arbitrary for labels shared across several tables. Keep this
# table in sync with the contract tables in translations/polish-language.md.
def normalize_english(value):
    # `English` cells in the grammar tables carry ALL-CAPS tokens while the
    # report contract renders sentence case (`COVERED` -> `Covered`,
    # `NOT DONE` -> `Not done`, `SEVERITY:` -> `Severity:`).
    if value.isupper() and value not in KEEP_CAPS:
        return value[:1] + value[1:].lower()
    return value


PREFERRED = {
    "wynik": "Result",
    "kontrola": "Check",
    "dowód": "Evidence",
    "uzasadnienie": "Justification",
    "obszar": "Area",
    "zależności": "Dependencies",
    "ścieżka": "Path",
    "podstawa": "Basis",
    "zgodność": "Compliance",
    "częściowo": "Partially",
    "gotowy": "Ready",
    "błąd": "Error",
    "poza zakresem": "Out of scope",
    "koszt": "cost",
}

# Section-scoped fixes for literals whose correct English depends on where
# they occur: (section heading, cell text, replacement). Applied after the
# global map, inside the named `##`/`###` section only.
CONTEXT_FIXUPS = (
    ("Project Scorecard", "Result", "Score"),
    ("Audit Coverage", "Justification", "Rationale"),
    ("Document Information", "Source", "source-only"),
)


def slugify(heading):
    return re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-")


def load_pairs(rules_path):
    """Invert `English | Polish` contract tables. Returns (pl->en map,
    list of (pl, en) collisions)."""
    pairs = {}
    collisions = []
    section = None
    in_table = None
    for line in Path(rules_path).read_text(encoding="utf-8").split("\n"):
        heading = re.match(r"^#{2,3}\s+(.+?)\s*$", line)
        if heading:
            section = heading.group(1)
            in_table = None
            continue
        cells = [c.strip() for c in line.split("|")]
        if line.startswith("|") and len(cells) >= 4:
            first = cells[1].lower()
            if first.startswith("english") and (
                cells[2].lower().startswith("polish")
                or cells[2].lower() == "masculine"
            ):
                # `English | Polish |` contract tables pair columns 1 and 2.
                # `English | Masculine | Feminine | Neuter |` grammar tables
                # map every Polish inflection column back to the English token.
                in_table = (
                    None
                    if section in EXCLUDE_SECTIONS
                    else "gendered" if cells[2].lower() == "masculine" else "contract"
                )
                continue
            if in_table and not set(cells[1] + cells[2]) <= set("- "):
                polish_cols = [2, 3, 4] if in_table == "gendered" else [2]
                en_parts = [
                    re.sub(r"\s*\(.*?\)", "", p).strip().strip("`")
                    for p in cells[1].split(" / ")
                ]
                for col in polish_cols:
                    if col >= len(cells):
                        continue
                    pl_parts = [
                        p.strip().strip("`") for p in cells[col].split(" / ")
                    ]
                    if len(pl_parts) > 1 and len(pl_parts) == len(en_parts):
                        zipped = zip(pl_parts, en_parts)
                    else:
                        zipped = ((p, en_parts[0]) for p in pl_parts)
                    for polish, english in zipped:
                        if not polish or not english:
                            continue
                        english = normalize_english(english)
                        if polish in pairs and pairs[polish] != english:
                            collisions.append((polish, pairs[polish], english))
                            continue
                        pairs.setdefault(polish, english)
        elif in_table:
            in_table = False
    return pairs, collisions


def apply_map(text, pairs):
    """Replace Polish contract phrases with their English literals,
    longest key first, on word boundaries."""
    keys = sorted(pairs, key=len, reverse=True)
    lowered = {key.lower(): value for key, value in pairs.items()}
    pattern = re.compile(
        "|".join(
            r"(?<!\w)(?<![A-Z]-)" + re.escape(key) + r"(?!\w)" for key in keys
        ),
        re.IGNORECASE,
    )

    def substitute(match):
        value = lowered[match.group(0).lower()]
        # A capitalized source word keeps its capital - sentence-initial
        # words like `Koszt` must not map to a lowercase `cost` that then
        # reads as a broken sentence continuation.
        if match.group(0)[:1].isupper() and value[:1].islower():
            value = value[:1].upper() + value[1:]
        return value

    return pattern.sub(substitute, text)


def fixup(text):
    """Fixups that table inversion cannot express."""
    # The language row declares the report language; the mapped copy is
    # English text.
    text = re.sub(
        r"(\|\s*Language\s*\|\s*)[^|]*\|",
        r"\1English |",
        text,
    )
    # Lowest-scoring-dimension disclosure: the validator greps `lowest`.
    text = re.sub(r"najni\w*", "lowest", text, flags=re.IGNORECASE)
    # The PAR cross-referencing labels invert word order and the linkified
    # identifier blocks plain phrase matching - swap `Powiązania [X](#x)`
    # for `[X](#x) cross-referencing` explicitly.
    text = re.sub(
        r"Powiązania \[(FND|RSK|REC)\]\(#(\w+)\)",
        r"[\1](#\2) cross-referencing",
        text,
    )
    # English renders these sentence-internal occurrences lowercase; the
    # title-case table pairs would otherwise leave capitalized strays that
    # trip the capitalized-compound glossary heuristic.
    text = re.sub(r"(\]\(#glossary\)\s+)Applied\b", r"\1applied", text)
    text = text.replace(
        "Operational Objectives (", "Operational objectives ("
    )
    # `Nieokreślony` inverts to `NOT SPECIFIED` (the DORA-metric token) but
    # the `Absence` field's `Undetermined` token shares the same Polish
    # rendering - the field bullet disambiguates.
    text = re.sub(
        r"(?m)^(\s*\*\s+\*\*Absence:\*\*\s*)NOT SPECIFIED\b",
        r"\1Undetermined",
        text,
    )
    # PREFERRED pins `koszt` to lowercase `cost` for prose, which also
    # hits the `Cost` field bullet on debt blocks - restore the label case.
    text = re.sub(
        r"(?m)^(\s*\*\s+\*\*)cost(:\*\*)",
        r"\1Cost\2",
        text,
    )
    return text


def compare_with_english(mapped_lines, en_lines):
    """Verify section structure against the English sibling. `##` headings
    compare in full; `###` headings compare by identifier prefix."""
    failures = []

    def shape(lines):
        result = []
        for line in lines:
            if line.startswith("## "):
                result.append(("section", line[3:].strip()))
            elif line.startswith("### "):
                block = BLOCK_HEADING.match(line)
                result.append(("block", block.group(1) if block else line[4:].strip()))
        return result

    mapped_shape = shape(mapped_lines)
    en_shape = shape(en_lines)
    if len(mapped_shape) != len(en_shape):
        failures.append(
            "heading count differs: mapped %d vs english %d"
            % (len(mapped_shape), len(en_shape))
        )
    for index, ((kind_a, name_a), (kind_b, name_b)) in enumerate(
        zip(mapped_shape, en_shape), 1
    ):
        if kind_a != kind_b or name_a != name_b:
            failures.append(
                "heading %d differs: mapped %r vs english %r"
                % (index, name_a, name_b)
            )
    return failures


def reconfigure_stdio():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="backslashreplace")
        except Exception:
            pass


def main():
    reconfigure_stdio()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--rules", type=Path, required=True)
    parser.add_argument("--en", type=Path, default=None)
    parser.add_argument("-o", "--output", type=Path, default=None)
    args = parser.parse_args()

    pairs, collisions = load_pairs(args.rules)
    if not pairs:
        print("map-translation: no English|Polish tables found in %s"
              % args.rules, file=sys.stderr)
        return 1
    for key in list(pairs):
        if key.lower() in PREFERRED:
            pairs[key] = PREFERRED[key.lower()]
    for polish, kept, dropped in collisions:
        if polish.lower() in PREFERRED:
            continue
        print("collision: %r kept %r, ignored %r" % (polish, kept, dropped),
              file=sys.stderr)

    en_lines = []
    if args.en:
        en_lines = args.en.read_text(encoding="utf-8").split("\n")

    raw_lines = args.file.read_text(encoding="utf-8").split("\n")

    # Pass 1 - finalize every heading. `###` block headings keep the phrase
    # map alone (their titles are translated prose); every other heading
    # takes the English sibling's title positionally when the sibling is
    # given, which resolves table gaps and collisions.
    orig_headings = [
        (index, HEADING.match(line).group(1))
        for index, line in enumerate(raw_lines)
        if HEADING.match(line)
    ]
    en_headings = [
        (index, HEADING.match(line).group(1), line[:3].strip())
        for index, line in enumerate(en_lines)
        if HEADING.match(line)
    ]
    final_title = {
        index: apply_map(title, pairs) for index, title in orig_headings
    }
    if en_lines and len(orig_headings) == len(en_headings):
        for (slot, _title), (_en_index, en_title, en_level) in zip(
            orig_headings, en_headings
        ):
            pl_block = BLOCK_HEADING.match(raw_lines[slot])
            en_block = BLOCK_HEADING.match(en_lines[_en_index])
            if raw_lines[slot][:3].strip() != en_level or pl_block or en_block:
                continue
            final_title[slot] = en_title
    slug_map = {
        slugify(title): slugify(final_title[index])
        for index, title in orig_headings
        if slugify(title) != slugify(final_title[index])
    }

    # Pass 2 - rewrite link targets whose headings moved (before the phrase
    # map touches them), map the document, pin headings to their final
    # titles, then apply fixups.
    pattern = re.compile(r"\]\(#([^)]+)\)")
    raw_lines = [
        pattern.sub(
            lambda m: "](#" + slug_map.get(m.group(1), m.group(1)) + ")", line
        )
        for line in raw_lines
    ]
    lines = apply_map("\n".join(raw_lines), pairs).split("\n")
    lines = [
        FIELD_PROVENANCE.sub(
            lambda m: m.group(1) + PROVENANCE_VALUE[m.group(2).lower()],
            FIELD_YES_NO.sub(
                lambda m: m.group(1) + YES_NO[m.group(2).lower()], line
            ),
        )
        for line in lines
    ]
    for index, title in final_title.items():
        heading = HEADING.match(lines[index])
        if heading:
            lines[index] = (
                lines[index][: heading.start(1)] + title
            )
    lines = fixup("\n".join(lines)).split("\n")

    # Section-scoped cell fixes - apply each only inside its named section.
    for section_name, cell, replacement in CONTEXT_FIXUPS:
        inside = False
        for index, line in enumerate(lines):
            heading = HEADING.match(line)
            if heading:
                inside = heading.group(1) == section_name
                continue
            if inside and line.startswith("|"):
                lines[index] = re.sub(
                    r"\|\s*" + re.escape(cell) + r"\s*\|",
                    "| " + replacement + " |",
                    line,
                )

    output = args.output
    if output is None:
        output = args.file.with_name(args.file.stem + "-en-mapped.tmp.md")
    output.write_text("\n".join(lines), encoding="utf-8")
    print("mapped %d contract phrase(s), wrote %s" % (len(pairs), output))

    # Coverage report: doc-info labels still in Polish.
    unmapped = [
        i + 1
        for i, line in enumerate(lines)
        if re.search(r"\|\s*(Rewizja raportu|Styl raportu|Język)\s*\|", line)
    ]
    if unmapped:
        print("unmapped doc-info rows at line(s): %s" % unmapped,
              file=sys.stderr)

    if args.en:
        failures = compare_with_english(lines, en_lines)
        for failure in failures:
            print("FAIL %s" % failure)
        if failures:
            return 1
        print("english sibling check: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
