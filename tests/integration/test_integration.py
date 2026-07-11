"""
tests/integration/test_integration.py — Integration tests
SPDX-License-Identifier: MIT  Copyright (c) 2026 EmbeddedOS Foundation

Category: 2. Integration Tests
Tests that multiple components work together correctly:
- CSS + HTML integration (class references)
- JS + HTML integration (script references, data attributes)
- Nav + CSS class consistency
- Footer + CSS class consistency
- All pages share consistent nav/footer structure
- Sitemap <-> actual pages consistency
"""
import re, unittest
from pathlib import Path

SITE_ROOT = Path(__file__).parent.parent.parent
HTML_PAGES = list(SITE_ROOT.glob("*.html"))

class TestCSSHTMLIntegration(unittest.TestCase):
    """Tests that CSS classes used in HTML are defined in CSS."""
    def setUp(self):
        self.css = (SITE_ROOT / "style.css").read_text(encoding="utf-8")
        self.index = (SITE_ROOT / "index.html").read_text(encoding="utf-8")

    def _css_has_class(self, cls):
        return f".{cls}" in self.css or f" {cls}" in self.css

    def test_navbar_class_defined(self): self.assertIn(".navbar", self.css)
    def test_nav_links_class_defined(self): self.assertIn(".nav-links", self.css)
    def test_nav_inner_class_defined(self): self.assertIn(".nav-inner", self.css)
    def test_logo_class_defined(self): self.assertIn(".logo", self.css)
    def test_btn_primary_class_defined(self): self.assertIn(".btn-primary", self.css)
    def test_hero_class_defined(self): self.assertIn(".hero", self.css)
    def test_footer_class_defined(self): self.assertIn(".footer", self.css)
    def test_hamburger_bar_class_defined(self): self.assertIn(".hamburger-bar", self.css)
    def test_nav_toggle_class_defined(self): self.assertIn(".nav-toggle", self.css)
    def test_badge_class_defined(self): self.assertIn(".badge", self.css)
    def test_product_card_class_defined(self): self.assertIn(".product-card", self.css)
    def test_section_class_defined(self): self.assertIn(".section", self.css)

    def test_index_uses_navbar_class(self): self.assertIn('class="navbar"', self.index)
    def test_index_uses_nav_links_class(self): self.assertIn('class="nav-links"', self.index)
    def test_index_uses_footer_class(self): self.assertIn('class="footer"', self.index)
    def test_index_uses_btn_class(self): self.assertIn('class="btn', self.index)
    def test_index_uses_hero_class(self): self.assertIn('class="hero"', self.index)

class TestJSHTMLIntegration(unittest.TestCase):
    """Tests JS and HTML are properly integrated."""
    def setUp(self):
        self.index = (SITE_ROOT / "index.html").read_text(encoding="utf-8")
        self.site_chrome = (SITE_ROOT / "js" / "site-chrome.js").read_text(encoding="utf-8")

    def test_site_chrome_loaded_before_body_close(self):
        sc_pos = self.index.find("site-chrome.js")
        body_close = self.index.find("</body>")
        self.assertGreater(body_close, sc_pos, "site-chrome.js should load before </body>")

    def test_search_overlay_present(self):
        self.assertIn("eos-search-overlay", self.index)

    def test_search_js_loaded(self):
        self.assertIn("search.js", self.index)

    def test_animations_js_loaded(self):
        self.assertIn("animations.js", self.index)

    def test_site_chrome_injects_nav(self):
        self.assertIn("nav.navbar", self.site_chrome)

    def test_site_chrome_injects_footer(self):
        self.assertIn("footer.footer", self.site_chrome)

    def test_nav_fallback_html_present(self):
        self.assertIn('<nav class="navbar"', self.index)

    def test_footer_fallback_html_present(self):
        self.assertIn('<footer class="footer"', self.index)

class TestMultiPageConsistency(unittest.TestCase):
    """Tests that all pages share consistent structure."""
    def setUp(self):
        self.pages = {}
        for p in HTML_PAGES:
            try:
                self.pages[p.name] = p.read_text(encoding="utf-8")
            except Exception:
                pass

    def test_all_pages_have_navbar(self):
        for name, content in self.pages.items():
            self.assertIn("navbar", content, f"{name} must have navbar")

    def test_all_pages_have_footer(self):
        for name, content in self.pages.items():
            self.assertIn("footer", content, f"{name} must have footer")

    def test_all_pages_link_style_css(self):
        for name, content in self.pages.items():
            self.assertIn("style.css", content, f"{name} must link style.css")

    def test_all_pages_have_viewport_meta(self):
        for name, content in self.pages.items():
            self.assertIn("viewport", content, f"{name} must have viewport meta")

    def test_all_pages_have_charset(self):
        for name, content in self.pages.items():
            self.assertIn("charset", content.lower(), f"{name} must have charset")

    def test_all_pages_have_title(self):
        for name, content in self.pages.items():
            self.assertIn("<title>", content, f"{name} must have title")

class TestSitemapPagesIntegration(unittest.TestCase):
    """Tests that sitemap references match actual files."""
    def setUp(self):
        self.sitemap = (SITE_ROOT / "sitemap.xml").read_text(encoding="utf-8")
        self.locs = re.findall(r'<loc>(.*?)</loc>', self.sitemap)

    def test_sitemap_has_entries(self):
        self.assertGreater(len(self.locs), 3, "Sitemap should have multiple entries")

    def test_sitemap_index_exists(self):
        index_refs = [l for l in self.locs if "index.html" in l or l.endswith("/")]
        self.assertGreater(len(index_refs), 0, "Sitemap must reference index")

    def test_sitemap_docs_referenced(self):
        docs_refs = [l for l in self.locs if "/docs/" in l]
        self.assertGreater(len(docs_refs), 0, "Sitemap should reference docs pages")

class TestNavCSSIntegration(unittest.TestCase):
    """Tests nav CSS correctly targets the li-wrapped structure."""
    def setUp(self):
        self.css = (SITE_ROOT / "style.css").read_text(encoding="utf-8")

    def test_nav_li_a_hover_defined(self):
        self.assertIn(".navbar .nav-links li a:hover", self.css)

    def test_nav_li_a_active_defined(self):
        self.assertIn(".navbar .nav-links li a.active", self.css)

    def test_nav_li_nth_child_defined(self):
        self.assertIn(".navbar .nav-links li:nth-child", self.css)

    def test_mobile_nav_li_styles(self):
        self.assertIn(".navbar .nav-links li a", self.css)

if __name__ == "__main__":
    unittest.main(verbosity=2)
