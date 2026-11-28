"""Contract tests for `scripts/continue-history.py`."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests import SCRIPTS

SCRIPT = SCRIPTS / "continue-history.py"
CATEGORIES = [{"id": "fix", "label": "Fixes", "color": "#e64980", "order": 30}]


def _version(name: str, kind: str, span: list[int], start: str, end: str, sha: tuple) -> dict:
    return {"version": name, "kind": kind, "range": {"from": sha[0], "to": sha[1]},
            "dates": {"from": start, "to": end}, "stats": {"commits": span[1] - span[0] + 1},
            "commit_span": span, "events": [], "eventCounts": {}, "gapDays": 0}


def _prior() -> dict:
    return {
        "schema": 2,
        "view": {"layout": "islands", "theme": "dark", "palette": "green"},
        "project": {"name": "example-service", "description": "Example.", "repository": "origin",
                    "generated": "2026-01-10T00:00:00+00:00", "head": "f" * 40, "commits": 30,
                    "span": {"from": "2025-01-01T00:00:00+00:00", "to": "2026-01-10T00:00:00+00:00"}},
        "categories": CATEGORIES,
        "versions": [
            _version("1.0.0", "release", [0, 19], "2025-01-01", "2025-06-01", ("a" * 40, "b" * 40)),
            _version("1.1.0", "developing", [20, 29], "2025-06-02", "2026-01-10",
                     ("c" * 40, "f" * 40)),
        ],
    }


def _update() -> dict:
    newer = [_version("1.1.0", "release", [0, 14], "2025-06-02", "2026-02-01", ("c" * 40, "d" * 40)),
             _version("1.2.0", "developing", [15, 19], "2026-02-10", "2026-03-01",
                      ("e" * 40, "9" * 40))]
    newer[1]["events"] = [{"type": "chore", "title": "x", "date": "2026-02-10", "sha": "e" * 40}]
    return {"schema": 2, "view": {"layout": "square", "theme": "day", "palette": "blue"},
            "project": {"name": "renamed", "generated": "2026-03-02T00:00:00+00:00",
                        "head": "9" * 40, "commits": 20,
                        "span": {"from": "2025-06-02T00:00:00+00:00",
                                 "to": "2026-03-01T00:00:00+00:00"}},
            "categories": CATEGORIES + [{"id": "chore", "label": "Chores", "color": "#364fc7",
                                         "order": 70}],
            "versions": newer}


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True,
                          timeout=60)


class ContinueHistoryTests(unittest.TestCase):
    def test_merge_keeps_prior_eras_and_settings(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            (root / "prior.json").write_text(json.dumps(_prior()), encoding="utf-8")
            (root / "update.json").write_text(json.dumps(_update()), encoding="utf-8")
            result = _run("merge", "--prior", str(root / "prior.json"), "--update",
                          str(root / "update.json"), "--out", str(root / "out.json"),
                          "--provenance", str(root / "prov.json"))
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads((root / "out.json").read_text(encoding="utf-8"))
            self.assertEqual([v["version"] for v in data["versions"]], ["1.0.0", "1.1.0", "1.2.0"])
            self.assertEqual(data["versions"][1]["kind"], "release")
            self.assertEqual(data["view"]["layout"], "islands")
            self.assertEqual(data["project"]["name"], "example-service")
            self.assertEqual(data["project"]["span"]["from"], "2025-01-01T00:00:00+00:00")
            self.assertEqual(data["versions"][1]["commit_span"], [20, 34])
            self.assertIn("chore", [c["id"] for c in data["categories"]])
            self.assertEqual(json.loads((root / "prov.json").read_text())["anchor"], "1.1.0")

    def test_reads_packed_html_and_shim(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            payload = json.dumps(_prior()).replace("</", "<\\/")
            (root / "prior.html").write_text(
                "<html><script>/* window.HISTORY_DATA = maybe */</script>"
                f"<script>window.HISTORY_DATA = {payload};</script></html>", encoding="utf-8")
            (root / "history.js").write_text(f"window.HISTORY_DATA = {json.dumps(_prior())};\n",
                                             encoding="utf-8")
            (root / "update.json").write_text(json.dumps(_update()), encoding="utf-8")
            for prior in ("prior.html", "history.js"):
                result = _run("merge", "--prior", str(root / prior), "--update",
                              str(root / "update.json"), "--out", str(root / "out.json"))
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_plan_reports_anchor_without_repository_commits(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            subprocess.run(["git", "init", "-q", str(root / "repo")], check=True)
            (root / "prior.json").write_text(json.dumps(_prior()), encoding="utf-8")
            result = _run("plan", "--prior", str(root / "prior.json"), "--repo", str(root / "repo"))
            self.assertEqual(result.returncode, 0, result.stderr)
            plan = json.loads(result.stdout)
            self.assertEqual(plan["anchor"], "1.1.0")
            self.assertEqual(plan["kept"], ["1.0.0"])
            self.assertTrue(plan["truncated_history"])
            self.assertIsNone(plan["gather_from"])
            self.assertIn("warning", plan)
            self.assertEqual(plan["settings"]["view"]["palette"], "green")


if __name__ == "__main__":
    unittest.main()
