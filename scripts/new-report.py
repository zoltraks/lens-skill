"""Generate a Lens report skeleton.

Emits a structurally complete report scaffold - every required heading, the
table headers the validator expects, and one field-labeled template block per
register - so an author starts from the enforced contract instead of a blank
file. Placeholder cells carry ``<...>`` markers: content-bearing checks fail
until the author replaces them, which is deliberate.

Usage:
  python new-report.py --style audit|hunt|review [--scope structure]
                       [--projects a,b] [--params file] [--output report.md]

``--params`` reads a saved intake file (``work/lens-params.json``) carrying
``report_style``, ``review_scope``, ``projects``, ``subject``, ``revision``,
``language``, and ``detail_level`` so a second report in the same session
reuses the locked intake values. Command-line options override the file.
``--scope structure`` with ``--style review`` emits the structure-review
variant contract instead of the execution-register one.
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
    ("Verification Scope", "Static repository analysis - no execution"),
    ("Evidence Mode", "Source-only"),
    ("Subject Revision", "<commit> (branch <branch>)"),
    ("Skill Version", "<version>"),
    ("State", "Draft"),
]

COVERAGE_HEADER = "| Report type | Status | Rationale |\n|---|---|---|\n"

FINDING_BLOCK = """### {fnd_id}: <finding title>{suffix}

<what the discovered state is, where, and why it is a finding>

* **Pillar:** Security & Compliance
* **Severity:** <Critical | High | Medium | Low>
* **Type:** Concern
* **Targets:** {targets}
* **Basis:** <requirement or source basis>
* **Criteria:** <criterion ID - violated or uncertain property>
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
    for number in range(1, 31)
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
            value = style.capitalize()
        elif field == "Detail Level":
            value = params.get("detail_level", "Standard")
        elif field == "Evidence Mode":
            value = params.get("evidence_mode", "Source-only")
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
        parts += audit_shared_tail(multi)
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
    rec_id = f"REC-{number:03d}"
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
                    "| Impact | Low | Medium | High |",
                    "|---|---|---|---|",
                    ["| Critical |  |  |  |\n", "| High |  |  |  |\n",
                     "| Medium |  |  |  |\n", "| Low |  |  |  |\n"],
                )
            )
            parts.append("**Scorecard Summary**\n\n")
            parts.append(table("| Dimension | Score | Notes |", "|---|---|---|"))
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
    parts.append(heading(level, "Remediation Roadmap"))
    parts.append(
        table(
            "| Rec | Priority | Finding | Recommendation | Impact | Effort | Complexity | Breaking | Verification |",
            "|---|---|---|---|---|---|---|---|---|",
            [f"| {rec_id} | P1 | {fnd_id} | <recommendation> | <impact> | <effort> | <complexity> | None | <verification step> |\n"],
        )
    )
    parts.append(REC_BLOCK.format(suffix=suffix, target=qualified(project, fnd_id), rec_id=rec_id) + "\n")
    parts.append(heading(level, "Recommendation Classification"))
    parts.append(
        table(
            "| Rec | Recommendation | Class | Basis |",
            "|---|---|---|---|",
            [f"| {rec_id} | <action> | Recommended | {fnd_id} - <short reason> |\n"],
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
        table(
            "| Reference | Publisher or Author | Used In |",
            "|---|---|---|",
            ["| <title> | <publisher or author> | <section names> |\n"],
        ),
        "- [<title>](<url>)\n\n",
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
        table(
            "| Reference | Publisher or Author | Used In |",
            "|---|---|---|",
            ["| <title> | <publisher or author> | <section names> |\n"],
        ),
        "- [<title>](<url>)\n\n",
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
        "Checks selected, the criterion each evaluates, the evidence level each reaches, "
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
            heading(2, "Operator Verification Handoff"),
            "Checks outside the commissioned set, with the exact command or procedure "
            "and its pass criteria.\n\n",
        ]
    else:
        parts += [
            heading(2, "Operator Verification Handoff"),
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
        heading(2, "Limitations and Unknowns"),
        "- <each check that stayed NOT RUN and every unresolved unknown>\n\n",
        heading(2, "Validation Record"),
        validation_record() + "\n",
        heading(2, "References"),
        table(
            "| Reference | Publisher or Author | Used In |",
            "|---|---|---|",
            ["| <title> | <publisher or author> | <section names> |\n"],
        ),
        "- [<title>](<url>)\n\n",
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
    ]
    return "".join(parts)


def parse_args(argv: list[str]) -> dict:
    options: dict = {"style": None, "scope": None, "projects": [], "params": None, "output": None}
    index = 1
    while index < len(argv):
        argument = argv[index]
        if argument in ("--style", "--scope", "--projects", "--params", "--output"):
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
