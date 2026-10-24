#!/usr/bin/env python3
"""Lint Polish Markdown prose for calques, spliced clauses, and typography.

Reads the `Calque And Style Replacements` table ("Instead of / Use") from
translations/polish-language.md and reports each forbidden form in the target
document. Also runs heuristic checks: comma splices, "tylko, gdy", bare "per",
typographic characters under the ASCII convention, "w." as an abbreviation,
and all-caps renderings of the title-case fixed vocabulary.

Every finding is an error and exits non-zero.

Usage:
    lint-polish.py <file.md> [--rules <rulefile.md> ...]

When --rules is omitted, translations/polish-language.md is loaded relative to
this script. Polish audit reports must pass with zero errors before delivery;
it is a translation-quality gate and earns no row in the Validation Record,
which mirrors the English report row for row.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TABLE_HEADERS = {"zamiast", "instead of", "forbidden"}

# First-column headers of tables listing phrases that are masked out before
# the calque check - sanctioned idioms and canonical English names kept
# verbatim.
ALLOWED_HEADERS = {"allowed phrase", "canonical name"}

# Words that legitimately follow a comma (conjunctions, relatives,
# prepositions, common adverbs, abbreviations).
COMMA_OK = {
    "i", "oraz", "a", "ale", "jednak", "lub", "albo", "ani", "czy", "czyli",
    "tj.", "tzn.", "np.", "itp.", "itd.", "m.in.", "w", "we", "z", "ze", "na",
    "do", "o", "po", "przy", "dla", "od", "przez", "za", "pod", "nad", "przed",
    "bez", "między", "według", "wg", "ku", "u", "jak", "że", "żeby", "aby",
    "by", "co", "który", "która", "które", "którzy", "których", "której",
    "któremu", "którym", "którą", "gdzie", "gdy", "kiedy", "jeśli", "jeżeli",
    "chociaż",
    "choć", "bo", "ponieważ", "gdyż", "więc", "natomiast", "nawet", "to",
    "mimo", "poza", "wraz", "dzięki", "zamiast", "oprócz", "wskutek", "innymi",
    "inaczej", "zwłaszcza", "szczególnie", "tylko", "także", "również",
    "wreszcie", "potem", "najpierw", "następnie", "wówczas", "wtedy", "zanim",
    "dopóki", "skoro", "bądź", "nie", "tak", "tedy", "zatem", "toteż",
    "lecz", "czego", "czym", "kim", "podczas", "jako", "ponadto", "wobec",
    "nigdy", "zawsze", "stąd", "wszędzie", "gdziekolwiek", "gdyby",
    "ani", "aż", "którego", "którymi", "wyłącznie", "więcej", "zgodnie",
}

# Subordinate-clause openers - a comma following such a segment closes the
# subordinate clause, it does not splice two clauses together.
_SUBORDINATE_OPENERS = re.compile(
    r"\b(?:gdzie|gdy|jeśli|jeżeli|ponieważ|chociaż|choć|gdyż|skoro|aby|żeby|"
    r"zanim|dopóki|gdyby|jako że)\b"
)

# Closed set of Polish inflectional suffixes. A vowel-final forbidden form
# also matches stem + one of these - enough to catch declensions such as
# 'bramy', 'bramce', or 'dotykania' without prefix-matching unrelated stems
# like 'zastanowić'.
INFLECT_SUFFIX = (
    "a|ą|e|ę|i|o|u|y|ie|em|om|ami|ach|ych|ego|ej|ym|im|owi|owa|owo|ową|"
    "owej|ce|ki|ka|kę|ek|ko|ów|ich|imi|ania|enia|ąc|ąca|ące|ący|ącą|ących|"
    "ącym|ącymi|ona|one|ony|oną|onej|onym|onych|ane|ana|any|aną|anej|anym|"
    "anych|ęta|ęte|ęty|ętą|ętej|ętym|ętych|ta|te|ty|tą|tej|tym|tych|"
    "ła|ło|ły|li"
)

# Words that can open nothing after a comma but a new independent clause -
# the confident splice shapes. Finite auxiliaries and impersonal modals, and
# personal pronouns starting a clause subject.
SPLICE_AUX = {
    "jest", "są", "był", "była", "było", "byli", "były", "będzie", "będą",
    "można", "trzeba", "wolno", "należy", "warto",
}
SPLICE_SUBJECTS = {"on", "ona", "ono", "oni", "one"}

# All-caps Polish words are never valid report renderings - the fixed
# vocabulary is title-case and true abbreviations (`OK`, `N/D`) stay short.
# A diacritic marks a word as Polish outright; the ASCII-only prefixes cover
# the rest of the fixed vocabulary (severity, status, type tags, markers).
CAPS_TOKEN_PREFIXES = (
    "NIE", "GOTOW", "NOW", "OTWART", "ZAMKNI", "ZASTOSOWA", "POTWIERDZON",
    "ZAAKCEPTOWA", "ZAPLANOWA", "ZABLOKOWA", "MONITOROWA", "PRZENIESIO",
    "ZALECAN", "OPCJONALN", "ZADEKLAROWA", "WZNOWION", "ZWERYFIKOWA",
    "OBSERWACJ", "KRYTYCZN", "TEORETYCZN", "WYSOK", "NISK", "UMIARKOWA",
    "ODROCZON", "STATYCZNIE", "DYNAMICZNIE", "DOTYCZY", "ZAKRESEM",
    "INFORMACJE", "POZA", "WNIOSEK", "BLAD",
)

# Polish filename stems stay uppercase - they are literals, not vocabulary.
CAPS_TOKEN_KEEP = {"POLOWANIE", "PRZEGLĄD", "AUDYT"}

POLISH_DIACRITICS = "ĄĆĘŁŃÓŚŹŻ"

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
    """Remove inline code spans and markdown link targets from a line."""
    text = re.sub(r"`[^`]*`", "", line)
    return re.sub(r"(\[[^\]]*\])\([^)]*\)", r"\1", text)


def pair_sibling(path):
    """True when the file is the translation sibling of a language pair:
    a `<stem>-<LANG>` name with a `<stem>-EN.md` file beside it. Under the
    pair-skeleton convention headings, `* **Label:**` field labels, and
    table label cells stay English verbatim and are exempt."""
    match = re.match(r"^(.*)-[A-Z]{2}$", path.stem)
    if not match:
        return False
    return path.with_name(f"{match.group(1)}-EN{path.suffix}").exists()


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


def load_allowed(rules_paths):
    """Parse allowed-phrase tables. Returns a list of phrase strings."""
    phrases = []
    seen = set()
    for rules in rules_paths:
        if not rules.exists():
            continue
        in_table = False
        for line in rules.read_text(encoding="utf-8").split("\n"):
            cells = [c.strip() for c in line.split("|")]
            if line.startswith("|") and len(cells) >= 4:
                first = cells[1].strip("`").lower()
                if first in ALLOWED_HEADERS:
                    in_table = True
                    continue
                if in_table:
                    if set(cells[1] + cells[2]) <= set("- "):
                        continue
                    phrase = re.sub(r"\(.*?\)", "", cells[1]).strip().strip("`")
                    if phrase and phrase.lower() not in seen:
                        seen.add(phrase.lower())
                        phrases.append(phrase)
            elif in_table:
                in_table = False
    return phrases


def mask_allowed(text, phrases):
    """Blank out allowed phrases so calque stems inside them cannot match."""
    masked = text
    for phrase in phrases:
        pattern = re.compile(
            r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", re.IGNORECASE
        )
        masked = pattern.sub(lambda m: " " * len(m.group(0)), masked)
    return masked


def check_forbidden(lineno, text, pairs, findings):
    lowered = text.lower()
    for forbidden, replacement in pairs:
        patterns = []
        if " " in forbidden:
            patterns.append(
                re.compile(r"\b" + re.escape(forbidden.lower()) + r"\w*")
            )
        else:
            root = stem(forbidden.lower())
            if len(root) <= 3:
                patterns.append(re.compile(r"\b" + re.escape(root) + r"\b"))
            else:
                patterns.append(re.compile(r"\b" + re.escape(root) + r"\w*"))
            # A vowel-final entry also gets a closed inflection match: the
            # word minus its final vowel is the stem, and only a Polish
            # inflectional suffix may follow it. Prefix-matching alone misses
            # declensions like 'bramy' or 'bramce', while an open 'bram\w*'
            # stem would cry wolf on 'bramofon' or 'zastanowić'.
            vowel_stripped = re.sub(r"[aąeęioóuy]$", "", root)
            if len(vowel_stripped) >= 4 and vowel_stripped != root:
                patterns.append(
                    re.compile(
                        r"\b" + re.escape(vowel_stripped)
                        + r"(?:" + INFLECT_SUFFIX + r")\b"
                    )
                )
        for pattern in patterns:
            for match in pattern.finditer(lowered):
                # ALL-CAPS tokens are data - enum labels (REQUEST CHANGES),
                # acronyms, identifier prefixes - not prose using the stem.
                token = text[match.start():match.end()]
                if len(token) >= 2 and token.isupper():
                    continue
                # A table cell whose whole content is the token is a label,
                # not prose - e.g. a 'Właściciel' column header naming owners.
                cell = re.compile(
                    r"\|\s*" + re.escape(token) + r"\s*\|", re.IGNORECASE
                )
                around = text[max(0, match.start() - 8):match.end() + 8]
                if cell.search(around):
                    continue
                findings.append(
                    ("error", lineno,
                     "calque '%s' - use '%s'" % (match.group(0), replacement))
                )


def check_token_case(lineno, text, findings):
    """Flag all-caps renderings of the title-case fixed vocabulary."""
    for match in re.finditer(r"\b[A-ZĄĆĘŁŃÓŚŹŻ]{3,}\b", text):
        word = match.group(0)
        if word in CAPS_TOKEN_KEEP:
            continue
        if any(c in POLISH_DIACRITICS for c in word) or word.startswith(
            CAPS_TOKEN_PREFIXES
        ):
            findings.append(
                ("error", lineno,
                 "all-caps Polish token '%s' - the fixed vocabulary renders "
                 "title-case" % word)
            )


_SERIES_BOUNDARY = re.compile(r"[,;:()\n]|\s(?:i|oraz|lub|albo|ani)(?=\s|$)")


def _in_enumeration_series(lowered, match):
    """A comma introduces a list item, not a clause, when the fragment after
    it is short and either ends at another list separator or already follows
    a list comma in the same run. A segment carrying a subordinate opener is
    a clause boundary, not a list, so it counts as a series as well."""
    segment_start = (
        max(lowered.rfind(char, 0, match.start()) for char in ".!?;:") + 1
    )
    segment = lowered[segment_start : match.start()]
    if _SUBORDINATE_OPENERS.search(segment):
        return True
    frag_start = match.start(1)
    boundary = _SERIES_BOUNDARY.search(lowered, frag_start)
    frag_end = boundary.start() if boundary else len(lowered)
    frag = lowered[frag_start:frag_end].strip()
    if len(re.findall(r"\w+", frag)) > 4:
        return False
    if re.match(r"[,;()]|\s(?:i|oraz|lub|albo|ani)(?=\s|$)", lowered[frag_end:]):
        return True
    return "," in segment


def check_mechanical(lineno, text, findings, splice=True):
    if "tylko, gdy" in text.lower():
        findings.append(("error", lineno, "'tylko, gdy' - write 'tylko wtedy, gdy'"))
    if re.search(r"\bper\s+\w", text):
        findings.append(("error", lineno, "'per X' - write 'dla każdego X'"))
    if re.search(r"\bw\.\s*\d", text):
        findings.append(("error", lineno, "'w.' - do not abbreviate 'wierszy'"))
    if re.search(r"~\s*\d", text):
        findings.append(("error", lineno, "'~N' - write 'ok. N' or 'około N'"))
    if re.search(r"\bNiej\b", text):
        findings.append(("error", lineno, "'Niej' - possible misspelling of a negated adjective"))
    if re.search(r"\bparitet\b", text.lower()):
        findings.append(("error", lineno, "'paritet' - misspelling of 'parytet'"))
    for char, name in TYPOGRAPHIC.items():
        if char in text:
            findings.append(("error", lineno, "typographic %s %r" % (name, char)))
    if ";" in text:
        findings.append(("error", lineno, "semicolon in prose"))

    # Comma-splice heuristic: a comma followed by a word that opens neither a
    # subordinate clause nor a prepositional phrase. Tables, list items, and
    # headings are skipped - their commas are usually enumerations. Commas
    # inside parentheses are masked out, a comma closing a parenthesized
    # enumeration item is allowed, and a comma before an identifier token such
    # as F-02 or ADR-3 separates list items. Enumeration noise is suppressed:
    # alphanumeric codes (A02), capitalized items mid-line (proper nouns and
    # defined names), and short fragments inside a comma series are lists.
    if not splice:
        return
    lowered = text.lower()
    paren_masked = re.sub(
        r"\([^()]*\)", lambda m: " " * len(m.group(0)), lowered
    )
    paren_masked = re.sub(
        r"\([^()]*$", lambda m: " " * len(m.group(0)), paren_masked
    )
    for match in re.finditer(r",\s+(\w+(?:-\w+)*)", paren_masked):
        word = match.group(1)
        if word in COMMA_OK or word[0].isdigit():
            continue
        if re.fullmatch(r"[a-z]+-\d+", word):
            continue
        if re.fullmatch(r"[a-z]+\d+", word):
            continue
        if lowered[: match.start()].rstrip().endswith(")"):
            continue
        # Only comma + finite auxiliary/modal or comma + personal pronoun is a
        # confident splice - the following word can open nothing but a new
        # independent clause. Participles, appositions, relative clauses, and
        # serial-verb continuations all legally follow a comma in Polish, so
        # flagging on them would make the gate cry wolf on every report.
        if word not in SPLICE_AUX and word not in SPLICE_SUBJECTS:
            continue
        original = text[match.start(1) : match.end(1)]
        before = lowered[: match.start()].rstrip()
        if (
            original[:1].isupper()
            and before
            and not before.endswith((".", "!", "?", ":", ";"))
        ):
            continue
        if _in_enumeration_series(lowered, match):
            continue
        findings.append(
            ("error", lineno,
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
    allowed = load_allowed(rules)
    if not pairs:
        print(
            "lint-polish: no forbidden forms loaded - pass "
            "--rules <path to polish-language.md>",
            file=sys.stderr,
        )

    skeleton = pair_sibling(args.file)
    block_label = re.compile(r"^\*\s+\*\*[^:*]+:\*\*")

    findings = []
    for lineno, text in iter_prose_lines(args.file):
        stripped = text.strip()
        if stripped.startswith("<!--"):
            continue
        is_table = stripped.startswith("|")
        is_list = bool(re.match(r"^[-*+]\s|^\d+\.\s|^\s+[-*+]\s", text))
        is_heading = stripped.startswith("#")
        if skeleton:
            if is_heading:
                continue
            label = block_label.match(stripped)
            if label:
                text = stripped[label.end():]
            elif is_table:
                text = re.sub(r"^\|[^|]*\|", "||", text)
        check_forbidden(lineno, mask_allowed(text, allowed), pairs, findings)
        check_token_case(lineno, text, findings)
        check_mechanical(lineno, text, findings,
                         splice=not (is_table or is_list or is_heading))

    errors = sum(1 for f in findings if f[0] == "error")
    for severity, lineno, message in findings:
        print("%s:%d: [%s] %s" % (args.file, lineno, severity.upper(), message))
    print("lint-polish: %d error(s), %d warning(s), %d forbidden forms loaded, "
          "%d allowed phrases loaded"
          % (errors, len(findings) - errors, len(pairs), len(allowed)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
