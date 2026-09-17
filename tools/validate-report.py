"""Mechanical consistency checker for Lens audit reports.

Runs the scriptable part of the Validation Record and the Pre-Delivery
Mechanical Checklist. Copy into the audited repository's `work/`
directory as `validate-report.tmp.py`, run it on the report file, then
remove the copy.

Usage: python validate-report.py <report.md>
Exit code 0 = all checks pass, 1 = failures found.
"""

import re
import sys

NL = chr(10)
EMDASH = chr(0x2014)
ENDASH = chr(0x2013)
ARROW = chr(0x2192)


def split_code(lines):
    """Return flags marking which lines are inside fenced blocks."""
    flags = []
    inside = False
    for line in lines:
        if line.lstrip().startswith("```"):
            inside = not inside
            flags.append(True)
            continue
        flags.append(inside)
    return flags


def strip_spans(s):
    s = re.sub("`[^`]*`", "", s)
    return re.sub(r"\]\([^)]*\)", "]", s)


def check_headings(lines, fences):
    bad = []
    for i, (l, f) in enumerate(zip(lines, fences)):
        if f:
            continue
        if re.match("^#{4,} ", l):
            bad.append("line %d: %s" % (i + 1, l[:60]))
            continue
        if re.match("^#{1,3} ", l):
            j = i + 1
            if j < len(lines) and lines[j].strip() != "":
                bad.append("line %d: heading not followed by one blank line" % (i + 1))
    return bad


def check_semicolons(lines, fences):
    bad = []
    for i, (l, f) in enumerate(zip(lines, fences)):
        if not f and ";" in strip_spans(l):
            bad.append("line %d: %s" % (i + 1, l[:70]))
    return bad


def check_dashes(lines, fences):
    bad = []
    for i, (l, f) in enumerate(zip(lines, fences)):
        if f:
            continue
        s = strip_spans(l)
        for ch, name in ((EMDASH, "em dash"), (ENDASH, "en dash"), (ARROW, "arrow")):
            if ch in s:
                bad.append("line %d: %s found: %s" % (i + 1, name, l[:60]))
    return bad


def check_table_code_spans(lines, fences):
    """A literal pipe inside an inline code span silently splits a table cell."""
    bad = []
    for i, (l, f) in enumerate(zip(lines, fences)):
        if f or not l.startswith("|"):
            continue
        for c in l.split("|")[1:-1]:
            if c.count("`") % 2:
                bad.append("line %d: unbalanced backtick in cell (literal pipe?): %s" % (i + 1, l[:60]))
                break
    return bad


def check_table_separators(lines, fences):
    bad = []
    for i, (l, f) in enumerate(zip(lines, fences)):
        if f or not l.startswith("|"):
            continue
        cells = l.split("|")[1:-1]
        if cells and all(set(c) <= set("-: ") and "-" in c for c in cells):
            for c in cells:
                if c != c.strip(" ") or " " in c.strip(":"):
                    bad.append("line %d: separator with spaces: %s" % (i + 1, l[:60]))
                    break
    return bad


def check_ids(text):
    bad = []
    fnds = set(re.findall("FND-[A-Z]{3}-[0-9]{3}", text))
    for m in re.finditer("RSK-[0-9]{3}.{0,200}?(FND-[A-Z]{3}-[0-9]{3})", text):
        if m.group(1) not in fnds:
            bad.append("risk cites unknown finding " + m.group(1))
    for m in re.finditer("REC-[0-9]{3}.{0,200}?(FND-[A-Z]{3}-[0-9]{3})", text):
        if m.group(1) not in fnds:
            bad.append("recommendation cites unknown finding " + m.group(1))
    return bad


def check_finding_blocks(lines):
    required = [
        "Pillar:", "Severity:", "Target Files/Modules:", "Requirement Basis:",
        "Evidence:", "Confidence:", "Verification State:", "Counter-check:",
        "Security Classification:", "Description:", "Impact:",
        "Remediation Recommendation:", "Verification Method:",
    ]
    bad = []
    starts = [i for i, l in enumerate(lines) if l.startswith("### FND-")]
    for k, i in enumerate(starts):
        end = starts[k + 1] if k + 1 < len(starts) else len(lines)
        block = NL.join(lines[i:end])
        name = lines[i][8:][:50]
        for field in required:
            if "**" + field + "**" not in block:
                bad.append("FND-" + name + ": missing " + field)
    return bad


def check_par_rows(text):
    bad = []
    for n in range(1, 10):
        p = "PAR-%d" % n
        if p not in text:
            bad.append("missing " + p)
    return bad


def check_trailing(text, lines):
    bad = []
    tail = [l for l in lines if l.strip()][-5:]
    if any("End of audit report" in l for l in tail):
        bad.append("closing line 'End of audit report' present")
    for i, l in enumerate(lines):
        if l != l.rstrip():
            bad.append("line %d: trailing whitespace" % (i + 1))
            if len(bad) > 10:
                break
    return bad


def main(path):
    text = open(path, "rb").read().decode("utf-8")
    lines = text.replace(chr(13) + NL, NL).split(NL)
    fences = split_code(lines)

    checks = [
        ("headings (no ####+, blank line after)", check_headings(lines, fences)),
        ("semicolons in prose", check_semicolons(lines, fences)),
        ("non-ASCII dashes/arrows", check_dashes(lines, fences)),
        ("table separator format", check_table_separators(lines, fences)),
        ("literal pipe inside code span", check_table_code_spans(lines, fences)),
        ("FND/RSK/REC cross-refs", check_ids(text)),
        ("finding-block fields", check_finding_blocks(lines)),
        ("PAR-1..PAR-9 present", check_par_rows(text)),
        ("trailing whitespace/closing line", check_trailing(text, lines)),
    ]

    failures = 0
    for name, bad in checks:
        print("[%s] %s" % ("FAIL" if bad else "PASS", name))
        for b in bad[:10]:
            print("       " + b)
        failures += len(bad)
    print("%d issue(s) found" % failures)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main(sys.argv[1])
