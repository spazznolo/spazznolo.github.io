import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const pages = ['/', '/research/', '/subjects/', '/about/', '/archive/', '/404.html', '/research/goalie-performance/', '/research/nhl-pick-probability/'];
const widths = [320, 768, 1440];
const responsivePages = ['/research/goalie-performance/', '/research/nhl-pick-probability/', '/2022/03/28/goalie-consistency-1.html', '/2022/09/16/tennis-liveblog.html'];

for (const path of pages) {
  test(`${path} has no serious accessibility violations`, async ({ page }) => {
    const response = await page.goto(path);
    expect(response?.ok()).toBe(true);
    const results = await new AxeBuilder({ page }).analyze();
    const serious = results.violations.filter(v => ['serious', 'critical'].includes(v.impact));
    expect(serious).toEqual([]);
  });

  test(`${path} has no serious accessibility violations in light mode`, async ({ page }) => {
    const response = await page.goto(path);
    expect(response?.ok()).toBe(true);
    await page.locator('.quarto-color-scheme-toggle').click();
    await expect(page.locator('body')).toHaveClass(/quarto-light/);
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

for (const path of responsivePages) {
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

for (const mode of ['dark', 'light']) {
  for (const width of [320, 1440]) {
    test(`body type scale stays at 13px in ${mode} mode at ${width}px`, async ({ page }) => {
      await page.setViewportSize({ width, height: 900 });
      await page.goto('/');
      if (mode === 'light') {
        await page.locator('.quarto-color-scheme-toggle').click();
        await expect(page.locator('body')).toHaveClass(/quarto-light/);
      } else {
        await expect(page.locator('body')).toHaveClass(/quarto-dark/);
      }
      await expect(page.locator('html')).toHaveCSS('font-size', '13px');
      await expect(page.locator('body')).toHaveCSS('font-size', '13px');
    });
  }
}

test('homepage starts with the approved image and About content', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('#title-block-header')).toBeHidden();
  const visibleChildren = await page.locator('.home-stream').evaluate((stream) =>
    [...stream.children]
      .filter((child) => getComputedStyle(child).display !== 'none' && getComputedStyle(child).visibility !== 'hidden')
      .slice(0, 2)
      .map((child) => child.classList.contains('home-image') ? 'home-image' : child.classList.contains('home-about') ? 'home-about' : child.className || child.tagName.toLowerCase()),
  );
  expect(visibleChildren).toEqual(['home-image', 'home-about']);
  await expect(page.locator('.home-image img')).toBeVisible();
  await expect(page.getByRole('heading', { name: 'About' })).toBeVisible();
});

test('homepage featured reading times match the rendered listings', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByText(/Goalie Performance.*15 min/)).toBeVisible();
  await expect(page.getByText(/NHL Pick Probability.*19 min/)).toBeVisible();
  await expect(page.getByText(/Goalie Performance.*18 min/)).toHaveCount(0);
  await expect(page.getByText(/NHL Pick Probability.*23 min/)).toHaveCount(0);
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

test('keyboard focus reaches navigation and activates Research', async ({ page }) => {
  await page.goto('/');
  const research = page.locator('nav').getByRole('link', { name: 'Research', exact: true });
  await research.focus();
  await expect(research).toBeFocused();
  await expect(research).toHaveCSS('outline-style', /solid|auto/);
  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/\/research\/$/);
});

for (const path of ['/research/goalie-performance/', '/2022/03/28/goalie-consistency-1.html']) {
  test(`${path} activates category links without failed local requests`, async ({ page }) => {
    const failedLocal = [];
    page.on('response', (response) => {
      if (response.url().startsWith('http://127.0.0.1:4173/') && response.status() >= 400) {
        failedLocal.push(`${response.status()} ${response.url()}`);
      }
    });
    await page.goto(path);
    const category = page.locator('header.quarto-title-block .quarto-category-link').first();
    await expect(category).toBeVisible();
    await expect(category).toHaveAttribute('href', /\/subjects\/#[-a-z0-9]+$/);
    const categoryText = (await category.textContent()).trim().toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    await expect(category).toHaveAttribute('href', new RegExp(`/subjects/#${categoryText}$`));
    expect(new URL(await category.getAttribute('href'), await page.url()).pathname).toBe('/subjects/');
    await expect(page.locator('#quarto-search')).toHaveCount(0);
    await page.waitForTimeout(250);
    expect(failedLocal).toEqual([]);
  });
}

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
