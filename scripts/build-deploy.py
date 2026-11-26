#!/usr/bin/env python3
"""Build the minified static deployment tree without modifying tracked sources.

Two rules govern this script:

1. **It never writes outside ``dist/``.** The version this replaced minified the
   tracked sources over themselves and then deleted ``tests/`` and ``.github/``
   from the working tree. A build step must not be able to damage the thing it
   is building from.
2. **It never guesses at syntax.** The version this replaced minified with bare
   regexes, so ``re.sub(r'//[^\\n]*', '', text)`` truncated every line
   containing ``https://`` inside a string literal. The minifiers below are
   single-pass scanners that track which construct they are inside, so comment
   and whitespace rules are only applied where they actually hold.

Scope is deliberately limited to transformations that are provably safe without
a full parser: comments and inter-token whitespace. HTML text nodes are left
alone -- collapsing them changes rendering next to inline elements and inside
``white-space: pre`` -- so HTML shrinks through its comments and its embedded
``<style>``/``<script>`` blocks rather than its prose.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist"
SOURCE_ONLY = {
    "tests",
    "test-screenshots",
    ".github",
    "scripts",
    "dist",
    ".git",
    "node_modules",
}

# A '/' begins a regex literal, rather than a division, when the last
# significant token cannot end an expression.
_REGEX_OK_AFTER_CHARS = set("(,=:[!&|?{};+-*%~^<>")
_REGEX_OK_AFTER_WORDS = {
    "return",
    "typeof",
    "instanceof",
    "in",
    "of",
    "new",
    "delete",
    "void",
    "throw",
    "case",
    "do",
    "else",
    "yield",
    "await",
}


def _collapse(ws: str) -> str:
    """Reduce a whitespace run to the least that preserves meaning.

    A run containing a newline collapses to a newline, never to nothing, so
    automatic semicolon insertion keeps behaving the way the source did.
    """
    return "\n" if "\n" in ws else " "


def minify_js(src: str) -> str:
    """Strip JavaScript comments and indentation without entering literals."""
    out: list[str] = []
    i, n = 0, len(src)
    last_sig = ""  # last emitted non-whitespace character
    last_word = ""

    while i < n:
        ch = src[i]

        # Whitespace run.
        if ch in " \t\r\n":
            j = i
            while j < n and src[j] in " \t\r\n":
                j += 1
            # Drop leading/trailing whitespace entirely.
            if out and j < n:
                out.append(_collapse(src[i:j]))
            i = j
            continue

        # Comments.
        if ch == "/" and i + 1 < n:
            nxt = src[i + 1]
            if nxt == "/":
                j = src.find("\n", i)
                i = n if j == -1 else j
                continue
            if nxt == "*":
                j = src.find("*/", i + 2)
                i = n if j == -1 else j + 2
                # A block comment separated two tokens; keep a separator.
                if out and out[-1] not in (" ", "\n"):
                    out.append(" ")
                continue

        # String and template literals: copied verbatim.
        if ch in "\"'`":
            quote = ch
            j = i + 1
            while j < n:
                if src[j] == "\\":
                    j += 2
                    continue
                if src[j] == quote:
                    j += 1
                    break
                j += 1
            out.append(src[i:j])
            last_sig = quote
            last_word = ""
            i = j
            continue

        # Regex literal, distinguished from division by what precedes it.
        if ch == "/":
            prev_allows = (
                last_sig == ""
                or last_sig in _REGEX_OK_AFTER_CHARS
                or last_word in _REGEX_OK_AFTER_WORDS
            )
            if prev_allows:
                j = i + 1
                in_class = False
                while j < n:
                    c = src[j]
                    if c == "\\":
                        j += 2
                        continue
                    if c == "[":
                        in_class = True
                    elif c == "]":
                        in_class = False
                    elif c == "/" and not in_class:
                        j += 1
                        break
                    elif c == "\n":
                        break
                    j += 1
                out.append(src[i:j])
                last_sig = "/"
                last_word = ""
                i = j
                continue

        # Ordinary code.
        if ch.isalnum() or ch in "_$":
            j = i
            while j < n and (src[j].isalnum() or src[j] in "_$"):
                j += 1
            token = src[i:j]
            out.append(token)
            last_sig = token[-1]
            last_word = token
            i = j
            continue

        out.append(ch)
        last_sig = ch
        last_word = ""
        i += 1

    return "".join(out).strip()


def minify_css(src: str) -> str:
    """Strip CSS comments and inter-token whitespace, leaving literals intact.

    Literal runs -- quoted strings and unquoted ``url(...)`` values -- are
    lifted out behind placeholders before any whitespace rule is applied, so a
    declaration such as ``content: "a ; b"`` keeps its spacing.
    """
    out: list[str] = []
    literals: list[str] = []
    i, n = 0, len(src)

    def stash(text: str) -> str:
        literals.append(text)
        return f"\x00{len(literals) - 1}\x00"

    while i < n:
        ch = src[i]

        if ch in " \t\r\n":
            j = i
            while j < n and src[j] in " \t\r\n":
                j += 1
            if out and j < n:
                out.append(" ")
            i = j
            continue

        if ch == "/" and src.startswith("/*", i):
            j = src.find("*/", i + 2)
            i = n if j == -1 else j + 2
            continue

        if ch in "\"'":
            quote = ch
            j = i + 1
            while j < n:
                if src[j] == "\\":
                    j += 2
                    continue
                if src[j] == quote:
                    j += 1
                    break
                j += 1
            out.append(stash(src[i:j]))
            i = j
            continue

        # url(...) may hold an unquoted value; copy it whole.
        if src[i : i + 4].lower() == "url(":
            j = src.find(")", i)
            if j != -1:
                out.append(stash(src[i : j + 1]))
                i = j + 1
                continue

        out.append(ch)
        i += 1

    text = "".join(out)
    # Whitespace adjacent to these delimiters never carries meaning in CSS.
    text = re.sub(r"\s*([{};,])\s*", r"\1", text)

    # ':' only loses its surrounding whitespace inside a declaration block or an
    # at-rule's parentheses. In a selector, 'a :hover' (descendant) and
    # 'a:hover' (pseudo-class) are different rules, so selectors are left alone.
    pieces: list[str] = []
    depth = 0
    for part in re.split(r"([{}()])", text):
        if part in "{(":
            depth += 1
        elif part in "})":
            depth -= 1
        elif depth > 0:
            part = re.sub(r"\s*:\s*", ":", part)
        pieces.append(part)
    text = "".join(pieces)

    text = text.replace(";}", "}")
    return re.sub(r"\x00(\d+)\x00", lambda m: literals[int(m.group(1))], text).strip()


_PRESERVE = re.compile(
    r"(<pre\b[^>]*>.*?</pre>|<textarea\b[^>]*>.*?</textarea>)",
    re.IGNORECASE | re.DOTALL,
)
_COMMENT = re.compile(r"<!--(?!\[if|<!|\s*#)(?:(?!<!\[endif\]).)*?-->", re.DOTALL)
_STYLE = re.compile(r"(<style\b[^>]*>)(.*?)(</style>)", re.IGNORECASE | re.DOTALL)
_SCRIPT = re.compile(r"(<script\b[^>]*>)(.*?)(</script>)", re.IGNORECASE | re.DOTALL)


def _script_is_js(open_tag: str) -> bool:
    """True when a <script> body is JavaScript rather than data (JSON-LD etc.)."""
    m = re.search(r"""type\s*=\s*["']?([^"'>\s]+)""", open_tag, re.IGNORECASE)
    if not m:
        return True
    return m.group(1).lower() in {
        "text/javascript",
        "application/javascript",
        "module",
    }


def minify_html(src: str) -> str:
    """Strip HTML comments and minify embedded CSS/JS. Text nodes are untouched."""

    def one(chunk: str) -> str:
        chunk = _COMMENT.sub("", chunk)
        chunk = _STYLE.sub(
            lambda m: m.group(1) + minify_css(m.group(2)) + m.group(3), chunk
        )

        def script(m: re.Match[str]) -> str:
            if not _script_is_js(m.group(1)):
                return m.group(0)
            return m.group(1) + minify_js(m.group(2)) + m.group(3)

        return _SCRIPT.sub(script, chunk)

    # Split on <pre>/<textarea> so their contents are never rewritten.
    parts = _PRESERVE.split(src)
    return "".join(
        part if idx % 2 else one(part) for idx, part in enumerate(parts)
    ).strip()


MINIFIERS = {".css": minify_css, ".js": minify_js, ".html": minify_html}


def stage_tree() -> None:
    """Copy publishable files into OUT while leaving the checkout untouched."""
    if OUT.exists():
        shutil.rmtree(OUT)

    def ignore(directory: str, names: list[str]) -> set[str]:
        if Path(directory).resolve() == ROOT:
            return SOURCE_ONLY.intersection(names)
        return {"node_modules"}.intersection(names)

    shutil.copytree(ROOT, OUT, ignore=ignore)


def minify_tree() -> tuple[int, int]:
    """Minify the staged copy in place. Returns (files changed, bytes saved)."""
    files = saved = 0
    for path in sorted(OUT.rglob("*")):
        fn = MINIFIERS.get(path.suffix.lower())
        if fn is None or not path.is_file():
            continue
        original = path.read_text(encoding="utf-8")
        minified = fn(original)
        if len(minified) < len(original):
            path.write_text(minified, encoding="utf-8")
            saved += len(original) - len(minified)
            files += 1
    return files, saved


def build() -> None:
    stage_tree()
    files, saved = minify_tree()
    print(f"Deploy tree written to {OUT.relative_to(ROOT)}/ (source tree untouched)")
    print(f"Minified {files} files, saved {saved:,} bytes")


if __name__ == "__main__":
    build()
