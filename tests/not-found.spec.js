// @ts-check
const { test, expect } = require('@playwright/test');

const BASE = process.env.BASE_URL || 'http://localhost:8080';
const MISSING = '/no/such/page/';

// GitHub Pages serves /404.html at whatever path was requested, so the page's
// stylesheet, scripts and links must resolve from the site root. Relative
// URLs resolved under the missing path instead: every asset 404'd, and a link
// checker following them generated ever-deeper missing paths without end.
test.describe('404 page served at a nested missing path', () => {
  test('its assets load and its links resolve from the site root', async ({ page }) => {
    const failed = [];
    page.on('response', (r) => {
      const url = r.url();
      if (url.startsWith(BASE) && r.status() >= 400 && new URL(url).pathname !== MISSING) {
        failed.push(`${r.status()} ${url}`);
      }
    });
    const res = await page.goto(`${BASE}${MISSING}`);
    expect(res && res.status()).toBe(404);
    await page.waitForLoadState('networkidle');
    expect(failed).toEqual([]);

    const internal = await page.$$eval('a[href]', (as) =>
      as.map((a) => a.href).filter((h) => h.startsWith(location.origin)),
    );
    expect(internal.length).toBeGreaterThan(0);
    for (const href of internal) {
      expect(new URL(href).pathname.startsWith(MISSING), href).toBe(false);
    }
  });
});
