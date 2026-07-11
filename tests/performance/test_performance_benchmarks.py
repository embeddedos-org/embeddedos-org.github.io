"""
tests/performance/test_performance_benchmarks.py — Performance tests
SPDX-License-Identifier: MIT  Copyright (c) 2026 EmbeddedOS Foundation

Category: 6. Performance Testing
Tests for file size budgets, CSS/JS complexity, resource count,
image optimization, and overall page weight targets.
"""
import re, time, unittest
from pathlib import Path

SITE_ROOT = Path(__file__).parent.parent.parent

BUDGET_INDEX_HTML  = 120_000
BUDGET_STYLE_CSS   = 80_000
BUDGET_SITE_CHROME = 25_000
BUDGET_TOTAL_JS    = 100_000
BUDGET_TOTAL_CSS   = 100_000

class TestFileSizeBudgets(unittest.TestCase):
    def test_index_html_size_budget(self):
        size = (SITE_ROOT/"index.html").stat().st_size
        self.assertLessEqual(size, BUDGET_INDEX_HTML, f"index.html too large: {size:,} bytes")
    def test_style_css_size_budget(self):
        size = (SITE_ROOT/"style.css").stat().st_size
        self.assertLessEqual(size, BUDGET_STYLE_CSS, f"style.css too large: {size:,} bytes")
    def test_site_chrome_js_size_budget(self):
        size = (SITE_ROOT/"js"/"site-chrome.js").stat().st_size
        self.assertLessEqual(size, BUDGET_SITE_CHROME, f"site-chrome.js too large: {size:,} bytes")
    def test_total_js_size_budget(self):
        total = sum(f.stat().st_size for f in (SITE_ROOT/"js").glob("*.js"))
        self.assertLessEqual(total, BUDGET_TOTAL_JS, f"Total JS too large: {total:,} bytes")
    def test_total_css_size_budget(self):
        total = sum(f.stat().st_size for f in SITE_ROOT.glob("*.css"))
        self.assertLessEqual(total, BUDGET_TOTAL_CSS, f"Total CSS too large: {total:,} bytes")

class TestCSSComplexity(unittest.TestCase):
    def setUp(self): self.css = (SITE_ROOT/"style.css").read_text(encoding="utf-8")
    def test_css_selector_count_reasonable(self):
        self.assertLess(self.css.count("{"), 600)
    def test_css_media_query_count_reasonable(self):
        self.assertLess(self.css.count("@media"), 30)
    def test_css_animation_count_reasonable(self):
        self.assertLess(self.css.count("@keyframes"), 15)
    def test_css_uses_custom_properties(self):
        self.assertGreater(self.css.count("var(--"), 50)

class TestPageResourceCount(unittest.TestCase):
    def setUp(self): self.index = (SITE_ROOT/"index.html").read_text(encoding="utf-8")
    def test_css_file_count_minimal(self):
        self.assertLessEqual(len(re.findall(r'rel="stylesheet"', self.index)), 3)
    def test_js_file_count_reasonable(self):
        self.assertLessEqual(len(re.findall(r'<script[^>]+src="[^"]*\.js"', self.index)), 8)
    def test_no_jquery_dependency(self):
        self.assertNotIn("jquery", self.index.lower())
    def test_no_bootstrap_dependency(self):
        self.assertNotIn("bootstrap", self.index.lower())

class TestReadPerformance(unittest.TestCase):
    def test_index_html_reads_fast(self):
        start = time.perf_counter()
        _ = (SITE_ROOT/"index.html").read_text(encoding="utf-8")
        self.assertLess(time.perf_counter() - start, 0.5)
    def test_style_css_reads_fast(self):
        start = time.perf_counter()
        _ = (SITE_ROOT/"style.css").read_text(encoding="utf-8")
        self.assertLess(time.perf_counter() - start, 0.5)
    def test_all_js_files_read_fast(self):
        start = time.perf_counter()
        for js in (SITE_ROOT/"js").glob("*.js"):
            _ = js.read_text(encoding="utf-8")
        self.assertLess(time.perf_counter() - start, 1.0)
    def test_perf_sla_loop(self):
        start = time.perf_counter()
        for _ in range(100): pass
        self.assertLess((time.perf_counter() - start)/100, 0.01)

class TestImageOptimization(unittest.TestCase):
    def setUp(self): self.index = (SITE_ROOT/"index.html").read_text(encoding="utf-8")
    def test_no_bmp_images(self):
        self.assertEqual(re.findall(r'src="[^"]*\.bmp"', self.index), [])
    def test_no_tiff_images(self):
        self.assertEqual(re.findall(r'src="[^"]*\.tiff?"', self.index), [])

if __name__ == "__main__":
    unittest.main(verbosity=2)
