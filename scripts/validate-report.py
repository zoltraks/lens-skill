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
    "Audit Coverage",
    "Executive Summary",
    "System Context",
    "Software Bill of Materials",
    "License Compliance",
    "Health Dashboard",
    "Delivery Practice & Team Continuity",
    "High-Level Observations",
    "Auditing Methodology",
    "Scoring Rubrics",
    "Architectural Assessment",
    "Structure Review",
    "Trade-off Analysis",
    "Strengths & What's Working",
    "Technical Findings",
    "Unified Risk Register",
    "Remediation Roadmap",
    "Scope Exclusions",
    "Limitations and Unknowns",
    "Validation Record",
    "References",
]
BRIEF_SECTIONS = {
    "Document Information",
    "Audit Coverage",
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


LINK_MARKUP = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")


def cell_text(cell: str) -> str:
    match = re.fullmatch(r"\[([^\]]+)\]\([^)]*\)", cell)
    return match.group(1) if match else cell


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
            if index > 0 and lines[index - 1].strip() != "":
                failures.append(f"line {index + 1}: heading is not preceded by one blank line")
    return failures


ID_RANGE = re.compile(r"\b[A-Z]{2,8}-[A-Z0-9-]*\d+\.\.")
ABBREV_TAIL = re.compile(
    r"(?:e\.g\.|i\.e\.|etc\.|vs\.|cf\.|ca\.|approx\.|U\.S\.|U\.K\.|"
    r"tj\.|np\.|itp\.|itd\.|m\.in\.|tzw\.|n\.bw\.|ang\.|por\.|zw\.|nr\.|"
    r"ok\.|im\.|prof\.|dr\.|inż\.|mgr\.|hab\.|płk\.|św\.)$"
)
SINGLE_INITIAL = re.compile(r"\b[A-ZĄĆĘŁŃÓŚŹŻ]\.$")
SENT_JOIN = re.compile(r"[.?!](?=\s+[A-ZĄĆĘŁŃÓŚŹŻ[(])")
NON_PROSE = re.compile(r"#{1,6}\s|\||[-*+]\s|\d+[.)]\s|>|<!--|\*\*")


def prose_line(line: str, fenced: bool) -> bool:
    # A prose paragraph line is flush-left and carries no markdown block
    # marker - list items, table rows, headings, quotes, comments, bold
    # run headings, and indented continuations are not prose.
    return bool(line.strip()) and not fenced and not (
        line[:1].isspace() or NON_PROSE.match(line)
    )


def sentence_breaks_on(text: str) -> bool:
    match = re.search(
        r"\|\s*Sentence breaks\s*\|\s*([^|]+)", text, re.IGNORECASE
    )
    return not (
        match and re.search(r"off|disabled|wyłącz", match.group(1), re.IGNORECASE)
    )


def check_sentence_breaks(
    lines: list[str], fences: list[bool], breaks_on: bool
) -> list[str]:
    failures: list[str] = []
    for index, (line, fenced) in enumerate(zip(lines, fences)):
        if fenced or not line.strip():
            continue
        value = strip_spans(line)
        collapsed = strip_spans(
            re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)
        )
        if ID_RANGE.search(collapsed):
            failures.append(
                f"line {index + 1}: identifier range written with '..' - cite each "
                f"register identifier individually: {line[:80]}"
            )
        if re.match(r"^#{1,3} ", line) or line.startswith("|"):
            continue
        # The raw tail decides what the reader sees: a trailing code span or
        # link means the prose did not end at an earlier period - a wrapped
        # quote-subject like `…`. `Option` / continues is a legal break.
        tail = line.rstrip()
        if re.search(r"[,;:]\.$", strip_spans(tail)):
            failures.append(f"line {index + 1}: doubled end mark: {line[:80]}")
        elif (
            tail.endswith(".")
            and not ABBREV_TAIL.search(tail)
            and not re.match(r"^\s*\d+\.$", tail)
            and index + 1 < len(lines)
        ):
            nxt = lines[index + 1]
            if (
                nxt.strip()
                and not fences[index + 1]
                and not re.match(r"^\s*(#{1,6}\s|\||[-*+]\s|>|```|<!--)", nxt)
            ):
                if nxt.lstrip()[:1].islower():
                    failures.append(
                        f"line {index + 1}: sentence split at line break (period "
                        f"then lowercase continuation): {line[:80]}"
                    )
                elif (
                    breaks_on
                    and prose_line(line, fenced)
                    and prose_line(nxt, fences[index + 1])
                ):
                    failures.append(
                        f"line {index + 1}: sentence boundary inside a paragraph - "
                        f"separate sentences with one blank line: {line[:80]}"
                    )
        if breaks_on and prose_line(line, fenced):
            for match in SENT_JOIN.finditer(collapsed):
                prefix = collapsed[: match.start() + 1]
                if ABBREV_TAIL.search(prefix) or SINGLE_INITIAL.search(prefix):
                    continue
                failures.append(
                    f"line {index + 1}: sentences joined in one line - each "
                    f"sentence is its own paragraph: {line[:80]}"
                )
                break
    return failures


def check_sentence_breaks_row(text: str) -> list[str]:
    match = re.search(r"\|\s*Sentence breaks\s*\|\s*([^|]+)", text, re.IGNORECASE)
    if match and not re.search(r"off|disabled|wyłącz", match.group(1), re.IGNORECASE):
        return [
            "Document Information has a Sentence breaks row that is not 'Off' - "
            "the row is written only when sentence-per-paragraph prose is "
            "explicitly suppressed"
        ]
    return []


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
        end = start + len(rows)
        if start > 0 and lines[start - 1].strip():
            failures.append(
                f"line {start + 1}: table is not preceded by a blank line"
            )
        if end < len(lines) and lines[end].strip():
            failures.append(
                f"line {end + 1}: table is not followed by a blank line"
            )
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
        for position, row in enumerate(rows[2:], start=2):
            cells = content_cells(row)
            if is_separator(cells):
                continue
            if len(cells) != len(header):
                failures.append(f"line {start + position + 1}: table column count differs from header")
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


def check_bold_markers(lines: list[str], fences: list[bool]) -> list[str]:
    failures: list[str] = []
    for index, (line, fenced) in enumerate(zip(lines, fences)):
        if fenced:
            continue
        if len(re.findall(r"\*\*", strip_spans(line))) % 2:
            failures.append(
                f"line {index + 1}: unbalanced '**' marker: {line[:80]}"
            )
        if re.match(r"^\*\*[^*]+\.\*\*\s*$", line):
            failures.append(
                f"line {index + 1}: bold pseudo-heading ends with a period: {line[:80]}"
            )
        if re.search(r"\d{4}-\d{2}-\d{2}\.\.\d{4}-\d{2}-\d{2}", line):
            failures.append(
                f"line {index + 1}: '..' range - use 'between X and Y' or 'X to Y': {line[:80]}"
            )
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
    "Targets:",
    "Basis:",
    "Criteria:",
    "Impact:",
    "Recommendation:",
    "Method:",
    "Confidence:",
    "Mitigating factors:",
    "Evidence:",
]
RISK_REQUIRED = [
    "Severity:",
    "Likelihood:",
    "Residual:",
    "Impact:",
    "Trigger:",
    "Controls:",
    "Mitigation:",
    "Closure:",
    "Source:",
    "Confidence:",
]
FINDING_STATUS = ("Open", "Closed", "Pass")
CHANGE_VALUES = ("New", "Unchanged", "Reopened", "Closed")
RISK_STATUS = ("Open", "Accepted", "Transferred", "Monitoring", "Closed")
VERIFICATION_QUALIFIERS = ("Verification", "Confirmed", "Reported")
FINDING_PILLARS = ("ARC", "CQY", "SEC", "INF", "AIP", "CPR", "API", "STR")
FINDING_ID = re.compile(r"FND-(?:ARC|CQY|SEC|INF|AIP|CPR|API|STR)-\d{3}")
ABSENCE_VALUES = ("No documented rationale", "Deliberate - recorded decision",
                  "Undetermined")
EMPTY_FIELD_VALUE = re.compile(r"^(N/?A|N/D|NOT SPECIFIED|NIEOKREŚLON)\b", re.IGNORECASE)


def field_value(block: str, field: str) -> str:
    match = re.search(rf"\*\*{re.escape(field)}:\*\*\s*(.*)", block)
    return match.group(1).strip() if match else ""


def field_token(value: str) -> str:
    """The leading vocabulary token of a field or cell value - a token and
    its qualifier join with a comma (`High, chain traced`)."""
    return value.split(",", 1)[0].split(" ")[0].strip()


def check_description_paragraphs(lines: list[str]) -> list[str]:
    failures: list[str] = []
    for index, line in enumerate(lines):
        if not re.match(r"^### (FND|RSK|REC|TDR)-", line):
            continue
        cursor = index + 1
        body: list[str] = []
        while cursor < len(lines) and not re.match(r"^\* \*\*", lines[cursor])                 and not lines[cursor].startswith("#"):
            body.append(lines[cursor])
            cursor += 1
        if not any(segment.strip() for segment in body):
            failures.append(
                f"{line[4:][:70]}: missing description paragraph after heading"
            )
    return failures


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
            failures.append(f"{name}: Status is not a lifecycle value (Open/Closed/Pass)")
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
        criterion = field_value(block, "Criteria")
        if EMPTY_FIELD_VALUE.match(criterion):
            failures.append(
                f"{name}: Criteria renders {criterion.split(' ')[0]} - name a declared "
                "criteria-table row instead"
            )
        verified = field_value(block, "Verification")
        if verified and re.match(r"^(yes|no)\b", verified, re.IGNORECASE):
            failures.append(f"{name}: Verification value must not start with yes or no")
        runtime = field_value(block, "Runtime")
        if runtime and re.match(r"^(yes|no|not applicable)\b", runtime, re.IGNORECASE):
            failures.append(
                f"{name}: Runtime value must not start with yes, no, or not applicable"
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


CRITERION_ID_SHAPE = re.compile(r"^[A-Z]{3}-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
CRITERION_REDUNDANT_ONE = re.compile(r"^([A-Z]{3}-[A-Z]+(?:-[A-Z]+)*)-(0?1)$")


def declared_criteria(lines: list[str]) -> tuple[list[str], list[str]]:
    criteria: list[str] = []
    heading_issues: list[str] = []
    for index, line in enumerate(lines):
        if re.match(
            r"(?:\*\*Criterion table\*\*|#{2,3}\s+Criterion table\s*$)",
            line,
        ):
            heading_issues.append(
                f"line {index + 1}: use '**Criteria table**' instead of 'Criterion table'"
            )
            continue
        if not re.match(
            r"(?:\*\*Criteria table\*\*|#{2,3}\s+Criteria table\s*$)",
            line,
            re.IGNORECASE,
        ):
            continue
        j = index + 1
        while j < len(lines) and not lines[j].lstrip().startswith("|"):
            if re.match(r"\*\*[^*]+\*\*", lines[j]) or lines[j].startswith("#"):
                break
            j += 1
        if j >= len(lines) or not lines[j].lstrip().startswith("|"):
            continue
        header = [cell.strip() for cell in lines[j].strip("|").split("|")]
        if not header or header[0].lower() != "criteria":
            continue
        j += 1
        if j < len(lines) and set(lines[j].strip()) <= set("|-: "):
            j += 1
        while j < len(lines) and lines[j].lstrip().startswith("|"):
            cell = lines[j].strip("|").split("|")[0].strip().strip("`")
            if cell and not cell.startswith("<"):
                criteria.append(cell)
            j += 1
    return criteria, heading_issues


def check_criterion_references(lines: list[str], style: str) -> list[str]:
    declared_list, failures = declared_criteria(lines)
    declared = set(declared_list)
    for cid in declared_list:
        if not CRITERION_ID_SHAPE.match(cid):
            failures.append(
                f"Criteria table: '{cid}' must use a three-letter uppercase prefix "
                "(e.g. TST-UNIT, MNT-COHES, DEP-BUILD, SCA-POOL, COM-DATA, DLY-HIST, SKL-PRES)"
            )
            continue
        one = CRITERION_REDUNDANT_ONE.match(cid)
        if one:
            stem = one.group(1)
            has_sibling = any(
                other != cid and other.startswith(stem + "-") for other in declared
            )
            if not has_sibling:
                failures.append(
                    f"Criteria table: '{cid}' has an unnecessary '-{one.group(2)}' suffix - "
                    f"use '{stem}' when no '{stem}-02' sibling exists"
                )
    starts = [index for index, line in enumerate(lines) if line.startswith("### FND-")]
    used = False
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = NL.join(lines[start:end])
        name = lines[start][4:][:70]
        value = field_value(block, "Criteria")
        if not value or value.startswith("<"):
            continue
        used = True
        token = re.split(r"\s+-\s+|,\s*", value, maxsplit=1)[0].strip()
        if declared and token not in declared:
            failures.append(
                f"{name}: Criteria '{token}' is not a declared criteria-table row"
            )
    if used and not declared and style == "audit":
        failures.append(
            "findings name criteria but no Criteria table is declared - "
            "add the Criteria table to Auditing Methodology per "
            "process/report-format/methodology-scoring.md"
        )
    return failures


def check_risk_blocks(lines: list[str]) -> list[str]:
    failures: list[str] = []
    starts = [index for index, line in enumerate(lines) if line.startswith("### RSK-")]
    fnd_blocks = {line[4:].split(":", 1)[0].strip()
                  for line in lines if line.startswith("### FND-")}
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
        source = field_value(block, "Source")
        if source and fnd_blocks:
            src = re.search(FINDING_ID, source)
            if not src or src.group(0) not in fnd_blocks:
                failures.append(f"{name}: Source does not name a defined finding")
    return failures


REC_REQUIRED = [
    "Priority:",
    "Finding:",
    "Condition:",
    "Impact:",
    "Effort:",
    "Complexity:",
    "Verification:",
]
TDR_REQUIRED = [
    "Category:",
    "Source:",
]
TDR_CATEGORIES = ("Reliability", "Performance Efficiency", "Security", "Maintainability")
TDR_STATUS = ("Open", "In progress", "Resolved")


def check_rec_blocks(lines: list[str]) -> list[str]:
    failures: list[str] = []
    starts = [index for index, line in enumerate(lines) if line.startswith("### REC-")]
    rec_ids = {lines[start].split(":", 1)[0][4:].strip() for start in starts}
    fnd_blocks = {line[4:].split(":", 1)[0].strip()
                  for line in lines if line.startswith("### FND-")}
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = NL.join(lines[start:end])
        name = lines[start][4:][:70]
        for field in REC_REQUIRED:
            if f"**{field}**" not in block:
                failures.append(
                    f"{name}: missing {field[:-1]} - expected literal "
                    f"'* **{field}** <value>'"
                )
        priority = field_value(block, "Priority")
        if priority and not re.match(r"^P[1-4]\b", priority):
            failures.append(f"{name}: Priority is not P1-P4")
        finding = field_value(block, "Finding")
        if finding:
            ref = re.search(FINDING_ID, finding)
            if not ref or ref.group(0) not in fnd_blocks:
                failures.append(f"{name}: Finding does not name a defined finding")
        depends = field_value(block, "Depends on")
        if depends and not re.match(r"^none\b", depends, re.IGNORECASE):
            for ref in re.findall(r"REC-\d{3}", depends):
                if ref not in rec_ids:
                    failures.append(f"{name}: Depends on cites undefined {ref}")
    return failures


def check_tdr_blocks(lines: list[str]) -> list[str]:
    failures: list[str] = []
    starts = [index for index, line in enumerate(lines) if line.startswith("### TDR-")]
    fnd_blocks = {line[4:].split(":", 1)[0].strip()
                  for line in lines if line.startswith("### FND-")}
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = NL.join(lines[start:end])
        name = lines[start][4:][:70]
        for field in TDR_REQUIRED:
            if f"**{field}**" not in block:
                failures.append(
                    f"{name}: missing {field[:-1]} - expected literal "
                    f"'* **{field}** <value>'"
                )
        category = field_value(block, "Category")
        if category and not re.match(rf"^({'|'.join(TDR_CATEGORIES)})\b", category):
            failures.append(f"{name}: Category is not a CISQ characteristic")
        status = field_value(block, "Status")
        if status and not re.match(rf"^({'|'.join(TDR_STATUS)})\b", status):
            failures.append(f"{name}: Status is not Open/In progress/Resolved")
        source = field_value(block, "Source")
        if source and not source.startswith("Direct observation"):
            ref = re.search(FINDING_ID, source)
            if not ref or ref.group(0) not in fnd_blocks:
                failures.append(f"{name}: Source is not a finding or Direct observation")
    return failures


SCORE_INTERVAL = re.compile(
    r"(\d+(?:\.\d+)?)/(\d+)\s*\[(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)\]"
)


def check_scorecard_interval(text: str) -> list[str]:
    failures: list[str] = []
    for match in SCORE_INTERVAL.finditer(text):
        score, denom, lo, hi = (
            float(match.group(1)), float(match.group(2)),
            float(match.group(3)), float(match.group(4)),
        )
        label = match.group(0)
        if lo >= hi:
            failures.append(
                f"interval {label} is degenerate - omit the brackets when lo equals hi"
            )
        elif not lo <= score <= hi:
            failures.append(
                f"interval {label} does not contain its point score"
            )
        if denom and (lo < 0 or hi > denom):
            failures.append(f"interval {label} falls outside the 0-{int(denom)} scale")
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
    return "Technical Findings"


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
    for wanted in ("Finding", "Result", "Status", "Change"):
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
            if value and field_token(value) not in FINDING_STATUS:
                failures.append(
                    f"findings summary row has non-lifecycle Status '{value}' - "
                    "expected Open/Closed/Pass"
                )
        if change_idx >= 0 and len(row_cells) > change_idx:
            value = row_cells[change_idx]
            if value and field_token(value) not in CHANGE_VALUES:
                failures.append(
                    f"findings summary row has non-provenance Change '{value}' - "
                    "expected New/Unchanged/Reopened/Closed"
                )
        if verification_idx >= 0 and len(row_cells) > verification_idx:
            value = row_cells[verification_idx]
            if value and field_token(value) not in VERIFICATION_QUALIFIERS:
                failures.append(
                    f"findings summary row has bad Verification '{value}' - "
                    "expected Verification/Confirmed/Reported or empty"
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


SCORECARD_MARKER = re.compile(
    r"(?:^#{1,4}\s+Scorecard Summary\s*$|\*\*Scorecard Summary\*\*)",
    re.MULTILINE,
)


def check_scorecard_mean(text: str) -> list[str]:
    failures: list[str] = []
    summaries: list[tuple[float, int]] = []
    for marker in SCORECARD_MARKER.finditer(text):
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
            elif "★" in cells[score_idx]:
                values.append(cells[score_idx].count("★") / 5)
        if values:
            summaries.append((sum(values) / len(values), len(values)))
    overalls: list[tuple[float, int]] = []
    for line in text.split("\n"):
        if line.startswith("|"):
            cells = [cell.strip() for cell in raw_cells(line)]
            if len(cells) >= 2 and cells[0].strip("*") == "Overall score":
                pairs = SCORE_PAIR.findall(cells[1])
                if pairs:
                    num, denom = float(pairs[-1][0]), float(pairs[-1][1])
                    if denom:
                        overalls.append((num / denom, int(denom)))
        else:
            paragraph = re.search(
                r"^Overall:\s*.*?(\d+(?:\.\d+)?)/(\d+)", strip_spans(line)
            )
            if paragraph:
                num, denom = float(paragraph.group(1)), int(paragraph.group(2))
                if denom:
                    overalls.append((num / denom, denom))
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
    ledger = section_block(text, r"Evidence List")
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
    marker = SCORECARD_MARKER.search(text)
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
                and not re.search(r"CWE-[0-9]+|\bUnknown\b|\bNIEZNANE\b", match.group(1)):
            failures.append(f"{lines[start][4:70]}: security classification lacks CWE or an unknown token")
        if "**Pillar:** Security & Compliance" not in block:
            continue
        severity = re.search(r"\* \*\*Severity:\*\*\s*(.*)", block)
        narrative = re.search(r"\* \*\*Exploitability:\*\*\s*(.*)", block)
        if severity and narrative and re.search(r"\b(critical|high|krytyczna|wysoka)\b", severity.group(1), re.IGNORECASE):
            if re.fullmatch(r"N/?A|N/D", narrative.group(1).strip()):
                failures.append(f"{lines[start][4:70]}: Critical/High security finding's exploitability narrative is bare N/A without a reason")
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


PAR_RESULTS = ("Applied", "Pass", "N/A")


def check_par_rows(text: str) -> list[str]:
    failures: list[str] = []
    for number in range(1, 28):
        if not re.search(rf"^\|\s*PAR-{number}(?:\s|\||:)", text, re.MULTILINE):
            failures.append(f"missing Validation Record row PAR-{number}")
    for match in re.finditer(r"^\|\s*PAR-\d+\s*\|\s*([^|]*)\|", text, re.MULTILINE):
        result = cell_text(match.group(1).strip())
        if result and not result.startswith("<") and result not in PAR_RESULTS:
            failures.append(
                f"Validation Record row has non-check result '{result}' - "
                f"expected {'/'.join(PAR_RESULTS)}"
            )
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
        base = re.sub(r"[^\w -]", "", match.group(1).lower()).replace(" ", "-")
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

# Mapped validation copies still carry Polish prose - Polish function words
# join the exemption set so a translated report's `Każde [FND](#fnd)` does
# not read as a capitalized compound name. Keep in sync with the
# `_PL` set in `scripts/link-glossary.py`.
COMPOUND_NEIGHBOR_STOPWORDS |= {
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


def _compound_word(token: str, trailing: bool) -> str:
    link = re.fullmatch(r"\[([^\]]+)\]\([^)]*\)", token)
    if link:
        return link.group(1)
    if trailing:
        return re.sub(r"[^\w]+$", "", token)
    return re.sub(r"^[^\w]+", "", token)


def _capitalized_word(token: str) -> bool:
    """Unicode-aware `[A-Z][A-Za-z0-9]*` - mapped validation copies still
    carry Polish diacritics, so `Zgodność API` must read as a compound."""
    return bool(
        re.fullmatch(r"[^\W\d_][^\W_]*(?:\.[^\W_]+)*", token)
        and token[0].isupper()
    )


FIELD_VALUE_LABELS = (
    "Pillar",
    "Severity",
    "Type",
    "Security",
    "Status",
    "Change",
    "Absence",
    "Verification",
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
    return re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-")


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
    failures.extend(check_glossary_triplets(text, text[heading.end() : g_end]))
    failures.extend(check_glossary_body_links(text, terms, sub_slugs))
    return failures


REGISTER_TRIPLETS = ("FND", "EVD", "TDR", "RSK", "REC", "PAR")


def check_glossary_triplets(text: str, glossary_block: str) -> list[str]:
    if not re.search(r"\|\s*Detail Level\s*\|\s*Detailed\b", text, re.IGNORECASE):
        return []
    declared_crit, _ = declared_criteria(text.split("\n"))
    crit_prefixes = [
        cid.split("-", 1)[0]
        for cid in declared_crit
        if re.match(r"^[A-Z]{3}-", cid)
    ]
    fnd_pillars = re.findall(r"^###\s+FND-([A-Z]{3})-\d{3}\b", text, re.MULTILINE)
    if not crit_prefixes and not fnd_pillars:
        return []
    triplet_table = None
    for tbl in tables_in(glossary_block):
        hdr, rows = table_cells(tbl)
        if hdr and cell_text(hdr[0]).strip().lower() == "triplet":
            triplet_table = rows
            break
    if triplet_table is None:
        return [
            "Detailed report with a Glossary is missing the '**Identifier triplets**' "
            "table (Triplet | Scope | Description)"
        ]
    failures: list[str] = []
    triplets: list[str] = []
    for row in triplet_table:
        if not row:
            continue
        code = cell_text(row[0]).strip().strip("`")
        if not re.fullmatch(r"[A-Z]{3}", code):
            failures.append(
                f"Glossary Identifier triplets row '{code}' is not a three-letter uppercase code"
            )
            continue
        triplets.append(code)
    if len(triplets) != len(set(triplets)):
        failures.append("Glossary Identifier triplets table has duplicate rows")
    if triplets[:2] != ["FND", "EVD"]:
        failures.append(
            "Glossary Identifier triplets table must start with 'FND' then 'EVD'"
        )
    needed_registers = ["FND", "EVD"]
    for reg in ("TDR", "RSK", "REC", "PAR"):
        if re.search(rf"\b{reg}-\d+\b", text):
            needed_registers.append(reg)
    needed_criteria: list[str] = []
    for code in crit_prefixes + fnd_pillars:
        if code not in needed_registers and code not in needed_criteria:
            needed_criteria.append(code)
    for code in needed_registers + needed_criteria:
        if code not in triplets:
            failures.append(
                f"Glossary Identifier triplets table is missing '{code}'"
            )
    reg_positions = [triplets.index(r) for r in needed_registers if r in triplets]
    crit_positions = [triplets.index(c) for c in needed_criteria if c in triplets]
    if reg_positions and crit_positions and max(reg_positions) > min(crit_positions):
        failures.append(
            "Glossary Identifier triplets table must list register triplets "
            "(FND, EVD, ...) before criteria/pillar triplets"
        )
    return failures


def check_glossary_body_links(text: str, terms: list[str], sub_slugs: dict[str, str]) -> list[str]:
    section_names = set(re.findall(r"^##\s+(.+?)\s*$", text, re.MULTILINE))
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
            if link_text in section_names:
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


REF_TOKEN = (
    r"(?:[\w][\w.-]*::)?"
    r"(?:FND-(?:ARC|CQY|SEC|INF|AIP|CPR|API|STR)-\d{3}"
    r"|EVD-\d{3}|RSK-\d{3}|REC-\d{3}|TDR-\d{3}|PAR-\d+)"
)
REF_PATTERN = re.compile(REF_TOKEN)
REF_LINK = re.compile(r"\[(" + REF_TOKEN + r")\]\(#([^)]+)\)")
REF_BLOCK_HEADING = re.compile(
    r"^#{3,6}\s+((?:FND-(?:ARC|CQY|SEC|INF|AIP|CPR|API|STR)|RSK|REC|TDR)-\d{3})\s*:"
)
REF_PROJECT_SUFFIX = re.compile(r"\(([^()]+)\)\s*$")


REF_ROW_TOKEN = re.compile(r"(?:[\w][\w.-]*::)?(?:EVD-\d{3}|PAR-\d+)")


def defining_row_id(line: str) -> tuple[str, int]:
    """Return (identifier, second-pipe index) when the row's first cell is
    exactly one row-defined register identifier (EVD or PAR)."""
    second_pipe = line.find("|", 1)
    if second_pipe < 0:
        return "", -1
    text = cell_text(line[1:second_pipe].strip())
    if not REF_ROW_TOKEN.fullmatch(text):
        return "", -1
    return text, second_pipe


def register_definitions(
    lines: list[str], fences: list[bool]
) -> tuple[dict[str, list[str]], set[str], dict[str, str]]:
    """Return (block ID -> heading slugs, row-defined IDs, family -> section
    slug) collected from the report's own register definitions."""
    blocks: dict[str, list[str]] = {}
    row_ids: set[str] = set()
    section: dict[str, str] = {}
    counts: dict[str, int] = {}
    last_slug = ""
    for line, fenced in zip(lines, fences):
        if fenced:
            continue
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading:
            base = slugify(heading.group(2))
            seen = counts.get(base, 0)
            counts[base] = seen + 1
            last_slug = base if seen == 0 else f"{base}-{seen}"
            block = REF_BLOCK_HEADING.match(line)
            if block:
                blocks.setdefault(block.group(1), []).append(last_slug)
            continue
        if line.startswith("|"):
            token, _ = defining_row_id(line)
            bare = token.rsplit("::", 1)[-1]
            family = next(
                (f for f in ("EVD", "PAR") if bare.startswith(f + "-")), None
            )
            if family:
                row_ids.add(bare)
                if family not in section and last_slug:
                    section[family] = last_slug
    return blocks, row_ids, section


def check_reference_links(
    lines: list[str], fences: list[bool], text: str
) -> list[str]:
    failures: list[str] = []
    blocks, row_ids, section = register_definitions(lines, fences)
    slugs = heading_slugs(text)
    for index, (line, fenced) in enumerate(zip(lines, fences)):
        if fenced or re.match(r"^#{1,6}\s", line):
            continue
        lineno = index + 1
        for link in REF_LINK.finditer(line):
            token, anchor = link.group(1), link.group(2)
            bare = token.rsplit("::", 1)[-1]
            if bare.startswith(("EVD-", "PAR-")):
                family = "EVD" if bare.startswith("EVD-") else "PAR"
                expected = section.get(family)
                if expected is not None and anchor != expected:
                    failures.append(
                        f"line {lineno}: [{token}](#{anchor}) should link to "
                        f"#{expected}"
                    )
                elif expected is None and anchor not in slugs:
                    failures.append(
                        f"line {lineno}: [{token}](#{anchor}) links to a "
                        "missing anchor"
                    )
            else:
                candidates = blocks.get(bare, [])
                if anchor not in slugs:
                    failures.append(
                        f"line {lineno}: [{token}](#{anchor}) links to a "
                        "missing anchor"
                    )
                elif candidates and anchor not in candidates:
                    failures.append(
                        f"line {lineno}: [{token}](#{anchor}) does not point "
                        f"at a ### {bare}: heading"
                    )
        masked = re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line)
        masked = LINK_MARKUP.sub(lambda m: " " * len(m.group(0)), masked)
        masked = re.sub(r"https?://\S+", lambda m: " " * len(m.group(0)), masked)
        masked = re.sub(r"\[[^\]]*\]", lambda m: " " * len(m.group(0)), masked)
        first, cell_end = (
            defining_row_id(line) if line.startswith("|") else ("", -1)
        )
        for match in REF_PATTERN.finditer(masked):
            start, end = match.start(), match.end()
            before = masked[start - 1] if start else " "
            after = masked[end] if end < len(masked) else " "
            if re.match(r"[\w/#.:-]", before) or re.match(r"[\w/-]", after):
                continue
            token = match.group(0)
            bare = token.rsplit("::", 1)[-1]
            if first and bare == first.rsplit("::", 1)[-1] and start < cell_end:
                continue
            if bare in blocks:
                hint = (
                    " - ambiguous across projects, qualify it as "
                    "<project>::" + bare
                    if len(blocks[bare]) > 1
                    else ""
                )
                failures.append(
                    f"line {lineno}: unlinked register reference {token}{hint}"
                )
            elif bare in row_ids:
                failures.append(
                    f"line {lineno}: unlinked register reference {token}"
                )
            else:
                failures.append(
                    f"line {lineno}: {token} cites an undefined register "
                    "identifier"
                )
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


def heading_depth(match: re.Match) -> int:
    return len(match.group(0)) - len(match.group(0).lstrip("#"))


def section_end(rest: str, depth: int, skip_registers: bool = False) -> int:
    """Offset where a section ends inside `rest` - the next heading of the
    same or shallower depth, so a `###` section inside a multi-project
    `##` block stops at its sibling `###` headings instead of running
    into the next project. `skip_registers` keeps `### FND-`/`RSK-`/
    `REC-`/`TDR-` register-item headings inside their parent section."""
    pattern = rf"^#{{1,{depth}}}\s+"
    if skip_registers:
        pattern += r"(?!(?:FND|RSK|REC|TDR)-)"
    match = re.search(pattern, rest, re.MULTILINE)
    return match.start() if match else len(rest)


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
STRUCTURE_VERDICT_AREAS = (
    "Directory organization",
    "Naming conventions",
    "Component placement",
    "Supporting-artifact layout",
    "Consistency",
)
CONFORMANCE_STATUS_TOKENS = {"Pass", "Partial", "Fail", "Unknown", "N/A"}
CONFORMANCE_VERDICT_TOKENS = {"Passed", "Partially", "Failed"}


def check_structure_and_naming(text: str) -> list[str]:
    if re.search(r"\|\s*Detail Level\s*\|\s*Brief\b", text, re.IGNORECASE):
        return []
    failures: list[str] = []
    for match in re.finditer(r"^#{2,3}\s+Structure Review\s*$", text, re.MULTILINE):
        rest = text[match.end() :]
        block = rest[: section_end(rest, heading_depth(match))]
        verdict_rows: dict[str, str] = {}
        for table in tables_in(block):
            header, rows = table_cells(table)
            if len(header) >= 2 and header[0] == "Area" and header[1] == "Verdict":
                for row in rows:
                    if len(row) >= 2:
                        verdict_rows[cell_text(row[0]).strip()] = cell_text(row[1]).strip()
        if not verdict_rows:
            failures.append(
                "Structure Review is missing the Area | Verdict | Basis table"
            )
        else:
            for area in STRUCTURE_VERDICT_AREAS:
                if area not in verdict_rows:
                    failures.append(
                        f"Structure Review verdict table is missing row '{area}'"
                    )
                elif verdict_rows[area] not in CONFORMANCE_VERDICT_TOKENS:
                    failures.append(
                        f"Structure Review '{area}' verdict '{verdict_rows[area]}' "
                        f"is not in {sorted(CONFORMANCE_VERDICT_TOKENS)}"
                    )
    for match in re.finditer(
        r"^#{2,3}\s+Structure Conformance\s*$", text, re.MULTILINE
    ):
        rest = text[match.end() :]
        block = rest[: section_end(rest, heading_depth(match))]
        status_tables = 0
        for table in tables_in(block):
            header, rows = table_cells(table)
            if "Status" not in header:
                continue
            status_tables += 1
            sidx = header.index("Status")
            for row in rows:
                if len(row) > sidx:
                    token = cell_text(row[sidx]).strip()
                    if token not in CONFORMANCE_STATUS_TOKENS:
                        failures.append(
                            f"Structure Conformance status '{token}' "
                            f"is not in {sorted(CONFORMANCE_STATUS_TOKENS)}"
                        )
        if status_tables == 0:
            failures.append(
                "Structure Conformance has no conformance table with a Status column"
            )
    for match in re.finditer(r"^#{2,3}\s+Code Style\s*$", text, re.MULTILINE):
        rest = text[match.end() :]
        block = rest[: section_end(rest, heading_depth(match))]
        status_tables = 0
        for table in tables_in(block):
            header, rows = table_cells(table)
            if "Status" not in header:
                continue
            status_tables += 1
            sidx = header.index("Status")
            for row in rows:
                if len(row) > sidx:
                    token = cell_text(row[sidx]).strip()
                    if token not in CONFORMANCE_STATUS_TOKENS:
                        failures.append(
                            f"Code Style status '{token}' "
                            f"is not in {sorted(CONFORMANCE_STATUS_TOKENS)}"
                        )
        if status_tables == 0:
            failures.append(
                "Code Style has no sub-score or lens table with a Status column"
            )
    return failures


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


REFERENCE_PATH_EXT = re.compile(
    r"\.(?:adoc|bat|c|cc|cfg|cmd|conf|cpp|cs|csproj|csv|go|gradle|h|hpp|ini|java|"
    r"js|json|jsx|kt|lock|md|markdown|mod|php|properties|ps1|py|rb|rs|rst|sh|sln|"
    r"sql|sum|toml|ts|tsx|txt|xml|ya?ml)$",
    re.IGNORECASE,
)
REFERENCE_PATH_NAMES = {
    "codeowners", "containerfile", "dockerfile", "gemfile", "jenkinsfile",
    "justfile", "license", "makefile", "notice", "pipfile", "procfile",
    "rakefile", "taskfile", "vagrantfile",
}


def check_references_section(text: str) -> list[str]:
    match = re.search(r"^##\s+References\s*$", text, re.MULTILINE)
    if not match:
        return []
    failures: list[str] = []
    if re.search(r"^##\s+\S", text[match.end() :], re.MULTILINE):
        failures.append("References is not the final section of the report")
    block = text[match.end() :]
    end = re.search(r"^##\s+", block, re.MULTILINE)
    if end:
        block = block[: end.start()]
    is_draft = bool(re.search(r"\|\s*State\s*\|\s*Draft\b", text))
    if (
        not re.search(r"\]\(https?://", block)
        and not re.search(r"No external sources consulted|No public URL", block)
        and not (is_draft and re.search(r"\]\(<url>\)", block))
    ):
        failures.append(
            "References section carries no external link or declared absence - "
            "each row renders a [title](url) link paragraph, `No public URL` "
            "marks an unlinked source, `No external sources consulted` replaces "
            "the table"
        )
    for table in tables_in(block):
        header, rows = table_cells(table)
        if not header or header[0] != "Reference":
            continue
        for cells in rows:
            if not cells:
                continue
            first = cells[0]
            inner = first[1:-1] if first.startswith("`") and first.endswith("`") else ""
            base = first.rsplit("/", 1)[-1].rstrip("/*}").lower()
            looks_path = base in REFERENCE_PATH_NAMES
            if inner:
                looks_path = looks_path or (
                    REFERENCE_PATH_EXT.search(inner) is not None
                    or "{" in inner
                    or "*" in inner
                    or inner.endswith("/")
                    or (
                        "/" in inner
                        and re.fullmatch(r"[\w.\-]+(?:/[\w.\-{}*]+)+/?", inner)
                        is not None
                    )
                )
            if looks_path:
                failures.append(
                    f"References row '{first}' looks like a repository path - "
                    "the section lists external authoritative sources, internal "
                    "artifacts belong to the evidence ledger"
                )
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
    start = re.search(r"^##\s+Audit Coverage\s*$", text, re.MULTILINE)
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
                "expected Covered, Partially, or Not done - the taxonomy vocabulary "
                "is uppercase, but Status cells render title case like every other "
                "report vocabulary, and NOT APPLICABLE rows are omitted"
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
            cells = raw_cells(line)
            # Only the row's Rec cell counts - citing another REC in a
            # text cell such as Basis is not a second classification.
            if cells:
                classified += re.findall(r"REC-\d{3}", cells[0])
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


MATURITY_LEVELS = (
    "Prototype",
    "Early development",
    "Pre-production",
    "Production-ready",
    "Undetermined",
)
EXEC_SUMMARY_FIELDS = (
    "System type",
    "Scope",
    "Source basis",
    "Maturity level",
    "Overall score",
)


def check_executive_summary(text: str) -> list[str]:
    """The audit Executive Summary opens with the Field/Value key-value table
    from summary-changes.md. A multi-project report's combined `## Executive
    Summary` carries the per-project table instead, so a first table with a
    `Project` column exempts that one section."""
    if "Document Information" not in text or report_style(text) != "audit":
        return []
    failures: list[str] = []
    for match in re.finditer(r"^(#{2,3})\s+Executive Summary\s*$", text, re.MULTILINE):
        level = len(match.group(1))
        rest = text[match.end() :]
        following = re.search(rf"^#{{1,{level}}}\s", rest, re.MULTILINE)
        block = rest[: following.start()] if following else rest
        tables = tables_in(block)
        if tables:
            header = [cell.strip() for cell in raw_cells(tables[0][0])]
            if "Project" in header:
                continue
        kv = None
        for table in tables:
            header = [cell.strip() for cell in raw_cells(table[0])]
            if header[:2] == ["Field", "Value"]:
                kv = table
                break
        if kv is None:
            failures.append(
                "Executive Summary lacks the required Field/Value key-value table "
                "(System type, Scope, Source basis, Maturity level, Overall score)"
            )
            continue
        fields = {}
        for row in kv[2:]:
            cells = [cell.strip() for cell in raw_cells(row)]
            if len(cells) >= 2:
                fields[cells[0]] = cells[1]
        for wanted in EXEC_SUMMARY_FIELDS:
            if wanted not in fields:
                failures.append(f"Executive Summary table lacks the {wanted} row")
        level_value = fields.get("Maturity level", "")
        if level_value:
            clean = cell_text(level_value).strip().strip("`")
            if not clean.startswith("<") and clean not in MATURITY_LEVELS:
                failures.append(
                    f"Maturity level '{level_value}' is not one of "
                    f"{'/'.join(MATURITY_LEVELS)}"
                )
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
    "Audit Coverage",
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
    "Audit Coverage",
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

REVIEW_RESULTS = ("Pass", "Fail", "Error", "Blocked", "Skipped", "Not run", "N/A")
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
    "audit": "Remediation Roadmap",
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
    names = [DISPOSITION_SECTION.get(style, "Remediation Roadmap")]
    if style not in ("hunt", "review"):
        names.append("Recommendation Classification")
    regions: list[tuple[str, str]] = []
    for name in names:
        for match in re.finditer(
            rf"^#{{2,3}}\s+{re.escape(name)}\s*$", text, re.MULTILINE
        ):
            rest = text[match.end() :]
            region = rest[
                : section_end(rest, heading_depth(match), skip_registers=True)
            ]
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
        if re.match(r"^(Closed|Pass)\b", status):
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
        if status != "Pass" and (
            interp_idx < 0 or len(row) <= interp_idx or not row[interp_idx]
        ):
            failures.append(
                f"check '{row[0][:50]}' is {status} but states no Interpretation"
            )
    return failures


def check_hunt_scenarios(lines: list[str]) -> list[str]:
    """Defect scenario is required on High/Critical findings under the
    `audit` and `hunt` report styles - the call site gates on style."""
    failures: list[str] = []
    starts = [index for index, line in enumerate(lines) if line.startswith("### FND-")]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = NL.join(lines[start:end])
        severity = field_token(field_value(block, "Severity"))
        if severity.lower() not in ("high", "critical"):
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
                    "Fail",
                    "Error",
                    "Blocked",
                ):
                    failed.append(row[0])
    if not failed:
        return []
    retest = section_block(text, r"^##\s+Retest Register\s*$")
    if not retest:
        return [
            f"execution register carries {len(failed)} Fail/Error/Blocked row(s) "
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
        if field_token(value).capitalize() not in REVIEW_EVIDENCE_LEVELS:
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
            elif field_token(value).capitalize() not in PROVENANCE_BASIS_VALUES:
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
                    cell_text(cell).split("::")[-1]
                    for cell in cells
                    if re.fullmatch(r"(?:[\w.-]+::)?RSK-\d{3}", cell_text(cell))
                ),
                None,
            )
            if not rid or rid not in blocks:
                continue
            candidates = blocks[rid]
            for idx, field in ((sev_idx, "Severity"), (lik_idx, "Likelihood")):
                table_token = field_token(cells[idx]).lower() if len(cells) > idx else ""
                if table_token not in bands:
                    continue
                # A bare RSK id can recur across per-project blocks, so flag only
                # when no block carrying the id supports the table cell.
                if not any(
                    field_token(field_value(block, field)).lower() == table_token
                    for block in candidates
                ) and any(
                    field_token(field_value(block, field)).lower() in bands
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
            status = row[result_idx].strip()
            if not any(
                status == token or status.startswith(token + " ")
                for token in REVIEW_RESULTS
            ):
                failures.append(
                    f"executed log row '{row[0][:50]}' has result "
                    f"'{row[result_idx]}' - expected {'/'.join(REVIEW_RESULTS)}"
                )
    return failures


def check_register_numbering(lines: list[str], fences: list[bool]) -> list[str]:
    """Register identifiers are report-global: each block identifier defines
    exactly once in a `### <ID>:` heading (each EVD identifier in exactly one
    first-cell ledger row), and every family's numbers run contiguously from
    001 in document order - FND contiguous per pillar."""
    failures: list[str] = []
    sequences: dict[str, list[str]] = {}
    for line, fenced in zip(lines, fences):
        if fenced:
            continue
        block = REF_BLOCK_HEADING.match(line)
        if block:
            ident = block.group(1)
            family = ident.rsplit("-", 1)[0]
            sequences.setdefault(family, []).append(ident)
            continue
        if line.startswith("|"):
            token, _ = defining_row_id(line)
            bare = token.rsplit("::", 1)[-1]
            if bare.startswith("EVD-"):
                sequences.setdefault("EVD", []).append(bare)
    for family, idents in sequences.items():
        seen: set[str] = set()
        for ident in idents:
            if ident in seen:
                failures.append(
                    f"{ident} is defined more than once - register identifiers "
                    "are report-global"
                )
            seen.add(ident)
        numbers = [int(ident.rsplit("-", 1)[1]) for ident in idents]
        expected = list(range(1, len(numbers) + 1))
        if numbers != expected:
            failures.append(
                f"{family} identifiers {', '.join(idents)} do not form a "
                "contiguous sequence starting at 001"
            )
    return failures


FRAME_TOP_LEFT, FRAME_TOP_RIGHT = "╭", "╮"
FRAME_BOT_LEFT, FRAME_BOT_RIGHT = "╰", "╯"
FRAME_SIDE = "│"


def frame_pairs(line: str, left: str, right: str) -> tuple[list[tuple[int, int]], bool]:
    """Pair `left`/`right` frame corners on one line; the second element is
    False when a left corner finds no right corner or the counts differ."""
    pairs: list[tuple[int, int]] = []
    cursor = 0
    while True:
        lpos = line.find(left, cursor)
        if lpos < 0:
            break
        rpos = line.find(right, lpos + 1)
        if rpos < 0:
            return pairs, False
        pairs.append((lpos, rpos))
        cursor = rpos + 1
    return pairs, line.count(left) == line.count(right)


def check_frame_geometry(lines: list[str], fences: list[bool]) -> list[str]:
    """Inside fenced code, every ╭─╮/│/╰─╯ frame keeps identical border
    columns on each of its rows - the side bars align vertically and the
    bottom border spans the top border's columns."""
    failures: list[str] = []
    open_frames: list[tuple[int, int, int]] = []
    for index, (line, fenced) in enumerate(zip(lines, fences)):
        if not fenced:
            for _left, _right, start in open_frames:
                failures.append(f"frame opened at line {start} never closes")
            open_frames = []
            continue
        if line.lstrip().startswith("```"):
            continue
        tops, tops_ok = frame_pairs(line, FRAME_TOP_LEFT, FRAME_TOP_RIGHT)
        bots, bots_ok = frame_pairs(line, FRAME_BOT_LEFT, FRAME_BOT_RIGHT)
        if not tops_ok:
            failures.append(
                f"line {index + 1}: unbalanced "
                f"{FRAME_TOP_LEFT}/{FRAME_TOP_RIGHT} frame corners"
            )
        if not bots_ok:
            failures.append(
                f"line {index + 1}: unbalanced "
                f"{FRAME_BOT_LEFT}/{FRAME_BOT_RIGHT} frame corners"
            )
        sides = {i for i, ch in enumerate(line) if ch == FRAME_SIDE}
        still_open: list[tuple[int, int, int]] = []
        for left, right, start in open_frames:
            if (left, right) in bots:
                continue
            still_open.append((left, right, start))
            if left not in sides or right not in sides:
                failures.append(
                    f"line {index + 1}: frame opened at line {start} "
                    f"(columns {left}-{right}) has no side border on this row"
                )
        for left, right in bots:
            if not any(l == left and r == right for l, r, _ in open_frames):
                failures.append(
                    f"line {index + 1}: frame bottom border at columns "
                    f"{left}-{right} matches no open frame"
                )
        open_frames = still_open + [
            (left, right, index + 1) for left, right in tops
        ]
    for _left, _right, start in open_frames:
        failures.append(f"frame opened at line {start} never closes")
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
        block = rest[
            : section_end(rest, heading_depth(match), skip_registers=True)
        ]
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
                    cell_text(cell).split("::")[-1]
                    for cell in cells
                    if re.fullmatch(r"(?:[\w.-]+::)?FND-[A-Z]{3}-\d{3}", cell_text(cell))
                ),
                None,
            )
            if not fid or fid not in details:
                continue
            detail = details[fid]
            claimed = cells[vidx] if len(cells) > vidx else ""
            verified = field_value(detail, "Verification").lower()
            runtime = field_value(detail, "Runtime").lower()
            if claimed.startswith("Verified") and not verified:
                failures.append(f"{fid}: summary says Verified but block has no Verification field")
            if claimed.startswith("Confirmed") and not runtime:
                failures.append(f"{fid}: summary says Confirmed but block does not confirm it")
    return failures


def check_fresh_audit_claims(lines: list[str], fences: list[bool]) -> list[str]:
    text = NL.join(lines)
    if re.search(r"^#{2,3}\s+Changes Since Previous Audit\s*$", text, re.MULTILINE):
        return []
    failures: list[str] = []
    for index, (line, fenced) in enumerate(zip(lines, fences)):
        if fenced or re.search(
            r"parity baseline|industry baseline|comparison baseline|stack baseline",
            line,
            re.IGNORECASE,
        ):
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
    for match in re.finditer(r"^#{2,3}\s+Remediation Roadmap\s*$", text, re.MULTILINE):
        rest = text[match.end() :]
        block = rest[: section_end(rest, heading_depth(match))]
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
            "project_qualified": "FND-<pillar>-NNN (<project>) - bare ID, heading suffix",
            "numbering": "report-global - every register identifier defines "
            "exactly once and numbers contiguously from 001 in document "
            "order, FND contiguous per pillar",
            "risk": "RSK-NNN",
            "recommendation": "REC-NNN",
            "debt": "TDR-NNN",
            "evidence": "EVD-NNN",
            "validation": "PAR-NN",
            "reference_links": "every register identifier cited outside its "
            "defining location links to its definition - ### heading anchors "
            "for FND/RSK/REC/TDR blocks, the register's section anchor for "
            "EVD/PAR rows",
        },
        "styles": {
            "audit": {
                "sections": BASELINE_SECTIONS + ["Recommendation Classification"],
                "brief_sections": sorted(BRIEF_SECTIONS),
                "findings_section": "Technical Findings",
                "recommendation_classification": "required at Standard/Detailed",
                "finding_disposition": "every open ### FND- block is cited in the "
                "roadmap/classification region or carries an explicit disposition",
                "defect_scenarios": "required on High/Critical findings",
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
                "defect_scenarios": "required on High/Critical findings",
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
                    "Follow-up Plan",
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
            "conformance_status": sorted(CONFORMANCE_STATUS_TOKENS),
            "structure_verdict": sorted(CONFORMANCE_VERDICT_TOKENS),
            "validation_record_result": list(PAR_RESULTS),
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
            "coverage": "Status cells render Covered, Partially, or Not done",
        },
        "rules": [
            "headings no deeper than ###, preceded and followed by one blank line",
            "no line ends a sentence with '.' and continues it lowercase on the "
            "next line, no doubled end marks, no '..' identifier ranges",
            "the audit Executive Summary carries the Field/Value key-value table "
            "with System type, Scope, Source basis, Maturity level, and Overall "
            "score rows; Maturity level is Prototype/Early development/"
            "Pre-production/Production-ready/Undetermined",
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
            "register identifiers are report-global - defined exactly once "
            "and contiguous from 001 per family, FND contiguous per pillar",
            "fenced frame drawings keep identical border columns on every "
            "row of the frame",
            "a coverage row claiming SBOM/component-inventory Covered requires a "
            "Software Bill of Materials section - a module inventory is not an SBOM",
            "High/Critical findings carry a Defect scenario field under the "
            "audit and hunt styles",
            "Error/Blocked are runner states, never product failures - "
            "Not run is never a pass",
            "a model reproduction never upgrades app-level reachability",
            "Executed Evidence Log and Execution Register Result cells take the "
            "check-status vocabulary",
            "table column widths count the full [text](target) and "
            "![alt](src) markup in source text - brackets, text, and target "
            "together",
        ],
    }


LANGUAGE_ROW = re.compile(
    r"^\|\s*(Language|Język|Sprache|Langue|Lingua|Idioma)\s*\|\s*([^|]+)\|",
    re.MULTILINE | re.IGNORECASE,
)
ENGLISH_VALUES = {"english", "angielski"}

TRANSLATED_REPORT_GUIDANCE = (
    "lint-polish.py <report> --rules <translations/polish-language.md>",
    "lint-prose.py <report>",
    "link-glossary.py <report> --lang pl --check",
    "map-translation.py <report> --rules <translations/polish-language.md>"
    " --en <english-sibling.md>",
    "format-table.py <mapped-copy> and validate-report.py <mapped-copy>",
    "check-translation.py <report>",
)


def non_english_language(text: str) -> str | None:
    """Return a `label: value` string when the Document Information
    language row declares a non-English report, else None. The row lives
    in the first `##` section; scanning the whole document would risk a
    stray `Language` cell in an unrelated table."""
    lines = text.split("\n")
    sections = [i for i, line in enumerate(lines) if line.startswith("## ")]
    if len(sections) > 1:
        text = "\n".join(lines[: sections[1]])
    match = LANGUAGE_ROW.search(text)
    if not match:
        return None
    label, value = match.group(1).strip(), match.group(2).strip()
    if label.lower() == "language" and value.lower() in ENGLISH_VALUES:
        return None
    return f"{label}: {value}"


def reconfigure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="backslashreplace")
        except Exception:
            pass


def main(path: str, repo_root: str | None = None) -> int:
    reconfigure_stdio()
    text = Path(path).read_text(encoding="utf-8")
    lines = text.replace("\r\n", "\n").split("\n")
    fences = split_code(lines)
    language = non_english_language(text)
    if language is not None:
        print(f"report language: {language}")
        print(
            "validate-report.py checks the English report contract only; "
            "running it on a translated report produces false failures."
        )
        print("Use the translated-report gates instead:")
        for step in TRANSLATED_REPORT_GUIDANCE:
            print(f"  {step}")
        return 2
    kind = report_kind(path, text)
    checks = [
        ("headings", check_headings(lines, fences)),
        ("semicolons", check_semicolons(lines, fences)),
        ("non-ASCII dashes and arrows", check_dashes(lines, fences)),
        (
            "sentence line breaks",
            check_sentence_breaks(lines, fences, sentence_breaks_on(text)),
        ),
        ("sentence breaks row", check_sentence_breaks_row(text)),
        ("tables", check_tables(lines, fences)),
        ("frame geometry", check_frame_geometry(lines, fences)),
        ("bold markers", check_bold_markers(lines, fences)),
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
                    ("register reference links", check_reference_links(lines, fences, text)),
                    ("register numbering", check_register_numbering(lines, fences)),
                    ("finding-block fields", check_finding_blocks(lines)),
                    ("criterion references", check_criterion_references(lines, style)),
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
                    ("executive summary table", check_executive_summary(text)),
                    ("coverage rows", check_coverage_rows(text)),
                    ("FND/RSK/REC cross-references", check_ids(text)),
                    ("register reference links", check_reference_links(lines, fences, text)),
                    ("register numbering", check_register_numbering(lines, fences)),
                    ("finding-block fields", check_finding_blocks(lines)),
                    ("criterion references", check_criterion_references(lines, style)),
                    ("description paragraphs", check_description_paragraphs(lines)),
                    ("risk-block fields", check_risk_blocks(lines)),
                    ("recommendation blocks", check_rec_blocks(lines)),
                    ("debt blocks", check_tdr_blocks(lines)),
                    ("legacy field names", check_legacy_fields(lines, fences)),
                    ("findings summary columns", check_finding_summary(text)),
                    ("findings count", check_finding_counts(text)),
                    ("scorecard mean", check_scorecard_mean(text)),
                    ("scorecard intervals", check_scorecard_interval(text)),
                    ("ledger columns", check_ledger_columns(text)),
                    ("scorecard N/A rows", check_scorecard_na(text)),
                    ("security classifications", check_security_classification(lines)),
                    ("score disclosure", check_score_disclosure(lines)),
                    ("project qualification", check_project_qualification(text)),
                    ("PAR-1..PAR-27", check_par_rows(text)),
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
                    ("references links", check_references_section(text)),
                ]
            )
            if style == "hunt":
                checks.extend(
                    [
                        ("hunt domain ratings", check_hunt_ratings(text)),
                        ("hunt verdict elements", check_hunt_verdict(text)),
                        ("hunt journey traces", check_hunt_journeys(text)),
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
                checks.extend(
                    [
                        ("structure and naming conformance", check_structure_and_naming(text)),
                        ("audit finding disposition", check_finding_disposition(text, lines)),
                    ]
                )
            if style in ("audit", "hunt"):
                checks.append(("defect scenarios", check_hunt_scenarios(lines)))
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
