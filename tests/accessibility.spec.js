// @ts-check
const { test, expect } = require('@playwright/test');

const BASE = process.env.BASE_URL || 'http://localhost:8080';

const PAGES = [
  { name: 'Home', path: '/index.html' },
  { name: 'Get Started', path: '/getting-started.html' },
  { name: 'Docs Hub', path: '/docs/index.html' },
  { name: 'Books', path: '/books.html' },
  { name: '404', path: '/404.html' },
];

// ─── ARIA landmarks exist ───
test.describe('Accessibility: ARIA Landmarks', () => {
  for (const page of PAGES) {
    test(`${page.name} has navigation landmark`, async ({ browser }) => {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const p = await ctx.newPage();
      await p.goto(`${BASE}${page.path}`, { waitUntil: 'domcontentloaded' });

      const hasNav = await p.$('nav, [role="navigation"]');
      expect(hasNav, `Missing navigation landmark on ${page.name}`).not.toBeNull();
      await ctx.close();
    });
  }
});

// ─── All images have alt text ───
test.describe('Accessibility: Image Alt Text', () => {
  for (const page of PAGES) {
    test(`${page.name}: images have alt attributes`, async ({ browser }) => {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const p = await ctx.newPage();
      await p.goto(`${BASE}${page.path}`, { waitUntil: 'domcontentloaded' });

      const imagesWithoutAlt = await p.$$eval('img', (imgs) =>
        imgs.filter((img) => !img.hasAttribute('alt')).map((img) => img.src)
      );

      expect(imagesWithoutAlt, `Images without alt: ${imagesWithoutAlt.join(', ')}`).toEqual([]);
      await ctx.close();
    });
  }
});

// ─── Decorative SVGs have aria-hidden ───
test.describe('Accessibility: SVG aria-hidden', () => {
  test('Home page inline SVGs have aria-hidden', async ({ browser }) => {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const p = await ctx.newPage();
    await p.goto(`${BASE}/index.html`, { waitUntil: 'domcontentloaded' });

    const decorativeSvgs = await p.$$eval('svg:not([role])', (svgs) =>
      svgs.filter((svg) => !svg.getAttribute('aria-hidden') && !svg.closest('a') && !svg.closest('button'))
        .length
    );

    // Most decorative SVGs should have aria-hidden
    expect(decorativeSvgs).toBeLessThan(5);
    await ctx.close();
  });
});

// ─── Interactive elements are keyboard accessible ───
test.describe('Accessibility: Keyboard Navigation', () => {
  test('Home page buttons and links are focusable', async ({ browser }) => {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const p = await ctx.newPage();
    await p.goto(`${BASE}/index.html`, { waitUntil: 'domcontentloaded' });

    // Tab through first 10 interactive elements
    for (let i = 0; i < 10; i++) {
      await p.keyboard.press('Tab');
    }

    const activeEl = await p.evaluate(() => {
      const el = document.activeElement;
      return el ? el.tagName : 'NONE';
    });

    // After tabbing, active element should be an interactive element
    expect(['A', 'BUTTON', 'INPUT', 'SELECT', 'TEXTAREA']).toContain(activeEl);
    await ctx.close();
  });
});

// ─── Color contrast (basic check) ───
test.describe('Accessibility: Color Contrast', () => {
  test('Home page text has sufficient contrast', async ({ browser }) => {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const p = await ctx.newPage();
    await p.goto(`${BASE}/index.html`, { waitUntil: 'domcontentloaded' });

    // Check that primary text is not invisible (same color as background)
    const textVisible = await p.evaluate(() => {
      const body = window.getComputedStyle(document.body);
      const bgColor = body.backgroundColor;
      const textColor = body.color;
      return bgColor !== textColor;
    });

    expect(textVisible).toBe(true);
    await ctx.close();
  });
});

// ─── Search overlay keyboard accessible ───
test.describe('Accessibility: Search', () => {
  test('Search opens with / key and closes with Escape', async ({ browser }) => {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const p = await ctx.newPage();
    await p.goto(`${BASE}/index.html`, { waitUntil: 'load' });
    await p.waitForTimeout(500);

    // Press / to open search
    await p.keyboard.press('/');
    await p.waitForTimeout(300);

    const overlayVisible = await p.$eval('#eos-search-overlay', (el) => !el.hidden);
    expect(overlayVisible).toBe(true);

    // Press Escape to close
    await p.keyboard.press('Escape');
    await p.waitForTimeout(300);

    const overlayClosed = await p.$eval('#eos-search-overlay', (el) => el.hidden);
    expect(overlayClosed).toBe(true);

    await ctx.close();
  });
});

// ─── eBot chat widget accessibility ───
test.describe('Accessibility: eBot Chat', () => {
  test('eBot FAB has aria-label', async ({ browser }) => {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const p = await ctx.newPage();
    await p.goto(`${BASE}/index.html`, { waitUntil: 'load' });
    await p.waitForTimeout(500);

    const fab = await p.$('#ebot-fab');
    if (fab) {
      const ariaLabel = await fab.getAttribute('aria-label');
      expect(ariaLabel).not.toBeNull();
      expect(ariaLabel.length).toBeGreaterThan(3);
    }
    await ctx.close();
  });

  test('eBot panel opens when FAB is clicked', async ({ browser }) => {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const p = await ctx.newPage();
    await p.goto(`${BASE}/index.html`, { waitUntil: 'load' });
    await p.waitForTimeout(500);

    const fab = await p.$('#ebot-fab');
    if (fab) {
      await fab.click();
      await p.waitForTimeout(300);
      const panel = await p.$('#ebot-panel');
      if (panel) {
        const isHidden = await panel.getAttribute('hidden');
        expect(isHidden).toBeNull();
      }
    }
    await ctx.close();
  });
});
