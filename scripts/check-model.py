#!/usr/bin/env python3
"""Model-quality checker for `work/audit-model.json`.

Validates the canonical audit model before report generation: required shape,
referential integrity across evidence/criteria/findings/risks/requirements/
recommendations, catalogue membership and level/outcome consistency, and
recomputation of the scoring engine's outputs (mastery, interval bounds,
coverage, eligibility, caps, headline records) under scoring policy 3 per
`process/readiness-scoring.md` and `references/criteria-catalogue.json`.

Usage:
    python scripts/check-model.py path/to/work/audit-model.json [--json]

Exit code 0 means all checks passed, 1 means model-quality failures, 2 means
usage or parse errors.
"""

from __future__ import annotations

import argparse
import hashlib
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
CRITERIA_OUTCOMES = {
    "PASS", "FAIL", "PARTIAL", "UNKNOWN", "NOT_ASSESSED", "NOT_APPLICABLE",
}
CRITERIA_ID_SHAPE = re.compile(r"^[A-Z]{3}-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
CRITERIA_REDUNDANT_ONE = re.compile(r"^([A-Z]{3}-[A-Z]+(?:-[A-Z]+)*)-(0?1)$")
RESOLVED = {"PASS", "FAIL", "PARTIAL"}
COVERAGE_LABELS = {
    "COMPLETE_FOR_DECLARED_SCOPE", "PARTIAL", "NOT_ASSESSED", "NOT_APPLICABLE",
}
TOP_LEVEL = [
    "model_version", "scope", "inventory", "criteria", "requirements", "evidence",
    "findings", "risks", "recommendations", "readiness", "scores", "coverage",
    "exclusions",
]

CANONICAL_DIMENSIONS = (
    "functional_suitability", "testability", "design_soundness", "code_quality",
    "code_style", "stack_alignment", "dependency_health", "maintainability",
    "structure", "deployability", "scalability", "security", "compliance",
    "observability", "operational_safety", "documentation", "api_compatibility",
    "delivery_continuity", "originality_licensing", "skill_definition",
)
DIMENSION_GROUP = {
    name: "process" for name in (
        "delivery_continuity", "originality_licensing", "skill_definition",
    )
}
DIMENSION_GROUP.update(
    {name: "product" for name in CANONICAL_DIMENSIONS if name not in DIMENSION_GROUP}
)
DIMENSION_TIER = {
    "functional_suitability": 3, "testability": 3, "design_soundness": 2,
    "code_quality": 2, "code_style": 1, "stack_alignment": 1,
    "dependency_health": 2, "maintainability": 2, "structure": 1,
    "deployability": 2, "scalability": 2, "security": 3, "compliance": 2,
    "observability": 2, "operational_safety": 3, "documentation": 2,
    "api_compatibility": 2,
    "delivery_continuity": 1,
    "originality_licensing": 1, "skill_definition": 1,
}
SCORING_POLICY = 3
SEVERITIES = ("CRITICAL", "HIGH", "MEDIUM", "LOW")
SEVERITY_BOUND = {"CRITICAL": 0.0, "HIGH": 0.25, "MEDIUM": 0.5, "LOW": 0.75}
BOUNDING_CLASSES = ("confirmed defect", "confirmed structural weakness", "configuration risk")
CLAIM_CLASSES = BOUNDING_CLASSES + ("plausible hypothesis", "evidence gap")
ABSENCE_TOKENS = ("No documented rationale", "Deliberate - recorded decision", "Undetermined")
NA_BASES = ("deployment-model", "census-none", "history-out-of-scope")
HISTORY_STATES = ("present", "absent", "out-of-scope")
DETAIL_LEVELS = ("Detailed", "Standard", "Brief")
PRODUCT_NATURES = (
    "service", "library", "cli", "pipeline", "retrieval",
    "agent-tooling", "frontend", "automation", "unclassified",
)
CRITERIA_CHANNELS = ("score", "conformance")
CONFORMANCE_PREFIXES = ("CNF-", "REQ-")
LEVEL_OUTCOME = {
    "PASS": "PASS", "P75": "PARTIAL", "P50": "PARTIAL",
    "P25": "PARTIAL", "FAIL": "FAIL",
}
LEVEL_VALUES = {
    "PASS": Fraction(1), "P75": Fraction(3, 4), "P50": Fraction(1, 2),
    "P25": Fraction(1, 4), "FAIL": Fraction(0),
}
OBLIGATIONS = ("mandatory", "recommended", "optional", "future")
REQUIREMENT_STATES = ("PASS", "PARTIAL", "FAIL", "UNKNOWN")
READINESS_STATES = ("READY", "NOT READY", "PENDING EVIDENCE", "NOT ASSESSED")
SINGLE_CEILINGS = {
    10: {"critical": 3, "high": 6},
    5: {"critical": 2, "high": 3},
    3: {"critical": 1, "high": 2},
}
SINGLE_BANDS = {
    10: ((9, "Excellent"), (7, "Good"), (4, "Average"), (1, "Poor")),
    5: ((5, "Excellent"), (4, "Good"), (3, "Average"), (2, "Poor"), (1, "Bad")),
    3: ((3, "Excellent"), (2, "Average"), (1, "Poor")),
}
FNC_REQ_APPLICABILITY = "no mandatory requirements declared or advertised"
CATALOGUE_FILE = "references/criteria-catalogue.json"
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


def criteria_mastery(entry: dict) -> Fraction:
    outcome = entry.get("outcome")
    if outcome == "PASS":
        return Fraction(1)
    if outcome == "FAIL":
        return Fraction(0)
    partial = entry.get("mastery")
    if isinstance(partial, (int, float)):
        return Fraction(str(partial))
    return Fraction(0)


def criteria_weight(entry: dict) -> Fraction:
    return Fraction(str(entry.get("weight", 1.0)))


def recompute_dimension(criteria: list[dict], backing: dict[str, set[str]]):
    """Recompute one dimension's scoring tuple from its criteria."""
    applicable = [c for c in criteria if c.get("outcome") != "NOT_APPLICABLE"]
    resolved = [c for c in applicable if c.get("outcome") in RESOLVED]
    app_weight = sum((criteria_weight(c) for c in applicable), Fraction(0))
    res_weight = sum((criteria_weight(c) for c in resolved), Fraction(0))

    def mastery_with(fill: Fraction | None) -> Fraction | None:
        if not res_weight:
            return None
        total = Fraction(0)
        for c in applicable:
            if c["outcome"] in RESOLVED:
                total += criteria_weight(c) * criteria_mastery(c)
            elif fill is not None:
                total += criteria_weight(c) * fill
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


def load_catalogue() -> dict | None:
    """Load `references/criteria-catalogue.json` from the skill root.

    Returns the parsed catalogue dict, or None when the file is absent or
    cannot be parsed.
    """
    path = Path(__file__).resolve().parent.parent / CATALOGUE_FILE
    if not path.is_file():
        return None
    try:
        catalogue = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return catalogue if isinstance(catalogue, dict) else None


def _group_mean(
    group_dims: list[str], dims: dict, key: str, weighted: bool
) -> Fraction | None:
    """Tier-weighted (product) or equal (process) mean of `key` over dims."""
    total = Fraction(0)
    denom = Fraction(0)
    for name in group_dims:
        weight = Fraction(DIMENSION_TIER[name]) if weighted else Fraction(1)
        total += weight * Fraction(str(dims[name][key]))
        denom += weight
    if not denom:
        return None
    return total / denom


def compute_headline(dims, scale_max, critical_open, high_open, readiness_state):
    """Recompute the product/process/single headline records.

    `dims` maps canonical dimension ids to
    `{"applicable": bool, "eligible": bool, "score": int | None,
      "lo": int, "hi": int}` - `lo`/`hi` are the capped interval bounds, both
    equal to `score` when the interval is omitted, and the substitution bounds
    for an ineligible applicable dimension (`lo` 1 and `hi` scale_max when no
    criteria entry resolved). All arithmetic is exact.
    """
    def applicable(group: str) -> list[str]:
        return [
            name for name in CANONICAL_DIMENSIONS
            if DIMENSION_GROUP[name] == group
            and isinstance(dims.get(name), dict)
            and dims[name].get("applicable", True)
        ]

    def block(group: str):
        app = applicable(group)
        eligible = [d for d in app if dims[d].get("eligible")]
        if group == "product":
            t3_ok = all(
                dims[d].get("eligible")
                for d in app if DIMENSION_TIER[d] == 3
            )
            weight_of = lambda d: Fraction(DIMENSION_TIER[d])
            eligible_weight = int(sum(weight_of(d) for d in eligible))
            applicable_weight = int(sum(weight_of(d) for d in app))
            published = t3_ok and eligible_weight * 2 > applicable_weight
            extra = {
                "eligible_weight": eligible_weight,
                "applicable_weight": applicable_weight,
            }
        else:
            published = len(eligible) * 2 > len(app) and len(app) >= 1
            extra = {"scored": len(eligible), "applicable": len(app)}
        score = interval = None
        lowest = []
        weighted = group == "product"
        if published:
            score = float(
                half_up(_group_mean(eligible, dims, "score", weighted), 1)
            )
            lo = half_up(_group_mean(app, dims, "lo", weighted), 1)
            hi = half_up(_group_mean(app, dims, "hi", weighted), 1)
            interval = [float(lo), float(hi)] if lo != hi else None
            floor = min(Fraction(str(dims[d]["score"])) for d in eligible)
            lowest = [
                d for d in eligible
                if Fraction(str(dims[d]["score"])) == floor
            ]
        return {
            "score": score, "interval": interval, "published": published,
            "lowest": lowest, **extra,
        }

    product = block("product")
    process = block("process")

    if not product["published"]:
        single = {
            "score": None, "raw": None, "interval": None,
            "flag": None, "ceiling": None, "band": None,
        }
    else:
        p_lo, p_hi = product["interval"] or (product["score"], product["score"])
        if process["published"]:
            q_lo, q_hi = (
                process["interval"] or (process["score"], process["score"])
            )
            blend = lambda a, b: Fraction(7, 10) * Fraction(str(a)) + Fraction(
                3, 10
            ) * Fraction(str(b))
            raw = half_up(blend(product["score"], process["score"]), 1)
            lo = half_up(blend(p_lo, q_lo), 1)
            hi = half_up(blend(p_hi, q_hi), 1)
            flag = None
        else:
            raw = Fraction(str(product["score"]))
            lo, hi = Fraction(str(p_lo)), Fraction(str(p_hi))
            flag = "product-only"
        reasons = []
        limits = []
        ceilings = SINGLE_CEILINGS[scale_max]
        if critical_open:
            reasons.append("severity:CRITICAL")
            limits.append(ceilings["critical"])
        if high_open:
            reasons.append("severity:HIGH")
            limits.append(ceilings["high"])
        if readiness_state == "NOT READY":
            reasons.append("readiness:NOT READY")
            limits.append(ceilings["high"])
        ceiling = (
            {"limit": min(limits), "reasons": reasons} if reasons else None
        )
        limit = ceiling["limit"] if ceiling else None
        score = float(min(raw, limit)) if limit is not None else float(raw)
        lo_s = float(min(lo, limit)) if limit is not None else float(lo)
        hi_s = float(min(hi, limit)) if limit is not None else float(hi)
        interval = [lo_s, hi_s] if lo_s != hi_s else None
        band = next(
            (
                name for floor, name in SINGLE_BANDS[scale_max]
                if half_up(Fraction(str(score))) >= floor
            ),
            SINGLE_BANDS[scale_max][-1][1],
        )
        single = {
            "score": score, "raw": float(raw), "interval": interval,
            "flag": flag, "ceiling": ceiling, "band": band,
        }

    return {"product": product, "process": process, "single": single}


def fix_model(model: dict, catalogue: dict | None = None) -> list[str]:
    """Fill every mechanically computable record in a model in place.

    The fixer mirrors `check_model`'s recomputation so a model written by
    `--fix` passes cleanly: criteria `mastery` from the declared level,
    mechanical criteria levels from the requirements coverage, the frozen
    `requirements_baseline` digest, `scores.dimensions` records including
    triggered caps and substitution intervals, and the
    `product`/`process`/`single` or `per_project` headline records.

    Returns a list of human-readable change descriptions.
    """
    changes: list[str] = []
    scope = model.get("scope", {})
    criteria = model.get("criteria", [])
    evidence = model.get("evidence", [])
    findings = model.get("findings", [])
    requirements = model.get("requirements", [])
    scores = model.setdefault("scores", {})
    scale_max = scores.get("scale_max", 10)
    if scale_max not in SCALES:
        scale_max = 10
        scores["scale_max"] = 10
        changes.append("scores.scale_max set to 10")

    projects = scope.get("projects", [])
    named = {
        p["name"] for p in projects if isinstance(p, dict) and p.get("name")
    }
    multi = len(named) >= 2

    # Criteria mastery from the declared level.
    for c in criteria:
        level = c.get("level")
        outcome = c.get("outcome")
        if level in LEVEL_VALUES and outcome in RESOLVED:
            want = float(LEVEL_VALUES[level])
            if c.get("mastery") != want:
                changes.append(
                    f"{c.get('id')}: mastery {c.get('mastery')!r} -> {want:g}"
                )
                c["mastery"] = want
        elif outcome == "PASS" and c.get("mastery") != 1.0:
            changes.append(f"{c.get('id')}: mastery set to 1.0")
            c["mastery"] = 1.0
        elif outcome == "FAIL" and c.get("mastery") != 0.0:
            changes.append(f"{c.get('id')}: mastery set to 0.0")
            c["mastery"] = 0.0
        elif outcome in ("PARTIAL",) and not isinstance(c.get("mastery"), (int, float)):
            c["mastery"] = 0.5
            changes.append(f"{c.get('id')}: mastery defaulted to 0.5")

    # Requirements baseline digest.
    if requirements:
        digest = hashlib.sha256(
            "\n".join(
                sorted(
                    f"{r.get('id')}:{r.get('obligation')}"
                    for r in requirements
                )
            ).encode("utf-8")
        ).hexdigest()
        if scope.get("requirements_baseline") != digest:
            scope["requirements_baseline"] = digest
            changes.append("scope.requirements_baseline recomputed")

    # Mechanical criteria (e.g. FNC-REQ) from requirements coverage.
    cat_entries = {
        e.get("id"): e
        for e in (catalogue or {}).get("criteria", [])
        if isinstance(e, dict)
    }
    if cat_entries and requirements:
        req_values = {"PASS": Fraction(1), "PARTIAL": Fraction(1, 2),
                      "FAIL": Fraction(0)}
        mandatory = [
            r for r in requirements if r.get("obligation") == "mandatory"
        ]
        graded = [r for r in mandatory if r.get("status") != "UNKNOWN"]
        n_req, g_req = len(mandatory), len(graded)
        coverage_req = (
            sum((req_values.get(r.get("status"), Fraction(0)) for r in graded),
                Fraction(0)) / g_req
            if g_req else Fraction(0)
        )
        if n_req == 0:
            computed = "NOT_APPLICABLE"
        elif g_req * 2 <= n_req:
            computed = "UNKNOWN"
        else:
            computed = "FAIL"
            for bound, level in (
                (Fraction(19, 20), "PASS"), (Fraction(17, 20), "P75"),
                (Fraction(7, 10), "P50"), (Fraction(1, 2), "P25"),
            ):
                if coverage_req >= bound:
                    computed = level
                    break
        for c in criteria:
            if c.get("channel") != "score":
                continue
            entry = cat_entries.get(c.get("catalogue_id"))
            if not isinstance(entry, dict) or not entry.get("mechanical"):
                continue
            if computed in LEVEL_VALUES:
                if c.get("level") != computed:
                    changes.append(
                        f"{c.get('id')}: level {c.get('level')!r} -> "
                        f"{computed} (coverage {float(coverage_req):.3f})"
                    )
                    c["level"] = computed
                if c.get("outcome") != LEVEL_OUTCOME[computed]:
                    c["outcome"] = LEVEL_OUTCOME[computed]
                    changes.append(f"{c.get('id')}: outcome -> {c['outcome']}")
                want = float(LEVEL_VALUES[computed])
                if c.get("mastery") != want:
                    c["mastery"] = want
            elif computed == "NOT_APPLICABLE":
                c["outcome"] = "NOT_APPLICABLE"
                c["level"] = None
                c["mastery"] = None
                c["na_basis"] = "deployment-model"
                c["applicability"] = FNC_REQ_APPLICABILITY
                changes.append(f"{c.get('id')}: marked NOT_APPLICABLE")
            else:
                c["outcome"] = computed
                c["level"] = None
                c["mastery"] = None
                changes.append(f"{c.get('id')}: outcome -> {computed}")

    # Evidence backing and bounding findings.
    backing: dict[str, set[str]] = {}
    for e in evidence:
        for claim in e.get("claims", []):
            backing.setdefault(claim, set()).add(e.get("kind"))
    bounding = [
        f for f in findings
        if f.get("status") == "Open"
        and f.get("claim_class") in BOUNDING_CLASSES
    ]
    crit_dim = {c.get("id"): c.get("dimension", "<none>") for c in criteria}

    dimensions: dict[str, list[dict]] = {}
    for c in criteria:
        if c.get("channel") == "score":
            dimensions.setdefault(c.get("dimension", "<none>"), []).append(c)

    cap_limits = CAP_LIMITS[scale_max]
    dims = scores.get("dimensions")
    if not isinstance(dims, dict):
        dims = {}
        scores["dimensions"] = dims
        changes.append("scores.dimensions created")
    recomputed: dict[str, dict] = {}
    for dim, cs in dimensions.items():
        applicable, mastery, lo, hi, coverage, eligible = recompute_dimension(
            cs, backing
        )
        if not applicable:
            if dim in dims:
                del dims[dim]
                changes.append(f"dimension '{dim}': record removed (inapplicable)")
            continue
        if not eligible:
            sub_lo = scale_score(lo, scale_max) if lo is not None else 1
            sub_hi = scale_score(hi, scale_max) if hi is not None else scale_max
            record = {
                "mastery": None, "uncapped": None, "score": None,
                "interval": [sub_lo, sub_hi] if sub_lo != sub_hi else None,
                "coverage": round(float(coverage), 4), "eligible": False,
                "caps": [],
            }
            if dims.get(dim) != record:
                dims[dim] = record
                changes.append(f"dimension '{dim}': marked ineligible")
            recomputed[dim] = {
                "eligible": False, "score": None, "lo": sub_lo, "hi": sub_hi,
            }
            continue
        triggers = {
            "severity-critical": sorted(
                f.get("id") for f in bounding
                if f.get("severity") == "CRITICAL"
                and crit_dim.get(f.get("criteria")) == dim
            ),
            "severity-high": sorted(
                f.get("id") for f in bounding
                if f.get("severity") == "HIGH"
                and crit_dim.get(f.get("criteria")) == dim
            ),
            "material-unknown": sorted(
                c.get("id") for c in cs
                if c.get("criticality") in ("critical", "high")
                and c.get("outcome") in ("UNKNOWN", "NOT_ASSESSED")
            ),
        }
        caps = [
            {"rule": rule, "limit": cap_limits[rule], "source": triggered}
            for rule in MECHANICAL_CAPS if triggers[rule]
        ]
        capmin = min(cap["limit"] for cap in caps) if caps else None
        uncapped = scale_score(mastery, scale_max)
        expected_score = (
            min(uncapped, capmin) if capmin is not None else uncapped
        )
        lo_s = scale_score(lo, scale_max)
        hi_s = scale_score(hi, scale_max)
        if capmin is not None:
            lo_s, hi_s = min(lo_s, capmin), min(hi_s, capmin)
        record = {
            "mastery": round(float(mastery), 4),
            "uncapped": uncapped,
            "score": expected_score,
            "interval": [lo_s, hi_s] if lo_s != hi_s else None,
            "coverage": round(float(coverage), 4),
            "eligible": True,
            "caps": caps,
        }
        if dims.get(dim) != record:
            dims[dim] = record
            changes.append(f"dimension '{dim}': score record recomputed")
        recomputed[dim] = {
            "eligible": True, "score": expected_score, "lo": lo_s, "hi": hi_s,
        }

    # Headline records per scoring scope.
    def project_dims(prefix):
        leaf = {}
        for d in CANONICAL_DIMENSIONS:
            key = f"{prefix}.{d}" if prefix is not None else d
            entry = recomputed.get(key)
            if entry is not None:
                leaf[d] = {"applicable": True, **entry}
        return leaf

    def project_open(prefix):
        critical = high = False
        for f in bounding:
            if prefix is not None:
                dim = crit_dim.get(f.get("criteria"))
                if not isinstance(dim, str) or not dim.startswith(prefix + "."):
                    continue
            if f.get("severity") == "CRITICAL":
                critical = True
            if f.get("severity") == "HIGH":
                high = True
        return critical, high

    readiness = model.get("readiness", {})
    readiness = readiness if isinstance(readiness, dict) else {}
    if multi:
        for key in ("product", "process", "single"):
            if key in scores:
                del scores[key]
                changes.append(f"scores.{key} removed (multi-project model)")
        per_project = scores.get("per_project")
        if not isinstance(per_project, dict):
            per_project = {}
            scores["per_project"] = per_project
        readiness_pp = readiness.get("per_project", {})
        readiness_pp = readiness_pp if isinstance(readiness_pp, dict) else {}
        for name in sorted(named):
            critical, high = project_open(name)
            state = readiness_pp.get(name, {}).get("state")
            expected = compute_headline(
                project_dims(name), scale_max, critical, high, state
            )
            if per_project.get(name) != expected:
                per_project[name] = expected
                changes.append(f"per_project[{name}]: headline recomputed")
    else:
        if "per_project" in scores:
            del scores["per_project"]
            changes.append("scores.per_project removed (single-project model)")
        critical, high = project_open(None)
        state = readiness.get("state")
        expected = compute_headline(
            project_dims(None), scale_max, critical, high, state
        )
        for key, record in expected.items():
            if scores.get(key) != record:
                scores[key] = record
                changes.append(f"scores.{key} recomputed")
    return changes


def check_model(model: dict, catalogue: dict | None = None) -> list[str]:
    failures: list[str] = []
    for key in TOP_LEVEL:
        if key not in model:
            failures.append(f"missing top-level key '{key}'")
    if model.get("model_version") != 2:
        failures.append(f"model_version is {model.get('model_version')!r}, expected 2")
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
    if scope.get("detail_level") not in DETAIL_LEVELS:
        failures.append(
            f"scope.detail_level {scope.get('detail_level')!r} is not "
            "Detailed, Standard, or Brief"
        )
    natures = scope.get("product_profile", {}).get("natures")
    if not isinstance(natures, list) or not natures:
        failures.append("scope.product_profile.natures is required")
        natures = []
    else:
        for nature in natures:
            if nature not in PRODUCT_NATURES:
                failures.append(
                    f"scope.product_profile.natures entry {nature!r} is not "
                    "a declared project nature"
                )

    if catalogue is None:
        catalogue = load_catalogue()
    catalogue_ok = isinstance(catalogue, dict)
    cat_entries: dict[str, dict] = {}
    level_values = dict(LEVEL_VALUES)
    if not catalogue_ok:
        failures.append(f"catalogue file {CATALOGUE_FILE} is missing")
    else:
        for entry in catalogue.get("criteria", []):
            cat_entries[entry.get("id")] = entry
        for name, value in catalogue.get("levels", {}).items():
            level_values[name] = Fraction(str(value))
        if scope.get("catalogue_version") != catalogue.get("catalogue_version"):
            failures.append(
                f"scope.catalogue_version "
                f"{scope.get('catalogue_version')!r} does not match "
                f"catalogue version {catalogue.get('catalogue_version')!r}"
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

    open_findings_by_criteria: dict[str, list[dict]] = {}
    for f in findings:
        if f.get("status") == "Open":
            open_findings_by_criteria.setdefault(f.get("criteria"), []).append(f)

    def owner_project(dimension) -> dict | None:
        if isinstance(dimension, str) and "." in dimension:
            prefix = dimension.partition(".")[0]
            return next(
                (p for p in projects if p.get("name") == prefix), None
            )
        return projects[0] if projects else None

    multi = len(named) >= 2
    seen_crit_ids: set[str] = set()
    for c in criteria:
        cid = c.get("id", "<no id>")
        if cid in seen_crit_ids:
            failures.append(f"{cid}: criteria id {cid!r} is not unique")
        seen_crit_ids.add(cid)
        if not CRITERIA_ID_SHAPE.match(str(cid)):
            failures.append(
                f"{cid}: criteria id must start with a three-letter uppercase prefix"
            )
        else:
            one = CRITERIA_REDUNDANT_ONE.match(str(cid))
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
        channel = c.get("channel")
        if channel not in CRITERIA_CHANNELS:
            failures.append(
                f"{cid}: channel {channel!r} is not a criteria channel"
            )
        if channel == "conformance":
            if not str(cid).startswith(CONFORMANCE_PREFIXES):
                failures.append(
                    f"{cid}: conformance criteria use the CNF- or REQ- prefix"
                )
        outcome = c.get("outcome")
        if channel == "score" and catalogue_ok:
            cat_id = c.get("catalogue_id")
            if not multi and cid != cat_id:
                failures.append(
                    f"{cid}: id must equal catalogue_id {cat_id!r} in a "
                    "single-project model"
                )
            entry = cat_entries.get(cat_id)
            if entry is None:
                failures.append(
                    f"{cid}: catalogue_id {cat_id!r} is not in catalogue "
                    f"version {catalogue.get('catalogue_version')}"
                )
            else:
                leaf = (
                    str(dimension).partition(".")[2]
                    if isinstance(dimension, str) and "." in dimension
                    else dimension
                )
                for field, value in (
                    ("dimension", leaf),
                    ("weight", c.get("weight")),
                    ("criticality", c.get("criticality")),
                ):
                    if value != entry.get(field):
                        failures.append(
                            f"{cid}: {field} {value!r} differs from the "
                            f"catalogue value {entry.get(field)!r}"
                        )
                allowed = set(entry.get("levels", {}))
                level = c.get("level")
                if outcome in RESOLVED:
                    if level not in allowed:
                        failures.append(
                            f"{cid}: level {level!r} is not allowed by the "
                            "catalogue"
                        )
                    elif LEVEL_OUTCOME.get(level) != outcome:
                        failures.append(
                            f"{cid}: level {level} does not match outcome "
                            f"{outcome}"
                        )
                    else:
                        value = level_values[level]
                        mastery = c.get("mastery")
                        numeric = isinstance(mastery, (int, float))
                        if not numeric or Fraction(str(mastery)) != value:
                            shown = f"{mastery:g}" if numeric else repr(mastery)
                            failures.append(
                                f"{cid}: mastery {shown} does not equal "
                                f"level {level} value {float(value):g}"
                            )
                elif level is not None:
                    if level not in allowed:
                        failures.append(
                            f"{cid}: level {level!r} is not allowed by the "
                            "catalogue"
                        )
                    else:
                        failures.append(
                            f"{cid}: level {level} does not match outcome "
                            f"{outcome}"
                        )
                if outcome == "NOT_APPLICABLE":
                    if c.get("na_basis") not in entry.get("na_rules", []):
                        failures.append(
                            f"{cid}: na_basis {c.get('na_basis')} is not a "
                            "declared N/A rule for this criteria entry"
                        )
                if (
                    "census-none" in entry.get("na_rules", [])
                    and (owner_project(dimension) or {}).get(
                        "automation_census"
                    ) == "none"
                    and (
                        outcome != "NOT_APPLICABLE"
                        or c.get("na_basis") != "census-none"
                    )
                ):
                    failures.append(
                        f"{cid}: automation census none makes this criteria entry "
                        "NOT_APPLICABLE (census-none)"
                    )
                if (
                    "history-out-of-scope" in entry.get("na_rules", [])
                    and scope.get("history") in ("absent", "out-of-scope")
                    and (
                        outcome != "NOT_APPLICABLE"
                        or c.get("na_basis") != "history-out-of-scope"
                    )
                ):
                    failures.append(
                        f"{cid}: scope.history {scope.get('history')} makes "
                        "this criteria entry NOT_APPLICABLE (history-out-of-scope)"
                    )
        if outcome not in CRITERIA_OUTCOMES:
            failures.append(f"{cid}: outcome {outcome!r} is not a criteria state")
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
            cited = bool(open_findings_by_criteria.get(c.get("id")))
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

    if catalogue_ok:
        applicable_entries = [
            entry for entry in catalogue.get("criteria", [])
            if "*" in entry.get("natures", [])
            or set(entry.get("natures", [])) & set(natures)
        ]

        def project_score_criteria(prefix) -> list[dict]:
            if prefix is None:
                return [c for c in criteria if c.get("channel") == "score"]
            return [
                c for c in criteria
                if c.get("channel") == "score"
                and isinstance(c.get("dimension"), str)
                and c["dimension"].startswith(prefix + ".")
            ]

        for name in (sorted(named) if multi else [None]):
            cset = project_score_criteria(name)
            label = name if name is not None else "subject"
            for entry in applicable_entries:
                count = sum(
                    1 for c in cset
                    if c.get("catalogue_id") == entry.get("id")
                )
                if count == 0:
                    failures.append(
                        f"{label}: catalogue criteria {entry.get('id')} is "
                        "missing from the model"
                    )
                elif count > 1:
                    failures.append(
                        f"{label}: catalogue criteria {entry.get('id')} "
                        f"appears {count} times"
                    )

    for e in evidence:
        eid = e.get("id", "<no id>")
        if e.get("kind") not in EVIDENCE_KINDS:
            failures.append(f"{eid}: kind {e.get('kind')!r} is not an evidence kind")
        for claim in e.get("claims", []):
            if claim not in crit_ids:
                failures.append(f"{eid}: claims unknown criteria {claim}")

    for f in findings:
        fid = f.get("id", "<no id>")
        if f.get("criteria") not in crit_ids:
            failures.append(f"{fid}: criteria {f.get('criteria')!r} is undeclared")
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
            c = crit_by_id.get(f.get("criteria"))
            if c is not None:
                cid = c.get("id")
                outcome = c.get("outcome")
                if outcome in RESOLVED:
                    mastery = criteria_mastery(c)
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
                        f"criteria {cid} - a confirmed finding resolves its "
                        "criteria entry"
                    )
                elif outcome == "NOT_APPLICABLE":
                    if not (
                        f.get("absence")
                        and c.get("na_basis") in ("census-none", "history-out-of-scope")
                    ):
                        failures.append(
                            f"{fid}: open {f.get('claim_class')} cites inapplicable "
                            f"criteria {cid} without the absence exemption"
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
        if c.get("channel") == "score":
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

    recomputed: dict[str, dict] = {}
    for dim, cs in dimensions.items():
        applicable, mastery, lo, hi, coverage, eligible = recompute_dimension(cs, backing)
        if not applicable:
            continue
        record = dims.get(dim)
        if not eligible:
            sub_lo = scale_score(lo, scale_max) if lo is not None else 1
            sub_hi = scale_score(hi, scale_max) if hi is not None else scale_max
            recomputed[dim] = {
                "eligible": False, "score": None, "lo": sub_lo, "hi": sub_hi,
            }
            if record is None:
                failures.append(
                    f"dimension '{dim}' has applicable criteria but no score "
                    "record"
                )
                continue
            if record.get("eligible") or record.get("score") is not None:
                failures.append(
                    f"dimension '{dim}': fails the eligibility gate but carries a "
                    "numeric score or eligible flag"
                )
            continue
        if record is None:
            failures.append(f"dimension '{dim}' has applicable criteria but no score record")
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
                and crit_dim.get(f.get("criteria")) == dim
            ),
            "severity-high": sorted(
                f.get("id") for f in bounding
                if f.get("severity") == "HIGH"
                and crit_dim.get(f.get("criteria")) == dim
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
        recomputed[dim] = {
            "eligible": True, "score": expected, "lo": lo_s, "hi": hi_s,
        }

    requirements = model.get("requirements", [])
    if not isinstance(requirements, list):
        failures.append(
            f"requirements is {type(requirements).__name__}, expected a list"
        )
        requirements = []
    req_ids: set[str] = set()
    for r in requirements:
        rid = r.get("id", "<no id>")
        if rid in req_ids:
            failures.append(f"{rid}: id {rid!r} is invalid")
        req_ids.add(rid)
        if r.get("obligation") not in OBLIGATIONS:
            failures.append(
                f"{rid}: obligation {r.get('obligation')!r} is invalid"
            )
        if r.get("status") not in REQUIREMENT_STATES:
            failures.append(f"{rid}: status {r.get('status')!r} is invalid")
        if r.get("status") in ("PARTIAL", "FAIL"):
            target = next(
                (f for f in findings if f.get("id") == r.get("finding")), None
            )
            if target is None or target.get("status") != "Open":
                failures.append(
                    f"{rid}: {r.get('status')} requirement needs an open finding"
                )
        for eid in r.get("evidence", []):
            if eid not in evd_ids:
                failures.append(f"{rid}: cites unknown evidence {eid}")
    if requirements:
        digest = hashlib.sha256(
            "\n".join(
                sorted(
                    f"{r.get('id')}:{r.get('obligation')}"
                    for r in requirements
                )
            ).encode("utf-8")
        ).hexdigest()
        if scope.get("requirements_baseline") != digest:
            failures.append(
                "requirements_baseline does not match the requirements "
                "registry"
            )
    elif scope.get("requirements_baseline") is not None:
        failures.append(
            "requirements_baseline does not match the requirements registry"
        )

    if catalogue_ok:
        REQ_VALUES = {
            "PASS": Fraction(1), "PARTIAL": Fraction(1, 2), "FAIL": Fraction(0),
        }
        mandatory = [
            r for r in requirements if r.get("obligation") == "mandatory"
        ]
        n_req = len(mandatory)
        graded = [r for r in mandatory if r.get("status") != "UNKNOWN"]
        g_req = len(graded)
        coverage_req = (
            sum(
                (REQ_VALUES.get(r.get("status"), Fraction(0)) for r in graded),
                Fraction(0),
            )
            / g_req if g_req else Fraction(0)
        )
        if n_req == 0:
            computed = "NOT_APPLICABLE"
        elif g_req * 2 <= n_req:
            computed = "UNKNOWN"
        else:
            computed = "FAIL"
            for bound, level in (
                (Fraction(19, 20), "PASS"), (Fraction(17, 20), "P75"),
                (Fraction(7, 10), "P50"), (Fraction(1, 2), "P25"),
            ):
                if coverage_req >= bound:
                    computed = level
                    break
        for c in criteria:
            if c.get("channel") != "score":
                continue
            entry = cat_entries.get(c.get("catalogue_id"))
            if not isinstance(entry, dict) or not entry.get("mechanical"):
                continue
            cid = c.get("id", "<no id>")
            expected_level = computed if computed in LEVEL_VALUES else None
            expected_outcome = (
                LEVEL_OUTCOME[computed]
                if expected_level is not None else computed
            )
            if (
                c.get("level") != expected_level
                or c.get("outcome") != expected_outcome
            ):
                failures.append(
                    f"{cid}: level {c.get('level')!r} does not match the "
                    f"computed {computed} (coverage "
                    f"{float(coverage_req):.3f} over {g_req} of {n_req} "
                    "mandatory requirements)"
                )
            elif computed == "NOT_APPLICABLE" and (
                c.get("na_basis") != "deployment-model"
                or c.get("applicability") != FNC_REQ_APPLICABILITY
            ):
                failures.append(
                    f"{cid}: NOT_APPLICABLE requires na_basis "
                    "deployment-model and applicability "
                    f"'{FNC_REQ_APPLICABILITY}'"
                )

    scores = model.get("scores", {})
    if "overall" in scores:
        failures.append(
            "scores.overall is removed in model v2 - record product, process, "
            "and single"
        )
    if multi:
        for key in ("product", "process", "single"):
            if key in scores:
                failures.append(
                    f"scores.{key} must be absent in a multi-project model - "
                    "record scores.per_project"
                )
    elif "per_project" in scores:
        failures.append(
            "scores.per_project must be absent in a single-project model"
        )

    def project_dims(prefix) -> dict:
        """compute_headline `dims` input for one scoring scope."""
        leaf_dims = {}
        for leaf in CANONICAL_DIMENSIONS:
            key = f"{prefix}.{leaf}" if prefix is not None else leaf
            entry = recomputed.get(key)
            if entry is not None:
                leaf_dims[leaf] = {"applicable": True, **entry}
        return leaf_dims

    def project_open(prefix) -> tuple[bool, bool]:
        """Open CRITICAL/HIGH bounding findings in one scoring scope."""
        critical = high = False
        for f in bounding:
            if prefix is not None:
                dim = crit_dim.get(f.get("criteria"))
                if not isinstance(dim, str) or not dim.startswith(prefix + "."):
                    continue
            if f.get("severity") == "CRITICAL":
                critical = True
            if f.get("severity") == "HIGH":
                high = True
        return critical, high

    def fields_match(record, expected) -> list[tuple]:
        mismatches = []
        for field, want in expected.items():
            got = record.get(field)
            if field == "interval":
                ok = (
                    got is None if want is None else
                    isinstance(got, list) and len(got) == 2
                    and all(
                        isinstance(g, (int, float)) and abs(g - w) < 0.001
                        for g, w in zip(got, want)
                    )
                )
            elif field in ("score", "raw"):
                ok = (
                    got is None if want is None else
                    isinstance(got, (int, float)) and abs(got - want) < 0.001
                )
            else:
                ok = got == want
            if not ok:
                mismatches.append((field, got, want))
        return mismatches

    readiness = model.get("readiness", {})
    readiness = readiness if isinstance(readiness, dict) else {}
    scopes = sorted(named) if multi else [None]
    per_project = scores.get("per_project", {})
    for name in scopes:
        prefix = name if multi else None
        critical_open, high_open = project_open(prefix)
        if prefix is None:
            records = scores
            readiness_record = readiness
        else:
            records = per_project.get(name)
            if not isinstance(records, dict):
                failures.append(
                    f"per_project record missing for project {name!r}"
                )
                continue
            readiness_record = (
                readiness.get("per_project", {}).get(name, {})
                if isinstance(readiness.get("per_project"), dict) else {}
            )
        state = readiness_record.get("state")
        expected = compute_headline(
            project_dims(prefix), scale_max, critical_open, high_open, state
        )
        for rec_name, expected_record in expected.items():
            label = (
                rec_name if prefix is None
                else f"per_project[{name}].{rec_name}"
            )
            record = records.get(rec_name)
            record = record if isinstance(record, dict) else {}
            for field, got, want in fields_match(record, expected_record):
                failures.append(
                    f"{label}.{field} {got!r} does not recompute to {want!r}"
                )

    known_ids = (
        fnd_ids
        | {r.get("id") for r in risks}
        | {r.get("id") for r in recommendations}
    )

    def check_readiness_record(record, label, prefix) -> None:
        state = record.get("state")
        if state not in READINESS_STATES:
            failures.append(f"{label}.state {state!r} is not a readiness state")
        blocking = record.get("blocking")
        blocking = blocking if isinstance(blocking, list) else []
        for bid in blocking:
            if not (
                isinstance(bid, str)
                and (bid in known_ids or bid.startswith("gate:"))
            ):
                failures.append(f"{label}.blocking cites unknown {bid}")
        if state == "READY":
            for f in bounding:
                if f.get("severity") not in ("CRITICAL", "HIGH"):
                    continue
                if prefix is not None:
                    dim = crit_dim.get(f.get("criteria"))
                    if not isinstance(dim, str) or not dim.startswith(
                        prefix + "."
                    ):
                        continue
                failures.append(
                    f"{label} READY conflicts with open "
                    f"{f.get('severity')} finding {f.get('id')}"
                )
        if state in ("NOT READY", "PENDING EVIDENCE") and not blocking:
            failures.append(
                f"{label} {state} needs at least one blocking id"
            )
        if (
            state == "NOT ASSESSED"
            and "readiness" in str(scope.get("purpose", "")).lower()
        ):
            failures.append(
                f"{label} NOT ASSESSED conflicts with a readiness purpose"
            )

    if multi:
        per_project_readiness = readiness.get("per_project", {})
        per_project_readiness = (
            per_project_readiness
            if isinstance(per_project_readiness, dict) else {}
        )
        for name in sorted(named):
            record = per_project_readiness.get(name)
            if not isinstance(record, dict):
                failures.append(
                    f"readiness.per_project record missing for project "
                    f"{name!r}"
                )
                continue
            check_readiness_record(
                record, f"per_project[{name}].readiness", name
            )
    else:
        check_readiness_record(readiness, "readiness", None)

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
    parser.add_argument(
        "--fix",
        action="store_true",
        help="recompute mechanically derived records (criteria mastery, "
        "mechanical criteria, requirements baseline, dimension scores, and "
        "the product/process/single or per_project headline) in place, then "
        "run the check",
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

    if args.fix:
        changes = fix_model(model, load_catalogue())
        if changes:
            path.write_text(
                json.dumps(model, indent=1) + "\n", encoding="utf-8"
            )
            print(f"check-model --fix: {len(changes)} change(s)")
            for change in changes:
                print(f"  FIX {change}")
        else:
            print("check-model --fix: model already consistent")

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
