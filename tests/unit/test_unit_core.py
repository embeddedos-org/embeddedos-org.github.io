"""
tests/unit/test_unit_core.py — Comprehensive website unit tests
SPDX-License-Identifier: MIT  Copyright (c) 2026 EmbeddedOS Foundation
"""
import os
import re
import unittest
from html.parser import HTMLParser as _HTMLParser
from pathlib import Path

SITE_ROOT = Path(__file__).parent.parent.parent


class HTMLValidator(_HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.meta_tags = {}
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "a" and "href" in attrs_dict:
            self.links.append(attrs_dict["href"])
        if tag == "meta":
            name = attrs_dict.get("name", attrs_dict.get("property", ""))
            if name:
                self.meta_tags[name] = attrs_dict.get("content", "")
        if tag == "title":
            self._in_title = True

    def handle_data(self, data):
        if self._in_title:
            self.title += data

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False


class TestEmbeddedOsGitHubIoUnit(unittest.TestCase):
    def setUp(self):
        self.index = (SITE_ROOT / "index.html").read_text(encoding="utf-8")
        self.v = HTMLValidator()
        self.v.feed(self.index)

    def test_index_html_exists(self):
        self.assertTrue((SITE_ROOT / "index.html").exists())

    def test_index_has_title(self):
        self.assertGreater(len(self.v.title.strip()), 0)

    def test_index_has_links(self):
        self.assertGreater(len(self.v.links), 0)

    def test_no_broken_internal_links(self):
        broken = []
        for link in self.v.links:
            if link.startswith("#") or link.startswith("http") or link.startswith("mailto"):
                continue
            path = link.split("?")[0].split("#")[0]
            if not path:
                continue
            full = SITE_ROOT / path.lstrip("/")
            if not full.exists():
                broken.append(link)
        self.assertEqual(broken, [], f"Broken internal links: {broken}")

    def test_style_css_exists(self):
        self.assertTrue((SITE_ROOT / "style.css").exists())

    def test_robots_txt_exists(self):
        self.assertTrue((SITE_ROOT / "robots.txt").exists())

    def test_sitemap_xml_exists(self):
        self.assertTrue((SITE_ROOT / "sitemap.xml").exists())

    def test_404_page_exists(self):
        self.assertTrue((SITE_ROOT / "404.html").exists())

    def test_favicon_exists(self):
        favicon = (SITE_ROOT / "favicon.svg").exists() or (SITE_ROOT / "favicon.ico").exists()
        self.assertTrue(favicon)

    def test_index_contains_embeddedos(self):
        self.assertIn("EmbeddedOS", self.index, "Index should mention EmbeddedOS")

    def test_no_lorem_ipsum(self):
        self.assertNotIn("Lorem ipsum", self.index)

    def test_eapps_directory_exists(self):
        self.assertTrue((SITE_ROOT / "eApps").exists())

    def test_sitemap_valid_xml(self):
        import xml.etree.ElementTree as ET
        sitemap = (SITE_ROOT / "sitemap.xml").read_text()
        try:
            ET.fromstring(sitemap)
            valid = True
        except ET.ParseError:
            valid = False
        self.assertTrue(valid)


if __name__ == "__main__":
    unittest.main()
