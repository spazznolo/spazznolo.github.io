import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const pages = ['/', '/research/', '/about/', '/archive/', '/404.html', '/research/goalie-performance/', '/research/nhl-pick-probability/'];
const widths = [320, 768, 1440];
const responsivePages = ['/research/goalie-performance/', '/research/nhl-pick-probability/', '/goalies/consistency/', '/2022/09/16/tennis-liveblog.html'];

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

test('homepage presentation is retained without header links', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('nav .navbar-nav .nav-link')).toHaveCount(0);
  await expect(page.locator('.navbar-brand')).toHaveCount(0);
  await expect(page.locator('.quarto-color-scheme-toggle')).toHaveCount(0);
  await expect(page.locator('body')).toHaveCSS('font-family', /Source Code Pro/);
});

for (const width of [320, 1440]) {
  test(`body type scale stays at 13px at ${width}px`, async ({ page }) => {
    await page.setViewportSize({ width, height: 900 });
    await page.goto('/');
    await expect(page.locator('html')).toHaveCSS('font-size', '13px');
    await expect(page.locator('body')).toHaveCSS('font-size', '13px');
  });
}

test('homepage starts with the approved image', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('#title-block-header')).toBeHidden();
  const visibleChildren = await page.locator('.home-stream').evaluate((stream) =>
    [...stream.children]
      .filter((child) => getComputedStyle(child).display !== 'none' && getComputedStyle(child).visibility !== 'hidden')
      .slice(0, 1)
      .map((child) => child.classList.contains('home-image') ? 'home-image' : child.classList.contains('home-about') ? 'home-about' : child.className || child.tagName.toLowerCase()),
  );
  expect(visibleChildren).toEqual(['home-image']);
  await expect(page.locator('.home-image img')).toBeVisible();
  await expect(page.locator('.home-about')).toHaveCount(0);
});

test('homepage research descriptions sit below their titles', async ({ page }) => {
  await page.goto('/');
  for (const title of ['Goalie Performance', 'Pick Probability']) {
    const link = page.locator('#research').getByRole('link', { name: title, exact: true });
    await expect(link).toHaveCSS('display', 'block');
  }
});

test('top navigation exposes no destinations', async ({ page }) => {
  await page.goto('/');
  const nav = page.locator('nav');
  await expect(nav.getByRole('link', { name: 'Research' })).toHaveCount(0);
  await expect(nav.getByRole('link', { name: 'Home', exact: true })).toHaveCount(0);
  await expect(nav.getByRole('link', { name: 'Subjects' })).toHaveCount(0);
  await expect(nav.getByRole('link', { name: 'About' })).toHaveCount(0);
  await expect(nav.getByRole('link', { name: 'GitHub' })).toHaveCount(0);
  await expect(nav.getByRole('link', { name: /LinkedIn|Twitter/i })).toHaveCount(0);
});

test('GitHub is linked from the homepage body', async ({ page }) => {
  await page.goto('/');
  const github = page.locator('main').getByRole('link', { name: 'GitHub', exact: true });
  await github.focus();
  await expect(github).toBeFocused();
  await expect(github).toHaveCSS('outline-style', /solid|auto/);
  await expect(github).toHaveAttribute('href', 'https://github.com/spazznolo');
});

for (const path of ['/research/goalie-performance/', '/goalies/consistency/']) {
  test(`${path} does not show subjects beneath the post title`, async ({ page }) => {
    await page.goto(path);
    await expect(page.locator('header.quarto-title-block .quarto-categories')).toHaveCount(0);
    await expect(page.locator('header.quarto-title-block .quarto-category-link')).toHaveCount(0);
  });
}

test('recent writing uses readable stacked rows at 320px', async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 900 });
  await page.goto('/');
  const listing = page.locator('#listing-recent-writing');
  const table = listing.locator('table');
  await expect(table.locator('thead th')).toHaveCount(3);
  const row = table.locator('tbody tr').first();
  await expect(row).toHaveCSS('display', 'block');
  await expect(row.locator('td').first()).toHaveCSS('display', 'grid');
  await expect(row.locator('.listing-title')).toContainText('WTA Rankings');
  const titleBox = await row.locator('.listing-title').boundingBox();
  expect(titleBox?.width ?? 0).toBeGreaterThan(140);
  await expect(row.locator('.listing-categories')).toHaveCount(0);
  await expect(row).toHaveCSS('border-style', 'none');
  const labels = await page.evaluate(() =>
    [...document.querySelectorAll('#listing-recent-writing tbody tr:first-child td')].map((cell) =>
      getComputedStyle(cell, '::before').content,
    ),
  );
  expect(labels).toEqual(['"Date"', '"Title"', '"Reading time"']);
});

test('recent writing gives the title column most of the desktop width', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/');
  const widths = await page.locator('#listing-recent-writing thead th').evaluateAll((cells) =>
    cells.map((cell) => cell.getBoundingClientRect().width),
  );
  expect(widths[1]).toBeGreaterThan(widths[0] + widths[2]);
});

test('homepage framing is restrained and the decorative image has no caption', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('.home-image')).toHaveCSS('border-bottom-style', 'none');
  await expect(page.locator('.home-about')).toHaveCount(0);
  await expect(page.locator('.home-stream h2').first()).toHaveCSS('border-bottom-style', 'none');
  await expect(page.locator('.home-image figcaption')).toHaveCount(0);

  await page.goto('/research/goalie-performance/');
  await expect(page.locator('#TOC h2')).toHaveCSS('border-bottom-style', 'none');
  await expect(page.locator('main section.level2 > h2').first()).toHaveCSS('border-bottom-style', 'none');
});

test('homepage section labels use the compact type scale', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Research', exact: true })).toHaveCSS('font-size', '9.75px');
  await expect(page.getByRole('heading', { name: 'Recent writing' })).toHaveCSS('font-size', '9.75px');
});

test('article section headings use the smaller reading hierarchy', async ({ page }) => {
  await page.goto('/research/goalie-performance/');
  await expect(page.getByRole('heading', { name: 'Accounting for shot quality' })).toHaveCSS('font-size', '16.25px');
});

test('article table of contents omits its redundant title', async ({ page }) => {
  await page.goto('/research/goalie-performance/');
  await expect(page.getByRole('heading', { name: 'On this page' })).toBeHidden();
  await expect(page.locator('#TOC a').first()).toBeVisible();
});

test('article reading frame is wider on desktop', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/research/goalie-performance/');
  const frame = await page.locator('#quarto-content').boundingBox();
  expect(frame?.width ?? 0).toBeGreaterThanOrEqual(900);
});

test('long article URLs can wrap on narrow screens', async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 800 });
  await page.goto('/research/goalie-performance/');
  const longUrl = page.locator('main a[href*="goalie-performance/blob/main/posts/post-1.R"]');
  await expect(longUrl).toHaveCSS('overflow-wrap', 'anywhere');
});

test('equations use the informal working-note treatment', async ({ page }) => {
  await page.goto('/research/goalie-performance/');
  const equation = page.locator('.equation-note').first();
  await expect(equation).toBeVisible();
  await expect(equation).toHaveCSS('border-left-style', 'solid');
  await expect(equation).toHaveCSS('border-top-style', 'none');
  await expect(equation).toHaveCSS('border-right-style', 'none');
  await expect(equation).toHaveCSS('border-bottom-style', 'none');
  await expect(equation.locator('details')).toHaveCount(0);

  await page.goto('/research/nhl-pick-probability/');
  const draftEquation = page.locator('.equation-note').first();
  await expect(draftEquation).toBeVisible();
  await expect(draftEquation.locator('details')).toHaveCount(0);
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
