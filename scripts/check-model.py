#!/usr/bin/env python3
"""Model-quality checker for `work/audit-model.json`.

Validates the canonical audit model before report generation: required shape,
referential integrity across evidence/criteria/findings/risks/recommendations,
and recomputation of the scoring engine's outputs (mastery, interval bounds,
coverage, eligibility, caps, overall mean) under scoring policy 2 per
`process/readiness-scoring.md`.

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
from fractions import Fraction
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

CANONICAL_DIMENSIONS = (
    "testability", "design_soundness", "code_quality", "code_style", "stack_alignment",
    "dependency_health", "maintainability", "structure", "deployability", "scalability",
    "security", "compliance", "observability", "operational_safety", "delivery_continuity",
    "ai_provenance", "originality_licensing", "skill_definition", "api_compatibility",
)
SCORING_POLICY = 2
SEVERITIES = ("CRITICAL", "HIGH", "MEDIUM", "LOW")
SEVERITY_BOUND = {"CRITICAL": 0.0, "HIGH": 0.25, "MEDIUM": 0.5, "LOW": 0.75}
BOUNDING_CLASSES = ("confirmed defect", "confirmed structural weakness", "configuration risk")
CLAIM_CLASSES = BOUNDING_CLASSES + ("plausible hypothesis", "evidence gap")
ABSENCE_TOKENS = ("No documented rationale", "Deliberate - recorded decision", "Undetermined")
NA_BASES = ("deployment-model", "census-none", "history-out-of-scope")
HISTORY_STATES = ("present", "absent", "out-of-scope")
SCALES = (10, 5, 3)
CAP_LIMITS = {
    10: {"severity-critical": 3, "severity-high": 5, "material-unknown": 8, "historical-only": 7},
    5:  {"severity-critical": 2, "severity-high": 3, "material-unknown": 4, "historical-only": 4},
    3:  {"severity-critical": 1, "severity-high": 2, "material-unknown": 2, "historical-only": 2},
}
MECHANICAL_CAPS = ("severity-critical", "severity-high", "material-unknown")


def half_up(x: Fraction, places: int = 0) -> Fraction:
    q = Fraction(10) ** places
    return Fraction(math.floor(x * q + Fraction(1, 2))) / q


def scale_score(mastery: Fraction, scale_max: int) -> int:
    return max(1, int(half_up(mastery * scale_max)))


def criterion_mastery(criterion: dict) -> Fraction:
    outcome = criterion.get("outcome")
    if outcome == "PASS":
        return Fraction(1)
    if outcome == "FAIL":
        return Fraction(0)
    partial = criterion.get("mastery")
    if isinstance(partial, (int, float)):
        return Fraction(str(partial))
    return Fraction(0)


def criterion_weight(criterion: dict) -> Fraction:
    return Fraction(str(criterion.get("weight", 1.0)))


def recompute_dimension(criteria: list[dict], backing: dict[str, set[str]]):
    """Recompute one dimension's scoring tuple from its criteria."""
    applicable = [c for c in criteria if c.get("outcome") != "NOT_APPLICABLE"]
    resolved = [c for c in applicable if c.get("outcome") in RESOLVED]
    app_weight = sum((criterion_weight(c) for c in applicable), Fraction(0))
    res_weight = sum((criterion_weight(c) for c in resolved), Fraction(0))

    def mastery_with(fill: Fraction | None) -> Fraction | None:
        if not res_weight:
            return None
        total = Fraction(0)
        for c in applicable:
            if c["outcome"] in RESOLVED:
                total += criterion_weight(c) * criterion_mastery(c)
            elif fill is not None:
                total += criterion_weight(c) * fill
        denom = app_weight if fill is not None else res_weight
        return total / denom if denom else None

    mastery = mastery_with(None)
    lo = mastery_with(Fraction(0))
    hi = mastery_with(Fraction(1))
    coverage = res_weight / app_weight if app_weight else Fraction(0)
    eligible = (
        coverage > Fraction(1, 2)
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

    scope = model.get("scope", {})
    if scope.get("scoring_policy") != SCORING_POLICY:
        failures.append(
            f"scope.scoring_policy is {scope.get('scoring_policy')!r}, "
            f"expected {SCORING_POLICY}"
        )
    if scope.get("history") not in HISTORY_STATES:
        failures.append(
            f"scope.history is {scope.get('history')!r}, expected present, "
            "absent, or out-of-scope"
        )

    scale_max = model.get("scores", {}).get("scale_max", 10)
    if scale_max not in SCALES:
        failures.append(f"scores.scale_max is {scale_max!r}, expected 10, 5, or 3")
        scale_max = 10

    projects = scope.get("projects", [])
    named = {
        p["name"] for p in projects
        if isinstance(p, dict) and p.get("name")
    }

    def canonical_dim(dim) -> bool:
        if dim in CANONICAL_DIMENSIONS:
            return True
        if isinstance(dim, str) and "." in dim:
            project, _, leaf = dim.partition(".")
            return project in named and leaf in CANONICAL_DIMENSIONS
        return False

    criteria = model["criteria"]
    evidence = model["evidence"]
    findings = model["findings"]
    risks = model["risks"]
    recommendations = model["recommendations"]

    crit_ids = {c.get("id") for c in criteria}
    evd_ids = {e.get("id") for e in evidence}
    fnd_ids = {f.get("id") for f in findings}
    crit_by_id = {c.get("id"): c for c in criteria}
    backing: dict[str, set[str]] = {}
    for e in evidence:
        for claim in e.get("claims", []):
            backing.setdefault(claim, set()).add(e.get("kind"))

    open_findings_by_criterion: dict[str, list[dict]] = {}
    for f in findings:
        if f.get("status") == "Open":
            open_findings_by_criterion.setdefault(f.get("criterion"), []).append(f)

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
        dimension = c.get("dimension")
        if not canonical_dim(dimension):
            failures.append(
                f"{cid}: dimension {dimension!r} is not a canonical dimension id"
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
        if outcome == "NOT_APPLICABLE":
            na_basis = c.get("na_basis")
            if na_basis not in NA_BASES:
                failures.append(
                    f"{cid}: NOT_APPLICABLE needs na_basis deployment-model, "
                    "census-none, or history-out-of-scope"
                )
            elif na_basis == "census-none":
                owner = None
                if isinstance(dimension, str) and "." in dimension:
                    prefix = dimension.partition(".")[0]
                    owner = next(
                        (p for p in projects if p.get("name") == prefix), None
                    )
                elif projects:
                    owner = projects[0]
                census = (owner or {}).get("automation_census")
                if census != "none":
                    failures.append(
                        f"{cid}: census-none basis requires automation census "
                        f"none, found {census!r}"
                    )
            elif na_basis == "history-out-of-scope":
                if scope.get("history") not in ("absent", "out-of-scope"):
                    failures.append(
                        f"{cid}: history-out-of-scope basis requires scope.history "
                        f"absent or out-of-scope, found {scope.get('history')!r}"
                    )
            elif na_basis == "deployment-model":
                if not isinstance(c.get("applicability"), str) or not c["applicability"].strip():
                    failures.append(
                        f"{cid}: deployment-model basis needs an applicability "
                        "justification"
                    )
        if outcome in ("PARTIAL", "FAIL"):
            cited = bool(open_findings_by_criterion.get(c.get("id")))
            shortfall = c.get("shortfall")
            evidenced = (
                isinstance(shortfall, str) and bool(shortfall.strip())
                and any(c.get("id") in e.get("claims", []) for e in evidence)
            )
            if not cited and not evidenced:
                failures.append(
                    f"{cid}: {outcome} deduction has no open finding and no "
                    "recorded shortfall with evidence"
                )

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
        if f.get("claim_class") not in CLAIM_CLASSES:
            failures.append(
                f"{fid}: claim_class {f.get('claim_class')!r} is not a declared "
                "claim class"
            )
        if f.get("severity") not in SEVERITIES:
            failures.append(
                f"{fid}: severity {f.get('severity')!r} is not a finding severity"
            )
        if f.get("absence") is not None and f.get("absence") not in ABSENCE_TOKENS:
            failures.append(
                f"{fid}: absence {f.get('absence')!r} is not an absence token"
            )
        if f.get("status") == "Open" and f.get("claim_class") in BOUNDING_CLASSES:
            c = crit_by_id.get(f.get("criterion"))
            if c is not None:
                cid = c.get("id")
                outcome = c.get("outcome")
                if outcome in RESOLVED:
                    mastery = criterion_mastery(c)
                    bound = Fraction(str(SEVERITY_BOUND.get(f.get("severity"), 1)))
                    if f.get("severity") in SEVERITY_BOUND and mastery > bound:
                        failures.append(
                            f"{cid}: mastery {float(mastery):g} exceeds the "
                            f"{float(bound):g} bound of open {f['severity']} "
                            f"finding {fid}"
                        )
                elif outcome in ("UNKNOWN", "NOT_ASSESSED"):
                    failures.append(
                        f"{fid}: open {f.get('claim_class')} cites unresolved "
                        f"criterion {cid} - a confirmed finding resolves its "
                        "criterion"
                    )
                elif outcome == "NOT_APPLICABLE":
                    if not (
                        f.get("absence")
                        and c.get("na_basis") in ("census-none", "history-out-of-scope")
                    ):
                        failures.append(
                            f"{fid}: open {f.get('claim_class')} cites inapplicable "
                            f"criterion {cid} without the absence exemption"
                        )

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

    dims = model["scores"].get("dimensions", {})
    for key in dims:
        if not canonical_dim(key):
            failures.append(
                f"scores.dimensions key {key!r} is not a canonical dimension id"
            )

    cap_limits = CAP_LIMITS[scale_max]
    crit_dim = {c.get("id"): c.get("dimension", "<none>") for c in criteria}
    bounding = [
        f for f in findings
        if f.get("status") == "Open" and f.get("claim_class") in BOUNDING_CLASSES
    ]

    scored = 0
    applicable_dims = 0
    scored_dims: set[str] = set()
    applicable_dim_names: set[str] = set()
    for dim, cs in dimensions.items():
        applicable, mastery, lo, hi, coverage, eligible = recompute_dimension(cs, backing)
        if not applicable:
            continue
        applicable_dims += 1
        applicable_dim_names.add(dim)
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
        if record.get("mastery") is not None and not math.isclose(
            record["mastery"], float(mastery), abs_tol=0.01
        ):
            failures.append(
                f"dimension '{dim}': mastery {record.get('mastery')!r} does not "
                f"recompute to {float(mastery):.2f}"
            )
        uncapped = scale_score(mastery, scale_max)
        if record.get("uncapped") != uncapped:
            failures.append(
                f"dimension '{dim}': uncapped {record.get('uncapped')!r} does not "
                f"recompute to {uncapped}"
            )
        triggers = {
            "severity-critical": sorted(
                f.get("id") for f in bounding
                if f.get("severity") == "CRITICAL"
                and crit_dim.get(f.get("criterion")) == dim
            ),
            "severity-high": sorted(
                f.get("id") for f in bounding
                if f.get("severity") == "HIGH"
                and crit_dim.get(f.get("criterion")) == dim
            ),
            "material-unknown": sorted(
                c.get("id") for c in cs
                if c.get("criticality") in ("critical", "high")
                and c.get("outcome") in ("UNKNOWN", "NOT_ASSESSED")
            ),
        }
        caps = record.get("caps")
        if not isinstance(caps, list):
            caps = []
        seen: set[str] = set()
        valid_limits: list[int] = []
        for cap in caps:
            rule = cap.get("rule") if isinstance(cap, dict) else None
            if rule not in cap_limits:
                failures.append(
                    f"dimension '{dim}': cap rule {rule!r} is not a declared cap rule"
                )
                continue
            if rule in seen:
                failures.append(
                    f"dimension '{dim}': cap rule {rule} is listed twice"
                )
                continue
            seen.add(rule)
            cap_valid = cap.get("limit") == cap_limits[rule]
            if not cap_valid:
                failures.append(
                    f"dimension '{dim}': cap {rule} limit {cap.get('limit')!r} is "
                    f"not {cap_limits[rule]}"
                )
            source = cap.get("source")
            source = source if isinstance(source, list) else []
            if rule in MECHANICAL_CAPS:
                triggered = triggers[rule]
                if not triggered:
                    failures.append(
                        f"dimension '{dim}': cap {rule} is listed but not triggered"
                    )
                    cap_valid = False
                elif not set(triggered) <= set(source):
                    failures.append(
                        f"dimension '{dim}': missing mechanical cap {rule} "
                        f"triggered by {','.join(triggered)}"
                    )
            else:
                if not source:
                    failures.append(
                        f"dimension '{dim}': historical-only cap cites no evidence"
                    )
                    cap_valid = False
                else:
                    for eid in source:
                        if eid not in evd_ids:
                            failures.append(
                                f"dimension '{dim}': historical-only cap cites "
                                f"unknown evidence {eid}"
                            )
                            cap_valid = False
            if cap_valid:
                valid_limits.append(cap["limit"])
        for rule in MECHANICAL_CAPS:
            if triggers[rule] and rule not in seen:
                failures.append(
                    f"dimension '{dim}': missing mechanical cap {rule} triggered "
                    f"by {','.join(triggers[rule])}"
                )
        capmin = min(valid_limits) if valid_limits else None
        expected = min(uncapped, capmin) if capmin is not None else uncapped
        if record.get("score") != expected:
            failures.append(
                f"dimension '{dim}': score {record.get('score')!r} does not recompute "
                f"to {expected}"
            )
        lo_s = scale_score(lo, scale_max)
        hi_s = scale_score(hi, scale_max)
        if capmin is not None:
            lo_s = min(lo_s, capmin)
            hi_s = min(hi_s, capmin)
        if lo_s == hi_s:
            if record.get("interval") is not None:
                failures.append(
                    f"dimension '{dim}': interval {record.get('interval')!r} is not "
                    "omitted although its capped bounds are equal"
                )
        elif record.get("interval") != [lo_s, hi_s]:
            failures.append(
                f"dimension '{dim}': interval {record.get('interval')!r} does not "
                "equal the capped FAIL/PASS substitution bounds "
                f"[{lo_s}, {hi_s}]"
            )
        if not math.isclose(record.get("coverage", -1), float(coverage), abs_tol=0.01):
            failures.append(
                f"dimension '{dim}': coverage {record.get('coverage')!r} does not "
                f"recompute to {float(coverage):.2f}"
            )
        if record.get("eligible") is not True:
            failures.append(f"dimension '{dim}': eligible is not true on a scoring dimension")
        scored += 1
        scored_dims.add(dim)

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

    def recorded_points(dim_names) -> list[Fraction]:
        return [
            Fraction(str(dims[d]["score"])) for d in dims
            if d in dim_names
            and dims[d].get("score") is not None
            and dims[d].get("eligible")
        ]

    score = overall.get("score")
    if len(named) >= 2:
        if score is not None:
            failures.append(
                "overall.score must be null in a multi-project model - score "
                "per project"
            )
        per_project = model["scores"].get("per_project", {})
        for name in sorted(named):
            record = per_project.get(name)
            if record is None:
                failures.append(f"per_project record missing for project {name!r}")
                continue
            p_dims = {
                d for d in dimensions
                if "." in str(d) and str(d).partition(".")[0] == name
            }
            p_scored = len(p_dims & scored_dims)
            p_applicable = len(p_dims & applicable_dim_names)
            if record.get("scored") != p_scored:
                failures.append(
                    f"per_project[{name!r}].scored {record.get('scored')!r} does "
                    f"not match {p_scored}"
                )
            if record.get("applicable") != p_applicable:
                failures.append(
                    f"per_project[{name!r}].applicable {record.get('applicable')!r} "
                    f"does not match {p_applicable}"
                )
            p_score = record.get("score")
            if p_scored * 2 <= p_applicable and p_score is not None:
                failures.append(
                    f"per_project[{name!r}].score is set while half or fewer "
                    "applicable dimensions scored"
                )
            if p_scored > 0 and p_score is not None:
                points = recorded_points(p_dims | {
                    d for d in dims
                    if "." in str(d) and str(d).partition(".")[0] == name
                })
                if points:
                    expected_score = float(
                        half_up(sum(points, Fraction(0)) / len(points), 1)
                    )
                    if abs(p_score - expected_score) >= 0.001:
                        failures.append(
                            f"per_project[{name!r}].score {p_score!r} does not "
                            f"recompute to {expected_score}"
                        )
    else:
        if scored * 2 <= applicable_dims and score is not None:
            failures.append(
                "overall.score is set while half or fewer applicable dimensions scored"
            )
        if scored > 0 and score is not None:
            points = recorded_points(set(dims))
            if points:
                expected_overall = float(
                    half_up(sum(points, Fraction(0)) / len(points), 1)
                )
                if abs(score - expected_overall) >= 0.001:
                    failures.append(
                        f"overall.score {score!r} does not recompute to the "
                        f"dimension mean {expected_overall}"
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
