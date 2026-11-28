"""Contract tests for the visualisation packer in `scripts/pack-visualisation.py`."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests import SCRIPTS, load_script


def _dataset(view=None) -> dict:
    data = {
        "schema": 2,
        "project": {"name": "example-service", "head": "a" * 40, "commits": 2,
                    "span": {"from": "2026-01-01", "to": "2026-01-31"}},
        "categories": [{"id": "fix", "label": "Fixes", "color": "#e64980", "order": 30}],
        "versions": [
            {"version": "1.0.0", "kind": "release", "events": [],
             "stats": {"delta": {"added": 1}}, "metrics": {"files": 1}},
            {"version": "1.1.0", "kind": "developing", "events": [],
             "stats": {"delta": {"added": 1}}, "metrics": {"files": 1}},
        ],
    }
    if view is not None:
        data["view"] = view
    return data


def _args(**kw) -> argparse.Namespace:
    base = {"layout": None, "theme": None, "palette": None}
    base.update(kw)
    return argparse.Namespace(**base)


SHELL = (
    "<html>\n<head></head>\n<body>\n<script>app()</script>\n"
    "<!-- dataset placeholder - replaced by the inlined dataset when cooked -->\n\n"
    '<script src="history.js"></script>\n\n</body>\n</html>\n'
)


class TestPackVisualisation(unittest.TestCase):
    def setUp(self):
        self.packer = load_script("pack-visualisation.py")

    def test_pack_replaces_anchor_with_data_payload(self):
        script = self.packer.data_script(_dataset(), "history.json")
        out = self.packer.pack(SHELL, script)
        self.assertIn("window.HISTORY_DATA = {", out)
        self.assertIn('"version":"1.0.0"', out)
        self.assertNotIn('src="history.js"', out)
        self.assertNotIn("dataset placeholder", out)

    def test_pack_escapes_closing_tags_inside_payload(self):
        data = _dataset()
        data["project"]["description"] = "ends a </script> literal"
        script = self.packer.data_script(data, "history.json")
        payload = script.split("window.HISTORY_DATA = ", 1)[1].rsplit(";", 1)[0]
        self.assertNotIn("</script>", payload)
        self.assertIn(r"<\/script>", payload)
        self.assertTrue(script.rstrip().endswith("</script>"))

    def test_pack_refuses_shell_without_anchor(self):
        with self.assertRaises(SystemExit):
            self.packer.pack("<html><body>no anchor</body></html>", "<script>x</script>")

    def test_view_overrides_stamp_into_embedded_copy(self):
        data = _dataset(view={"layout": "square", "theme": "dark", "palette": "blue"})
        out = self.packer.apply_view(data, _args(layout="islands", palette="green"))
        self.assertEqual(out["view"], {"layout": "islands", "theme": "dark", "palette": "green"})

    def test_view_defaults_left_alone_without_overrides(self):
        data = _dataset()
        out = self.packer.apply_view(data, _args())
        self.assertNotIn("view", out)

    def test_read_dataset_rejects_non_dataset(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text('{"not": "a dataset"}', encoding="utf-8")
            with self.assertRaises(SystemExit):
                self.packer.read_dataset(bad)

    def test_output_name_derives_from_dataset(self):
        self.assertEqual(self.packer.output_name(_dataset()), "example-service-1.1.0.html")

    def test_cli_packs_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shell = root / "shell.html"
            shell.write_text(SHELL, encoding="utf-8")
            history = root / "history.json"
            history.write_text(json.dumps(_dataset()), encoding="utf-8")
            out = root / "out.html"
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "pack-visualisation.py"),
                 "--history", str(history), "--shell", str(shell),
                 "--out", str(out), "--layout", "metro"],
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            packed = out.read_text(encoding="utf-8")
            self.assertIn('"layout":"metro"', packed)
            self.assertIn("window.HISTORY_DATA", packed)

    def test_cli_check_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            history = root / "history.json"
            history.write_text(json.dumps(_dataset()), encoding="utf-8")
            out = root / "out.html"
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "pack-visualisation.py"),
                 "--history", str(history), "--out", str(out), "--check"],
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("shell anchor present", result.stdout)
            self.assertFalse(out.exists())

    def test_cli_shim_emits_js_twin(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shell = root / "shell.html"
            shell.write_text(SHELL, encoding="utf-8")
            history = root / "history.json"
            history.write_text(json.dumps(_dataset()), encoding="utf-8")
            shim = root / "history.js"
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "pack-visualisation.py"),
                 "--history", str(history), "--shell", str(shell),
                 "--out", str(root / "o.html"), "--shim", str(shim)],
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            twin = shim.read_text(encoding="utf-8")
            self.assertTrue(twin.startswith("window.HISTORY_DATA = {"))
            self.assertEqual(len(twin.strip().splitlines()), 1)

    def test_registry_gate_refuses_violating_dataset(self):
        data = _dataset()
        data["versions"][0]["changelog_items"] = [{"sha": "abc"}]
        with tempfile.TemporaryDirectory() as tmp:
            history = Path(tmp) / "history.json"
            history.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                self.packer.enforce_registry_gate(history)
            self.assertIn("repair-history.py", str(ctx.exception))

    def test_registry_gate_passes_conforming_dataset(self):
        with tempfile.TemporaryDirectory() as tmp:
            history = Path(tmp) / "history.json"
            history.write_text(json.dumps(_dataset()), encoding="utf-8")
            self.packer.enforce_registry_gate(history)


if __name__ == "__main__":
    unittest.main()
