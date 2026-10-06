"""Contract tests for the report-production tools in `scripts/`."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests import SCRIPTS, load_script


class TestLinkGlossary(unittest.TestCase):
    def setUp(self):
        self.linker = load_script("link-glossary.py")

    def test_absence_is_a_field_value_label(self):
        self.assertIn("Absence", self.linker.FIELD_VALUE_LABELS)

    def test_crlf_preserved(self):
        raw = (
            b"# T\r\n\r\n## Glossary\r\n\r\n| Term | Definition |\r\n|---|---|\r\n"
            b"| CWE | Weakness taxonomy |\r\n\r\n## Notes\r\n\r\nText.\r\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "report.md"
            target.write_bytes(raw)
            self.assertEqual(self.linker.main(str(target)), 0)
            data = target.read_bytes()
            self.assertEqual(data.count(b"\n"), data.count(b"\r\n"))

    def test_body_term_gets_linked(self):
        doc = (
            "# T\n\n## Glossary\n\n| Term | Definition |\n|---|---|\n"
            "| CWE | Weakness taxonomy |\n\n## Notes\n\nThe CWE id matters.\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "report.md"
            target.write_text(doc, encoding="utf-8")
            self.linker.main(str(target))
            self.assertIn("[CWE](#glossary)", target.read_text(encoding="utf-8"))


class TestFormatTable(unittest.TestCase):
    def setUp(self):
        self.formatter = load_script("format-table.py")

    def test_requires_path_argument(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "format-table.py")],
            capture_output=True,
        )
        self.assertEqual(result.returncode, 2)

    def test_formats_misaligned_table(self):
        raw = "| a | bb |\n|--|--|\n| 1 | 22 |\n"
        out_lines, _warnings, tables = self.formatter.format_text(raw)
        self.assertEqual(tables, 1)
        widths = {len(line) for line in out_lines if line.startswith("|")}
        self.assertEqual(len(widths), 1)

    def test_crlf_preserved_via_cli(self):
        raw = b"| a | bb |\r\n|--|--|\r\n| 1 | 22 |\r\n"
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "t.md"
            target.write_bytes(raw)
            subprocess.run(
                [sys.executable, str(SCRIPTS / "format-table.py"), str(target)],
                check=True,
            )
            self.assertIn(b"\r\n", target.read_bytes())


class TestValidateReport(unittest.TestCase):
    def setUp(self):
        self.validator = load_script("validate-report.py")

    def test_finding_fields_cover_runtime_and_change(self):
        for field in ("Runtime confirmed:", "Change:", "Verified:"):
            self.assertIn(field, self.validator.FINDING_REQUIRED)

    def test_par_bound_is_nineteen(self):
        rows = "".join(f"| PAR-{n} | PASS | x |\n" for n in range(1, 20))
        self.assertEqual(self.validator.check_par_rows(rows), [])
        missing_19 = "".join(f"| PAR-{n} | PASS | x |\n" for n in range(1, 19))
        self.assertTrue(any("PAR-19" in f for f in self.validator.check_par_rows(missing_19)))

    def test_absence_tokens(self):
        self.assertIn("Deliberate - recorded decision", self.validator.ABSENCE_VALUES)
        self.assertIn("Undetermined", self.validator.ABSENCE_VALUES)

    def test_status_vocabularies(self):
        self.assertIn("Closed", self.validator.FINDING_STATUS)
        self.assertIn("Reopened", self.validator.CHANGE_VALUES)
        self.assertIn("Accepted", self.validator.RISK_STATUS)


class TestNewReport(unittest.TestCase):
    def setUp(self):
        self.generator = load_script("new-report.py")

    def test_par_rows_cover_nineteen(self):
        self.assertEqual(len(self.generator.PAR_ROWS), 19)
        self.assertIn("PAR-19", self.generator.PAR_ROWS[-1])


if __name__ == "__main__":
    unittest.main()
