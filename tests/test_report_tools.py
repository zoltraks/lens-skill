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


class TestLinkReferences(unittest.TestCase):
    DOC = (
        "# T\n\n"
        "## Verification And Evidence Ledger\n\n"
        "| Evidence | Check | Result |\n|---|---|---|\n"
        "| EVD-001 | git | sha |\n\n"
        "## Detailed Technical Findings\n\n"
        "### FND-SEC-001: Bad thing\n\n"
        "* **Evidence:** EVD-001 - inspected\n\n"
        "## Handoff\n\n"
        "| Claim | Resolves |\n|---|---|\n"
        "| tests pass | EVD-001, FND-SEC-001 |\n"
    )

    def setUp(self):
        self.linker = load_script("link-references.py")

    def write(self, tmp, doc):
        target = Path(tmp) / "report.md"
        target.write_text(doc, encoding="utf-8")
        self.linker.main(str(target))
        return target.read_text(encoding="utf-8")

    def test_references_link_to_definitions(self):
        with tempfile.TemporaryDirectory() as tmp:
            text = self.write(tmp, self.DOC)
            self.assertIn("[EVD-001](#verification-and-evidence-ledger)", text)
            self.assertIn("[FND-SEC-001](#fnd-sec-001-bad-thing)", text)

    def test_defining_sites_stay_plain(self):
        with tempfile.TemporaryDirectory() as tmp:
            text = self.write(tmp, self.DOC)
            self.assertIn("| EVD-001 | git | sha |", text)
            self.assertIn("### FND-SEC-001: Bad thing", text)

    def test_inline_code_and_links_untouched(self):
        doc = self.DOC + "\n`EVD-001` stays code and [FND-SEC-001](#x) stays.\n"
        with tempfile.TemporaryDirectory() as tmp:
            text = self.write(tmp, doc)
            self.assertIn("`EVD-001` stays code", text)
            self.assertIn("[FND-SEC-001](#x) stays", text)

    def test_unicode_heading_slug_keeps_diacritics(self):
        doc = "# T\n\n## Rejestr dowodów audytowych\n\n| Dowód | Wynik |\n|---|---|\n| EVD-001 | ok |\n\nCites EVD-001.\n"
        with tempfile.TemporaryDirectory() as tmp:
            text = self.write(tmp, doc)
            self.assertIn("[EVD-001](#rejestr-dowodów-audytowych)", text)

    def test_qualified_reference_resolves_project_block(self):
        doc = (
            "# T\n\n## api-service\n\n### FND-SEC-001: Bad (api-service)\n\n"
            "Block.\n\n## web-app\n\n### FND-SEC-001: Bad (web-app)\n\n"
            "Cites api-service::FND-SEC-001.\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            text = self.write(tmp, doc)
            self.assertIn(
                "[api-service::FND-SEC-001](#fnd-sec-001-bad-api-service)", text
            )

    def test_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "report.md"
            target.write_text(self.DOC, encoding="utf-8")
            self.linker.main(str(target))
            once = target.read_text(encoding="utf-8")
            self.linker.main(str(target))
            self.assertEqual(once, target.read_text(encoding="utf-8"))


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

    def test_link_cells_measure_source_width(self):
        raw = "| a | bb |\n|--|--|\n| [x](#anchor-here) | 22 |\n"
        out_lines, _warnings, tables = self.formatter.format_text(raw)
        self.assertEqual(tables, 1)
        self.assertEqual(out_lines[1], "|-------------------|----|")
        self.assertEqual(out_lines[2], "| [x](#anchor-here) | 22 |")

    def test_link_markup_inside_code_span_counts_verbatim(self):
        raw = "| a | bb |\n|--|--|\n| `[x](#y)` | 22 |\n"
        out_lines, _warnings, tables = self.formatter.format_text(raw)
        self.assertEqual(tables, 1)
        self.assertEqual(out_lines[1], "|-----------|----|")

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

    def test_par_bound_is_twenty(self):
        rows = "".join(f"| PAR-{n} | PASS | x |\n" for n in range(1, 21))
        self.assertEqual(self.validator.check_par_rows(rows), [])
        missing_20 = "".join(f"| PAR-{n} | PASS | x |\n" for n in range(1, 20))
        self.assertTrue(any("PAR-20" in f for f in self.validator.check_par_rows(missing_20)))

    def test_absence_tokens(self):
        self.assertIn("Deliberate - recorded decision", self.validator.ABSENCE_VALUES)
        self.assertIn("Undetermined", self.validator.ABSENCE_VALUES)

    def test_status_vocabularies(self):
        self.assertIn("Closed", self.validator.FINDING_STATUS)
        self.assertIn("Reopened", self.validator.CHANGE_VALUES)
        self.assertIn("Accepted", self.validator.RISK_STATUS)

    def test_register_reference_links(self):
        lines = [
            "## Verification And Evidence Ledger",
            "",
            "| Evidence | Result |",
            "|----------|--------|",
            "| EVD-001  | sha    |",
            "",
            "### FND-SEC-001: Bad thing",
            "",
            "## Handoff",
            "",
            "| Claim | Resolves |",
            "|-------|----------|",
            "| tests | EVD-001, FND-SEC-001 |",
        ]
        fences = self.validator.split_code(lines)
        text = "\n".join(lines)
        failures = self.validator.check_reference_links(lines, fences, text)
        self.assertTrue(
            any("unlinked register reference EVD-001" in f for f in failures)
        )
        self.assertTrue(
            any("unlinked register reference FND-SEC-001" in f for f in failures)
        )

        linked = [
            line.replace("EVD-001", "[EVD-001](#verification-and-evidence-ledger)")
            .replace("FND-SEC-001", "[FND-SEC-001](#fnd-sec-001-bad-thing)")
            if line.startswith("| tests") else line
            for line in lines
        ]
        failures = self.validator.check_reference_links(
            linked, self.validator.split_code(linked), "\n".join(linked)
        )
        self.assertEqual(failures, [])

    def test_table_pipes_aligned_on_source_width(self):
        lines = [
            "| Claim | Resolves           |",
            "|-------|--------------------|",
            "| tests | [EVD-001](#ledger) |",
        ]
        failures = self.validator.check_tables(lines, [False] * len(lines))
        self.assertEqual(failures, [])

    def test_aip_provenance_basis(self):
        block = ["### FND-AIP-001 x", "", "* **Provenance basis:** Declared - trailers"]
        self.assertEqual(self.validator.check_aip_provenance(block), [])
        missing = ["### FND-AIP-001 x", "", "* **Severity:** LOW"]
        self.assertTrue(
            any("Provenance basis" in f for f in self.validator.check_aip_provenance(missing))
        )
        stray = ["### FND-SEC-001 x", "", "* **Provenance basis:** Declared"]
        self.assertTrue(
            any("reserved" in f for f in self.validator.check_aip_provenance(stray))
        )
        bad_value = ["### FND-AIP-001 x", "", "* **Provenance basis:** Human-authored"]
        self.assertTrue(
            any("not one of" in f for f in self.validator.check_aip_provenance(bad_value))
        )


class TestNewReport(unittest.TestCase):
    def setUp(self):
        self.generator = load_script("new-report.py")

    def test_par_rows_cover_twenty(self):
        self.assertEqual(len(self.generator.PAR_ROWS), 20)
        self.assertIn("PAR-20", self.generator.PAR_ROWS[-1])


RULES = SCRIPTS.parent / "translations" / "polish-language.md"


class TestLintPolish(unittest.TestCase):
    def setUp(self):
        self.lint = load_script("lint-polish.py")

    def test_allowed_idioms_masked(self):
        pairs = [("pod", "under")]
        allowed = self.lint.load_allowed([RULES])
        findings = []
        masked = self.lint.mask_allowed(
            "System jest pod względem wydajności gotowy.", allowed
        )
        self.lint.check_forbidden(1, masked, pairs, findings)
        self.assertEqual(findings, [])

    def test_canonical_names_masked(self):
        pairs = [("server", "serwer")]
        allowed = self.lint.load_allowed([RULES])
        findings = []
        masked = self.lint.mask_allowed(
            "Atak Server-Side Request Forgery omija filtr.", allowed
        )
        self.lint.check_forbidden(1, masked, pairs, findings)
        self.assertEqual(findings, [])

    def test_chudy_inflections_flagged(self):
        pairs = self.lint.load_forbidden([RULES])
        findings = []
        self.lint.check_forbidden(
            1, "chuda treść, chude pliki i chudymi powierzchniami.",
            pairs, findings,
        )
        self.assertEqual(len(findings), 3)
        self.assertTrue(all(f[0] == "warn" for f in findings))

    def test_enumeration_series_suppressed(self):
        findings = []
        self.lint.check_mechanical(
            1, "Zakres obejmuje budowania, testów, lintu i publikacji.",
            findings,
        )
        self.assertFalse(any("spliced" in f[2] for f in findings))

    def test_genuine_splice_flagged(self):
        findings = []
        self.lint.check_mechanical(
            1, "Ważność jest wysoka, kod łamie kontrakt.", findings
        )
        self.assertTrue(any("spliced" in f[2] for f in findings))

    def test_zero_rules_hint(self):
        import contextlib
        import io

        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "r.md"
            report.write_text("Tekst bez reguł.\n", encoding="utf-8")
            argv = sys.argv
            err = io.StringIO()
            try:
                sys.argv = [
                    "lint-polish.py",
                    str(report),
                    "--rules",
                    str(Path(tmp) / "missing.md"),
                ]
                with contextlib.redirect_stderr(err):
                    self.lint.main()
            finally:
                sys.argv = argv
        self.assertIn("no forbidden forms loaded", err.getvalue())


class TestMapReportTranslation(unittest.TestCase):
    RULES_DOC = (
        "## Document Information\n\n"
        "| English | Polish |\n|---|---|\n"
        "| Language | Język |\n"
        "| English | Angielski |\n"
        "| Document Information | Informacje o dokumencie |\n\n"
        "## Glossary\n\n"
        "| English | Polish |\n|---|---|\n"
        "| Glossary | Słownik |\n"
        "| Verified | Zweryfikowane |\n\n"
        "## Status\n\n"
        "| English | Masculine | Feminine | Neuter |\n|---|---|---|---|\n"
        "| `COVERED` | Objęty | Objęta | Objęte |\n"
        "| `OPEN` | Otwarty | Otwarta | Otwarte |\n"
    )
    PL_DOC = (
        "# Audyt\n\n"
        "## Informacje o dokumencie\n\n"
        "| Język | Polski |\n\n"
        "## Słownik\n\n"
        "| Termin | Definicja |\n|---|---|\n"
        "| X | y |\n\n"
        "Termin [X](#słownik) w tekście.\n\n"
        "## Szczegóły\n\n"
        "| Objęty | Otwarty |\n\n"
        "* **Zweryfikowane:** tak - ok.\n\n"
        "Proza: tak i nie zostają.\n"
    )
    EN_DOC = (
        "# Audit\n\n"
        "## Document Information\n\n"
        "| Language | English |\n\n"
        "## Glossary\n\n"
        "| Term | Definition |\n|---|---|\n"
        "| X | y |\n\n"
        "## Szczegóły\n\n"
        "| Covered | Open |\n"
    )

    def setUp(self):
        self.mapper = load_script("map-translation.py")

    def test_gender_table_inverts_all_forms(self):
        with tempfile.TemporaryDirectory() as tmp:
            rules = Path(tmp) / "rules.md"
            rules.write_text(self.RULES_DOC, encoding="utf-8")
            pairs, _collisions = self.mapper.load_pairs(rules)
        self.assertEqual(pairs["Objęty"], "Covered")
        self.assertEqual(pairs["Objęta"], "Covered")
        self.assertEqual(pairs["Otwarte"], "Open")

    def test_caps_tokens_normalize_sentence_case(self):
        self.assertEqual(self.mapper.normalize_english("NOT DONE"), "Not done")
        self.assertEqual(self.mapper.normalize_english("VERIFIED"), "Verified")
        self.assertEqual(
            self.mapper.normalize_english("NOT SPECIFIED"), "NOT SPECIFIED"
        )

    def test_end_to_end_mapping(self):
        import contextlib
        import io

        with tempfile.TemporaryDirectory() as tmp:
            pl = Path(tmp) / "r-pl.md"
            en = Path(tmp) / "r-en.md"
            rules = Path(tmp) / "rules.md"
            pl.write_text(self.PL_DOC, encoding="utf-8")
            en.write_text(self.EN_DOC, encoding="utf-8")
            rules.write_text(self.RULES_DOC, encoding="utf-8")
            argv = sys.argv
            out = io.StringIO()
            try:
                sys.argv = [
                    "map-translation.py",
                    str(pl),
                    "--rules",
                    str(rules),
                    "--en",
                    str(en),
                ]
                with contextlib.redirect_stdout(out):
                    rc = self.mapper.main()
            finally:
                sys.argv = argv
            mapped = pl.with_name("r-pl-en-mapped.tmp.md").read_text(
                encoding="utf-8"
            )
        self.assertEqual(rc, 0)
        self.assertIn("english sibling check: PASS", out.getvalue())
        self.assertIn("| Language | English", mapped)
        self.assertIn("* **Verified:** yes", mapped)
        self.assertIn("[X](#glossary)", mapped)
        self.assertIn("tak i nie zostają", mapped)


class TestCheckPlReport(unittest.TestCase):
    DOC = (
        "# Audyt\n\n"
        "## Szczegółowe ustalenia techniczne\n\n"
        "| Ustalenie | Tytuł |\n|---|---|\n"
        "| [FND-001](#fnd-001-pierwsze-ustalenie) | Pierwsze ustalenie |\n\n"
        "### FND-001: Pierwsze ustalenie\n\n"
        "Rejestr liczy 1 ustalenie.\n"
    )

    def setUp(self):
        self.checker = load_script("check-translation.py")

    def run_checker(self, doc):
        import contextlib
        import io

        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "r.md"
            target.write_text(doc, encoding="utf-8")
            argv = sys.argv
            out = io.StringIO()
            try:
                sys.argv = ["check-translation.py", str(target)]
                with contextlib.redirect_stdout(out):
                    rc = self.checker.main()
            finally:
                sys.argv = argv
        return rc, out.getvalue()

    def test_clean_report_passes(self):
        rc, out = self.run_checker(self.DOC)
        self.assertEqual(rc, 0, out)

    def test_title_mismatch_fails(self):
        doc = self.DOC.replace(
            "| Pierwsze ustalenie |", "| Inny tytuł |"
        )
        rc, out = self.run_checker(doc)
        self.assertEqual(rc, 1)
        self.assertIn("FND-001", out)

    def test_prose_count_mismatch_fails(self):
        doc = self.DOC.replace("1 ustalenie", "5 ustaleń")
        rc, out = self.run_checker(doc)
        self.assertEqual(rc, 1)
        self.assertIn("claims 5 FND", out)

    def test_long_sentence_warns_not_fails(self):
        doc = self.DOC + "\n" + " ".join(["słowo"] * 45) + ".\n"
        rc, out = self.run_checker(doc)
        self.assertEqual(rc, 0)
        self.assertIn("WARN", out)


class TestLinkGlossaryPolish(unittest.TestCase):
    def setUp(self):
        self.linker = load_script("link-glossary.py")

    def write(self, tmp, doc):
        target = Path(tmp) / "report.md"
        target.write_text(doc, encoding="utf-8")
        return target

    def test_polish_glossary_linked(self):
        doc = (
            "# T\n\n## Słownik\n\n| Termin | Definicja |\n|---|---|\n"
            "| API | interfejs |\n\n## Treść\n\nKażde wywołanie API działa.\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            target = self.write(tmp, doc)
            self.assertEqual(self.linker.main(str(target), "pl"), 0)
            self.assertIn(
                "[API](#słownik)", target.read_text(encoding="utf-8")
            )

    def test_compound_diacritics_not_linked(self):
        doc = (
            "# T\n\n## Słownik\n\n| Termin | Definicja |\n|---|---|\n"
            "| API | interfejs |\n\n## Treść\n\nZgodność API działa.\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            target = self.write(tmp, doc)
            self.linker.main(str(target), "pl")
            self.assertIn(
                "Zgodność API działa.", target.read_text(encoding="utf-8")
            )

    def test_check_mode_reports_unlinked(self):
        doc = (
            "# T\n\n## Słownik\n\n| Termin | Definicja |\n|---|---|\n"
            "| API | interfejs |\n\n## Treść\n\nKażde wywołanie API działa.\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            target = self.write(tmp, doc)
            self.assertEqual(self.linker.main(str(target), "pl", check=True), 1)
            self.linker.main(str(target), "pl")
            self.assertEqual(self.linker.main(str(target), "pl", check=True), 0)


class TestValidateReportLanguage(unittest.TestCase):
    def setUp(self):
        self.validator = load_script("validate-report.py")

    def test_polish_report_exits_2_with_guidance(self):
        import contextlib
        import io

        doc = (
            "# Audyt\n\n## Informacje o dokumencie\n\n"
            "| Język | Polski |\n\n## Słownik\n\nx\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "report.md"
            target.write_text(doc, encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                rc = self.validator.main(str(target))
        self.assertEqual(rc, 2)
        self.assertIn("translated-report gates", out.getvalue())

    def test_english_row_proceeds(self):
        doc = "| Language | English |\n"
        self.assertIsNone(self.validator.non_english_language(doc))

    def test_stray_language_row_ignored(self):
        doc = (
            "# T\n\n## Document Information\n\n| Language | English |\n\n"
            "## Other\n\n| Language | Klingon |\n"
        )
        self.assertIsNone(self.validator.non_english_language(doc))

    def test_no_language_row_proceeds(self):
        self.assertIsNone(self.validator.non_english_language("# T\n\nx\n"))


if __name__ == "__main__":
    unittest.main()
