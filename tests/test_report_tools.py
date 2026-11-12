"""Contract tests for the report-production tools in `scripts/`."""

from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
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
            b"# T\r\n\r\n## Glossary Index\r\n\r\n| Term | Definition |\r\n|---|---|\r\n"
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
            "# T\n\n## Glossary Index\n\n| Term | Definition |\n|---|---|\n"
            "| CWE | Weakness taxonomy |\n\n## Notes\n\nThe CWE id matters.\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "report.md"
            target.write_text(doc, encoding="utf-8")
            self.linker.main(str(target))
            self.assertIn("[CWE](#glossary-index)", target.read_text(encoding="utf-8"))


class TestLinkReferences(unittest.TestCase):
    DOC = (
        "# T\n\n"
        "## Evidence List\n\n"
        "| Evidence | Check | Result |\n|---|---|---|\n"
        "| EVD-001 | git | sha |\n\n"
        "## Technical Findings\n\n"
        "### FND-SEC-001 Bad thing\n\n"
        "- **Evidence:** EVD-001 - inspected\n\n"
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
            self.assertIn("[EVD-001](#evidence-list)", text)
            self.assertIn("[FND-SEC-001](#fnd-sec-001-bad-thing)", text)

    def test_defining_sites_stay_plain(self):
        with tempfile.TemporaryDirectory() as tmp:
            text = self.write(tmp, self.DOC)
            self.assertIn("| EVD-001 | git | sha |", text)
            self.assertIn("### FND-SEC-001 Bad thing", text)

    def test_inline_code_and_links_untouched(self):
        doc = self.DOC + "\n`EVD-001` stays code and [FND-SEC-001](#x) is repaired.\n"
        with tempfile.TemporaryDirectory() as tmp:
            text = self.write(tmp, doc)
            self.assertIn("`EVD-001` stays code", text)
            self.assertIn("[FND-SEC-001](#fnd-sec-001-bad-thing) is repaired", text)
            self.assertNotIn("(#x)", text)

    def test_unicode_heading_slug_keeps_diacritics(self):
        doc = "# T\n\n## Lista dowodów\n\n| Dowód | Wynik |\n|---|---|\n| EVD-001 | ok |\n\nCites EVD-001.\n"
        with tempfile.TemporaryDirectory() as tmp:
            text = self.write(tmp, doc)
            self.assertIn("[EVD-001](#lista-dowodów)", text)

    def test_qualified_reference_resolves_project_block(self):
        doc = (
            "# T\n\n## api-service\n\n### FND-SEC-001 Bad (api-service)\n\n"
            "Block.\n\n## web-app\n\n### FND-SEC-001 Bad (web-app)\n\n"
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

    def test_pipe_inside_code_span_is_not_a_cell_boundary(self):
        raw = "| a | bb |\n|--|--|\n| `x | y` | 22 |\n"
        out_lines, _warnings, tables = self.formatter.format_text(raw)
        self.assertEqual(tables, 1)
        self.assertEqual(out_lines[2], "| `x | y` | 22 |")

    def test_pipe_inside_double_backtick_span_is_not_a_cell_boundary(self):
        raw = "| a | bb |\n|--|--|\n| ``x `|` y`` | 22 |\n"
        out_lines, _warnings, tables = self.formatter.format_text(raw)
        self.assertEqual(tables, 1)
        self.assertEqual(out_lines[2], "| ``x `|` y`` | 22 |")

    def test_width_budget_warning(self):
        raw = "| a | bb |\n|--|--|\n| " + "x" * 305 + " | 22 |\n"
        _out, warnings, _tables = self.formatter.format_text(raw)
        self.assertTrue(any("300-character" in w for w in warnings))

    def test_width_budget_quiet_under_limit(self):
        raw = "| a | bb |\n|--|--|\n| 1 | 22 |\n"
        _out, warnings, _tables = self.formatter.format_text(raw)
        self.assertFalse(any("300-character" in w for w in warnings))

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
        for field in ("Criteria:",):
            self.assertIn(field, self.validator.FINDING_REQUIRED)
        for field in ("Confirmation:", "Verification:", "Status:", "Change:"):
            self.assertNotIn(field, self.validator.FINDING_REQUIRED)

    def test_criteria_references(self):
        lines = [
            "**Criteria table**",
            "",
            "| Criteria | Family   | Applicability | Criticality | Method   | Sufficiency |",
            "|-----------|----------|---------------|-------------|----------|-------------|",
            "| SEC-AUTHZ | SEC      | applicable    | high        | inspect  | rule        |",
            "",
            "### FND-SEC-001 Bad thing",
            "",
            "- **Criteria:** SEC-INPUT - missing authz check",
        ]
        failures = self.validator.check_criteria_references(lines, "audit")
        self.assertTrue(any("SEC-INPUT" in f for f in failures))

        resolved = lines[:]
        resolved[-1] = "- **Criteria:** SEC-AUTHZ - missing authz check"
        self.assertEqual(self.validator.check_criteria_references(resolved, "audit"), [])

    def test_criteria_table_rejects_legacy_heading_long_prefix_and_unneeded_01(self):
        legacy = [
            "**Criterias table**",
            "",
            "| Criteria | Family | Applicability | Criticality | Method | Sufficiency |",
            "|-----------|--------|---------------|-------------|--------|-------------|",
            "| SEC-AUTHZ | SEC    | applicable    | high        | inspect| rule        |",
        ]
        self.assertTrue(
            any("use '**Criteria table**'" in f for f in self.validator.check_criteria_references(legacy, "audit"))
        )
        bad_ids = [
            "**Criteria table**",
            "",
            "| Criteria     | Family | Applicability | Criticality | Method  | Sufficiency |",
            "|---------------|--------|---------------|-------------|---------|-------------|",
            "| TEST-UNIT     | test   | applicable    | high        | inspect | rule        |",
            "| TST-PIPE-01   | test   | applicable    | high        | inspect | rule        |",
            "| SEC-AUTH-01   | sec    | applicable    | high        | inspect | rule        |",
            "| SEC-AUTH-02   | sec    | applicable    | high        | inspect | rule        |",
        ]
        joined = "\n".join(self.validator.check_criteria_references(bad_ids, "audit"))
        self.assertIn("'TEST-UNIT' must use a three-letter uppercase prefix", joined)
        self.assertIn("'TST-PIPE-01' has an unnecessary '-01' suffix", joined)
        self.assertNotIn("SEC-AUTH-01", joined)

    def test_criteria_table_required_for_audit_style(self):
        lines = [
            "### FND-SEC-001 Bad thing",
            "",
            "- **Criteria:** SEC-AUTHZ - missing authz check",
        ]
        failures = self.validator.check_criteria_references(lines, "audit")
        self.assertTrue(any("no Criteria table" in f for f in failures))
        self.assertEqual(self.validator.check_criteria_references(lines, "hunt"), [])

    def test_par_bound_is_thirty_three(self):
        rows = "## Validation Protocol\n\n" + "".join(f"| PAR-{n} | Pass | x |\n" for n in range(1, 34))
        self.assertEqual(self.validator.check_par_rows(rows), [])
        missing_30 = "## Validation Protocol\n\n" + "".join(f"| PAR-{n} | Pass | x |\n" for n in range(1, 33))
        self.assertTrue(any("PAR-33" in f for f in self.validator.check_par_rows(missing_30)))

    def test_par_result_cells_render_check_vocabulary(self):
        rows = "## Validation Protocol\n\n" + "".join(f"| PAR-{n} | Pass | x |\n" for n in range(1, 34))
        bad = rows.replace("| PAR-3 | Pass |", "| PAR-3 | PASS |").replace(
            "| PAR-9 | Pass |", "| PAR-9 | Skipped |"
        )
        joined = "\n".join(self.validator.check_par_rows(bad))
        self.assertIn("non-check result 'PASS'", joined)
        self.assertIn("non-check result 'Skipped'", joined)

    def test_absence_tokens(self):
        self.assertIn("Deliberate - recorded decision", self.validator.ABSENCE_VALUES)
        self.assertIn("Undetermined", self.validator.ABSENCE_VALUES)

    def test_status_vocabularies(self):
        self.assertIn("Closed", self.validator.FINDING_STATUS)
        self.assertIn("Pass", self.validator.FINDING_STATUS)
        self.assertIn("Reopened", self.validator.CHANGE_VALUES)
        self.assertIn("Accepted", self.validator.RISK_STATUS)
        self.assertIn("Fail", self.validator.CONFORMANCE_STATUS_TOKENS)
        self.assertIn("Passed", self.validator.CONFORMANCE_VERDICT_TOKENS)
        self.assertIn("Not run", self.validator.REVIEW_RESULTS)

    def test_coverage_rows_render_title_case(self):
        text = (
            "## Audit Coverage\n\n"
            "| Report type                   | Status   | Rationale |\n"
            "|-------------------------------|----------|-----------|\n"
            "| Software Architecture Review  | Covered  | x         |\n"
            "| Penetration Test              | Not done | Separate  |\n"
            "| Performance Audit             | Partially| no load   |\n"
        )
        self.assertEqual(self.validator.check_coverage_rows(text), [])
        for bad in ("Done", "COVERED", "N/A", "Not Done"):
            mutated = text.replace("| Covered  |", f"| {bad:<8} |")
            failures = self.validator.check_coverage_rows(mutated)
            self.assertTrue(failures, f"{bad!r} should fail")

    def test_register_reference_links(self):
        lines = [
            "## Evidence List",
            "",
            "| Evidence | Result |",
            "|----------|--------|",
            "| EVD-001  | sha    |",
            "",
            "### FND-SEC-001 Bad thing",
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
            line.replace("EVD-001", "[EVD-001](#evidence-list)")
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

    def test_table_blank_line_separation(self):
        above = [
            "A sentence.",
            "| Claim | Resolves           |",
            "|-------|--------------------|",
            "| tests | [EVD-001](#ledger) |",
            "",
        ]
        failures = self.validator.check_tables(above, [False] * len(above))
        self.assertTrue(any("not preceded by a blank line" in f for f in failures))
        below = [
            "| Claim | Resolves           |",
            "|-------|--------------------|",
            "| tests | [EVD-001](#ledger) |",
            "**Label**",
        ]
        failures = self.validator.check_tables(below, [False] * len(below))
        self.assertTrue(any("not followed by a blank line" in f for f in failures))
        clean = ["", "| a |", "|---|", "", "text."]
        self.assertEqual(
            self.validator.check_tables(clean, [False] * len(clean)), []
        )

    def test_duplicate_separator_flagged(self):
        lines = [
            "",
            "| A | B |",
            "|---|---|",
            "|---|---|",
            "| x | y |",
            "",
        ]
        failures = self.validator.check_tables(lines, [False] * len(lines))
        self.assertTrue(any("duplicate separator" in f for f in failures))

    def test_placeholder_column_flagged(self):
        lines = [
            "",
            "| A | B |",
            "|---|---|",
            "| x | - |",
            "| y | - |",
            "",
        ]
        failures = self.validator.check_tables(lines, [False] * len(lines))
        self.assertTrue(any("no value in any row" in f for f in failures))

    def test_bold_markers_balanced(self):
        bad = ["- **Done when:*- ** The thing holds."]
        self.assertTrue(
            self.validator.check_bold_markers(bad, [False])
        )
        good = ["- **Done when:** The thing holds.", "**Run heading**"]
        self.assertEqual(self.validator.check_bold_markers(good, [False] * 2), [])
        code = ["`` `**` stays inside code ``"]
        self.assertEqual(self.validator.check_bold_markers(code, [False]), [])

    def test_aip_provenance_basis(self):
        block = ["### FND-AIP-001 x", "", "- **Provenance:** Declared, trailers"]
        self.assertEqual(self.validator.check_aip_provenance(block), [])
        missing = ["### FND-AIP-001 x", "", "- **Severity:** Low"]
        self.assertTrue(
            any("Provenance" in f for f in self.validator.check_aip_provenance(missing))
        )
        stray = ["### FND-SEC-001 x", "", "- **Provenance:** Declared"]
        self.assertTrue(
            any("reserved" in f for f in self.validator.check_aip_provenance(stray))
        )
        bad_value = ["### FND-AIP-001 x", "", "- **Provenance:** Human-authored"]
        self.assertTrue(
            any("not one of" in f for f in self.validator.check_aip_provenance(bad_value))
        )

    def test_references_section(self):
        block = (
            "## Reference Sources\n\n"
            "| Reference | Publisher or Author | Used In |\n"
            "|-----------|---------------------|---------|\n"
            "| OWASP ASVS 5.0 | OWASP | Auditing Methodology |\n"
        )
        self.assertEqual(self.validator.check_references_section(block), [])

        bare = "## Reference Sources\n\nNothing cited here.\n"
        failures = self.validator.check_references_section(bare)
        self.assertTrue(any("no source entry" in f for f in failures))

        linked = block + "\n[OWASP ASVS](https://owasp.org/)\n"
        self.assertEqual(self.validator.check_references_section(linked), [])

        internal = linked.replace(
            "| OWASP ASVS 5.0 | OWASP |", "| `docs/GUIDELINES.md` | maintainer |"
        )
        self.assertTrue(
            any("repository path" in f for f in self.validator.check_references_section(internal))
        )

        empty = "## Reference Sources\n\nNo external sources consulted.\n"
        self.assertEqual(self.validator.check_references_section(empty), [])

        trailing = linked + "\n## Appendix\n"
        self.assertTrue(
            any("final section" in f for f in self.validator.check_references_section(trailing))
        )

    def test_paragraph_sentence_boundary(self):
        lines = ["First sentence.", "Second sentence.", "", "Only one."]
        fences = self.validator.split_code(lines)
        failures = self.validator.check_sentence_breaks(lines, fences, True)
        self.assertFalse(any("boundary inside a paragraph" in f for f in failures))
        joined = ["Alpha ends here. Beta starts next."]
        failures = self.validator.check_sentence_breaks(
            joined, self.validator.split_code(joined), True
        )
        self.assertFalse(any("own paragraph" in f for f in failures))

    def test_midline_sentence_join(self):
        short = ["Alpha ends here. Beta starts next."]
        fences = self.validator.split_code(short)
        self.assertEqual(
            self.validator.check_sentence_breaks(short, fences, True), []
        )
        long_join = [
            "Alpha ends here. This second sentence carries a clause list of "
            "twenty one plain words that push the sentence past the limit set "
            "for shared paragraph lines and it keeps going still."
        ]
        failures = self.validator.check_sentence_breaks(
            long_join, self.validator.split_code(long_join), True
        )
        self.assertTrue(any("own paragraph" in f for f in failures))
        exempt = ["See e.g. Foo for details.", "", "Name J. Smith wrote it."]
        self.assertEqual(
            self.validator.check_sentence_breaks(
                exempt, self.validator.split_code(exempt), True
            ),
            [],
        )

    def test_sentence_breaks_row_values(self):
        self.assertFalse(
            self.validator.sentence_breaks_on("| Sentence breaks | Off |\n")
        )
        self.assertTrue(
            self.validator.sentence_breaks_on("| Detail Level | Detailed |\n")
        )
        self.assertEqual(
            self.validator.check_sentence_breaks_row("| Sentence breaks | Off |\n"), []
        )
        self.assertTrue(
            self.validator.check_sentence_breaks_row("| Sentence breaks | On |\n")
        )

    def test_prose_line_scope(self):
        prose = self.validator.prose_line("Flush-left sentence.", False)
        self.assertTrue(prose)
        for line in (
            "* bullet item.",
            "| table | row |",
            "  indented continuation.",
            "**Bold run heading**",
            "## Heading",
        ):
            self.assertFalse(self.validator.prose_line(line, False))


class TestNewReport(unittest.TestCase):
    def setUp(self):
        self.generator = load_script("new-report.py")

    def test_par_rows_cover_thirty_three(self):
        self.assertEqual(len(self.generator.PAR_ROWS), 33)
        self.assertIn("PAR-33", self.generator.PAR_ROWS[-1])

    def test_references_scaffold(self):
        for skeleton in (
            self.generator.audit_skeleton,
            self.generator.hunt_skeleton,
            self.generator.review_skeleton,
        ):
            body = skeleton([], {})
            self.assertIn("| Reference | Publisher or Author | Used In |", body)
            self.assertIn("[<title>](<url>)", body)

    def test_model_population_validates_clean(self):
        validator = load_script("validate-report.py")
        model = {
            "scope": {"subject": "Fixture Service"},
            "scores": {
                "scale_max": 10,
                "dimensions": {
                    "functional_suitability": {"score": 9, "eligible": True},
                    "security": {"score": 8, "eligible": True},
                },
                "product": {"score": 8.5, "lowest": ["security"]},
                "process": {"score": 6.0, "scored": 3, "lowest": ["delivery_continuity"]},
                "single": {"score": 6.0, "raw": 8.5, "band": "Average",
                           "ceiling": {"reasons": ["readiness:NOT READY"]}},
            },
            "findings": [{
                "id": "FND-SEC-001", "severity": "MEDIUM", "type": "Concern",
                "criteria": "SEC-SESS", "observation": "tokens persist without atomic write",
                "consequence": "mass invalidation", "confidence": "HIGH",
                "counter": "narrow window", "evidence": ["EVD-001"],
                "next_verification": "atomic persist adopted",
            }],
            "risks": [{
                "id": "RSK-001", "finding": "FND-SEC-001", "severity": "MEDIUM",
                "impact": "all tokens die", "likelihood": "low",
                "prerequisites": "crash during write", "controls": "fresh-key fallback",
                "uncertainty": "medium",
            }],
            "recommendations": [{
                "id": "REC-001", "finding": "FND-SEC-001", "priority": "P3",
                "postcondition": "atomic persist adopted", "effort": "S",
                "verification": "fault-injection test",
            }],
            "criteria": [{
                "id": "SEC-SESS", "dimension": "security", "weight": 2,
                "criticality": "high", "outcome": "PARTIAL",
            }],
            "evidence": [{
                "id": "EVD-001", "kind": "INSPECTED", "method": "file read",
                "locator": {"path": "src/auth.rs"}, "result": "non-atomic write",
            }],
        }
        with tempfile.TemporaryDirectory() as tmp:
            model_path = Path(tmp) / "audit-model.json"
            model_path.write_text(json.dumps(model))
            target = Path(tmp) / "AUDIT-1.0.md"
            rc = self.generator.main(
                ["new-report.py", "--style", "audit",
                 "--model", str(model_path), "--output", str(target)]
            )
            self.assertEqual(rc, 0)
            self.assertEqual(validator.main(str(target)), 0)
            body = target.read_text()
            self.assertIn("### FND-SEC-001", body)
            self.assertIn("FND-SEC-001", body)
            self.assertIn("Security & Compliance", body)
            self.assertIn("### RSK-001", body)
            self.assertIn("### REC-001", body)
            self.assertIn("| Functional Suitability | 9/10", body)

    def test_skeletons_validate_clean(self):
        validator = load_script("validate-report.py")
        with tempfile.TemporaryDirectory() as tmp:
            for args, name in (
                (["--style", "audit"], "AUDIT-1.0.md"),
                (["--style", "audit", "--projects", "api,worker"], "AUDIT-2.0.md"),
                (["--style", "hunt", "--projects", "api,worker"], "HUNT-1.0.md"),
                (["--style", "review"], "REVIEW.md"),
                (["--style", "review", "--scope", "structure"], "REVIEW-1.0.md"),
            ):
                target = Path(tmp) / name
                rc = self.generator.main(["new-report.py", *args, "--output", str(target)])
                self.assertEqual(rc, 0)
                self.assertEqual(validator.main(str(target)), 0)


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
        self.assertTrue(all(f[0] == "error" for f in findings))

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
            1, "Ważność jest wysoka, jest rozstrzygana wstępnie.", findings
        )
        self.assertTrue(any("spliced" in f[2] for f in findings))

    def test_participle_continuation_not_splice(self):
        findings = []
        self.lint.check_mechanical(
            1, "Sekcja opisuje zakres, dostarczająca dowody.", findings
        )
        self.assertFalse(any("spliced" in f[2] for f in findings))

    def test_inflected_calque_flagged(self):
        pairs = [("brama", "warunek / kontrola blokująca")]
        findings = []
        self.lint.check_forbidden(
            1, "Zmiana nie przechodzi bramy przeglądu.", pairs, findings
        )
        self.assertTrue(any("calque" in f[2] for f in findings))

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
        "## Glossary Index\n\n"
        "| English | Polish |\n|---|---|\n"
        "| Glossary Index | Słownik pojęć |\n"
        "| Verification | Weryfikacja |\n\n"
        "## Status\n\n"
        "| English | Masculine | Feminine | Neuter |\n|---|---|---|---|\n"
        "| `COVERED` | Objęty | Objęta | Objęte |\n"
        "| `OPEN` | Otwarty | Otwarta | Otwarte |\n"
    )
    PL_DOC = (
        "# Audyt\n\n"
        "## Informacje o dokumencie\n\n"
        "| Język | Polski |\n\n"
        "## Słownik pojęć\n\n"
        "| Termin | Definicja |\n|---|---|\n"
        "| X | y |\n\n"
        "Termin [X](#słownik-pojęć) w tekście.\n\n"
        "## Szczegóły\n\n"
        "| Objęty | Otwarty |\n\n"
        "- **Weryfikacja:** Zaobserwowane w źródłach.\n\n"
        "Proza: tak i nie zostają.\n"
    )
    EN_DOC = (
        "# Audit\n\n"
        "## Document Information\n\n"
        "| Language | English |\n\n"
        "## Glossary Index\n\n"
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
        self.assertIn("- **Verification:**", mapped)
        self.assertIn("[X](#glossary-index)", mapped)
        self.assertIn("tak i nie zostają", mapped)


class TestCheckPlReport(unittest.TestCase):
    DOC = (
        "# Audyt\n\n"
        "## Ustalenia techniczne\n\n"
        "| Ustalenie | Tytuł |\n|---|---|\n"
        "| [FND-001](#fnd-001-pierwsze-ustalenie) | Pierwsze ustalenie |\n\n"
        "### FND-001 Pierwsze ustalenie\n\n"
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

    def test_foreign_block_label_fails(self):
        doc = self.DOC + "\n- **Skutek:** wpływ bloku.\n"
        rc, out = self.run_checker(doc)
        self.assertEqual(rc, 1)
        self.assertIn("Skutek", out)

    def test_known_block_label_passes(self):
        doc = self.DOC + "\n- **Wpływ:** Wpływ bloku.\n"
        rc, out = self.run_checker(doc)
        self.assertEqual(rc, 0, out)

    def test_unresolved_anchor_fails(self):
        doc = self.DOC + "\nOdnośnik do [brak](#nieistniejący-nagłówek).\n"
        rc, out = self.run_checker(doc)
        self.assertEqual(rc, 1)
        self.assertIn("nieistniejący", out)

    def test_resolved_anchor_passes(self):
        doc = self.DOC + "\nOdnośnik do [ustaleń](#ustalenia-techniczne).\n"
        rc, out = self.run_checker(doc)
        self.assertEqual(rc, 0, out)


class TestLinkGlossaryPolish(unittest.TestCase):
    def setUp(self):
        self.linker = load_script("link-glossary.py")

    def write(self, tmp, doc):
        target = Path(tmp) / "report.md"
        target.write_text(doc, encoding="utf-8")
        return target

    def test_polish_glossary_linked(self):
        doc = (
            "# T\n\n## Słownik pojęć\n\n| Termin | Definicja |\n|---|---|\n"
            "| API | interfejs |\n\n## Treść\n\nKażde wywołanie API działa.\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            target = self.write(tmp, doc)
            self.assertEqual(self.linker.main(str(target), "pl"), 0)
            self.assertIn(
                "[API](#słownik-pojęć)", target.read_text(encoding="utf-8")
            )

    def test_compound_diacritics_not_linked(self):
        doc = (
            "# T\n\n## Słownik pojęć\n\n| Termin | Definicja |\n|---|---|\n"
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
            "# T\n\n## Słownik pojęć\n\n| Termin | Definicja |\n|---|---|\n"
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
            "| Język | Polski |\n\n## Słownik pojęć\n\nx\n"
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


class TestScanStructure(unittest.TestCase):
    def setUp(self):
        self.scanner = load_script("scan-structure.py")

    def _tree(self, root: Path, files: list[str]):
        for rel in files:
            target = root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("x\n", encoding="utf-8")

    def test_classification_classes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._tree(
                root,
                [
                    "src/app.py",
                    "tests/test_app.py",
                    "tests/conftest.py",
                    "vendor/lib/x.py",
                    "examples/demo.py",
                    "scripts/deploy.sh",
                    "docs/guide.md",
                    "package.json",
                    "src/api.generated.py",
                    "assets/logo.png",
                    "data/blob.dat",
                    "misc/file.xyz",
                ],
            )
            result = self.scanner.scan(str(root), use_git=False)
            by_path = {e["path"]: e["class"] for e in result["inventory"]}
            self.assertEqual(by_path["src/app.py"], "production")
            self.assertEqual(by_path["tests/test_app.py"], "test")
            self.assertEqual(by_path["tests/conftest.py"], "test-support")
            self.assertEqual(by_path["vendor/lib/x.py"], "vendored")
            self.assertEqual(by_path["examples/demo.py"], "example")
            self.assertEqual(by_path["scripts/deploy.sh"], "script")
            self.assertEqual(by_path["docs/guide.md"], "doc")
            self.assertEqual(by_path["package.json"], "config")
            self.assertEqual(by_path["src/api.generated.py"], "generated")
            self.assertEqual(by_path["assets/logo.png"], "asset")
            self.assertEqual(by_path["misc/file.xyz"], "other")

    def test_noise_dirs_skipped_and_totals_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._tree(
                root,
                [
                    "src/app.py",
                    ".git/objects/ab",
                    "__pycache__/app.pyc",
                    "node_modules/pkg/i.js",
                ],
            )
            result = self.scanner.scan(str(root), use_git=False)
            self.assertEqual(result["total_files"], 1)
            self.assertEqual(result["classes"]["production"], 1)
            self.assertEqual(result["mode"], "filesystem")

    def test_module_and_json_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._tree(root, ["a/x.py", "b/y.py", "loose.py"])
            result = self.scanner.scan(str(root), use_git=False)
            self.assertIn("a", result["modules"])
            self.assertIn("b", result["modules"])
            self.assertIn(".", result["modules"])
            self.assertEqual(result["modules"]["a"]["files"], 1)
            for key in (
                "root", "mode", "classes", "modules", "extensions", "naming", "inventory"
            ):
                self.assertIn(key, result)

    def test_naming_signals_detect_casing_abbreviations_and_multi_type_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "src" / "OrderApp" / "App").mkdir(parents=True)
            (root / "src" / "OrderApp" / "Config").mkdir(parents=True)
            (root / "src" / "OrderApp" / "App" / "Misc.cs").write_text(
                "namespace OrderApp.App;\npublic class Misc {}\n",
                encoding="utf-8",
            )
            (root / "src" / "OrderApp" / "Config" / "IStore.cs").write_text(
                "namespace OrderApp.Config;\n"
                "public interface IStore {}\n"
                "public sealed class NullStore : IStore {}\n",
                encoding="utf-8",
            )
            result = self.scanner.scan(str(root), use_git=False)
            naming = result["naming"]
            self.assertIn("src/OrderApp/App", naming["abbreviated_dirs"])
            self.assertIn("src/OrderApp/Config", naming["abbreviated_dirs"])
            self.assertIn("src/OrderApp/App/Misc.cs", naming["catch_all_paths"])
            self.assertEqual(len(naming["multi_type_files"]), 1)
            self.assertEqual(
                naming["multi_type_files"][0]["types"], ["IStore", "NullStore"]
            )


class TestCheckModel(unittest.TestCase):
    def setUp(self):
        self.checker = load_script("check-model.py")
        self.catalogue = self._catalogue()

    def _cat_entry(self, cid, dimension, weight=1.0, criticality="medium",
                   na_rules=None, mechanical=False):
        return {"id": cid, "dimension": dimension, "weight": weight,
                "criticality": criticality, "natures": ["*"],
                "na_rules": na_rules or [],
                "levels": {"PASS": "...", "P75": "...", "P50": "...",
                           "P25": "...", "FAIL": "..."},
                "mechanical": mechanical}

    def _catalogue(self, criteria=None) -> dict:
        if criteria is None:
            criteria = [
                self._cat_entry("SEC-AUTHZ", "security", criticality="high"),
                self._cat_entry("SEC-INJ", "security", criticality="high"),
                self._cat_entry("SEC-CRYPTO", "security", criticality="medium"),
                self._cat_entry("CMP-API", "api_compatibility",
                                criticality="low",
                                na_rules=["deployment-model"]),
            ]
        return {
            "catalogue_version": 1, "scoring_policy": 3,
            "levels": {"PASS": 1.0, "P75": 0.75, "P50": 0.5,
                       "P25": 0.25, "FAIL": 0.0},
            "dimensions": [], "criteria": criteria, "severity_anchors": [],
        }

    def _valid_model(self) -> dict:
        return {
            "model_version": 2,
            "scope": {"subject": "demo", "revision": "abc123",
                      "purpose": "audit", "evidence_mode": "source-only",
                      "scoring_policy": 3, "catalogue_version": 1,
                      "history": "present", "detail_level": "Standard",
                      "requirements_baseline": None,
                      "projects": [{"path": ".", "provenance": "in-tree",
                                    "fetch_state": "n/a", "pin_state": "n/a",
                                    "automation_census": "signals"}],
                      "product_profile": {"natures": ["service"]}},
            "inventory": [{"path": "src/app.py", "class": "production",
                           "module": "src", "read": True,
                           "excluded_reason": None}],
            "criteria": [
                {"id": "SEC-AUTHZ", "catalogue_id": "SEC-AUTHZ",
                 "channel": "score", "source": "catalogue",
                 "applicability": "applicable", "criticality": "high",
                 "weight": 1.0, "expected": "...", "method": "...",
                 "sufficiency": "...", "dimension": "security",
                 "outcome": "PASS", "level": "PASS", "mastery": 1.0},
                {"id": "SEC-INJ", "catalogue_id": "SEC-INJ",
                 "channel": "score", "source": "catalogue",
                 "applicability": "applicable", "criticality": "high",
                 "weight": 1.0, "expected": "...", "method": "...",
                 "sufficiency": "...", "dimension": "security",
                 "outcome": "PARTIAL", "level": "P25", "mastery": 0.25},
                {"id": "SEC-CRYPTO", "catalogue_id": "SEC-CRYPTO",
                 "channel": "score", "source": "catalogue",
                 "applicability": "applicable", "criticality": "medium",
                 "weight": 1.0, "expected": "...", "method": "...",
                 "sufficiency": "...", "dimension": "security",
                 "outcome": "UNKNOWN", "level": None, "mastery": None},
                {"id": "CMP-API", "catalogue_id": "CMP-API",
                 "channel": "score", "source": "catalogue",
                 "applicability": "not applicable - deployable service, not a published library",
                 "criticality": "low",
                 "weight": 1.0, "expected": "...", "method": "...",
                 "sufficiency": "...", "dimension": "api_compatibility",
                 "outcome": "NOT_APPLICABLE", "level": None, "mastery": None,
                 "na_basis": "deployment-model"},
            ],
            "requirements": [],
            "evidence": [
                {"id": "EVD-001", "kind": "INSPECTED", "collector": "x",
                 "method": "read", "timestamp": "...", "tool": None,
                 "locator": {"path": "src/app.py", "lines": [1, 40]},
                 "procedure": None, "result": "...",
                 "claims": ["SEC-AUTHZ", "SEC-INJ"], "limits": "...",
                 "sampling": "full", "counter": "...", "redaction": "none",
                 "unavailable": None},
                {"id": "EVD-002", "kind": "INSPECTED", "collector": "x",
                 "method": "read", "timestamp": "...", "tool": None,
                 "locator": {"path": "src/db.py", "lines": [1, 20]},
                 "procedure": None, "result": "...",
                 "claims": ["SEC-INJ"], "limits": "...",
                 "sampling": "full", "counter": "...", "redaction": "none",
                 "unavailable": None},
            ],
            "findings": [
                {"id": "FND-SEC-001", "criteria": "SEC-INJ",
                 "type": "Concern", "severity": "HIGH",
                 "claim_class": "confirmed defect", "observation": "...",
                 "property": "...", "evidence": ["EVD-002"],
                 "counter": "checked alternate injection paths",
                 "consequence": "...", "scope": "...", "confidence": "HIGH",
                 "status": "Open", "next_verification": "..."},
            ],
            "risks": [
                {"id": "RSK-001", "finding": "FND-SEC-001", "impact": "...",
                 "likelihood": "...", "scope": "...", "prerequisites": "...",
                 "controls": "...", "uncertainty": "...",
                 "rule": "impact x likelihood matrix", "severity": "HIGH"},
            ],
            "recommendations": [
                {"id": "REC-001", "finding": "FND-SEC-001",
                 "postcondition": "...", "options": "...", "owner": "...",
                 "effort": "...", "verification": "...", "residual": "...",
                 "priority": "P1"},
            ],
            "readiness": {"state": "PENDING EVIDENCE",
                          "blocking": ["FND-SEC-001"]},
            "scores": {
                "scale_max": 10,
                "dimensions": {
                    "security": {"mastery": 0.625, "uncapped": 6, "score": 5,
                                 "interval": [4, 5], "coverage": 0.67,
                                 "eligible": True,
                                 "caps": [{"rule": "severity-high", "limit": 5,
                                           "source": ["FND-SEC-001"]}]},
                },
                "product": {"score": 5.0, "interval": [4.0, 5.0],
                            "published": True, "eligible_weight": 3,
                            "applicable_weight": 3, "lowest": ["security"]},
                "process": {"score": None, "interval": None,
                            "published": False, "scored": 0,
                            "applicable": 0, "lowest": []},
                "single": {"score": 5.0, "raw": 5.0, "interval": [4.0, 5.0],
                           "flag": "product-only",
                           "ceiling": {"limit": 6,
                                       "reasons": ["severity:HIGH",
                                                   "readiness:PENDING EVIDENCE"]},
                           "band": "Average"},
            },
            "coverage": {"families": {}, "labels": {"security": "PARTIAL"}},
            "exclusions": ["docs/generated - generated content"],
        }

    def check(self, model, catalogue=None):
        return self.checker.check_model(
            model, self.catalogue if catalogue is None else catalogue
        )

    def test_valid_model_passes(self):
        self.assertEqual(self.check(self._valid_model()), [])

    def test_broken_model_reports_each_failure(self):
        model = self._valid_model()
        model["evidence"][0]["claims"] = ["SEC-NOPE-01"]
        model["findings"][0]["counter"] = ""
        model["risks"][0]["finding"] = "FND-SEC-099"
        model["scores"]["dimensions"]["security"]["interval"] = [6, 9]
        failures = self.check(model)
        joined = "\n".join(failures)
        self.assertIn("claims unknown criteria SEC-NOPE-01", joined)
        self.assertIn("no recorded counter-evidence", joined)
        self.assertIn("cites unknown finding 'FND-SEC-099'", joined)
        self.assertIn(
            "does not equal the capped FAIL/PASS substitution bounds [4, 5]",
            joined)

    def test_partial_without_mastery_fails(self):
        model = self._valid_model()
        model["criteria"][1]["mastery"] = None
        joined = "\n".join(self.check(model))
        self.assertIn("PARTIAL requires a recorded mastery fraction", joined)

    def test_declared_only_dimension_fails_gate(self):
        model = self._valid_model()
        model["evidence"][0]["kind"] = "DECLARED"
        model["evidence"][1]["kind"] = "DECLARED"
        failures = self.check(model)
        self.assertTrue(
            any("fails the eligibility gate" in failure for failure in failures),
            failures,
        )

    def _finding(self, fid, criteria, severity, claim_class, **extra):
        finding = {"id": fid, "criteria": criteria, "type": "Concern",
                   "severity": severity, "claim_class": claim_class,
                   "observation": "...", "property": "...",
                   "evidence": ["EVD-001"],
                   "counter": "checked alternate paths",
                   "consequence": "...", "scope": "...", "confidence": "HIGH",
                   "status": "Open", "next_verification": "..."}
        finding.update(extra)
        return finding

    def _criteria_entry(self, cid, dimension, outcome, **extra):
        entry = {"id": cid, "catalogue_id": cid, "channel": "score",
                     "source": "catalogue",
                     "applicability": "applicable", "criticality": "medium",
                     "weight": 1.0, "expected": "...", "method": "...",
                     "sufficiency": "...", "dimension": dimension,
                     "outcome": outcome, "level": None, "mastery": None}
        entry.update(extra)
        return entry

    def test_open_bounding_finding_bounds_criteria_mastery(self):
        model = copy.deepcopy(self._valid_model())
        model["findings"].append(
            self._finding("FND-SEC-002", "SEC-AUTHZ", "MEDIUM",
                          "confirmed defect"))
        joined = "\n".join(self.check(model))
        self.assertIn("exceeds the 0.5 bound", joined)

    def test_bounding_finding_citing_unresolved_criteria_fails(self):
        model = copy.deepcopy(self._valid_model())
        model["findings"].append(
            self._finding("FND-SEC-003", "SEC-CRYPTO", "MEDIUM",
                          "confirmed defect"))
        joined = "\n".join(self.check(model))
        self.assertIn("cites unresolved criteria SEC-CRYPTO", joined)

    def test_census_none_basis_checked_against_project_census(self):
        catalogue = self._catalogue(
            self.catalogue["criteria"] + [
                self._cat_entry("DEP-CI", "deployability",
                                na_rules=["census-none", "deployment-model"]),
            ]
        )

        def model_with(census):
            model = copy.deepcopy(self._valid_model())
            model["scope"]["projects"][0]["automation_census"] = census
            model["criteria"].append(
                self._criteria_entry(
                    "DEP-CI", "deployability", "NOT_APPLICABLE",
                    na_basis="census-none",
                    applicability="not applicable - automation census none"))
            model["findings"].append(
                self._finding("FND-INF-001", "DEP-CI", "MEDIUM",
                              "confirmed structural weakness",
                              absence="No documented rationale"))
            return model

        self.assertEqual(self.check(model_with("none"), catalogue), [])
        joined = "\n".join(self.check(model_with("signals"), catalogue))
        self.assertIn("census-none basis requires automation census none", joined)

    def test_deduction_needs_open_finding_or_evidenced_shortfall(self):
        model = copy.deepcopy(self._valid_model())
        catalogue = self._catalogue(
            self.catalogue["criteria"] + [
                self._cat_entry("SEC-SESS", "security"),
            ]
        )
        model["criteria"].append(
            self._criteria_entry("SEC-SESS", "security", "PARTIAL", mastery=0.5,
                            level="P50"))
        model["evidence"][0]["claims"].append("SEC-SESS")
        failures = self.check(model, catalogue)
        self.assertIn(
            "SEC-SESS: PARTIAL deduction has no open finding and no recorded "
            "shortfall with evidence",
            failures,
        )
        model["criteria"][-1]["shortfall"] = "session rotation absent"
        failures = self.check(model, catalogue)
        self.assertNotIn(
            "SEC-SESS: PARTIAL deduction has no open finding and no recorded "
            "shortfall with evidence",
            failures,
        )

    def test_noncanonical_dimension_id_fails(self):
        model = copy.deepcopy(self._valid_model())
        model["criteria"][0]["dimension"] = "design-soundness"
        joined = "\n".join(self.check(model))
        self.assertIn(
            "dimension 'design-soundness' is not a canonical dimension id",
            joined)

    def test_half_up_rounding_of_uncapped(self):
        """A P25 mastery (0.25 x 10 = 2.5) rounds up to 3 - Python round()
        gives 2."""
        model = {
            "model_version": 2,
            "scope": {"scoring_policy": 3, "history": "present",
                      "catalogue_version": 1, "detail_level": "Standard",
                      "requirements_baseline": None,
                      "product_profile": {"natures": ["service"]},
                      "projects": [{"path": ".",
                                    "automation_census": "signals"}]},
            "inventory": [],
            "criteria": [
                self._criteria_entry("CQY-DEAD", "code_quality", "PARTIAL",
                                mastery=0.25, level="P25",
                                shortfall="dead code paths remain"),
            ],
            "requirements": [],
            "evidence": [
                {"id": "EVD-001", "kind": "INSPECTED", "collector": "x",
                 "method": "read", "timestamp": "...", "tool": None,
                 "locator": {"path": "src/app.py", "lines": [1, 40]},
                 "procedure": None, "result": "...",
                 "claims": ["CQY-DEAD"], "limits": "...",
                 "sampling": "full", "counter": "...", "redaction": "none",
                 "unavailable": None},
            ],
            "findings": [], "risks": [], "recommendations": [],
            "readiness": {"state": "READY", "blocking": []},
            "scores": {
                "scale_max": 10,
                "dimensions": {
                    "code_quality": {"mastery": 0.25, "uncapped": 3,
                                     "score": 3, "coverage": 1.0,
                                     "eligible": True},
                },
                "product": {"score": 3.0, "interval": None,
                            "published": True, "eligible_weight": 2,
                            "applicable_weight": 2,
                            "lowest": ["code_quality"]},
                "process": {"score": None, "interval": None,
                            "published": False, "scored": 0,
                            "applicable": 0, "lowest": []},
                "single": {"score": 3.0, "raw": 3.0, "interval": None,
                           "flag": "product-only", "ceiling": None,
                           "band": "Poor"},
            },
            "coverage": {"families": {}, "labels": {}},
            "exclusions": [],
        }
        catalogue = self._catalogue(
            [self._cat_entry("CQY-DEAD", "code_quality")]
        )
        self.assertEqual(self.check(model, catalogue), [])
        model["scores"]["dimensions"]["code_quality"]["uncapped"] = 2
        model["scores"]["dimensions"]["code_quality"]["score"] = 2
        joined = "\n".join(self.check(model, catalogue))
        self.assertIn("does not recompute to 3", joined)

    def test_missing_triggered_mechanical_cap_fails(self):
        model = copy.deepcopy(self._valid_model())
        del model["scores"]["dimensions"]["security"]["caps"]
        joined = "\n".join(self.check(model))
        self.assertIn(
            "missing mechanical cap severity-high triggered by FND-SEC-001",
            joined)

    def test_material_unknown_cap_tracks_criticality(self):
        model = copy.deepcopy(self._valid_model())
        catalogue = copy.deepcopy(self.catalogue)
        model["criteria"][2]["criticality"] = "high"
        catalogue["criteria"][2]["criticality"] = "high"
        joined = "\n".join(self.check(model, catalogue))
        self.assertIn(
            "missing mechanical cap material-unknown triggered by SEC-CRYPTO",
            joined)
        model["scores"]["dimensions"]["security"]["caps"].append(
            {"rule": "material-unknown", "limit": 8, "source": ["SEC-CRYPTO"]})
        self.assertEqual(self.check(model, catalogue), [])

    def test_undeclared_claim_class_fails(self):
        model = copy.deepcopy(self._valid_model())
        model["findings"][0]["claim_class"] = "suspected bug"
        joined = "\n".join(self.check(model))
        self.assertIn("is not a declared claim class", joined)

    def test_not_applicable_needs_valid_na_basis(self):
        model = copy.deepcopy(self._valid_model())
        del model["criteria"][3]["na_basis"]
        joined = "\n".join(self.check(model))
        self.assertIn("NOT_APPLICABLE needs na_basis", joined)

        model = copy.deepcopy(self._valid_model())
        model["criteria"][3]["na_basis"] = "history-out-of-scope"
        joined = "\n".join(self.check(model))
        self.assertIn(
            "history-out-of-scope basis requires scope.history absent or "
            "out-of-scope",
            joined)

    def test_nonbounding_findings_carry_no_bound(self):
        model = copy.deepcopy(self._valid_model())
        model["findings"].append(
            self._finding("FND-SEC-004", "SEC-CRYPTO", "LOW",
                          "plausible hypothesis"))
        model["findings"].append(
            self._finding("FND-SEC-005", "SEC-CRYPTO", "LOW",
                          "evidence gap"))
        self.assertEqual(self.check(model), [])

    def test_multi_project_scores_per_project(self):
        model = copy.deepcopy(self._valid_model())
        model["scope"]["projects"] = [
            {"name": "api", "automation_census": "signals"},
            {"name": "cli", "automation_census": "signals"},
        ]
        model["criteria"] = [
            self._criteria_entry("SEC-AUTHZ", "api.security", "PASS",
                            criticality="high", level="PASS", mastery=1.0),
            self._criteria_entry("SEC-AUTHZ-02", "cli.security", "PASS",
                            criticality="high", level="PASS", mastery=1.0,
                            catalogue_id="SEC-AUTHZ"),
        ]
        catalogue = self._catalogue([
            self._cat_entry("SEC-AUTHZ", "security", criticality="high"),
        ])
        model["evidence"][0]["claims"] = ["SEC-AUTHZ", "SEC-AUTHZ-02"]
        del model["evidence"][1]
        model["findings"] = []
        model["risks"] = []
        model["recommendations"] = []
        model["readiness"] = {"per_project": {
            "api": {"state": "READY", "blocking": []},
            "cli": {"state": "READY", "blocking": []},
        }}
        model["scores"]["dimensions"] = {
            "api.security": {"mastery": 1.0, "uncapped": 10, "score": 10,
                             "coverage": 1.0, "eligible": True},
            "cli.security": {"mastery": 1.0, "uncapped": 10, "score": 10,
                             "coverage": 1.0, "eligible": True},
        }
        for key in ("product", "process", "single"):
            del model["scores"][key]
        headline = {
            "product": {"score": 10.0, "interval": None, "published": True,
                        "eligible_weight": 3, "applicable_weight": 3,
                        "lowest": ["security"]},
            "process": {"score": None, "interval": None, "published": False,
                        "scored": 0, "applicable": 0, "lowest": []},
            "single": {"score": 10.0, "raw": 10.0, "interval": None,
                       "flag": "product-only", "ceiling": None,
                       "band": "Excellent"},
        }
        model["scores"]["per_project"] = {
            "api": copy.deepcopy(headline),
            "cli": copy.deepcopy(headline),
        }
        self.assertEqual(self.check(model, catalogue), [])
        model["scores"]["overall"] = {"score": None}
        joined = "\n".join(self.check(model, catalogue))
        self.assertIn("scores.overall is removed in model v2", joined)
        del model["scores"]["overall"]
        del model["scores"]["per_project"]["cli"]
        joined = "\n".join(self.check(model, catalogue))
        self.assertIn("per_project record missing for project 'cli'", joined)

    def test_scoring_policy_must_be_three(self):
        model = copy.deepcopy(self._valid_model())
        del model["scope"]["scoring_policy"]
        joined = "\n".join(self.check(model))
        self.assertIn("scope.scoring_policy is None, expected 3", joined)


class TestRegisterBlocks(unittest.TestCase):
    def setUp(self):
        self.validator = load_script("validate-report.py")

    REC_BLOCK = (
        "### REC-001 Add input validation\n\n"
        "- **Priority:** P1\n"
        "- **Finding:** FND-SEC-001\n"
        "- **Condition:** input rejected at boundary\n"
        "- **Description:** adds a validator\n"
        "- **Impact:** fewer injection paths\n"
        "- **Effort:** Low\n"
        "- **Complexity:** Low\n"
        "- **Verification:** unit test rejects payload\n"
    )

    FND_HEADING = "### FND-SEC-001 Missing input validation\n\n"

    def test_rec_block_complete_passes(self):
        lines = (self.FND_HEADING + self.REC_BLOCK).split("\n")
        self.assertEqual(self.validator.check_rec_blocks(lines), [])

    def test_rec_block_missing_condition_and_bad_refs(self):
        block = self.REC_BLOCK.replace(
            "- **Condition:** input rejected at boundary\n", ""
        ).replace("- **Priority:** P1", "- **Priority:** P9")
        block += "- **Depends:** REC-042\n"
        block = block.replace("- **Finding:** FND-SEC-001",
                              "- **Finding:** FND-SEC-099")
        lines = (self.FND_HEADING + block).split("\n")
        joined = "\n".join(self.validator.check_rec_blocks(lines))
        self.assertIn("missing Condition", joined)
        self.assertIn("Priority is not P1-P4", joined)
        self.assertIn("Finding does not name a defined finding", joined)
        self.assertIn("Depends cites undefined REC-042", joined)

    def test_tdr_block_validation(self):
        lines = (
            self.FND_HEADING
            + "### TDR-001 Legacy session store\n\n"
            + "- **Category:** Habitability\n"
            + "- **Source:** FND-SEC-099\n"
            + "- **Description:** debt\n"
            + "- **Status:** Open\n"
        ).split("\n")
        joined = "\n".join(self.validator.check_tdr_blocks(lines))
        self.assertNotIn("missing Cost", joined)
        self.assertNotIn("missing Delay", joined)
        self.assertIn("Category is not a CISQ characteristic", joined)
        self.assertIn("Source is not a finding or Direct observation", joined)

    def test_risk_source_must_resolve(self):
        risk = (
            "### RSK-001 Injection reaches production\n\n"
            "- **Severity:** High\n"
            "- **Likelihood:** Medium\n"
            "- **Residual:** Medium\n"
            "- **Status:** Open\n"
            "- **Description:** what could go wrong\n"
            "- **Impact:** consequence\n"
            "- **Trigger:** crafted input\n"
            "- **Controls:** none verified\n"
            "- **Mitigation:** validate input\n"
            "- **Closure:** retest\n"
            "- **Source:** {source}\n"
            "- **Confidence:** High\n"
        )
        good = self.FND_HEADING + risk.format(source="FND-SEC-001")
        bad = self.FND_HEADING + risk.format(source="FND-SEC-099")
        self.assertEqual(self.validator.check_risk_blocks(good.split("\n")), [])
        joined = "\n".join(
            self.validator.check_risk_blocks(bad.split("\n"))
        )
        self.assertIn("Source does not name a defined finding", joined)

    def test_scorecard_interval_sanity(self):
        self.assertEqual(
            self.validator.check_scorecard_interval("| D | 7/10 [4-9] | x |\n"),
            [],
        )
        joined = "\n".join(
            self.validator.check_scorecard_interval(
                "| D | 7/10 [8-9] | x |\n| E | 5/10 [5-5] | y |\n"
                "| F | 3/10 [0-12] | z |\n"
            )
        )
        self.assertIn("does not contain its point score", joined)
        self.assertIn("degenerate", joined)
        self.assertIn("outside the 0-10 scale", joined)

    def test_structure_and_naming_conformance_checks(self):
        good = (
            "## Structure Review\n\n"
            "| Area | Verdict | Basis |\n"
            "|---|---|---|\n"
            "| Directory organization | Partially | established |\n"
            "| Naming conventions | Partially | required |\n"
            "| Component placement | Passed | established |\n"
            "| Supporting-artifact layout | Passed | recommended |\n"
            "| Consistency | Passed | established |\n\n"
            "## Structure Conformance\n\n"
            "| Component | Surface | Convention | Observed | Status | Evidence |\n"
            "|---|---|---|---|---|---|\n"
            "| `src/App` | Directories | Full words | `App/` | Partial | EVD-001 |\n\n"
            "## Code Style\n\n"
            "| Lens | Status | Justification |\n"
            "|---|---|---|\n"
            "| SL-1 Convention fit | Partial | 88% dominant |\n"
        )
        self.assertEqual(self.validator.check_structure_and_naming(good), [])
        bad = (
            "## Structure Review\n\n"
            "| Area | Verdict | Basis |\n"
            "|---|---|---|\n"
            "| Directory organization | GOOD | established |\n\n"
            "## Structure Conformance\n\n"
            "| Component | Surface | Status |\n"
            "|---|---|---|\n"
            "| `src/App` | Directories | INVALID |\n"
        )
        joined = "\n".join(self.validator.check_structure_and_naming(bad))
        self.assertIn("missing row 'Naming conventions'", joined)
        self.assertIn("verdict 'GOOD'", joined)
        self.assertIn("status 'INVALID'", joined)

    def test_glossary_triplets_table_enforced_at_detailed_level(self):
        base = (
            "## Document Information\n\n"
            "| | |\n|---|---|\n"
            "| Detail Level | Detailed |\n\n"
            "## Glossary Index\n\n"
            "{triplets}"
            "## Auditing Methodology\n\n"
            "**Criteria table**\n\n"
            "| Criteria | Family | Applicability | Criticality | Method | Sufficiency |\n"
            "|---|---|---|---|---|---|\n"
            "| TST-UNIT | test | applicable | high | inspect | files |\n"
            "| SEC-AUTHZ | sec | applicable | high | inspect | files |\n\n"
            "## Technical Findings\n\n"
            "### FND-SEC-001 Finding\n"
        )
        missing = base.format(triplets="")
        self.assertTrue(
            any(
                "missing the '**Identifier triplets**' table" in f
                for f in self.validator.check_glossary_triplets(missing, "")
            )
        )
        wrong_order = (
            "**Identifier triplets**\n\n"
            "| Triplet | Scope | Description |\n"
            "|---|---|---|\n"
            "| EVD | Evidence | ledger |\n"
            "| FND | Findings | findings |\n"
            "| TST | Criteria | test |\n"
        )
        joined = "\n".join(
            self.validator.check_glossary_triplets(
                base.format(triplets=wrong_order), wrong_order
            )
        )
        self.assertIn("must start with 'FND' then 'EVD'", joined)
        self.assertIn("missing 'SEC'", joined)
        valid = (
            "**Identifier triplets**\n\n"
            "| Triplet | Scope | Description |\n"
            "|---|---|---|\n"
            "| FND | Findings | findings |\n"
            "| EVD | Evidence | ledger |\n"
            "| TST | Criteria | test |\n"
            "| SEC | Criteria | security |\n"
        )
        self.assertEqual(
            self.validator.check_glossary_triplets(
                base.format(triplets=valid), valid
            ),
            [],
        )


class TestRegisterNumbering(unittest.TestCase):
    def setUp(self):
        self.validator = load_script("validate-report.py")

    def run_check(self, body):
        lines = body.split("\n")
        return self.validator.check_register_numbering(
            lines, self.validator.split_code(lines)
        )

    def test_global_contiguous_numbering_passes(self):
        body = (
            "## alpha\n\n### FND-SEC-001 A\n\n### FND-ARC-001 B\n\n"
            "## beta\n\n### FND-SEC-002 C\n\n### RSK-001 R\n\n"
            "### REC-001 X\n\n### REC-002 Y\n\n### TDR-001 D\n\n"
            "## Evidence List\n\n| Evidence | Result |\n|---|---|\n"
            "| EVD-001 | ok |\n| EVD-002 | ok |\n"
        )
        self.assertEqual(self.run_check(body), [])

    def test_per_project_reset_is_flagged(self):
        body = (
            "## alpha\n\n### FND-SEC-001 A\n\n### RSK-001 R\n\n"
            "## beta\n\n### FND-SEC-001 B\n\n### RSK-001 S\n\n"
        )
        joined = "\n".join(self.run_check(body))
        self.assertIn("FND-SEC-001 is defined more than once", joined)
        self.assertIn("RSK-001 is defined more than once", joined)

    def test_gap_in_sequence_is_flagged(self):
        body = "### FND-SEC-001 A\n\n### FND-SEC-003 B\n\n### REC-002 X\n"
        joined = "\n".join(self.run_check(body))
        self.assertIn("FND-SEC identifiers", joined)
        self.assertIn("REC identifiers", joined)

    def test_evd_rows_are_unique_and_contiguous(self):
        good = "| EVD-001 | a |\n| EVD-002 | b |\n"
        self.assertEqual(self.run_check(good), [])
        dup = "| EVD-001 | a |\n| EVD-002 | b |\n| EVD-002 | c |\n"
        self.assertTrue(
            any("EVD-002 is defined more than once" in f for f in self.run_check(dup))
        )

    def test_qualified_definition_cells_count_once(self):
        body = "| api::EVD-001 | a |\n| EVD-002 | b |\n"
        self.assertEqual(self.run_check(body), [])


class TestFrameGeometry(unittest.TestCase):
    def setUp(self):
        self.validator = load_script("validate-report.py")

    def run_check(self, diagram):
        lines = ("```\n" + diagram + "```\n").split("\n")
        return self.validator.check_frame_geometry(
            lines, self.validator.split_code(lines)
        )

    def test_aligned_frame_passes(self):
        body = (
            "  ╭────────╮\n"
            "  │ Client │\n"
            "  ╰────────╯\n"
        )
        self.assertEqual(self.run_check(body), [])

    def test_side_by_side_frames_pass(self):
        body = (
            "╭───╮  ╭─────╮\n"
            "│ A │  │  B  │\n"
            "╰───╯  ╰─────╯\n"
        )
        self.assertEqual(self.run_check(body), [])

    def test_misaligned_side_border_fails(self):
        body = (
            "╭────────╮\n"
            "│ Client  │\n"
            "╰────────╯\n"
        )
        self.assertTrue(self.run_check(body))

    def test_misaligned_bottom_border_fails(self):
        body = (
            "╭────────╮\n"
            "│ Client │\n"
            "╰─────────╯\n"
        )
        self.assertTrue(self.run_check(body))

    def test_unclosed_frame_fails(self):
        body = "╭────────╮\n│ Client │\n"
        self.assertTrue(
            any("never closes" in f for f in self.run_check(body))
        )

    def test_connector_rows_between_frames_pass(self):
        body = (
            "╭────────╮\n"
            "│ Client │\n"
            "╰────────╯\n"
            "    │\n"
            "    v\n"
            "╭────────╮\n"
            "│ Server │\n"
            "╰────────╯\n"
        )
        self.assertEqual(self.run_check(body), [])


class TestDefectScenarios(unittest.TestCase):
    def setUp(self):
        self.validator = load_script("validate-report.py")

    BLOCK = (
        "### FND-SEC-001 Bad\n\n"
        "- **Severity:** {sev}\n"
    )

    def test_high_finding_needs_scenario(self):
        lines = self.BLOCK.format(sev="High, chain traced").split("\n")
        failures = self.validator.check_hunt_scenarios(lines)
        self.assertTrue(any("Scenario" in f for f in failures))

    def test_medium_finding_exempt(self):
        lines = self.BLOCK.format(sev="Medium").split("\n")
        self.assertEqual(self.validator.check_hunt_scenarios(lines), [])

    def test_high_finding_with_scenario_passes(self):
        lines = (
            self.BLOCK.format(sev="Critical")
            + "- **Scenario:** conditions; steps; expected; observed; static\n"
        ).split("\n")
        self.assertEqual(self.validator.check_hunt_scenarios(lines), [])


if __name__ == "__main__":
    unittest.main()


class TestScorecardConformance(unittest.TestCase):
    def test_noncanonical_dimension_flagged(self):
        vr = load_script("validate-report.py")
        text = "**Scorecard Summary**\n\n| Dimension | Score |\n|---|---|\n| Correctness | 7/10 |\n| Security | 6/10 |\n"
        fails = vr.check_scorecard_dimensions(text)
        self.assertTrue(any("Correctness" in f for f in fails))

    def test_out_of_order_dimension_flagged(self):
        vr = load_script("validate-report.py")
        text = "**Scorecard Summary**\n\n| Dimension | Score |\n|---|---|\n| API Compatibility | 3/10 |\n| Security | 6/10 |\n"
        fails = vr.check_scorecard_dimensions(text)
        self.assertTrue(any("order" in f for f in fails))

    def test_na_row_flagged_in_dashboard_table(self):
        vr = load_script("validate-report.py")
        text = "### Health Dashboard\n\n| Dimension | Score | Basis |\n|---|---|---|\n| Testability | N/A | none |\n"
        fails = vr.check_scorecard_dimensions(text)
        self.assertTrue(any("N/A" in f for f in fails))

    def test_interval_cell_accepted(self):
        vr = load_script("validate-report.py")
        text = "**Scorecard Summary**\n\n| Dimension | Score |\n|---|---|\n| Scalability | 8/10 [6-8] |\n"
        self.assertEqual(vr.check_scorecard_dimensions(text), [])

    def test_extra_column_flagged(self):
        vr = load_script("validate-report.py")
        text = "**Scorecard Summary**\n\n| Dimension | Score | Notes |\n|---|---|---|\n| Scalability | 8/10 | x |\n"
        fails = vr.check_scorecard_dimensions(text)
        self.assertTrue(any("exactly" in f for f in fails), fails)


class TestHealthDashboard(unittest.TestCase):
    def _report(self, dashboard_body):
        return ("# R\n\n## Document Information\n\n| | |\n|---|---|\n"
                + "## Health Dashboard\n\n" + dashboard_body)

    def test_missing_markers_flagged(self):
        vr = load_script("validate-report.py")
        fails = vr.check_health_dashboard(self._report("| a | b |\n|---|---|\n"))
        self.assertEqual(len(fails), 4)

    def test_bold_and_heading_forms_accepted(self):
        vr = load_script("validate-report.py")
        body = ("**Risk Map**\n\nx\n\n**Legend**\n\n"
                "| Band | Score |\n|---|---|\n"
                "| Poor | 1-3 |\n| Average | 4-6 |\n| Good | 7-8 |\n| Excellent | 9-10 |\n\n"
                "**Scorecard Summary**\n\ny\n\n**Team & Continuity**\n\nz\n")
        self.assertEqual(vr.check_health_dashboard(self._report(body)), [])
        body2 = ("### Risk Map\n\nx\n\n**Legend**\n\n"
                 "| Band | Score |\n|---|---|\n"
                 "| Poor | 1-3 |\n| Average | 4-6 |\n| Good | 7-8 |\n| Excellent | 9-10 |\n\n"
                 "### Scorecard Summary\n\ny\n\n### Team & Continuity\n\nz\n")
        self.assertEqual(vr.check_health_dashboard(self._report(body2)), [])


class TestDocInfoFields(unittest.TestCase):
    def _report(self, rows):
        table = "\n".join(f"| {k} | {v} |" for k, v in rows)
        return "## Document Information\n\n| | |\n|---|---|\n" + table + "\n"

    REQUIRED = [
        ("Report Revision", "1.0"), ("Report Date", "2026-01-01"),
        ("Report Style", "Audit"), ("Detail Level", "Detailed"),
        ("Evaluation Scale", "1-10"), ("Language", "English"),
        ("Audit Purpose", "Production readiness"),
        ("Target Environment", "Self-hosted"),
        ("Verification Scope", "Static repository analysis"),
        ("Evidence Mode", "Source-only"),
        ("Subject Revision", "abc123 (main)"),
        ("Skill Version", "2.6.5"), ("Time taken", "10:00"),
    ]

    def test_conforming_table_passes(self):
        vr = load_script("validate-report.py")
        self.assertEqual(vr.check_doc_info_fields(self._report(self.REQUIRED)), [])

    def test_missing_required_flagged(self):
        vr = load_script("validate-report.py")
        rows = [r for r in self.REQUIRED if r[0] != "Language"]
        fails = vr.check_doc_info_fields(self._report(rows))
        self.assertTrue(any("Language" in f for f in fails))

    def test_prefixed_skill_version_flagged(self):
        vr = load_script("validate-report.py")
        rows = [(k, "lens-skill" if k == "Skill Version" else v) for k, v in self.REQUIRED]
        fails = vr.check_doc_info_fields(self._report(rows))
        self.assertTrue(any("Skill Version" in f for f in fails))

    def test_noncanonical_row_flagged(self):
        vr = load_script("validate-report.py")
        rows = self.REQUIRED + [("System type", "Codebase under development")]
        fails = vr.check_doc_info_fields(self._report(rows))
        self.assertTrue(any("System type" in f for f in fails))


class TestModelConsistency(unittest.TestCase):
    def setUp(self):
        self.validator = load_script("validate-report.py")

    def _model(self) -> dict:
        return {
            "model_version": 1,
            "scope": {"subject": "demo", "scoring_policy": 2, "history": "present",
                      "projects": [{"path": ".", "name": "demo",
                                    "automation_census": "signals"}]},
            "inventory": [],
            "criteria": [
                {"id": "SEC-AUTHZ", "dimension": "security", "outcome": "PASS",
                 "weight": 1.0, "mastery": None},
                {"id": "SEC-INJ", "dimension": "security", "outcome": "PARTIAL",
                 "weight": 1.0, "mastery": 0.25},
                {"id": "CMP-API", "dimension": "api_compatibility",
                 "outcome": "NOT_APPLICABLE", "weight": 1.0, "mastery": None},
            ],
            "evidence": [
                {"id": "EVD-001", "kind": "INSPECTED", "claims": ["SEC-AUTHZ"]},
                {"id": "EVD-002", "kind": "INSPECTED", "claims": ["SEC-INJ"]},
            ],
            "findings": [
                {"id": "FND-SEC-001", "criteria": "SEC-INJ", "severity": "HIGH",
                 "claim_class": "confirmed defect", "status": "Open",
                 "evidence": ["EVD-002"]},
            ],
            "risks": [
                {"id": "RSK-001", "finding": "FND-SEC-001", "severity": "HIGH"},
            ],
            "recommendations": [
                {"id": "REC-001", "finding": "FND-SEC-001", "priority": "P1"},
            ],
            "scores": {
                "scale_max": 10,
                "dimensions": {
                    "security": {"mastery": 0.625, "uncapped": 6, "score": 5,
                                 "interval": [4, 5], "coverage": 0.67,
                                 "eligible": True,
                                 "caps": [{"rule": "severity-high", "limit": 5,
                                           "source": ["FND-SEC-001"]}]},
                },
                "overall": {"score": 5.0, "scored": 1, "applicable": 1},
            },
            "coverage": {"families": {}, "labels": {}},
            "exclusions": [],
        }

    REPORT = """## Document Information

| Field | Value |
|-------|-------|
| Report Style | audit |

## Executive Summary

| Overall score | 5.0/10 |
|---------------|--------|

The lowest dimension is security.

## Health Dashboard

**Legend**

| Band | Score |
|---|---|
| Poor | 1-3 |
| Average | 4-6 |
| Good | 7-8 |
| Excellent | 9-10 |

**Legend**

| Band | Score |
|---|---|
| Poor | 1-3 |
| Average | 4-6 |
| Good | 7-8 |
| Excellent | 9-10 |

**Scorecard Summary**

| Dimension | Score |
|-----------|-------|
| Security  | 5/10  |

Security's interval [4-5] bounds the unresolved criteria.

## Technical Findings

### FND-SEC-001 Injection sink reaches the handler

- **Severity:** High

## Unified Risk Register

### RSK-001 Injection ships to release

- **Severity:** High

## Remediation Roadmap

### REC-001 Validate the input path

- **Priority:** P1

## Auditing Methodology

**Evidence List**

| Evidence | Source | Result |
|----------|--------|--------|
| EVD-001  | read   | ok     |
| EVD-002  | read   | ok     |
"""

    def _check(self, text=None, model=None, style="audit"):
        return self.validator.check_model_consistency(
            self.REPORT if text is None else text,
            self._model() if model is None else model,
            style,
        )

    def test_x1_consistent_fragment_passes(self):
        self.assertEqual(self._check(), [])

    def test_x2_score_mismatch(self):
        text = self.REPORT.replace("| Security  | 5/10  |", "| Security  | 6/10       |")
        fails = self._check(text)
        self.assertTrue(any("Security" in f and "model has 5/10" in f
                            for f in fails), fails)

    def test_x2_interval_in_report_absent_in_model(self):
        model = self._model()
        del model["scores"]["dimensions"]["security"]["interval"]
        fails = self._check(model=model)
        self.assertFalse(any("interval" in f for f in fails), fails)

    def test_x2_interval_in_cell_flagged(self):
        text = self.REPORT.replace("| Security  | 5/10  |",
                                   "| Security  | 5/10 [4-5] |")
        fails = self._check(text)
        self.assertTrue(any("disclosure line" in f for f in fails), fails)

    def test_x2_unknown_cell_while_model_scores(self):
        text = self.REPORT.replace("| Security  | 5/10  |", "| Security  | Unknown |")
        fails = self._check(text)
        self.assertTrue(any("Security" in f for f in fails), fails)

    def test_x2_applicable_dimension_omitted(self):
        model = self._model()
        model["criteria"].append(
            {"id": "TST-UNIT", "dimension": "testability", "outcome": "PASS",
             "weight": 1.0, "mastery": None}
        )
        fails = self._check(model=model)
        self.assertTrue(
            any("omits applicable dimension Testability" in f for f in fails),
            fails,
        )

    def test_x3_overall_value_differs(self):
        text = self.REPORT.replace("| Overall score | 5.0/10 |",
                                   "| Overall score | 5.5/10 |")
        fails = self._check(text)
        self.assertTrue(any("overall score 5.5/10 differs" in f for f in fails),
                        fails)

    def test_x4_register_mismatches(self):
        model = self._model()
        model["findings"].append(
            {"id": "FND-SEC-002", "criteria": "SEC-INJ", "severity": "LOW",
             "claim_class": "confirmed defect", "status": "Open",
             "evidence": ["EVD-002"]}
        )
        fails = self._check(model=model)
        joined = "\n".join(fails)
        self.assertIn("report has 1 FND blocks, model has 2", joined)
        self.assertIn("FND-SEC-002 appears in the model but not in the report",
                      joined)
        text = self.REPORT.replace("- **Severity:** High",
                                   "- **Severity:** Low", 1)
        fails = self._check(text)
        self.assertTrue(any("FND-SEC-001: report severity Low differs" in f
                            for f in fails), fails)

    def test_x5_evidence_mismatches(self):
        text = self.REPORT + "\nCited: EVD-099 nowhere.\n"
        fails = self._check(text)
        self.assertTrue(any("EVD-099 not present in the model" in f
                            for f in fails), fails)
        model = self._model()
        model["evidence"].append(
            {"id": "EVD-003", "kind": "INSPECTED", "claims": ["SEC-AUTHZ"]}
        )
        fails = self._check(model=model)
        self.assertTrue(any("evidence ledger lists 2 records, model has 3" in f
                            for f in fails), fails)

    def test_x6_multi_project_mapping(self):
        model = self._model()
        model["scope"]["projects"] = [
            {"path": "a", "name": "api", "automation_census": "none"},
            {"path": "c", "name": "cli", "automation_census": "none"},
        ]
        model["criteria"] = [
            {"id": "SEC-A", "dimension": "api.security", "outcome": "PASS",
             "weight": 1.0, "mastery": None},
            {"id": "SEC-C", "dimension": "cli.security", "outcome": "PASS",
             "weight": 1.0, "mastery": None},
        ]
        model["scores"]["dimensions"] = {
            "api.security": {"score": 5, "interval": [4, 5], "eligible": True},
            "cli.security": {"score": 7, "interval": None, "eligible": True},
        }
        model["scores"]["per_project"] = {
            "api": {"score": 5.0, "scored": 1, "applicable": 1},
            "cli": {"score": 7.0, "scored": 1, "applicable": 1},
        }
        model["scores"]["overall"] = {"score": None, "scored": 2, "applicable": 2}
        model["findings"] = []
        model["risks"] = []
        model["recommendations"] = []
        model["evidence"] = []
        text = """## Document Information

| Field | Value |
|-------|-------|
| Report Style | audit |

## Project `api`

| Overall score | 5.0/10 |
|---------------|--------|

**Legend**

| Band | Score |
|---|---|
| Poor | 1-3 |
| Average | 4-6 |
| Good | 7-8 |
| Excellent | 9-10 |

**Scorecard Summary**

| Dimension | Score |
|-----------|-------|
| Security  | 5/10  |

Security's interval [4-5] bounds the unresolved criteria.

## Project `cli`

| Overall score | 7.0/10 |
|---------------|--------|

**Legend**

| Band | Score |
|---|---|
| Poor | 1-3 |
| Average | 4-6 |
| Good | 7-8 |
| Excellent | 9-10 |

**Scorecard Summary**

| Dimension | Score |
|-----------|-------|
| Security  | 7/10  |
"""
        self.assertEqual(self._check(text, model), [])
        swapped = text.replace("| Overall score | 7.0/10 |",
                               "| Overall score | 5.0/10 |")
        fails = self._check(swapped, model)
        self.assertTrue(any("overall score cli 5.0/10 differs" in f
                            for f in fails), fails)

    def test_x7_criteria_table_outcome_mismatch(self):
        text = self.REPORT + """
**Criteria table**

| Criteria  | Outcome |
|-----------|---------|
| SEC-AUTHZ | PASS    |
| SEC-INJ   | PASS    |
"""
        fails = self._check(text)
        self.assertTrue(
            any("criteria table SEC-INJ: report PASS differs from the model "
                "PARTIAL" in f for f in fails),
            fails,
        )


class TestStateConsistency(unittest.TestCase):
    def setUp(self):
        self.validator = load_script("validate-report.py")

    def _state(self) -> dict:
        return {
            "state_version": 1,
            "run": {"phase": "validation",
                    "started": "2026-11-05T12:00:00Z",
                    "completed_phases": list(self.validator.PHASES[:6]),
                    "failed_phases": []},
            "gates": {
                g: {"resolution": "accepted", "tier": "explicit"}
                for g in self.validator.REQUIRED_GATES
            },
            "artifacts": [
                {"path": "report.md", "kind": "report",
                 "declared_phase": "validation"},
                {"path": "part-1.md", "kind": "part",
                 "declared_phase": "synthesis"},
            ],
            "timestamps": {"created": "2026-11-05T12:00:00Z",
                           "updated": "2026-11-05T13:00:00Z"},
        }

    def _check(self, state, root):
        state_path = Path(root) / "work" / "audit-state.json"
        return self.validator.check_state_consistency(state, state_path, None)

    def test_s1_consistent_state_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "work"
            work.mkdir()
            (Path(tmp) / "report.md").write_text("x", encoding="utf-8")
            self.assertEqual(self._check(self._state(), tmp), [])

    def test_s2_wrong_phase_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "work"
            work.mkdir()
            (Path(tmp) / "report.md").write_text("x", encoding="utf-8")
            state = self._state()
            state["run"]["phase"] = "scope-definition"
            fails = self._check(state, tmp)
            self.assertTrue(any("run.phase" in f for f in fails), fails)

    def test_s3_capitalized_phase_fails_twice(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "work"
            work.mkdir()
            (Path(tmp) / "report.md").write_text("x", encoding="utf-8")
            state = self._state()
            state["run"]["completed_phases"] = ["intake", "Synthesis"]
            fails = self._check(state, tmp)
            joined = "\n".join(fails)
            self.assertIn("phase name 'Synthesis' is not a workflow phase",
                          joined)
            self.assertIn("must list intake through synthesis", joined)

    def test_s4_missing_model_artifact_fails_part_exempt(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "work"
            work.mkdir()
            (Path(tmp) / "report.md").write_text("x", encoding="utf-8")
            state = self._state()
            state["artifacts"].append(
                {"path": "audit-model.json", "kind": "model",
                 "declared_phase": "synthesis"}
            )
            fails = self._check(state, tmp)
            self.assertTrue(
                any("'audit-model.json' (model) is missing" in f for f in fails),
                fails,
            )
            self.assertFalse(any("part-1.md" in f for f in fails), fails)

    def test_s5_unknown_gate_tier_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "work"
            work.mkdir()
            (Path(tmp) / "report.md").write_text("x", encoding="utf-8")
            state = self._state()
            state["gates"]["audit-mode"]["tier"] = "guess"
            fails = self._check(state, tmp)
            self.assertTrue(any("gate audit-mode" in f for f in fails), fails)


class TestModelStateCli(unittest.TestCase):
    def test_cli_returns_zero_for_consistent_pair(self):
        validator = load_script("validate-report.py")
        generator = load_script("new-report.py")
        state_helper = TestStateConsistency()
        state_helper.setUp()
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "AUDIT-1.0.md"
            rc = generator.main(
                ["new-report.py", "--output", str(report)]
            )
            self.assertEqual(rc, 0)
            model_doc = {
                "scope": {"projects": [
                    {"path": ".", "name": "demo"}
                ]},
                "criteria": [],
                "evidence": [],
                "findings": [
                    {"id": "FND-SEC-001", "severity": "HIGH"}
                ],
                "risks": [{"id": "RSK-001", "severity": "HIGH"}],
                "recommendations": [{"id": "REC-001"}],
                "scores": {"scale_max": 10, "dimensions": {},
                           "overall": {"score": None}},
            }
            model = Path(tmp) / "audit-model.json"
            model.write_text(json.dumps(model_doc), encoding="utf-8")
            state = Path(tmp) / "work" / "audit-state.json"
            state.parent.mkdir()
            state.write_text(
                json.dumps(state_helper._state()), encoding="utf-8"
            )
            (Path(tmp) / "report.md").write_text("x", encoding="utf-8")
            rc = validator.main(str(report), model_path=str(model),
                                state_path=str(state))
            self.assertEqual(rc, 0)
            model_doc["findings"] = [{"id": "FND-SEC-002", "severity": "LOW"}]
            model.write_text(json.dumps(model_doc), encoding="utf-8")
            rc = validator.main(str(report), model_path=str(model))
            self.assertEqual(rc, 1)

    def test_dimension_id_parity_with_check_model(self):
        validator = load_script("validate-report.py")
        checker = load_script("check-model.py")
        self.assertEqual(
            [validator.dimension_slug(n) for n in validator.SCORECARD_DIMENSIONS],
            list(checker.CANONICAL_DIMENSIONS),
        )


class TestRepairs26(unittest.TestCase):
    def setUp(self):
        self.validator = load_script("validate-report.py")

    def test_r1_optional_doc_info_rows(self):
        rows = [
            ("Report Revision", "1.0"), ("Report Date", "2026-11-05"),
            ("Report Style", "audit"), ("Detail Level", "Detailed"),
            ("Evaluation Scale", "1-10"), ("Language", "English"),
            ("Verification Scope", "Static repository analysis"),
            ("Evidence Mode", "Source-only"), ("Subject Revision", "abc123"),
            ("Skill Version", "2.6.6"), ("Time taken", "1:00"),
        ]
        text = "## Document Information\n\n| Field | Value |\n|---|---|\n"
        text += "".join(f"| {k} | {v} |\n" for k, v in rows)
        self.assertEqual(self.validator.check_doc_info_fields(text), [])

    def test_r2_linked_dimension_name(self):
        text = ("**Scorecard Summary**\n\n"
                "| Dimension | Score |\n|---|---|\n"
                "| [Security](#security) | 7/10 |\n")
        self.assertEqual(self.validator.check_scorecard_dimensions(text), [])

    def test_r3_anchored_score_grammar(self):
        text = ("**Scorecard Summary**\n\n"
                "| Dimension | Score |\n|---|---|\n"
                "| Security | 7/10 garbage |\n")
        fails = self.validator.check_scorecard_dimensions(text)
        self.assertTrue(any("expected n/m" in f for f in fails), fails)

    def test_r4_dashboard_subsections_do_not_end_block(self):
        text = ("## Document Information\n\n| Field | Value |\n|---|---|\n"
                "| Report Style | audit |\n\n"
                "## Health Dashboard\n\n"
                "### Risk Map\n\nx\n\n"
                "**Legend**\n\n| Band | Score |\n|---|---|\n"
                "| Poor | 1-3 |\n| Average | 4-6 |\n"
                "| Good | 7-8 |\n| Excellent | 9-10 |\n\n"
                "### Scorecard Summary\n\nx\n\n"
                "### Team & Continuity\n\nx\n\n"
                "## Scope Exclusions\n\nx\n")
        self.assertEqual(self.validator.check_health_dashboard(text), [])

    def test_r5_fresh_audit_section_name_not_a_claim(self):
        lines = [
            "## Scope Exclusions",
            "",
            "No Changes Since Previous Audit section - fresh audit.",
        ]
        fences = [False] * len(lines)
        self.assertEqual(
            self.validator.check_fresh_audit_claims(lines, fences), []
        )
        comparative = ["Security improved since the previous audit."]
        fails = self.validator.check_fresh_audit_claims(comparative, [False])
        self.assertTrue(any("comparative claim" in f for f in fails), fails)


class TestRenderContract(unittest.TestCase):
    def setUp(self):
        self.renderer = load_script("render-contract.py")

    def test_dump_contract_exposes_canonical_enumerations(self):
        validator = load_script("validate-report.py")
        contract = validator.report_contract()
        self.assertEqual(
            contract["dimension_ids"],
            [validator.dimension_slug(n) for n in validator.SCORECARD_DIMENSIONS],
        )
        for key in (
            "scorecard_dimensions", "health_dashboard_markers", "doc_info",
            "run_state", "par_rows",
        ):
            self.assertIn(key, contract)
        self.assertEqual(contract["par_rows"], 33)
        self.assertNotIn("Audit Purpose", contract["doc_info"]["required"])
        self.assertIn("Audit Purpose", contract["doc_info"]["allowed"])

    def test_check_passes_on_checked_in_contract(self):
        rc = self.renderer.main(
            ["render-contract.py", "--check", "process/report-contract.md"]
        )
        self.assertEqual(rc, 0)

    def test_check_flags_stale_block(self):
        source = Path("process/report-contract.md").read_text(encoding="utf-8")
        stale = source.replace("`validation`", "`delivery`", 1)
        self.assertNotEqual(stale, source)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "report-contract.md"
            target.write_text(stale, encoding="utf-8")
            rc = self.renderer.main(["render-contract.py", "--check", str(target)])
        self.assertEqual(rc, 1)


class TestComputeHeadline(unittest.TestCase):
    """The scoring-policy-3 spec's E1-E12 worked examples, asserted verbatim."""

    def setUp(self):
        self.checker = load_script("check-model.py")

    def _dims(self, entries):
        dims = {}
        for ident, spec in entries.items():
            if isinstance(spec, dict):
                dims[ident] = {"applicable": True, **spec}
            else:
                dims[ident] = {"applicable": True, "eligible": True,
                               "score": spec, "lo": spec, "hi": spec}
        return dims

    def _ineligible(self):
        return {"eligible": False, "score": None, "lo": 1, "hi": 10}

    def _e2_dims(self):
        return self._dims({
            "functional_suitability": 8, "testability": 8, "security": 7,
            "operational_safety": 7, "design_soundness": 6, "code_quality": 6,
            "maintainability": 6, "dependency_health": 6, "deployability": 6,
            "scalability": 6, "observability": 6, "compliance": 6,
            "code_style": 5, "stack_alignment": 5, "structure": 5,
            "delivery_continuity": 4, "originality_licensing": 5,
            "skill_definition": 7,
        })

    def test_e1_product_only_not_ready(self):
        dims = self._dims({
            "functional_suitability": 6, "testability": 4, "security": 8,
            "operational_safety": 9, "design_soundness": 6, "code_quality": 7,
            "maintainability": 4, "dependency_health": 8, "scalability": 8,
            "observability": 7, "compliance": 8, "code_style": 9,
            "structure": 8, "stack_alignment": 8,
            "originality_licensing": 7,
        })
        result = self.checker.compute_headline(
            dims, 10, False, False, "NOT READY")
        product = result["product"]
        self.assertEqual(product["score"], 7.0)  # 202/29 = 6.9655
        self.assertIsNone(product["interval"])
        self.assertTrue(product["published"])
        self.assertEqual(product["eligible_weight"], 29)
        self.assertEqual(product["applicable_weight"], 29)
        self.assertEqual(
            product["lowest"], ["testability", "maintainability"])
        process = result["process"]
        self.assertTrue(process["published"])
        self.assertEqual(process["score"], 7.0)
        self.assertEqual(process["scored"], 1)
        self.assertEqual(process["applicable"], 1)
        self.assertEqual(process["lowest"], ["originality_licensing"])
        single = result["single"]
        self.assertEqual(single["raw"], 7.0)
        self.assertIsNone(single["flag"])
        self.assertEqual(
            single["ceiling"],
            {"limit": 6, "reasons": ["readiness:NOT READY"]})
        self.assertEqual(single["score"], 6.0)
        self.assertIsNone(single["interval"])
        self.assertEqual(single["band"], "Average")

    def test_e2_both_published_no_ceiling(self):
        result = self.checker.compute_headline(
            self._e2_dims(), 10, False, False, "READY")
        self.assertEqual(result["product"]["score"], 6.5)  # 201/31 = 6.4839
        self.assertEqual(result["process"]["score"], 5.3)  # 16/3 = 5.3333
        self.assertEqual(result["process"]["scored"], 3)
        self.assertEqual(result["process"]["applicable"], 3)
        self.assertEqual(
            result["process"]["lowest"], ["delivery_continuity"])
        single = result["single"]
        self.assertEqual(single["raw"], 6.1)
        self.assertEqual(single["score"], 6.1)
        self.assertIsNone(single["flag"])
        self.assertIsNone(single["ceiling"])
        self.assertEqual(single["band"], "Average")

    def test_e3_float_hazard(self):
        dims = self._e2_dims()
        for ident in ("delivery_continuity",
                      "originality_licensing", "skill_definition"):
            dims[ident] = {"applicable": True, "eligible": True,
                           "score": 5, "lo": 5, "hi": 5}
        result = self.checker.compute_headline(
            dims, 10, False, False, "READY")
        self.assertEqual(result["product"]["score"], 6.5)
        self.assertEqual(result["process"]["score"], 5.0)
        # 0.7 x 6.5 + 0.3 x 5.0 = 6.05 -> half-up 6.1; a float floor gives 6.0
        self.assertEqual(result["single"]["raw"], 6.1)
        self.assertEqual(result["single"]["score"], 6.1)

    def test_e4_open_high(self):
        result = self.checker.compute_headline(
            self._e2_dims(), 10, False, True, "READY")
        single = result["single"]
        self.assertEqual(single["raw"], 6.1)
        self.assertEqual(
            single["ceiling"], {"limit": 6, "reasons": ["severity:HIGH"]})
        self.assertEqual(single["score"], 6.0)
        self.assertEqual(single["band"], "Average")

    def test_e5_open_critical_and_high(self):
        result = self.checker.compute_headline(
            self._e2_dims(), 10, True, True, "NOT READY")
        single = result["single"]
        self.assertEqual(
            single["ceiling"],
            {"limit": 3, "reasons": ["severity:CRITICAL", "severity:HIGH",
                                     "readiness:NOT READY"]})
        self.assertEqual(single["score"], 3.0)
        self.assertEqual(single["band"], "Poor")

    def test_e6_core_dimension_ineligible(self):
        dims = self._e2_dims()
        dims["security"] = self._ineligible()
        result = self.checker.compute_headline(
            dims, 10, False, False, "READY")
        product = result["product"]
        self.assertFalse(product["published"])
        self.assertIsNone(product["score"])
        self.assertEqual(product["eligible_weight"], 28)
        self.assertEqual(product["applicable_weight"], 31)
        self.assertTrue(
            all(value is None for value in result["single"].values()))
        self.assertEqual(result["process"]["score"], 5.3)

    def test_e7_weight_floor(self):
        dims = self._dims({
            "functional_suitability": 8, "testability": 8, "security": 7,
            "operational_safety": 7,
        })
        for ident in ("design_soundness", "code_quality", "maintainability",
                      "dependency_health", "deployability", "scalability",
                      "observability", "compliance", "code_style",
                      "stack_alignment", "structure"):
            dims[ident] = self._ineligible()
        result = self.checker.compute_headline(
            dims, 10, False, False, "READY")
        # 12 * 2 = 24 is not more than 31
        self.assertFalse(result["product"]["published"])
        self.assertFalse(result["process"]["published"])
        self.assertEqual(result["process"]["applicable"], 0)
        self.assertTrue(
            all(value is None for value in result["single"].values()))

    def test_e8_process_floor_gives_product_only(self):
        dims = self._e2_dims()
        del dims["delivery_continuity"]
        del dims["skill_definition"]
        dims["originality_licensing"] = self._ineligible()
        result = self.checker.compute_headline(
            dims, 10, False, False, "READY")
        process = result["process"]
        self.assertFalse(process["published"])
        self.assertEqual(process["scored"], 0)
        self.assertEqual(process["applicable"], 1)
        single = result["single"]
        self.assertEqual(single["raw"], 6.5)
        self.assertEqual(single["flag"], "product-only")
        self.assertEqual(single["score"], 6.5)
        self.assertEqual(single["band"], "Good")

    def test_e9_scale_5(self):
        dims = self._dims({
            "functional_suitability": 4, "testability": 4, "security": 4,
            "operational_safety": 4, "design_soundness": 4, "code_quality": 4,
            "maintainability": 4, "dependency_health": 4, "deployability": 4,
            "scalability": 4, "observability": 4, "compliance": 4,
            "code_style": 5, "stack_alignment": 5, "structure": 5,
            "delivery_continuity": 3, "originality_licensing": 3,
            "skill_definition": 3,
        })
        result = self.checker.compute_headline(
            dims, 5, False, True, "READY")
        self.assertEqual(result["product"]["score"], 4.1)  # 127/31 = 4.0968
        self.assertEqual(result["process"]["score"], 3.0)
        single = result["single"]
        self.assertEqual(single["raw"], 3.8)  # hu1(3.77)
        self.assertEqual(
            single["ceiling"], {"limit": 3, "reasons": ["severity:HIGH"]})
        self.assertEqual(single["score"], 3.0)
        self.assertEqual(single["band"], "Average")

    def test_e10_intervals(self):
        dims = self._e2_dims()
        dims["observability"] = self._ineligible()
        result = self.checker.compute_headline(
            dims, 10, False, False, "READY")
        product = result["product"]
        self.assertEqual(product["score"], 6.5)  # 189/29 = 6.5172
        self.assertEqual(product["interval"], [6.2, 6.7])
        self.assertEqual(product["eligible_weight"], 29)
        self.assertEqual(product["applicable_weight"], 31)
        self.assertEqual(result["process"]["score"], 5.3)
        self.assertIsNone(result["process"]["interval"])
        single = result["single"]
        self.assertEqual(single["raw"], 6.1)
        self.assertEqual(single["interval"], [5.9, 6.3])
        self.assertEqual(single["score"], 6.1)
        self.assertEqual(single["band"], "Average")

    def test_e11_not_ready_both_published(self):
        dims = self._dims({
            "functional_suitability": 8, "testability": 7, "security": 8,
            "operational_safety": 7, "design_soundness": 7, "code_quality": 7,
            "maintainability": 7, "dependency_health": 7, "deployability": 7,
            "scalability": 7, "observability": 7, "compliance": 7,
            "code_style": 8, "stack_alignment": 8, "structure": 8,
            "delivery_continuity": 6, "originality_licensing": 7,
            "skill_definition": 7,
        })
        result = self.checker.compute_headline(
            dims, 10, False, False, "NOT READY")
        self.assertEqual(result["product"]["score"], 7.3)  # 226/31 = 7.2903
        self.assertEqual(result["process"]["score"], 6.7)  # 20/3 = 6.6667
        single = result["single"]
        self.assertEqual(single["raw"], 7.1)  # hu1(5.11 + 2.01 = 7.12)
        self.assertEqual(
            single["ceiling"],
            {"limit": 6, "reasons": ["readiness:NOT READY"]})
        self.assertEqual(single["score"], 6.0)

    def test_e12_dimension_intervals_propagate(self):
        dims = self._e2_dims()
        dims["testability"] = {"applicable": True, "eligible": True,
                               "score": 8, "lo": 6, "hi": 9}
        result = self.checker.compute_headline(
            dims, 10, False, False, "READY")
        product = result["product"]
        self.assertEqual(product["score"], 6.5)
        self.assertEqual(product["interval"], [6.3, 6.6])
        single = result["single"]
        self.assertEqual(single["interval"], [6.0, 6.2])
        self.assertEqual(single["raw"], 6.1)
        self.assertEqual(single["score"], 6.1)

    def test_e13_pending_evidence_ceiling(self):
        dims = self._dims({
            "functional_suitability": 8, "testability": 7, "security": 8,
            "operational_safety": 7, "design_soundness": 7, "code_quality": 7,
            "maintainability": 7, "dependency_health": 7, "deployability": 7,
            "scalability": 7, "observability": 7, "compliance": 7,
            "code_style": 8, "stack_alignment": 8, "structure": 8,
            "delivery_continuity": 6, "originality_licensing": 7,
            "skill_definition": 7,
        })
        result = self.checker.compute_headline(
            dims, 10, False, False, "PENDING EVIDENCE")
        self.assertEqual(result["product"]["score"], 7.3)
        single = result["single"]
        self.assertEqual(single["raw"], 7.1)
        self.assertEqual(
            single["ceiling"],
            {"limit": 6, "reasons": ["readiness:PENDING EVIDENCE"]})
        self.assertEqual(single["score"], 6.0)


class TestCheckModelPolicy3(unittest.TestCase):
    def setUp(self):
        self.checker = load_script("check-model.py")

    def _cat_entry(self, cid, dimension, weight=1.0, criticality="medium",
                   na_rules=None, mechanical=False):
        return {"id": cid, "dimension": dimension, "weight": weight,
                "criticality": criticality, "natures": ["*"],
                "na_rules": na_rules or [],
                "levels": {"PASS": "...", "P75": "...", "P50": "...",
                           "P25": "...", "FAIL": "..."},
                "mechanical": mechanical}

    def _catalogue(self, extra=()):
        return {
            "catalogue_version": 1, "scoring_policy": 3,
            "levels": {"PASS": 1.0, "P75": 0.75, "P50": 0.5,
                       "P25": 0.25, "FAIL": 0.0},
            "dimensions": [],
            "criteria": [
                self._cat_entry("FNC-REQ", "functional_suitability", weight=3,
                                criticality="critical", mechanical=True,
                                na_rules=["deployment-model"]),
                self._cat_entry("SEC-AUTHZ", "security", criticality="high"),
                self._cat_entry("SEC-INJ", "security", criticality="high"),
                self._cat_entry("SEC-CRYPTO", "security"),
                self._cat_entry("CMP-API", "api_compatibility",
                                criticality="low",
                                na_rules=["deployment-model"]),
                *extra,
            ],
            "severity_anchors": [],
        }

    def _criteria_entry(self, cid, dimension, outcome, **extra):
        entry = {"id": cid, "catalogue_id": cid, "channel": "score",
                     "source": "catalogue", "applicability": "applicable",
                     "criticality": "medium", "weight": 1.0, "expected": "...",
                     "method": "...", "sufficiency": "...",
                     "dimension": dimension, "outcome": outcome,
                     "level": None, "mastery": None}
        entry.update(extra)
        return entry

    def _valid_model(self):
        return {
            "model_version": 2,
            "scope": {"subject": "demo", "revision": "abc123",
                      "purpose": "audit", "evidence_mode": "source-only",
                      "scoring_policy": 3, "catalogue_version": 1,
                      "history": "present", "detail_level": "Standard",
                      "requirements_baseline": None,
                      "projects": [{"path": ".",
                                    "automation_census": "signals"}],
                      "product_profile": {"natures": ["service"]}},
            "inventory": [],
            "criteria": [
                self._criteria_entry(
                    "FNC-REQ", "functional_suitability", "NOT_APPLICABLE",
                    criticality="critical", weight=3,
                    na_basis="deployment-model",
                    applicability=(
                        "no mandatory requirements declared or advertised")),
                self._criteria_entry("SEC-AUTHZ", "security", "PASS",
                                criticality="high", level="PASS",
                                mastery=1.0),
                self._criteria_entry("SEC-INJ", "security", "PARTIAL",
                                criticality="high", level="P25",
                                mastery=0.25),
                self._criteria_entry("SEC-CRYPTO", "security", "UNKNOWN"),
                self._criteria_entry(
                    "CMP-API", "api_compatibility", "NOT_APPLICABLE",
                    criticality="low", na_basis="deployment-model",
                    applicability="not a published library"),
            ],
            "requirements": [],
            "evidence": [
                {"id": "EVD-001", "kind": "INSPECTED", "collector": "x",
                 "method": "read", "timestamp": "...", "tool": None,
                 "locator": {"path": "src/app.py", "lines": [1, 40]},
                 "procedure": None, "result": "...",
                 "claims": ["SEC-AUTHZ", "SEC-INJ"], "limits": "...",
                 "sampling": "full", "counter": "...", "redaction": "none",
                 "unavailable": None},
                {"id": "EVD-002", "kind": "INSPECTED", "collector": "x",
                 "method": "read", "timestamp": "...", "tool": None,
                 "locator": {"path": "src/db.py", "lines": [1, 20]},
                 "procedure": None, "result": "...",
                 "claims": ["SEC-INJ"], "limits": "...",
                 "sampling": "full", "counter": "...", "redaction": "none",
                 "unavailable": None},
            ],
            "findings": [
                {"id": "FND-SEC-001", "criteria": "SEC-INJ",
                 "type": "Concern", "severity": "HIGH",
                 "claim_class": "confirmed defect", "observation": "...",
                 "property": "...", "evidence": ["EVD-002"],
                 "counter": "checked alternate injection paths",
                 "consequence": "...", "scope": "...", "confidence": "HIGH",
                 "status": "Open", "next_verification": "..."},
            ],
            "risks": [], "recommendations": [],
            "readiness": {"state": "PENDING EVIDENCE",
                          "blocking": ["FND-SEC-001"]},
            "scores": {
                "scale_max": 10,
                "dimensions": {
                    "security": {"mastery": 0.625, "uncapped": 6, "score": 5,
                                 "interval": [4, 5], "coverage": 0.67,
                                 "eligible": True,
                                 "caps": [{"rule": "severity-high", "limit": 5,
                                           "source": ["FND-SEC-001"]}]},
                },
                "product": {"score": 5.0, "interval": [4.0, 5.0],
                            "published": True, "eligible_weight": 3,
                            "applicable_weight": 3, "lowest": ["security"]},
                "process": {"score": None, "interval": None,
                            "published": False, "scored": 0,
                            "applicable": 0, "lowest": []},
                "single": {"score": 5.0, "raw": 5.0, "interval": [4.0, 5.0],
                           "flag": "product-only",
                           "ceiling": {"limit": 6,
                                       "reasons": ["severity:HIGH",
                                                   "readiness:PENDING EVIDENCE"]},
                           "band": "Average"},
            },
            "coverage": {}, "exclusions": [],
        }

    def check(self, model, catalogue=None):
        return self.checker.check_model(
            model, self._catalogue() if catalogue is None else catalogue)

    def test_valid_model_passes(self):
        self.assertEqual(self.check(self._valid_model()), [])

    def test_model_v2_shape_rules(self):
        model = self._valid_model()
        model["model_version"] = 1
        failures = self.check(model)
        self.assertIn("model_version is 1, expected 2", failures)

        model = self._valid_model()
        model["scope"]["scoring_policy"] = 2
        failures = self.check(model)
        self.assertIn("scope.scoring_policy is 2, expected 3", failures)

        model = self._valid_model()
        model["scope"]["catalogue_version"] = 9
        failures = self.check(model)
        self.assertIn(
            "scope.catalogue_version 9 does not match catalogue version 1",
            failures)

        model = self._valid_model()
        del model["scope"]["detail_level"]
        failures = self.check(model)
        self.assertIn(
            "scope.detail_level None is not Detailed, Standard, or Brief",
            failures)

        model = self._valid_model()
        model["scope"]["product_profile"] = {}
        failures = self.check(model)
        self.assertIn("scope.product_profile.natures is required", failures)
        model["scope"]["product_profile"] = {"natures": ["service", "qubit"]}
        failures = self.check(model)
        self.assertIn(
            "scope.product_profile.natures entry 'qubit' is not a declared "
            "project nature",
            failures)

        model = self._valid_model()
        model["scores"]["overall"] = {"score": 5.0}
        failures = self.check(model)
        self.assertIn(
            "scores.overall is removed in model v2 - record product, "
            "process, and single",
            failures)

    def test_missing_catalogue_reports_once_and_other_checks_run(self):
        original = self.checker.load_catalogue
        self.checker.load_catalogue = lambda: None
        try:
            model = self._valid_model()
            model["scores"]["product"]["score"] = 9.9
            failures = self.checker.check_model(model)
        finally:
            self.checker.load_catalogue = original
        missing = "catalogue file references/criteria-catalogue.json is missing"
        self.assertIn(missing, failures)
        self.assertEqual(failures.count(missing), 1)
        self.assertIn("product.score 9.9 does not recompute to 5.0", failures)

    def test_c1_membership(self):
        model = self._valid_model()
        model["criteria"][0]["catalogue_id"] = "FNC-NOPE"
        failures = self.check(model)
        self.assertIn(
            "FNC-REQ: catalogue_id 'FNC-NOPE' is not in catalogue version 1",
            failures)

        model = self._valid_model()
        model["criteria"][1]["weight"] = 2
        failures = self.check(model)
        self.assertIn(
            "SEC-AUTHZ: weight 2 differs from the catalogue value 1.0",
            failures)

    def test_c1_id_equals_catalogue_id_single_project(self):
        model = self._valid_model()
        model["criteria"][1]["id"] = "SEC-AUTHZ-01"
        failures = self.check(model)
        self.assertIn(
            "SEC-AUTHZ-01: id must equal catalogue_id 'SEC-AUTHZ' in a "
            "single-project model",
            failures)

    def test_c2_completeness(self):
        model = self._valid_model()
        del model["criteria"][3]
        failures = self.check(model)
        self.assertIn(
            "subject: catalogue criteria SEC-CRYPTO is missing from the model",
            failures)

        model = self._valid_model()
        model["criteria"].append(
            self._criteria_entry("SEC-DUP", "security", "PASS", level="PASS",
                            mastery=1.0, catalogue_id="SEC-AUTHZ",
                            criticality="high"))
        failures = self.check(model)
        self.assertIn(
            "subject: catalogue criteria SEC-AUTHZ appears 2 times", failures)

    def test_c3_level_outcome_mastery(self):
        model = self._valid_model()
        model["criteria"][1]["level"] = "P50"
        failures = self.check(model)
        self.assertIn(
            "SEC-AUTHZ: level P50 does not match outcome PASS", failures)

        model = self._valid_model()
        model["criteria"][1]["level"] = "BAD"
        failures = self.check(model)
        self.assertIn(
            "SEC-AUTHZ: level 'BAD' is not allowed by the catalogue", failures)

        model = self._valid_model()
        model["criteria"][2]["mastery"] = 0.5
        failures = self.check(model)
        self.assertIn(
            "SEC-INJ: mastery 0.5 does not equal level P25 value 0.25",
            failures)

        model = self._valid_model()
        model["criteria"][3]["level"] = "PASS"
        failures = self.check(model)
        self.assertIn(
            "SEC-CRYPTO: level PASS does not match outcome UNKNOWN", failures)

    def test_c4_na_basis_declared_rules_only(self):
        model = self._valid_model()
        model["criteria"][4]["na_basis"] = "census-none"
        failures = self.check(model)
        self.assertIn(
            "CMP-API: na_basis census-none is not a declared N/A rule for "
            "this criteria entry",
            failures)

    def test_c5_census_determinism(self):
        catalogue = self._catalogue([
            self._cat_entry("DEP-CI", "deployability",
                            na_rules=["census-none", "deployment-model"]),
        ])
        model = self._valid_model()
        model["scope"]["projects"][0]["automation_census"] = "none"
        model["criteria"].append(
            self._criteria_entry("DEP-CI", "deployability", "NOT_APPLICABLE",
                            na_basis="deployment-model",
                            applicability="no deployable target"))
        failures = self.check(model, catalogue)
        self.assertIn(
            "DEP-CI: automation census none makes this criteria entry "
            "NOT_APPLICABLE (census-none)",
            failures)
        model["criteria"][-1]["na_basis"] = "census-none"
        joined = "\n".join(self.check(model, catalogue))
        self.assertNotIn("makes this criteria entry NOT_APPLICABLE", joined)

    def test_c6_history_determinism(self):
        catalogue = self._catalogue([
            self._cat_entry("DLY-HIST", "delivery_continuity",
                            na_rules=["history-out-of-scope",
                                      "deployment-model"]),
        ])
        model = self._valid_model()
        model["scope"]["history"] = "absent"
        model["criteria"].append(
            self._criteria_entry("DLY-HIST", "delivery_continuity",
                            "NOT_APPLICABLE", na_basis="deployment-model",
                            applicability="not applicable"))
        failures = self.check(model, catalogue)
        self.assertIn(
            "DLY-HIST: scope.history absent makes this criteria entry "
            "NOT_APPLICABLE (history-out-of-scope)",
            failures)

    def test_c7_conformance_channel_prefix(self):
        model = self._valid_model()
        model["criteria"].append(
            self._criteria_entry("SKL-DEPS", "skill_definition", "PASS",
                            channel="conformance"))
        failures = self.check(model)
        self.assertIn(
            "SKL-DEPS: conformance criteria use the CNF- or REQ- prefix",
            failures)

        model = self._valid_model()
        model["criteria"].append(
            self._criteria_entry("CNF-STYLE", "skill_definition", "PASS",
                            channel="conformance"))
        failures = self.check(model)
        self.assertFalse(
            [f for f in failures if f.startswith("CNF-STYLE")], failures)

    def test_c8_requirements_registry(self):
        model = self._valid_model()
        model["requirements"] = [
            {"id": "A-01", "obligation": "optional", "status": "PASS",
             "evidence": ["EVD-001"], "finding": None, "statement": "x",
             "source": {"path": "docs/X.md", "line": 1}},
        ]
        digest = hashlib.sha256(b"A-01:optional").hexdigest()
        model["scope"]["requirements_baseline"] = digest
        self.assertEqual(self.check(model), [])

        model["scope"]["requirements_baseline"] = "0" * 64
        joined = "\n".join(self.check(model))
        self.assertIn(
            "requirements_baseline does not match the requirements registry",
            joined)

        model["scope"]["requirements_baseline"] = digest
        model["requirements"] = []
        joined = "\n".join(self.check(model))
        self.assertIn(
            "requirements_baseline does not match the requirements registry",
            joined)

        model["requirements"] = [
            {"id": "A-01", "obligation": "must", "status": "PASS",
             "evidence": [], "finding": None, "statement": "x",
             "source": {"path": "docs/X.md", "line": 1}},
        ]
        joined = "\n".join(self.check(model))
        self.assertIn("A-01: obligation 'must' is invalid", joined)

        model["requirements"][0]["obligation"] = "mandatory"
        model["requirements"][0]["status"] = "FAIL"
        joined = "\n".join(self.check(model))
        self.assertIn("A-01: FAIL requirement needs an open finding", joined)

        model["requirements"][0]["status"] = "PASS"
        model["requirements"][0]["evidence"] = ["EVD-999"]
        joined = "\n".join(self.check(model))
        self.assertIn("A-01: cites unknown evidence EVD-999", joined)

        model["requirements"].append(
            {"id": "A-01", "obligation": "mandatory", "status": "PASS",
             "evidence": [], "finding": None, "statement": "x",
             "source": {"path": "docs/X.md", "line": 2}})
        joined = "\n".join(self.check(model))
        self.assertIn("A-01: id 'A-01' is invalid", joined)

    def test_c9_fnc_req_mechanical_derivation(self):
        model = copy.deepcopy(self._valid_model())
        model["criteria"][0].update(
            {"outcome": "PARTIAL", "level": "P50", "mastery": 0.5,
             "na_basis": None, "applicability": "applicable"})
        model["requirements"] = [
            {"id": "A-01", "obligation": "mandatory", "status": "PASS",
             "evidence": ["EVD-001"], "finding": None, "statement": "x",
             "source": {"path": "docs/X.md", "line": 1}},
            {"id": "A-02", "obligation": "mandatory", "status": "PARTIAL",
             "evidence": ["EVD-001"], "finding": "FND-REQ-001",
             "statement": "y", "source": {"path": "docs/X.md", "line": 2}},
        ]
        model["scope"]["requirements_baseline"] = hashlib.sha256(
            b"A-01:mandatory\nA-02:mandatory").hexdigest()
        model["evidence"][0]["claims"].append("FNC-REQ")
        model["findings"].append(
            {"id": "FND-REQ-001", "criteria": "FNC-REQ", "type": "Concern",
             "severity": "LOW", "claim_class": "evidence gap",
             "observation": "...", "property": "...", "evidence": ["EVD-001"],
             "counter": None, "consequence": "...", "scope": "...",
             "confidence": "LOW", "status": "Open",
             "next_verification": "..."})
        model["scores"]["dimensions"]["functional_suitability"] = {
            "mastery": 0.5, "uncapped": 5, "score": 5, "coverage": 1.0,
            "eligible": True}
        model["scores"]["product"] = {
            "score": 5.0, "interval": [4.5, 5.0], "published": True,
            "eligible_weight": 6, "applicable_weight": 6,
            "lowest": ["functional_suitability", "security"]}
        model["scores"]["single"] = {
            "score": 5.0, "raw": 5.0, "interval": [4.5, 5.0],
            "flag": "product-only",
            "ceiling": {"limit": 6, "reasons": ["severity:HIGH",
                                                "readiness:PENDING EVIDENCE"]},
            "band": "Average"}
        self.assertEqual(self.check(model), [])
        model["criteria"][0]["level"] = "PASS"
        joined = "\n".join(self.check(model))
        self.assertIn(
            "FNC-REQ: level 'PASS' does not match the computed P50 "
            "(coverage 0.750 over 2 of 2 mandatory requirements)",
            joined)

    def test_c9_zero_mandatory_is_not_applicable(self):
        model = self._valid_model()
        model["criteria"][0].update(
            {"outcome": "UNKNOWN", "level": None, "na_basis": None,
             "applicability": "applicable"})
        joined = "\n".join(self.check(model))
        self.assertIn(
            "FNC-REQ: level None does not match the computed NOT_APPLICABLE "
            "(coverage 0.000 over 0 of 0 mandatory requirements)",
            joined)

    def test_c9_unknown_band(self):
        model = self._valid_model()
        model["requirements"] = [
            {"id": "A-01", "obligation": "mandatory", "status": "PASS",
             "evidence": ["EVD-001"], "finding": None, "statement": "x",
             "source": {"path": "docs/X.md", "line": 1}},
            {"id": "A-02", "obligation": "mandatory", "status": "UNKNOWN",
             "evidence": [], "finding": None, "statement": "y",
             "source": {"path": "docs/X.md", "line": 2}},
        ]
        model["scope"]["requirements_baseline"] = hashlib.sha256(
            b"A-01:mandatory\nA-02:mandatory").hexdigest()
        joined = "\n".join(self.check(model))
        # g = 1, n = 2: 1 * 2 <= 2 -> UNKNOWN
        self.assertIn(
            "FNC-REQ: level None does not match the computed UNKNOWN "
            "(coverage 1.000 over 1 of 2 mandatory requirements)",
            joined)

    def test_c10_headline_records_recompute(self):
        model = self._valid_model()
        model["scores"]["product"]["score"] = 9.9
        failures = self.check(model)
        self.assertIn("product.score 9.9 does not recompute to 5.0", failures)

        model = self._valid_model()
        model["scores"]["single"]["flag"] = "both"
        failures = self.check(model)
        self.assertIn(
            "single.flag 'both' does not recompute to 'product-only'",
            failures)

        model = self._valid_model()
        model["scores"]["product"]["lowest"] = ["testability"]
        failures = self.check(model)
        self.assertIn(
            "product.lowest ['testability'] does not recompute to "
            "['security']",
            failures)

    def test_c11_readiness_states(self):
        model = self._valid_model()
        model["readiness"] = {"state": "BOGUS", "blocking": []}
        failures = self.check(model)
        self.assertIn(
            "readiness.state 'BOGUS' is not a readiness state", failures)

        model = self._valid_model()
        model["readiness"] = {"state": "READY", "blocking": []}
        failures = self.check(model)
        self.assertIn(
            "readiness READY conflicts with open HIGH finding FND-SEC-001",
            failures)

        model = self._valid_model()
        model["readiness"] = {"state": "NOT READY", "blocking": []}
        failures = self.check(model)
        self.assertIn(
            "readiness NOT READY needs at least one blocking id", failures)

        model = self._valid_model()
        model["readiness"] = {"state": "PENDING EVIDENCE",
                              "blocking": ["FND-NOPE"]}
        failures = self.check(model)
        self.assertIn("readiness.blocking cites unknown FND-NOPE", failures)

        model = self._valid_model()
        model["scope"]["purpose"] = "readiness review"
        model["readiness"] = {"state": "NOT ASSESSED", "blocking": []}
        failures = self.check(model)
        self.assertIn(
            "readiness NOT ASSESSED conflicts with a readiness purpose",
            failures)

    def test_cli_missing_catalogue_exits_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "model.json"
            path.write_text(json.dumps(self._valid_model()),
                            encoding="utf-8")
            original = self.checker.load_catalogue
            self.checker.load_catalogue = lambda: None
            out = io.StringIO()
            try:
                with contextlib.redirect_stdout(out):
                    rc = self.checker.main([str(path), "--json"])
            finally:
                self.checker.load_catalogue = original
        self.assertEqual(rc, 1)
        failures = json.loads(out.getvalue())["failures"]
        self.assertIn(
            "catalogue file references/criteria-catalogue.json is missing",
            failures)


class TestExtractRequirements(unittest.TestCase):
    FIXTURE = (
        "# Requirements\n\n"
        "| ID   | Requirement                     | Note  |\n"
        "|------|---------------------------------|-------|\n"
        "| A-01 | The service SHALL restart in 5s | core  |\n"
        "| A-02 | proposed cache layer for reads  | row   |\n"
        "| F-01 | deferred export to CSV          | later |\n\n"
        "### N-01 Latency budget\n\n"
        "- N-02: list-defined item\n\n"
        "A-03 is mentioned only in prose.\n"
    )

    def setUp(self):
        self.extractor = load_script("extract-requirements.py")

    def _run_json(self, args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = self.extractor.main(args)
        return rc, out.getvalue()

    def test_ids_hints_and_referenced_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "doc.md"
            path.write_text(self.FIXTURE, encoding="utf-8")
            rc, raw = self._run_json([str(path), "--json"])
        self.assertEqual(rc, 0)
        result = json.loads(raw)
        self.assertEqual(
            [r["id"] for r in result["requirements"]],
            ["A-01", "A-02", "F-01", "N-01", "N-02"])
        self.assertEqual(
            [r["obligation_hint"] for r in result["requirements"]],
            ["mandatory", "optional", "future", "mandatory", "mandatory"])
        self.assertEqual(result["referenced_only"], ["A-03"])
        self.assertEqual(result["documents"], [str(path)])
        self.assertEqual(result["pattern"], self.extractor.DEFAULT_PATTERN)

    def test_first_defining_location_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "one.md"
            second = Path(tmp) / "two.md"
            first.write_text("| B-01 | first definition |\n|---|\n",
                             encoding="utf-8")
            second.write_text("### B-01 second definition\n",
                              encoding="utf-8")
            rc, raw = self._run_json(
                [str(first), str(second), "--json"])
        self.assertEqual(rc, 0)
        record = json.loads(raw)["requirements"][0]
        self.assertEqual(record["id"], "B-01")
        self.assertEqual(record["path"], str(first))
        self.assertEqual(record["line"], 1)
        self.assertEqual(record["occurrences"], 2)

    def test_custom_pattern_and_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "doc.md"
            path.write_text("### WIDGET-9 Widget requirement\n",
                            encoding="utf-8")
            rc, raw = self._run_json(
                [str(path), "--pattern", r"WIDGET-\d+", "--json"])
            self.assertEqual(rc, 0)
            self.assertEqual(
                [r["id"] for r in json.loads(raw)["requirements"]],
                ["WIDGET-9"])
            rc, _ = self._run_json([str(Path(tmp) / "none.md")])
            self.assertEqual(rc, 2)


class TestRenderTables(unittest.TestCase):
    def setUp(self):
        self.renderer = load_script("render-tables.py")

    def _model(self):
        return {
            "model_version": 2,
            "scope": {"projects": [{"path": "."}],
                      "product_profile": {"natures": ["service"]}},
            "criteria": [
                {"id": "SEC-INJ", "catalogue_id": "SEC-INJ",
                 "channel": "score", "dimension": "security", "weight": 2,
                 "level": "P50", "outcome": "PARTIAL"},
                {"id": "SEC-AUTHZ", "catalogue_id": "SEC-AUTHZ",
                 "channel": "score", "dimension": "security", "weight": 1,
                 "level": "PASS", "outcome": "PASS"},
                {"id": "CNF-STYLE", "catalogue_id": None,
                 "channel": "conformance", "dimension": "skill_definition",
                 "weight": 1, "level": None, "outcome": "PASS"},
            ],
            "requirements": [
                {"id": "A-01", "obligation": "mandatory", "status": "PASS",
                 "evidence": ["EVD-001"]},
                {"id": "A-02", "obligation": "recommended",
                 "status": "UNKNOWN", "evidence": []},
            ],
            "scores": {
                "scale_max": 10,
                "dimensions": {
                    "testability": {"score": None, "eligible": False,
                                    "note": "coverage too thin"},
                    "design_soundness": {"score": 7},
                    "security": {"score": 5, "interval": [4, 5]},
                },
                "product": {"score": 5.0, "interval": [4.0, 5.0],
                            "published": True, "eligible_weight": 3,
                            "applicable_weight": 3, "lowest": ["security"]},
                "process": {"score": None, "interval": None,
                            "published": False, "scored": 1,
                            "applicable": 2, "lowest": []},
                "single": {"score": 5.0, "raw": 5.0, "interval": [4.0, 5.0],
                           "flag": "product-only",
                           "ceiling": {"limit": 6,
                                       "reasons": ["severity:HIGH",
                                                   "readiness:PENDING EVIDENCE"]},
                           "band": "Average"},
            },
        }

    def test_scorecard_canonical_order_unknown_and_na_omitted(self):
        text = self.renderer.render_scorecard(self._model(), None)
        lines = text.splitlines()
        self.assertTrue(lines[0].startswith("| Dimension"))
        names = [
            line.split("|")[1].strip()
            for line in lines[2:]
            if line.startswith("|")
        ]
        self.assertEqual(
            names, ["Testability", "Design Soundness", "Security"])
        self.assertIn("Unknown", text)
        self.assertIn("| Security  | 5/10/10" if False else "5/10", text)
        self.assertNotIn("[4-5]", text.split("## ")[0])
        self.assertIn("7/10", text)
        self.assertIn("coverage too thin", text)
        self.assertNotIn("Functional Suitability", text)

    def test_splice_replaces_table_and_fills_titles(self):
        report = (
            "## Technical Findings\n\n"
            "| Finding | Result |\n|---|---|\n| FND-SEC-001 | old |\n\n"
            "### FND-SEC-001 Injection sink\n\nbody\n"
        )
        titles = self.renderer.block_titles(report)
        self.assertEqual(titles["FND-SEC-001"], "Injection sink")
        table = self.renderer.fill_titles(
            "| Finding | Result |\n|---|---|\n| FND-SEC-001 | <title> |",
            titles,
        )
        self.assertIn("Injection sink", table)
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "r.md"
            path.write_text(report, encoding="utf-8")
            changed = self.renderer.splice_table(
                path,
                r"^## Technical Findings[^\n]*$",
                "| Finding | Result |\n|---|---|\n| FND-SEC-001 | <title> |",
            )
            self.assertTrue(changed)
            self.assertIn("Injection sink", path.read_text())

    def test_evidence_uniform_tag_omits_type(self):
        model = {"evidence": [
            {"id": "EVD-001", "locator": {"path": "a"}, "result": "r1",
             "type": "Observation"},
            {"id": "EVD-002", "locator": {"path": "b"}, "result": "r2",
             "type": "Observation"},
        ]}
        text = self.renderer.render_evidence(model, None)
        self.assertNotIn("Type", text)
        self.assertTrue(text.splitlines()[0].startswith("| Evidence"))

    def test_evidence_mixed_tag_keeps_type(self):
        model = {"evidence": [
            {"id": "EVD-001", "locator": {"path": "a"}, "result": "r1",
             "type": "Observation"},
            {"id": "EVD-002", "locator": {"path": "b"}, "result": "r2",
             "type": "Concern"},
        ]}
        text = self.renderer.render_evidence(model, None)
        self.assertIn("| Type", text)
        self.assertIn("Concern", text)

    def test_headline_rows(self):
        text = self.renderer.render_headline(self._model(), None)
        lines = text.splitlines()
        self.assertTrue(lines[0].startswith("| Score"))
        self.assertIn("| Product Quality", text)
        self.assertIn("5.0/10 (Average)", text)
        self.assertIn("[4-5]", text)
        self.assertIn("Tier-weighted mean of 3 product dimensions", text)
        self.assertIn("lowest Security 5/10", text)
        self.assertIn("| Engineering Process | Not published", text)
        self.assertIn("1 of 2 applicable process dimensions scored", text)
        self.assertNotIn("| Overall Score", text)
        self.assertIn("Product-only", text)
        self.assertIn("ceiling 6: severity HIGH", text)

    def test_criteria_table_catalogue_order(self):
        catalogue = {
            "criteria": [
                {"id": "SEC-AUTHZ"}, {"id": "SEC-INJ"},
            ]
        }
        text = self.renderer.render_criteria(
            self._model(), None, catalogue)
        lines = text.splitlines()
        self.assertTrue(lines[0].startswith("| Criteria"))
        self.assertIn("| Dimension", lines[0])
        self.assertIn("| Weight", lines[0])
        self.assertIn("| Level", lines[0])
        self.assertIn("| Outcome", lines[0])
        ids = [line.split("|")[1].strip() for line in lines[2:]]
        self.assertEqual(ids, ["SEC-AUTHZ", "SEC-INJ"])
        self.assertNotIn("CNF-STYLE", text)

    def test_requirements_table(self):
        text = self.renderer.render_requirements(self._model(), None)
        lines = text.splitlines()
        self.assertTrue(lines[0].startswith("| Requirement"))
        self.assertIn("| Obligation", lines[0])
        self.assertIn("| Status", lines[0])
        self.assertIn("| Evidence", lines[0])
        ids = [line.split("|")[1].strip() for line in lines[2:]]
        self.assertEqual(ids, ["A-01", "A-02"])
        self.assertIn("EVD-001", text)

    def test_cli_all_and_output_and_lang_fallback(self):
        model = self._model()
        with tempfile.TemporaryDirectory() as tmp:
            model_path = Path(tmp) / "model.json"
            model_path.write_text(json.dumps(model), encoding="utf-8")
            out_path = Path(tmp) / "tables.md"
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                rc = self.renderer.main(
                    [str(model_path), "--part", "all", "--lang", "pl",
                     "--output", str(out_path)])
            self.assertEqual(rc, 0)
            self.assertIn("--lang pl", err.getvalue())
            text = out_path.read_text(encoding="utf-8")
            for marker in ("| Dimension", "| Score", "| Criteria",
                           "| Requirement"):
                self.assertIn(marker, text)
            rc = self.renderer.main(
                [str(model_path), "--part", "all", "--project", "ghost"])
            self.assertEqual(rc, 2)


class TestCompareModels(unittest.TestCase):
    def setUp(self):
        self.comparator = load_script("compare-models.py")
        self.checker = load_script("check-model.py")

    def _cat_entry(self, cid, dimension, weight=1.0, criticality="medium",
                   na_rules=None, mechanical=False):
        return {"id": cid, "dimension": dimension, "weight": weight,
                "criticality": criticality, "natures": ["*"],
                "na_rules": na_rules or [],
                "levels": {"PASS": "...", "P75": "...", "P50": "...",
                           "P25": "...", "FAIL": "..."},
                "mechanical": mechanical}

    def _catalogue(self, extra=()):
        return {
            "catalogue_version": 1, "scoring_policy": 3,
            "levels": {"PASS": 1.0, "P75": 0.75, "P50": 0.5,
                       "P25": 0.25, "FAIL": 0.0},
            "dimensions": [],
            "criteria": [
                self._cat_entry("FNC-REQ", "functional_suitability", weight=3,
                                criticality="critical", mechanical=True,
                                na_rules=["deployment-model"]),
                self._cat_entry("SEC-AUTHZ", "security", criticality="high"),
                self._cat_entry("SEC-INJ", "security", criticality="high"),
                self._cat_entry("SEC-CRYPTO", "security"),
                self._cat_entry("CMP-API", "api_compatibility",
                                criticality="low",
                                na_rules=["deployment-model"]),
                *extra,
            ],
            "severity_anchors": [],
        }

    def _small_catalogue(self):
        return {
            "catalogue_version": 1, "scoring_policy": 3,
            "levels": {"PASS": 1.0, "P75": 0.75, "P50": 0.5,
                       "P25": 0.25, "FAIL": 0.0},
            "dimensions": [],
            "criteria": [
                self._cat_entry("SEC-AUTHZ", "security", criticality="high"),
            ],
            "severity_anchors": [],
        }

    def _criteria_entry(self, cid, dimension, outcome, **extra):
        entry = {"id": cid, "catalogue_id": cid, "channel": "score",
                     "source": "catalogue", "applicability": "applicable",
                     "criticality": "medium", "weight": 1.0, "expected": "...",
                     "method": "...", "sufficiency": "...",
                     "dimension": dimension, "outcome": outcome,
                     "level": None, "mastery": None}
        entry.update(extra)
        return entry

    def _valid_model(self):
        return {
            "model_version": 2,
            "scope": {"subject": "demo", "revision": "abc123",
                      "purpose": "audit", "evidence_mode": "source-only",
                      "scoring_policy": 3, "catalogue_version": 1,
                      "history": "present", "detail_level": "Standard",
                      "requirements_baseline": None,
                      "projects": [{"path": ".",
                                    "automation_census": "signals"}],
                      "product_profile": {"natures": ["service"]}},
            "inventory": [],
            "criteria": [
                self._criteria_entry(
                    "FNC-REQ", "functional_suitability", "NOT_APPLICABLE",
                    criticality="critical", weight=3,
                    na_basis="deployment-model",
                    applicability=(
                        "no mandatory requirements declared or advertised")),
                self._criteria_entry("SEC-AUTHZ", "security", "PASS",
                                criticality="high", level="PASS",
                                mastery=1.0),
                self._criteria_entry("SEC-INJ", "security", "PARTIAL",
                                criticality="high", level="P25",
                                mastery=0.25),
                self._criteria_entry("SEC-CRYPTO", "security", "UNKNOWN"),
                self._criteria_entry(
                    "CMP-API", "api_compatibility", "NOT_APPLICABLE",
                    criticality="low", na_basis="deployment-model",
                    applicability="not a published library"),
            ],
            "requirements": [],
            "evidence": [
                {"id": "EVD-001", "kind": "INSPECTED", "collector": "x",
                 "method": "read", "timestamp": "...", "tool": None,
                 "locator": {"path": "src/app.py", "lines": [1, 40]},
                 "procedure": None, "result": "...",
                 "claims": ["SEC-AUTHZ", "SEC-INJ"], "limits": "...",
                 "sampling": "full", "counter": "...", "redaction": "none",
                 "unavailable": None},
                {"id": "EVD-002", "kind": "INSPECTED", "collector": "x",
                 "method": "read", "timestamp": "...", "tool": None,
                 "locator": {"path": "src/db.py", "lines": [1, 20]},
                 "procedure": None, "result": "...",
                 "claims": ["SEC-INJ"], "limits": "...",
                 "sampling": "full", "counter": "...", "redaction": "none",
                 "unavailable": None},
            ],
            "findings": [
                {"id": "FND-SEC-001", "criteria": "SEC-INJ",
                 "type": "Concern", "severity": "HIGH",
                 "claim_class": "confirmed defect", "observation": "...",
                 "property": "...", "evidence": ["EVD-002"],
                 "counter": "checked alternate injection paths",
                 "consequence": "...", "scope": "...", "confidence": "HIGH",
                 "status": "Open", "next_verification": "..."},
            ],
            "risks": [], "recommendations": [],
            "readiness": {"state": "PENDING EVIDENCE",
                          "blocking": ["FND-SEC-001"]},
            "scores": {
                "scale_max": 10,
                "dimensions": {
                    "security": {"mastery": 0.625, "uncapped": 6, "score": 5,
                                 "interval": [4, 5], "coverage": 0.67,
                                 "eligible": True,
                                 "caps": [{"rule": "severity-high", "limit": 5,
                                           "source": ["FND-SEC-001"]}]},
                },
                "product": {"score": 5.0, "interval": [4.0, 5.0],
                            "published": True, "eligible_weight": 3,
                            "applicable_weight": 3, "lowest": ["security"]},
                "process": {"score": None, "interval": None,
                            "published": False, "scored": 0,
                            "applicable": 0, "lowest": []},
                "single": {"score": 5.0, "raw": 5.0, "interval": [4.0, 5.0],
                           "flag": "product-only",
                           "ceiling": {"limit": 6,
                                       "reasons": ["severity:HIGH",
                                                   "readiness:PENDING EVIDENCE"]},
                           "band": "Average"},
            },
            "coverage": {}, "exclusions": [],
        }

    def _process_catalogue(self):
        return self._catalogue([
            self._cat_entry("DLY-OPS", "delivery_continuity",
                            na_rules=["deployment-model"]),
        ])

    def _with_na_dly(self, model):
        model = copy.deepcopy(model)
        model["criteria"].append(
            self._criteria_entry(
                "DLY-OPS", "delivery_continuity", "NOT_APPLICABLE",
                na_basis="deployment-model",
                applicability="no delivery process in scope"))
        return model

    def _with_process(self, model):
        model = copy.deepcopy(model)
        model["criteria"].append(
            self._criteria_entry("DLY-OPS", "delivery_continuity", "PASS",
                            level="PASS", mastery=1.0))
        model["evidence"].append(
            {"id": "EVD-003", "kind": "INSPECTED", "collector": "x",
             "method": "read", "timestamp": "...", "tool": None,
             "locator": {"path": "src/ops.py", "lines": [1, 10]},
             "procedure": None, "result": "...", "claims": ["DLY-OPS"],
             "limits": "...", "sampling": "full", "counter": "...",
             "redaction": "none", "unavailable": None})
        model["scores"]["dimensions"]["delivery_continuity"] = {
            "mastery": 1.0, "uncapped": 10, "score": 10, "coverage": 1.0,
            "eligible": True}
        dims = {
            "security": {"applicable": True, "eligible": True, "score": 5,
                         "lo": 4, "hi": 5},
            "delivery_continuity": {"applicable": True, "eligible": True,
                                    "score": 10, "lo": 10, "hi": 10},
        }
        expected = self.checker.compute_headline(
            dims, 10, False, True, "PENDING EVIDENCE")
        for key in ("product", "process", "single"):
            model["scores"][key] = expected[key]
        return model

    def _with_api_scored(self, model):
        model = copy.deepcopy(model)
        entry = next(
            c for c in model["criteria"] if c["id"] == "CMP-API")
        entry.update(
            {"outcome": "PASS", "level": "PASS", "mastery": 1.0,
             "na_basis": None, "applicability": "applicable"})
        model["evidence"][0]["claims"].append("CMP-API")
        model["scores"]["dimensions"]["api_compatibility"] = {
            "mastery": 1.0, "uncapped": 10, "score": 10, "coverage": 1.0,
            "eligible": True}
        dims = {
            "security": {"applicable": True, "eligible": True, "score": 5,
                         "lo": 4, "hi": 5},
            "api_compatibility": {"applicable": True, "eligible": True,
                                  "score": 10, "lo": 10, "hi": 10},
        }
        expected = self.checker.compute_headline(
            dims, 10, False, True, "PENDING EVIDENCE")
        for key in ("product", "process", "single"):
            model["scores"][key] = expected[key]
        return model

    def _multi_model(self, names):
        model = self._valid_model()
        model["scope"]["projects"] = [
            {"name": n, "path": ".", "automation_census": "signals"}
            for n in names
        ]
        criteria = []
        claims = []
        dimensions = {}
        per_project = {}
        readiness = {}
        for i, name in enumerate(names):
            cid = "SEC-AUTHZ" if i == 0 else f"SEC-AUTHZ-{i + 1:02d}"
            criteria.append(self._criteria_entry(
                cid, f"{name}.security", "PASS", criticality="high",
                level="PASS", mastery=1.0, catalogue_id="SEC-AUTHZ"))
            claims.append(cid)
            dimensions[f"{name}.security"] = {
                "mastery": 1.0, "uncapped": 10, "score": 10,
                "coverage": 1.0, "eligible": True}
            per_project[name] = {
                "product": {"score": 10.0, "interval": None,
                            "published": True, "eligible_weight": 3,
                            "applicable_weight": 3, "lowest": ["security"]},
                "process": {"score": None, "interval": None,
                            "published": False, "scored": 0,
                            "applicable": 0, "lowest": []},
                "single": {"score": 10.0, "raw": 10.0, "interval": None,
                           "flag": "product-only", "ceiling": None,
                           "band": "Excellent"},
            }
            readiness[name] = {"state": "READY", "blocking": []}
        model["criteria"] = criteria
        model["evidence"] = [
            {"id": "EVD-001", "kind": "INSPECTED", "collector": "x",
             "method": "read", "timestamp": "...", "tool": None,
             "locator": {"path": "src/app.py", "lines": [1, 40]},
             "procedure": None, "result": "...", "claims": claims,
             "limits": "...", "sampling": "full", "counter": "...",
             "redaction": "none", "unavailable": None},
        ]
        model["findings"] = []
        model["risks"] = []
        model["recommendations"] = []
        model["readiness"] = {"per_project": readiness}
        model["scores"]["dimensions"] = dimensions
        for key in ("product", "process", "single"):
            del model["scores"][key]
        model["scores"]["per_project"] = per_project
        return model

    def _run(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), \
                contextlib.redirect_stderr(err):
            rc = self.comparator.main(argv)
        return rc, out.getvalue(), err.getvalue()

    def _write(self, tmp, model, name):
        path = Path(tmp) / name
        path.write_text(json.dumps(model), encoding="utf-8")
        return path

    def _patched_check(self, fn):
        original = self.comparator.CHECK.check_model
        self.comparator.CHECK.check_model = fn
        return original

    def test_identical_models_zero_deltas_and_leads_by_zero(self):
        model = self._valid_model()
        self.assertEqual(
            self.checker.check_model(model, self._catalogue()), [])
        result, failures = self.comparator.compare(
            [model, copy.deepcopy(model)], catalogue=self._catalogue())
        self.assertEqual(failures, [])
        comp = result["compared"][0]
        self.assertTrue(comp["product"]["comparable"])
        self.assertTrue(comp["single"]["comparable"])
        for row in comp["dimensions"]:
            self.assertEqual(row["delta"], 0, row)
        self.assertIn("leads m2 by 0.0", comp["ranking"]["line"])
        self.assertIn(
            "product-only vs product-only", comp["ranking"]["line"])
        text = self.comparator.render_text(result)
        self.assertIn("ranking: m1 leads m2 by 0.0", text)

    def test_unpublished_process_marks_not_comparable(self):
        catalogue = self._process_catalogue()
        m1 = self._with_na_dly(self._valid_model())
        m2 = self._with_process(self._valid_model())
        self.assertEqual(self.checker.check_model(m1, catalogue), [])
        self.assertEqual(self.checker.check_model(m2, catalogue), [])
        result, failures = self.comparator.compare(
            [m1, m2], catalogue=catalogue)
        self.assertEqual(failures, [])
        comp = result["compared"][0]
        self.assertIn(
            "not comparable - process unpublished",
            comp["process"]["comparison"])
        self.assertIn("not comparable", comp["single"]["comparison"])
        self.assertIn("delta", comp["product"]["comparison"])

    def test_catalogue_version_mismatch_exits_2(self):
        m2 = self._valid_model()
        m2["scope"]["catalogue_version"] = 2
        with tempfile.TemporaryDirectory() as tmp:
            p1 = self._write(tmp, self._valid_model(), "m1.json")
            p2 = self._write(tmp, m2, "m2.json")
            original = self._patched_check(lambda m, c=None: [])
            try:
                rc, _out, err = self._run([str(p1), str(p2)])
            finally:
                self.comparator.CHECK.check_model = original
        self.assertEqual(rc, 2)
        self.assertIn("catalogue_version differs", err)
        # through the real check_model the mismatching model already fails
        result, failures = self.comparator.compare(
            [self._valid_model(), m2], catalogue=self._catalogue())
        self.assertIsNone(result)
        self.assertTrue(any("catalogue_version" in f for f in failures))

    def test_failing_input_exits_2(self):
        bad = self._valid_model()
        bad["scope"]["subject"] = "bad"
        with tempfile.TemporaryDirectory() as tmp:
            p1 = self._write(tmp, self._valid_model(), "m1.json")
            p2 = self._write(tmp, bad, "m2.json")
            original = self._patched_check(
                lambda m, c=None: (
                    ["subject bad: intentional failure"]
                    if m.get("scope", {}).get("subject") == "bad" else []
                )
            )
            try:
                rc, _out, err = self._run([str(p1), str(p2)])
            finally:
                self.comparator.CHECK.check_model = original
        self.assertEqual(rc, 2)
        self.assertIn("intentional failure", err)
        # real check_model failures abort the same way
        broken = self._valid_model()
        broken["criteria"][1]["outcome"] = "BOGUS"
        result, failures = self.comparator.compare(
            [self._valid_model(), broken], catalogue=self._catalogue())
        self.assertIsNone(result)
        self.assertTrue(any("not a criteria state" in f for f in failures))

    def test_multi_project_pairs_by_name_and_lists_unpaired(self):
        catalogue = self._small_catalogue()
        m1 = self._multi_model(["api", "cli"])
        m2 = self._multi_model(["api", "ghost"])
        self.assertEqual(self.checker.check_model(m1, catalogue), [])
        self.assertEqual(self.checker.check_model(m2, catalogue), [])
        result, failures = self.comparator.compare(
            [m1, m2], catalogue=catalogue)
        self.assertEqual(failures, [])
        self.assertEqual(
            [c["scope"] for c in result["compared"]], ["api"])
        self.assertEqual(result["unpaired"], [
            {"name": "cli", "only_in": ["m1"]},
            {"name": "ghost", "only_in": ["m2"]},
        ])
        text = self.comparator.render_text(result)
        self.assertIn("unpaired: cli (only in m1)", text)
        self.assertIn("unpaired: ghost (only in m2)", text)

    def test_product_only_vs_full_single_not_comparable(self):
        catalogue = self._process_catalogue()
        m1 = self._with_na_dly(self._valid_model())
        m2 = self._with_process(self._valid_model())
        result, failures = self.comparator.compare(
            [m1, m2], catalogue=catalogue)
        self.assertEqual(failures, [])
        comp = result["compared"][0]
        self.assertEqual(comp["single"]["flags"],
                         {"m1": "product-only", "m2": "full"})
        self.assertIn("not comparable", comp["single"]["comparison"])
        self.assertIn("not comparable", comp["ranking"]["line"])
        self.assertIn("product-only vs full", comp["ranking"]["line"])

    def test_unpaired_applicability_shows_dash(self):
        m1 = self._valid_model()
        m2 = self._with_api_scored(self._valid_model())
        self.assertEqual(
            self.checker.check_model(m2, self._catalogue()), [])
        result, failures = self.comparator.compare(
            [m1, m2], catalogue=self._catalogue())
        self.assertEqual(failures, [])
        comp = result["compared"][0]
        row = next(
            r for r in comp["dimensions"]
            if r["dim"] == "api_compatibility")
        self.assertEqual(row["m1"], "-")
        self.assertEqual(row["m2"], 10)
        self.assertEqual(row["delta"], "-")

    def test_detail_level_mismatch_needs_anyway(self):
        m2 = self._valid_model()
        m2["scope"]["detail_level"] = "Detailed"
        result, failures = self.comparator.compare(
            [self._valid_model(), m2], catalogue=self._catalogue())
        self.assertIsNone(result)
        self.assertTrue(any("detail_level differs" in f for f in failures))
        result, failures = self.comparator.compare(
            [self._valid_model(), m2], anyway=True,
            catalogue=self._catalogue())
        self.assertEqual(failures, [])
        self.assertTrue(result["detail_level_mismatch"])
        self.assertIn("warning", result)

class TestFollowupPlan(unittest.TestCase):
    """Follow-up Plan contract: columns and FND-keyed rows."""

    PLAN = """## Remediation Roadmap

### Follow-up Plan

| Finding     | Priority | Owner      | Evidence        |
|-------------|----------|------------|-----------------|
| FND-SEC-001 | P1       | Maintainer | Regression test |

"""

    def test_conforming_plan_passes(self):
        vr = load_script("validate-report.py")
        self.assertEqual(vr.check_followup_plan(self.PLAN), [])

    def test_missing_columns_flagged(self):
        vr = load_script("validate-report.py")
        bad = self.PLAN.replace("| Finding     | Priority | Owner      | Evidence        |",
                                "| Item | Owner | Closure evidence |")
        fails = vr.check_followup_plan(bad)
        self.assertTrue(any("Finding" in f for f in fails))

    def test_rec_keyed_rows_flagged(self):
        vr = load_script("validate-report.py")
        bad = self.PLAN.replace("FND-SEC-001", "REC-001")
        fails = vr.check_followup_plan(bad)
        self.assertTrue(any("FND-XXX" in f for f in fails))

    def test_render_followup_p1_p2_only(self):
        rt = load_script("render-tables.py")
        model = {"recommendations": [
            {"finding": "FND-A", "priority": "P1", "owner": "maintainer",
             "verification": "regression test"},
            {"finding": "FND-B", "priority": "P3", "owner": "maintainer",
             "verification": "cosmetic"},
        ]}
        text = rt.render_followup(model, None)
        self.assertIn("FND-A", text)
        self.assertNotIn("FND-B", text)
        self.assertNotIn("Owner", text)

    def test_render_followup_keeps_distinct_owners(self):
        rt = load_script("render-tables.py")
        model = {"recommendations": [
            {"finding": "FND-A", "priority": "P1", "owner": "alice",
             "verification": "t1"},
            {"finding": "FND-B", "priority": "P2", "owner": "bob",
             "verification": "t2"},
        ]}
        text = rt.render_followup(model, None)
        self.assertIn("Owner", text)


class TestRegisterProse(unittest.TestCase):
    """Register-block prose rules."""

    GOOD = "### FND-SEC-001 Short title\n\nThe sentence reads fine.\n\n- **Pillar:** SEC\n"
    BAD = "### FND-SEC-001 t\n\nlowercase start without period\n\n- **Pillar:** SEC\n"

    def test_good_block_passes(self):
        vr = load_script("validate-report.py")
        self.assertEqual(vr.check_register_prose(self.GOOD, self.GOOD.split("\n")), [])

    def test_lowercase_no_period_flagged(self):
        vr = load_script("validate-report.py")
        fails = vr.check_register_prose(self.BAD, self.BAD.split("\n"))
        self.assertTrue(any("capital" in f for f in fails))
        self.assertTrue(any("period" in f for f in fails))

    def test_long_sentence_flagged(self):
        vr = load_script("validate-report.py")
        block = "### FND-A-001 t\n\n" + " ".join(["word"] * 21) + ".\n\n- **Pillar:** A\n"
        fails = vr.check_register_prose(block, block.split("\n"))
        self.assertTrue(any("20-word" in f for f in fails))

    def test_conjunction_start_flagged(self):
        vr = load_script("validate-report.py")
        block = "### FND-A-001 t\n\nAnd then it broke.\n\n- **Pillar:** A\n"
        fails = vr.check_register_prose(block, block.split("\n"))
        self.assertTrue(any("conjunction" in f for f in fails))

    def test_long_title_flagged(self):
        vr = load_script("validate-report.py")
        block = "### FND-A-001 " + "x" * 90 + "\n\nFine.\n\n- **Pillar:** A\n"
        fails = vr.check_register_prose(block, block.split("\n"))
        self.assertTrue(any("title" in f for f in fails))

    def test_blank_run_flagged(self):
        vr = load_script("validate-report.py")
        fails = vr.check_register_prose("a\n\n\nb", ["a", "", "", "b"])
        self.assertTrue(any("blank" in f for f in fails))


class TestValuelessRows(unittest.TestCase):
    """Metric rows carrying no information."""

    def test_zero_value_flagged(self):
        vr = load_script("validate-report.py")
        fails = vr.check_valueless_rows(["| Metric | Value |", "|---|---|", "| Tags | 0 |"])
        self.assertTrue(any("no" in f and "information" in f for f in fails))

    def test_meaningful_value_passes(self):
        vr = load_script("validate-report.py")
        self.assertEqual(vr.check_valueless_rows(["| Metric | Value |", "|---|---|", "| Commits | 148 |"]), [])

    def test_none_value_flagged(self):
        vr = load_script("validate-report.py")
        fails = vr.check_valueless_rows(["| Metric | Value |", "|---|---|", "| Tags | None |"])
        self.assertTrue(fails)


class TestRecResolves(unittest.TestCase):
    """REC description must not restate Resolves FND-XXX."""

    def test_resolves_restatement_flagged(self):
        vr = load_script("validate-report.py")
        block = "### REC-001 Fix the thing\n\nFix the thing. Resolves [FND-SEC-001](#x).\n\n- **Priority:** P1\n- **Finding:** FND-SEC-001\n"
        fails = vr.check_rec_blocks(block.split("\n"))
        self.assertTrue(any("restates" in f for f in fails))


    def test_meta_prefix_flagged(self):
        vr = load_script("validate-report.py")
        block = "### REC-001 t\n\nThe defect: something broke.\n\n- **Priority:** P1\n"
        fails = vr.check_register_prose(block, block.split("\n"))
        self.assertTrue(any("meta prefix" in f for f in fails))

    def test_truncation_flagged(self):
        vr = load_script("validate-report.py")
        block = "### REC-001 t\n\nSomething broke badly...\n\n- **Priority:** P1\n"
        fails = vr.check_register_prose(block, block.split("\n"))
        self.assertTrue(any("truncation" in f for f in fails))

    def test_ellipsis_inside_code_allowed(self):
        vr = load_script("validate-report.py")
        block = "### FND-A-001 t\n\nThe `bind(...)` call discards errors.\n\n- **Pillar:** A\n"
        fails = vr.check_register_prose(block, block.split("\n"))
        self.assertFalse(any("truncation" in f for f in fails))


class TestFinalizeGate(unittest.TestCase):
    """--gate delivery battery verdicts."""

    def test_gate_functions_exist(self):
        mod = load_script("finalize-report.py")
        self.assertTrue(callable(mod.run_gate))
        self.assertTrue(callable(mod.repo_root))

    def test_gate_not_ready_on_placeholder(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "report.md"
            target.write_text("| Time taken | TT:TT |" + chr(10), encoding="utf-8")
            mod = load_script("finalize-report.py")
            self.assertEqual(mod.run_gate(target, None, None, SCRIPTS, None), 1)

    def test_gate_ready_on_clean_state(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "report.md"
            target.write_text("| Time taken | 12:34 |" + chr(10), encoding="utf-8")
            mod = load_script("finalize-report.py")
            self.assertEqual(mod.run_gate(target, None, None, SCRIPTS, None), 0)
