#!/usr/bin/env python3
"""
scripts/build-deploy.py — Deploy branch build script
Minifies HTML, CSS, and JS assets for the deploy branch.
Run from the repo root: python3 scripts/build-deploy.py
"""
import os, subprocess, shutil, tempfile
from pathlib import Path

SITE = Path(__file__).parent.parent
BACKUP = SITE / ".deploy_backup"

def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)

def minify_css(path):
    tmp = path.with_suffix(".min.css.tmp")
    r = run(["cleancss", "-o", str(tmp), str(path)])
    if r.returncode == 0 and tmp.exists():
        orig = path.stat().st_size
        mini = tmp.stat().st_size
        tmp.replace(path)
        pct = 100 - mini * 100 // orig if orig else 0
        print(f"  CSS  {path.name}: {orig:,} → {mini:,} bytes  (-{pct}%)")
    else:
        if tmp.exists(): tmp.unlink()
        print(f"  CSS  {path.name}: skipped ({r.stderr.strip()[:60]})")

def minify_js(path):
    tmp = path.with_suffix(".min.js.tmp")
    r = run(["terser", str(path), "--compress", "--mangle", "-o", str(tmp)])
    if r.returncode == 0 and tmp.exists():
        orig = path.stat().st_size
        mini = tmp.stat().st_size
        tmp.replace(path)
        pct = 100 - mini * 100 // orig if orig else 0
        print(f"  JS   {path.name}: {orig:,} → {mini:,} bytes  (-{pct}%)")
    else:
        if tmp.exists(): tmp.unlink()
        print(f"  JS   {path.name}: skipped ({r.stderr.strip()[:60]})")

def minify_html(path):
    tmp = path.with_suffix(".min.html.tmp")
    r = run([
        "html-minifier-terser",
        "--collapse-whitespace",
        "--remove-comments",
        "--remove-optional-tags",
        "--remove-redundant-attributes",
        "--remove-script-type-attributes",
        "--use-short-doctype",
        "--minify-css", "true",
        "--minify-js", "true",
        "-o", str(tmp), str(path)
    ])
    if r.returncode == 0 and tmp.exists():
        orig = path.stat().st_size
        mini = tmp.stat().st_size
        tmp.replace(path)
        pct = 100 - mini * 100 // orig if orig else 0
        print(f"  HTML {path.name}: {orig:,} → {mini:,} bytes  (-{pct}%)")
    else:
        if tmp.exists(): tmp.unlink()
        print(f"  HTML {path.name}: skipped ({r.stderr.strip()[:60]})")

def main():
    print("=" * 60)
    print("  EmbeddedOS — Deploy Build (minified)")
    print("=" * 60)

    print("\n[CSS]")
    for css in sorted(SITE.glob("*.css")):
        if not css.name.endswith(".bak"):
            minify_css(css)

    print("\n[JavaScript]")
    for js in sorted((SITE / "js").glob("*.js")):
        minify_js(js)

    print("\n[HTML — root]")
    for html in sorted(SITE.glob("*.html")):
        minify_html(html)

    print("\n[HTML — docs/]")
    docs = SITE / "docs"
    if docs.exists():
        for html in sorted(docs.glob("*.html")):
            minify_html(html)

    print("\n[HTML — eApps/]")
    eapps = SITE / "eApps"
    if eapps.exists():
        for html in sorted(eapps.glob("*.html")):
            minify_html(html)

    # Remove test files from deploy (not needed in production)
    tests_dir = SITE / "tests"
    if tests_dir.exists():
        shutil.rmtree(tests_dir)
        print("\n[Cleanup] Removed tests/ directory from deploy")

    # Remove backup files
    for bak in SITE.glob("*.bak"):
        bak.unlink()
        print(f"[Cleanup] Removed {bak.name}")

    print("\n" + "=" * 60)
    print("  Deploy build complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
