"""Contract tests for the dataset extractor in `scripts/extract-visualisation.py`."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests import SCRIPTS, load_script


def _dataset() -> dict:
    return {
        "schema": 2,
        "project": {"name": "example-service"},
        "categories": [{"id": "fix", "label": "Fixes", "color": "#e64980", "order": 30}],
        "versions": [
            {"version": "1.0.0", "kind": "release", "events": []},
            {"version": "1.1.0", "kind": "developing", "events": []},
        ],
    }


def _packed(data: dict) -> str:
    """Minimal packed artifact shaped like pack-visualisation.py output."""
    payload = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
    return (
        "<html>\n<head></head>\n<body>\n<script>app()</script>\n"
        "<script>\n\n/* embedded dataset - twin of history.json */\n\n"
        "window.HISTORY_DATA = " + payload + ";\n\n</script>\n</body>\n</html>\n"
    )


class TestExtractVisualisation(unittest.TestCase):
    def setUp(self):
        self.extractor = load_script("extract-visualisation.py")

    def test_find_payload_recovers_dataset_json(self):
        data = _dataset()
        payload = self.extractor.find_payload(_packed(data))
        self.assertEqual(json.loads(payload), data)

    def test_find_payload_roundtrips_escaped_closing_tags(self):
        data = _dataset()
        data["project"]["description"] = "ends a </script> literal"
        payload = self.extractor.find_payload(_packed(data))
        self.assertEqual(json.loads(payload), data)

    def test_find_payload_skips_loader_mentions(self):
        html = ("<script>if (window.HISTORY_DATA) { go(); }</script>\n"
                + _packed(_dataset()).split("<body>\n", 1)[1])
        payload = self.extractor.find_payload(html)
        self.assertEqual(json.loads(payload)["project"]["name"], "example-service")

    def test_find_payload_refuses_file_without_dataset(self):
        with self.assertRaises(SystemExit):
            self.extractor.find_payload("<html><body>no data</body></html>")

    def test_read_dataset_rejects_non_dataset(self):
        with self.assertRaises(SystemExit):
            self.extractor.read_dataset('{"not": "a dataset"}', Path("x.html"))

    def test_read_dataset_rejects_broken_json(self):
        with self.assertRaises(SystemExit):
            self.extractor.read_dataset("{broken", Path("x.html"))

    def test_cli_extracts_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            packed = root / "city.html"
            packed.write_text(_packed(_dataset()), encoding="utf-8")
            out = root / "data" / "history.json"
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "extract-visualisation.py"),
                 "--html", str(packed), "--out", str(out)],
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(out.read_text(encoding="utf-8")), _dataset())

    def test_cli_check_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            packed = root / "city.html"
            packed.write_text(_packed(_dataset()), encoding="utf-8")
            out = root / "history.json"
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "extract-visualisation.py"),
                 "--html", str(packed), "--out", str(out), "--check"],
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("embedded dataset found", result.stdout)
            self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()
