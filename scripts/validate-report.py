"""Mechanical consistency checker for Lens audit and review reports.

Runs structural, formatting, traceability, score-disclosure, and parity checks.
Copy into the audited repository's report-production directory as
``validate-report.tmp.py`` when validating a generated report.

Report style is read from the ``Report Style`` row in Document Information and
selects the audit, hunt, or review section contract. A ``Review Scope:
Structure`` row in a review report selects the structure variant contract.
Files in the ``REVIEW``/``PRZEGLĄD`` family whose names carry a custom suffix
run as ``custom`` reports - shared mechanical checks only, no structural
contract. Reports matching the removed amendment-review shape (``Review and
Amendment Instructions`` title, ``Findings and Corrections`` subsection, or
``Action Proposals`` section) run as ``legacy`` and fail with a pointer to the
current contract.

Usage:
  python validate-report.py <report.md> [--repo-root <dir>]
  python validate-report.py --dump-contract

Exit code 0 means all checks pass, 1 means failures were found.

With ``--repo-root`` the validator also checks that ``path:line`` citations in
finding ``Targets``/``Evidence`` fields resolve to real files within range.

``--dump-contract`` prints the mechanically enforced contract as JSON - required
sections, field lists, token sets, and the hunt- and check-specific rules - so an
agent can load the machine-readable surface without parsing the documentation
corpus.
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

NL = "\n"
EMDASH = chr(0x2014)
ENDASH = chr(0x2013)
ARROW = chr(0x2192)
BASELINE_SECTIONS = [
    "Document Information",
    "Audit Type Coverage",
    "Executive Summary",
    "System Context",
    "Software Bill of Materials",
    "License Compliance Review",
    "Health Dashboard",
    "Delivery Practice & Team Continuity",
    "High-Level Observations",
    "Auditing Methodology",
    "Scoring Rubrics",
    "Architectural Assessment",
    "Structure Review",
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
    "Audit Type Coverage",
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
            failures.append(
                f"line {index + 1}: semicolon in prose - use a comma or split the "
                f"sentence: {line[:80]}"
            )
    return failures


def check_dashes(lines: list[str], fences: list[bool]) -> list[str]:
    failures: list[str] = []
    for index, (line, fenced) in enumerate(zip(lines, fences)):
        if fenced:
            continue
        value = strip_spans(line)
        for character, name in ((EMDASH, "em dash"), (ENDASH, "en dash"), (ARROW, "arrow")):
            if character in value:
                failures.append(
                    f"line {index + 1}: {name} found - use ASCII '-' or '->': "
                    f"{line[:80]}"
                )
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


def sep_like(cells: list[str]) -> bool:
    return (
        bool(cells)
        and all(set(cell) <= {"-", ":"} for cell in cells)
        and any("-" in cell for cell in cells)
    )


def check_tables(lines: list[str], fences: list[bool]) -> list[str]:
    failures: list[str] = []
    for start, rows in table_blocks(lines, fences):
        for offset, row in enumerate(rows):
            if row.startswith("||"):
                failures.append(f"line {start + offset + 1}: table row starts with '||'")
        if len(rows) < 2:
            continue
        sep_index = next(
            (index for index, row in enumerate(rows) if sep_like(content_cells(row))),
            None,
        )
        if sep_index is None:
            failures.append(f"line {start + 1}: table has no separator row")
            continue
        if sep_index != 1:
            failures.append(
                f"line {start + sep_index + 1}: separator row is not the second table row"
            )
        for index, cell in enumerate(content_cells(rows[sep_index])):
            if "-" not in cell:
                failures.append(
                    f"line {start + sep_index + 1}: separator cell {index + 1} has no hyphen"
                )
        data_rows = [
            row
            for index, row in enumerate(rows)
            if index != sep_index and not is_separator(content_cells(row))
        ]
        if data_rows:
            ncols = max(len(content_cells(row)) for row in data_rows)
            for column in range(ncols):
                if all(
                    column >= len(content_cells(row))
                    or content_cells(row)[column] == ""
                    for row in data_rows
                ):
                    failures.append(
                        f"line {start + 1}: column {column + 1} is empty in every row"
                    )
        if sep_index != 1:
            continue
        header = content_cells(rows[0])
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
    "Status:",
    "Change:",
    "Targets:",
    "Basis:",
    "Description:",
    "Impact:",
    "Recommendation:",
    "Method:",
    "Verified:",
    "Runtime confirmed:",
    "Confidence:",
    "Mitigating factors:",
    "Evidence:",
]
RISK_REQUIRED = [
    "Severity:",
    "Likelihood:",
    "Residual:",
    "Status:",
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
FINDING_PILLARS = ("ARC", "CQY", "SEC", "INF", "AIP", "CPR", "API", "STR")
FINDING_ID = re.compile(r"FND-(?:ARC|CQY|SEC|INF|AIP|CPR|API|STR)-\d{3}")
ABSENCE_VALUES = ("No documented rationale", "Deliberate - recorded decision",
                  "Undetermined")
EMPTY_FIELD_VALUE = re.compile(r"^(N/?A|N/D|NOT SPECIFIED|NIEOKREŚLON)\b", re.IGNORECASE)


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
        pillar = re.match(r"FND-([A-Z]{3})-\d{3}", name)
        if pillar and pillar.group(1) not in FINDING_PILLARS:
            failures.append(
                f"{name}: pillar code '{pillar.group(1)}' is not one of "
                f"{'/'.join(FINDING_PILLARS)} - expected FND-<pillar>-NNN"
            )
        for field in FINDING_REQUIRED:
            if f"**{field}**" not in block:
                failures.append(
                    f"{name}: missing {field[:-1]} - expected literal "
                    f"'* **{field}** <value>'"
                )
        status = field_value(block, "Status")
        if status and not re.match(rf"^({'|'.join(FINDING_STATUS)})\b", status):
            failures.append(f"{name}: Status is not a lifecycle value (Open/Closed/PASS)")
        change = field_value(block, "Change")
        if change and not re.match(rf"^({'|'.join(CHANGE_VALUES)})\b", change):
            failures.append(f"{name}: Change is not a provenance value (New/Unchanged/Reopened/Closed)")
        absence = field_value(block, "Absence")
        if absence and not EMPTY_FIELD_VALUE.match(absence) \
                and not re.match(rf"^({'|'.join(ABSENCE_VALUES)})\b", absence):
            failures.append(f"{name}: Absence is not an allowed token")
        for field in ("Security", "Exploitability", "Absence"):
            value = field_value(block, field)
            if EMPTY_FIELD_VALUE.match(value):
                failures.append(f"{name}: {field} renders {value.split(' ')[0]} - omit the line entirely")
        verified = field_value(block, "Verified")
        if verified and not re.match(r"^(yes|no)\b", verified, re.IGNORECASE):
            failures.append(f"{name}: Verified does not start with yes or no")
        runtime = field_value(block, "Runtime confirmed")
        if runtime and not re.match(r"^(yes|no|not applicable)\b", runtime, re.IGNORECASE):
            failures.append(
                f"{name}: Runtime confirmed does not start with yes, no, or not applicable"
            )
        breaking = field_value(block, "Breaking change")
        if breaking and not re.match(r"^(None|Internal|Public API)\b", breaking):
            failures.append(f"{name}: Breaking change is not None/Internal/Public API")
        applicability = field_value(block, "Applicability")
        if applicability and not re.match(
            r"^(applicable|conditional|inapplicable|unverified)\b", applicability
        ):
            failures.append(f"{name}: Applicability is not an allowed token")
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
                failures.append(
                    f"{name}: missing {field[:-1]} - expected literal "
                    f"'* **{field}** <value>'"
                )
        status = field_value(block, "Status")
        if status and not re.match(rf"^({'|'.join(RISK_STATUS)})\b", status):
            failures.append(f"{name}: Status is not a treatment value (Open/Accepted/Transferred/Monitoring/Closed)")
        owner = field_value(block, "Owner")
        if owner and EMPTY_FIELD_VALUE.match(owner):
            failures.append(f"{name}: Owner renders an unspecified value - omit the line entirely")
        if re.search(r"^\*\s+\*\*Owner:\*\*\s*$", block, re.MULTILINE):
            failures.append(f"{name}: Owner renders an empty value - omit the line entirely")
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
            failures.append(
                f"line {index + 1}: legacy field name {match.group(1)} - "
                "expected the current field name per findings-registers.md"
            )
    return failures


def findings_heading(text: str) -> str:
    if report_style(text) in ("hunt", "review"):
        return "Domain Findings"
    return "Detailed Technical Findings"


def check_finding_summary(text: str) -> list[str]:
    block = section_block(text, rf"^#{{2,3}}\s+{findings_heading(text)}\s*$")
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
                failures.append(
                    f"findings summary row has non-lifecycle Status '{value}' - "
                    "expected Open/Closed/PASS"
                )
        if change_idx >= 0 and len(row_cells) > change_idx:
            value = row_cells[change_idx]
            if value and value.split(" ")[0] not in CHANGE_VALUES:
                failures.append(
                    f"findings summary row has non-provenance Change '{value}' - "
                    "expected New/Unchanged/Reopened/Closed"
                )
        if verification_idx >= 0 and len(row_cells) > verification_idx:
            value = row_cells[verification_idx]
            if value and value.split(" ")[0] not in VERIFICATION_QUALIFIERS:
                failures.append(
                    f"findings summary row has bad Verification '{value}' - "
                    "expected Verified/Confirmed/Reported or empty"
                )
    return failures


def check_finding_counts(text: str) -> list[str]:
    failures: list[str] = []
    heading = findings_heading(text)
    hunt = heading == "Domain Findings"
    pattern = re.compile(rf"^#{{2,3}}\s+{re.escape(heading)}\s*$", re.MULTILINE)
    for match in pattern.finditer(text):
        rest = text[match.end() :]
        if hunt:
            # ### domain headings interleave with ### FND- blocks inside the register,
            # so only a level-2 heading ends the section.
            end = re.search(r"^##\s", rest, re.MULTILINE)
        else:
            end = re.search(r"^#{2,3}\s+(?!FND-)", rest, re.MULTILINE)
        block = rest[: end.start()] if end else rest
        blocks = len(re.findall(r"^###\s+FND-", block, re.MULTILINE))
        # The hunt register opens its per-domain ### headings after the summary table,
        # so the summary ends at the first ### heading of any kind.
        first_block = re.search(
            r"^###\s+\S" if hunt else r"^###\s+FND-", block, re.MULTILINE
        )
        summary_part = block[: first_block.start()] if first_block else block
        rows = 0
        for line in summary_part.split("\n"):
            if line.startswith("|") and "FND-" in line:
                rows += 1
        if blocks and rows != blocks:
            failures.append(
                f"{heading}: summary cites {rows} finding row(s) "
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
    if len(summaries) > len(overalls):
        failures.append(
            f"{len(summaries)} scorecard table(s) found but only "
            f"{len(overalls)} 'Overall score' row(s) - every scorecard must state its overall"
        )
    for index, ((mean, count), (stated, denom)) in enumerate(zip(summaries, overalls), 1):
        expected_even = round(mean * denom, 1)
        expected_up = math.floor(mean * denom * 10 + 0.5) / 10
        stated_display = stated * denom
        if abs(stated_display - expected_even) > 1e-9 and abs(stated_display - expected_up) > 1e-9:
            failures.append(
                f"scorecard {index}: stated overall {stated_display:g}/{denom} does not equal "
                f"the recomputed mean {expected_up:g}/{denom} of {count} displayed "
                "dimension scores"
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
        match = re.search(r"\* \*\*Security:\*\*\s*(.*)", block)
        if match and not EMPTY_FIELD_VALUE.match(match.group(1).strip()) \
                and not re.search(r"CWE-[0-9]+|\bUNKNOWN\b|\bNIEZNANE\b", match.group(1)):
            failures.append(f"{lines[start][4:70]}: security classification lacks CWE or an unknown token")
        if "**Pillar:** Security & Compliance" not in block:
            continue
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
    for number in range(1, 21):
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
        term = re.split(r"\s*\(", sub_heading, maxsplit=1)[0].strip()
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


REVIEW_CANONICAL_STEM = re.compile(r"^(?:REVIEW|PRZEGLĄD|PRZEGLAD)(?:-\d+(?:\.\d+)?)?$")
REVIEW_FAMILY_STEM = re.compile(r"(?:^|[-_])(?:REVIEW|PRZEGLĄD|PRZEGLAD)(?:-|$)")
LEGACY_REVIEW_SHAPE = re.compile(
    r"(?m)^#\s+.+\bReview and Amendment Instructions\s*$"
    r"|^###\s+Findings and Corrections\s*$"
    r"|^##\s+Action Proposals\s*$"
)


def report_kind(path: str, text: str) -> str:
    """Classify the file as 'legacy', 'custom', or 'audit'.

    Files matching the removed amendment-review shape are 'legacy' - they fail
    with a pointer to the current contract rather than a wall of missing
    sections. REVIEW/PRZEGLĄD-family filenames with a custom suffix are
    'custom' - validated mechanically only. Everything else, including
    canonical REVIEW/PRZEGLĄD filenames, is an 'audit'-kind report whose
    section contract is selected by the Report Style row.
    """
    stem = Path(path).stem.upper()
    if LEGACY_REVIEW_SHAPE.search(text):
        return "legacy"
    if REVIEW_FAMILY_STEM.search(stem) and not REVIEW_CANONICAL_STEM.fullmatch(stem):
        return "custom"
    return "audit"


def section_block(text: str, heading_pattern: str) -> str:
    match = re.search(heading_pattern, text, re.MULTILINE)
    if not match:
        return ""
    block = text[match.end():]
    following = re.search(r"^##\s+", block, re.MULTILINE)
    return block[: following.start()] if following else block


STRUCTURE_VARIANT_SECTIONS = [
    "Document Information",
    "Project Context",
    "Structural Overview",
    "Findings",
    "Positive Practices",
    "Recommendations",
    "Prioritization",
    "Limitations and Assumptions",
]


def check_structure_variant_sections(text: str) -> list[str]:
    headings = [
        match.group(1).strip()
        for match in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)
    ]
    failures = [
        f"missing required structure-review section: {section}"
        for section in STRUCTURE_VARIANT_SECTIONS
        if section not in headings
    ]
    present = [h for h in headings if h in STRUCTURE_VARIANT_SECTIONS]
    if present != [s for s in STRUCTURE_VARIANT_SECTIONS if s in present]:
        failures.append("structure-review sections are not in the canonical order")
    return failures


REPORT_STYLES = ("audit", "hunt", "review")


def check_required_sections(text: str) -> list[str]:
    if "Document Information" not in text:
        return []
    style = report_style(text)
    if style not in REPORT_STYLES:
        return [
            f"unknown Report Style '{style}' - expected "
            f"{'/'.join(REPORT_STYLES)}"
        ]
    if style in ("hunt", "review"):
        required = HUNT_SECTIONS if report_style(text) == "hunt" else REVIEW_SECTIONS
        headings = set(re.findall(r"^#{2,3}\s+(.+?)\s*$", text, re.MULTILINE))
        return [
            f"missing required section: {section}"
            for section in required
            if section not in headings
        ]
    detail = re.search(r"\|\s*Detail Level\s*\|\s*([^|]+)", text)
    brief = detail is not None and detail.group(1).strip() == "Brief"
    required = set(BRIEF_SECTIONS if brief else BASELINE_SECTIONS)
    ordered = list(BASELINE_SECTIONS)
    if not brief:
        required.add("Recommendation Classification")
        ordered.append("Recommendation Classification")
    headings = set(re.findall(r"^#{2,3}\s+(.+?)\s*$", text, re.MULTILINE))
    return [f"missing required section: {section}" for section in ordered if section in required and section not in headings]


def check_coverage_rows(text: str) -> list[str]:
    start = re.search(r"^##\s+Audit Type Coverage\s*$", text, re.MULTILINE)
    if not start:
        return []
    rest = text[start.end() :]
    following = re.search(r"^#{1,3}\s", rest, re.MULTILINE)
    section = rest[: following.start()] if following else rest
    table = [line for line in section.split("\n") if line.startswith("|")]
    failures: list[str] = []
    if len(table) < 3:
        return failures
    header = [cell.strip() for cell in raw_cells(table[0])]
    if "Status" not in header:
        return failures
    status_idx = header.index("Status")
    name_idx = header.index("Report type") if "Report type" in header else 0
    for row in table[2:]:
        cells = [cell.strip() for cell in raw_cells(row)]
        if len(cells) <= status_idx:
            continue
        if cells[status_idx] and cells[status_idx] not in ("Covered", "Partially", "Not done"):
            name = cells[name_idx] if len(cells) > name_idx and cells[name_idx] else row
            failures.append(
                f"coverage row '{name}' has status '{cells[status_idx]}', "
                "expected Covered, Partially, or Not done - omit Not Applicable rows"
            )
            continue
        name = cells[name_idx] if len(cells) > name_idx else ""
        if (
            cells[status_idx] == "Covered"
            and re.search(r"SBOM|software bill of materials", name, re.IGNORECASE)
            and not re.search(
                r"^#{2,3}\s+Software Bill of Materials\s*$", text, re.MULTILINE
            )
        ):
            failures.append(
                f"coverage row '{name}' claims Covered but no Software Bill of "
                "Materials section exists - a module inventory is not an SBOM"
            )
    return failures


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


HUNT_SECTIONS = [
    "Document Information",
    "Audit Type Coverage",
    "Verdict",
    "System Context",
    "Methodology And Evidence",
    "Journey Traces",
    "Domain Findings",
    "Risk Register",
    "Remediation Phases",
    "Scope Exclusions",
    "Limitations and Unknowns",
    "Validation Record",
    "References",
]

HUNT_DOMAINS = (
    "Correctness",
    "Security",
    "Reliability",
    "Performance",
    "Dependencies",
    "Deployment",
    "Testability",
    "Documentation",
    "Maintainability",
    "Provenance",
)
HUNT_RATINGS = ("Red", "Amber", "Green", "Not assessed")
HUNT_VERDICTS = ("Ready", "Conditionally ready", "Not ready")
HUNT_GATE_RESULTS = ("Met", "Not met", "Not assessable")
HUNT_HOP_STATUS = ("conforming", "failing", "not assessable")
HUNT_MATCH_VALUES = ("conforming", "partially conforming", "failing", "not assessable")

REVIEW_SECTIONS = [
    "Document Information",
    "Audit Type Coverage",
    "Verdict",
    "System Context",
    "Check Plan And Methodology",
    "Execution Register",
    "Domain Findings",
    "Risk Register",
    "Improvement Plan",
    "Scope Exclusions",
    "Limitations and Unknowns",
    "Validation Record",
    "References",
]

REVIEW_RESULTS = ("PASS", "FAIL", "ERROR", "BLOCKED", "SKIPPED", "NOT RUN", "N/A")
REVIEW_EVIDENCE_LEVELS = ("Source", "Model", "App", "Deployed", "Unknown")
PROVENANCE_BASIS_VALUES = ("Declared", "Attested", "Supplied", "Indicated", "Undetermined")
REVIEW_DISPOSITIONS = ("Planned", "Deferred", "Accepted - no action", "Unresolved")


def tables_in(block: str) -> list[list[str]]:
    tables: list[list[str]] = []
    current: list[str] = []
    for line in block.split("\n"):
        if line.startswith("|"):
            current.append(line)
        elif current:
            tables.append(current)
            current = []
    if current:
        tables.append(current)
    return tables


def table_cells(table: list[str]) -> tuple[list[str], list[list[str]]]:
    header = [cell.strip() for cell in raw_cells(table[0])]
    rows = [
        [cell.strip() for cell in raw_cells(row)]
        for row in table[2:]
        if row.startswith("|")
    ]
    return header, rows


def check_hunt_ratings(text: str) -> list[str]:
    verdict = section_block(text, r"^##\s+Verdict\s*$")
    if not verdict:
        return []
    table = next(
        (
            candidate
            for candidate in tables_in(verdict)
            if {"Domain", "Rating"}
            <= {cell.strip() for cell in raw_cells(candidate[0])}
        ),
        None,
    )
    if table is None:
        return [
            "verdict section has no domain ratings table "
            "(expected header 'Domain | Rating | Basis')"
        ]
    header, rows = table_cells(table)
    rating_idx = header.index("Rating")
    basis_idx = header.index("Basis") if "Basis" in header else -1
    failures: list[str] = []
    seen: set[str] = set()
    for row in rows:
        if len(row) <= rating_idx or not row[0]:
            continue
        domain = row[0]
        seen.add(domain)
        rating = row[rating_idx]
        if rating not in HUNT_RATINGS:
            failures.append(
                f"domain '{domain}' has rating '{rating}' - "
                f"expected one of {'/'.join(HUNT_RATINGS)}"
            )
            continue
        basis = row[basis_idx] if 0 <= basis_idx < len(row) else ""
        if rating in ("Red", "Amber") and not re.search(r"FND-[A-Z]{3}-\d{3}", basis):
            failures.append(
                f"{rating} domain '{domain}' names no FND- finding in its Basis cell"
            )
    for domain in HUNT_DOMAINS:
        if domain not in seen:
            failures.append(f"domain ratings table lacks the fixed domain '{domain}'")
    return failures


def check_hunt_verdict(text: str) -> list[str]:
    verdict = section_block(text, r"^##\s+Verdict\s*$")
    if not verdict:
        return []
    failures: list[str] = []
    if not re.search(
        r"Verdict\s*[:*]*\s*\**(Conditionally ready|Not ready|Ready)\b", verdict
    ):
        failures.append(
            "verdict section states no verdict token - "
            "expected 'Verdict: Ready', 'Conditionally ready', or 'Not ready'"
        )
    gates = next(
        (
            candidate
            for candidate in tables_in(verdict)
            if {"Gate", "Result"}
            <= {cell.strip() for cell in raw_cells(candidate[0])}
        ),
        None,
    )
    if gates is None:
        failures.append(
            "verdict section has no hard-gates table "
            "(expected header 'Gate | Result | Basis')"
        )
    else:
        header, rows = table_cells(gates)
        result_idx = header.index("Result")
        for row in rows:
            if len(row) > result_idx and row[result_idx] \
                    and row[result_idx] not in HUNT_GATE_RESULTS:
                failures.append(
                    f"gate '{row[0][:50]}' has result '{row[result_idx]}' - "
                    f"expected {'/'.join(HUNT_GATE_RESULTS)}"
                )
    if not re.search(r"[Tt]op[- ]five", verdict):
        failures.append("verdict section lacks a top-five action list")
    elif not re.search(
        r"(?m)^\s*(?:\d+\.|[-*])\s+.*\b(REC-\d{3}|FND-[A-Z]{3}-\d{3})", verdict
    ):
        failures.append("top-five actions do not cite REC- or FND- identifiers")
    strengths = 0
    seen_marker = False
    for line in verdict.split("\n"):
        if re.match(r"^Strengths\b", line):
            seen_marker = True
            continue
        if not seen_marker:
            continue
        if re.match(r"^[-*]\s", line):
            strengths += 1
        elif re.match(r"^#{1,3}\s", line):
            break
    if strengths > 5:
        failures.append(f"verdict lists {strengths} strengths - the cap is five")
    return failures


def check_hunt_journeys(text: str) -> list[str]:
    block = section_block(text, r"^##\s+Journey Traces\s*$")
    if not block:
        return []
    failures: list[str] = []
    findings = set(re.findall(r"FND-[A-Z]{3}-\d{3}", text))
    hop_tables = 0
    for table in tables_in(block):
        if not table:
            continue
        header, rows = table_cells(table)
        if {"Hop", "Status"} <= set(header):
            hop_tables += 1
            status_idx = header.index("Status")
            for row in rows:
                if len(row) <= status_idx or not row[status_idx]:
                    continue
                status = row[status_idx].strip().lower()
                if status not in HUNT_HOP_STATUS:
                    failures.append(
                        f"journey hop '{row[0][:50]}' has status '{row[status_idx]}' - "
                        f"expected {'/'.join(HUNT_HOP_STATUS)}"
                    )
                    continue
                cited = re.findall(r"FND-[A-Z]{3}-\d{3}", " ".join(row))
                if status == "failing":
                    if not cited:
                        failures.append(
                            f"failing hop '{row[0][:50]}' cites no FND- finding"
                        )
                    for fid in cited:
                        if fid not in findings:
                            failures.append(
                                f"failing hop '{row[0][:50]}' cites undefined {fid}"
                            )
        elif "Representation match" in header:
            match_idx = header.index("Representation match")
            for row in rows:
                if len(row) > match_idx and row[match_idx]:
                    value = row[match_idx].strip().lower()
                    if value not in HUNT_MATCH_VALUES:
                        failures.append(
                            f"producer/consumer row '{row[0][:50]}' has match "
                            f"'{row[match_idx]}' - expected {'/'.join(HUNT_MATCH_VALUES)}"
                        )
    if hop_tables == 0:
        failures.append(
            "journey traces has no hop table (expected header 'Hop | Status | Evidence')"
        )
    return failures


DISPOSITION_SECTION = {
    "hunt": "Remediation Phases",
    "review": "Improvement Plan",
    "audit": "Actionable Remediation Roadmap",
}


def disposition_regions(text: str) -> list[tuple[str, str]]:
    """(owning ## heading, region text) pairs for the disposition sections.

    A roadmap/phase section at ### level lives inside a per-project ## block and
    cites bare FND ids, so each region records its enclosing ## heading.
    """
    level2 = [
        (match.start(), match.group(1).strip())
        for match in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)
    ]
    style = report_style(text)
    names = [DISPOSITION_SECTION.get(style, "Actionable Remediation Roadmap")]
    if style not in ("hunt", "review"):
        names.append("Recommendation Classification")
    regions: list[tuple[str, str]] = []
    for name in names:
        for match in re.finditer(
            rf"^#{{2,3}}\s+{re.escape(name)}\s*$", text, re.MULTILINE
        ):
            rest = text[match.end() :]
            end = re.search(r"^#{1,2}\s", rest, re.MULTILINE)
            region = rest[: end.start()] if end else rest
            owner = next(
                (title for position, title in reversed(level2) if position < match.start()),
                "",
            )
            regions.append((owner, region))
    return regions


def check_finding_disposition(text: str, lines: list[str]) -> list[str]:
    regions = disposition_regions(text)
    if not regions:
        return []
    qualified: set[str] = set()
    by_owner: dict[str, set[str]] = {}
    for owner, region in regions:
        found = re.findall(r"[\w.-]+::FND-[A-Z]{3}-\d{3}|FND-[A-Z]{3}-\d{3}", region)
        qualified.update(token for token in found if "::" in token)
        by_owner.setdefault(owner, set()).update(
            token.split("::")[-1] for token in found
        )
    failures: list[str] = []
    starts = [index for index, line in enumerate(lines) if line.startswith("### FND-")]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = NL.join(lines[start:end])
        status = field_value(block, "Status")
        if re.match(r"^(Closed|PASS)\b", status):
            continue
        fid = re.search(r"FND-[A-Z]{3}-\d{3}", lines[start]).group(0)
        qualifier = re.search(r"\(([\w.-]+)\)\s*$", lines[start])
        label = f"{qualifier.group(1)}::{fid}" if qualifier else fid
        covered = label in qualified
        if not covered and qualifier:
            covered = fid in by_owner.get(qualifier.group(1), set())
        if not covered and not qualifier:
            covered = any(fid in ids for ids in by_owner.values())
        if not covered:
            failures.append(
                f"finding {label} maps to no remediation entry and no "
                "'Accepted - no action' disposition"
            )
    return failures


def check_hunt_classification(text: str) -> list[str]:
    if re.search(r"^#{2,3}\s+Recommendation Classification\s*$", text, re.MULTILINE):
        return [
            "hunt report carries a Recommendation Classification section - "
            "disposition lives in Remediation Phases"
        ]
    return []


def check_review_classification(text: str) -> list[str]:
    if re.search(r"^#{2,3}\s+Recommendation Classification\s*$", text, re.MULTILINE):
        return [
            "review report carries a Recommendation Classification section - "
            "disposition lives in the Improvement Plan"
        ]
    return []


def check_review_execution_register(text: str) -> list[str]:
    block = section_block(text, r"^##\s+Execution Register\s*$")
    if not block:
        return []
    register = next(
        (
            candidate
            for candidate in tables_in(block)
            if {"Check", "Command", "Result"}
            <= {cell.strip() for cell in raw_cells(candidate[0])}
        ),
        None,
    )
    if register is None:
        return [
            "execution register has no check table "
            "(expected columns Check, Command, Result plus interpretation metadata)"
        ]
    header, rows = table_cells(register)
    result_idx = header.index("Result")
    interp_idx = header.index("Interpretation") if "Interpretation" in header else -1
    failures: list[str] = []
    for row in rows:
        if len(row) <= result_idx or not row[result_idx]:
            continue
        status = row[result_idx].strip()
        if status not in REVIEW_RESULTS:
            failures.append(
                f"check '{row[0][:50]}' has result '{status}' - "
                f"expected {'/'.join(REVIEW_RESULTS)}"
            )
            continue
        if status != "PASS" and (
            interp_idx < 0 or len(row) <= interp_idx or not row[interp_idx]
        ):
            failures.append(
                f"check '{row[0][:50]}' is {status} but states no Interpretation"
            )
    return failures


def check_hunt_scenarios(lines: list[str]) -> list[str]:
    failures: list[str] = []
    starts = [index for index, line in enumerate(lines) if line.startswith("### FND-")]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = NL.join(lines[start:end])
        severity = field_value(block, "Severity").split(" ")[0].upper()
        if severity not in ("HIGH", "CRITICAL"):
            continue
        if not field_value(block, "Defect scenario"):
            failures.append(
                f"{lines[start][4:70]}: {severity} finding lacks a Defect scenario - "
                "expected '* **Defect scenario:** <initial conditions; steps; expected; "
                "observed; confirmation level>'"
            )
    return failures


def check_review_dispositions(text: str) -> list[str]:
    block = section_block(text, r"^##\s+Improvement Plan\s*$")
    if not block:
        return []
    failures: list[str] = []
    for candidate in tables_in(block):
        header, rows = table_cells(candidate)
        if "Disposition" not in header:
            continue
        didx = header.index("Disposition")
        for row in rows:
            if len(row) <= didx or not row[didx]:
                continue
            value = row[didx].strip()
            if value not in REVIEW_DISPOSITIONS:
                failures.append(
                    f"disposition '{value}' is not one of {'/'.join(REVIEW_DISPOSITIONS)}"
                )
    return failures


def check_review_retest(text: str) -> list[str]:
    block = section_block(text, r"^##\s+Execution Register\s*$")
    if not block:
        return []
    failed: list[str] = []
    for candidate in tables_in(block):
        header, rows = table_cells(candidate)
        if {"Check", "Command", "Result"} <= set(header):
            result_idx = header.index("Result")
            for row in rows:
                if len(row) > result_idx and row[result_idx].strip() in (
                    "FAIL",
                    "ERROR",
                    "BLOCKED",
                ):
                    failed.append(row[0])
    if not failed:
        return []
    retest = section_block(text, r"^##\s+Retest Register\s*$")
    if not retest:
        return [
            f"execution register carries {len(failed)} FAIL/ERROR/BLOCKED row(s) "
            "but the report has no Retest Register"
        ]
    lowered = retest.lower()
    return [
        f"retest register does not cover failed check '{name[:60]}'"
        for name in failed
        if name.strip().lower() not in lowered
    ]


def check_review_evidence_levels(lines: list[str]) -> list[str]:
    failures: list[str] = []
    starts = [index for index, line in enumerate(lines) if line.startswith("### FND-")]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = NL.join(lines[start:end])
        name = lines[start][4:][:70]
        value = field_value(block, "Evidence level")
        if not value:
            failures.append(
                f"{name}: missing Evidence level - expected literal "
                "'* **Evidence level:** <Source | Model | App | Deployed | Unknown>'"
            )
            continue
        if value.split(" ")[0].capitalize() not in REVIEW_EVIDENCE_LEVELS:
            failures.append(
                f"{name}: Evidence level '{value[:60]}' is not one of "
                f"{'/'.join(REVIEW_EVIDENCE_LEVELS)}"
            )
    return failures


def check_aip_provenance(lines: list[str]) -> list[str]:
    """`Provenance basis` is required on FND-AIP- blocks and omitted elsewhere."""
    failures: list[str] = []
    starts = [index for index, line in enumerate(lines) if line.startswith("### FND-")]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = NL.join(lines[start:end])
        name = lines[start][4:][:70]
        value = field_value(block, "Provenance basis")
        if name.upper().startswith("FND-AIP-"):
            if not value:
                failures.append(
                    f"{name}: missing Provenance basis - expected literal "
                    "'* **Provenance basis:** <Declared / Attested / Supplied / "
                    "Indicated / Undetermined>'"
                )
            elif value.split(" ")[0].capitalize() not in PROVENANCE_BASIS_VALUES:
                failures.append(
                    f"{name}: Provenance basis '{value[:60]}' is not one of "
                    f"{'/'.join(PROVENANCE_BASIS_VALUES)}"
                )
        elif value:
            failures.append(
                f"{name}: Provenance basis is reserved for FND-AIP- blocks"
            )
    return failures


def check_risk_consistency(lines: list[str], fences: list[bool]) -> list[str]:
    failures: list[str] = []
    blocks: dict[str, list[str]] = {}
    starts = [index for index, line in enumerate(lines) if line.startswith("### RSK-")]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        rid = re.match(r"###\s+(RSK-\d+)", lines[start])
        if rid:
            blocks.setdefault(rid.group(1), []).append(NL.join(lines[start:end]))
    if not blocks:
        return []
    bands = {"low", "medium", "high", "critical"}
    for tstart, rows in table_blocks(lines, fences):
        if len(rows) < 2:
            continue
        header = [cell.strip() for cell in raw_cells(rows[0])]
        if not {"Severity", "Likelihood"} <= set(header):
            continue
        sev_idx = header.index("Severity")
        lik_idx = header.index("Likelihood")
        for row in rows[2:]:
            cells = [cell.strip() for cell in raw_cells(row)]
            rid = next(
                (
                    cell.split("::")[-1]
                    for cell in cells
                    if re.fullmatch(r"(?:[\w.-]+::)?RSK-\d{3}", cell)
                ),
                None,
            )
            if not rid or rid not in blocks:
                continue
            candidates = blocks[rid]
            for idx, field in ((sev_idx, "Severity"), (lik_idx, "Likelihood")):
                table_token = cells[idx].split(" ")[0].lower() if len(cells) > idx else ""
                if table_token not in bands:
                    continue
                # A bare RSK id can recur across per-project blocks, so flag only
                # when no block carrying the id supports the table cell.
                if not any(
                    field_value(block, field).split(" ")[0].lower() == table_token
                    for block in candidates
                ) and any(
                    field_value(block, field).split(" ")[0].lower() in bands
                    for block in candidates
                ):
                    failures.append(
                        f"{rid}: risk table {field} '{cells[idx]}' matches no "
                        f"{field} value in the {rid} block(s)"
                    )
    return failures


def check_executed_log(text: str) -> list[str]:
    block = section_block(text, r"^#{2,3}\s+Executed Evidence Log\s*$")
    if not block:
        return []
    failures: list[str] = []
    for candidate in tables_in(block):
        header, rows = table_cells(candidate)
        if "Result" not in header:
            continue
        result_idx = header.index("Result")
        for row in rows:
            if len(row) <= result_idx or not row[result_idx]:
                continue
            upper = row[result_idx].strip().upper()
            if not any(
                upper == token or upper.startswith(token + " ")
                for token in REVIEW_RESULTS
            ):
                failures.append(
                    f"executed log row '{row[0][:50]}' has result "
                    f"'{row[result_idx]}' - expected {'/'.join(REVIEW_RESULTS)}"
                )
    return failures


def report_style(text: str) -> str:
    match = re.search(r"\|\s*Report Style\s*\|\s*([^|]+)", text)
    return match.group(1).strip().lower() if match else "audit"


def evidence_mode(text: str) -> str:
    match = re.search(r"\|\s*Evidence Mode\s*\|\s*([^|]+)", text)
    return match.group(1).strip().lower() if match else "source-only"


def review_scope(text: str) -> str:
    match = re.search(r"\|\s*Review Scope\s*\|\s*([^|]+)", text)
    return match.group(1).strip().lower() if match else "full"


def check_snapshot_identity(text: str) -> list[str]:
    if "Document Information" not in text:
        return []
    failures: list[str] = []
    if not re.search(r"\|\s*Subject Revision\s*\|\s*\S", text):
        failures.append("Document Information lacks a Subject Revision snapshot anchor")
    if not re.search(r"\|\s*Report Style\s*\|", text):
        failures.append("Document Information lacks a Report Style row")
    if not re.search(r"\|\s*Evidence Mode\s*\|", text):
        failures.append("Document Information lacks an Evidence Mode row")
    return failures


def check_evidence_sections(text: str) -> list[str]:
    if "Document Information" not in text:
        return []
    if review_scope(text) == "structure":
        return []
    mode = evidence_mode(text)
    if mode in ("executed-readonly", "executed-commands"):
        if report_style(text) == "review":
            if not re.search(r"^#{2,3}\s+Artifact Manifest\s*$", text, re.MULTILINE):
                return ["executed review report has no Artifact Manifest section"]
            return []
        if not re.search(r"^#{2,3}\s+Executed Evidence Log\s*$", text, re.MULTILINE):
            return [f"{mode} report has no Executed Evidence Log section"]
        return []
    if mode not in ("source-only",):
        return [
            f"Evidence Mode '{mode}' is not a known mode - expected "
            "source-only, executed-readonly, or executed-commands"
        ]
    if not re.search(r"^#{2,3}\s+Operator Verification Handoff\s*$", text, re.MULTILINE):
        return ["source-only report has no Operator Verification Handoff section"]
    return []


def check_summary_verified(text: str) -> list[str]:
    failures: list[str] = []
    heading = findings_heading(text)
    for match in re.finditer(
        rf"^#{{2,3}}\s+{re.escape(heading)}\s*$", text, re.MULTILINE
    ):
        rest = text[match.end() :]
        end = re.search(r"^#{1,2}\s", rest, re.MULTILINE)
        block = rest[: end.start()] if end else rest
        details = {
            m.group(1): block[m.start() :]
            for m in re.finditer(r"^###\s+(FND-[A-Z]{3}-\d{3})", block, re.MULTILINE)
        }
        rows = block.split("\n")
        header_index = next(
            (i for i, line in enumerate(rows) if line.startswith("|") and "FND-" not in line),
            None,
        )
        if header_index is None:
            continue
        header = [cell.strip() for cell in raw_cells(rows[header_index])]
        if "Verification" not in header:
            continue
        vidx = header.index("Verification")
        for row in rows[header_index + 2 :]:
            if not row.startswith("|"):
                break
            cells = [cell.strip() for cell in raw_cells(row)]
            fid = next(
                (
                    cell.split("::")[-1]
                    for cell in cells
                    if re.fullmatch(r"(?:[\w.-]+::)?FND-[A-Z]{3}-\d{3}", cell)
                ),
                None,
            )
            if not fid or fid not in details:
                continue
            detail = details[fid]
            claimed = cells[vidx] if len(cells) > vidx else ""
            verified = field_value(detail, "Verified").lower()
            runtime = field_value(detail, "Runtime confirmed").lower()
            if claimed.startswith("Verified") and verified.startswith("no"):
                failures.append(f"{fid}: summary says Verified but block says Verified: no")
            if claimed.startswith("Confirmed") and not runtime.startswith("yes"):
                failures.append(f"{fid}: summary says Confirmed but block does not confirm it")
    return failures


def check_fresh_audit_claims(lines: list[str], fences: list[bool]) -> list[str]:
    text = NL.join(lines)
    if re.search(r"^#{2,3}\s+Changes Since Previous Audit\s*$", text, re.MULTILINE):
        return []
    failures: list[str] = []
    for index, (line, fenced) in enumerate(zip(lines, fences)):
        if fenced or re.search(r"parity baseline|industry baseline", line, re.IGNORECASE):
            continue
        if re.search(r"baseline|previous (audit|report|revision)", line, re.IGNORECASE) and re.search(
            r"better|improv|differ|regress|compar|since", line, re.IGNORECASE
        ):
            failures.append(
                f"line {index + 1}: comparative claim against a previous report in a fresh audit"
            )
    return failures


def check_roadmap_breaking(text: str) -> list[str]:
    if "**Breaking change:**" not in text:
        return []
    failures: list[str] = []
    for match in re.finditer(r"^#{2,3}\s+Actionable Remediation Roadmap\s*$", text, re.MULTILINE):
        rest = text[match.end() :]
        end = re.search(r"^#{1,2}\s", rest, re.MULTILINE)
        block = rest[: end.start()] if end else rest
        header = next(
            (line for line in block.split("\n") if line.startswith("|") and "Rec" in line),
            None,
        )
        if header is None:
            continue
        cells = [cell.strip() for cell in raw_cells(header)]
        if "Breaking" not in cells:
            failures.append("roadmap table lacks a Breaking column though findings assess it")
    return failures


PATH_LINE = re.compile(r"(?:[\w.\-]+/)*[\w.\-]+\.[A-Za-z]{1,6}:\d+(?:-\d+)?")


def check_evidence_paths(text: str, repo_root: str | None) -> list[str]:
    if repo_root is None:
        return []
    root = Path(repo_root).resolve()
    failures: list[str] = []
    seen: set[str] = set()
    for line in text.split("\n"):
        if "**Targets:**" not in line and "**Evidence:**" not in line:
            continue
        for citation in PATH_LINE.findall(line):
            if citation in seen:
                continue
            seen.add(citation)
            rel, _, span = citation.rpartition(":")
            first = int(span.split("-")[0])
            target = root / rel
            if not target.is_file():
                failures.append(f"evidence path does not exist: {citation}")
                continue
            with target.open(encoding="utf-8", errors="replace") as handle:
                total = sum(1 for _ in handle)
            if first > total:
                failures.append(f"evidence line {first} beyond file length {total}: {citation}")
            if len(failures) > 20:
                return failures
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


def report_contract() -> dict:
    """The mechanically enforced contract, generated from the live constants."""
    return {
        "schema": "lens-report-contract/1",
        "field_syntax": "* **Field:** value - asterisk bullet, bold name, colon outside the bold",
        "evidence_modes": ["source-only", "executed-readonly", "executed-commands"],
        "id_patterns": {
            "finding": "FND-<pillar>-NNN",
            "finding_pillars": list(FINDING_PILLARS),
            "project_qualified": "<project>::FND-<pillar>-NNN",
            "risk": "RSK-NNN",
            "recommendation": "REC-NNN",
        },
        "styles": {
            "audit": {
                "sections": BASELINE_SECTIONS + ["Recommendation Classification"],
                "brief_sections": sorted(BRIEF_SECTIONS),
                "findings_section": "Detailed Technical Findings",
                "recommendation_classification": "required at Standard/Detailed",
                "finding_disposition": "every open ### FND- block is cited in the "
                "roadmap/classification region or carries an explicit disposition",
            },
            "hunt": {
                "sections": HUNT_SECTIONS,
                "conditional_sections": [
                    "Glossary",
                    "Contradiction Register",
                    "Operator Verification Handoff",
                    "Executed Evidence Log",
                ],
                "findings_section": "Domain Findings",
                "domains": list(HUNT_DOMAINS),
                "ratings": list(HUNT_RATINGS),
                "verdicts": list(HUNT_VERDICTS),
                "gate_results": list(HUNT_GATE_RESULTS),
                "hop_status": list(HUNT_HOP_STATUS),
                "match_values": list(HUNT_MATCH_VALUES),
                "strengths_cap": 5,
                "defect_scenarios": "required on HIGH/CRITICAL findings",
                "recommendation_classification": "forbidden - disposition lives in Remediation Phases",
            },
            "review": {
                "sections": REVIEW_SECTIONS,
                "conditional_sections": [
                    "Glossary",
                    "Contradiction Register",
                    "Operator Verification Handoff",
                    "Artifact Manifest",
                    "Retest Register",
                    "Metrics Snapshot",
                    "Technical Debt Register",
                    "Re-audit And Follow-up Plan",
                    "Appendix <letter>: <title>",
                ],
                "findings_section": "Domain Findings",
                "domains": list(HUNT_DOMAINS),
                "ratings": list(HUNT_RATINGS),
                "verdicts": list(HUNT_VERDICTS),
                "gate_results": list(HUNT_GATE_RESULTS),
                "strengths_cap": 5,
                "execution_register": {
                    "required_columns": ["Check", "Command", "Result"],
                    "recommended_columns": [
                        "Cwd",
                        "Tool & Version",
                        "Timestamp",
                        "Input revision",
                        "Exit status",
                        "Interpretation",
                        "Artifact",
                    ],
                    "results": list(REVIEW_RESULTS),
                    "non_pass_requires_interpretation": True,
                },
                "evidence_levels": list(REVIEW_EVIDENCE_LEVELS),
                "retest_register": "required when the Execution Register carries "
                "FAIL/ERROR/BLOCKED rows - one row per failed check",
                "artifact_manifest": "required under executed-readonly/executed-commands",
                "dispositions": list(REVIEW_DISPOSITIONS),
                "recommendation_classification": "forbidden - disposition lives in the Improvement Plan",
                "structure_variant": {
                    "detection": "Review Scope row in Document Information reads Structure",
                    "sections": STRUCTURE_VARIANT_SECTIONS,
                },
            },
        },
        "fields": {
            "finding_required": [field.rstrip(":") for field in FINDING_REQUIRED],
            "risk_required": [field.rstrip(":") for field in RISK_REQUIRED],
            "legacy_forbidden": LEGACY_FIELDS,
            "aip_finding_required": ["Provenance basis"],
            "provenance_basis_exclusive_to": "FND-AIP-",
        },
        "tokens": {
            "finding_status": list(FINDING_STATUS),
            "change": list(CHANGE_VALUES),
            "risk_status": list(RISK_STATUS),
            "verification": list(VERIFICATION_QUALIFIERS),
            "absence": list(ABSENCE_VALUES),
            "breaking_change": ["None", "Internal", "Public API"],
            "applicability": ["applicable", "conditional", "inapplicable", "unverified"],
            "recommendation_class": ["Recommended", "Optional", "Not recommended"],
            "coverage_status": ["Covered", "Partially", "Not done"],
            "check_result": list(REVIEW_RESULTS),
            "evidence_level": list(REVIEW_EVIDENCE_LEVELS),
            "provenance_basis": list(PROVENANCE_BASIS_VALUES),
            "evidence_mode": ["source-only", "executed-readonly", "executed-commands"],
        },
        "tables": {
            "findings_summary_columns": [
                "Finding",
                "Result",
                "Status",
                "Change",
                "Verification",
            ],
            "evidence_ledger": "no Execution column, no legacy Evidence ID header, "
            "type tags Observation/Concern, Project column only in multi-project",
            "coverage": "Status cells must be Covered, Partially, or Not done",
        },
        "rules": [
            "headings no deeper than ###, followed by one blank line",
            "no semicolons in prose, no em/en dashes or Unicode arrows outside code",
            "scorecard means are recomputed from numeric Score cells; 'Overall score' "
            "rows belong to the Executive Summary table and must match the mean",
            "every stated overall score needs the word 'lowest' within six lines",
            "no ambiguous project labels ('both', 'either', 'the projects') in "
            "shared tables when a Project Inventory exists",
            "failing journey hops must cite a defined FND- identifier",
            "every open finding maps to a remediation entry or an "
            "'Accepted - no action'/'Deferred' disposition - Remediation Phases "
            "under hunt, Improvement Plan under review, roadmap/classification "
            "under audit",
            "risk table Severity/Likelihood cells must match the RSK- block fields",
            "a coverage row claiming SBOM/component-inventory Covered requires a "
            "Software Bill of Materials section - a module inventory is not an SBOM",
            "HIGH/CRITICAL hunt findings carry a Defect scenario field",
            "ERROR/BLOCKED are runner states, never product failures - NOT RUN "
            "is never a pass",
            "a model reproduction never upgrades app-level reachability",
            "Executed Evidence Log and Execution Register Result cells take the "
            "check-status vocabulary",
        ],
    }


def main(path: str, repo_root: str | None = None) -> int:
    text = Path(path).read_text(encoding="utf-8")
    lines = text.replace("\r\n", "\n").split("\n")
    fences = split_code(lines)
    kind = report_kind(path, text)
    checks = [
        ("headings", check_headings(lines, fences)),
        ("semicolons", check_semicolons(lines, fences)),
        ("non-ASCII dashes and arrows", check_dashes(lines, fences)),
        ("tables", check_tables(lines, fences)),
        ("location pattern", check_location(path)),
        ("trailing whitespace and ending", check_trailing(lines)),
    ]
    variant = ""
    if kind == "legacy":
        checks.append(
            (
                "legacy contract",
                [
                    "file follows the removed amendment-review contract - "
                    "that report type was deleted; regenerate it as a "
                    "review-style report per process/report-format/review-style.md"
                ],
            )
        )
    elif kind == "audit":
        style = report_style(text)
        variant = "structure" if style == "review" and review_scope(text) == "structure" else ""
        if variant:
            checks.extend(
                [
                    ("structure-variant sections", check_structure_variant_sections(text)),
                    ("FND cross-references", check_ids(text)),
                    ("finding-block fields", check_finding_blocks(lines)),
                    ("legacy field names", check_legacy_fields(lines, fences)),
                    ("Observation/Concern tags", check_type_tags(lines, fences)),
                    ("snapshot identity", check_snapshot_identity(text)),
                    ("evidence sections", check_evidence_sections(text)),
                    ("evidence paths", check_evidence_paths(text, repo_root)),
                    ("final-state gate", check_final_state(text)),
                ]
            )
        else:
            checks.extend(
                [
                    ("required sections", check_required_sections(text)),
                    ("coverage rows", check_coverage_rows(text)),
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
                    ("PAR-1..PAR-20", check_par_rows(text)),
                    ("recommendation classification", check_rec_classification(text)),
                    ("Observation/Concern tags", check_type_tags(lines, fences)),
                    ("snapshot identity", check_snapshot_identity(text)),
                    ("evidence sections", check_evidence_sections(text)),
                    ("summary verification labels", check_summary_verified(text)),
                    ("fresh-audit claims", check_fresh_audit_claims(lines, fences)),
                    ("roadmap breaking column", check_roadmap_breaking(text)),
                    ("evidence paths", check_evidence_paths(text, repo_root)),
                    ("glossary", check_glossary(text)),
                    ("final-state gate", check_final_state(text)),
                    ("risk detail consistency", check_risk_consistency(lines, fences)),
                    ("executed log vocabulary", check_executed_log(text)),
                ]
            )
            if style == "hunt":
                checks.extend(
                    [
                        ("hunt domain ratings", check_hunt_ratings(text)),
                        ("hunt verdict elements", check_hunt_verdict(text)),
                        ("hunt journey traces", check_hunt_journeys(text)),
                        ("hunt defect scenarios", check_hunt_scenarios(lines)),
                        ("hunt finding disposition", check_finding_disposition(text, lines)),
                        ("hunt classification ban", check_hunt_classification(text)),
                    ]
                )
            elif style == "review":
                checks.extend(
                    [
                        ("review verdict elements", check_hunt_verdict(text)),
                        ("review domain ratings", check_hunt_ratings(text)),
                        ("review execution register", check_review_execution_register(text)),
                        ("review evidence levels", check_review_evidence_levels(lines)),
                        ("review retest register", check_review_retest(text)),
                        ("review finding disposition", check_finding_disposition(text, lines)),
                        ("review dispositions", check_review_dispositions(text)),
                        ("review classification ban", check_review_classification(text)),
                    ]
                )
            elif style == "audit":
                checks.append(
                    ("audit finding disposition", check_finding_disposition(text, lines))
                )
            checks.append(("AIP provenance basis", check_aip_provenance(lines)))
    if kind == "audit":
        label = report_style(text)
        if variant:
            label = f"{label} ({variant})"
    else:
        label = kind
    print(f"report style: {label}")
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
    if sys.argv[1:] == ["--dump-contract"]:
        print(json.dumps(report_contract(), indent=2))
        raise SystemExit(0)
    if len(sys.argv) not in (2, 4) or (len(sys.argv) == 4 and sys.argv[2] != "--repo-root"):
        print("Usage: python validate-report.py <report.md> [--repo-root <dir>] | --dump-contract")
        raise SystemExit(1)
    raise SystemExit(main(sys.argv[1], sys.argv[3] if len(sys.argv) == 4 else None))
