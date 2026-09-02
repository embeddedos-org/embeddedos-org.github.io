#!/usr/bin/env python3
"""scripts/build-deploy.py — Minify HTML/CSS/JS for deploy branch."""
import re, os, shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT = ROOT / "dist"

# Everything below writes to OUT, never to ROOT.
#
# The original operated in place: it minified the tracked sources over
# themselves and then shutil.rmtree'd tests/, test-screenshots/ and .github/
# out of the working tree. Running it once on a checkout destroyed the CI
# configuration and the test suite, and left every source file minified. It is
# named "build for the deploy branch" but it never made a branch -- it mutated
# wherever it happened to be run.
#
# A build step must not be able to damage the thing it is building from.
SOURCE_ONLY = ("tests", "test-screenshots", ".github", "scripts", "dist", ".git")

def minify_css(text):
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s*([{};:,>~+])\s*', r'\1', text)
    text = re.sub(r';\}', '}', text)
    return text.strip()

def minify_js(text):
    text = re.sub(r'//[^\n]*', '', text)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    text = re.sub(r'\n\s*\n', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def minify_html(text):
    text = re.sub(r'<!--(?!.*\[if).*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n', text)
    return text.strip()

total_saved = 0
files_minified = 0


def stage_tree():
    """Copy the publishable tree into OUT, leaving the checkout alone."""
    if OUT.exists():
        shutil.rmtree(OUT)
    def ignore(directory, names):
        # Only prune at the top level; a nested directory called "scripts"
        # inside the site is content and must survive.
        if Path(directory).resolve() != ROOT.resolve():
            return {"node_modules"}
        return set(SOURCE_ONLY) | {"node_modules"}
    shutil.copytree(ROOT, OUT, ignore=ignore)


stage_tree()

for css_file in OUT.glob('**/*.css'):
    if 'node_modules' in str(css_file): continue
    orig = css_file.read_text(encoding='utf-8')
    mini = minify_css(orig)
    css_file.write_text(mini, encoding='utf-8')
    total_saved += len(orig) - len(mini); files_minified += 1
    print(f'  CSS {css_file.name}: {len(orig):,} -> {len(mini):,} bytes')

for js_file in OUT.glob('**/*.js'):
    if 'node_modules' in str(js_file): continue
    orig = js_file.read_text(encoding='utf-8')
    mini = minify_js(orig)
    js_file.write_text(mini, encoding='utf-8')
    total_saved += len(orig) - len(mini); files_minified += 1
    print(f'  JS  {js_file.name}: {len(orig):,} -> {len(mini):,} bytes')

for html_file in OUT.glob('**/*.html'):
    if 'node_modules' in str(html_file) or 'test-screenshots' in str(html_file): continue
    orig = html_file.read_text(encoding='utf-8')
    mini = minify_html(orig)
    html_file.write_text(mini, encoding='utf-8')
    total_saved += len(orig) - len(mini); files_minified += 1

print(f'\n✓ Minified {files_minified} files, saved {total_saved:,} bytes')
print(f'✓ Deploy tree written to {OUT.relative_to(ROOT)}/ (source tree untouched)')
