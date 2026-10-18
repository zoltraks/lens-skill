#!/usr/bin/env python3
"""Model-quality checker for `work/audit-model.json`.

Validates the canonical audit model before report generation: required shape,
referential integrity across evidence/criteria/findings/risks/recommendations,
and recomputation of the scoring engine's outputs (mastery, interval bounds,
coverage, eligibility, overall mean) per `process/readiness-scoring.md`.

Usage:
    python scripts/check-model.py path/to/work/audit-model.json [--json]

Exit code 0 means all checks passed, 1 means model-quality failures, 2 means
usage or parse errors.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

EVIDENCE_KINDS = {
    "DECLARED", "INSPECTED", "STATICALLY_DERIVED",
    "EXECUTED", "MEASURED", "CORROBORATED",
}
SCORING_KINDS = {"INSPECTED", "STATICALLY_DERIVED", "EXECUTED", "MEASURED"}
CRITERION_OUTCOMES = {
    "PASS", "FAIL", "PARTIAL", "UNKNOWN", "NOT_ASSESSED", "NOT_APPLICABLE",
}
CRITERION_ID_SHAPE = re.compile(r"^[A-Z]{3}-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
CRITERION_REDUNDANT_ONE = re.compile(r"^([A-Z]{3}-[A-Z]+(?:-[A-Z]+)*)-(0?1)$")
RESOLVED = {"PASS", "FAIL", "PARTIAL"}
COVERAGE_LABELS = {
    "COMPLETE_FOR_DECLARED_SCOPE", "PARTIAL", "NOT_ASSESSED", "NOT_APPLICABLE",
}
TOP_LEVEL = [
    "model_version", "scope", "inventory", "criteria", "evidence",
    "findings", "risks", "recommendations", "scores", "coverage", "exclusions",
]


def criterion_mastery(criterion: dict) -> float:
    outcome = criterion.get("outcome")
    if outcome == "PASS":
        return 1.0
    if outcome == "FAIL":
        return 0.0
    partial = criterion.get("mastery")
    return float(partial) if isinstance(partial, (int, float)) else 0.0


def recompute_dimension(criteria: list[dict], backing: dict[str, set[str]]):
    """Recompute one dimension's scoring tuple from its criteria."""
    applicable = [c for c in criteria if c.get("outcome") != "NOT_APPLICABLE"]
    resolved = [c for c in applicable if c.get("outcome") in RESOLVED]
    app_weight = sum(float(c.get("weight", 1.0)) for c in applicable)
    res_weight = sum(float(c.get("weight", 1.0)) for c in resolved)

    def mastery_with(fill: float | None) -> float | None:
        if not res_weight:
            return None
        total = 0.0
        for c in applicable:
            if c["outcome"] in RESOLVED:
                total += float(c.get("weight", 1.0)) * criterion_mastery(c)
            elif fill is not None:
                total += float(c.get("weight", 1.0)) * fill
        denom = app_weight if fill is not None else res_weight
        return total / denom if denom else None

    mastery = mastery_with(None)
    lo = mastery_with(0.0)
    hi = mastery_with(1.0)
    coverage = res_weight / app_weight if app_weight else 0.0
    eligible = (
        coverage > 0.5
        and any(
            kind in SCORING_KINDS
            for c in resolved for kind in backing.get(c.get("id"), ())
        )
    )
    return applicable, mastery, lo, hi, coverage, eligible


def check_model(model: dict) -> list[str]:
    failures: list[str] = []
    for key in TOP_LEVEL:
        if key not in model:
            failures.append(f"missing top-level key '{key}'")
    if model.get("model_version") != 1:
        failures.append(f"model_version is {model.get('model_version')!r}, expected 1")
    if failures:
        return failures

    scale_max = model.get("scores", {}).get("scale_max", 10)
    if not isinstance(scale_max, (int, float)) or scale_max <= 0:
        failures.append(f"scores.scale_max is {scale_max!r}, expected a positive number")
        scale_max = 10

    criteria = model["criteria"]
    evidence = model["evidence"]
    findings = model["findings"]
    risks = model["risks"]
    recommendations = model["recommendations"]

    crit_ids = {c.get("id") for c in criteria}
    evd_ids = {e.get("id") for e in evidence}
    fnd_ids = {f.get("id") for f in findings}
    backing: dict[str, set[str]] = {}
    for e in evidence:
        for claim in e.get("claims", []):
            backing.setdefault(claim, set()).add(e.get("kind"))

    for c in criteria:
        cid = c.get("id", "<no id>")
        if not CRITERION_ID_SHAPE.match(str(cid)):
            failures.append(
                f"{cid}: criterion id must start with a three-letter uppercase prefix"
            )
        else:
            one = CRITERION_REDUNDANT_ONE.match(str(cid))
            if one and not any(
                other != cid and str(other).startswith(one.group(1) + "-")
                for other in crit_ids
            ):
                failures.append(
                    f"{cid}: unnecessary '-{one.group(2)}' suffix when no '{one.group(1)}-02' sibling exists"
                )
        outcome = c.get("outcome")
        if outcome not in CRITERION_OUTCOMES:
            failures.append(f"{cid}: outcome {outcome!r} is not a criterion state")
        if outcome == "PARTIAL":
            m = c.get("mastery")
            if not isinstance(m, (int, float)) or not 0 < m < 1:
                failures.append(
                    f"{cid}: PARTIAL requires a recorded mastery fraction 0 < m < 1"
                )
        if not isinstance(c.get("weight"), (int, float)) or c["weight"] <= 0:
            failures.append(f"{cid}: weight must be a positive number")

    for e in evidence:
        eid = e.get("id", "<no id>")
        if e.get("kind") not in EVIDENCE_KINDS:
            failures.append(f"{eid}: kind {e.get('kind')!r} is not an evidence kind")
        for claim in e.get("claims", []):
            if claim not in crit_ids:
                failures.append(f"{eid}: claims unknown criterion {claim}")

    for f in findings:
        fid = f.get("id", "<no id>")
        if f.get("criterion") not in crit_ids:
            failures.append(f"{fid}: criterion {f.get('criterion')!r} is undeclared")
        for e in f.get("evidence", []):
            if e not in evd_ids:
                failures.append(f"{fid}: cites unknown evidence {e}")
        if f.get("severity") in ("CRITICAL", "HIGH") and not f.get("counter"):
            failures.append(f"{fid}: {f['severity']} finding has no recorded counter-evidence")

    for r in risks:
        rid = r.get("id", "<no id>")
        if r.get("finding") not in fnd_ids:
            failures.append(f"{rid}: cites unknown finding {r.get('finding')!r}")

    for r in recommendations:
        rid = r.get("id", "<no id>")
        if r.get("finding") not in fnd_ids:
            failures.append(f"{rid}: cites unknown finding {r.get('finding')!r}")

    for label in model.get("coverage", {}).get("labels", {}).values():
        if label not in COVERAGE_LABELS:
            failures.append(f"coverage label {label!r} is not a declared label")

    dimensions: dict[str, list[dict]] = {}
    for c in criteria:
        dimensions.setdefault(c.get("dimension", "<none>"), []).append(c)

    scored = 0
    applicable_dims = 0
    dims = model["scores"].get("dimensions", {})
    for dim, cs in dimensions.items():
        applicable, mastery, lo, hi, coverage, eligible = recompute_dimension(cs, backing)
        if not applicable:
            continue
        applicable_dims += 1
        record = dims.get(dim)
        if record is None:
            failures.append(f"dimension '{dim}' has applicable criteria but no score record")
            continue
        if not eligible:
            if record.get("eligible") or record.get("score") is not None:
                failures.append(
                    f"dimension '{dim}': fails the eligibility gate but carries a "
                    "numeric score or eligible flag"
                )
            continue
        expected = max(1, round(mastery * scale_max))
        if record.get("score") != expected:
            failures.append(
                f"dimension '{dim}': score {record.get('score')!r} does not recompute "
                f"to {expected}"
            )
        if lo == hi:
            if record.get("interval") not in (None, [expected, expected]):
                failures.append(
                    f"dimension '{dim}': no unresolved criteria but interval "
                    f"{record.get('interval')!r} is not omitted"
                )
        elif record.get("interval") != [max(1, round(lo * scale_max)),
                                        max(1, round(hi * scale_max))]:
            failures.append(
                f"dimension '{dim}': interval {record.get('interval')!r} does not "
                "equal the FAIL/PASS substitution bounds "
                f"[{max(1, round(lo * scale_max))}, {max(1, round(hi * scale_max))}]"
            )
        if not math.isclose(record.get("coverage", -1), coverage, abs_tol=0.01):
            failures.append(
                f"dimension '{dim}': coverage {record.get('coverage')!r} does not "
                f"recompute to {coverage:.2f}"
            )
        if record.get("eligible") is not True:
            failures.append(f"dimension '{dim}': eligible is not true on a scoring dimension")
        scored += 1

    overall = model["scores"].get("overall", {})
    if overall.get("scored") != scored:
        failures.append(
            f"overall.scored {overall.get('scored')!r} does not match {scored} "
            "eligible dimensions"
        )
    if overall.get("applicable") != applicable_dims:
        failures.append(
            f"overall.applicable {overall.get('applicable')!r} does not match "
            f"{applicable_dims} applicable dimensions"
        )
    score = overall.get("score")
    if scored * 2 <= applicable_dims and score is not None:
        failures.append(
            "overall.score is set while half or fewer applicable dimensions scored"
        )
    if scored > 0 and score is not None:
        points = [
            dims[d]["score"] for d in dims
            if dims[d].get("score") is not None and dims[d].get("eligible")
        ]
        expected_overall = round(sum(points) / len(points), 1) if points else None
        if expected_overall is not None and not math.isclose(
            score, expected_overall, abs_tol=0.05
        ):
            failures.append(
                f"overall.score {score!r} does not recompute to the dimension mean "
                f"{expected_overall}"
            )

    if not all(isinstance(x, str) and x.strip() for x in model.get("exclusions", [])):
        failures.append("an exclusion entry is empty - every exclusion names its reason")
    return failures


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Model-quality checker for work/audit-model.json"
    )
    parser.add_argument("model", help="path to the audit-model.json file")
    parser.add_argument(
        "--json", action="store_true", help="emit failures as JSON instead of text"
    )
    args = parser.parse_args(argv)

    path = Path(args.model)
    if not path.is_file():
        print(f"check-model: no such file: {args.model}", file=sys.stderr)
        return 2
    try:
        model = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"check-model: cannot parse {args.model}: {exc}", file=sys.stderr)
        return 2
    if not isinstance(model, dict):
        print("check-model: top-level value is not an object", file=sys.stderr)
        return 2

    failures = check_model(model)
    if args.json:
        print(json.dumps({"failures": failures}, indent=1))
    elif failures:
        print(f"check-model: {len(failures)} failure(s)")
        for failure in failures:
            print(f"  FAIL {failure}")
    else:
        print("PASS model quality holds")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
