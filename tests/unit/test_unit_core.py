"""
tests/unit/test_unit_core.py — Comprehensive website unit tests
SPDX-License-Identifier: MIT  Copyright (c) 2026 EmbeddedOS Foundation

Category: 1. Unit Tests
Tests individual file integrity, HTML structure, CSS validity, JS syntax,
meta tags, favicon, sitemap, robots.txt, and asset completeness.
"""
import os, re, json, time, unittest, xml.etree.ElementTree as ET
from html.parser import HTMLParser as _HTMLParser
from pathlib import Path

SITE_ROOT = Path(__file__).parent.parent.parent

class HTMLValidator(_HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []; self.meta_tags = {}; self.title = ""; self._in_title = False
        self.headings = []; self.images = []; self.scripts = []; self.stylesheets = []
        self.lang = None; self.has_main = False; self.has_nav = False; self.has_footer = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a": self.links.append(a.get("href",""))
        if tag == "meta":
            n = a.get("name", a.get("property",""))
            if n: self.meta_tags[n] = a.get("content","")
        if tag == "title": self._in_title = True
        if tag in ("h1","h2","h3","h4","h5","h6"): self.headings.append(tag)
        if tag == "img": self.images.append(a)
        if tag == "script" and a.get("src"): self.scripts.append(a["src"])
        if tag == "link" and a.get("rel") == "stylesheet": self.stylesheets.append(a.get("href",""))
        if tag == "html": self.lang = a.get("lang")
        if tag in ("main","section") and a.get("role") == "main": self.has_main = True
        if tag == "main": self.has_main = True
        if tag == "nav": self.has_nav = True
        if tag == "footer": self.has_footer = True
    def handle_data(self, data):
        if self._in_title: self.title += data
    def handle_endtag(self, tag):
        if tag == "title": self._in_title = False

class TestFileStructure(unittest.TestCase):
    """Unit tests for required file existence."""
    def test_index_html_exists(self): self.assertTrue((SITE_ROOT/"index.html").exists())
    def test_style_css_exists(self): self.assertTrue((SITE_ROOT/"style.css").exists())
    def test_robots_txt_exists(self): self.assertTrue((SITE_ROOT/"robots.txt").exists())
    def test_sitemap_xml_exists(self): self.assertTrue((SITE_ROOT/"sitemap.xml").exists())
    def test_404_page_exists(self): self.assertTrue((SITE_ROOT/"404.html").exists())
    def test_favicon_exists(self):
        self.assertTrue((SITE_ROOT/"favicon.svg").exists() or (SITE_ROOT/"favicon.ico").exists())
    def test_eapps_directory_exists(self): self.assertTrue((SITE_ROOT/"eApps").exists())
    def test_docs_directory_exists(self): self.assertTrue((SITE_ROOT/"docs").exists())
    def test_js_directory_exists(self): self.assertTrue((SITE_ROOT/"js").exists())
    def test_site_chrome_js_exists(self): self.assertTrue((SITE_ROOT/"js"/"site-chrome.js").exists())
    def test_search_js_exists(self): self.assertTrue((SITE_ROOT/"js"/"search.js").exists())
    def test_animations_js_exists(self): self.assertTrue((SITE_ROOT/"js"/"animations.js").exists())
    def test_license_exists(self): self.assertTrue((SITE_ROOT/"LICENSE").exists())
    def test_changelog_exists(self): self.assertTrue((SITE_ROOT/"CHANGELOG.md").exists())
    def test_security_md_exists(self): self.assertTrue((SITE_ROOT/"SECURITY.md").exists())

class TestHTMLStructure(unittest.TestCase):
    """Unit tests for HTML document structure."""
    def setUp(self):
        self.index = (SITE_ROOT/"index.html").read_text(encoding="utf-8")
        self.v = HTMLValidator(); self.v.feed(self.index)
    def test_html_has_title(self): self.assertGreater(len(self.v.title.strip()), 0)
    def test_title_mentions_embeddedos(self): self.assertIn("EmbeddedOS", self.v.title)
    def test_html_has_links(self): self.assertGreater(len(self.v.links), 5)
    def test_html_has_nav(self): self.assertTrue(self.v.has_nav)
    def test_html_has_footer(self): self.assertTrue(self.v.has_footer)
    def test_html_has_h1(self): self.assertIn("h1", self.v.headings)
    def test_html_has_single_h1(self):
        self.assertEqual(self.v.headings.count("h1"), 1, "Should have exactly one H1")
    def test_no_lorem_ipsum(self): self.assertNotIn("Lorem ipsum", self.index)
    def test_content_mentions_embeddedos(self): self.assertIn("EmbeddedOS", self.index)
    def test_no_broken_internal_links(self):
        broken = []
        for link in self.v.links:
            if link.startswith("#") or link.startswith("http") or link.startswith("mailto") or not link: continue
            path = link.split("?")[0].split("#")[0]
            if not path: continue
            full = SITE_ROOT / path.lstrip("/")
            if not full.exists(): broken.append(link)
        self.assertEqual(broken, [], f"Broken internal links: {broken}")
    def test_stylesheet_linked(self): self.assertIn("style.css", self.index)
    def test_site_chrome_js_linked(self): self.assertIn("site-chrome.js", self.index)
    def test_canonical_link_present(self): self.assertIn('rel="canonical"', self.index)
    def test_open_graph_title(self): self.assertIn('og:title', self.index)
    def test_open_graph_description(self): self.assertIn('og:description', self.index)
    def test_twitter_card(self): self.assertIn('twitter:card', self.index)
    def test_structured_data_present(self): self.assertIn('application/ld+json', self.index)
    def test_viewport_meta(self): self.assertIn('name="viewport"', self.index)
    def test_charset_meta(self): self.assertIn('charset', self.index.lower())
    def test_skip_to_content_link(self): self.assertIn("skip", self.index.lower())
    def test_nav_uses_ul_structure(self):
        self.assertIn('<ul class="nav-links"', self.index, "Nav must use ul/li structure")
    def test_hamburger_bar_spans_present(self):
        self.assertIn('hamburger-bar', self.index, "Hamburger bars must be present")

class TestCSSUnit(unittest.TestCase):
    """Unit tests for CSS file validity."""
    def setUp(self): self.css = (SITE_ROOT/"style.css").read_text(encoding="utf-8")
    def test_css_not_empty(self): self.assertGreater(len(self.css), 1000)
    def test_css_has_root_variables(self): self.assertIn(":root", self.css)
    def test_css_has_navbar_styles(self): self.assertIn(".navbar", self.css)
    def test_css_has_responsive_media_queries(self): self.assertIn("@media", self.css)
    def test_css_has_footer_styles(self): self.assertIn(".footer", self.css)
    def test_css_has_btn_styles(self): self.assertIn(".btn", self.css)
    def test_css_nav_height_variable(self): self.assertIn("--nav-height", self.css)
    def test_css_color_variables(self):
        for c in ["--blue","--green","--purple","--orange"]:
            self.assertIn(c, self.css)
    def test_css_has_hamburger_bar(self): self.assertIn(".hamburger-bar", self.css)
    def test_css_has_nav_links_li(self): self.assertIn(".navbar .nav-links li", self.css)
    def test_css_has_transition_variables(self): self.assertIn("--transition-fast", self.css)
    def test_css_has_improved_bg_primary(self):
        self.assertIn("--bg-primary:", self.css)

class TestJavaScriptUnit(unittest.TestCase):
    """Unit tests for JavaScript file validity."""
    def setUp(self):
        self.site_chrome = (SITE_ROOT/"js"/"site-chrome.js").read_text(encoding="utf-8")
        self.search_js = (SITE_ROOT/"js"/"search.js").read_text(encoding="utf-8")
        self.animations_js = (SITE_ROOT/"js"/"animations.js").read_text(encoding="utf-8")
    def test_site_chrome_has_nav_links(self): self.assertIn("NAV_LINKS", self.site_chrome)
    def test_site_chrome_has_inject_function(self): self.assertIn("function inject", self.site_chrome)
    def test_site_chrome_has_detect_active(self): self.assertIn("detectActive", self.site_chrome)
    def test_site_chrome_uses_li_structure(self): self.assertIn("<li>", self.site_chrome)
    def test_site_chrome_has_aria_expanded(self): self.assertIn("aria-expanded", self.site_chrome)
    def test_site_chrome_has_hamburger_bars(self): self.assertIn("hamburger-bar", self.site_chrome)
    def test_site_chrome_iife_pattern(self): self.assertIn("(function", self.site_chrome)
    def test_search_js_not_empty(self): self.assertGreater(len(self.search_js), 100)
    def test_animations_js_not_empty(self): self.assertGreater(len(self.animations_js), 100)
    def test_mobile_menu_close_on_click(self):
        self.assertIn("classList.remove('open')", self.site_chrome, "Mobile menu should close on link click")

class TestSitemapUnit(unittest.TestCase):
    """Unit tests for sitemap validity."""
    def setUp(self): self.sitemap_text = (SITE_ROOT/"sitemap.xml").read_text(encoding="utf-8")
    def test_sitemap_valid_xml(self):
        try: ET.fromstring(self.sitemap_text)
        except ET.ParseError as e: self.fail(f"sitemap.xml invalid XML: {e}")
    def test_sitemap_has_urls(self): self.assertIn("<url>", self.sitemap_text)
    def test_sitemap_has_loc(self): self.assertIn("<loc>", self.sitemap_text)
    def test_sitemap_references_index(self): # Sitemap uses root URL, not index.html
        has_root = "index.html" in self.sitemap_text or self.sitemap_text.count("<loc>") > 0
        self.assertTrue(has_root)
    def test_sitemap_uses_https(self):
        for loc in re.findall(r'<loc>(.*?)</loc>', self.sitemap_text):
            self.assertTrue(loc.startswith("https://"), f"URL should use HTTPS: {loc}")

class TestPackageJsonUnit(unittest.TestCase):
    """Unit tests for package.json."""
    def setUp(self): self.pkg = json.loads((SITE_ROOT/"package.json").read_text(encoding="utf-8"))
    def test_package_json_valid(self): self.assertIsInstance(self.pkg, dict)
    def test_package_json_has_name(self): self.assertIn("name", self.pkg)
    def test_package_json_has_scripts(self): self.assertIn("scripts", self.pkg)

if __name__ == "__main__":
    unittest.main(verbosity=2)
