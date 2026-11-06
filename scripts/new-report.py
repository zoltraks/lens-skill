"""Generate a Lens report skeleton.

Emits a structurally complete report scaffold - every required heading, the
table headers the validator expects, and one field-labeled template block per
register - so an author starts from the enforced contract instead of a blank
file. Placeholder cells carry ``<...>`` markers: content-bearing checks fail
until the author replaces them, which is deliberate.

Usage:
  python new-report.py --style audit|hunt|review [--scope structure]
                       [--projects a,b] [--params file] [--model file]\n                       [--output report.md]

``--params`` reads a saved intake file (``work/lens-params.json``) carrying
``report_style``, ``review_scope``, ``projects``, ``subject``, ``revision``,
``language``, and ``detail_level`` so a second report in the same session
reuses the locked intake values. Command-line options override the file.
``--scope structure`` with ``--style review`` emits the structure-review
variant contract instead of the execution-register one.
"""

from __future__ import annotations

import json
import re
import os
import subprocess
import sys
from pathlib import Path

AUDIT_SECTIONS = [
    "Executive Summary",
    "System Context",
    "Software Bill of Materials",
    "License Compliance",
    "Health Dashboard",
    "Delivery Practice",
    "High-Level Observations",
    "Auditing Methodology",
    "Scoring Rubrics",
    "Architectural Assessment",
    "Structure Review",
    "Solution Comparison",
    "Strengths & What's Working",
]

CLOSING_SECTIONS = [
    "Scope Exclusions",
    "Known Limitations",
    "Validation Protocol",
    "Reference Sources",
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
    ("Verification Scope", "Static repository analysis - no execution"),
    ("Evidence Mode", "Source-only"),
    ("Subject Revision", "<commit> (branch <branch>)"),
    ("Skill Version", "<version>"),
    ("Time taken", "<mm:ss>"),
]

COVERAGE_HEADER = "| Report type | Status | Rationale |\n|---|---|---|\n"

FINDING_BLOCK = """### {fnd_id}: <finding title>{suffix}

<what the discovered state is, where, and why it is a finding>

* **Pillar:** Security & Compliance
* **Severity:** <Critical | High | Medium | Low>
* **Type:** Concern
* **Targets:** {targets}
* **Basis:** <requirement or source basis>
* **Criteria:** <criteria ID - violated or uncertain property>
* **Impact:** <concrete consequence>
* **Method:** <test or command that confirms the fix>
* **Verification:** Observed in source, <basis>
* **Defect scenario:** <initial conditions, steps, expected result, observed result, confirmation level - required on High/Critical>
* **Runtime:** <confirmed behavior note>
* **Confidence:** <High | Medium | Low>
* **Mitigating factors:** <factors or omit line>
* **Breaking change:** None
* **Evidence:** <EVD IDs, `path:line` ranges, inspected basis>
* **Recommendation:** <step-by-step technical guidance>
"""

RISK_BLOCK = """### {rsk_id}: <risk title>{suffix}

<what could go wrong>

* **Severity:** <Critical | High | Medium | Low>
* **Likelihood:** <High | Medium | Low>
* **Residual:** <residual after mitigation>
* **Impact:** <concrete consequence>
* **Trigger:** <what sets it off>
* **Controls:** <existing controls>
* **Closure:** <closure condition>
* **Source:** {fnd_id}
* **Confidence:** <High | Medium | Low>
* **Mitigation:** <treatment plan>
"""

REC_BLOCK = """### {rec_id}: <recommendation title>{suffix}

<what the action changes and how it resolves the finding>

* **Priority:** P1
* **Finding:** {target}
* **Condition:** <verifiable end state the action must establish>
* **Impact:** <business or technical impact of applying this fix>
* **Effort:** <Low | Medium | High>
* **Complexity:** <Low | Medium | High>
* **Verification:** <test or process confirming the fix, with pass criteria>
"""

PAR_ROWS = [
    f"| PAR-{number} | <result> | <evidence or `N/A` justification> |\n"
    for number in range(1, 34)
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


def skill_version() -> str:
    skill_md = Path(__file__).resolve().parent.parent / "SKILL.md"
    try:
        for line in skill_md.read_text().split("\n"):
            if line.strip().startswith("version:"):
                return line.split(":", 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass
    return "<version>"


def document_info(style: str, projects: list[str], params: dict) -> str:
    rows = []
    for field, value in DOC_INFO:
        if field == "Report Style":
            value = style.capitalize()
        elif field == "Detail Level":
            value = params.get("detail_level", "Standard")
        elif field == "Evidence Mode":
            value = params.get("evidence_mode", "Source-only")
        elif field == "Skill Version":
            value = skill_version()
        rows.append(f"| {field} | {value} |")
        if field == "Report Style" and params.get("review_scope") == "structure":
            rows.append("| Review Scope | Structure |")
    if projects:
        rows.append(f"| Projects | {', '.join('[' + p + '](#' + p.lstrip('.').replace(' ', '-').lower() + ')' for p in projects)} |")
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
            "| Evidence | Project | Source | Result | Type | Artifact |",
            "|---|---|---|---|---|---|",
        )
    return table(
        "| Evidence | Source | Result | Type | Artifact |",
        "|---|---|---|---|---|",
    )


def finding_summary_table(projects: list[str], fnd_id: str = "FND-SEC-001") -> str:
    if len(projects) > 1:
        return table(
            "| Project | Finding | Pillar | Severity | Title | Result | Status | Change | Verification |",
            "|---|---|---|---|---|---|---|---|---|",
            [
                f"| {projects[0]} | {fnd_id} | Security & Compliance | <severity> | <title> | <result> | Open | New | Verification |\n"
            ],
        )
    return table(
        "| Finding | Pillar | Severity | Title | Result | Status | Change | Verification |",
        "|---|---|---|---|---|---|---|---|",
        [f"| {fnd_id} | Security & Compliance | <severity> | <title> | <result> | Open | New | Verification |\n"],
    )


def audit_skeleton(projects: list[str], params: dict) -> str:
    multi = len(projects) > 1
    parts = [
        "# <subject> - Lens audit report\n\n",
        heading(2, "Document Information"),
        document_info("audit", projects, params),
        heading(2, "Audit Coverage"),
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
        for index, name in enumerate(projects):
            parts.append(heading(2, name))
            parts += audit_project_body(name, index + 1)
        parts += audit_shared_tail(multi, projects)
    else:
        parts += audit_project_body("")
        parts += audit_shared_tail(False)
    return "".join(parts)


def audit_project_body(project: str, number: int = 1) -> list[str]:
    level = 3 if project else 2
    suffix = f" ({project})" if project else ""
    # Register identifiers number globally across the whole report - each
    # project's blocks continue the single FND/RSK/REC sequences.
    fnd_id = f"FND-SEC-{number:03d}"
    rsk_id = f"RSK-{number:03d}"
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
            parts.append(
                table(
                    "| Score | Value | Basis |",
                    "|---|---|---|",
                    [
                        "| Product Quality | <score>/<scale> (<band>) | <formula>, lowest <dimension> <score> |\n",
                        "| Engineering Process | <score>/<scale> (<band>) or Not published | <formula>, lowest <dimension> <score> |\n",
                        "| Overall Score | <score>/<scale> (<band>) or Not published | <blend, Product-only, ceiling wording> |\n",
                    ],
                )
            )
            parts.append("Lowest-scoring applicable dimension: <dimension> <score>.\n\n")
        elif section == "Health Dashboard":
            parts.append("**Risk Map**\n\n")
            parts.append(
                table(
                    "| Impact | Low | Medium | High |",
                    "|---|---|---|---|",
                    ["| Critical |  |  |  |\n", "| High |  |  |  |\n",
                     "| Medium |  |  |  |\n", "| Low |  |  |  |\n"],
                )
            )
            parts.append("**Scorecard Summary**\n\n")
            parts.append(table("| Dimension | Score | Notes |", "|---|---|---|"))
            parts.append("**Team & Continuity**\n\n")
            parts.append(
                "<one-line contributor/continuity summary anchored to EVD-XXX - "
                "`Not collected` when git history was out of scope>\n\n"
            )
        elif section == "Structure Review":
            parts.append(
                "<context line - stack, component roles, architectural approach, "
                "scale signal>\n\n"
            )
            parts.append("<structural overview - existing directory, file, and component organization>\n\n")
            parts.append(
                table(
                    "| Level | Directory | Contents | Role |",
                    "|---|---|---|---|",
                    ["| `1` | `<dir>` | <contents> | <component role> |\n"],
                )
            )
            parts.append(
                table(
                    "| Area | Verdict | Basis |",
                    "|---|---|---|",
                    [
                        "| Directory organization | Passed | <convention tier> |\n",
                        "| Naming conventions | Passed | <basis> |\n",
                        "| Component placement | Passed | <basis> |\n",
                        "| Supporting-artifact layout | Passed | <basis> |\n",
                        "| Consistency | Passed | <basis> |\n",
                    ],
                )
            )
            parts.append("Positive practices: <evidenced organizational decisions worth preserving>\n\n")
            parts.append("Limitations: <areas that could not be evaluated>\n\n")
        elif section == "High-Level Observations":
            parts.append(table("| Observation |", "|---|", ["| <observation> |\n"]))
    parts.append(heading(level, "Technical Findings"))
    parts.append(finding_summary_table([project] if project else [], fnd_id))
    parts.append(FINDING_BLOCK.format(suffix=suffix, targets=qualified(project, fnd_id), fnd_id=fnd_id) + "\n")
    parts.append(heading(level, "Unified Risk Register"))
    parts.append(RISK_BLOCK.format(suffix=suffix, rsk_id=rsk_id, fnd_id=fnd_id) + "\n")
    return parts


def roadmap_sections(projects: list[str]) -> list[str]:
    """The consolidated Remediation Roadmap - one level-2 section per report.

    A multi-project call merges every project's recommendations into one shared
    matrix with a leading Project column and carries the classification and
    follow-up subsections; a single-project call renders the same shape without
    the Project column.
    """
    multi = len(projects) > 1
    names = projects if projects else [""]
    project_col = "Project | " if multi else ""
    span = 9 if multi else 8
    rows = []
    blocks = []
    class_rows = []
    followup_rows = []
    for index, name in enumerate(names):
        number = index + 1
        fnd_id = f"FND-SEC-{number:03d}"
        rec_id = f"REC-{number:03d}"
        cells = f"{name} | " if multi else ""
        suffix = f" ({name})" if name else ""
        rows.append(
            f"| {cells}{rec_id} | P1 | {fnd_id} | <recommendation> | <impact> |"
            " <effort> | <complexity> | None | <verification step> |\n"
        )
        blocks.append(
            REC_BLOCK.format(suffix=suffix, target=fnd_id, rec_id=rec_id) + "\n"
        )
        class_rows.append(
            f"| {cells}{rec_id} | <action> | Recommended | {fnd_id} - <short reason> |\n"
        )
        followup_rows.append(
            f"| {cells}{fnd_id} | P1 | <verifiable artifact> | <milestone> |\n"
        )
    return [
        heading(2, "Remediation Roadmap"),
        table(
            f"| {project_col}Rec | Priority | Finding | Recommendation | Impact |"
            " Effort | Complexity | Breaking | Verification |",
            "|---|" + "---|" * span,
            rows,
        ),
        *blocks,
        heading(3, "Recommendation Classification"),
        table(
            f"| {project_col}Rec | Recommendation | Class | Basis |",
            "|---|" + "---|" * (4 if multi else 3),
            class_rows,
        ),
        heading(3, "Follow-up Plan"),
        table(
            f"| {project_col}Finding | Priority | Evidence | Trigger |",
            "|---|" + "---|" * (4 if multi else 3),
            followup_rows,
        ),
    ]


def audit_shared_tail(multi: bool, projects: list[str] | None = None) -> list[str]:
    parts: list[str] = []
    if multi:
        parts += [
            heading(2, "Solution Comparison"),
            "Cross-project trade-offs only - decisions made once that bind several "
            "projects.\n\n",
            table(
                "| Project | Trade-off | Context | Option A: gain / cost |"
                " Option B: gain / cost | Evidence | Implication |",
                "|---|---|---|---|---|---|---|",
            ),
        ]
    parts += [
        heading(2, "Scope Exclusions"),
        "- Glossary omitted - Descriptive mode disabled.\n\n",
        heading(2, "Known Limitations"),
        "- <each check that would require execution and was not performed>\n\n",
        heading(2, "Further Verification"),
        "Every material claim the audit could not resolve from source, with the\n"
        "exact command or procedure and its pass criteria.\n\n",
        heading(2, "Validation Protocol"),
        validation_record(),
    ]
    parts += roadmap_sections(list(projects or []))
    parts += [
        heading(2, "Reference Sources"),
        table(
            "| Reference | Publisher or Author | Used In |",
            "|---|---|---|",
            ["| <title> | <publisher or author> | <section names> |\n"],
        ),
        "- [<title>](<url>)\n",
    ]
    return parts


def qualified(project: str, fnd_id: str) -> str:
    return f"{project}::{fnd_id}" if project else fnd_id


def hunt_skeleton(projects: list[str], params: dict) -> str:
    multi = len(projects) > 1
    parts = [
        "# <subject> - Lens hunt report\n\n",
        heading(2, "Document Information"),
        document_info("hunt", projects, params),
        heading(2, "Audit Coverage"),
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
                targets=qualified(projects[0] if multi else "", "FND-SEC-001"),
                fnd_id="FND-SEC-001",
            )
            + "\n"
        )
    parts += [
        heading(2, "Risk Register"),
        RISK_BLOCK.format(
            suffix=f" ({projects[0]})" if multi else "",
            rsk_id="RSK-001",
            fnd_id="FND-SEC-001",
        ) + "\n",
        heading(2, "Remediation Phases"),
        heading(3, "Stabilize"),
        table(
            "| Rec | Recommendation | Resolves | Effort | Breaking |",
            "|---|---|---|---|---|",
            [f"| REC-001 | <recommendation> | {qualified(projects[0] if multi else '', 'FND-SEC-001')} | <effort> | None |\n"],
        ),
        REC_BLOCK.format(
            suffix=f" ({projects[0]})" if multi else "",
            target=qualified(projects[0] if multi else "", "FND-SEC-001"),
            rec_id="REC-001",
        )
        + "\n",
        heading(3, "Accepted - no action"),
        table("| Finding | Disposition |", "|---|---|"),
        heading(2, "Further Verification"),
        "Every material claim the hunt could not resolve from source, with the\n"
        "exact command or procedure and its pass criteria.\n\n",
        heading(2, "Scope Exclusions"),
        "- Glossary omitted - Descriptive mode disabled.\n\n",
        heading(2, "Known Limitations"),
        "- <each check that would require execution and was not performed>\n\n",
        heading(2, "Validation Protocol"),
        validation_record(),
        heading(2, "Reference Sources"),
        table(
            "| Reference | Publisher or Author | Used In |",
            "|---|---|---|",
            ["| <title> | <publisher or author> | <section names> |\n"],
        ),
        "- [<title>](<url>)\n",
    ]
    return "".join(parts)


HUNT_FINDING_BLOCK = FINDING_BLOCK

REVIEW_FINDING_BLOCK = HUNT_FINDING_BLOCK.replace(
    "* **Evidence:**",
    "* **Evidence level:** Source - <inspected basis>\n* **Evidence:**",
)


def review_skeleton(projects: list[str], params: dict) -> str:
    multi = len(projects) > 1
    executed = params.get("evidence_mode", "source-only") != "source-only"
    suffix = f" ({projects[0]})" if multi else ""
    target = qualified(projects[0] if multi else "", "FND-SEC-001")
    parts = [
        "# <subject> - Lens review report\n\n",
        heading(2, "Document Information"),
        document_info("review", projects, params),
        heading(2, "Audit Coverage"),
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
        "Checks selected, the criteria entry each evaluates, the evidence level each reaches, "
        "and the commands the user commissioned:\n\n",
        table("| Check | Criteria | Evidence level |", "|---|---|---|"),
        "Read-depth table:\n\n",
        table("| Area | Files | Read depth |", "|---|---|---|"),
        "Evidence ledger:\n\n",
        ledger_table(multi),
        heading(2, "Execution Register"),
        "One row per check.\n\n"
        "`Result` is Pass, Fail, Error, Blocked, Skipped, Not run, or N/A - "
        "`Error`/`Blocked` are runner states, never product failures, and "
        "`Not run` is never a pass.\n\n"
        "Every non-Pass row states its Interpretation.\n\n",
        table(
            "| Check | Command | Cwd | Tool & Version | Timestamp | Input revision | Exit status | Result | Interpretation | Artifact |",
            "|---|---|---|---|---|---|---|---|---|---|",
            [
                "| <check> | <exact command> | <cwd> | <tool and version> | <timestamp> | "
                "<revision> | <exit code> | Not run | <why or outcome meaning> | <artifact or `None retained`> |\n"
            ],
        ),
        heading(2, "Domain Findings"),
        finding_summary_table(projects),
        heading(3, "Security"),
        REVIEW_FINDING_BLOCK.format(suffix=suffix, targets=target, fnd_id="FND-SEC-001") + "\n",
        heading(2, "Risk Register"),
        RISK_BLOCK.format(suffix=suffix, rsk_id="RSK-001", fnd_id="FND-SEC-001") + "\n",
        heading(2, "Improvement Plan"),
        heading(3, "Stabilize"),
        table(
            "| Rec | Recommendation | Resolves | Effort | Breaking |",
            "|---|---|---|---|---|",
            [f"| REC-001 | <recommendation> | {target} | <effort> | None |\n"],
        ),
        REC_BLOCK.format(suffix=suffix, target=target, rec_id="REC-001") + "\n",
        heading(3, "Accepted - no action"),
        table("| Finding | Disposition |", "|---|---|"),
        heading(2, "Retest Register"),
        "One row per `Fail`, `Error`, or `Blocked` register row - omit the section when "
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
            heading(2, "Further Verification"),
            "Checks outside the commissioned set, with the exact command or procedure "
            "and its pass criteria.\n\n",
        ]
    else:
        parts += [
            heading(2, "Further Verification"),
            "Every material claim the review could not resolve from source, with the\n"
            "exact command or procedure and its pass criteria.\n\n",
        ]
    parts += [
        heading(2, "Scope Exclusions"),
        "- Glossary omitted - Descriptive mode disabled.\n"
        "- Artifact Manifest omitted - `source-only` evidence mode retains no "
        "artifacts.\n\n"
        if not executed
        else "- Glossary omitted - Descriptive mode disabled.\n\n",
        heading(2, "Known Limitations"),
        "- <each check that stayed NOT RUN and every unresolved unknown>\n\n",
        heading(2, "Validation Protocol"),
        validation_record(),
        heading(2, "Reference Sources"),
        table(
            "| Reference | Publisher or Author | Used In |",
            "|---|---|---|",
            ["| <title> | <publisher or author> | <section names> |\n"],
        ),
        "- [<title>](<url>)\n",
    ]
    return "".join(parts)


STR_FINDING_BLOCK = FINDING_BLOCK.replace(
    "* **Pillar:** Security & Compliance", "* **Pillar:** Structure & Organization"
)


def structure_review_skeleton(projects: list[str], params: dict) -> str:
    parts = [
        "# <subject> - Lens structure review report\n\n",
        heading(2, "Document Information"),
        document_info("review", projects, {**params, "review_scope": "structure"}),
        heading(2, "Project Context"),
        table(
            "| Field | Value |",
            "|---|---|",
            [
                "| Language | <primary and secondary languages> |\n",
                "| Framework and libraries | <framework or `none`, structure-shaping libraries> |\n",
                "| Application type | <backend service, web application, library, CLI, ...> |\n",
                "| Architectural approach | <layered, feature-based, modular monolith, ...> |\n",
                "| Project scale | <module count, size, growth expectation> |\n",
                "| Build and deployment model | <build, packaging, deployment shape> |\n",
                "| Constraints | <conventions or tooling the structure must satisfy> |\n",
            ],
        ),
        heading(2, "Structural Overview"),
        "<concise description of the existing directory, file, and component organization>\n\n",
        table(
            "| Level | Directory | Contents | Role |",
            "|---|---|---|---|",
            ["| 1 | <directory> | <contents> | <role> |\n"],
        ),
        heading(2, "Findings"),
        STR_FINDING_BLOCK.format(suffix="", targets="FND-STR-001", fnd_id="FND-STR-001") + "\n",
        heading(2, "Positive Practices"),
        table(
            "| Practice | Evidence |",
            "|---|---|",
            ["| <organizational decision worth preserving> | <path or citation> |\n"],
        ),
        heading(2, "Recommendations"),
        table(
            "| Recommendation | Rationale | Addresses |",
            "|---|---|---|",
            ["| <proportionate change> | <why> | FND-STR-001 |\n"],
        ),
        heading(2, "Prioritization"),
        table(
            "| Recommendation | Class |",
            "|---|---|",
            ["| <recommendation> | <Necessary, Meaningful, or Optional> |\n"],
        ),
        heading(2, "Limitations and Assumptions"),
        "- <areas that could not be evaluated and assumptions the verdicts rest on>\n\n",
        heading(2, "Validation Protocol"),
        validation_record(),
        heading(2, "Reference Sources"),
        table(
            "| Reference | Publisher or Author | Used In |",
            "|---|---|---|",
            ["| <title> | <publisher or author> | <section names> |\n"],
        ),
        "- [<title>](<url>)\n",
    ]
    return "".join(parts)




DIMENSION_ORDER = [
    "Functional Suitability", "Testability", "Design Soundness", "Code Quality",
    "Code Style", "Stack Alignment", "Dependency Health", "Maintainability",
    "Structure", "Deployability", "Scalability", "Security", "Compliance",
    "Observability", "Operational Safety", "Documentation",
    "API Compatibility", "Delivery & Continuity", "Originality & Licensing",
    "Skill Definition",
]

PILLAR_LABELS = {
    "ARC": "Architecture & Design", "CQY": "Code Quality",
    "SEC": "Security & Compliance", "INF": "Delivery & Operations",
    "AIP": "AI Provenance", "CPR": "Licensing & Provenance",
    "API": "API Compatibility", "STR": "Structure",
}


def _pillar(fnd_id: str) -> str:
    parts = fnd_id.split("-")
    return PILLAR_LABELS.get(parts[1], "Security & Compliance") if len(parts) > 2 else "Security & Compliance"


def _clean(text: str) -> str:
    """Sanitize model text for report prose - no semicolons, no trailing space."""
    return re.sub(r"\s{2,}", " ", str(text).replace(";", ",")).strip()


def populate_audit(body: str, model: dict) -> str:
    """Seed an audit skeleton's model-driven cells from ``audit-model.json``.

    Fills the scorecard, executive-summary score cells, finding/risk/rec
    registers, requirements table, criteria table, evidence ledger, and the
    executed-evidence log. Author prose, exclusions, and limitations stay as
    placeholders.
    """
    scores = model.get("scores", {})
    scale = int(scores.get("scale_max", 10))
    dims = scores.get("dimensions", {})
    rows = []
    for name in DIMENSION_ORDER:
        key = name.lower().replace(" & ", "_").replace(" ", "_")
        cell = dims.get(key, {})
        if not cell or not cell.get("eligible", True):
            continue
        rows.append(f"| {name} | {cell['score']}/{scale} |  |\n")
    if rows:
        body = body.replace(
            "| Dimension | Score | Notes |\n|---|---|---|\n",
            "| Dimension | Score | Notes |\n|---|---|---|\n" + "".join(rows),
            1,
        )
    prod = scores.get("product", {})
    proc = scores.get("process", {})
    single = scores.get("single", {})
    scale_max = scores.get("scale_max", 10)
    if prod.get("score") is not None:
        body = body.replace(
            "| Product Quality | <score>/<scale> (<band>) | <formula>, lowest <dimension> <score> |",
            f"| Product Quality | {prod['score']}/{scale_max} | tier-weighted, lowest "
            f"{', '.join(prod.get('lowest') or ['-'])} |",
            1,
        )
        body = body.replace(
            "| Engineering Process | <score>/<scale> (<band>) or Not published | <formula>, lowest <dimension> <score> |",
            f"| Engineering Process | {proc['score']}/{scale_max} | mean of {proc.get('scored','?')} dimensions, lowest "
            f"{', '.join(proc.get('lowest') or ['-'])} |",
            1,
        )
        ceiling = (single.get("ceiling") or {}).get("reasons")
        ceiling_text = f"ceiling {ceiling}" if ceiling else "blend"
        body = body.replace(
            "| Overall Score | <score>/<scale> (<band>) or Not published | <blend, Product-only, ceiling wording> |",
            f"| Overall Score | {single['score']}/{scale_max} ({single.get('band','')}) | {ceiling_text}, raw {single.get('raw','?')} |",
            1,
        )
        body = body.replace(
            "| Overall score | <mean>/<scale> (<band>) |",
            f"| Overall score | {single['score']}/{scale_max} ({single.get('band','')}) |",
            1,
        )
    findings = model.get("findings", [])
    subject = model.get("scope", {}).get("subject", "<subject>")
    if findings:
        summary_rows = "".join(
            f"| {f['id']} | {_pillar(f['id'])} | {f['severity'].title()} | {_clean(f.get('observation',''))[:60]} |"
            f" {_clean(f.get('claim_class',''))} | Open | New | "
            f"{'Confirmed' if any(e.get('kind')=='EXECUTED' for e in model.get('evidence',[]) if e.get('id') in f.get('evidence',[])) else ('Verification' if f.get('confidence')=='HIGH' else '')} |\n"
            for f in findings
        )
        body = re.sub(
            r"\| FND-[A-Z]+-001 \| [^\n]*<severity>[^\n]*\|\n",
            summary_rows, body, count=1,
        )
        blocks = ""
        for f in findings:
            evidence = ", ".join(f.get("evidence", [])) or "<EVD IDs>"
            verification = ""
            if any(
                e.get("kind") == "EXECUTED"
                for e in model.get("evidence", [])
                if e.get("id") in f.get("evidence", [])
            ):
                verification = "* **Runtime:** Confirmed - executed evidence\n"
            elif f.get("confidence") == "HIGH":
                verification = "* **Verification:** Verified - source inspection\n"
            absence = f"* **Absence:** {f['absence']}\n" if f.get("absence") else ""
            blocks += (
                f"### {f['id']}: {_clean(f.get('observation',''))[:70]}\n\n"
                f"{_clean(f.get('observation',''))}\n\n"
                f"* **Pillar:** {_pillar(f['id'])}\n"
                f"* **Severity:** {f['severity'].title()}\n"
                f"* **Type:** {f.get('type','Concern')}\n"
                f"* **Targets:** {subject}\n"
                f"* **Basis:** Inspected\n"
                f"* **Criteria:** {f.get('criteria','')}\n"
                f"* **Impact:** {_clean(f.get('consequence',''))}\n"
                f"* **Method:** {_clean(f.get('next_verification',''))}\n"
                f"{verification}"
                f"* **Confidence:** {f.get('confidence','').title()}\n"
                f"* **Mitigating factors:** {_clean(f.get('counter',''))}\n"
                f"* **Evidence:** {evidence}\n"
                f"* **Recommendation:** {_clean(f.get('next_verification',''))}\n"
                f"{absence}\n"
            )
        body = re.sub(
            r"### FND-[A-Z]+-001:.*?(?=### |## |\Z)",
            blocks.rstrip() + "\n\n", body, count=1, flags=re.S,
        )
    risks = model.get("risks", [])
    if risks:
        blocks = ""
        for r in risks:
            blocks += (
                f"### {r['id']}: {_clean(r.get('impact',''))[:60]}\n\n"
                f"{_clean(r.get('impact',''))}.\n\n"
                f"* **Severity:** {r.get('severity','').title()}\n"
                f"* **Likelihood:** {_clean(r.get('likelihood',''))}\n"
                f"* **Residual:** {r.get('severity','').title()}\n"
                f"* **Impact:** {_clean(r.get('impact',''))}\n"
                f"* **Trigger:** {_clean(r.get('prerequisites',''))}\n"
                f"* **Controls:** {_clean(r.get('controls',''))}\n"
                f"* **Closure:** {_clean(r.get('closure','<closure condition>'))}\n"
                f"* **Source:** {r.get('finding','')}\n"
                f"* **Confidence:** {r.get('uncertainty','').title()}\n"
                f"* **Mitigation:** {_clean(r.get('mitigation','<treatment plan>'))}\n\n"
            )
        body = re.sub(
            r"### RSK-001:.*?(?=### |## |\Z)",
            blocks.rstrip() + "\n\n", body, count=1, flags=re.S,
        )
    recs = model.get("recommendations", [])
    if recs:
        blocks = ""
        for r in recs:
            blocks += (
                f"### {r['id']}: {_clean(r.get('postcondition',''))[:60]}\n\n"
                f"{_clean(r.get('postcondition',''))}.\n\n"
                f"* **Priority:** {r.get('priority','P3')}\n"
                f"* **Finding:** {r.get('finding','')}\n"
                f"* **Condition:** {_clean(r.get('postcondition',''))}\n"
                f"* **Impact:** {_clean(r.get('residual','closes the finding'))}\n"
                f"* **Effort:** {r.get('effort','M')}\n"
                f"* **Complexity:** low\n"
                f"* **Verification:** {_clean(r.get('verification',''))}\n\n"
            )
        body = re.sub(
            r"### REC-001:.*?(?=### |## |\Z)",
            blocks.rstrip() + "\n\n", body, count=1, flags=re.S,
        )
        roadmap_rows = "".join(
            f"| {r['id']} | {r.get('priority','P3')} | {r.get('finding','')} |"
            f" {_clean(r.get('options',''))} | {_clean(r.get('residual',''))} |"
            f" {r.get('effort','M')} | low | None | {_clean(r.get('verification',''))} |\n"
            for r in recs
        )
        body = re.sub(
            r"\| REC-001 \| P1 \| FND-[A-Z]+-001 \|[^\n]*\|\n",
            roadmap_rows, body, count=1,
        )
        class_rows = "".join(
            f"| {r['id']} | {_clean(r.get('postcondition',''))[:50]} |"
            f" {'Optional' if r.get('priority') == 'P4' else 'Recommended'} | {r.get('finding','')} |\n"
            for r in recs
        )
        body = re.sub(
            r"\| REC-001 \| <action> \| Recommended \| FND-[A-Z]+-001[^\n]*\|\n",
            class_rows, body, count=1,
        )
        follow_rows = "".join(
            f"| {r.get('finding','')} | {r.get('priority','P3')} | {_clean(r.get('verification',''))} | {r['id']} |\n"
            for r in recs
        )
        body = re.sub(
            r"\| FND-[A-Z]+-001 \| P1 \| <verifiable artifact> \| <milestone> \|\n",
            follow_rows, body, count=1,
        )
    evidence = model.get("evidence", [])
    if evidence:
        ledger_rows = "".join(
            f"| {e['id']} | {_clean(e.get('method',''))} - `{e.get('locator',{}).get('path','')}` |"
            f" {_clean(e.get('result',''))[:120]} | {e.get('type','Observation')} | <artifact> |\n"
            for e in evidence
        )
        ledger = "## Evidence Ledger\n\n| Evidence | Source | Result | Type | Artifact |\n|---|---|---|---|---|\n" + ledger_rows + "\n"
        body = body.replace("## Validation Protocol", ledger + "\n## Validation Protocol", 1)
    executed = [e for e in evidence if e.get("kind") == "EXECUTED"]
    executed_rows = "".join(
        f"| {_clean(e.get('method',''))[:40]} | `{_clean(e.get('locator',{}).get('path',''))}` |"
        f" {'Pass' if 'PASS' in str(e.get('result','')).upper()[:10] else 'Fail'} | {_clean(e.get('result',''))[:140]} |\n"
        for e in executed
    )
    if executed:
        executed_log = (
            "## Executed Evidence\n\n"
            "| Check | Command | Result | Interpretation |\n|---|---|---|---|\n"
            + executed_rows + "\n"
        )
        body = body.replace("## Further Verification", executed_log, 1)
        body = re.sub(
            r"Every material claim the audit could not resolve from source, with the\n"
            r"exact command or procedure and its pass criteria\.\n",
            "", body, count=1,
        )
    criteria = model.get("criteria", [])
    if criteria and findings:
        crit_rows = "".join(
            f"| {c['id']} | {c.get('dimension','')} | {c.get('weight','')} | {c.get('criticality','')} | {c.get('outcome','')} |\n"
            for c in criteria if c.get("outcome") not in ("PASS", "NOT_APPLICABLE")
        )
        if crit_rows:
            crit_table = (
                "**Criteria table**\n\n"
                "| Criteria | Dimension | Weight | Criticality | Outcome |\n|---|---|---|---|---|\n"
                + crit_rows + "\n"
            )
            body = body.replace(
                "## Scoring Rubrics", crit_table + "\n## Scoring Rubrics", 1
            )
    body = re.sub(r"[ \t]+$", "", body, flags=re.M)
    body = re.sub(r"\n{3,}", "\n\n", body)
    requirements = model.get("requirements", [])
    if requirements:
        req_rows = "".join(
            f"| {r['id']} | {r.get('obligation','')} | "
            f"{'Partial' if r.get('status') == 'PARTIAL' else r.get('status','Pass').title()} |"
            f" <basis> |\n"
            for r in requirements
        )
        body = body.replace("## Standards Conformance", "## Requirements Conformance\n\n| Requirement | Obligation | Status | Basis |\n|---|---|---|---|\n" + req_rows + "\n## Standards Conformance", 1)
    return body


def parse_args(argv: list[str]) -> dict:
    options: dict = {"style": None, "scope": None, "projects": [], "params": None, "output": None, "model": None}
    index = 1
    while index < len(argv):
        argument = argv[index]
        if argument in ("--style", "--scope", "--projects", "--params", "--output", "--model"):
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
    if style not in ("audit", "hunt", "review"):
        print(f"unknown style '{style}' - expected audit, hunt, or review")
        return 1
    scope = options["scope"] or params.get("review_scope") or "full"
    if scope != "structure" and scope != "full":
        print(f"unknown scope '{scope}' - expected full or structure")
        return 1
    if scope == "structure" and style != "review":
        print("--scope structure only applies to --style review")
        return 1
    projects = (
        [name.strip() for name in options["projects"].split(",") if name.strip()]
        if options["projects"]
        else list(params.get("projects", []))
    )
    if style == "hunt":
        body = hunt_skeleton(projects, params)
    elif style == "review" and scope == "structure":
        body = structure_review_skeleton(projects, params)
    elif style == "review":
        body = review_skeleton(projects, params)
    else:
        body = audit_skeleton(projects, params)
        if options["model"]:
            model = json.loads(Path(options["model"]).read_text(encoding="utf-8"))
            body = populate_audit(body, model)
    if options["output"]:
        target = Path(options["output"])
        target.write_text(body, encoding="utf-8")
        linker = find_tool("link-references")
        if linker is not None:
            subprocess.run([sys.executable, str(linker), str(target)], check=False)
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
