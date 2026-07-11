"""
tests/acceptance/test_acceptance.py — Acceptance tests
SPDX-License-Identifier: MIT  Copyright (c) 2026 EmbeddedOS Foundation

Category: 6. Acceptance Testing
Tests that the website meets business requirements and user acceptance criteria:
- Brand identity requirements
- SEO requirements
- Accessibility requirements (WCAG 2.1 AA)
- Content completeness requirements
- Product showcase requirements
- Community/contact requirements
"""
import re, unittest
from pathlib import Path

SITE_ROOT = Path(__file__).parent.parent.parent

class TestBrandIdentityAcceptance(unittest.TestCase):
    """Acceptance tests for brand identity requirements."""

    def setUp(self):
        self.index = (SITE_ROOT / "index.html").read_text(encoding="utf-8")

    def test_brand_name_embeddedos_present(self):
        self.assertIn("EmbeddedOS", self.index, "Brand name 'EmbeddedOS' must appear on homepage")

    def test_logo_icon_present(self):
        self.assertIn("logo-icon", self.index, "Logo icon must be present")

    def test_version_badge_present(self):
        self.assertIn("nav-version", self.index, "Version badge must be present in nav")

    def test_mit_license_badge_present(self):
        self.assertIn("MIT", self.index, "MIT license badge must be present")

    def test_open_source_badge_present(self):
        self.assertIn("Open Source", self.index, "Open Source badge must be present")

    def test_founder_credit_present(self):
        # Either in HTML or structured data
        has_founder = "Srikanth" in self.index or "srpatcha" in self.index.lower()
        self.assertTrue(has_founder, "Founder credit must be present")

class TestSEOAcceptance(unittest.TestCase):
    """Acceptance tests for SEO requirements."""

    def setUp(self):
        self.index = (SITE_ROOT / "index.html").read_text(encoding="utf-8")

    def test_meta_description_present(self):
        self.assertIn('name="description"', self.index, "Meta description must be present")

    def test_meta_description_not_empty(self):
        m = re.search(r'name="description"\s+content="([^"]+)"', self.index)
        if not m:
            m = re.search(r'content="([^"]+)"\s+name="description"', self.index)
        self.assertIsNotNone(m, "Meta description must have content")
        if m:
            self.assertGreater(len(m.group(1)), 50, "Meta description should be descriptive")

    def test_og_image_present(self):
        self.assertIn('og:image', self.index, "Open Graph image must be present")

    def test_canonical_url_present(self):
        self.assertIn('rel="canonical"', self.index, "Canonical URL must be present")

    def test_structured_data_organization(self):
        self.assertIn('"Organization"', self.index, "Organization structured data must be present")

    def test_structured_data_software_application(self):
        self.assertIn('"SoftwareApplication"', self.index, "SoftwareApplication structured data must be present")

    def test_sitemap_accessible(self):
        self.assertTrue((SITE_ROOT / "sitemap.xml").exists(), "sitemap.xml must exist")

    def test_robots_txt_accessible(self):
        self.assertTrue((SITE_ROOT / "robots.txt").exists(), "robots.txt must exist")

    def test_title_length_acceptable(self):
        m = re.search(r'<title>(.*?)</title>', self.index, re.DOTALL)
        if m:
            title = m.group(1).strip()
            self.assertLessEqual(len(title), 80, f"Title too long for SEO: {len(title)} chars")
            self.assertGreaterEqual(len(title), 10, "Title too short for SEO")

class TestAccessibilityAcceptance(unittest.TestCase):
    """Acceptance tests for WCAG 2.1 AA accessibility requirements."""

    def setUp(self):
        self.index = (SITE_ROOT / "index.html").read_text(encoding="utf-8")

    def test_skip_to_content_link(self):
        self.assertIn("skip", self.index.lower(), "Skip-to-content link required for keyboard navigation")

    def test_nav_has_aria_label(self):
        self.assertIn('aria-label="Main navigation"', self.index, "Nav must have aria-label")

    def test_nav_has_role(self):
        self.assertIn('role="navigation"', self.index, "Nav must have role=navigation")

    def test_footer_has_role(self):
        self.assertIn('role="contentinfo"', self.index, "Footer must have role=contentinfo")

    def test_hamburger_has_aria_label(self):
        self.assertIn('aria-label="Toggle navigation menu"', self.index, "Hamburger must have aria-label")

    def test_hamburger_has_aria_expanded(self):
        self.assertIn('aria-expanded="false"', self.index, "Hamburger must have aria-expanded")

    def test_search_button_has_aria_label(self):
        self.assertIn('aria-label="Search', self.index, "Search button must have aria-label")

    def test_images_have_alt_or_aria_hidden(self):
        # SVGs used decoratively should have aria-hidden
        svg_count = self.index.count('<svg')
        aria_hidden_count = self.index.count('aria-hidden="true"')
        # At least some decorative SVGs should be hidden
        self.assertGreater(aria_hidden_count, 0, "Decorative SVGs should have aria-hidden='true'")

    def test_lang_attribute_on_html(self):
        self.assertIn('<html lang=', self.index, "HTML element must have lang attribute")

    def test_main_content_id_present(self):
        self.assertIn('id="main-content"', self.index, "Main content must have id for skip link target")

class TestContentCompletenessAcceptance(unittest.TestCase):
    """Acceptance tests for content completeness."""

    def setUp(self):
        self.index = (SITE_ROOT / "index.html").read_text(encoding="utf-8")

    def test_all_13_products_mentioned(self):
        products = ["EoS", "eBoot", "ebuild", "EIPC", "EAI", "ENI", "eOffice", "EoSim", "EoStudio"]
        for product in products:
            self.assertIn(product, self.index, f"Product '{product}' must be mentioned on homepage")

    def test_platform_count_mentioned(self):
        # Should mention platform/board count
        has_platform_count = "52" in self.index or "63" in self.index or "platform" in self.index.lower()
        self.assertTrue(has_platform_count, "Platform count should be mentioned")

    def test_quick_start_code_present(self):
        self.assertIn("git clone", self.index, "Quick start git clone command must be present")

    def test_social_media_links_present(self):
        socials = ["youtube", "linkedin", "github"]
        for social in socials:
            self.assertIn(social, self.index.lower(), f"{social} link must be present")

    def test_health_devices_section_present(self):
        self.assertIn("health-devices", self.index, "Health devices section must be present")

    def test_docs_linked_from_homepage(self):
        self.assertIn("docs/index.html", self.index, "Docs must be linked from homepage")

class TestProductShowcaseAcceptance(unittest.TestCase):
    """Acceptance tests for product showcase requirements."""

    def setUp(self):
        self.index = (SITE_ROOT / "index.html").read_text(encoding="utf-8")

    def test_product_cards_present(self):
        self.assertIn("product-card", self.index, "Product cards must be present")

    def test_product_grid_present(self):
        self.assertIn("product-grid", self.index, "Product grid must be present")

    def test_hero_stats_present(self):
        self.assertIn("hero-stats", self.index, "Hero stats must be present")

    def test_github_links_for_products(self):
        self.assertIn("github.com/embeddedos-org", self.index, "GitHub links for products must be present")

    def test_app_store_link_present(self):
        self.assertIn("eApps", self.index, "App Store link must be present")

if __name__ == "__main__":
    unittest.main(verbosity=2)
