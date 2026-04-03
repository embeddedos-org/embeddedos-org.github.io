// @ts-check
const { test, expect } = require('@playwright/test');

const BASE = process.env.BASE_URL || 'http://localhost:8080';

const PAGES = [
  { name: 'Home',         path: '/index.html' },
  { name: 'Get Started',  path: '/getting-started.html' },
  { name: 'Docs Hub',     path: '/docs/index.html' },
  { name: 'Flow',         path: '/flow.html' },
  { name: 'Kids',         path: '/kids.html' },
  { name: 'Hardware Lab', path: '/hardware-lab.html' },
];

const VIEWPORTS = {
  'iPhone SE':      { width: 375,  height: 667 },
  'iPhone 14 Pro':  { width: 393,  height: 852 },
  'iPad':           { width: 768,  height: 1024 },
  'Laptop':         { width: 1280, height: 800 },
  'Desktop 1080p':  { width: 1920, height: 1080 },
};

const fs = require('fs');
const path = require('path');
const screenshotDir = path.join(__dirname, 'screenshots');
fs.mkdirSync(screenshotDir, { recursive: true });

// ─── SANITY: Every page loads without errors ───
test.describe('Page Load Sanity', () => {
  for (const page of PAGES) {
    test(`${page.name} loads without console errors`, async ({ browser }) => {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const p = await ctx.newPage();
      const errors = [];
      p.on('pageerror', (err) => errors.push(err.message));

      const response = await p.goto(`${BASE}${page.path}`, { waitUntil: 'domcontentloaded' });
      expect(response.status()).toBeLessThan(400);

      // Check page has content
      const bodyText = await p.textContent('body');
      expect(bodyText.length).toBeGreaterThan(50);

      // No JS errors
      expect(errors).toEqual([]);
      await ctx.close();
    });
  }
});

// ─── STRUCTURE: Required elements exist ───
test.describe('HTML Structure', () => {
  for (const page of PAGES) {
    test(`${page.name} has navbar and footer`, async ({ browser }) => {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const p = await ctx.newPage();
      await p.goto(`${BASE}${page.path}`, { waitUntil: 'domcontentloaded' });

      // Must have navbar
      const navbar = await p.$('.navbar');
      expect(navbar).not.toBeNull();

      // Must have footer
      const footer = await p.$('.footer');
      expect(footer).not.toBeNull();

      // Must have title
      const title = await p.title();
      expect(title.length).toBeGreaterThan(3);
      expect(title).toContain('EmbeddedOS');

      await ctx.close();
    });
  }
});

// ─── MOBILE: No horizontal overflow ───
test.describe('Mobile Layout', () => {
  for (const page of PAGES) {
    test(`${page.name} has no horizontal overflow on mobile`, async ({ browser }) => {
      const ctx = await browser.newContext({ viewport: { width: 375, height: 667 } });
      const p = await ctx.newPage();
      await p.goto(`${BASE}${page.path}`, { waitUntil: 'domcontentloaded' });
      await p.waitForTimeout(300);

      const overflow = await p.evaluate(() => {
        return document.documentElement.scrollWidth > document.documentElement.clientWidth + 10;
      });
      expect(overflow, `${page.name} overflows horizontally on mobile`).toBe(false);

      await p.screenshot({
        path: path.join(screenshotDir, `${page.name.toLowerCase().replace(/\s+/g, '-')}-mobile.png`),
        fullPage: true
      });
      await ctx.close();
    });
  }
});

// ─── MOBILE NAV: Hamburger menu works ───
test.describe('Mobile Navigation', () => {
  for (const page of PAGES) {
    test(`${page.name} hamburger menu toggles`, async ({ browser }) => {
      const ctx = await browser.newContext({ viewport: { width: 375, height: 667 } });
      const p = await ctx.newPage();
      await p.goto(`${BASE}${page.path}`, { waitUntil: 'domcontentloaded' });

      const toggle = await p.$('.nav-toggle');
      if (!toggle) {
        test.skip();
        return;
      }

      // Nav links should be hidden on mobile
      const navLinks = await p.$('.nav-links');
      const isVisible = await navLinks.evaluate((el) => {
        const style = window.getComputedStyle(el);
        return style.display !== 'none';
      });

      // Click hamburger - nav should open
      await toggle.click();
      await p.waitForTimeout(200);
      const isOpen = await p.$('.nav-links.open');
      expect(isOpen).not.toBeNull();

      await ctx.close();
    });
  }
});

// ─── DESKTOP: Layout renders correctly ───
test.describe('Desktop Layout', () => {
  for (const page of PAGES) {
    test(`${page.name} renders correctly at 1920x1080`, async ({ browser }) => {
      const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
      const p = await ctx.newPage();
      await p.goto(`${BASE}${page.path}`, { waitUntil: 'domcontentloaded' });
      await p.waitForTimeout(300);

      // No horizontal overflow
      const overflow = await p.evaluate(() => {
        return document.documentElement.scrollWidth > document.documentElement.clientWidth + 10;
      });
      expect(overflow).toBe(false);

      // Content has reasonable height
      const height = await p.evaluate(() => document.documentElement.scrollHeight);
      expect(height).toBeGreaterThan(500);

      await p.screenshot({
        path: path.join(screenshotDir, `${page.name.toLowerCase().replace(/\s+/g, '-')}-desktop.png`),
        fullPage: true
      });
      await ctx.close();
    });
  }
});

// ─── RESPONSIVE: All viewports render without overflow ───
test.describe('Multi-Viewport Responsive', () => {
  for (const [vpName, vpSize] of Object.entries(VIEWPORTS)) {
    test(`Home page at ${vpName} (${vpSize.width}x${vpSize.height})`, async ({ browser }) => {
      const ctx = await browser.newContext({ viewport: vpSize });
      const p = await ctx.newPage();
      await p.goto(`${BASE}/index.html`, { waitUntil: 'domcontentloaded' });
      await p.waitForTimeout(300);

      const overflow = await p.evaluate(() => {
        return document.documentElement.scrollWidth > document.documentElement.clientWidth + 10;
      });
      expect(overflow, `Horizontal overflow at ${vpName}`).toBe(false);

      // Navbar should be visible
      const navbar = await p.$('.navbar');
      const navVisible = await navbar.evaluate(el => {
        const rect = el.getBoundingClientRect();
        return rect.height > 0;
      });
      expect(navVisible).toBe(true);

      await ctx.close();
    });
  }
});

// ─── NAVIGATION: Internal links work ───
test.describe('Navigation Links', () => {
  test('Home page nav links resolve', async ({ browser }) => {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const p = await ctx.newPage();
    await p.goto(`${BASE}/index.html`, { waitUntil: 'domcontentloaded' });

    const links = await p.$$eval('.nav-links a[href]', (anchors) =>
      anchors.map(a => a.getAttribute('href')).filter(h => h && !h.startsWith('http') && !h.startsWith('#'))
    );

    for (const link of links) {
      const url = new URL(link, `${BASE}/index.html`).href;
      const response = await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 10000 });
      expect(response.status(), `Broken nav link: ${link}`).toBeLessThan(400);
    }
    await ctx.close();
  });

  test('Docs hub links resolve', async ({ browser }) => {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const p = await ctx.newPage();
    await p.goto(`${BASE}/docs/index.html`, { waitUntil: 'domcontentloaded' });

    const links = await p.$$eval('a[href$=".html"]', (anchors) =>
      anchors.map(a => a.getAttribute('href')).filter(h => h && !h.startsWith('http'))
    );

    const unique = [...new Set(links)];
    for (const link of unique.slice(0, 20)) {
      const url = new URL(link, `${BASE}/docs/index.html`).href;
      const response = await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 10000 });
      expect(response.status(), `Broken docs link: ${link}`).toBeLessThan(400);
    }
    await ctx.close();
  });
});

// ─── INTERACTIVE: Getting Started path switcher works ───
test.describe('Interactive Elements', () => {
  test('Getting Started path selector works', async ({ browser }) => {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const p = await ctx.newPage();
    await p.goto(`${BASE}/getting-started.html`, { waitUntil: 'domcontentloaded' });

    // Default path should be visible
    const simPath = await p.$('#path-sim');
    if (simPath) {
      const isActive = await simPath.evaluate(el => el.classList.contains('active'));
      expect(isActive).toBe(true);
    }

    // Click STM32 path button
    const stm32Btn = await p.$('.path-btn:nth-child(3)');
    if (stm32Btn) {
      await stm32Btn.click();
      await p.waitForTimeout(300);
      const stm32Path = await p.$('#path-stm32');
      if (stm32Path) {
        const isActive = await stm32Path.evaluate(el => el.classList.contains('active'));
        expect(isActive).toBe(true);
      }
    }
    await ctx.close();
  });
});
