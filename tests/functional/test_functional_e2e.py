"""
tests/functional/test_functional_e2e.py — Functional & E2E tests
SPDX-License-Identifier: MIT  Copyright (c) 2026 EmbeddedOS Foundation

Categories: 3. Functional Tests | 4. End-to-End Tests
Tests complete user workflows, page content correctness, navigation flow,
and all key functional requirements of the EmbeddedOS website.
"""
import re, unittest
from pathlib import Path

SITE_ROOT = Path(__file__).parent.parent.parent

class TestFunctionalNavigation(unittest.TestCase):
    """Functional tests for navigation system."""
    def setUp(self):
        self.site_chrome = (SITE_ROOT/"js"/"site-chrome.js").read_text(encoding="utf-8")
        self.index = (SITE_ROOT/"index.html").read_text(encoding="utf-8")

    def test_home_nav_link_present(self): self.assertIn("/index.html", self.site_chrome)
    def test_get_started_nav_link_present(self): self.assertIn("/getting-started.html", self.site_chrome)
    def test_docs_nav_link_present(self): self.assertIn("/docs/index.html", self.site_chrome)
    def test_app_store_nav_link_present(self): self.assertIn("eApps", self.site_chrome)
    def test_kids_nav_link_present(self): self.assertIn("/kids.html", self.site_chrome)
    def test_hardware_lab_nav_link_present(self): self.assertIn("/hardware-lab.html", self.site_chrome)
    def test_flow_nav_link_present(self): self.assertIn("/flow.html", self.site_chrome)
    def test_books_nav_link_present(self): self.assertIn("/books.html", self.site_chrome)
    def test_stacks_nav_link_present(self): self.assertIn("/stacks/index.html", self.site_chrome)
    def test_get_involved_nav_link_present(self): self.assertIn("/get-involved.html", self.site_chrome)
    def test_github_nav_link_present(self): self.assertIn("github.com/embeddedos-org", self.site_chrome)
    def test_health_nav_link_present(self): self.assertIn("health-devices", self.site_chrome)
    def test_search_button_present(self): self.assertIn("nav-search-btn", self.site_chrome)

    def test_active_state_home(self): self.assertIn("'home'", self.site_chrome)
    def test_active_state_docs(self): self.assertIn("'docs'", self.site_chrome)
    def test_active_state_getting_started(self): self.assertIn("'getting-started'", self.site_chrome)

    def test_nav_links_count(self):
        links = re.findall(r'\{ href:', self.site_chrome)
        self.assertGreaterEqual(len(links), 10, "Nav should have at least 10 links")

class TestFunctionalContent(unittest.TestCase):
    """Functional tests for page content correctness."""
    def setUp(self):
        self.index = (SITE_ROOT/"index.html").read_text(encoding="utf-8")

    def test_hero_section_present(self): self.assertIn('class="hero"', self.index)
    def test_hero_title_present(self): self.assertIn("Operating System", self.index)
    def test_get_started_button_present(self): self.assertIn("Get Started", self.index)
    def test_github_star_button_present(self): self.assertIn("GitHub", self.index)
    def test_stats_section_present(self): self.assertIn("hero-stats", self.index)
    def test_product_grid_present(self): self.assertIn("product-grid", self.index)
    def test_eos_product_card_present(self): self.assertIn("EoS", self.index)
    def test_eboot_product_card_present(self): self.assertIn("eBoot", self.index)
    def test_eai_product_card_present(self): self.assertIn("EAI", self.index)
    def test_eni_product_card_present(self): self.assertIn("ENI", self.index)
    def test_quick_start_section_present(self): self.assertIn("Quick Start", self.index)
    def test_footer_brand_present(self): self.assertIn("footer-brand", self.index)
    def test_footer_has_social_links(self): self.assertIn("social-link", self.index)
    def test_footer_has_youtube(self): self.assertIn("youtube", self.index.lower())
    def test_footer_has_github(self): self.assertIn("github.com/embeddedos-org", self.index)
    def test_footer_copyright_present(self): self.assertIn("2025", self.index)
    def test_mit_license_mentioned(self): self.assertIn("MIT", self.index)

class TestFunctionalAllPages(unittest.TestCase):
    """Functional tests for all HTML pages."""
    def _load(self, name):
        p = SITE_ROOT / name
        return p.read_text(encoding="utf-8") if p.exists() else None

    def test_getting_started_page_loads(self):
        c = self._load("getting-started.html")
        self.assertIsNotNone(c); self.assertIn("Get Started", c)

    def test_books_page_loads(self):
        c = self._load("books.html")
        self.assertIsNotNone(c); self.assertIn("book", c.lower())

    def test_flow_page_loads(self):
        c = self._load("flow.html")
        self.assertIsNotNone(c)

    def test_hardware_lab_page_loads(self):
        c = self._load("hardware-lab.html")
        self.assertIsNotNone(c); self.assertIn("hardware", c.lower())

    def test_kids_page_loads(self):
        c = self._load("kids.html")
        self.assertIsNotNone(c)

    def test_get_involved_page_loads(self):
        c = self._load("get-involved.html")
        self.assertIsNotNone(c)

    def test_404_page_loads(self):
        c = self._load("404.html")
        self.assertIsNotNone(c); self.assertIn("404", c)

    def test_docs_index_loads(self):
        c = self._load("docs/index.html")
        self.assertIsNotNone(c)

    def test_eapps_index_loads(self):
        c = self._load("eApps/index.html")
        self.assertIsNotNone(c)

class TestE2EUserJourney(unittest.TestCase):
    """End-to-end tests simulating user journeys through the site."""
    def setUp(self):
        self.index = (SITE_ROOT/"index.html").read_text(encoding="utf-8")
        self.getting_started = (SITE_ROOT/"getting-started.html").read_text(encoding="utf-8") \
            if (SITE_ROOT/"getting-started.html").exists() else ""

    def test_e2e_homepage_to_get_started_link(self):
        self.assertIn("getting-started.html", self.index)

    def test_e2e_homepage_to_docs_link(self):
        self.assertIn("docs/index.html", self.index)

    def test_e2e_homepage_to_github_link(self):
        self.assertIn("github.com/embeddedos-org", self.index)

    def test_e2e_homepage_has_quick_start_code(self):
        self.assertIn("<pre>", self.index)
        self.assertIn("<code>", self.index)

    def test_e2e_getting_started_has_install_instructions(self):
        if self.getting_started:
            self.assertIn("install", self.getting_started.lower())

    def test_e2e_footer_community_links(self):
        self.assertIn("discussions", self.index.lower())

    def test_e2e_search_overlay_accessible(self):
        self.assertIn("search-overlay", self.index)
        self.assertIn("search-input", self.index)

if __name__ == "__main__":
    unittest.main(verbosity=2)
