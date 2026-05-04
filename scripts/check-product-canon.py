"""Validate the canonical EmbeddedOS product roster across this repo.

Fails with a non-zero exit code if any of the following appear in tracked
.html / .md files (excluding this script itself, build artefacts, and
node_modules):

    Forbidden  ->  reason
    ─────────────────────
    eVera                          (dropped product)
    eStocks / eStocks_Trading_Scripts (dropped product)
    eHardware-Designs-Products     (renamed -> eCAD-Hardware-Products)
    "15 products" / "15 Products"  (canonical is 13)
    "16 books"  / "16 Books"       (canonical is 14)
    "16 titles" / "16 guides"      (canonical is 14)
    "15-product"                   (canonical is 13-product)
    "16 repos"  / "15 repos"       (canonical is 13)

The intent is to lock the canonical list (13 products, 14 books) so
accidental copy-paste regressions surface immediately in CI.

Run locally:    python scripts/check-product-canon.py
CI exit codes:  0 = all good, 1 = at least one violation found.
"""
from __future__ import annotations
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SELF_REL = Path(__file__).resolve().relative_to(REPO_ROOT)

SCAN_EXTS = {'.html', '.md'}
EXCLUDE_DIR_NAMES = {
    '.git', 'node_modules', 'test-results', '_site', 'dist', 'build', '.next',
    '.venv', 'venv', '__pycache__',
}
EXCLUDE_PATH_FRAGMENTS = (
    'tests/screenshots',
    'tests\\screenshots',
    # Archival book/long-form sources that intentionally document historical
    # products. These compile to PDFs and are not user-facing canonical surfaces.
    'docs/embeddedos-ecosystem-guide.md',
    'docs\\embeddedos-ecosystem-guide.md',
    'CHANGELOG.md',
)

# (regex, friendly reason). Use re.IGNORECASE-compatible patterns where helpful.
FORBIDDEN: list[tuple[str, str]] = [
    (r'\beVera\b',                     'eVera (dropped product)'),
    (r'\beStocks\b',                   'eStocks (dropped product)'),
    (r'eStocks_Trading_Scripts',       'eStocks_Trading_Scripts (dropped product / renamed away)'),
    (r'eHardware-Designs-Products',    'eHardware-Designs-Products (renamed -> eCAD-Hardware-Products)'),
    (r'\b15 [Pp]roducts\b',            '"15 products" (canonical is 13)'),
    (r'\b15 repos\b',                  '"15 repos" (canonical is 13)'),
    (r'\b15-product\b',                '"15-product" (canonical is 13-product)'),
    (r'\b16 [Bb]ooks\b',               '"16 books" (canonical is 14)'),
    (r'\b16 [Tt]itles\b',              '"16 titles" (canonical is 14)'),
    (r'\b16 [Gg]uides\b',              '"16 guides" (canonical is 14)'),
    (r'\b16 repos\b',                  '"16 repos" (canonical is 13)'),
    (r'\b16 repositories\b',           '"16 repositories" (canonical is 13)'),
]

# Patterns that are expected to appear at least once anywhere under the repo.
# Empty list = no presence requirement (suitable for repos that don't surface
# product names directly, e.g. config-only repos).
EXPECTED_AT_LEAST_ONCE: list[tuple[str, str]] = [
    # Re-enable per-repo if you want to enforce the canonical hardware repo
    # name appears somewhere. Disabled here so the same script can be dropped
    # into any repo (including ones that don't list products).
    # (r'eCAD-Hardware-Products', 'expected to mention the canonical hardware repo'),
]


def is_excluded(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_DIR_NAMES:
        return True
    s = str(path)
    if any(frag in s for frag in EXCLUDE_PATH_FRAGMENTS):
        return True
    rel = path.resolve().relative_to(REPO_ROOT)
    if rel == SELF_REL:
        return True
    return False


def iter_files() -> list[Path]:
    out: list[Path] = []
    for p in REPO_ROOT.rglob('*'):
        if not p.is_file():
            continue
        if p.suffix.lower() not in SCAN_EXTS:
            continue
        if is_excluded(p):
            continue
        out.append(p)
    return sorted(out)


def main() -> int:
    files = iter_files()
    print(f'Scanning {len(files)} file(s) under {REPO_ROOT}')

    violations: list[str] = []
    expected_hits: dict[str, int] = {pat: 0 for pat, _ in EXPECTED_AT_LEAST_ONCE}

    compiled = [(re.compile(pat), reason) for pat, reason in FORBIDDEN]
    compiled_expected = [(re.compile(pat), reason) for pat, reason in EXPECTED_AT_LEAST_ONCE]

    for f in files:
        try:
            text = f.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            text = f.read_text(encoding='utf-8', errors='replace')

        rel = f.relative_to(REPO_ROOT)
        for cre, reason in compiled:
            for m in cre.finditer(text):
                line_no = text.count('\n', 0, m.start()) + 1
                snippet = text.splitlines()[line_no - 1].strip()[:160]
                violations.append(f'  {rel}:{line_no}  ->  {reason}\n      {snippet}')

        for cre, _ in compiled_expected:
            expected_hits[cre.pattern] += len(cre.findall(text))

    missing_expected = [
        (pat, reason) for (pat, reason) in EXPECTED_AT_LEAST_ONCE
        if expected_hits.get(pat, 0) == 0
    ]

    if not violations and not missing_expected:
        print('OK: no canonical-list violations.')
        return 0

    if violations:
        print(f'\nFOUND {len(violations)} forbidden reference(s):')
        for v in violations:
            print(v)

    if missing_expected:
        print(f'\nMISSING {len(missing_expected)} required reference(s):')
        for pat, reason in missing_expected:
            print(f'  expected /{pat}/ : {reason}')

    print('\nFAIL — please fix the references above or update the canonical list.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
