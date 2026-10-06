"""Generate a Lens report skeleton.

Emits a structurally complete report scaffold - every required heading, the
table headers the validator expects, and one field-labeled template block per
register - so an author starts from the enforced contract instead of a blank
file. Placeholder cells carry ``<...>`` markers: content-bearing checks fail
until the author replaces them, which is deliberate.

Usage:
  python new-report.py --style audit|hunt|check [--projects a,b] [--params file]
                       [--output report.md]

``--params`` reads a saved intake file (``work/lens-params.json``) carrying
``report_style``, ``projects``, ``subject``, ``revision``, ``language``, and
``detail_level`` so a second report in the same session reuses the locked
intake values. Command-line options override the file.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

AUDIT_SECTIONS = [
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
    "Trade-off Analysis",
    "Strengths & What's Working",
]

CLOSING_SECTIONS = [
    "Scope Exclusions",
    "Limitations and Unknowns",
    "Validation Record",
    "References",
]

HUNT_DOMAINS = [
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
]

DOC_INFO = [
    ("Report Revision", "1.0"),
    ("Report Date", "<YYYY-MM-DD>"),
    ("Report Style", None),
    ("Detail Level", None),
    ("Evaluation Scale", "1-10"),
    ("Language", "English"),
    ("Audit Purpose", "<audit purpose>"),
    ("Target Environment", "<target environment>"),
    ("Verification Scope", "static repository analysis - no execution"),
    ("Evidence Mode", "source-only"),
    ("Subject Revision", "<commit> (branch <branch>)"),
    ("Skill Version", "<version>"),
    ("State", "Draft"),
]

COVERAGE_HEADER = "| Report type | Status | Rationale |\n|---|---|---|\n"

FINDING_BLOCK = """### FND-SEC-001: <finding title>{suffix}

* **Pillar:** Security & Compliance
* **Severity:** <CRITICAL | HIGH | MEDIUM | LOW>
* **Type:** Concern
* **Status:** Open
* **Change:** New
* **Targets:** {targets}
* **Basis:** <requirement or source basis>
* **Description:** <what the discovered state is, where, and why it is a finding>
* **Impact:** <concrete consequence>
* **Recommendation:** <step-by-step technical guidance>
* **Method:** <test or command that confirms the fix>
* **Verified:** yes - <basis> or no - <basis>
* **Runtime confirmed:** no - <basis>
* **Confidence:** <High | Medium | Low>
* **Mitigating factors:** <factors or omit line>
* **Breaking change:** None
* **Evidence:** <EVD IDs, `path:line` ranges, inspected basis>
"""

RISK_BLOCK = """### RSK-001: <risk title>{suffix}

* **Severity:** <CRITICAL | HIGH | MEDIUM | LOW>
* **Likelihood:** <High | Medium | Low>
* **Residual:** <residual after mitigation>
* **Status:** Open
* **Description:** <what could go wrong>
* **Impact:** <concrete consequence>
* **Trigger:** <what sets it off>
* **Controls:** <existing controls>
* **Mitigation:** <treatment plan>
* **Closure:** <closure condition>
* **Source:** FND-SEC-001
* **Confidence:** <High | Medium | Low>
"""

REC_BLOCK = """### REC-001: <recommendation title>{suffix}

* **Priority:** P1
* **Target:** {target}
* **Action:** <what to do>
* **Effort:** <Low | Medium | High>
* **Breaking change:** None
* **Verification:** <how the fix is confirmed>
"""

PAR_ROWS = [
    f"| PAR-{number} | <result> | <evidence or `N/A` justification> |\n"
    for number in range(1, 19)
]


def validation_record() -> str:
    return table(
        "| Check | Result | Evidence / Justification |",
        "|---|---|---|",
        PAR_ROWS + ["| Parity baseline | <report or `none found`> | <note> |\n"],
    )


def heading(level: int, title: str) -> str:
    return f"{'#' * level} {title}\n\n"


def table(header: str, separator: str, rows: list[str] | None = None) -> str:
    return header + "\n" + separator + "\n" + "".join(rows or []) + "\n"


def document_info(style: str, projects: list[str], params: dict) -> str:
    rows = []
    for field, value in DOC_INFO:
        if field == "Report Style":
            value = style
        elif field == "Detail Level":
            value = params.get("detail_level", "Standard")
        elif field == "Evidence Mode":
            value = params.get("evidence_mode", "source-only")
        rows.append(f"| {field} | {value} |")
    if projects:
        rows.append(f"| Projects | {', '.join(projects)} |")
    return table("| Field | Value |", "|---|---|", [row + "\n" for row in rows])


def inventory(projects: list[str]) -> str:
    rows = [f"| {name} | <path> | <version> | <one-line description> |\n" for name in projects]
    return table(
        "| Project | Path | Version | Description |",
        "|---|---|---|---|",
        rows,
    )


def ledger_table(multi: bool) -> str:
    if multi:
        return table(
            "| Evidence | Project | Check / Source | Result | Type | Artifact |",
            "|---|---|---|---|---|---|",
        )
    return table(
        "| Evidence | Check / Source | Result | Type | Artifact |",
        "|---|---|---|---|---|",
    )


def finding_summary_table(projects: list[str]) -> str:
    if len(projects) > 1:
        return table(
            "| Project | Finding | Pillar | Severity | Title | Result | Status | Change | Verification |",
            "|---|---|---|---|---|---|---|---|---|",
            [
                f"| {projects[0]} | FND-SEC-001 | Security & Compliance | <severity> | <title> | <result> | Open | New | Verified |\n"
            ],
        )
    return table(
        "| Finding | Pillar | Severity | Title | Result | Status | Change | Verification |",
        "|---|---|---|---|---|---|---|---|",
        ["| FND-SEC-001 | Security & Compliance | <severity> | <title> | <result> | Open | New | Verified |\n"],
    )


def audit_skeleton(projects: list[str], params: dict) -> str:
    multi = len(projects) > 1
    parts = [
        "# <subject> - Lens audit report\n\n",
        heading(2, "Document Information"),
        document_info("audit", projects, params),
        heading(2, "Audit Type Coverage"),
        COVERAGE_HEADER + "\n",
    ]
    if multi:
        parts += [heading(2, "Project Inventory"), inventory(projects)]
    if multi:
        parts.append(heading(2, "Executive Summary"))
        parts.append(
            table(
                "| Project | Score | Lowest | Risks | Readiness |",
                "|---|---|---|---|---|",
                [f"| {name} | <mean>/<scale> (<band>) | <dimension> <score> | <top RSK-XXX> | <readiness> |\n" for name in projects],
            )
        )
        for name in projects:
            parts.append(heading(2, name))
            parts += audit_project_body(name)
        parts += audit_shared_tail(multi)
    else:
        parts += audit_project_body("")
        parts += audit_shared_tail(False)
    return "".join(parts)


def audit_project_body(project: str) -> list[str]:
    level = 3 if project else 2
    suffix = f" ({project})" if project else ""
    parts: list[str] = []
    for section in AUDIT_SECTIONS:
        parts.append(heading(level, section))
        if section == "Executive Summary":
            parts.append(
                table(
                    "| Field | Value |",
                    "|---|---|",
                    [
                        "| System type | <prototype / codebase / production system / proposal> |\n",
                        "| Scope | <what was reviewed and what was excluded> |\n",
                        "| Source basis | <running system / inspected code / description> |\n",
                        "| Maturity level | <maturity level> |\n",
                        "| Overall score | <mean>/<scale> (<band>) |\n",
                    ],
                )
            )
            parts.append("Lowest-scoring applicable dimension: <dimension> <score>.\n\n")
        elif section == "Health Dashboard":
            parts.append(
                table(
                    "| Impact | LOW | MEDIUM | HIGH |",
                    "|---|---|---|---|",
                    ["| CRITICAL |  |  |  |\n", "| HIGH |  |  |  |\n",
                     "| MEDIUM |  |  |  |\n", "| LOW |  |  |  |\n"],
                )
            )
            parts.append("**Scorecard Summary**\n\n")
            parts.append(table("| Dimension | Score | Notes |", "|---|---|---|"))
        elif section == "High-Level Observations":
            parts.append(table("| Observation |", "|---|", ["| <observation> |\n"]))
    parts.append(heading(level, "Detailed Technical Findings"))
    parts.append(finding_summary_table([project] if project else []))
    parts.append(FINDING_BLOCK.format(suffix=suffix, targets=qualified(project)) + "\n")
    parts.append(heading(level, "Unified Risk Register"))
    parts.append(RISK_BLOCK.format(suffix=suffix) + "\n")
    parts.append(heading(level, "Actionable Remediation Roadmap"))
    parts.append(
        table(
            "| Priority | Recommendation | Addresses | Effort | Breaking |",
            "|---|---|---|---|---|",
            ["| P1 | REC-001 <recommendation> | FND-SEC-001 | <effort> | None |\n"],
        )
    )
    parts.append(REC_BLOCK.format(suffix=suffix, target=qualified(project)) + "\n")
    parts.append(heading(level, "Recommendation Classification"))
    parts.append(
        table(
            "| Rec | Recommendation | Class | Basis |",
            "|---|---|---|---|",
            ["| REC-001 | <action> | Recommended | FND-SEC-001 - <short reason> |\n"],
        )
    )
    return parts


def audit_shared_tail(multi: bool) -> list[str]:
    parts = [
        heading(2, "Operator Verification Handoff"),
        "Every material claim the audit could not resolve from source, with the\n"
        "exact command or procedure and its pass criteria.\n\n",
        heading(2, "Scope Exclusions"),
        "- Glossary omitted - Descriptive mode disabled.\n\n",
        heading(2, "Limitations and Unknowns"),
        "- <each check that would require execution and was not performed>\n\n",
        heading(2, "Validation Record"),
        validation_record() + "\n",
        heading(2, "References"),
        "- <external source>\n\n",
    ]
    return parts


def qualified(project: str) -> str:
    return f"{project}::FND-SEC-001" if project else "FND-SEC-001"


def hunt_skeleton(projects: list[str], params: dict) -> str:
    multi = len(projects) > 1
    parts = [
        "# <subject> - Lens hunt report\n\n",
        heading(2, "Document Information"),
        document_info("hunt", projects, params),
        heading(2, "Audit Type Coverage"),
        COVERAGE_HEADER + "\n",
    ]
    if multi:
        parts += [heading(2, "Project Inventory"), inventory(projects)]
    parts += [
        heading(2, "Verdict"),
        "<purpose statement - what the subject is, what was hunted, at which snapshot>\n\n",
        "Verdict: **Not ready**. <one sentence on what the verdict does not mean>\n\n",
        table(
            "| Domain | Rating | Basis |",
            "|---|---|---|",
            [f"| {domain} | Not assessed | <no scoreable evidence yet> |\n" for domain in HUNT_DOMAINS],
        ),
        "Hard readiness gates:\n\n",
        table(
            "| Gate | Result | Basis |",
            "|---|---|---|",
            ["| <gate> | Not assessable | <basis> |\n"],
        ),
        "Top five actions:\n\n",
        "1. REC-001 - <first remediation step> (FND-SEC-001).\n\n",
        "Strengths:\n\n",
        "- <evidenced positive>\n\n",
        heading(2, "System Context"),
        "<purpose, stack with locked versions, component inventory>\n\n",
        table("| Component | Lines | Role |", "|---|---|---|"),
        heading(2, "Methodology And Evidence"),
        "Read-depth table:\n\n",
        table("| Area | Files | Read depth |", "|---|---|---|"),
        "Evidence ledger:\n\n",
        ledger_table(multi),
        heading(2, "Journey Traces"),
        "Producer/consumer matrix for every value crossing a component boundary.\n\n",
        table(
            "| Value | Producer | Consumer | Representation match | Evidence |",
            "|---|---|---|---|---|",
        ),
        "Per-workflow traces, each hop `conforming`, `failing`, or `not assessable`:\n\n",
        "**<workflow> journey** (<entry> -> <exit>)\n\n",
        table(
            "| Hop | Status | Evidence |",
            "|---|---|---|",
            ["| <hop> | conforming | <EVD-XXX> |\n", "| <hop> | failing | <EVD-XXX> (FND-SEC-001) |\n"],
        ),
        heading(2, "Domain Findings"),
        finding_summary_table(projects),
    ]
    for domain in ("Security",):
        parts.append(heading(3, domain))
        parts.append(
            HUNT_FINDING_BLOCK.format(
                suffix=f" ({projects[0]})" if multi else "",
                targets=qualified(projects[0] if multi else ""),
            )
            + "\n"
        )
    parts += [
        heading(2, "Risk Register"),
        RISK_BLOCK.format(suffix=f" ({projects[0]})" if multi else "") + "\n",
        heading(2, "Remediation Phases"),
        heading(3, "Stabilize"),
        table(
            "| Rec | Recommendation | Resolves | Effort | Breaking |",
            "|---|---|---|---|---|",
            [f"| REC-001 | <recommendation> | {qualified(projects[0] if multi else '')} | <effort> | None |\n"],
        ),
        REC_BLOCK.format(
            suffix=f" ({projects[0]})" if multi else "",
            target=qualified(projects[0] if multi else ""),
        )
        + "\n",
        heading(3, "Accepted - no action"),
        table("| Finding | Disposition |", "|---|---|"),
        heading(2, "Operator Verification Handoff"),
        "Every material claim the hunt could not resolve from source, with the\n"
        "exact command or procedure and its pass criteria.\n\n",
        heading(2, "Scope Exclusions"),
        "- Glossary omitted - Descriptive mode disabled.\n\n",
        heading(2, "Limitations and Unknowns"),
        "- <each check that would require execution and was not performed>\n\n",
        heading(2, "Validation Record"),
        validation_record() + "\n",
        heading(2, "References"),
        "- <external source>\n\n",
    ]
    return "".join(parts)


HUNT_FINDING_BLOCK = FINDING_BLOCK.replace(
    "* **Runtime confirmed:**",
    "* **Defect scenario:** <initial conditions, steps, expected result, observed result, "
    "confirmation level - required on HIGH/CRITICAL>\n* **Runtime confirmed:**",
)

CHECK_FINDING_BLOCK = HUNT_FINDING_BLOCK.replace(
    "* **Evidence:**",
    "* **Evidence level:** Source - <inspected basis>\n* **Evidence:**",
)


def check_skeleton(projects: list[str], params: dict) -> str:
    multi = len(projects) > 1
    executed = params.get("evidence_mode", "source-only") != "source-only"
    suffix = f" ({projects[0]})" if multi else ""
    target = qualified(projects[0] if multi else "")
    parts = [
        "# <subject> - Lens check report\n\n",
        heading(2, "Document Information"),
        document_info("check", projects, params),
        heading(2, "Audit Type Coverage"),
        COVERAGE_HEADER + "\n",
    ]
    if multi:
        parts += [heading(2, "Project Inventory"), inventory(projects)]
    parts += [
        heading(2, "Verdict"),
        "<purpose statement - what the subject is, what was checked, at which snapshot>\n\n",
        "Verdict: **Not ready**. <one sentence on what the verdict does not mean>\n\n",
        table(
            "| Domain | Rating | Basis |",
            "|---|---|---|",
            [f"| {domain} | Not assessed | <no scoreable evidence yet> |\n" for domain in HUNT_DOMAINS],
        ),
        "Hard readiness gates:\n\n",
        table(
            "| Gate | Result | Basis |",
            "|---|---|---|",
            ["| <gate> | Not assessable | <basis> |\n"],
        ),
        "Top five actions:\n\n",
        "1. REC-001 - <first remediation step> (FND-SEC-001).\n\n",
        "Strengths:\n\n",
        "- <evidenced positive>\n\n",
        heading(2, "System Context"),
        "<purpose, stack with locked versions, component inventory, runtime environment>\n\n",
        table("| Component | Lines | Role |", "|---|---|---|"),
        heading(2, "Check Plan And Methodology"),
        "Checks selected, the criterion each evaluates, the evidence level each reaches, "
        "and the commands the user commissioned:\n\n",
        table("| Check | Criterion | Evidence level |", "|---|---|---|"),
        "Read-depth table:\n\n",
        table("| Area | Files | Read depth |", "|---|---|---|"),
        "Evidence ledger:\n\n",
        ledger_table(multi),
        heading(2, "Execution Register"),
        "One row per check. `Result` is PASS, FAIL, ERROR, BLOCKED, SKIPPED, NOT RUN, "
        "or N/A - `ERROR`/`BLOCKED` are runner states, never product failures, and "
        "`NOT RUN` is never a pass. Every non-PASS row states its Interpretation.\n\n",
        table(
            "| Check | Command | Cwd | Tool & Version | Timestamp | Input revision | Exit status | Result | Interpretation | Artifact |",
            "|---|---|---|---|---|---|---|---|---|---|",
            [
                "| <check> | <exact command> | <cwd> | <tool and version> | <timestamp> | "
                "<revision> | <exit code> | NOT RUN | <why or outcome meaning> | <artifact or `None retained`> |\n"
            ],
        ),
        heading(2, "Domain Findings"),
        finding_summary_table(projects),
        heading(3, "Security"),
        CHECK_FINDING_BLOCK.format(suffix=suffix, targets=target) + "\n",
        heading(2, "Risk Register"),
        RISK_BLOCK.format(suffix=suffix) + "\n",
        heading(2, "Improvement Plan"),
        heading(3, "Stabilize"),
        table(
            "| Rec | Recommendation | Resolves | Effort | Breaking |",
            "|---|---|---|---|---|",
            [f"| REC-001 | <recommendation> | {target} | <effort> | None |\n"],
        ),
        REC_BLOCK.format(suffix=suffix, target=target) + "\n",
        heading(3, "Accepted - no action"),
        table("| Finding | Disposition |", "|---|---|"),
        heading(2, "Retest Register"),
        "One row per `FAIL`, `ERROR`, or `BLOCKED` register row - omit the section when "
        "no such rows exist.\n\n",
        table(
            "| Check | Register result | Blocking condition | Retest command | Closes |",
            "|---|---|---|---|---|",
        ),
    ]
    if executed:
        parts += [
            heading(2, "Metrics Snapshot"),
            table("| Metric | Value | Scope |", "|---|---|---|"),
            heading(2, "Artifact Manifest"),
            table(
                "| Artifact | Check | Location / Digest | Notes |",
                "|---|---|---|---|",
            ),
            heading(2, "Operator Verification Handoff"),
            "Checks outside the commissioned set, with the exact command or procedure "
            "and its pass criteria.\n\n",
        ]
    else:
        parts += [
            heading(2, "Operator Verification Handoff"),
            "Every material claim the check could not resolve from source, with the\n"
            "exact command or procedure and its pass criteria.\n\n",
        ]
    parts += [
        heading(2, "Scope Exclusions"),
        "- Glossary omitted - Descriptive mode disabled.\n"
        "- Artifact Manifest omitted - `source-only` evidence mode retains no "
        "artifacts.\n\n"
        if not executed
        else "- Glossary omitted - Descriptive mode disabled.\n\n",
        heading(2, "Limitations and Unknowns"),
        "- <each check that stayed NOT RUN and every unresolved unknown>\n\n",
        heading(2, "Validation Record"),
        validation_record() + "\n",
        heading(2, "References"),
        "- <external source>\n\n",
    ]
    return "".join(parts)


def parse_args(argv: list[str]) -> dict:
    options: dict = {"style": None, "projects": [], "params": None, "output": None}
    index = 1
    while index < len(argv):
        argument = argv[index]
        if argument in ("--style", "--projects", "--params", "--output"):
            index += 1
            if index >= len(argv):
                raise SystemExit(f"{argument} needs a value")
            options[argument[2:]] = argv[index]
        else:
            raise SystemExit(f"unknown option: {argument}")
        index += 1
    return options


def main(argv: list[str]) -> int:
    options = parse_args(argv)
    params: dict = {}
    if options["params"]:
        params = json.loads(Path(options["params"]).read_text(encoding="utf-8"))
    style = options["style"] or params.get("report_style") or "audit"
    if style not in ("audit", "hunt", "check"):
        print(f"unknown style '{style}' - expected audit, hunt, or check")
        return 1
    projects = (
        [name.strip() for name in options["projects"].split(",") if name.strip()]
        if options["projects"]
        else list(params.get("projects", []))
    )
    if style == "hunt":
        body = hunt_skeleton(projects, params)
    elif style == "check":
        body = check_skeleton(projects, params)
    else:
        body = audit_skeleton(projects, params)
    if options["output"]:
        target = Path(options["output"])
        target.write_text(body, encoding="utf-8")
        formatter = find_tool("format-table")
        if formatter is not None:
            subprocess.run([sys.executable, str(formatter), str(target)], check=False)
            print(f"wrote {options['output']} (tables aligned)")
        else:
            print(f"wrote {options['output']} - run format-table.py to align tables")
    else:
        sys.stdout.write(body)
    return 0


def find_tool(base: str) -> Path | None:
    roots = [Path(__file__).resolve().parent]
    root = os.environ.get("LENS_SKILL_ROOT")
    if root:
        roots += [Path(root) / "scripts", Path(root)]
    for directory in roots:
        matches = sorted(
            candidate
            for candidate in directory.glob(f"*{base}*.py")
            if candidate.resolve() != Path(__file__).resolve()
        )
        if len(matches) == 1:
            return matches[0]
    return None


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
