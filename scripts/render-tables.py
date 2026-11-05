#!/usr/bin/env python3
"""Render `audit-model.json` sections as source-width-aligned Markdown tables.

Produces the Scorecard Summary, the headline score rows, the frozen criteria
table, and the requirements registry table for a single-project model, or for
one project of a multi-project model with `--project`.

Usage:
    python3 scripts/render-tables.py <audit-model.json> \
        --part scorecard|headline|criteria|requirements|all \
        [--project NAME] [--lang en|pl] [--output FILE]

Exit code 0 means the render ran, 2 means usage or read errors.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

DIMENSIONS = [
    ("functional_suitability", "Functional Suitability", "product"),
    ("testability", "Testability", "product"),
    ("design_soundness", "Design Soundness", "product"),
    ("code_quality", "Code Quality", "product"),
    ("code_style", "Code Style", "product"),
    ("stack_alignment", "Stack Alignment", "product"),
    ("dependency_health", "Dependency Health", "product"),
    ("maintainability", "Maintainability", "product"),
    ("structure", "Structure", "product"),
    ("deployability", "Deployability", "product"),
    ("scalability", "Scalability", "product"),
    ("security", "Security", "product"),
    ("compliance", "Compliance", "product"),
    ("observability", "Observability", "product"),
    ("operational_safety", "Operational Safety", "product"),
    ("api_compatibility", "API Compatibility", "product"),
    ("delivery_continuity", "Delivery & Continuity", "process"),
    ("ai_provenance", "AI Provenance", "process"),
    ("originality_licensing", "Originality & Licensing", "process"),
    ("skill_definition", "Skill Definition", "process"),
]
DIMENSION_ORDER = [ident for ident, _, _ in DIMENSIONS]
DIMENSION_NAMES = {ident: name for ident, name, _ in DIMENSIONS}
DIMENSION_GROUP = {ident: group for ident, _, group in DIMENSIONS}

BANDS = {
    10: ((9, "Excellent"), (7, "Good"), (4, "Average"), (1, "Poor")),
    5: ((5, "Excellent"), (4, "Good"), (3, "Average"), (2, "Poor"), (1, "Bad")),
    3: ((3, "Excellent"), (2, "Average"), (1, "Poor")),
}
CATALOGUE_FILE = "references/criterion-catalogue.json"


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    """One Markdown table with format-table.py source-width alignment."""
    widths = [len(h) for h in headers]
    for row in rows:
        for j, cell in enumerate(row):
            widths[j] = max(widths[j], len(cell))
    lines = [
        "| " + " | ".join(h.ljust(widths[j]) for j, h in enumerate(headers))
        + " |",
        "|" + "|".join("-" * (w + 2) for w in widths) + "|",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(c.ljust(widths[j]) for j, c in enumerate(row))
            + " |"
        )
    return "\n".join(lines)


def band_of(score: float, scale_max: int) -> str:
    """Band label for the half-up integer of a headline score."""
    value = int(math.floor(Fraction(str(score)) + Fraction(1, 2)))
    for floor, name in BANDS.get(scale_max, BANDS[10]):
        if value >= floor:
            return name
    return BANDS.get(scale_max, BANDS[10])[-1][1]


def score_value(score, scale_max: int, interval) -> str:
    cell = f"{float(score):.1f}/{scale_max} ({band_of(score, scale_max)})"
    if interval:
        cell += f" [{interval[0]:g}-{interval[1]:g}]"
    return cell


def load_catalogue() -> dict:
    """Best-effort catalogue load for criteria ordering; {} when absent."""
    path = Path(__file__).resolve().parent.parent / CATALOGUE_FILE
    if not path.is_file():
        return {}
    try:
        catalogue = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return catalogue if isinstance(catalogue, dict) else {}


def scope_records(model: dict, project: str | None) -> dict:
    scores = model.get("scores", {})
    if project is None:
        return scores
    record = scores.get("per_project", {}).get(project)
    return record if isinstance(record, dict) else {}


def render_scorecard(model: dict, project: str | None) -> str:
    scores = model.get("scores", {})
    scale_max = scores.get("scale_max", 10)
    dims = scores.get("dimensions", {})
    prefix = f"{project}." if project else ""
    rows = []
    for ident in DIMENSION_ORDER:
        record = dims.get(prefix + ident)
        if record is None or record.get("applicable") is False:
            continue
        score = record.get("score")
        if score is None:
            cell = "Unknown"
        else:
            cell = f"{score}/{scale_max}"
            interval = record.get("interval")
            if interval:
                cell += f" [{interval[0]:g}-{interval[1]:g}]"
        rows.append(
            [DIMENSION_NAMES[ident], cell, str(record.get("note") or "-")]
        )
    return render_table(["Dimension", "Score", "Notes"], rows)


def _lowest_clause(records: dict, lowest: list, prefix: str, scale_max: int) -> str:
    dims = records.get("dimensions", {})
    names = []
    for ident in lowest:
        record = dims.get(f"{prefix}{ident}") or dims.get(ident) or {}
        score = record.get("score")
        names.append(
            f"{DIMENSION_NAMES.get(ident, ident)} "
            + (f"{score:g}/{scale_max}" if score is not None else "Unknown")
        )
    return ", lowest " + ", ".join(names)


def render_headline(model: dict, project: str | None) -> str:
    scores = model.get("scores", {})
    scale_max = scores.get("scale_max", 10)
    prefix = f"{project}." if project else ""
    records = scope_records(model, project)
    product = records.get("product", {})
    process = records.get("process", {})
    single = records.get("single", {})
    dims = scores.get("dimensions", {})
    count = {}
    for group in ("product", "process"):
        count[group] = sum(
            1 for ident in DIMENSION_ORDER
            if DIMENSION_GROUP[ident] == group
            and dims.get(prefix + ident) is not None
            and dims[prefix + ident].get("applicable", True)
        )

    if product.get("published"):
        value = score_value(
            product.get("score"), scale_max, product.get("interval")
        )
        basis = (
            f"Tier-weighted mean of {count['product']} product dimensions"
            + _lowest_clause(scores, product.get("lowest", []), prefix, scale_max)
        )
    else:
        value = "Not published"
        basis = (
            f"tier weight {product.get('eligible_weight', 0)} of "
            f"{product.get('applicable_weight', 0)} eligible"
        )
    product_row = ["Product Quality", value, basis]

    if process.get("published"):
        value = score_value(
            process.get("score"), scale_max, process.get("interval")
        )
        basis = (
            f"Equal-weight mean of {count['process']} process dimensions"
            + _lowest_clause(scores, process.get("lowest", []), prefix, scale_max)
        )
    else:
        value = "Not published"
        basis = (
            f"{process.get('scored', 0)} of "
            f"{process.get('applicable', 0)} applicable process dimensions "
            "scored"
        )
    process_row = ["Engineering Process", value, basis]

    if single.get("score") is None:
        single_row = ["Overall Score", "Not published", "-"]
    else:
        value = score_value(
            single.get("score"), scale_max, single.get("interval")
        )
        parts = []
        if single.get("flag") == "product-only":
            parts.append("Product-only")
        else:
            parts.append("7/10 product + 3/10 process")
        ceiling = single.get("ceiling")
        if isinstance(ceiling, dict):
            reasons = ", ".join(
                str(r).replace(":", " ") for r in ceiling.get("reasons", [])
            )
            parts.append(f"ceiling {ceiling.get('limit')}: {reasons}")
        single_row = ["Overall Score", value, ", ".join(parts)]

    return render_table(
        ["Score", "Value", "Basis"], [product_row, process_row, single_row]
    )


def render_criteria(model: dict, project: str | None, catalogue: dict) -> str:
    criteria = [
        c for c in model.get("criteria", []) if c.get("channel") == "score"
    ]
    if project is not None:
        criteria = [
            c for c in criteria
            if str(c.get("dimension", "")).startswith(project + ".")
        ]
    order = [
        entry.get("id") for entry in catalogue.get("criteria", [])
    ]
    criteria.sort(
        key=lambda c: (
            order.index(c.get("catalogue_id"))
            if c.get("catalogue_id") in order else len(order)
        )
    )
    rows = []
    for c in criteria:
        dimension = str(c.get("dimension", ""))
        leaf = dimension.partition(".")[2] if "." in dimension else dimension
        weight = c.get("weight")
        rows.append(
            [
                str(c.get("id", "")),
                DIMENSION_NAMES.get(leaf, leaf),
                f"{weight:g}" if isinstance(weight, (int, float)) else str(weight),
                str(c.get("level") or "-"),
                str(c.get("outcome") or "-"),
            ]
        )
    return render_table(
        ["Criteria", "Dimension", "Weight", "Level", "Outcome"], rows
    )


def render_requirements(model: dict, project: str | None) -> str:
    rows = []
    for r in model.get("requirements", []):
        evidence = r.get("evidence", [])
        rows.append(
            [
                str(r.get("id", "")),
                str(r.get("obligation", "")),
                str(r.get("status", "")),
                ", ".join(str(e) for e in evidence) if evidence else "-",
            ]
        )
    return render_table(
        ["Requirement", "Obligation", "Status", "Evidence"], rows
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Render audit-model.json sections as Markdown tables"
    )
    parser.add_argument("model", help="path to the audit-model.json file")
    parser.add_argument(
        "--part",
        required=True,
        choices=("scorecard", "headline", "criteria", "requirements", "all"),
        help="which table(s) to render",
    )
    parser.add_argument(
        "--project", help="render one project of a multi-project model"
    )
    parser.add_argument(
        "--lang", default="en", choices=("en", "pl"), help="table language"
    )
    parser.add_argument("--output", help="write to FILE instead of stdout")
    args = parser.parse_args(argv)

    if args.lang == "pl":
        print(
            "render-tables: --lang pl has no translation keys yet - rendering "
            "English labels",
            file=sys.stderr,
        )

    path = Path(args.model)
    if not path.is_file():
        print(f"render-tables: no such file: {args.model}", file=sys.stderr)
        return 2
    try:
        model = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"render-tables: cannot parse {args.model}: {exc}", file=sys.stderr)
        return 2
    if not isinstance(model, dict):
        print("render-tables: top-level value is not an object", file=sys.stderr)
        return 2

    if args.project is not None:
        names = {
            p.get("name")
            for p in model.get("scope", {}).get("projects", [])
            if isinstance(p, dict) and p.get("name")
        }
        known = names | set(
            model.get("scores", {}).get("per_project", {})
        )
        if args.project not in known:
            print(
                f"render-tables: unknown project {args.project!r}",
                file=sys.stderr,
            )
            return 2

    catalogue = load_catalogue()
    parts = {
        "scorecard": lambda: render_scorecard(model, args.project),
        "headline": lambda: render_headline(model, args.project),
        "criteria": lambda: render_criteria(model, args.project, catalogue),
        "requirements": lambda: render_requirements(model, args.project),
    }
    selected = (
        list(parts.values()) if args.part == "all" else [parts[args.part]]
    )
    text = "\n\n".join(render() for render in selected) + "\n"

    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
