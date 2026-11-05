#!/usr/bin/env python3
"""Compare two or more policy-3 audit models side by side.

Reads model-version-2 audit models (scoring policy 3, same catalogue
version) and emits a comparison that refuses to rank across incompatible
denominators: unpublished product or process records and mismatched
`product-only` overall flags render `not comparable` rather than a
substituted mean. Multi-project models pair projects by
`scope.projects[].name` - an unpaired project is listed, never compared.

Usage:
    python3 scripts/compare-models.py <audit-model.json> <audit-model.json> [<audit-model.json> ...] [--json] [--anyway]

`--anyway` proceeds across a `scope.detail_level` mismatch - the output
carries `detail_level_mismatch: true` and a warning line. It never
suppresses the absence-based refusals.

Exit code 0 means the comparison ran, 2 means usage, read, model-check,
or compatibility-gate failures.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


def _load_script(name: str):
    """Load `scripts/<name>` as a module - the hyphen blocks `import`."""
    spec = importlib.util.spec_from_file_location(
        name.replace("-", "_").removesuffix(".py"),
        Path(__file__).resolve().parent / name,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CHECK = _load_script("check-model.py")
TABLES = _load_script("render-tables.py")

PRODUCT_FIELDS = (
    "score", "interval", "published", "lowest",
    "eligible_weight", "applicable_weight",
)
PROCESS_FIELDS = (
    "score", "interval", "published", "lowest", "scored", "applicable",
)
SINGLE_FIELDS = ("score", "raw", "interval", "flag", "ceiling", "band")


def _pick(record: dict, fields: tuple) -> dict:
    return {field: record.get(field) for field in fields}


def _named_projects(model: dict) -> list:
    return [
        p.get("name")
        for p in model.get("scope", {}).get("projects", [])
        if isinstance(p, dict) and p.get("name")
    ]


def _is_multi(model: dict) -> bool:
    return len(_named_projects(model)) >= 2


def _headline_records(model: dict, key) -> dict:
    """The product/process/single record block for one compared scope."""
    scores = model.get("scores", {})
    if key is not None:
        record = scores.get("per_project", {}).get(key)
        if isinstance(record, dict):
            return record
        if not _is_multi(model):
            return scores
        return {}
    return scores


def _dimension_records(model: dict, key) -> dict:
    """Canonical-id-keyed dimension records for one compared scope."""
    dims = model.get("scores", {}).get("dimensions", {})
    if key is None or not _is_multi(model):
        return dims
    prefix = f"{key}."
    return {
        name[len(prefix):]: record
        for name, record in dims.items()
        if name.startswith(prefix)
    }


def _criterion_map(model: dict) -> dict:
    return {c.get("id"): c for c in model.get("criteria", [])}


def _criterion_family(criteria: dict, criterion_id) -> str:
    """Catalogue-level criterion identity, stable across audit runs."""
    criterion = criteria.get(criterion_id) or {}
    return criterion.get("catalogue_id") or criterion_id


def _model_findings(model: dict, key) -> tuple:
    """(findings, criterion map) owned by one compared scope."""
    criteria = _criterion_map(model)
    multi = _is_multi(model)
    selected = []
    for finding in model.get("findings", []):
        criterion = criteria.get(finding.get("criterion")) or {}
        dimension = criterion.get("dimension")
        owner = (
            dimension.partition(".")[0]
            if isinstance(dimension, str) and "." in dimension else None
        )
        if multi:
            if owner == key:
                selected.append(finding)
        elif owner is None or owner == key:
            selected.append(finding)
    return selected, criteria


def _finding_key(finding: dict, criteria: dict) -> tuple:
    return (
        finding.get("claim_class"),
        finding.get("severity"),
        _criterion_family(criteria, finding.get("criterion")),
    )


def _flag_state(record: dict) -> str:
    if record.get("score") is None:
        return "unpublished"
    return record.get("flag") or "full"


def _delta_suffix(scores: list, labels: list) -> str:
    """`delta`-cell text: each later model's score minus the first."""
    parts = []
    for i in range(1, len(labels)):
        if scores[i] is None or scores[0] is None:
            parts.append(f"{labels[i]}-{labels[0]} -")
        else:
            parts.append(f"{labels[i]}-{labels[0]} {scores[i] - scores[0]:.1f}")
    return "delta " + ", ".join(parts)


def _diff_dimensions(models: list, labels: list, key) -> list:
    """One row per canonical dimension applicable in any model."""
    records = [_dimension_records(m, key) for m in models]
    rows = []
    for dim in TABLES.DIMENSION_ORDER:
        cells = []
        applicable = False
        for dims in records:
            record = dims.get(dim)
            if not isinstance(record, dict) or record.get("applicable") is False:
                cells.append(("-", None))
                continue
            applicable = True
            score = record.get("score")
            if isinstance(score, (int, float)):
                cells.append((score, score))
            else:
                cells.append(("Unknown", None))
        if not applicable:
            continue
        row = {"dim": dim}
        for label, (display, _numeric) in zip(labels, cells):
            row[label] = display
        numerics = [numeric for _display, numeric in cells]
        if len(labels) == 2:
            row["delta"] = (
                numerics[1] - numerics[0]
                if numerics[0] is not None and numerics[1] is not None
                else "-"
            )
        else:
            row["delta"] = {
                labels[i]: (
                    numerics[i] - numerics[0]
                    if numerics[i] is not None and numerics[0] is not None
                    else "-"
                )
                for i in range(1, len(labels))
            }
        rows.append(row)
    return rows


def _diff_findings(models: list, labels: list, key) -> dict:
    """Set diff by normalized claim: (claim_class, severity, criterion)."""
    grouped: dict = {}
    for label, model in zip(labels, models):
        findings, criteria = _model_findings(model, key)
        for finding in findings:
            grouped.setdefault(
                _finding_key(finding, criteria), []
            ).append((label, finding))
    rank = {s: i for i, s in enumerate(CHECK.SEVERITIES)}
    order = sorted(
        grouped, key=lambda k: (rank.get(k[1], len(rank)), str(k[0]), str(k[2]))
    )
    common, partial = [], []
    only = {label: [] for label in labels}
    for fkey in order:
        claim_class, severity, criterion = fkey

        def brief(f):
            return {
                "id": f.get("id"), "claim_class": claim_class,
                "severity": severity, "criterion": criterion,
            }

        per_label = {
            l: [f for lb, f in grouped[fkey] if lb == l] for l in labels
        }
        owners = [l for l in labels if per_label[l]]
        if len(owners) == len(labels):
            count = min(len(per_label[l]) for l in labels)
            for i in range(count):
                ids = {l: per_label[l][i].get("id") for l in labels}
                common.append({
                    "ids": ids, "claim_class": claim_class,
                    "severity": severity, "criterion": criterion,
                    "matched_by": (
                        "exact id" if len(set(ids.values())) == 1
                        else "normalized claim"
                    ),
                })
            for l in labels:
                for f in per_label[l][count:]:
                    only[l].append(brief(f))
        elif len(owners) == 1:
            for f in per_label[owners[0]]:
                only[owners[0]].append(brief(f))
        else:
            for l in owners:
                for f in per_label[l]:
                    partial.append({**brief(f), "in": owners})
    block = {
        "counts": {
            "common": len(common),
            **{f"only_in_{l}": len(only[l]) for l in labels},
        },
        "common": common,
    }
    for l in labels:
        block[f"only_in_{l}"] = only[l]
    if partial:
        block["partial"] = partial
        block["counts"]["partial"] = len(partial)
    return block


def _diff_requirements(models: list, labels: list) -> dict:
    """Set diff on requirements[].id with status deltas on shared ids."""
    registries = [
        {
            r.get("id"): r for r in m.get("requirements", [])
            if isinstance(r, dict)
        }
        for m in models
    ]
    all_ids = sorted({rid for reg in registries for rid in reg})
    shared, partial = [], []
    only = {label: [] for label in labels}
    for rid in all_ids:
        owners = [l for l, reg in zip(labels, registries) if rid in reg]
        status = {
            l: registries[i][rid].get("status")
            for i, l in enumerate(labels) if rid in registries[i]
        }
        if len(owners) == len(labels):
            shared.append({
                "id": rid, "status": status,
                "changed": len(set(status.values())) > 1,
            })
        elif len(owners) == 1:
            only[owners[0]].append({"id": rid, "status": status[owners[0]]})
        else:
            partial.append({"id": rid, "in": owners, "status": status})
    block = {
        "counts": {
            "common": len(shared),
            **{f"only_in_{l}": len(only[l]) for l in labels},
        },
        "shared": shared,
    }
    for l in labels:
        block[f"only_in_{l}"] = only[l]
    if partial:
        block["partial"] = partial
        block["counts"]["partial"] = len(partial)
    return block


def _scope_keys(models: list, labels: list) -> tuple:
    """(compared scope keys, unpaired list) from project-name pairing."""
    named = [_named_projects(m) for m in models]
    if not any(len(ns) >= 2 for ns in named):
        return [None], []
    sets = [set(ns) for ns in named]
    common = set.intersection(*sets) if sets else set()
    union = set.union(*sets) if sets else set()
    unpaired = [
        {
            "name": name,
            "only_in": [l for l, s in zip(labels, sets) if name in s],
        }
        for name in sorted(union - common)
    ]
    return sorted(common), unpaired


def _compare_scope(models: list, labels: list, key, scale_max: int) -> dict:
    records = [_headline_records(m, key) for m in models]
    product = [r.get("product") or {} for r in records]
    process = [r.get("process") or {} for r in records]
    single = [r.get("single") or {} for r in records]

    if all(p.get("published") for p in product):
        product_cmp = _delta_suffix([p.get("score") for p in product], labels)
        product_ok = True
    else:
        weights = ", ".join(
            f"{l} {p.get('eligible_weight')}/{p.get('applicable_weight')}"
            for l, p in zip(labels, product)
        )
        product_cmp = f"not comparable - product unpublished ({weights})"
        product_ok = False

    if all(p.get("published") for p in process):
        process_cmp = _delta_suffix([p.get("score") for p in process], labels)
        process_ok = True
    else:
        weights = ", ".join(
            f"{l} {p.get('scored')}/{p.get('applicable')}"
            for l, p in zip(labels, process)
        )
        process_cmp = f"not comparable - process unpublished ({weights})"
        process_ok = False

    states = [_flag_state(s) for s in single]
    published = all(s.get("score") is not None for s in single)
    if published and len(set(states)) == 1:
        single_cmp = _delta_suffix([s.get("score") for s in single], labels)
        single_ok = True
    else:
        if not published:
            who = ", ".join(
                l for l, s in zip(labels, single) if s.get("score") is None
            )
            single_cmp = f"not comparable ({who} unpublished)"
        else:
            single_cmp = f"not comparable ({' vs '.join(states)})"
        single_ok = False

    if single_ok:
        order = sorted(
            range(len(labels)), key=lambda i: -float(single[i]["score"])
        )
        leader, trailer = order[0], order[-1]
        delta = float(single[leader]["score"]) - float(single[trailer]["score"])
        line = (
            f"ranking: {labels[leader]} leads {labels[trailer]} by "
            f"{delta:.1f} ({' vs '.join(states)})"
        )
    else:
        reasons = []
        if not published:
            reasons.append(", ".join(
                f"{l} single unpublished" for l, s in zip(labels, single)
                if s.get("score") is None
            ))
        if len(set(states)) > 1:
            reasons.append("flags differ")
        line = (
            f"ranking: {' vs '.join(labels)} not comparable - "
            f"{'; '.join(reasons)} ({' vs '.join(states)})"
        )

    return {
        "scope": "subject" if key is None else key,
        "product": {
            "comparable": product_ok, "comparison": product_cmp,
            **{l: _pick(p, PRODUCT_FIELDS) for l, p in zip(labels, product)},
        },
        "process": {
            "comparable": process_ok, "comparison": process_cmp,
            **{l: _pick(p, PROCESS_FIELDS) for l, p in zip(labels, process)},
        },
        "single": {
            "comparable": single_ok, "comparison": single_cmp,
            "flags": {l: s for l, s in zip(labels, states)},
            **{l: _pick(s, SINGLE_FIELDS) for l, s in zip(labels, single)},
        },
        "dimensions": _diff_dimensions(models, labels, key),
        "findings": _diff_findings(models, labels, key),
        "requirements": _diff_requirements(models, labels),
        "ranking": {"comparable": single_ok, "line": line},
    }


def compare(models: list, labels: list | None = None,
            paths: list | None = None, anyway: bool = False,
            catalogue: dict | None = None) -> tuple:
    """Run the model check, the compatibility gate, then the comparison.

    Returns `(result, failures)` - `failures` non-empty means the gate
    refused the comparison and `result` is None. `catalogue` is passed
    through to `check_model`; None loads the skill catalogue.
    """
    labels = labels or [f"m{i + 1}" for i in range(len(models))]
    failures: list[str] = []
    for label, model in zip(labels, models):
        for failure in CHECK.check_model(model, catalogue):
            failures.append(f"{label}: {failure}")
    if failures:
        return None, failures

    scopes = [m.get("scope", {}) for m in models]
    blocks = [m.get("scores", {}) for m in models]
    for field, values in (
        ("catalogue_version", [s.get("catalogue_version") for s in scopes]),
        ("scoring_policy", [s.get("scoring_policy") for s in scopes]),
        ("scale_max", [s.get("scale_max") for s in blocks]),
    ):
        if len({repr(v) for v in values}) > 1:
            detail = ", ".join(f"{l} {v!r}" for l, v in zip(labels, values))
            failures.append(f"{field} differs ({detail})")
    if failures:
        return None, failures

    levels = [s.get("detail_level") for s in scopes]
    mismatch = len({repr(v) for v in levels}) > 1
    warning = None
    if mismatch:
        detail = ", ".join(f"{l} {v}" for l, v in zip(labels, levels))
        if not anyway:
            return None, [
                f"detail_level differs ({detail}) - rerun with --anyway"
            ]
        warning = f"detail_level differs ({detail}) - comparing anyway"

    keys, unpaired = _scope_keys(models, labels)
    scale_max = blocks[0].get("scale_max", 10)
    result = {
        "models": [
            {"label": l, **({"path": p} if p else {})}
            for l, p in zip(labels, paths or labels)
        ],
        "scale_max": scale_max,
        "detail_level_mismatch": mismatch,
        "compared": [
            _compare_scope(models, labels, key, scale_max) for key in keys
        ],
        "unpaired": unpaired,
    }
    if warning:
        result["warning"] = warning
    return result, []


def _headline_cell(record: dict, scale_max: int, kind: str) -> str:
    if not record.get("published"):
        if kind == "product":
            weight = (
                f"{record.get('eligible_weight')}/"
                f"{record.get('applicable_weight')}"
            )
        else:
            weight = f"{record.get('scored')}/{record.get('applicable')}"
        return f"not published ({weight})"
    cell = f"{float(record.get('score')):.1f}/{scale_max}"
    interval = record.get("interval")
    if interval:
        cell += f" [{interval[0]:g}-{interval[1]:g}]"
    lowest = record.get("lowest") or []
    if lowest:
        cell += " lowest " + ", ".join(str(d) for d in lowest)
    return cell


def _single_cell(record: dict) -> str:
    if record.get("score") is None:
        return "not published"
    parts = [_flag_state(record)]
    if record.get("band"):
        parts.append(str(record["band"]))
    ceiling = record.get("ceiling")
    if isinstance(ceiling, dict):
        parts.append(
            f"ceiling {ceiling.get('limit')}: "
            + "; ".join(str(r) for r in ceiling.get("reasons", []))
        )
    return f"{float(record['score']):.1f} " + ", ".join(parts)


def _cell(value) -> str:
    return f"{value:g}" if isinstance(value, (int, float)) else str(value)


def render_text(result: dict) -> str:
    """Aligned text rendering of a `compare()` result."""
    labels = [m["label"] for m in result["models"]]
    scale_max = result.get("scale_max", 10)
    lines = ["models:"]
    for m in result["models"]:
        lines.append(f"  {m['label']}  {m.get('path', '-')}")
    if result.get("warning"):
        lines.append(f"warning: {result['warning']}")
    for entry in result.get("unpaired", []):
        lines.append(
            f"unpaired: {entry['name']} (only in "
            f"{', '.join(entry['only_in'])})"
        )

    for comp in result["compared"]:
        lines.append("")
        lines.append(f"== {comp['scope']} ==")
        lines.append("")
        record_rows = [
            ["product",
             *[_headline_cell(comp["product"].get(l) or {}, scale_max,
                             "product") for l in labels],
             comp["product"]["comparison"]],
            ["process",
             *[_headline_cell(comp["process"].get(l) or {}, scale_max,
                             "process") for l in labels],
             comp["process"]["comparison"]],
            ["single",
             *[_single_cell(comp["single"].get(l) or {}) for l in labels],
             comp["single"]["comparison"]],
        ]
        lines.append(
            TABLES.render_table(["Record", *labels, "Comparison"], record_rows)
        )
        lines.append("")
        dim_rows = []
        for row in comp["dimensions"]:
            delta = row["delta"]
            if isinstance(delta, dict):
                delta = ", ".join(
                    f"{l} {_cell(v)}" for l, v in delta.items()
                )
            else:
                delta = _cell(delta)
            dim_rows.append(
                [row["dim"], *[_cell(row[l]) for l in labels], delta]
            )
        lines.append(
            TABLES.render_table(["Dimension", *labels, "delta"], dim_rows)
        )
        lines.append("")
        findings = comp["findings"]
        counts = findings["counts"]
        summary = [f"common {counts['common']}"]
        summary += [
            f"only_in_{l} {counts.get(f'only_in_{l}', 0)}" for l in labels
        ]
        if "partial" in counts:
            summary.append(f"partial {counts['partial']}")
        lines.append("findings: " + ", ".join(summary))
        for entry in findings["common"]:
            ids = ", ".join(entry["ids"].get(l) or "-" for l in labels)
            lines.append(
                f"  common  {ids}  {entry['claim_class']} / "
                f"{entry['severity']} / {entry['criterion']}  "
                f"(matched_by {entry['matched_by']})"
            )
        for l in labels:
            for entry in findings.get(f"only_in_{l}", []):
                lines.append(
                    f"  only_in_{l}  {entry['id']}  {entry['claim_class']} / "
                    f"{entry['severity']} / {entry['criterion']}"
                )
        for entry in findings.get("partial", []):
            lines.append(
                f"  shared ({', '.join(entry['in'])})  {entry['id']}  "
                f"{entry['claim_class']} / {entry['severity']} / "
                f"{entry['criterion']}"
            )
        lines.append("")
        requirements = comp["requirements"]
        req_rows = {}
        for entry in requirements["shared"]:
            req_rows[entry["id"]] = [
                entry["id"],
                *[str(entry["status"].get(l) or "-") for l in labels],
                "changed" if entry["changed"] else "same",
            ]
        for l in labels:
            for entry in requirements.get(f"only_in_{l}", []):
                req_rows[entry["id"]] = [
                    entry["id"],
                    *[
                        str(entry["status"]) if lb == l else "-"
                        for lb in labels
                    ],
                    f"only_in_{l}",
                ]
        for entry in requirements.get("partial", []):
            req_rows[entry["id"]] = [
                entry["id"],
                *[str(entry["status"].get(l) or "-") for l in labels],
                "shared " + ",".join(entry["in"]),
            ]
        lines.append(
            TABLES.render_table(
                ["Requirement", *labels, "delta"],
                [req_rows[rid] for rid in sorted(req_rows)],
            )
        )
        lines.append("")
        lines.append(comp["ranking"]["line"])
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Compare policy-3 audit models side by side"
    )
    parser.add_argument(
        "models", nargs="+", help="audit-model.json files to compare"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="emit the comparison as JSON instead of text",
    )
    parser.add_argument(
        "--anyway", action="store_true",
        help="proceed across a scope.detail_level mismatch",
    )
    args = parser.parse_args(argv)
    if len(args.models) < 2:
        parser.error("compare-models needs at least two model files")

    models = []
    for name in args.models:
        path = Path(name)
        if not path.is_file():
            print(f"compare-models: no such file: {name}", file=sys.stderr)
            return 2
        try:
            model = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(
                f"compare-models: cannot parse {name}: {exc}",
                file=sys.stderr,
            )
            return 2
        if not isinstance(model, dict):
            print(
                f"compare-models: {name}: top-level value is not an object",
                file=sys.stderr,
            )
            return 2
        models.append(model)

    labels = [f"m{i + 1}" for i in range(len(models))]
    result, failures = compare(
        models, labels=labels, paths=args.models, anyway=args.anyway
    )
    if failures:
        for label, name in zip(labels, args.models):
            print(f"compare-models: {label} = {name}", file=sys.stderr)
        for failure in failures:
            print(f"compare-models: {failure}", file=sys.stderr)
        return 2
    if args.json:
        if result.get("warning"):
            print(
                f"compare-models: warning: {result['warning']}",
                file=sys.stderr,
            )
        print(json.dumps(result, indent=1))
    else:
        sys.stdout.write(render_text(result))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
