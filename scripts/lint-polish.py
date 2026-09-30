#!/usr/bin/env python3
"""Lint Polish Markdown prose for calques, spliced clauses, and typography.

Reads the `Calque And Style Replacements` table ("Instead of / Use") from
translations/polish-language.md and reports each forbidden form in the target
document. Also runs heuristic checks: comma splices, "tylko, gdy", bare "per",
typographic characters under the ASCII convention, and "w." as an abbreviation.

Errors exit non-zero; warnings are advisory and never fail the run.

Usage:
    lint-polish.py <file.md> [--rules <rulefile.md> ...]

When --rules is omitted, translations/polish-language.md is loaded relative to
this script. Polish audit reports must pass with zero errors before delivery,
and the Validation Record records the run.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TABLE_HEADERS = {"zamiast", "instead of", "forbidden"}

# Single common Polish words that are calques only in context - demoted to
# warnings so the check stays a usable gate.
SOFT_STEMS = {
    "pod", "plus", "wskaźnik", "niesie", "niosą", "dotyka", "zyskuje",
    "właściciel", "mieszkają", "żyje", "lustro", "ładunek", "rekord",
    "chudy", "najcięższy", "najlżejszy", "autorytatywny", "wydawniczy",
    "wykonawcz", "powierzchnia", "konsumowana", "zaadresować", "kosztuje",
    "przypięty", "celują", "rekursują", "serwujący", "strażnik", "zastany",
    "brama", "bramka", "bramy", "realna", "realne", "diff", "wyjątek",
    "to jest", "skonsultowano", "rozdzielczy",
}

# Words that legitimately follow a comma (conjunctions, relatives,
# prepositions, common adverbs, abbreviations).
COMMA_OK = {
    "i", "oraz", "a", "ale", "jednak", "lub", "albo", "ani", "czy", "czyli",
    "tj.", "tzn.", "np.", "itp.", "itd.", "m.in.", "w", "we", "z", "ze", "na",
    "do", "o", "po", "przy", "dla", "od", "przez", "za", "pod", "nad", "przed",
    "bez", "między", "według", "wg", "ku", "u", "jak", "że", "żeby", "aby",
    "by", "co", "który", "która", "które", "którzy", "których", "której",
    "któremu", "którym", "gdzie", "gdy", "kiedy", "jeśli", "jeżeli", "chociaż",
    "choć", "bo", "ponieważ", "gdyż", "więc", "natomiast", "nawet", "to",
    "mimo", "poza", "wraz", "dzięki", "zamiast", "oprócz", "wskutek", "innymi",
    "inaczej", "zwłaszcza", "szczególnie", "tylko", "także", "również",
    "wreszcie", "potem", "najpierw", "następnie", "wówczas", "wtedy", "zanim",
    "dopóki", "skoro", "bądź", "nie", "tak", "tedy", "zatem", "toteż",
    "lecz", "czego", "czym", "kim", "podczas", "jako", "ponadto", "wobec",
    "nigdy", "zawsze", "stąd", "wszędzie", "gdziekolwiek", "gdyby",
}

TYPOGRAPHIC = {
    "„": "typographic open quote", "”": "typographic close quote",
    "“": "typographic open quote", "’": "typographic apostrophe",
    "‘": "typographic apostrophe", "–": "półpauza", "—": "pauza",
    "…": "ellipsis character", "→": "arrow character",
    "«": "guillemet", "»": "guillemet",
}


def reconfigure_stdio():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="backslashreplace")
        except Exception:
            pass


def strip_code(line):
    """Remove inline code spans from a line."""
    return re.sub(r"`[^`]*`", "", line)


def iter_prose_lines(path):
    """Yield (lineno, text) for lines outside fenced code blocks."""
    in_fence = False
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        stripped = raw.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        yield lineno, strip_code(raw)


def stem(word):
    """Reduce an infinitive or inflected form to a matchable stem."""
    for ending in ("ować", "iwać", "ać", "eć", "ić", "yć"):
        if word.endswith(ending) and len(word) - len(ending) >= 3:
            return word[: -len(ending)]
    return word


def load_forbidden(rules_paths):
    """Parse forbidden-form tables. Returns [(forbidden, replacement)]."""
    pairs = []
    seen = set()
    for rules in rules_paths:
        if not rules.exists():
            continue
        in_table = False
        for line in rules.read_text(encoding="utf-8").split("\n"):
            cells = [c.strip() for c in line.split("|")]
            if line.startswith("|") and len(cells) >= 4:
                first = cells[1].strip("`").lower()
                if first in TABLE_HEADERS:
                    in_table = True
                    continue
                if in_table:
                    if set(cells[1] + cells[2]) <= set("- "):
                        continue
                    bad = re.sub(r"\(.*?\)", "", cells[1]).strip()
                    good = re.sub(r"\(.*?\)", "", cells[2]).strip()
                    if bad:
                        for form in bad.split(" / "):
                            form = form.strip().strip("`")
                            if form and form.lower() not in seen:
                                seen.add(form.lower())
                                pairs.append((form, good))
            elif in_table:
                in_table = False
    return pairs


def word_is_soft(forbidden):
    base = forbidden.split("(")[0].strip().lower()
    return base in SOFT_STEMS or stem(base) in SOFT_STEMS


def check_forbidden(lineno, text, pairs, findings):
    lowered = text.lower()
    for forbidden, replacement in pairs:
        if " " in forbidden:
            pattern = re.compile(r"\b" + re.escape(forbidden.lower()) + r"\w*")
        else:
            root = stem(forbidden.lower())
            if len(root) <= 3:
                pattern = re.compile(r"\b" + re.escape(root) + r"\b")
            else:
                pattern = re.compile(r"\b" + re.escape(root) + r"\w*")
        for match in pattern.finditer(lowered):
            severity = "warn" if word_is_soft(forbidden) else "error"
            findings.append(
                (severity, lineno,
                 "calque '%s' - use '%s'" % (match.group(0), replacement))
            )


def check_mechanical(lineno, text, findings, splice=True):
    if "tylko, gdy" in text.lower():
        findings.append(("error", lineno, "'tylko, gdy' - write 'tylko wtedy, gdy'"))
    if re.search(r"\bper\s+\w", text):
        findings.append(("error", lineno, "'per X' - write 'dla każdego X'"))
    if re.search(r"\bw\.\s*\d", text):
        findings.append(("warn", lineno, "'w.' - do not abbreviate 'wierszy'"))
    if re.search(r"~\s*\d", text):
        findings.append(("warn", lineno, "'~N' - write 'ok. N' or 'około N'"))
    if re.search(r"\bNiej\b", text):
        findings.append(("warn", lineno, "'Niej' - possible misspelling of a negated adjective"))
    if re.search(r"\bparitet\b", text.lower()):
        findings.append(("error", lineno, "'paritet' - misspelling of 'parytet'"))
    for char, name in TYPOGRAPHIC.items():
        if char in text:
            findings.append(("error", lineno, "typographic %s %r" % (name, char)))
    if ";" in text:
        findings.append(("error", lineno, "semicolon in prose"))

    # Comma-splice heuristic: a comma followed by a word that opens neither a
    # subordinate clause nor a prepositional phrase. Tables and list items are
    # skipped - their commas are usually enumerations.
    if not splice:
        return
    for match in re.finditer(r",\s+(\w+)", text.lower()):
        word = match.group(1)
        if word not in COMMA_OK and not word[0].isdigit():
            findings.append(
                ("warn", lineno,
                 "possible spliced clause - ', %s' does not open a "
                 "subordinate phrase" % word)
            )


def main():
    reconfigure_stdio()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--rules", type=Path, action="append", default=[])
    args = parser.parse_args()

    rules = args.rules
    if not rules:
        root = Path(__file__).resolve().parent.parent
        rules = [root / "translations" / "polish-language.md"]
    pairs = load_forbidden(rules)

    findings = []
    for lineno, text in iter_prose_lines(args.file):
        stripped = text.strip()
        if stripped.startswith("<!--"):
            continue
        is_table = stripped.startswith("|")
        is_list = bool(re.match(r"^[-*+]\s|^\d+\.\s|^\s+[-*+]\s", text))
        check_forbidden(lineno, text, pairs, findings)
        check_mechanical(lineno, text, findings,
                         splice=not (is_table or is_list))

    errors = sum(1 for f in findings if f[0] == "error")
    for severity, lineno, message in findings:
        print("%s:%d: [%s] %s" % (args.file, lineno, severity.upper(), message))
    print("lint-polish: %d error(s), %d warning(s), %d forbidden forms loaded"
          % (errors, len(findings) - errors, len(pairs)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
