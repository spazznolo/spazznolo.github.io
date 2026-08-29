import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const pages = ['/', '/research/', '/subjects/', '/about/', '/archive/', '/404.html', '/research/goalie-performance/', '/research/nhl-pick-probability/'];
const widths = [320, 768, 1440];

for (const path of pages) {
  test(`${path} has no serious accessibility violations`, async ({ page }) => {
    const response = await page.goto(path);
    expect(response?.ok()).toBe(true);
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

for (const path of ['/research/goalie-performance/', '/research/nhl-pick-probability/']) {
  for (const width of widths) {
    test(`${path} fits ${width}px`, async ({ page }) => {
      await page.setViewportSize({ width, height: 900 });
      const response = await page.goto(path);
      expect(response?.ok()).toBe(true);
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
      expect(overflow).toBe(false);
    });
  }
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

test('recent writing uses readable stacked rows at 320px', async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 900 });
  await page.goto('/');
  const listing = page.locator('#listing-recent-writing');
  const table = listing.locator('table');
  await expect(table.locator('thead th')).toHaveCount(4);
  const row = table.locator('tbody tr').first();
  await expect(row).toHaveCSS('display', 'block');
  await expect(row.locator('td').first()).toHaveCSS('display', 'grid');
  await expect(row.locator('.listing-title')).toContainText('Goalie Performance');
  await expect(row.locator('.listing-categories')).toContainText('Bayesian statistics');
  const titleBox = await row.locator('.listing-title').boundingBox();
  const categoriesBox = await row.locator('.listing-categories').boundingBox();
  expect(titleBox?.width ?? 0).toBeGreaterThan(140);
  expect(categoriesBox?.width ?? 0).toBeGreaterThan(140);
  const labels = await page.evaluate(() =>
    [...document.querySelectorAll('#listing-recent-writing tbody tr:first-child td')].map((cell) =>
      getComputedStyle(cell, '::before').content,
    ),
  );
  expect(labels).toEqual(['"Date"', '"Title"', '"Reading time"', '"Subjects"']);
});

test('historical video has an in-element fallback link', async ({ page }) => {
  await page.goto('/2022/09/16/tennis-liveblog.html');
  const video = page.locator('video').last();
  await expect(video).toContainText('browser does not support');
  await expect(video.locator('a')).toHaveAttribute('href', /player-detect-demo\.mp4/);
  await expect(page.getByText('The clip demonstrates the player-detection stage')).toBeVisible();
});

test('historical code is behind an accessible disclosure', async ({ page }) => {
  await page.goto('/research/nhl-pick-probability/');
  const disclosure = page.locator('details.historical-code-disclosure').first();
  await expect(disclosure).toHaveCount(1);
  await expect(disclosure.locator('summary')).toContainText('Show historical code');
  await disclosure.locator('summary').click();
  await expect(disclosure.locator('pre code')).toBeVisible();
});
