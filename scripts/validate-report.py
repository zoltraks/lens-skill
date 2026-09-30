"""Mechanical consistency checker for Lens audit and review reports.

Runs structural, formatting, traceability, score-disclosure, and parity checks.
Copy into the audited repository's report-production directory as
``validate-report.tmp.py`` when validating a generated report.

Review reports per ``process/review-report.md`` are detected by an H1 ending in
``Review and Amendment Instructions`` or a ``REVIEW``-family or ``PRZEGLĄD``-family
filename, and validated against the review contract instead of the audit checks.

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
    "Audit Type Coverage & Assurance Matrix",
    "Executive Summary",
    "System Context",
    "Software Bill of Materials",
    "License & IP Compliance Review",
    "Health Dashboard",
    "Delivery Practice & Team Continuity",
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
    "Audit Type Coverage & Assurance Matrix",
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


FINDING_REQUIRED = [
    "Pillar:",
    "Severity:",
    "Type:",
    "Security:",
    "Status:",
    "Change:",
    "Targets:",
    "Basis:",
    "Absence:",
    "Description:",
    "Impact:",
    "Recommendation:",
    "Method:",
    "Verified:",
    "Confidence:",
    "Mitigating factors:",
    "Exploitability:",
    "Evidence:",
]
RISK_REQUIRED = [
    "Severity:",
    "Likelihood:",
    "Residual:",
    "Status:",
    "Owner:",
    "Description:",
    "Impact:",
    "Trigger:",
    "Controls:",
    "Mitigation:",
    "Closure:",
    "Source:",
    "Confidence:",
]
FINDING_STATUS = ("Open", "Closed", "PASS")
CHANGE_VALUES = ("New", "Unchanged", "Reopened", "Closed")
RISK_STATUS = ("Open", "Accepted", "Transferred", "Monitoring", "Closed")
VERIFICATION_QUALIFIERS = ("Verified", "Confirmed", "Reported")
ABSENCE_VALUES = ("No documented rationale", "Deliberate - recorded decision",
                  "Undetermined", "N/A")


def field_value(block: str, field: str) -> str:
    match = re.search(rf"\*\*{re.escape(field)}:\*\*\s*(.*)", block)
    return match.group(1).strip() if match else ""


def check_finding_blocks(lines: list[str]) -> list[str]:
    failures: list[str] = []
    starts = [index for index, line in enumerate(lines) if line.startswith("### FND-")]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = NL.join(lines[start:end])
        name = lines[start][4:][:70]
        for field in FINDING_REQUIRED:
            if f"**{field}**" not in block:
                failures.append(f"{name}: missing {field}")
        status = field_value(block, "Status")
        if status and not re.match(rf"^({'|'.join(FINDING_STATUS)})\b", status):
            failures.append(f"{name}: Status is not a lifecycle value (Open/Closed/PASS)")
        change = field_value(block, "Change")
        if change and not re.match(rf"^({'|'.join(CHANGE_VALUES)})\b", change):
            failures.append(f"{name}: Change is not a provenance value (New/Unchanged/Reopened/Closed)")
        absence = field_value(block, "Absence")
        if absence and not re.match(rf"^({'|'.join(ABSENCE_VALUES)})\b", absence):
            failures.append(f"{name}: Absence is not an allowed token")
        verified = field_value(block, "Verified")
        if verified and not re.match(r"^(yes|no)\b", verified, re.IGNORECASE):
            failures.append(f"{name}: Verified does not start with yes or no")
    return failures


def check_risk_blocks(lines: list[str]) -> list[str]:
    failures: list[str] = []
    starts = [index for index, line in enumerate(lines) if line.startswith("### RSK-")]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = NL.join(lines[start:end])
        name = lines[start][4:][:70]
        for field in RISK_REQUIRED:
            if f"**{field}**" not in block:
                failures.append(f"{name}: missing {field}")
        status = field_value(block, "Status")
        if status and not re.match(rf"^({'|'.join(RISK_STATUS)})\b", status):
            failures.append(f"{name}: Status is not a treatment value (Open/Accepted/Transferred/Monitoring/Closed)")
    return failures


LEGACY_FIELDS = [
    "Target Files/Modules",
    "Requirement Basis",
    "Absence Assessment",
    "Verification State",
    "Countercheck",
    "Counter-check",
    "Security Classification",
    "Remediation Status",
    "Remediation Recommendation",
    "Verification Method",
    "Exploitability Narrative",
    "Source Finding",
    "Triggering Condition",
    "Existing Controls",
    "Residual Risk",
    "Treatment State",
    "Closure Trigger",
    "Remediation Cost",
    "Cost of Delay",
]


def check_legacy_fields(lines: list[str], fences: list[bool]) -> list[str]:
    failures: list[str] = []
    pattern = re.compile(r"\*\*(" + "|".join(re.escape(f) for f in LEGACY_FIELDS) + r"):\*\*")
    for index, (line, fenced) in enumerate(zip(lines, fences)):
        match = pattern.search(line)
        if match and not fenced:
            failures.append(f"line {index + 1}: legacy field name {match.group(1)}")
    return failures


def check_finding_summary(text: str) -> list[str]:
    block = section_block(text, r"^#{2,3}\s+Detailed Technical Findings\s*$")
    if not block:
        return []
    lines = block.split("\n")
    header_index = next(
        (index for index, line in enumerate(lines) if line.startswith("|") and "FND-" not in line),
        None,
    )
    if header_index is None:
        return []
    cells = [cell.strip() for cell in raw_cells(lines[header_index])]
    failures = []
    for wanted in ("Finding", "Result", "Status", "Change", "Verification"):
        if wanted not in cells:
            failures.append(f"findings summary table lacks a {wanted} column")
    for legacy in ("Finding ID", "Remediation Status"):
        if legacy in cells:
            failures.append(f"findings summary table still uses legacy column {legacy}")
    status_idx = cells.index("Status") if "Status" in cells else -1
    change_idx = cells.index("Change") if "Change" in cells else -1
    verification_idx = cells.index("Verification") if "Verification" in cells else -1
    for row in lines[header_index + 2 :]:
        if not row.startswith("|"):
            break
        row_cells = [cell.strip() for cell in raw_cells(row)]
        if not any("FND-" in cell for cell in row_cells):
            continue
        if status_idx >= 0 and len(row_cells) > status_idx:
            value = row_cells[status_idx]
            if value and value.split(" ")[0] not in FINDING_STATUS:
                failures.append(f"findings summary row has non-lifecycle Status '{value}'")
        if change_idx >= 0 and len(row_cells) > change_idx:
            value = row_cells[change_idx]
            if value and value.split(" ")[0] not in CHANGE_VALUES:
                failures.append(f"findings summary row has non-provenance Change '{value}'")
        if verification_idx >= 0 and len(row_cells) > verification_idx:
            value = row_cells[verification_idx]
            if value and value.split(" ")[0] not in VERIFICATION_QUALIFIERS:
                failures.append(f"findings summary row has bad Verification '{value}'")
    return failures


def check_finding_counts(text: str) -> list[str]:
    failures: list[str] = []
    pattern = re.compile(r"^#{2,3}\s+Detailed Technical Findings\s*$", re.MULTILINE)
    for match in pattern.finditer(text):
        rest = text[match.end() :]
        end = re.search(r"^#{2,3}\s+(?!FND-)", rest, re.MULTILINE)
        block = rest[: end.start()] if end else rest
        blocks = len(re.findall(r"^###\s+FND-", block, re.MULTILINE))
        first_block = re.search(r"^###\s+FND-", block, re.MULTILINE)
        summary_part = block[: first_block.start()] if first_block else block
        rows = 0
        for line in summary_part.split("\n"):
            if line.startswith("|") and "FND-" in line:
                rows += 1
        if blocks and rows != blocks:
            failures.append(
                f"Detailed Technical Findings: summary cites {rows} finding row(s) "
                f"but the section defines {blocks} ### FND- block(s)"
            )
    return failures


SCORE_PAIR = re.compile(r"(\d+(?:\.\d+)?)/(\d+)")


def check_scorecard_mean(text: str) -> list[str]:
    failures: list[str] = []
    summaries: list[tuple[float, int]] = []
    for marker in re.finditer(r"\*\*Scorecard Summary\*\*", text):
        rest = text[marker.end() :]
        lines = rest.split("\n")
        table = []
        for line in lines:
            if line.startswith("|"):
                table.append(line)
            elif table:
                break
        if len(table) < 3:
            continue
        header = [cell.strip() for cell in raw_cells(table[0])]
        score_idx = header.index("Score") if "Score" in header else -1
        if score_idx < 0:
            continue
        values: list[float] = []
        for row in table[2:]:
            cells = [cell.strip() for cell in raw_cells(row)]
            if len(cells) <= score_idx:
                continue
            pairs = SCORE_PAIR.findall(cells[score_idx])
            if pairs:
                num, denom = float(pairs[-1][0]), float(pairs[-1][1])
                if denom:
                    values.append(num / denom)
        if values:
            summaries.append((sum(values) / len(values), len(values)))
    overalls: list[tuple[float, int]] = []
    for line in text.split("\n"):
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in raw_cells(line)]
        if len(cells) >= 2 and cells[0] == "Overall score":
            pairs = SCORE_PAIR.findall(cells[1])
            if pairs:
                num, denom = float(pairs[-1][0]), float(pairs[-1][1])
                if denom:
                    overalls.append((num / denom, int(denom)))
    if len(overalls) != len(summaries):
        return failures
    for index, ((mean, count), (stated, denom)) in enumerate(zip(summaries, overalls), 1):
        if abs(mean - stated) > 0.5 / denom + 1e-9:
            failures.append(
                f"scorecard {index}: stated overall {stated * denom:g}/{denom} does not match "
                f"the mean of {count} dimension scores"
            )
    return failures


def check_ledger_columns(text: str) -> list[str]:
    failures: list[str] = []
    ledger = section_block(text, r"Verification And Evidence Ledger")
    if not ledger:
        return []
    header = None
    for line in ledger.split("\n"):
        if line.startswith("|"):
            header = line
            break
    if header is None:
        return []
    cells = [cell.strip() for cell in raw_cells(header)]
    if "Execution" in cells:
        failures.append("evidence ledger still has an Execution column")
    if "Evidence ID" in cells:
        failures.append("evidence ledger still uses legacy header Evidence ID")
    if "Project" in cells and "Project Inventory" not in text:
        failures.append("single-project ledger carries a Project column")
    return failures


def check_scorecard_na(text: str) -> list[str]:
    failures: list[str] = []
    marker = re.search(r"\*\*Scorecard Summary\*\*", text)
    if not marker:
        return []
    rest = text[marker.end():]
    rows = []
    for line in rest.split("\n"):
        if line.startswith("|"):
            rows.append(line)
            continue
        if rows:
            break
    for row in rows[2:]:
        cells = [cell.strip() for cell in raw_cells(row)]
        if len(cells) >= 2 and cells[1] == "N/A":
            failures.append(f"scorecard summary keeps an N/A row: {cells[0]}")
    return failures


def check_security_classification(lines: list[str]) -> list[str]:
    failures: list[str] = []
    starts = [index for index, line in enumerate(lines) if line.startswith("### FND-")]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = NL.join(lines[start:end])
        if "**Pillar:** Security & Compliance" not in block:
            continue
        match = re.search(r"\* \*\*Security:\*\*\s*(.*)", block)
        if not match or not re.search(r"CWE-[0-9]+|\bUNKNOWN\b|\bN/A\b|\bN/D\b|\bNIEZNANE\b", match.group(1)):
            failures.append(f"{lines[start][4:70]}: security classification lacks CWE or an unknown/not-applicable token")
        severity = re.search(r"\* \*\*Severity:\*\*\s*(.*)", block)
        narrative = re.search(r"\* \*\*Exploitability:\*\*\s*(.*)", block)
        if severity and narrative and re.search(r"\b(critical|high|krytyczna|wysoka)\b", severity.group(1), re.IGNORECASE):
            if re.fullmatch(r"N/?A|N/D", narrative.group(1).strip()):
                failures.append(f"{lines[start][4:70]}: HIGH/CRITICAL security finding's exploitability narrative is bare N/A without a reason")
    return failures


def check_type_tags(lines: list[str], fences: list[bool]) -> list[str]:
    failures: list[str] = []
    for index, (line, fenced) in enumerate(zip(lines, fences)):
        if fenced or not line.startswith("| EVD-"):
            continue
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if not any(cell in ("Observation", "Concern") for cell in cells):
            failures.append(f"line {index + 1}: evidence ledger row lacks an Observation/Concern tag")
    starts = [index for index, line in enumerate(lines) if line.startswith("### FND-")]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = NL.join(lines[start:end])
        match = re.search(r"\* \*\*Type:\*\*\s*(.*)", block)
        if match and match.group(1).strip() not in ("Observation", "Concern"):
            failures.append(f"{lines[start][4:70]}: Type is not Observation or Concern")
    return failures


def check_par_rows(text: str) -> list[str]:
    failures: list[str] = []
    for number in range(1, 19):
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


def _compound_word(token: str, trailing: bool) -> str:
    link = re.fullmatch(r"\[([^\]]+)\]\([^)]*\)", token)
    if link:
        return link.group(1)
    if trailing:
        return re.sub(r"[^A-Za-z0-9]+$", "", token)
    return re.sub(r"^[^A-Za-z0-9]+", "", token)


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

FIELD_LINE = re.compile(
    r"^\s*[*-]\s+\*\*(?:" + "|".join(FIELD_VALUE_LABELS) + r"):\*\*"
)


def mask_field_value(masked: str) -> str:
    match = FIELD_LINE.match(masked)
    if not match:
        return masked
    return masked[: match.end()] + " " * (len(masked) - match.end())


def slugify(heading: str) -> str:
    return re.sub(r"[^a-z0-9 _-]", "", heading.lower()).replace(" ", "-")


def check_glossary(text: str) -> list[str]:
    failures: list[str] = []
    if "Document Information" not in text:
        return failures
    heading = re.search(r"^#{2,3}\s+Glossary\s*$", text, re.MULTILINE)
    if not heading:
        exclusions = re.search(r"^#{2,3}\s+Scope Exclusions\s*$", text, re.MULTILINE)
        scope = ""
        if exclusions:
            following = re.search(r"^#{2,3}\s+", text[exclusions.end():], re.MULTILINE)
            scope = text[exclusions.end() : exclusions.end() + following.start() if following else len(text)]
        if not re.search(r"glossar|descriptive", scope, re.IGNORECASE):
            failures.append("report has no Glossary section and Scope Exclusions does not justify the omission")
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
        masked = re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line)
        for link in re.finditer(r"\[([^\]]+)\]\(#([^)]+)\)", masked):
            link_text, anchor = link.group(1), link.group(2)
            if anchor != "glossary" and anchor not in sub_anchors:
                continue
            if compound_context(masked, link.start(), link.end()):
                failures.append(
                    f"line {lineno}: [{link_text}](#{anchor}) links an acronym inside a capitalized compound name"
                )
                continue
            term = variant_map.get(link_text)
            if term is None:
                failures.append(f"line {lineno}: link [{link_text}](#{anchor}) text is not a glossary term")
            else:
                expected = sub_slugs.get(term, "glossary")
                if anchor != expected:
                    failures.append(f"line {lineno}: [{link_text}](#{anchor}) should link to #{expected}")
        masked = re.sub(r"\[[^\]]*\]\([^)]*\)", lambda m: " " * len(m.group(0)), masked)
        masked = re.sub(r"https?://\S+", lambda m: " " * len(m.group(0)), masked)
        masked = re.sub(r"\[[^\]]*\]", lambda m: " " * len(m.group(0)), masked)
        masked = mask_field_value(masked)
        for match in pattern.finditer(masked):
            start, end = match.start(), match.end()
            before = masked[start - 1] if start else " "
            after = masked[end] if end < len(masked) else " "
            if re.match(r"[\w/#.-]", before) or re.match(r"[\w/-]", after):
                continue
            if compound_context(masked, start, end):
                continue
            unlinked += 1
            if unlinked <= 30:
                failures.append(f"line {lineno}: unlinked acronym {match.group(0)}")
    if unlinked > 30:
        failures.append(f"unlinked acronym occurrences total: {unlinked}")
    return failures


def is_review_report(path: str, text: str) -> bool:
    stem = Path(path).stem.upper()
    if re.search(r"(?:^|[-_])(?:REVIEW|PRZEGLĄD|PRZEGLAD)(?:-|$)", stem):
        return True
    return bool(re.search(r"^#\s+.+\bReview and Amendment Instructions\s*$", text, re.MULTILINE))


def section_block(text: str, heading_pattern: str) -> str:
    match = re.search(heading_pattern, text, re.MULTILINE)
    if not match:
        return ""
    block = text[match.end():]
    following = re.search(r"^##\s+", block, re.MULTILINE)
    return block[: following.start()] if following else block


def check_review_sections(text: str) -> list[str]:
    failures: list[str] = []
    for pattern, label in (
        (r"^##\s+Assessment\s*$", "Assessment"),
        (r"^###\s+Findings and Corrections\s*$", "Findings and Corrections"),
        (r"^##\s+Required Changes\b", "Required Changes"),
        (r"^##\s+Suggested Amendment Order\s*$", "Suggested Amendment Order"),
        (r"^##\s+Public Source Register\s*$", "Public Source Register"),
    ):
        if not re.search(pattern, text, re.MULTILINE):
            failures.append(f"missing required review section: {label}")
    return failures


def check_review_findings_table(text: str) -> list[str]:
    block = section_block(text, r"^###\s+Findings and Corrections\s*$")
    if not block:
        return []
    header = next(
        (line for line in block.split("\n") if line.startswith("|") and "Finding" in line),
        None,
    )
    if header is None:
        return ["Findings and Corrections has no findings table"]
    cells = [cell.strip() for cell in raw_cells(header)]
    failures = []
    if "Finding" not in cells:
        failures.append("findings table lacks a Finding column")
    if "Required correction" not in cells:
        failures.append("findings table lacks a Required correction column")
    return failures


def check_review_change_groups(text: str) -> list[str]:
    block = section_block(text, r"^##\s+Required Changes\b.*$")
    if not block:
        return []
    if not re.search(r"^###\s+", block, re.MULTILINE):
        return ["Required Changes has no ### change group"]
    return []


def check_review_sources(text: str) -> list[str]:
    register = section_block(text, r"^##\s+Public Source Register\s*$")
    if not register:
        return []
    rows = set(re.findall(r"^\|\s*(S\d+)\s*\|", register, re.MULTILINE))
    body = text[: re.search(r"^##\s+Public Source Register\s*$", text, re.MULTILINE).start()]
    cited: set[str] = set()
    for group in re.findall(r"\[([^\]\[]+)\]", body):
        if re.fullmatch(r"[S\d,\s]+", group):
            cited.update(re.findall(r"S\d+", group))
    failures = [f"citation [{missing}] has no register row" for missing in sorted(cited - rows)]
    failures.extend(
        f"register row {unused} is never cited in the body" for unused in sorted(rows - cited)
    )
    return failures


def check_required_sections(text: str) -> list[str]:
    if "Document Information" not in text:
        return []
    detail = re.search(r"\|\s*Detail Level\s*\|\s*([^|]+)", text)
    brief = detail is not None and detail.group(1).strip() == "Brief"
    required = set(BRIEF_SECTIONS if brief else BASELINE_SECTIONS)
    ordered = list(BASELINE_SECTIONS)
    if not brief:
        required.add("Recommendation Classification")
        ordered.append("Recommendation Classification")
    headings = set(re.findall(r"^#{2,3}\s+(.+?)\s*$", text, re.MULTILINE))
    return [f"missing required section: {section}" for section in ordered if section in required and section not in headings]


def check_rec_classification(text: str) -> list[str]:
    failures: list[str] = []
    starts = [
        match.end()
        for match in re.finditer(r"^#{2,3}\s+Recommendation Classification\s*$", text, re.MULTILINE)
    ]
    if not starts:
        return failures
    classified: list[str] = []
    for end in starts:
        rest = text[end:]
        following = re.search(r"^#{1,3}\s", rest, re.MULTILINE)
        section = rest[: following.start()] if following else rest
        table = [line for line in section.split("\n") if line.startswith("|")]
        for line in table:
            classified += re.findall(r"REC-\d{3}", line)
        if len(table) >= 2:
            header = [cell.strip() for cell in raw_cells(table[0])]
            if "Class" in header:
                class_idx = header.index("Class")
                for row in table[2:]:
                    row_cells = [cell.strip() for cell in raw_cells(row)]
                    if len(row_cells) <= class_idx or not re.search(r"REC-\d{3}", row):
                        continue
                    if row_cells[class_idx] not in ("Recommended", "Optional", "Not recommended"):
                        failures.append(f"classification row has invalid class '{row_cells[class_idx]}'")
    defined = re.findall(r"^###\s+(REC-\d{3})", text, re.MULTILINE)
    for rec in sorted(set(defined)):
        if classified.count(rec) != defined.count(rec):
            failures.append(
                f"{rec} appears {classified.count(rec)} time(s) in classification sections, "
                f"expected {defined.count(rec)}"
            )
    for rec in sorted(set(classified) - set(defined)):
        failures.append(f"classification cites unknown {rec}")
    return failures


def check_final_state(text: str) -> list[str]:
    # The State row is written only while a report is Draft; a final report omits it.
    # An explicit `State | Draft` marks the report as still in progress, so the gate skips.
    # Without any State row an English report is final and the gate runs.
    # Checks keyed on English anchors stay lenient on non-English reports, matching the
    # English-mapped validation copy convention.
    state = re.search(r"\|\s*State\s*\|\s*([^|]+)", text)
    if state and state.group(1).strip() == "Draft":
        return []
    if not state and "Document Information" not in text:
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


VERSION_DIR = re.compile(r"v?\d+\.\d+(?:\.\d+)?")
DATE_DIR = re.compile(r"\d{4}-\d{2}-\d{2}")


def dir_pattern(name: str) -> str | None:
    if VERSION_DIR.fullmatch(name):
        return "version-numbered"
    if DATE_DIR.fullmatch(name):
        return "date-named"
    return None


def check_location(path: str) -> list[str]:
    parent = Path(path).resolve().parent
    own = dir_pattern(parent.name)
    if own is None:
        return []
    siblings = [
        dir_pattern(child.name)
        for child in parent.parent.iterdir()
        if child.is_dir() and child != parent
    ]
    other = "date-named" if own == "version-numbered" else "version-numbered"
    if siblings.count(other) > siblings.count(own):
        return [
            f"report directory '{parent.name}' is {own} but its siblings are predominantly {other}"
        ]
    return []


def main(path: str) -> int:
    text = Path(path).read_text(encoding="utf-8")
    lines = text.replace("\r\n", "\n").split("\n")
    fences = split_code(lines)
    review = is_review_report(path, text)
    checks = [
        ("headings", check_headings(lines, fences)),
        ("semicolons", check_semicolons(lines, fences)),
        ("non-ASCII dashes and arrows", check_dashes(lines, fences)),
        ("tables", check_tables(lines, fences)),
        ("location pattern", check_location(path)),
        ("trailing whitespace and ending", check_trailing(lines)),
    ]
    if review:
        checks.extend(
            [
                ("review sections", check_review_sections(text)),
                ("review findings table", check_review_findings_table(text)),
                ("review change groups", check_review_change_groups(text)),
                ("review source register", check_review_sources(text)),
            ]
        )
    else:
        checks.extend(
            [
                ("required sections", check_required_sections(text)),
                ("FND/RSK/REC cross-references", check_ids(text)),
                ("finding-block fields", check_finding_blocks(lines)),
                ("risk-block fields", check_risk_blocks(lines)),
                ("legacy field names", check_legacy_fields(lines, fences)),
                ("findings summary columns", check_finding_summary(text)),
                ("findings count", check_finding_counts(text)),
                ("scorecard mean", check_scorecard_mean(text)),
                ("ledger columns", check_ledger_columns(text)),
                ("scorecard N/A rows", check_scorecard_na(text)),
                ("security classifications", check_security_classification(lines)),
                ("score disclosure", check_score_disclosure(lines)),
                ("project qualification", check_project_qualification(text)),
                ("PAR-1..PAR-18", check_par_rows(text)),
                ("recommendation classification", check_rec_classification(text)),
                ("Observation/Concern tags", check_type_tags(lines, fences)),
                ("glossary", check_glossary(text)),
                ("final-state gate", check_final_state(text)),
            ]
        )
    print(f"report type: {'review' if review else 'audit'}")
    failures = 0
    for name, problems in checks:
        status = "FAIL" if problems else "PASS"
        total = f" ({len(problems)} issue(s))" if problems else ""
        print(f"[{status}] {name}{total}")
        for problem in problems[:10]:
            print(f"       {problem}")
        if len(problems) > 10:
            print(f"       ... and {len(problems) - 10} more")
        failures += len(problems)
    print(f"{failures} issue(s) found")
    return 1 if failures else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate-report.py <report.md>")
        raise SystemExit(1)
    raise SystemExit(main(sys.argv[1]))
