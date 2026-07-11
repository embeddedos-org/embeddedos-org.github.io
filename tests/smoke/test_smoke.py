"""
tests/smoke/test_smoke.py — Smoke tests
SPDX-License-Identifier: MIT  Copyright (c) 2026 EmbeddedOS Foundation

Category: 7. Smoke Testing
Quick sanity checks that the most critical parts of the website are working.
These are the first tests to run — if any fail, deeper testing is pointless.
"""
import unittest
from pathlib import Path

SITE_ROOT = Path(__file__).parent.parent.parent

class TestCriticalFilesSmoke(unittest.TestCase):
    """Smoke tests: critical files must exist and be non-empty."""

    def test_smoke_index_html_exists_and_not_empty(self):
        p = SITE_ROOT / "index.html"
        self.assertTrue(p.exists(), "SMOKE FAIL: index.html missing")
        self.assertGreater(p.stat().st_size, 1000, "SMOKE FAIL: index.html is too small")

    def test_smoke_style_css_exists_and_not_empty(self):
        p = SITE_ROOT / "style.css"
        self.assertTrue(p.exists(), "SMOKE FAIL: style.css missing")
        self.assertGreater(p.stat().st_size, 5000, "SMOKE FAIL: style.css is too small")

    def test_smoke_site_chrome_js_exists(self):
        p = SITE_ROOT / "js" / "site-chrome.js"
        self.assertTrue(p.exists(), "SMOKE FAIL: site-chrome.js missing")
        self.assertGreater(p.stat().st_size, 500, "SMOKE FAIL: site-chrome.js is too small")

    def test_smoke_404_page_exists(self):
        self.assertTrue((SITE_ROOT / "404.html").exists(), "SMOKE FAIL: 404.html missing")

    def test_smoke_favicon_exists(self):
        has = (SITE_ROOT / "favicon.svg").exists() or (SITE_ROOT / "favicon.ico").exists()
        self.assertTrue(has, "SMOKE FAIL: No favicon found")

    def test_smoke_docs_directory_exists(self):
        self.assertTrue((SITE_ROOT / "docs").exists(), "SMOKE FAIL: docs/ directory missing")

    def test_smoke_eapps_directory_exists(self):
        self.assertTrue((SITE_ROOT / "eApps").exists(), "SMOKE FAIL: eApps/ directory missing")

class TestCriticalContentSmoke(unittest.TestCase):
    """Smoke tests: critical content must be present."""

    def setUp(self):
        self.index = (SITE_ROOT / "index.html").read_text(encoding="utf-8")

    def test_smoke_page_has_html_tag(self):
        self.assertIn("<html", self.index, "SMOKE FAIL: No <html> tag")

    def test_smoke_page_has_head(self):
        self.assertIn("<head>", self.index, "SMOKE FAIL: No <head> tag")

    def test_smoke_page_has_body(self):
        self.assertIn("<body>", self.index, "SMOKE FAIL: No <body> tag")

    def test_smoke_page_has_title(self):
        self.assertIn("<title>", self.index, "SMOKE FAIL: No <title> tag")

    def test_smoke_page_has_navbar(self):
        self.assertIn("navbar", self.index, "SMOKE FAIL: No navbar")

    def test_smoke_page_has_footer(self):
        self.assertIn("footer", self.index, "SMOKE FAIL: No footer")

    def test_smoke_embeddedos_brand_present(self):
        self.assertIn("EmbeddedOS", self.index, "SMOKE FAIL: Brand name missing")

    def test_smoke_css_linked(self):
        self.assertIn("style.css", self.index, "SMOKE FAIL: CSS not linked")

    def test_smoke_js_linked(self):
        self.assertIn("site-chrome.js", self.index, "SMOKE FAIL: site-chrome.js not linked")

    def test_smoke_no_500_error_markers(self):
        for marker in ["Internal Server Error", "500 Error", "Fatal error"]:
            self.assertNotIn(marker, self.index, f"SMOKE FAIL: Error marker found: {marker}")

    def test_smoke_no_php_errors(self):
        self.assertNotIn("<?php", self.index, "SMOKE FAIL: PHP code in HTML")
        self.assertNotIn("Warning:", self.index, "SMOKE FAIL: PHP warning in HTML")

class TestCriticalStructureSmoke(unittest.TestCase):
    """Smoke tests: critical HTML structure."""

    def setUp(self):
        self.index = (SITE_ROOT / "index.html").read_text(encoding="utf-8")

    def test_smoke_html_closes_properly(self):
        self.assertIn("</html>", self.index, "SMOKE FAIL: HTML not closed")

    def test_smoke_body_closes_properly(self):
        self.assertIn("</body>", self.index, "SMOKE FAIL: Body not closed")

    def test_smoke_nav_closes_properly(self):
        self.assertIn("</nav>", self.index, "SMOKE FAIL: Nav not closed")

    def test_smoke_footer_closes_properly(self):
        self.assertIn("</footer>", self.index, "SMOKE FAIL: Footer not closed")

if __name__ == "__main__":
    unittest.main(verbosity=2)
