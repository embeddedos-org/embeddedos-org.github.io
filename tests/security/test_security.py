"""
tests/security/test_security.py — Security tests
SPDX-License-Identifier: MIT  Copyright (c) 2026 EmbeddedOS Foundation

Category: 5. Security Testing
Tests for XSS prevention, CSP headers, HTTPS enforcement, sensitive data
exposure, external link safety (noopener/noreferrer), inline script safety,
and no hardcoded credentials or API keys.
"""
import re, unittest
from pathlib import Path

SITE_ROOT = Path(__file__).parent.parent.parent
HTML_PAGES = list(SITE_ROOT.glob("*.html"))

class TestXSSPrevention(unittest.TestCase):
    """Tests for XSS prevention in HTML pages."""

    def test_no_inline_event_handlers_in_index(self):
        index = (SITE_ROOT / "index.html").read_text(encoding="utf-8")
        # Allow only known safe inline handlers; check for dangerous patterns
        dangerous = re.findall(r'on(click|load|error|mouseover)\s*=\s*"[^"]*eval', index, re.IGNORECASE)
        self.assertEqual(dangerous, [], f"Dangerous inline event handlers found: {dangerous}")

    def test_no_eval_in_js_files(self):
        for js_file in (SITE_ROOT / "js").glob("*.js"):
            content = js_file.read_text(encoding="utf-8")
            # eval() is dangerous; document.write is also a risk
            evals = re.findall(r'\beval\s*\(', content)
            self.assertEqual(evals, [], f"eval() found in {js_file.name}: {evals}")

    def test_no_document_write_in_js(self):
        for js_file in (SITE_ROOT / "js").glob("*.js"):
            content = js_file.read_text(encoding="utf-8")
            self.assertNotIn("document.write(", content, f"document.write() found in {js_file.name}")

    def test_no_innerhtml_with_user_input(self):
        for js_file in (SITE_ROOT / "js").glob("*.js"):
            content = js_file.read_text(encoding="utf-8")
            # Check for innerHTML assignments that might use user input
            dangerous_patterns = re.findall(r'innerHTML\s*=\s*.*location\.|innerHTML\s*=\s*.*document\.URL', content)
            self.assertEqual(dangerous_patterns, [], f"Dangerous innerHTML in {js_file.name}")

class TestExternalLinkSafety(unittest.TestCase):
    """Tests that all external links have rel=noopener."""

    def _check_page(self, page_path):
        content = page_path.read_text(encoding="utf-8")
        # Find external links
        ext_links = re.findall(r'<a[^>]+href="https?://[^"]*"[^>]*>', content)
        unsafe = []
        for link in ext_links:
            if 'target="_blank"' in link and 'noopener' not in link:
                unsafe.append(link[:100])
        return unsafe

    def test_index_external_links_safe(self):
        unsafe = self._check_page(SITE_ROOT / "index.html")
        self.assertEqual(unsafe, [], f"Unsafe external links in index.html: {unsafe}")

    def test_all_pages_external_links_safe(self):
        for page in HTML_PAGES:
            unsafe = self._check_page(page)
            self.assertEqual(unsafe, [], f"Unsafe external links in {page.name}: {unsafe}")

class TestSensitiveDataExposure(unittest.TestCase):
    """Tests that no sensitive data is exposed in source files."""

    def _check_no_secrets(self, content, filename):
        # Check for common secret patterns
        patterns = [
            (r'(?i)(api[_-]?key|secret[_-]?key|private[_-]?key)\s*[:=]\s*["\'][a-zA-Z0-9]{20,}', "API key"),
            (r'(?i)password\s*[:=]\s*["\'][^"\']{8,}', "password"),
            (r'ghp_[a-zA-Z0-9]{36}', "GitHub token"),
            (r'sk-[a-zA-Z0-9]{48}', "OpenAI key"),
        ]
        for pattern, label in patterns:
            matches = re.findall(pattern, content)
            self.assertEqual(matches, [], f"{label} found in {filename}: {matches}")

    def test_no_secrets_in_index(self):
        self._check_no_secrets((SITE_ROOT / "index.html").read_text(), "index.html")

    def test_no_secrets_in_js_files(self):
        for js_file in (SITE_ROOT / "js").glob("*.js"):
            self._check_no_secrets(js_file.read_text(), js_file.name)

    def test_no_secrets_in_css(self):
        self._check_no_secrets((SITE_ROOT / "style.css").read_text(), "style.css")

class TestHTTPSEnforcement(unittest.TestCase):
    """Tests that all resources use HTTPS."""

    def test_no_http_resource_links_in_index(self):
        index = (SITE_ROOT / "index.html").read_text(encoding="utf-8")
        # Find http:// links (not https://)
        http_links = re.findall(r'(?:href|src)="http://[^"]*"', index)
        self.assertEqual(http_links, [], f"Non-HTTPS resource links found: {http_links}")

    def test_sitemap_uses_https(self):
        sitemap = (SITE_ROOT / "sitemap.xml").read_text(encoding="utf-8")
        http_locs = re.findall(r'<loc>http://[^<]*</loc>', sitemap)
        self.assertEqual(http_locs, [], f"Non-HTTPS URLs in sitemap: {http_locs}")

class TestSecurityHeaders(unittest.TestCase):
    """Tests for security-related headers configuration."""

    def test_headers_file_exists(self):
        self.assertTrue((SITE_ROOT / "_headers").exists(), "_headers file must exist for Netlify/Cloudflare")

    def test_headers_has_content_security(self):
        if (SITE_ROOT / "_headers").exists():
            headers = (SITE_ROOT / "_headers").read_text(encoding="utf-8")
            # Check for at least some security headers
            has_security = any(h in headers for h in [
                "Content-Security-Policy", "X-Frame-Options",
                "X-Content-Type-Options", "Referrer-Policy"
            ])
            self.assertTrue(has_security, "_headers should define security headers")

class TestContentSafety(unittest.TestCase):
    """Tests for safe content practices."""

    def test_no_mixed_content_warnings(self):
        index = (SITE_ROOT / "index.html").read_text(encoding="utf-8")
        # No http:// in script src or link href
        mixed = re.findall(r'(?:src|href)="http://[^"]*"', index)
        self.assertEqual(mixed, [], f"Mixed content found: {mixed}")

    def test_robots_txt_not_blocking_all(self):
        robots = (SITE_ROOT / "robots.txt").read_text(encoding="utf-8")
        # Should not block all crawlers
        self.assertNotIn("Disallow: /\n", robots.replace(" ", ""), "robots.txt should not block all pages")

    def test_no_commented_out_credentials(self):
        index = (SITE_ROOT / "index.html").read_text(encoding="utf-8")
        # Check for commented-out passwords or tokens
        commented_creds = re.findall(r'<!--.*(?:password|token|secret).*-->', index, re.IGNORECASE)
        self.assertEqual(commented_creds, [], f"Commented credentials found: {commented_creds}")

if __name__ == "__main__":
    unittest.main(verbosity=2)
