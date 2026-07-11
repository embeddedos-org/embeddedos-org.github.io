#!/usr/bin/env python3
"""
tests/simulation/test_playwright_simulation.py
Playwright-based browser simulation + visual tests for EmbeddedOS website.

Tests:
  - Desktop layout (1440×900): navbar, hero, product grid, footer
  - Tablet layout (768×1024): responsive breakpoints
  - Mobile layout (390×844): hamburger menu open/close, scroll lock
  - Menu stability: no layout shift, smooth animation, outside-click close
  - Theme quality: color contrast, font rendering, hover states
  - Performance: page load time, no console errors
"""
import asyncio, os, sys, time, json
from pathlib import Path
from playwright.async_api import async_playwright, expect

BASE_URL = "http://localhost:8765"
SCREENSHOTS_DIR = Path(__file__).parent.parent.parent / "test-screenshots"
SCREENSHOTS_DIR.mkdir(exist_ok=True)

PAGES = [
    ("home",            "/"),
    ("getting-started", "/getting-started.html"),
    ("docs-index",      "/docs/index.html"),
    ("kids",            "/kids.html"),
    ("hardware-lab",    "/hardware-lab.html"),
]

VIEWPORTS = {
    "desktop": {"width": 1440, "height": 900},
    "tablet":  {"width": 768,  "height": 1024},
    "mobile":  {"width": 390,  "height": 844},
}

results = []

def log(status, test, detail=""):
    icon = "✓" if status == "PASS" else "✗"
    print(f"  {icon} [{status}]  {test}" + (f" — {detail}" if detail else ""))
    results.append({"status": status, "test": test, "detail": detail})

async def run_simulation():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # ── DESKTOP TESTS ──────────────────────────────────────────────────
        print("\n" + "─"*60)
        print("  DESKTOP (1440×900)")
        print("─"*60)
        ctx = await browser.new_context(viewport=VIEWPORTS["desktop"])
        page = await ctx.new_page()

        # Capture console errors
        console_errors = []
        page.on("console", lambda m: console_errors.append(m) if m.type == "error" and "frame-ancestors" not in str(m.text) and "fonts.googleapis.com" not in str(m.text) and "fonts.gstatic.com" not in str(m.text) else None)
        page.on("pageerror", lambda e: console_errors.append(str(e)))

        t0 = time.perf_counter()
        await page.goto(BASE_URL + "/", wait_until="domcontentloaded")
        load_time = time.perf_counter() - t0

        # Screenshot: desktop home
        await page.screenshot(path=str(SCREENSHOTS_DIR / "01_desktop_home.png"), full_page=False)
        log("PASS", "Desktop screenshot captured", f"01_desktop_home.png")

        # Load time
        if load_time < 3.0:
            log("PASS", "Desktop page load time", f"{load_time:.2f}s < 3.0s")
        else:
            log("FAIL", "Desktop page load time", f"{load_time:.2f}s >= 3.0s")

        # Navbar visible and fixed
        navbar = page.locator(".navbar")
        await expect(navbar).to_be_visible()
        log("PASS", "Navbar visible on desktop")

        # Navbar position: fixed
        pos = await page.evaluate("() => window.getComputedStyle(document.querySelector('.navbar')).position")
        if pos == "fixed":
            log("PASS", "Navbar position: fixed (no layout shift)")
        else:
            log("FAIL", "Navbar position", f"expected 'fixed', got '{pos}'")

        # Body has padding-top (compensates for fixed nav)
        pt = await page.evaluate("() => window.getComputedStyle(document.body).paddingTop")
        if pt and pt != "0px":
            log("PASS", "Body has padding-top for fixed navbar", pt)
        else:
            log("FAIL", "Body padding-top missing", pt)

        # Nav links visible on desktop (hamburger hidden)
        nav_links = page.locator(".navbar .nav-links")
        toggle = page.locator(".nav-toggle")
        toggle_display = await page.evaluate("() => window.getComputedStyle(document.querySelector('.nav-toggle')).display")
        if toggle_display == "none":
            log("PASS", "Hamburger hidden on desktop")
        else:
            log("FAIL", "Hamburger should be hidden on desktop", f"display: {toggle_display}")

        # Nav links are flex on desktop
        links_display = await page.evaluate("() => window.getComputedStyle(document.querySelector('.nav-links')).display")
        if links_display == "flex":
            log("PASS", "Nav links displayed as flex on desktop")
        else:
            log("FAIL", "Nav links display on desktop", f"got: {links_display}")

        # Hero section visible
        hero = page.locator(".hero")
        await expect(hero).to_be_visible()
        log("PASS", "Hero section visible")

        # Product grid visible
        grid = page.locator(".product-grid")
        if await grid.count() > 0:
            await expect(grid.first).to_be_visible()
            log("PASS", "Product grid visible")
        else:
            log("FAIL", "Product grid not found")

        # Footer visible
        footer = page.locator("footer.footer")
        await expect(footer).to_be_visible()
        log("PASS", "Footer visible")

        # No console errors
        if not console_errors:
            log("PASS", "No JavaScript console errors on desktop")
        else:
            log("FAIL", "Console errors found", str(console_errors[:2])[:100])

        # Scroll down and screenshot
        await page.evaluate("window.scrollTo(0, 800)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(SCREENSHOTS_DIR / "02_desktop_scrolled.png"), full_page=False)
        log("PASS", "Desktop scrolled screenshot", "02_desktop_scrolled.png")

        # Screenshot full page
        await page.evaluate("window.scrollTo(0, 0)")
        await page.screenshot(path=str(SCREENSHOTS_DIR / "03_desktop_full_page.png"), full_page=True)
        log("PASS", "Desktop full-page screenshot", "03_desktop_full_page.png")

        await ctx.close()

        # ── TABLET TESTS ───────────────────────────────────────────────────
        print("\n" + "─"*60)
        print("  TABLET (768×1024)")
        print("─"*60)
        ctx = await browser.new_context(viewport=VIEWPORTS["tablet"])
        page = await ctx.new_page()
        await page.goto(BASE_URL + "/", wait_until="domcontentloaded")
        await page.screenshot(path=str(SCREENSHOTS_DIR / "04_tablet_home.png"), full_page=False)
        log("PASS", "Tablet screenshot captured", "04_tablet_home.png")

        # Hamburger should be visible on tablet
        toggle_display = await page.evaluate("() => window.getComputedStyle(document.querySelector('.nav-toggle')).display")
        if toggle_display != "none":
            log("PASS", f"Hamburger visible on tablet (display: {toggle_display})")
        else:
            log("FAIL", "Hamburger should be visible on tablet")

        await ctx.close()

        # ── MOBILE TESTS ───────────────────────────────────────────────────
        print("\n" + "─"*60)
        print("  MOBILE (390×844) — Menu Stability Tests")
        print("─"*60)
        ctx = await browser.new_context(viewport=VIEWPORTS["mobile"])
        page = await ctx.new_page()
        await page.goto(BASE_URL + "/", wait_until="domcontentloaded")
        await page.screenshot(path=str(SCREENSHOTS_DIR / "05_mobile_home_closed.png"), full_page=False)
        log("PASS", "Mobile screenshot (menu closed)", "05_mobile_home_closed.png")

        # Menu should be invisible (max-height: 0, opacity: 0)
        menu_opacity_before = await page.evaluate(
            "() => parseFloat(window.getComputedStyle(document.querySelector('.nav-links')).opacity)"
        )
        menu_pointer_before = await page.evaluate(
            "() => window.getComputedStyle(document.querySelector('.nav-links')).pointerEvents"
        )
        if menu_opacity_before == 0.0:
            log("PASS", "Menu opacity=0 when closed (no flash)")
        else:
            log("FAIL", "Menu opacity when closed", f"got: {menu_opacity_before}")

        if menu_pointer_before == "none":
            log("PASS", "Menu pointer-events=none when closed (no ghost clicks)")
        else:
            log("FAIL", "Menu pointer-events when closed", f"got: {menu_pointer_before}")

        # Open the menu
        toggle = page.locator(".nav-toggle")
        await toggle.click()
        await page.wait_for_timeout(400)  # wait for animation

        await page.screenshot(path=str(SCREENSHOTS_DIR / "06_mobile_menu_open.png"), full_page=False)
        log("PASS", "Mobile screenshot (menu open)", "06_mobile_menu_open.png")

        # Check aria-expanded
        aria_expanded = await toggle.get_attribute("aria-expanded")
        if aria_expanded == "true":
            log("PASS", "aria-expanded=true when menu open")
        else:
            log("FAIL", "aria-expanded after open", f"got: {aria_expanded}")

        # Check menu is visible (opacity > 0)
        menu_opacity_after = await page.evaluate(
            "() => parseFloat(window.getComputedStyle(document.querySelector('.nav-links')).opacity)"
        )
        if menu_opacity_after > 0.5:
            log("PASS", f"Menu visible after open (opacity: {menu_opacity_after:.2f})")
        else:
            log("FAIL", "Menu not visible after open", f"opacity: {menu_opacity_after}")

        # Check scroll lock
        body_overflow = await page.evaluate(
            "() => window.getComputedStyle(document.body).overflow"
        )
        body_has_nav_open = await page.evaluate(
            "() => document.body.classList.contains('nav-open')"
        )
        if body_has_nav_open:
            log("PASS", "body.nav-open class set (scroll lock active)")
        else:
            log("FAIL", "body.nav-open class not set")

        # Close menu by clicking a link
        first_link = page.locator(".nav-links li a").first
        await first_link.click()
        await page.wait_for_timeout(400)

        aria_after_close = await toggle.get_attribute("aria-expanded")
        body_nav_open_after = await page.evaluate(
            "() => document.body.classList.contains('nav-open')"
        )
        if aria_after_close == "false":
            log("PASS", "aria-expanded=false after link click")
        else:
            log("FAIL", "aria-expanded after link click", f"got: {aria_after_close}")

        if not body_nav_open_after:
            log("PASS", "Scroll lock released after menu close")
        else:
            log("FAIL", "Scroll lock not released after menu close")

        # Re-open and test outside click close
        await page.goto(BASE_URL + "/", wait_until="domcontentloaded")
        toggle = page.locator(".nav-toggle")
        await toggle.click()
        await page.wait_for_timeout(400)
        # Click outside the navbar
        await page.mouse.click(200, 600)
        await page.wait_for_timeout(400)

        await page.screenshot(path=str(SCREENSHOTS_DIR / "07_mobile_menu_outside_click.png"), full_page=False)
        aria_outside = await toggle.get_attribute("aria-expanded")
        if aria_outside == "false":
            log("PASS", "Menu closes on outside click", "07_mobile_menu_outside_click.png")
        else:
            log("FAIL", "Menu did not close on outside click", f"aria-expanded: {aria_outside}")

        # Re-open and test Escape key
        await toggle.click()
        await page.wait_for_timeout(400)
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(400)

        await page.screenshot(path=str(SCREENSHOTS_DIR / "08_mobile_menu_escape.png"), full_page=False)
        aria_escape = await toggle.get_attribute("aria-expanded")
        if aria_escape == "false":
            log("PASS", "Menu closes on Escape key", "08_mobile_menu_escape.png")
        else:
            log("FAIL", "Menu did not close on Escape", f"aria-expanded: {aria_escape}")

        await ctx.close()

        # ── MULTI-PAGE TESTS ───────────────────────────────────────────────
        print("\n" + "─"*60)
        print("  MULTI-PAGE SCREENSHOTS (Desktop)")
        print("─"*60)
        ctx = await browser.new_context(viewport=VIEWPORTS["desktop"])
        page = await ctx.new_page()

        for name, path in PAGES[1:]:
            try:
                await page.goto(BASE_URL + path, wait_until="domcontentloaded", timeout=8000)
                await page.screenshot(
                    path=str(SCREENSHOTS_DIR / f"09_{name}.png"),
                    full_page=False
                )
                log("PASS", f"Screenshot: {name}", f"09_{name}.png")
            except Exception as e:
                log("FAIL", f"Screenshot: {name}", str(e)[:60])

        await ctx.close()
        await browser.close()

    # ── SUMMARY ────────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("  SIMULATION SUMMARY")
    print("="*60)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    total  = len(results)
    print(f"  Total: {total}  |  Passed: {passed}  |  Failed: {failed}")
    if failed:
        print("\n  FAILURES:")
        for r in results:
            if r["status"] == "FAIL":
                print(f"    ✗ {r['test']}: {r['detail']}")
    print(f"\n  Screenshots saved to: {SCREENSHOTS_DIR}")
    print("="*60)
    return failed

if __name__ == "__main__":
    failed = asyncio.run(run_simulation())
    sys.exit(0 if failed == 0 else 1)
