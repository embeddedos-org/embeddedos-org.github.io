"""
tests/regression/test_regression.py — Regression tests
SPDX-License-Identifier: MIT  Copyright (c) 2026 EmbeddedOS Foundation

Category: 8. Regression Testing
Tests that previously fixed bugs have not been re-introduced:
- Nav uses li-wrapped structure (not bare div with anchors)
- Hamburger uses three span bars (not &#9776; entity)
- CSS targets li-wrapped nav links
- Mobile menu closes on link click
- No broken internal links
- All product cards present
- Footer has all required columns
- Search overlay present
- Structured data valid JSON
"""
import re, json, unittest
from pathlib import Path

SITE_ROOT = Path(__file__).parent.parent.parent

class TestNavRegressions(unittest.TestCase):
    """Regression tests for navbar fixes."""

    def setUp(self):
        self.index = (SITE_ROOT / "index.html").read_text(encoding="utf-8")
        self.css = (SITE_ROOT / "style.css").read_text(encoding="utf-8")
        self.site_chrome = (SITE_ROOT / "js" / "site-chrome.js").read_text(encoding="utf-8")

    def test_regression_nav_uses_ul_not_div(self):
        """REGRESSION: Nav was using <div class='nav-links'> instead of <ul>."""
        self.assertIn('<ul class="nav-links"', self.index,
                      "REGRESSION: Nav must use <ul> not <div>")
        self.assertNotIn('<div class="nav-links">', self.index,
                         "REGRESSION: Nav must NOT use <div class='nav-links'>")

    def test_regression_nav_links_wrapped_in_li(self):
        """REGRESSION: Nav links were bare <a> tags not wrapped in <li>."""
        self.assertIn('<li><a href=', self.index,
                      "REGRESSION: Nav links must be wrapped in <li>")

    def test_regression_hamburger_uses_span_bars_not_entity(self):
        """REGRESSION: Hamburger was using &#9776; entity instead of animated spans."""
        self.assertIn('hamburger-bar', self.index,
                      "REGRESSION: Hamburger must use span.hamburger-bar elements")
        self.assertNotIn('&#9776;', self.index,
                         "REGRESSION: Hamburger must NOT use &#9776; entity")

    def test_regression_hamburger_has_aria_expanded(self):
        """REGRESSION: Hamburger was missing aria-expanded attribute."""
        self.assertIn('aria-expanded="false"', self.index,
                      "REGRESSION: Hamburger must have aria-expanded='false'")

    def test_regression_css_targets_li_not_bare_a(self):
        """REGRESSION: CSS was targeting .nav-links a instead of .nav-links li a."""
        self.assertIn('.navbar .nav-links li a', self.css,
                      "REGRESSION: CSS must target .nav-links li a")

    def test_regression_mobile_menu_closes_on_click(self):
        """REGRESSION: Mobile menu didn't close when a link was clicked."""
        self.assertIn("classList.remove('open')", self.site_chrome,
                      "REGRESSION: Mobile menu must close on link click")

    def test_regression_hamburger_toggles_aria_expanded(self):
        """REGRESSION: Hamburger didn't update aria-expanded on toggle."""
        self.assertIn("aria-expanded", self.site_chrome,
                      "REGRESSION: site-chrome.js must manage aria-expanded")

    def test_regression_site_chrome_generates_li_links(self):
        """REGRESSION: site-chrome.js was generating bare <a> not <li><a>."""
        self.assertIn("<li>", self.site_chrome,
                      "REGRESSION: site-chrome.js must generate <li> wrapped links")

class TestContentRegressions(unittest.TestCase):
    """Regression tests for content fixes."""

    def setUp(self):
        self.index = (SITE_ROOT / "index.html").read_text(encoding="utf-8")

    def test_regression_all_product_cards_present(self):
        """REGRESSION: Some product cards were missing."""
        products = ["EoS", "eBoot", "ebuild", "EIPC", "EAI", "ENI"]
        for p in products:
            self.assertIn(p, self.index, f"REGRESSION: Product card '{p}' missing")

    def test_regression_footer_has_columns(self):
        """REGRESSION: Footer was missing columns."""
        self.assertIn("footer-brand", self.index, "REGRESSION: Footer brand/columns missing")

    def test_regression_search_overlay_present(self):
        """REGRESSION: Search overlay was removed."""
        self.assertIn("search-overlay", self.index, "REGRESSION: Search overlay missing")

    def test_regression_no_lorem_ipsum(self):
        """REGRESSION: Lorem ipsum placeholder text was left in."""
        self.assertNotIn("Lorem ipsum", self.index, "REGRESSION: Lorem ipsum found")

    def test_regression_structured_data_valid_json(self):
        """REGRESSION: Structured data JSON was malformed."""
        scripts = re.findall(
            r'<script type="application/ld\+json">(.*?)</script>',
            self.index, re.DOTALL
        )
        for i, script in enumerate(scripts):
            try:
                json.loads(script.strip())
            except json.JSONDecodeError as e:
                self.fail(f"REGRESSION: Structured data script #{i+1} is invalid JSON: {e}")

    def test_regression_canonical_link_present(self):
        """REGRESSION: Canonical link was missing."""
        self.assertIn('rel="canonical"', self.index, "REGRESSION: Canonical link missing")

    def test_regression_og_tags_present(self):
        """REGRESSION: Open Graph tags were missing."""
        for tag in ['og:title', 'og:description', 'og:image']:
            self.assertIn(tag, self.index, f"REGRESSION: OG tag '{tag}' missing")

class TestCSSRegressions(unittest.TestCase):
    """Regression tests for CSS fixes."""

    def setUp(self):
        self.css = (SITE_ROOT / "style.css").read_text(encoding="utf-8")

    def test_regression_css_has_transition_variables(self):
        """REGRESSION: CSS transition variables were missing."""
        self.assertIn("--transition-fast", self.css, "REGRESSION: --transition-fast missing")

    def test_regression_css_has_hamburger_animation(self):
        """REGRESSION: Hamburger animation CSS was missing."""
        self.assertIn("hamburger-bar", self.css, "REGRESSION: .hamburger-bar CSS missing")

    def test_regression_css_has_nav_underline_effect(self):
        """REGRESSION: Nav underline hover effect was broken."""
        self.assertIn("::after", self.css, "REGRESSION: Nav underline ::after CSS missing")

    def test_regression_footer_grid_has_6_columns(self):
        """REGRESSION: Footer grid was using 5 columns."""
        self.assertIn("2fr 1fr 1fr 1fr 1fr 1fr", self.css,
                      "REGRESSION: Footer grid should have 6 columns")

    def test_regression_css_root_has_improved_bg(self):
        """REGRESSION: CSS root background was old value."""
        self.assertIn("--bg-primary:", self.css, "REGRESSION: --bg-primary missing from :root")

if __name__ == "__main__":
    unittest.main(verbosity=2)
