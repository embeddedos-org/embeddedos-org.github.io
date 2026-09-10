#!/usr/bin/env python3
"""Build the static deployment tree without modifying tracked sources."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist"
SOURCE_ONLY = {"tests", "test-screenshots", ".github", "scripts", "dist", ".git", "node_modules"}
def stage_tree() -> None:
    """Copy publishable files into OUT while leaving the checkout untouched."""
    if OUT.exists():
        shutil.rmtree(OUT)

    def ignore(directory: str, names: list[str]) -> set[str]:
        if Path(directory).resolve() == ROOT:
            return SOURCE_ONLY.intersection(names)
        return {"node_modules"}.intersection(names)

    shutil.copytree(ROOT, OUT, ignore=ignore)


def build() -> None:
    # HTML, JavaScript, and CSS all contain contexts where whitespace and
    # comment-looking text are significant. Preserve source bytes until the
    # project adopts syntax-aware minifiers for each language.
    stage_tree()
    print(f"Deploy tree written to {OUT.relative_to(ROOT)}/ (source tree untouched)")


if __name__ == "__main__":
    build()
