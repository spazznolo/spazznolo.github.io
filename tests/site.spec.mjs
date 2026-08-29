import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const pages = ['/', '/research/', '/subjects/', '/about/', '/archive/', '/404.html'];
const widths = [320, 768, 1440];

for (const path of pages) {
  test(`${path} has no serious accessibility violations`, async ({ page }) => {
    await page.goto(path);
    const results = await new AxeBuilder({ page }).analyze();
    const serious = results.violations.filter(v => ['serious', 'critical'].includes(v.impact));
    expect(serious).toEqual([]);
  });
}

for (const width of widths) {
  test(`homepage fits ${width}px`, async ({ page }) => {
    await page.setViewportSize({ width, height: 900 });
    await page.goto('/');
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
    expect(overflow).toBe(false);
  });
}

test('approved homepage presentation is retained', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('.navbar-brand')).toHaveCount(1);
  await expect(page.getByRole('heading', { name: 'About' })).toBeVisible();
  await expect(page.locator('.home-about p')).toHaveCSS('color', 'rgb(242, 240, 235)');
  await expect(page.locator('body')).toHaveCSS('font-family', /Source Code Pro/);
});

test('top navigation exposes only approved destinations', async ({ page }) => {
  await page.goto('/');
  const nav = page.locator('nav');
  await expect(nav.getByRole('link', { name: 'Research' })).toBeVisible();
  await expect(nav.getByRole('link', { name: 'Subjects' })).toBeVisible();
  await expect(nav.getByRole('link', { name: 'About' })).toBeVisible();
  await expect(nav.getByRole('link', { name: 'GitHub' })).toHaveAttribute('href', 'https://github.com/spazznolo');
  await expect(nav.getByRole('link', { name: /LinkedIn|Twitter/i })).toHaveCount(0);
});
