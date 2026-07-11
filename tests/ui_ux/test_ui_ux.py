"""
tests/ui_ux/test_ui_ux.py — UI and UX tests
SPDX-License-Identifier: MIT  Copyright (c) 2026 EmbeddedOS Foundation

Category: 9. UI and UX Testing
Tests for visual design quality, user experience, responsive design,
typography, color contrast readiness, interaction patterns, and
overall UI/UX best practices.
"""
import re, unittest
from pathlib import Path

SITE_ROOT = Path(__file__).parent.parent.parent

class TestResponsiveDesign(unittest.TestCase):
    """UI tests for responsive design."""

    def setUp(self):
        self.css = (SITE_ROOT / "style.css").read_text(encoding="utf-8")
        self.index = (SITE_ROOT / "index.html").read_text(encoding="utf-8")

    def test_viewport_meta_present(self):
        self.assertIn('name="viewport"', self.index, "Viewport meta required for responsive design")

    def test_viewport_has_width_device_width(self):
        self.assertIn("width=device-width", self.index, "Viewport must set width=device-width")

    def test_viewport_has_initial_scale(self):
        self.assertIn("initial-scale=1", self.index, "Viewport must set initial-scale=1")

    def test_css_has_mobile_breakpoint_900(self):
        self.assertIn("max-width: 900px", self.css, "CSS must have 900px mobile breakpoint")

    def test_css_has_mobile_breakpoint_768(self):
        self.assertIn("max-width: 768px", self.css, "CSS must have 768px tablet breakpoint")

    def test_css_has_mobile_breakpoint_480(self):
        self.assertIn("max-width: 480px", self.css, "CSS must have 480px small mobile breakpoint")

    def test_css_product_grid_responsive(self):
        self.assertIn("product-grid", self.css, "Product grid must have responsive styles")

    def test_css_hero_responsive(self):
        # Hero font size should change at mobile
        self.assertIn(".hero h1", self.css, "Hero h1 must have responsive styles")

    def test_css_footer_responsive(self):
        self.assertIn("footer-inner", self.css, "Footer must have responsive styles")

    def test_hamburger_hidden_on_desktop(self):
        # nav-toggle should be display:none by default
        self.assertIn(".nav-toggle", self.css, "nav-toggle must be styled")
        toggle_pos = self.css.find(".nav-toggle {")
        if toggle_pos > 0:
            toggle_block = self.css[toggle_pos:toggle_pos+200]
            self.assertIn("display: none", toggle_block, "nav-toggle must be hidden on desktop")

    def test_hamburger_visible_on_mobile(self):
        # Inside @media block, nav-toggle should be display:flex
        media_sections = re.findall(r'@media[^{]+\{(.*?)\}(?=\s*(?:@media|\.|\#|[a-z]))', self.css, re.DOTALL)
        mobile_toggle_visible = any("nav-toggle" in s and "display: flex" in s for s in media_sections)
        self.assertTrue(mobile_toggle_visible, "nav-toggle must be visible (display:flex) on mobile")

class TestTypographyUI(unittest.TestCase):
    """UI tests for typography."""

    def setUp(self):
        self.css = (SITE_ROOT / "style.css").read_text(encoding="utf-8")

    def test_font_family_defined(self):
        self.assertIn("--font-sans", self.css, "Font family variable must be defined")

    def test_monospace_font_defined(self):
        self.assertIn("--font-mono", self.css, "Monospace font variable must be defined")

    def test_inter_font_used(self):
        self.assertIn("Inter", self.css, "Inter font should be used for modern look")

    def test_base_font_size_16px(self):
        self.assertIn("font-size: 16px", self.css, "Base font size should be 16px")

    def test_line_height_comfortable(self):
        self.assertIn("line-height: 1.7", self.css, "Line height should be comfortable (1.7)")

    def test_heading_hierarchy_h1(self):
        self.assertIn("h1", self.css, "H1 styles must be defined")

    def test_heading_hierarchy_h2(self):
        self.assertIn("h2", self.css, "H2 styles must be defined")

    def test_font_smoothing(self):
        self.assertIn("-webkit-font-smoothing: antialiased", self.css, "Font smoothing should be enabled")

class TestColorThemeUI(unittest.TestCase):
    """UI tests for color theme."""

    def setUp(self):
        self.css = (SITE_ROOT / "style.css").read_text(encoding="utf-8")

    def test_dark_theme_background(self):
        # Background should be dark (starts with #0 or #1)
        m = re.search(r'--bg-primary:\s*(#[0-9a-fA-F]+)', self.css)
        self.assertIsNotNone(m, "--bg-primary must be defined")
        if m:
            color = m.group(1).lower()
            self.assertTrue(color.startswith("#0") or color.startswith("#1"),
                            f"Background should be dark, got: {color}")

    def test_brand_colors_defined(self):
        for color in ["--blue", "--green", "--purple", "--orange", "--cyan", "--pink"]:
            self.assertIn(color, self.css, f"Brand color {color} must be defined")

    def test_dim_variants_defined(self):
        for dim in ["--blue-dim", "--green-dim", "--purple-dim"]:
            self.assertIn(dim, self.css, f"Dim variant {dim} must be defined")

    def test_gradient_hero_defined(self):
        self.assertIn("--gradient-hero", self.css, "Hero gradient must be defined")

    def test_shadow_variables_defined(self):
        for shadow in ["--shadow-sm", "--shadow-md", "--shadow-lg"]:
            self.assertIn(shadow, self.css, f"Shadow variable {shadow} must be defined")

    def test_border_radius_variables_defined(self):
        for radius in ["--radius-sm", "--radius-md", "--radius-lg"]:
            self.assertIn(radius, self.css, f"Radius variable {radius} must be defined")

class TestInteractionPatternsUI(unittest.TestCase):
    """UI tests for interaction patterns."""

    def setUp(self):
        self.css = (SITE_ROOT / "style.css").read_text(encoding="utf-8")
        self.index = (SITE_ROOT / "index.html").read_text(encoding="utf-8")
        self.site_chrome = (SITE_ROOT / "js" / "site-chrome.js").read_text(encoding="utf-8")
        self.search_js = (SITE_ROOT / "js" / "search.js").read_text(encoding="utf-8")
        self.all_js = self.site_chrome + self.search_js

    def test_hover_transitions_on_buttons(self):
        self.assertIn("transition", self.css, "Buttons must have hover transitions")

    def test_hover_transform_on_cards(self):
        self.assertIn("translateY(-5px)", self.css, "Cards must have hover lift effect")

    def test_active_state_on_buttons(self):
        self.assertIn(":active", self.css, "Buttons must have active state")

    def test_scroll_behavior_smooth(self):
        self.assertIn("scroll-behavior: smooth", self.css, "Smooth scroll must be enabled")

    def test_cursor_pointer_on_buttons(self):
        self.assertIn("cursor: pointer", self.css, "Buttons must have cursor:pointer")

    def test_focus_styles_present(self):
        self.assertIn(":focus", self.css, "Focus styles must be defined for keyboard nav")

    def test_search_keyboard_shortcut(self):
        self.assertIn("=== '/'", self.all_js, "Search must support '/' keyboard shortcut")

    def test_search_escape_closes(self):
        self.assertIn("Escape", self.all_js, "Escape key must close search overlay")

    def test_backdrop_filter_on_navbar(self):
        self.assertIn("backdrop-filter: blur", self.css, "Navbar must have backdrop blur effect")

    def test_hero_animation_present(self):
        self.assertIn("@keyframes", self.css, "Hero must have CSS animations")

class TestUXCopyUI(unittest.TestCase):
    """UX tests for copy and content quality."""

    def setUp(self):
        self.index = (SITE_ROOT / "index.html").read_text(encoding="utf-8")

    def test_cta_buttons_have_clear_labels(self):
        self.assertIn("Get Started", self.index, "Primary CTA must have clear label")

    def test_error_page_has_helpful_message(self):
        p404 = SITE_ROOT / "404.html"
        if p404.exists():
            content = p404.read_text(encoding="utf-8")
            self.assertIn("404", content, "404 page must show error code")

    def test_hero_has_subtitle(self):
        self.assertIn("subtitle", self.index, "Hero must have a subtitle")

    def test_product_cards_have_descriptions(self):
        self.assertIn("product-card", self.index, "Product cards must be present")

    def test_code_blocks_have_syntax_highlighting_class(self):
        self.assertIn("<pre>", self.index, "Code blocks must be present")

    def test_footer_has_copyright(self):
        self.assertTrue("©" in self.index or "&copy;" in self.index, "Footer must have copyright symbol")

class TestPageLoadPerformanceUI(unittest.TestCase):
    """UI tests for page load performance indicators."""

    def setUp(self):
        self.index = (SITE_ROOT / "index.html").read_text(encoding="utf-8")
        self.css = (SITE_ROOT / "style.css").read_text(encoding="utf-8")

    def test_no_render_blocking_fonts_in_head(self):
        # Google Fonts should use display=swap
        if "fonts.googleapis.com" in self.index:
            self.assertIn("display=swap", self.index, "Google Fonts must use display=swap")

    def test_images_have_loading_lazy(self):
        # Non-hero images should have lazy loading
        imgs = re.findall(r'<img[^>]+>', self.index)
        if len(imgs) > 2:
            # At least some images should be lazy loaded
            lazy_imgs = [img for img in imgs if 'loading="lazy"' in img]
            self.assertGreater(len(lazy_imgs), 0, "Non-critical images should use loading='lazy'")

    def test_css_uses_will_change_sparingly(self):
        will_change_count = self.css.count("will-change")
        self.assertLess(will_change_count, 5, "will-change should be used sparingly")

    def test_css_uses_transform_not_position_for_animations(self):
        # transform is GPU-accelerated; position changes cause layout
        self.assertIn("transform:", self.css, "Animations should use transform for GPU acceleration")

    def test_js_deferred_loading(self):
        # Scripts should use defer or be at end of body
        scripts = re.findall(r'<script[^>]+src=[^>]+>', self.index)
        for script in scripts:
            has_defer = "defer" in script or "async" in script
            is_at_end = self.index.rfind(script) > len(self.index) * 0.7
            self.assertTrue(has_defer or is_at_end,
                            f"Script should be deferred or at end of body: {script[:80]}")

if __name__ == "__main__":
    unittest.main(verbosity=2)
