#!/usr/bin/env python3
"""Validate a history.json dataset against references/history-schema.md.

Usage: python3 validate-history.py <history.json> [-v]

Mechanical checks for the producer contract and the verification gate in
process/history-visualisation.md. Exits 0 on a clean dataset, 1 listing
every violation found.
"""

import json
import re
import sys

KINDS = {"release", "changelog", "developing", "planned", "era"}
DATE_GROUPINGS = {"month", "quarter", "year", "gap"}
GROUPINGS = {"version"} | DATE_GROUPINGS
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
VIEW_KEYS = {"layout", "theme", "palette"}


def find_nulls(o, path):
    out = []
    if isinstance(o, dict):
        for k, v in o.items():
            if v is None:
                out.append(path + "." + str(k))
            else:
                out += find_nulls(v, path + "." + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            out += find_nulls(v, "%s[%d]" % (path, i))
    return out


def check(h, err):
    if not isinstance(h, dict):
        err.append("dataset is not a JSON object")
        return
    if not isinstance(h.get("schema"), int):
        err.append("schema: missing or not an integer")
    view = h.get("view")
    if view is not None:
        if not isinstance(view, dict):
            err.append("view: not an object")
        else:
            for k in view:
                if k not in VIEW_KEYS:
                    err.append("view: unknown key %r" % k)

    proj = h.get("project") or {}
    for f in ("name", "head", "commits", "span"):
        if f not in proj:
            err.append("project: missing %r" % f)
    grouping = proj.get("grouping")
    if grouping is not None and grouping not in GROUPINGS:
        err.append("project.grouping: unknown strategy %r" % grouping)

    cats = h.get("categories")
    if not isinstance(cats, list):
        err.append("categories: missing or not an array")
        cats = []
    ids = set()
    for i, c in enumerate(cats):
        for f in ("id", "label", "color", "order"):
            if f not in c:
                err.append("categories[%d]: missing %r" % (i, f))
        if c.get("id") in ids:
            err.append("categories[%d]: duplicate id %r" % (i, c.get("id")))
        ids.add(c.get("id"))
        if "color" in c and not re.match(r"^#[0-9a-fA-F]{6}$", str(c["color"])):
            err.append("categories[%d]: bad color %r" % (i, c.get("color")))

    vers = h.get("versions")
    if not isinstance(vers, list):
        err.append("versions: missing or not an array")
        vers = []

    seen_ver, prev_to = set(), None
    for vi, v in enumerate(vers):
        where = "versions[%d] %s" % (vi, v.get("version", "?"))
        if not isinstance(v.get("version"), str):
            err.append(where + ": version label missing")
        kind = v.get("kind")
        if kind not in KINDS:
            err.append(where + ": bad kind %r" % kind)
        if kind == "era" and grouping not in DATE_GROUPINGS:
            err.append(where + ": kind 'era' but project.grouping is %r" % grouping)
        if v.get("version") in seen_ver and not v.get("superseded"):
            err.append(where + ": duplicate version label not superseded")
        seen_ver.add(v.get("version"))

        stats = v.get("stats")
        metrics = v.get("metrics")
        if kind in ("release", "era", "developing"):
            if not stats:
                err.append(where + ": %s kind without stats" % kind)
            if stats and not metrics:
                err.append(where + ": stats present but metrics missing")
        if kind == "planned":
            if stats or v.get("dates"):
                err.append(where + ": planned record carries stats/dates")

        d = v.get("dates") or {}
        d_to = d.get("to")
        if prev_to and d.get("from") and "gapDays" in v:
            pass  # gapDays recompute is producer-side; presence checked only
        if d_to:
            prev_to = d_to

        counts = {}
        for e in v.get("events") or []:
            t = e.get("type")
            if t not in ids:
                err.append(where + ": event with unregistered type %r" % t)
            if not e.get("sha") and not e.get("ref"):
                err.append(where + ": event without sha or ref: %r" %
                           str(e.get("title", ""))[:60])
            if "date" not in e:
                err.append(where + ": event without date")
            counts[t] = counts.get(t, 0) + 1
        ec = v.get("eventCounts")
        if ec is not None and ec != counts:
            err.append(where + ": eventCounts %s != actual %s" % (ec, counts))

        cd = v.get("categoryDetail")
        if cd is not None:
            if not isinstance(cd, dict):
                err.append(where + ": categoryDetail not an object")
            else:
                delta = ((stats or {}).get("delta") or {})
                for k, blk in cd.items():
                    if k not in ids:
                        err.append(where + ": categoryDetail key %r not in registry" % k)
                    if not isinstance(blk, dict):
                        err.append(where + ": categoryDetail.%s not an object" % k)
                        continue
                    ev_n = blk.get("events")
                    if ev_n is not None and ev_n != counts.get(k, 0):
                        err.append(where + ": categoryDetail.%s.events=%s, actual %s"
                                   % (k, ev_n, counts.get(k, 0)))
                    ch = blk.get("churn")
                    if isinstance(ch, dict):
                        if delta.get("ins") is not None and \
                           (ch.get("ins") or 0) > delta["ins"]:
                            err.append(where + ": categoryDetail.%s.churn.ins %s > era delta %s"
                                       % (k, ch.get("ins"), delta["ins"]))

    err += ["null value at " + p for p in find_nulls(h, "$")]


def main(argv):
    if len(argv) < 2:
        print(__doc__.strip())
        return 2
    errors = []
    try:
        h = json.loads(open(argv[1], encoding="utf-8").read())
    except Exception as e:
        print("FAIL: cannot parse %s: %s" % (argv[1], e))
        return 1
    check(h, errors)
    if errors:
        print("FAIL: %d violation(s) in %s" % (len(errors), argv[1]))
        for e in errors:
            print("  - " + e)
        return 1
    print("OK: %s validates (schema %s, %d versions, %d categories)" % (
        argv[1], h.get("schema"), len(h.get("versions") or []),
        len(h.get("categories") or [])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
