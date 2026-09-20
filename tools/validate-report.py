"""Mechanical consistency checker for Lens audit reports.

Runs structural, formatting, traceability, score-disclosure, and parity checks.
Copy into the audited repository's report-production directory as
``validate-report.tmp.py`` when validating a generated report.

Usage: python validate-report.py <report.md>
Exit code 0 means all checks pass, 1 means failures were found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

NL = "\n"
EMDASH = chr(0x2014)
ENDASH = chr(0x2013)
ARROW = chr(0x2192)
BASELINE_SECTIONS = [
    "Document Information",
    "Executive Summary",
    "System Context",
    "Health Dashboard",
    "High-Level Observations",
    "Auditing Methodology",
    "Scoring Rubrics",
    "Architectural Assessment",
    "Trade-off Analysis",
    "Strengths & What's Working",
    "Detailed Technical Findings",
    "Unified Risk Register",
    "Actionable Remediation Roadmap",
    "Scope Exclusions",
    "Limitations and Unknowns",
    "Validation Record",
    "References",
]
BRIEF_SECTIONS = {
    "Document Information",
    "Executive Summary",
    "System Context",
    "Health Dashboard",
    "High-Level Observations",
    "Strengths & What's Working",
    "Scope Exclusions",
    "Limitations and Unknowns",
    "Validation Record",
    "References",
}


def split_code(lines: list[str]) -> list[bool]:
    flags: list[bool] = []
    inside = False
    for line in lines:
        if line.lstrip().startswith("```"):
            inside = not inside
            flags.append(True)
            continue
        flags.append(inside)
    return flags


def strip_spans(value: str) -> str:
    value = re.sub(r"`[^`]*`", "", value)
    return re.sub(r"\]\([^)]*\)", "]", value)


def check_headings(lines: list[str], fences: list[bool]) -> list[str]:
    failures: list[str] = []
    for index, (line, fenced) in enumerate(zip(lines, fences)):
        if fenced:
            continue
        if re.match(r"^#{4,} ", line):
            failures.append(f"line {index + 1}: heading is deeper than ###")
            continue
        if re.match(r"^#{1,3} ", line):
            if index + 1 < len(lines) and lines[index + 1].strip() != "":
                failures.append(f"line {index + 1}: heading is not followed by one blank line")
    return failures


def check_semicolons(lines: list[str], fences: list[bool]) -> list[str]:
    failures: list[str] = []
    for index, (line, fenced) in enumerate(zip(lines, fences)):
        if not fenced and ";" in strip_spans(line):
            failures.append(f"line {index + 1}: semicolon in prose: {line[:80]}")
    return failures


def check_dashes(lines: list[str], fences: list[bool]) -> list[str]:
    failures: list[str] = []
    for index, (line, fenced) in enumerate(zip(lines, fences)):
        if fenced:
            continue
        value = strip_spans(line)
        for character, name in ((EMDASH, "em dash"), (ENDASH, "en dash"), (ARROW, "arrow")):
            if character in value:
                failures.append(f"line {index + 1}: {name} found: {line[:80]}")
    return failures


def table_blocks(lines: list[str], fences: list[bool]) -> list[tuple[int, list[str]]]:
    blocks: list[tuple[int, list[str]]] = []
    index = 0
    while index < len(lines):
        if fences[index] or not lines[index].startswith("|"):
            index += 1
            continue
        start = index
        rows: list[str] = []
        while index < len(lines) and not fences[index] and lines[index].startswith("|"):
            rows.append(lines[index])
            index += 1
        blocks.append((start, rows))
    return blocks


def raw_cells(line: str) -> list[str]:
    parts = line.split("|")
    return parts[1:-1] if len(parts) >= 2 and parts[-1].strip() == "" else parts[1:]


def content_cells(line: str) -> list[str]:
    return [cell.strip() for cell in raw_cells(line)]


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(cell and set(cell) <= {"-"} for cell in cells)


def check_tables(lines: list[str], fences: list[bool]) -> list[str]:
    failures: list[str] = []
    for start, rows in table_blocks(lines, fences):
        if len(rows) < 2:
            continue
        header = content_cells(rows[0])
        separator = content_cells(rows[1])
        if not is_separator(separator):
            continue
        widths = [len(cell) for cell in header]
        for row in rows[2:]:
            cells = content_cells(row)
            if is_separator(cells):
                continue
            if len(cells) != len(header):
                failures.append(f"line {start + rows.index(row) + 1}: table column count differs from header")
                continue
            widths = [max(widths[index], len(cell)) for index, cell in enumerate(cells)]
        raw_separator = raw_cells(rows[1])
        if any(cell != cell.strip() for cell in raw_separator):
            failures.append(f"line {start + 2}: table separator has spaces around hyphens")
        if len(raw_separator) != len(widths):
            failures.append(f"line {start + 2}: table separator column count differs from header")
        else:
            for index, cell in enumerate(raw_separator):
                expected = "-" * (widths[index] + 2)
                if cell != expected:
                    failures.append(
                        f"line {start + 2}: separator width in column {index + 1} is not {len(expected)}"
                    )
        header_positions = [index for index, char in enumerate(rows[0]) if char == "|"]
        for offset, row in enumerate(rows[2:], start=2):
            if is_separator(content_cells(row)):
                continue
            positions = [index for index, char in enumerate(row) if char == "|"]
            if positions != header_positions:
                failures.append(f"line {start + offset + 1}: table pipes are not vertically aligned")
    return failures


def check_ids(text: str) -> list[str]:
    failures: list[str] = []
    findings = set(re.findall(r"FND-[A-Z]{3}-[0-9]{3}", text))
    for match in re.finditer(r"RSK-[0-9]{3}.{0,240}?(FND-[A-Z]{3}-[0-9]{3})", text, re.DOTALL):
        if match.group(1) not in findings:
            failures.append(f"risk cites unknown finding {match.group(1)}")
    for match in re.finditer(r"REC-[0-9]{3}.{0,240}?(FND-[A-Z]{3}-[0-9]{3})", text, re.DOTALL):
        if match.group(1) not in findings:
            failures.append(f"recommendation cites unknown finding {match.group(1)}")
    return failures


def check_finding_blocks(lines: list[str]) -> list[str]:
    required = [
        "Pillar:",
        "Severity:",
        "Target Files/Modules:",
        "Requirement Basis:",
        "Evidence:",
        "Confidence:",
        "Verification State:",
        "Counter-check:",
        "Security Classification:",
        "Description:",
        "Impact:",
        "Remediation Recommendation:",
        "Verification Method:",
    ]
    failures: list[str] = []
    starts = [index for index, line in enumerate(lines) if line.startswith("### FND-")]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = NL.join(lines[start:end])
        name = lines[start][4:][:70]
        for field in required:
            if f"**{field}**" not in block:
                failures.append(f"{name}: missing {field}")
    return failures


def check_security_classification(lines: list[str]) -> list[str]:
    failures: list[str] = []
    starts = [index for index, line in enumerate(lines) if line.startswith("### FND-")]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = NL.join(lines[start:end])
        if "**Pillar:** Security & Compliance" not in block:
            continue
        match = re.search(r"\* \*\*Security Classification:\*\*\s*(.*)", block)
        if not match or not re.search(r"CWE-[0-9]+|\bUNKNOWN\b|\bN/A\b", match.group(1)):
            failures.append(f"{lines[start][4:70]}: security classification lacks CWE, UNKNOWN, or N/A")
    return failures


def check_par_rows(text: str) -> list[str]:
    failures: list[str] = []
    for number in range(1, 11):
        if not re.search(rf"^\|\s*PAR-{number}(?:\s|\||:)", text, re.MULTILINE):
            failures.append(f"missing Validation Record row PAR-{number}")
    return failures


def heading_slugs(text: str) -> set[str]:
    slugs: set[str] = set()
    counts: dict[str, int] = {}
    in_fence = False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if not match:
            continue
        base = re.sub(r"[^a-z0-9 _-]", "", match.group(1).lower()).replace(" ", "-")
        seen = counts.get(base, 0)
        counts[base] = seen + 1
        slugs.add(base if seen == 0 else f"{base}-{seen}")
    return slugs


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


def slugify(heading: str) -> str:
    return re.sub(r"[^a-z0-9 _-]", "", heading.lower()).replace(" ", "-")


def check_glossary(text: str) -> list[str]:
    failures: list[str] = []
    if "Document Information" not in text:
        return failures
    mode = re.search(r"\|\s*Descriptive Mode\s*\|\s*([^|]+)", text)
    heading = re.search(r"^#{2,3}\s+Glossary\s*$", text, re.MULTILINE)
    if not mode:
        failures.append("Document Information has no Descriptive Mode row")
        return failures
    value = mode.group(1).strip()
    if value not in ("Enabled", "Disabled"):
        failures.append(f"Descriptive Mode value must be Enabled or Disabled, got {value}")
        return failures
    if value == "Disabled":
        if heading:
            failures.append("Descriptive Mode is Disabled but the report has a Glossary section")
        exclusions = re.search(r"^#{2,3}\s+Scope Exclusions\s*$", text, re.MULTILINE)
        scope = ""
        if exclusions:
            following = re.search(r"^#{2,3}\s+", text[exclusions.end():], re.MULTILINE)
            scope = text[exclusions.end() : exclusions.end() + following.start() if following else len(text)]
        if not re.search(r"glossar|descriptive", scope, re.IGNORECASE):
            failures.append("Descriptive Mode is Disabled but Scope Exclusions does not justify the omitted Glossary")
        return failures
    if not heading:
        failures.append("Descriptive Mode is Enabled but the report has no Glossary section")
        return failures
    rest = text[heading.end():]
    following = re.search(r"^##\s+", rest, re.MULTILINE)
    g_end = heading.end() + (following.start() if following else len(rest))
    sub_slugs: dict[str, str] = {}
    sub_terms: list[str] = []
    for match in re.finditer(r"^###\s+(.+?)\s*$", text[heading.end() : g_end], re.MULTILINE):
        sub_heading = match.group(1)
        term = re.split(r"\s*\(", sub_heading, 1)[0].strip()
        sub_terms.append(term)
        sub_slugs[term] = slugify(sub_heading)
    if sub_terms != sorted(sub_terms, key=str.lower):
        failures.append("glossary descriptions are not in alphabetical order")
    table: list[str] = []
    for line in text[heading.end() : g_end].split("\n"):
        if line.startswith("###"):
            break
        if line.startswith("|"):
            table.append(line)
            continue
        if table:
            break
    terms: list[str] = []
    term_links: dict[str, str] = {}
    bad_cells = 0
    for row in table[2:]:
        if not row.startswith("|") or re.match(r"^\|[\s\-:|]+\|?$", row):
            continue
        cell = row.split("|")[1].strip()
        link = re.fullmatch(r"\[([^\]]+)\]\(#([^)]+)\)", cell)
        if link:
            terms.append(link.group(1))
            term_links[link.group(1)] = link.group(2)
        elif re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9/().+-]*", cell):
            terms.append(cell)
        else:
            bad_cells += 1
    if bad_cells:
        failures.append(f"glossary index has {bad_cells} malformed term cell(s)")
    if terms != sorted(terms, key=str.lower):
        failures.append("glossary terms are not in alphabetical order")
    if len(terms) != len(set(terms)):
        failures.append("glossary has duplicate terms")
    for required in ("SLO", "RPO", "RTO"):
        if required not in terms:
            failures.append(f"glossary is missing required term {required}")
    for term, anchor in term_links.items():
        if term not in sub_slugs:
            failures.append(f"glossary term {term} links to #{anchor} but has no ### description")
        elif anchor != sub_slugs[term]:
            failures.append(f"glossary term {term} links to #{anchor}, expected #{sub_slugs[term]}")
    for term in sub_slugs:
        if term not in terms:
            failures.append(f"glossary ### description {term} has no index-table row")
        elif term not in term_links:
            failures.append(f"glossary term {term} has a ### description but is not linked in the index table")
    slugs = heading_slugs(text)
    for term, anchor in term_links.items():
        if anchor not in slugs:
            failures.append(f"glossary term {term} links to missing anchor #{anchor}")
    failures.extend(check_glossary_body_links(text, terms, sub_slugs))
    return failures


def check_glossary_body_links(text: str, terms: list[str], sub_slugs: dict[str, str]) -> list[str]:
    failures: list[str] = []
    variant_map: dict[str, str] = {}
    for term in terms:
        for variant in glossary_variants(term):
            variant_map[variant] = term
    if not variant_map:
        return failures
    pattern = re.compile("|".join(re.escape(v) for v in sorted(variant_map, key=len, reverse=True)))
    sub_anchors = set(sub_slugs.values())
    unlinked = 0
    in_fence = False
    in_glossary = False
    for lineno, line in enumerate(text.split("\n"), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if re.match(r"^##\s+Glossary\s*$", line):
            in_glossary = True
            continue
        if in_glossary:
            if re.match(r"^##\s+\S", line):
                in_glossary = False
            else:
                continue
        if re.match(r"^#{1,6}\s", line):
            continue
        masked = re.sub(r"`[^`]*`", "", line)
        for link in re.finditer(r"\[([^\]]+)\]\(#([^)]+)\)", masked):
            link_text, anchor = link.group(1), link.group(2)
            if anchor != "glossary" and anchor not in sub_anchors:
                continue
            term = variant_map.get(link_text)
            if term is None:
                failures.append(f"line {lineno}: link [{link_text}](#{anchor}) text is not a glossary term")
            else:
                expected = sub_slugs.get(term, "glossary")
                if anchor != expected:
                    failures.append(f"line {lineno}: [{link_text}](#{anchor}) should link to #{expected}")
        masked = re.sub(r"\[[^\]]*\]\([^)]*\)", "", masked)
        masked = re.sub(r"https?://\S+", "", masked)
        masked = re.sub(r"\[[^\]]*\]", "", masked)
        for match in pattern.finditer(masked):
            start, end = match.start(), match.end()
            before = masked[start - 1] if start else " "
            after = masked[end] if end < len(masked) else " "
            if re.match(r"[\w/#.-]", before) or re.match(r"[\w/-]", after):
                continue
            unlinked += 1
            if unlinked <= 30:
                failures.append(f"line {lineno}: unlinked acronym {match.group(0)}")
    if unlinked > 30:
        failures.append(f"unlinked acronym occurrences total: {unlinked}")
    return failures


def check_required_sections(text: str) -> list[str]:
    if "Document Information" not in text:
        return []
    detail = re.search(r"\|\s*Detail Level\s*\|\s*([^|]+)", text)
    required = BRIEF_SECTIONS if detail and detail.group(1).strip() == "Brief" else set(BASELINE_SECTIONS)
    headings = set(re.findall(r"^#{2,3}\s+(.+?)\s*$", text, re.MULTILINE))
    return [f"missing required section: {section}" for section in BASELINE_SECTIONS if section in required and section not in headings]


def check_final_state(text: str) -> list[str]:
    state = re.search(r"\|\s*State\s*\|\s*([^|]+)", text)
    if not state or state.group(1).strip() != "Final":
        return []
    failures: list[str] = []
    if "## Validation Record" not in text:
        failures.append("Final report has no Validation Record")
    if "Parity baseline" not in text:
        failures.append("Final report has no parity baseline result")
    return failures


def check_score_disclosure(lines: list[str]) -> list[str]:
    failures: list[str] = []
    for index, line in enumerate(lines):
        if "overall score" not in line.lower() or not re.search(r"\d+\.\d+\s*/\s*\d+", line):
            continue
        window = " ".join(lines[index : index + 6]).lower()
        if "lowest" not in window:
            failures.append(f"line {index + 1}: overall score has no lowest-dimension floor")
    return failures


def check_project_qualification(text: str) -> list[str]:
    if "Project Inventory" not in text:
        return []
    failures: list[str] = []
    if re.search(r"\|\s*(both|either|the projects)\s*\|", text, re.IGNORECASE):
        failures.append("shared multi-project table uses an ambiguous project label")
    return failures


def check_trailing(lines: list[str]) -> list[str]:
    failures: list[str] = []
    nonempty = [line for line in lines if line.strip()]
    if any("End of audit report" in line for line in nonempty[-5:]):
        failures.append("closing line 'End of audit report' is present")
    for index, line in enumerate(lines):
        if line != line.rstrip():
            failures.append(f"line {index + 1}: trailing whitespace")
            if len(failures) > 20:
                break
    return failures


def main(path: str) -> int:
    text = Path(path).read_text(encoding="utf-8")
    lines = text.replace("\r\n", "\n").split("\n")
    fences = split_code(lines)
    checks = [
        ("headings", check_headings(lines, fences)),
        ("required sections", check_required_sections(text)),
        ("semicolons", check_semicolons(lines, fences)),
        ("non-ASCII dashes and arrows", check_dashes(lines, fences)),
        ("tables", check_tables(lines, fences)),
        ("FND/RSK/REC cross-references", check_ids(text)),
        ("finding-block fields", check_finding_blocks(lines)),
        ("security classifications", check_security_classification(lines)),
        ("score disclosure", check_score_disclosure(lines)),
        ("project qualification", check_project_qualification(text)),
        ("PAR-1..PAR-10", check_par_rows(text)),
        ("glossary", check_glossary(text)),
        ("final-state gate", check_final_state(text)),
        ("trailing whitespace and ending", check_trailing(lines)),
    ]
    failures = 0
    for name, problems in checks:
        status = "FAIL" if problems else "PASS"
        print(f"[{status}] {name}")
        for problem in problems[:10]:
            print(f"       {problem}")
        failures += len(problems)
    print(f"{failures} issue(s) found")
    return 1 if failures else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate-report.py <report.md>")
        raise SystemExit(1)
    raise SystemExit(main(sys.argv[1]))
