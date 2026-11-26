"""
tests/unit/test_build_deploy.py — scripts/build-deploy.py safety and minification
SPDX-License-Identifier: MIT  Copyright (c) 2026 EmbeddedOS Foundation

Category: 1. Unit Tests

Guards the two ways this script has gone wrong:

1. It used to minify the tracked sources in place and then delete ``tests/``
   and ``.github/`` from the working tree. Running a build must never change
   the checkout it was run in.
2. It used to minify with bare regexes, so ``//`` inside a string literal was
   treated as a comment and the rest of the line was deleted. Minification
   must not alter what the code means.
"""

import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SITE_ROOT = Path(__file__).parent.parent.parent
SCRIPT = SITE_ROOT / "scripts" / "build-deploy.py"


def _load():
    spec = importlib.util.spec_from_file_location("build_deploy", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


bd = _load()


class TestSourceTreeIsNeverModified(unittest.TestCase):
    """A build step must not be able to damage the thing it builds from."""

    def test_running_the_build_leaves_the_checkout_byte_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "site"
            work.mkdir()
            (work / "scripts").mkdir()
            shutil.copy(SCRIPT, work / "scripts" / "build-deploy.py")
            (work / "index.html").write_text(
                "<html><head><title>T</title></head><body>\n"
                "  <!-- a comment -->\n  <p>hello</p>\n</body></html>",
                encoding="utf-8",
            )
            (work / "style.css").write_text(
                "/* note */\nbody {  color : red ; }\n", encoding="utf-8"
            )
            (work / "app.js").write_text(
                "// lead\nconst a = 1;\nconsole.log(a);\n", encoding="utf-8"
            )
            for keep in ("tests", ".github", "test-screenshots"):
                (work / keep).mkdir()
                (work / keep / "keep.txt").write_text("keep", encoding="utf-8")

            sources = sorted(
                p for p in work.rglob("*") if p.is_file() and "dist" not in p.parts
            )
            before = {p.relative_to(work): p.read_bytes() for p in sources}

            subprocess.run(
                [sys.executable, "-I", str(work / "scripts" / "build-deploy.py")],
                check=True,
                capture_output=True,
            )

            after = {
                p.relative_to(work): p.read_bytes()
                for p in sorted(work.rglob("*"))
                if p.is_file() and "dist" not in p.parts
            }
            self.assertEqual(
                before, after, "build-deploy.py modified its own source tree"
            )
            for keep in ("tests", ".github", "test-screenshots"):
                self.assertTrue(
                    (work / keep).is_dir(), f"build-deploy.py deleted {keep}/"
                )

            dist = work / "dist"
            self.assertTrue((dist / "index.html").is_file())
            for excluded in ("tests", ".github", "scripts", "test-screenshots"):
                self.assertFalse(
                    (dist / excluded).exists(),
                    f"{excluded}/ must not be published to dist/",
                )
            self.assertLess(
                len((dist / "style.css").read_text(encoding="utf-8")),
                len((work / "style.css").read_text(encoding="utf-8")),
                "dist/ was staged but never minified",
            )


class TestJavaScriptMinificationPreservesMeaning(unittest.TestCase):
    def test_double_slash_inside_a_string_is_not_a_comment(self):
        src = 'const u = "https://embeddedos.org/docs";\n'
        self.assertIn("https://embeddedos.org/docs", bd.minify_js(src))

    def test_comment_markers_inside_template_and_single_quotes_survive(self):
        src = "const a = `http://x/* y */`;\nconst b = 'z // w';\n"
        out = bd.minify_js(src)
        self.assertIn("http://x/* y */", out)
        self.assertIn("z // w", out)

    def test_regex_literal_containing_a_quote_is_not_a_string(self):
        src = "const re = /['\"]/g;\nconst after = 1;\n"
        out = bd.minify_js(src)
        self.assertIn("after", out)

    def test_division_is_not_mistaken_for_a_regex(self):
        src = "const r = total / count;\nconst next = r + 1;\n"
        out = bd.minify_js(src)
        self.assertIn("next", out)

    def test_comments_and_indentation_are_removed(self):
        src = "// gone\nfunction f() {\n    /* gone */\n    return 1;\n}\n"
        out = bd.minify_js(src)
        self.assertNotIn("gone", out)
        self.assertLess(len(out), len(src))

    def test_newlines_are_kept_so_semicolon_insertion_is_unchanged(self):
        src = "const a = 1\nconst b = 2\n"
        self.assertIn("\n", bd.minify_js(src))

    def test_minified_scripts_still_parse(self):
        src = (
            "const url = 'https://a/b'; // trailing\n"
            "const re = /ab+\\/c/gi;\n"
            "function f(x) { return x / 2; }\n"
            "const t = `a ${f(4)} b`;\n"
        )
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as fh:
            fh.write(bd.minify_js(src))
            tmp = fh.name
        try:
            node = shutil.which("node")
            if node is None:
                self.skipTest("node is not available")
            proc = subprocess.run(
                [node, "--check", tmp], capture_output=True, text=True
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
        finally:
            Path(tmp).unlink(missing_ok=True)


class TestCssMinificationPreservesMeaning(unittest.TestCase):
    def test_comments_go_and_rules_stay(self):
        out = bd.minify_css("/* c */\na {  color : red ; }\nb{top:0}\n")
        self.assertNotIn("/*", out)
        self.assertEqual(out.count("{"), 2)
        self.assertIn("color:red", out)

    def test_comment_text_inside_a_string_is_kept(self):
        out = bd.minify_css('a::after { content: "/* not a comment */"; }')
        self.assertIn("/* not a comment */", out)

    def test_media_queries_survive(self):
        out = bd.minify_css("@media (min-width: 600px) { a { top: 0; } }")
        self.assertIn("@media", out)
        self.assertIn("min-width:600px", out)

    def test_delimiters_inside_a_string_keep_their_spacing(self):
        out = bd.minify_css('a::after { content: "x ; y , z"; }')
        self.assertIn('"x ; y , z"', out)

    def test_descendant_selector_is_not_turned_into_a_pseudo_class(self):
        out = bd.minify_css("a :hover { top: 0; }")
        self.assertIn("a :hover", out)
        self.assertNotIn("a:hover", out)

    def test_unquoted_url_values_are_preserved(self):
        out = bd.minify_css("a { background: url(data:image/svg+xml;base64,AB==); }")
        self.assertIn("url(data:image/svg+xml;base64,AB==)", out)


class TestHtmlMinificationPreservesMeaning(unittest.TestCase):
    def test_pre_and_textarea_contents_are_untouched(self):
        src = "<pre>  keep\n   me  </pre><textarea>  raw  </textarea>"
        self.assertEqual(bd.minify_html(src), src)

    def test_comments_are_removed_but_conditional_comments_are_kept(self):
        out = bd.minify_html("<p>x</p><!-- drop --><!--[if IE]>keep<![endif]-->")
        self.assertNotIn("drop", out)
        self.assertIn("[if IE]", out)

    def test_text_nodes_are_left_alone(self):
        src = "<p>a <em>b</em> c</p>"
        self.assertIn("a <em>b</em> c", bd.minify_html(src))

    def test_json_ld_is_not_treated_as_javascript(self):
        src = '<script type="application/ld+json">{"a": 1}</script>'
        self.assertIn('{"a": 1}', bd.minify_html(src))

    def test_embedded_script_and_style_are_minified(self):
        src = "<style>/* x */ a { top : 0 ; }</style><script>// x\nvar a=1;</script>"
        out = bd.minify_html(src)
        self.assertNotIn("/* x */", out)
        self.assertNotIn("// x", out)
        self.assertIn("var a=1;", out)


if __name__ == "__main__":
    unittest.main()
