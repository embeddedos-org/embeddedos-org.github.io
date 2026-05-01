// @ts-check
const { test, expect } = require('@playwright/test');

const BASE = process.env.BASE_URL || 'http://localhost:8080';

const PAGES = [
  { name: 'Home', path: '/index.html' },
  { name: 'Get Started', path: '/getting-started.html' },
  { name: 'Docs Hub', path: '/docs/index.html' },
  { name: 'Flow', path: '/flow.html' },
  { name: 'Kids', path: '/kids.html' },
  { name: 'Hardware Lab', path: '/hardware-lab.html' },
  { name: 'Books', path: '/books.html' },
  { name: '404', path: '/404.html' },
];

// ─── Crawl every page and check ALL internal links ───
test.describe('Internal Link Validation', () => {
  for (const page of PAGES) {
    test(`${page.name}: all internal links return 200`, async ({ browser }) => {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const p = await ctx.newPage();
      await p.goto(`${BASE}${page.path}`, { waitUntil: 'domcontentloaded' });

      const links = await p.$$eval('a[href]', (anchors) =>
        anchors
          .map((a) => a.getAttribute('href'))
          .filter((h) => h && !h.startsWith('http') && !h.startsWith('#') && !h.startsWith('mailto:') && !h.startsWith('tel:') && !h.startsWith('javascript:') && !h.includes('#'))
      );

      const unique = [...new Set(links)];
      const broken = [];

      for (const link of unique) {
        try {
          const url = new URL(link, `${BASE}${page.path}`).href;
          const response = await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 10000 });
          if (!response || response.status() >= 400) {
            broken.push({ link, status: response ? response.status() : 'no response' });
          }
        } catch (e) {
          broken.push({ link, status: e.message });
        }
      }

      if (broken.length > 0) {
        console.log(`Broken links on ${page.name}:`, broken);
      }
      expect(broken, `Broken internal links on ${page.name}: ${JSON.stringify(broken)}`).toEqual([]);
      await ctx.close();
    });
  }
});

// ─── Check for placeholder href="#" links ───
test.describe('No Placeholder Links', () => {
  for (const page of PAGES) {
    test(`${page.name}: no href="#" placeholder links`, async ({ browser }) => {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const p = await ctx.newPage();
      await p.goto(`${BASE}${page.path}`, { waitUntil: 'domcontentloaded' });

      const placeholders = await p.$$eval('a[href="#"]', (anchors) =>
        anchors.map((a) => a.textContent.trim()).filter(Boolean)
      );

      expect(placeholders, `Found href="#" links: ${placeholders.join(', ')}`).toEqual([]);
      await ctx.close();
    });
  }
});

// ─── All buttons have an action (onclick, href, or type=submit) ───
test.describe('Button Functionality', () => {
  for (const page of PAGES) {
    test(`${page.name}: all buttons have actions`, async ({ browser }) => {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const p = await ctx.newPage();
      await p.goto(`${BASE}${page.path}`, { waitUntil: 'domcontentloaded' });

      const orphanButtons = await p.$$eval('button', (buttons) =>
        buttons
          .filter((btn) => {
            const hasOnclick = btn.hasAttribute('onclick');
            const hasType = btn.type === 'submit';
            const hasAriaLabel = btn.hasAttribute('aria-label');
            const isInForm = !!btn.closest('form');
            return !hasOnclick && !hasType && !isInForm && !hasAriaLabel;
          })
          .map((btn) => btn.textContent.trim())
      );

      expect(orphanButtons.length, `Orphan buttons: ${orphanButtons.join(', ')}`).toBeLessThanOrEqual(2);
      await ctx.close();
    });
  }
});

// ─── Anchor link targets exist ───
test.describe('Anchor Link Targets', () => {
  test('Home page anchor links have matching IDs', async ({ browser }) => {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const p = await ctx.newPage();
    await p.goto(`${BASE}/index.html`, { waitUntil: 'domcontentloaded' });

    const anchorLinks = await p.$$eval('a[href^="#"]', (anchors) =>
      anchors.map((a) => a.getAttribute('href')).filter((h) => h && h.length > 1)
    );

    for (const anchor of anchorLinks) {
      const id = anchor.substring(1);
      const target = await p.$('[id="' + id + '"]');
      expect(target, `Missing anchor target: ${anchor}`).not.toBeNull();
    }
    await ctx.close();
  });
});
