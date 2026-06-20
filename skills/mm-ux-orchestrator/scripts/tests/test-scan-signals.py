#!/usr/bin/env python3
"""Unit tests for scan-signals.py — run with: python3 scripts/tests/test-scan-signals.py"""

import json
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

# Add scripts/ to path so we can import helpers directly via subprocess
SCRIPTS_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import importlib.util

spec = importlib.util.spec_from_file_location("scan_signals", SCRIPTS_DIR / "scan-signals.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

scan_hex_drift = mod.scan_hex_drift
scan_missing_reference = mod.scan_missing_reference


class TestHexDrift(unittest.TestCase):
    def _write(self, tmp: Path, name: str, content: str) -> str:
        p = tmp / name
        p.write_text(textwrap.dedent(content))
        return name

    def test_detects_hex_color(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            rel = self._write(root, "Foo.astro", """\
                <template><div style="color: #3b82f6">hi</div></template>
            """)
            findings = scan_hex_drift(d, [rel])
        self.assertTrue(any(f["match"] == "#3b82f6" for f in findings))

    def test_detects_raw_css_var(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            rel = self._write(root, "Bar.ts", """\
                const x = "var(--color-primary)";
            """)
            findings = scan_hex_drift(d, [rel])
        self.assertTrue(any("var(--color" in f["match"] for f in findings))

    def test_skips_comment_lines(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            rel = self._write(root, "Baz.astro", """\
                // color: #ff0000 is forbidden
                /* #aabbcc */
            """)
            findings = scan_hex_drift(d, [rel])
        self.assertEqual(findings, [])

    def test_no_findings_for_token_class(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            rel = self._write(root, "Clean.astro", """\
                <div class="bg-primary text-secondary">ok</div>
            """)
            findings = scan_hex_drift(d, [rel])
        self.assertEqual(findings, [])

    def test_skips_unscannable_suffix(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            rel = self._write(root, "image.png", "#3b82f6")
            findings = scan_hex_drift(d, [rel])
        self.assertEqual(findings, [])

    def test_missing_file_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            findings = scan_hex_drift(d, ["does-not-exist.astro"])
        self.assertEqual(findings, [])

    def test_detects_hex_in_astro_template(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            rel = self._write(root, "Hero.astro", """\
                ---
                const color = "#ff6600";
                ---
                <div class="hero" />
            """)
            findings = scan_hex_drift(d, [rel])
        self.assertTrue(any(f["match"] == "#ff6600" for f in findings))


class TestMissingReference(unittest.TestCase):
    def _write(self, tmp: Path, name: str, content: str) -> str:
        p = tmp / name
        p.write_text(textwrap.dedent(content))
        return name

    def test_flags_apply_without_reference(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            rel = self._write(root, "Bad.astro", """\
                <style scoped>
                .foo { @apply bg-primary; }
                </style>
            """)
            findings = scan_missing_reference(d, [rel])
        self.assertEqual(len(findings), 1)
        self.assertIn("@reference", findings[0]["context"])

    def test_no_flag_when_reference_present(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            rel = self._write(root, "Good.astro", """\
                <style scoped>
                @reference "../../styles/global.css";
                .foo { @apply bg-primary; }
                </style>
            """)
            findings = scan_missing_reference(d, [rel])
        self.assertEqual(findings, [])

    def test_no_flag_when_no_apply(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            rel = self._write(root, "NoApply.astro", """\
                <style scoped>
                .foo { color: red; }
                </style>
            """)
            findings = scan_missing_reference(d, [rel])
        self.assertEqual(findings, [])

    def test_skips_non_astro_files(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            rel = self._write(root, "styles.css", "@apply bg-primary;")
            findings = scan_missing_reference(d, [rel])
        self.assertEqual(findings, [])

    def test_one_finding_per_file(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            rel = self._write(root, "Multi.astro", """\
                <style scoped>
                .a { @apply bg-primary; }
                .b { @apply text-secondary; }
                </style>
            """)
            findings = scan_missing_reference(d, [rel])
        self.assertEqual(len(findings), 1)


if __name__ == "__main__":
    unittest.main()
