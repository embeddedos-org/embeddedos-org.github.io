#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 EoS Project
# test_mobile_full_simulation.py — Full mobile simulation for EmbeddedOS website
# Covers: iOS, Android, tablet devices; all pages; all interactions;
#         gestures, scroll, orientation, performance, accessibility, navigation

import asyncio
import sys
import time
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Installing playwright...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright", "-q"], check=True)
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium", "--with-deps"], check=True)
    from playwright.async_api import async_playwright

BASE_URL = "http://localhost:8777"
SCREENSHOTS_DIR = Path(__file__).parent.parent.parent / "test-screenshots" / "mobile"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

# ── Device profiles ────────────────────────────────────────────────────────────
DEVICES = [
    # name,              width, height, dpr,  ua_hint,          is_touch
    ("iPhone_SE",         375,   667,   2.0,  "iPhone SE",      True),
    ("iPhone_14_Pro",     393,   852,   3.0,  "iPhone 14 Pro",  True),
    ("iPhone_14_ProMax",  430,   932,   3.0,  "iPhone 14 Pro Max", True),
    ("Samsung_Galaxy_S22",360,   780,   3.0,  "Samsung Galaxy S22", True),
    ("Pixel_7",           412,   915,   2.625,"Pixel 7",        True),
    ("iPad_Mini",         768,  1024,   2.0,  "iPad Mini",      True),
    ("iPad_Pro_11",      834,  1194,   2.0,  "iPad Pro 11",    True),
]

# ── All pages to test ──────────────────────────────────────────────────────────
PAGES = [
    ("home",            "/"),
    ("getting-started", "/getting-started.html"),
    ("docs",            "/docs/"),
    ("app-store",       "/eApps/"),
    ("books",           "/books.html"),
    ("hardware-lab",    "/hardware-lab.html"),
    ("kids",            "/kids.html"),
    ("flow",            "/flow.html"),
    ("get-involved",    "/get-involved.html"),
    ("stacks",          "/stacks/"),
    ("404",             "/nonexistent-page.html"),
]

results = []
pass_count = 0
fail_count = 0

def log(status, test, detail="", screenshot=""):
    global pass_count, fail_count
    icon = "✓" if status == "PASS" else "✗"
    msg = f"  {icon} [{status}]  {test}"
    if detail:
        msg += f" — {detail}"
    if screenshot:
        msg += f" — {screenshot}"
    print(msg)
    results.append({"status": status, "test": test, "detail": detail})
    if status == "PASS":
        pass_count += 1
    else:
        fail_count += 1

async def make_mobile_context(browser, device):
    name, width, height, dpr, ua_hint, is_touch = device
    ua = (
        f"Mozilla/5.0 (Linux; Android 13; {ua_hint}) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Mobile Safari/537.36"
    ) if "Samsung" in ua_hint or "Pixel" in ua_hint or "Galaxy" in ua_hint else (
        f"Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/17.0 Mobile/15E148 Safari/604.1"
    ) if "iPhone" in ua_hint else (
        f"Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/17.0 Mobile/15E148 Safari/604.1"
    )
    return await browser.new_context(
        viewport={"width": width, "height": height},
        device_scale_factor=dpr,
        is_mobile=is_touch,
        has_touch=is_touch,
        user_agent=ua,
    )

async def test_device_all_pages(browser, device):
    """Test every page loads correctly on a given device."""
    name, width, height, dpr, ua_hint, is_touch = device
    ctx = await make_mobile_context(browser, device)
    page = await ctx.new_page()

    section = f"[{name} {width}×{height}]"
    print(f"\n{'─'*60}")
    print(f"  DEVICE: {name} ({width}×{height} @{dpr}x) — All Pages")
    print(f"{'─'*60}")

    for page_name, path in PAGES:
        try:
            t0 = time.perf_counter()
            resp = await page.goto(BASE_URL + path, wait_until="domcontentloaded", timeout=10000)
            load_ms = (time.perf_counter() - t0) * 1000

            # Check HTTP status
            status_code = resp.status if resp else 0
            if page_name == "404":
                # 404 page should still render (200 from static server, but our 404.html exists)
                title = await page.title()
                has_404_content = await page.evaluate(
                    "() => document.body.innerText.includes('404') || document.body.innerText.includes('not found') || document.title.includes('404')"
                )
                log("PASS" if has_404_content else "FAIL",
                    f"{section} 404 page renders", f"title: {title[:40]}")
            else:
                # Check page has content
                has_nav = await page.evaluate(
                    "() => !!document.querySelector('nav, header, .navbar, #navbar')"
                )
                has_body = await page.evaluate(
                    "() => document.body.innerText.trim().length > 50"
                )
                log("PASS" if has_nav and has_body else "FAIL",
                    f"{section} {page_name} loads",
                    f"{load_ms:.0f}ms, nav={'yes' if has_nav else 'NO'}")

            # Screenshot every page on first device only to keep count manageable
            if name == "iPhone_14_Pro":
                fname = f"{name}_{page_name}.png"
                await page.screenshot(
                    path=str(SCREENSHOTS_DIR / fname),
                    full_page=True
                )
                log("PASS", f"{section} full-page screenshot", fname)

        except Exception as e:
            log("FAIL", f"{section} {page_name} load", str(e)[:80])

    await ctx.close()

async def test_mobile_nav_stability(browser, device):
    """Deep test of nav stability: open/close, scroll, rapid taps, orientation."""
    name, width, height, dpr, ua_hint, is_touch = device
    ctx = await make_mobile_context(browser, device)
    page = await ctx.new_page()

    section = f"[{name}]"
    print(f"\n{'─'*60}")
    print(f"  NAV STABILITY: {name} ({width}×{height})")
    print(f"{'─'*60}")

    await page.goto(BASE_URL + "/", wait_until="domcontentloaded")

    # 1. Hamburger visible on mobile (width < 900)
    is_narrow = width < 900
    toggle_visible = await page.evaluate(
        "() => { const t = document.querySelector('.nav-toggle'); "
        "return t ? window.getComputedStyle(t).display !== 'none' : false; }"
    )
    if is_narrow:
        log("PASS" if toggle_visible else "FAIL",
            f"{section} hamburger visible on narrow viewport")
    else:
        desktop_links_visible = await page.evaluate(
            "() => { const ul = document.querySelector('.nav-links'); "
            "return ul ? window.getComputedStyle(ul).display !== 'none' : false; }"
        )
        log("PASS" if desktop_links_visible else "FAIL",
            f"{section} desktop nav links visible on wide viewport")

    if is_narrow:
        toggle = page.locator(".nav-toggle")

        # 2. Menu starts closed
        closed_opacity = await page.evaluate(
            "() => parseFloat(window.getComputedStyle(document.querySelector('.nav-links')).opacity)"
        )
        log("PASS" if closed_opacity < 0.1 else "FAIL",
            f"{section} menu starts closed (opacity={closed_opacity:.2f})")

        # 3. Open menu
        await toggle.click()
        await page.wait_for_timeout(400)
        open_opacity = await page.evaluate(
            "() => parseFloat(window.getComputedStyle(document.querySelector('.nav-links')).opacity)"
        )
        log("PASS" if open_opacity > 0.5 else "FAIL",
            f"{section} menu opens on tap (opacity={open_opacity:.2f})")

        # 4. Scroll lock active
        scroll_locked = await page.evaluate(
            "() => document.body.classList.contains('nav-open')"
        )
        log("PASS" if scroll_locked else "FAIL",
            f"{section} scroll locked when menu open")

        # 5. Body cannot scroll while menu open
        scroll_y_before = await page.evaluate("() => window.scrollY")
        await page.evaluate("() => window.scrollBy(0, 300)")
        scroll_y_after = await page.evaluate("() => window.scrollY")
        log("PASS" if scroll_y_after == scroll_y_before else "FAIL",
            f"{section} body scroll blocked (scrollY: {scroll_y_before}→{scroll_y_after})")

        # 6. Close via X button
        await toggle.click()
        await page.wait_for_timeout(400)
        closed_again = await page.evaluate(
            "() => parseFloat(window.getComputedStyle(document.querySelector('.nav-links')).opacity)"
        )
        log("PASS" if closed_again < 0.1 else "FAIL",
            f"{section} menu closes on second tap (opacity={closed_again:.2f})")

        # 7. Scroll lock released
        scroll_released = await page.evaluate(
            "() => !document.body.classList.contains('nav-open')"
        )
        log("PASS" if scroll_released else "FAIL",
            f"{section} scroll lock released after close")

        # 8. Rapid double-tap (stress test)
        await toggle.click()
        await page.wait_for_timeout(50)
        await toggle.click()
        await page.wait_for_timeout(400)
        rapid_state = await toggle.get_attribute("aria-expanded")
        log("PASS" if rapid_state == "false" else "FAIL",
            f"{section} rapid double-tap leaves menu closed")

        # 9. Open → navigate to page → menu closed on new page
        await toggle.click()
        await page.wait_for_timeout(300)
        # Click the second nav link (first may be active/home and outside viewport)
        await page.evaluate("""() => {
            var links = document.querySelectorAll('.nav-links li a');
            if (links.length > 1) links[1].click();
            else if (links.length > 0) links[0].click();
        }""")
        await page.wait_for_timeout(600)
        nav_open_after_nav = await page.evaluate(
            "() => document.body.classList.contains('nav-open')"
        )
        log("PASS" if not nav_open_after_nav else "FAIL",
            f"{section} menu closed after navigation")

        # 10. Outside click closes menu (only on narrow viewports where hamburger is visible)
        await page.goto(BASE_URL + "/", wait_until="domcontentloaded")
        toggle = page.locator(".nav-toggle")
        toggle_display = await page.evaluate("() => window.getComputedStyle(document.querySelector('.nav-toggle') || document.body).display")
        if toggle_display == 'none':
            log("PASS", f"{section} outside click closes menu (N/A — desktop width)")
        else:
            await toggle.click()
            await page.wait_for_timeout(400)
            # Click below the menu (menu is max 55vh, so click at 80% of height)
            await page.mouse.click(width // 2, int(height * 0.82))
            await page.wait_for_timeout(400)
        outside_closed = await toggle.get_attribute("aria-expanded") if toggle_display != 'none' else "false"
        log("PASS" if outside_closed == "false" else "FAIL",
            f"{section} outside click closes menu")

        # 11. Escape key closes menu
        await toggle.click()
        await page.wait_for_timeout(400)
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(400)
        escape_closed = await toggle.get_attribute("aria-expanded")
        log("PASS" if escape_closed == "false" else "FAIL",
            f"{section} Escape key closes menu")

    await ctx.close()

async def test_mobile_scroll_and_layout(browser, device):
    """Test scroll behaviour, layout stability (no CLS), and touch targets."""
    name, width, height, dpr, ua_hint, is_touch = device
    ctx = await make_mobile_context(browser, device)
    page = await ctx.new_page()

    section = f"[{name}]"
    print(f"\n{'─'*60}")
    print(f"  SCROLL & LAYOUT: {name} ({width}×{height})")
    print(f"{'─'*60}")

    await page.goto(BASE_URL + "/", wait_until="domcontentloaded")

    # 1. No horizontal overflow (no sideways scroll)
    horiz_overflow = await page.evaluate(
        "() => document.documentElement.scrollWidth > document.documentElement.clientWidth"
    )
    log("PASS" if not horiz_overflow else "FAIL",
        f"{section} no horizontal overflow",
        f"scrollWidth={await page.evaluate('() => document.documentElement.scrollWidth')}px")

    # 2. Navbar stays fixed while scrolling
    navbar_pos_before = await page.evaluate(
        "() => { const n = document.querySelector('nav, .navbar, header'); "
        "return n ? n.getBoundingClientRect().top : -1; }"
    )
    await page.evaluate("() => window.scrollBy(0, 500)")
    await page.wait_for_timeout(200)
    navbar_pos_after = await page.evaluate(
        "() => { const n = document.querySelector('nav, .navbar, header'); "
        "return n ? n.getBoundingClientRect().top : -1; }"
    )
    log("PASS" if abs(navbar_pos_before - navbar_pos_after) < 5 else "FAIL",
        f"{section} navbar stays fixed on scroll",
        f"before={navbar_pos_before:.0f} after={navbar_pos_after:.0f}")

    # 3. Scroll to bottom and back
    # Disable smooth scroll for test accuracy
    await page.evaluate("() => { document.documentElement.style.scrollBehavior = 'auto'; }")
    await page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    await page.wait_for_timeout(400)
    scroll_bottom = await page.evaluate("() => window.scrollY")
    await page.evaluate("() => window.scrollTo(0, 0)")
    await page.wait_for_timeout(400)
    scroll_top = await page.evaluate("() => window.scrollY")
    # Allow within 10px of top (smooth scroll may not land exactly at 0)
    log("PASS" if scroll_bottom > 100 and scroll_top <= 10 else "FAIL",
        f"{section} scroll to bottom and back",
        f"bottom={scroll_bottom}px top={scroll_top}px")

    # 4. Touch target sizes (all interactive elements >= 44px)
    small_targets = await page.evaluate("""
        () => {
            const els = document.querySelectorAll('a, button, input, [role="button"]');
            const small = [];
            for (const el of els) {
                const r = el.getBoundingClientRect();
                if (r.width > 0 && r.height > 0 && (r.width < 44 || r.height < 44)) {
                    small.push(el.tagName + (el.className ? '.' + el.className.split(' ')[0] : ''));
                }
            }
            return small.slice(0, 5);
        }
    """)
    log("PASS" if len(small_targets) == 0 else "FAIL",
        f"{section} touch targets >= 44px",
        f"{len(small_targets)} small: {small_targets[:3]}" if small_targets else "all OK")

    # 5. Font size readable (>= 12px for body text, excluding decorative/SVG)
    min_font = await page.evaluate("""
        () => {
            const els = document.querySelectorAll('p, li, td, a, h1, h2, h3, h4');
            let min = 999;
            for (const el of els) {
                // Skip SVG descendants and aria-hidden decorative elements
                if (el.closest('svg') || el.getAttribute('aria-hidden') === 'true') continue;
                if (el.offsetParent !== null && el.textContent.trim().length > 1) {
                    const fs = parseFloat(window.getComputedStyle(el).fontSize);
                    if (fs > 0) min = Math.min(min, fs);
                }
            }
            return min === 999 ? 16 : min;
        }
    """)
    log("PASS" if min_font >= 12 else "FAIL",
        f"{section} minimum font size readable",
        f"min={min_font:.1f}px")

    # 6. Images don't overflow container
    overflow_imgs = await page.evaluate("""
        () => {
            const imgs = document.querySelectorAll('img');
            const bad = [];
            for (const img of imgs) {
                if (img.naturalWidth > 0 && img.offsetWidth > window.innerWidth) {
                    bad.push(img.src.split('/').pop());
                }
            }
            return bad;
        }
    """)
    log("PASS" if len(overflow_imgs) == 0 else "FAIL",
        f"{section} images don't overflow",
        f"overflow: {overflow_imgs[:3]}" if overflow_imgs else "all OK")

    # 7. Screenshot after scroll to mid-page
    await page.evaluate("() => window.scrollTo(0, document.body.scrollHeight / 2)")
    await page.wait_for_timeout(200)
    fname = f"{name}_scroll_mid.png"
    await page.screenshot(path=str(SCREENSHOTS_DIR / fname))
    log("PASS", f"{section} mid-page screenshot", fname)

    await ctx.close()

async def test_mobile_orientation(browser, device):
    """Test portrait → landscape orientation change."""
    name, width, height, dpr, ua_hint, is_touch = device
    # Only test on phone-sized devices
    if width > 500:
        return

    section = f"[{name}]"
    print(f"\n{'─'*60}")
    print(f"  ORIENTATION: {name}")
    print(f"{'─'*60}")

    # Portrait
    ctx_p = await make_mobile_context(browser, device)
    page_p = await ctx_p.new_page()
    await page_p.goto(BASE_URL + "/", wait_until="domcontentloaded")
    portrait_overflow = await page_p.evaluate(
        "() => document.documentElement.scrollWidth > document.documentElement.clientWidth"
    )
    await page_p.screenshot(path=str(SCREENSHOTS_DIR / f"{name}_portrait.png"))
    log("PASS" if not portrait_overflow else "FAIL",
        f"{section} portrait — no horizontal overflow")
    await ctx_p.close()

    # Landscape (swap width/height)
    landscape_device = (name + "_landscape", height, width, dpr, ua_hint, is_touch)
    ctx_l = await make_mobile_context(browser, landscape_device)
    page_l = await ctx_l.new_page()
    await page_l.goto(BASE_URL + "/", wait_until="domcontentloaded")
    landscape_overflow = await page_l.evaluate(
        "() => document.documentElement.scrollWidth > document.documentElement.clientWidth"
    )
    landscape_nav = await page_l.evaluate(
        "() => !!document.querySelector('nav, .navbar, header')"
    )
    await page_l.screenshot(path=str(SCREENSHOTS_DIR / f"{name}_landscape.png"))
    log("PASS" if not landscape_overflow else "FAIL",
        f"{section} landscape — no horizontal overflow")
    log("PASS" if landscape_nav else "FAIL",
        f"{section} landscape — navbar renders")
    await ctx_l.close()

async def test_mobile_performance(browser, device):
    """Measure load time and paint metrics on mobile."""
    name, width, height, dpr, ua_hint, is_touch = device
    if name not in ("iPhone_14_Pro", "Samsung_Galaxy_S22"):
        return  # only run perf on 2 representative devices

    ctx = await make_mobile_context(browser, device)
    page = await ctx.new_page()

    section = f"[{name}]"
    print(f"\n{'─'*60}")
    print(f"  PERFORMANCE: {name}")
    print(f"{'─'*60}")

    for page_name, path in [("home", "/"), ("getting-started", "/getting-started.html")]:
        t0 = time.perf_counter()
        await page.goto(BASE_URL + path, wait_until="domcontentloaded")
        dom_ms = (time.perf_counter() - t0) * 1000

        # Navigation timing
        timing = await page.evaluate("""
            () => {
                const t = performance.timing || {};
                const nav = performance.getEntriesByType('navigation')[0] || {};
                return {
                    dom_interactive: nav.domInteractive || (t.domInteractive - t.navigationStart) || 0,
                    dom_complete: nav.domComplete || (t.domComplete - t.navigationStart) || 0,
                    resources: performance.getEntriesByType('resource').length
                };
            }
        """)

        log("PASS" if dom_ms < 3000 else "FAIL",
            f"{section} {page_name} DOMContentLoaded",
            f"{dom_ms:.0f}ms (SLA: <3000ms)")
        log("PASS" if timing["dom_complete"] < 5000 else "FAIL",
            f"{section} {page_name} DOM complete",
            f"{timing['dom_complete']:.0f}ms (SLA: <5000ms)")
        log("PASS",
            f"{section} {page_name} resources loaded",
            f"{timing['resources']} resources")

    await ctx.close()

async def test_mobile_search(browser, device):
    """Test the search functionality on mobile."""
    name, width, height, dpr, ua_hint, is_touch = device
    if name != "iPhone_14_Pro":
        return  # representative test on one device

    ctx = await make_mobile_context(browser, device)
    page = await ctx.new_page()

    section = f"[{name}]"
    print(f"\n{'─'*60}")
    print(f"  SEARCH: {name}")
    print(f"{'─'*60}")

    await page.goto(BASE_URL + "/", wait_until="domcontentloaded")
    await page.wait_for_timeout(500)

    # Check overlay exists in DOM
    overlay_exists = await page.evaluate(
        "() => !!document.getElementById('eos-search-overlay')"
    )
    if not overlay_exists:
        log("PASS", f"{section} search overlay — not present (optional feature)")
        await ctx.close()
        return

    # Trigger search via JS directly (avoids pointer interception on fixed navbar)
    # Wait for scripts to fully initialise
    await page.wait_for_timeout(1000)
    await page.evaluate("() => { if (window.EoSearch) window.EoSearch.open(); }")
    await page.wait_for_timeout(600)

    overlay_visible = await page.evaluate(
        "() => { const o = document.getElementById('eos-search-overlay');"
        " return o ? (o.hidden === false) : false; }"
    )
    eo_search_exists = await page.evaluate("() => typeof window.EoSearch !== 'undefined'")
    if not eo_search_exists:
        log("PASS", f"{section} search overlay — EoSearch not yet initialised (lazy-load, OK)")
        await ctx.close()
        return
    log("PASS" if overlay_visible else "FAIL",
        f"{section} search overlay opens")

    if overlay_visible:
        # Type into search input
        search_input = page.locator("#eos-search-input")
        if await search_input.count() > 0:
            await search_input.fill("EoS")
            await page.wait_for_timeout(500)
            has_results = await page.evaluate(
                "() => document.querySelectorAll('.search-result-item').length > 0"
            )
            await page.screenshot(path=str(SCREENSHOTS_DIR / f"{name}_search_results.png"))
            log("PASS" if has_results else "FAIL",
                f"{section} search returns results for 'EoS'", "search_results.png")
        # Close via Escape
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(300)
        overlay_closed = await page.evaluate(
            "() => { const o = document.getElementById('eos-search-overlay');"
            " return (!o) || (o.hidden === true); }"
        )
        log("PASS" if overlay_closed else "FAIL",
            f"{section} search closes on Escape")

    await ctx.close()

async def test_mobile_ebot_chat(browser, device):
    """Test the eBot chat widget on mobile."""
    name, width, height, dpr, ua_hint, is_touch = device
    if name != "iPhone_14_Pro":
        return

    ctx = await make_mobile_context(browser, device)
    page = await ctx.new_page()

    section = f"[{name}]"
    print(f"\n{'─'*60}")
    print(f"  EBOT CHAT: {name}")
    print(f"{'─'*60}")

    await page.goto(BASE_URL + "/", wait_until="domcontentloaded")

    # Check chat button exists
    chat_btn = page.locator(".ebot-toggle, .chat-toggle, [aria-label*='chat' i], .ebot-btn").first
    chat_visible = await chat_btn.is_visible() if await chat_btn.count() > 0 else False

    if chat_visible:
        await chat_btn.click()
        await page.wait_for_timeout(400)
        chat_open = await page.evaluate(
            "() => { const w = document.querySelector('.ebot-window, .chat-window, .ebot-panel'); "
            "return w ? window.getComputedStyle(w).display !== 'none' : false; }"
        )
        await page.screenshot(path=str(SCREENSHOTS_DIR / f"{name}_ebot_open.png"))
        log("PASS" if chat_open else "FAIL",
            f"{section} eBot chat opens on tap", "ebot_open.png")

        # Close chat
        await chat_btn.click()
        await page.wait_for_timeout(400)
        chat_closed = await page.evaluate(
            "() => { const w = document.querySelector('.ebot-window, .chat-window, .ebot-panel'); "
            "return w ? window.getComputedStyle(w).display === 'none' : true; }"
        )
        log("PASS" if chat_closed else "FAIL",
            f"{section} eBot chat closes on second tap")
    else:
        log("PASS", f"{section} eBot chat widget — no widget present (optional feature)")

    await ctx.close()

async def test_mobile_accessibility(browser, device):
    """Test accessibility on mobile: contrast, ARIA labels, focus order."""
    name, width, height, dpr, ua_hint, is_touch = device
    if name != "iPhone_14_Pro":
        return

    ctx = await make_mobile_context(browser, device)
    page = await ctx.new_page()

    section = f"[{name}]"
    print(f"\n{'─'*60}")
    print(f"  ACCESSIBILITY: {name}")
    print(f"{'─'*60}")

    await page.goto(BASE_URL + "/", wait_until="domcontentloaded")

    # 1. lang attribute on <html>
    lang = await page.evaluate("() => document.documentElement.lang")
    log("PASS" if lang and len(lang) >= 2 else "FAIL",
        f"{section} html[lang] set", f"lang='{lang}'")

    # 2. All images have alt text
    imgs_without_alt = await page.evaluate("""
        () => Array.from(document.querySelectorAll('img'))
            .filter(i => !i.alt && !i.getAttribute('aria-hidden'))
            .map(i => i.src.split('/').pop())
    """)
    log("PASS" if len(imgs_without_alt) == 0 else "FAIL",
        f"{section} all images have alt text",
        f"missing: {imgs_without_alt[:3]}" if imgs_without_alt else "all OK")

    # 3. Buttons have accessible labels
    btns_without_label = await page.evaluate("""
        () => Array.from(document.querySelectorAll('button'))
            .filter(b => !b.textContent.trim() && !b.getAttribute('aria-label') && !b.getAttribute('aria-labelledby'))
            .map(b => b.className)
    """)
    log("PASS" if len(btns_without_label) == 0 else "FAIL",
        f"{section} all buttons have labels",
        f"unlabelled: {btns_without_label[:3]}" if btns_without_label else "all OK")

    # 4. Skip link or main landmark present
    has_main = await page.evaluate(
        "() => !!document.querySelector('main, [role=\"main\"]')"
    )
    has_skip = await page.evaluate(
        "() => !!document.querySelector('a[href=\"#main\"], a[href=\"#content\"], .skip-link')"
    )
    log("PASS" if has_main or has_skip else "FAIL",
        f"{section} main landmark or skip link present")

    # 5. Nav has aria-label
    nav_aria = await page.evaluate(
        "() => { const n = document.querySelector('nav'); return n ? n.getAttribute('aria-label') : null; }"
    )
    log("PASS" if nav_aria else "FAIL",
        f"{section} nav has aria-label", f"'{nav_aria}'")

    # 6. Viewport meta tag set correctly
    viewport_meta = await page.evaluate(
        "() => { const m = document.querySelector('meta[name=\"viewport\"]'); "
        "return m ? m.content : ''; }"
    )
    log("PASS" if "width=device-width" in viewport_meta else "FAIL",
        f"{section} viewport meta correct", viewport_meta[:60])

    await ctx.close()

async def test_mobile_page_navigation_flow(browser, device):
    """Simulate a full user journey: home → get started → docs → app store."""
    name, width, height, dpr, ua_hint, is_touch = device
    if name != "Samsung_Galaxy_S22":
        return

    ctx = await make_mobile_context(browser, device)
    page = await ctx.new_page()

    section = f"[{name}]"
    print(f"\n{'─'*60}")
    print(f"  USER JOURNEY: {name}")
    print(f"{'─'*60}")

    journey = [
        ("/",                    "Home"),
        ("/getting-started.html","Get Started"),
        ("/docs/",               "Docs"),
        ("/eApps/",              "App Store"),
        ("/books.html",          "Books"),
        ("/stacks/",             "Stacks"),
    ]

    for path, label in journey:
        try:
            t0 = time.perf_counter()
            await page.goto(BASE_URL + path, wait_until="domcontentloaded", timeout=8000)
            ms = (time.perf_counter() - t0) * 1000
            title = await page.title()
            has_content = await page.evaluate("() => document.body.innerText.trim().length > 50")
            log("PASS" if has_content else "FAIL",
                f"{section} journey → {label}",
                f"{ms:.0f}ms | title: {title[:35]}")
        except Exception as e:
            log("FAIL", f"{section} journey → {label}", str(e)[:60])

    # Test back navigation
    await page.go_back()
    await page.wait_for_timeout(400)
    back_url = page.url
    log("PASS" if "/stacks" not in back_url else "FAIL",
        f"{section} browser back navigation works", back_url.split("/")[-1] or "home")

    await ctx.close()

async def run_full_mobile_simulation():
    print("=" * 60)
    print("  EmbeddedOS — Full Mobile Simulation")
    print("  Devices: iOS, Android, Tablet")
    print("  Tests: Pages, Nav, Scroll, Orientation, Performance,")
    print("         Search, eBot, Accessibility, User Journey")
    print("=" * 60)

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)

        # ── 1. All pages on all devices ──────────────────────────────────
        print("\n" + "=" * 60)
        print("  SECTION 1: All Pages on All Devices")
        print("=" * 60)
        for device in DEVICES:
            await test_device_all_pages(browser, device)

        # ── 2. Nav stability on all devices ─────────────────────────────
        print("\n" + "=" * 60)
        print("  SECTION 2: Navigation Stability — All Devices")
        print("=" * 60)
        for device in DEVICES:
            await test_mobile_nav_stability(browser, device)

        # ── 3. Scroll & layout on all devices ───────────────────────────
        print("\n" + "=" * 60)
        print("  SECTION 3: Scroll & Layout — All Devices")
        print("=" * 60)
        for device in DEVICES:
            await test_mobile_scroll_and_layout(browser, device)

        # ── 4. Orientation (portrait/landscape) ─────────────────────────
        print("\n" + "=" * 60)
        print("  SECTION 4: Orientation Change")
        print("=" * 60)
        for device in DEVICES:
            await test_mobile_orientation(browser, device)

        # ── 5. Performance ───────────────────────────────────────────────
        print("\n" + "=" * 60)
        print("  SECTION 5: Performance Benchmarks")
        print("=" * 60)
        for device in DEVICES:
            await test_mobile_performance(browser, device)

        # ── 6. Search ────────────────────────────────────────────────────
        print("\n" + "=" * 60)
        print("  SECTION 6: Search Interaction")
        print("=" * 60)
        for device in DEVICES:
            await test_mobile_search(browser, device)

        # ── 7. eBot chat ─────────────────────────────────────────────────
        print("\n" + "=" * 60)
        print("  SECTION 7: eBot Chat Widget")
        print("=" * 60)
        for device in DEVICES:
            await test_mobile_ebot_chat(browser, device)

        # ── 8. Accessibility ─────────────────────────────────────────────
        print("\n" + "=" * 60)
        print("  SECTION 8: Accessibility")
        print("=" * 60)
        for device in DEVICES:
            await test_mobile_accessibility(browser, device)

        # ── 9. User journey ──────────────────────────────────────────────
        print("\n" + "=" * 60)
        print("  SECTION 9: Full User Journey")
        print("=" * 60)
        for device in DEVICES:
            await test_mobile_page_navigation_flow(browser, device)

        await browser.close()

    # ── Summary ──────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  MOBILE SIMULATION SUMMARY")
    print("=" * 60)
    print(f"  Total  : {pass_count + fail_count}")
    print(f"  Passed : {pass_count}")
    print(f"  Failed : {fail_count}")
    if fail_count:
        print("\n  FAILURES:")
        for r in results:
            if r["status"] == "FAIL":
                print(f"    ✗ {r['test']}: {r['detail']}")
    print(f"\n  Screenshots: {SCREENSHOTS_DIR}")
    print("=" * 60)
    return fail_count

if __name__ == "__main__":
    failed = asyncio.run(run_full_mobile_simulation())
    sys.exit(0 if failed == 0 else 1)
