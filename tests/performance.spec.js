// @ts-check
const { test, expect } = require('@playwright/test');

const BASE = process.env.BASE_URL || 'http://localhost:8080';

const PAGES = [
  { name: 'Home', path: '/index.html' },
  { name: 'Get Started', path: '/getting-started.html' },
  { name: 'Docs Hub', path: '/docs/index.html' },
  { name: 'Books', path: '/books.html' },
];

// ─── Page load time ───
test.describe('Performance: Page Load', () => {
  for (const page of PAGES) {
    test(`${page.name} loads within 5 seconds`, async ({ browser }) => {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const p = await ctx.newPage();
      const start = Date.now();
      await p.goto(`${BASE}${page.path}`, { waitUntil: 'domcontentloaded' });
      const loadTime = Date.now() - start;

      expect(loadTime, `${page.name} took ${loadTime}ms to load`).toBeLessThan(5000);
      await ctx.close();
    });
  }
});

// ─── No single resource > 1MB ───
test.describe('Performance: Resource Size', () => {
  test('Home page has no oversized resources', async ({ browser }) => {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const p = await ctx.newPage();

    const largeResources = [];
    p.on('response', (response) => {
      const headers = response.headers();
      const size = parseInt(headers['content-length'] || '0', 10);
      if (size > 1024 * 1024) {
        largeResources.push({ url: response.url(), size: Math.round(size / 1024) + 'KB' });
      }
    });

    await p.goto(`${BASE}/index.html`, { waitUntil: 'load' });

    expect(largeResources, `Oversized resources: ${JSON.stringify(largeResources)}`).toEqual([]);
    await ctx.close();
  });
});

// ─── CSS loads and applies ───
test.describe('Performance: CSS Loading', () => {
  test('style.css loads successfully', async ({ browser }) => {
    const ctx = await browser.newContext();
    const p = await ctx.newPage();
    const response = await p.goto(`${BASE}/style.css`);
    expect(response.status()).toBe(200);
    const contentType = response.headers()['content-type'] || '';
    expect(contentType).toContain('css');
    await ctx.close();
  });
});

// ─── JS files load without errors ───
test.describe('Performance: JavaScript Loading', () => {
  test('Home page JS loads without console errors', async ({ browser }) => {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const p = await ctx.newPage();

    const errors = [];
    p.on('pageerror', (err) => errors.push(err.message));

    const failedRequests = [];
    p.on('requestfailed', (req) => failedRequests.push(req.url()));

    await p.goto(`${BASE}/index.html`, { waitUntil: 'load' });
    await p.waitForTimeout(1000);

    expect(errors, `JS errors: ${errors.join(', ')}`).toEqual([]);
    // Filter out external request failures (CDN, analytics)
    const internalFailed = failedRequests.filter((url) => url.includes('localhost'));
    expect(internalFailed, `Failed internal requests: ${internalFailed.join(', ')}`).toEqual([]);
    await ctx.close();
  });
});

// ─── First Contentful Paint ───
test.describe('Performance: Web Vitals', () => {
  test('Home page FCP < 3000ms', async ({ browser }) => {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const p = await ctx.newPage();
    await p.goto(`${BASE}/index.html`, { waitUntil: 'load' });

    const fcp = await p.evaluate(() => {
      return new Promise((resolve) => {
        new PerformanceObserver((list) => {
          const entries = list.getEntriesByName('first-contentful-paint');
          if (entries.length) resolve(entries[0].startTime);
          else resolve(0);
        }).observe({ type: 'paint', buffered: true });
        setTimeout(() => resolve(0), 5000);
      });
    });

    if (fcp > 0) {
      expect(fcp, `FCP was ${fcp}ms`).toBeLessThan(3000);
    }
    await ctx.close();
  });
});
