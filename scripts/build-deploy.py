#!/usr/bin/env python3
"""scripts/build-deploy.py — Minify HTML/CSS/JS for deploy branch."""
import re, os, shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent

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

for css_file in ROOT.glob('**/*.css'):
    if 'node_modules' in str(css_file): continue
    orig = css_file.read_text(encoding='utf-8')
    mini = minify_css(orig)
    css_file.write_text(mini, encoding='utf-8')
    total_saved += len(orig) - len(mini); files_minified += 1
    print(f'  CSS {css_file.name}: {len(orig):,} -> {len(mini):,} bytes')

for js_file in ROOT.glob('**/*.js'):
    if 'node_modules' in str(js_file): continue
    orig = js_file.read_text(encoding='utf-8')
    mini = minify_js(orig)
    js_file.write_text(mini, encoding='utf-8')
    total_saved += len(orig) - len(mini); files_minified += 1
    print(f'  JS  {js_file.name}: {len(orig):,} -> {len(mini):,} bytes')

for html_file in ROOT.glob('**/*.html'):
    if 'node_modules' in str(html_file) or 'test-screenshots' in str(html_file): continue
    orig = html_file.read_text(encoding='utf-8')
    mini = minify_html(orig)
    html_file.write_text(mini, encoding='utf-8')
    total_saved += len(orig) - len(mini); files_minified += 1

print(f'\n✓ Minified {files_minified} files, saved {total_saved:,} bytes')

# Remove source-only dirs from deploy
for d in ['tests', 'test-screenshots', '.github']:
    p = ROOT / d
    if p.exists(): shutil.rmtree(p); print(f'  Removed: {d}')
print('✓ Deploy branch ready')
