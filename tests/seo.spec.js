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

// ─── Every page has a title containing EmbeddedOS ───
test.describe('SEO: Title Tags', () => {
  for (const page of PAGES) {
    test(`${page.name} has proper title tag`, async ({ browser }) => {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const p = await ctx.newPage();
      await p.goto(`${BASE}${page.path}`, { waitUntil: 'domcontentloaded' });

      const title = await p.title();
      expect(title.length).toBeGreaterThan(10);
      expect(title.toLowerCase()).toContain('embeddedos');
      await ctx.close();
    });
  }
});

// ─── Every page has meta description (50-160 chars) ───
test.describe('SEO: Meta Description', () => {
  for (const page of PAGES) {
    test(`${page.name} has valid meta description`, async ({ browser }) => {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const p = await ctx.newPage();
      await p.goto(`${BASE}${page.path}`, { waitUntil: 'domcontentloaded' });

      const desc = await p.$eval('meta[name="description"]', (el) => el.getAttribute('content'));
      expect(desc).not.toBeNull();
      expect(desc.length).toBeGreaterThan(40);
      expect(desc.length).toBeLessThan(300);
      await ctx.close();
    });
  }
});

// ─── Every page has canonical link ───
test.describe('SEO: Canonical Links', () => {
  for (const page of PAGES) {
    test(`${page.name} has canonical link`, async ({ browser }) => {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const p = await ctx.newPage();
      await p.goto(`${BASE}${page.path}`, { waitUntil: 'domcontentloaded' });

      const canonical = await p.$('link[rel="canonical"]');
      expect(canonical, `Missing canonical on ${page.name}`).not.toBeNull();
      if (canonical) {
        const href = await canonical.getAttribute('href');
        expect(href).toContain('embeddedos-org.github.io');
      }
      await ctx.close();
    });
  }
});

// ─── Every page has Open Graph tags ───
test.describe('SEO: Open Graph Tags', () => {
  for (const page of PAGES) {
    test(`${page.name} has OG tags`, async ({ browser }) => {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const p = await ctx.newPage();
      await p.goto(`${BASE}${page.path}`, { waitUntil: 'domcontentloaded' });

      const ogTitle = await p.$('meta[property="og:title"]');
      const ogDesc = await p.$('meta[property="og:description"]');
      const ogImage = await p.$('meta[property="og:image"]');

      expect(ogTitle, `Missing og:title on ${page.name}`).not.toBeNull();
      expect(ogDesc, `Missing og:description on ${page.name}`).not.toBeNull();
      expect(ogImage, `Missing og:image on ${page.name}`).not.toBeNull();
      await ctx.close();
    });
  }
});

// ─── Every page has exactly one H1 ───
test.describe('SEO: H1 Tag', () => {
  for (const page of PAGES) {
    test(`${page.name} has exactly one H1`, async ({ browser }) => {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const p = await ctx.newPage();
      await p.goto(`${BASE}${page.path}`, { waitUntil: 'domcontentloaded' });

      const h1Count = await p.$$eval('h1', (els) => els.length);
      expect(h1Count, `${page.name} has ${h1Count} H1 tags (expected 1)`).toBe(1);
      await ctx.close();
    });
  }
});

// ─── Home page has JSON-LD structured data ───
test.describe('SEO: Structured Data', () => {
  test('Home page has valid JSON-LD', async ({ browser }) => {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const p = await ctx.newPage();
    await p.goto(`${BASE}/index.html`, { waitUntil: 'domcontentloaded' });

    const jsonLdScripts = await p.$$eval('script[type="application/ld+json"]', (scripts) =>
      scripts.map((s) => {
        try {
          JSON.parse(s.textContent);
          return { valid: true, type: JSON.parse(s.textContent)['@type'] };
        } catch (e) {
          return { valid: false, error: e.message };
        }
      })
    );

    expect(jsonLdScripts.length).toBeGreaterThan(0);
    jsonLdScripts.forEach((s) => {
      expect(s.valid, `Invalid JSON-LD: ${s.error}`).toBe(true);
    });

    const types = jsonLdScripts.map((s) => s.type);
    expect(types).toContain('Organization');
    expect(types).toContain('WebSite');
    await ctx.close();
  });
});

// ─── Robots.txt exists and has sitemap ───
test.describe('SEO: Robots & Sitemap', () => {
  test('robots.txt is accessible', async ({ browser }) => {
    const ctx = await browser.newContext();
    const p = await ctx.newPage();
    const response = await p.goto(`${BASE}/robots.txt`);
    expect(response.status()).toBe(200);
    const text = await p.textContent('body');
    expect(text).toContain('Sitemap');
    await ctx.close();
  });

  test('sitemap.xml is valid', async ({ browser }) => {
    const ctx = await browser.newContext();
    const p = await ctx.newPage();
    const response = await p.goto(`${BASE}/sitemap.xml`);
    expect(response.status()).toBe(200);
    const text = await p.textContent('body');
    expect(text).toContain('embeddedos-org.github.io');
    await ctx.close();
  });
});
