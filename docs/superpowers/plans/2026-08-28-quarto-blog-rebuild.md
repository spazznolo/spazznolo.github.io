# Quarto Blog Rebuild Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Jekyll blog with the approved Quarto publication, preserve every public route, consolidate the two flagship subjects into one article each, and deploy a tested GitHub Pages site.

**Architecture:** A Quarto 1.10.18 website renders source `.qmd` files to `_site`, with the dark-first Source Code Pro design expressed in small SCSS files. Historical posts render as static archive pages at their existing production paths; new articles use directory-based clean URLs and may use frozen executable output. Python contract tests validate routes, links, assets, and metadata, while Playwright and axe validate responsive layout and accessibility before the official GitHub Pages workflow deploys the rendered artifact.

**Tech Stack:** Quarto 1.10.18, Pandoc/Lua filters, SCSS/Bootstrap 5, Python 3 standard library tests, Node.js 20.20.1, Playwright 1.62.1, axe-core Playwright 4.13.0, GitHub Actions, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-08-28-quarto-blog-rebuild-design.md`

## Global Constraints

- Preserve all 24 historical posts and every route in `tests/legacy-routes.json`.
- Do not reconstruct data, rerun models, or claim reproducibility for historical work or the two canonical consolidations.
- Apply executable Quarto, frozen output, and dependency-pinning expectations only to new posts.
- Keep the homepage introduction verbatim and keep `figs/fifty-four.png` prominent.
- Use Source Code Pro throughout, warm yellow accents, white About copy, a warm near-black dark default, and one vertical content stream.
- Show `jeremie.spagnolo` exactly once in the visible page chrome; do not add a hero name or slogan.
- Use statistical subjects as `categories`; store sports contexts separately as `sports` metadata.
- Link publicly to GitHub only; do not add LinkedIn, Twitter, comments, newsletter, search, or accounts.
- Use `Data science contractor for the Chicago Blackhawks` as the current professional wording.
- Describe tennis tracking as `paused with intent to return`.
- Retain only GA4 property `G-DGRHZS5DNM`; remove Universal Analytics and page-level duplicates.
- New production post URLs use `/posts/<slug>/`; canonical legacy articles use `/research/goalie-performance/` and `/research/nhl-pick-probability/`.
- Never commit `_site/`, `.quarto/`, `node_modules/`, Playwright reports, or `.superpowers/`.

---

## Planned File Structure

### Site configuration and presentation

- Create `_quarto.yml`: project, navigation, metadata, dark/light themes, GA4, RSS-capable site URL, rendering defaults, and explicit render/resource sets.
- Create `styles/dark.scss`: dark-first color variables.
- Create `styles/light.scss`: secondary light-mode color variables.
- Create `styles/site.scss`: shared typography, single-column layout, homepage, listing, archive, metadata, media, and mobile rules.
- Create `filters/reading-time.lua`: opt-in article reading-time line at 200 words per minute.
- Modify `.gitignore`: Quarto, Node, Playwright, and brainstorming output exclusions.

### Primary pages

- Replace `home.md` with `index.qmd`.
- Create `about/index.qmd`, `research/index.qmd`, `subjects/index.qmd`, and `archive/index.qmd`.
- Create `404.qmd` and `robots.txt`.
- Create `templates/post.qmd`: valid draft template for new computational posts.

### Legacy routes and content

- Create `tests/legacy-routes.json`: the production-route contract and source mapping.
- Create `background/index.qmd`, `goalies/index.qmd`, `tennis/index.qmd`, `draft/index.qmd`, and `post-regulation/index.qmd` for the existing collection routes.
- Move every `_posts/*.md` file to its production-dated `.qmd` path under `2021/`, `2022/`, `2023/`, or `2024/`.
- Keep `figs/` at the root so existing `/figs/...` URLs remain stable.
- Create `figs/player-detect-demo.mp4` as the browser-compatible video while retaining the original `.mov` asset.

### Canonical articles

- Create `research/goalie-performance/index.qmd`.
- Create `research/nhl-pick-probability/index.qmd`.
- Add supersession notices to the five archived Goalie Performance installments and six archived draft-probability installments.

### Validation and publishing

- Create `scripts/validate_rendered_site.py`: rendered-site route, link, asset, metadata, alt-text, and size checks.
- Create `tests/test_validate_rendered_site.py`: unit tests for validator behavior.
- Create `tests/test_canonical_articles.py`: source-level canonical structure and word-count checks.
- Create `package.json` and generated `package-lock.json`.
- Create `playwright.config.mjs` and `tests/site.spec.mjs`.
- Create `.github/workflows/site.yml`: render, validate, test, upload, and deploy.
- Replace `README.md` with local authoring, rendering, verification, and publishing instructions.
- Delete Jekyll-only files after parity is proven: `_config.yml`, `Gemfile`, `Gemfile.lock`, the six old root Markdown pages, the empty `_posts/` directory, and tracked `.DS_Store` files.

---

### Task 1: Quarto Foundation and Dark-First Homepage

**Files:**
- Create: `_quarto.yml`
- Create: `index.qmd`
- Create: `styles/dark.scss`
- Create: `styles/light.scss`
- Create: `styles/site.scss`
- Create: `filters/reading-time.lua`
- Create: `robots.txt`
- Create: `tests/test_rendered_site.py`
- Modify: `.gitignore`

**Interfaces:**
- Consumes: `figs/fifty-four.png`, GA4 property `G-DGRHZS5DNM`.
- Produces: `_site/`, shared theme classes `.home-image`, `.home-about`, `.article-reading-time`, and the `reading-time: true` metadata contract used by all later article tasks.

- [ ] **Step 1: Install the pinned Quarto CLI outside the repository**

Run on macOS:

```bash
curl -LO https://github.com/quarto-dev/quarto-cli/releases/download/v1.10.18/quarto-1.10.18-macos.pkg
sudo installer -pkg quarto-1.10.18-macos.pkg -target /
quarto --version
```

Expected: `1.10.18`. Remove the downloaded package after installation through Finder or another recoverable cleanup method; do not add it to the repository.

- [ ] **Step 2: Write the failing rendered-site smoke test**

Create `tests/test_rendered_site.py`:

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"


class RenderedSiteSmokeTest(unittest.TestCase):
    def test_foundation_outputs_exist(self):
        required = [
            SITE / "index.html",
            SITE / "robots.txt",
            SITE / "figs" / "fifty-four.png",
        ]
        missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
        self.assertEqual(missing, [])

    def test_homepage_keeps_approved_copy(self):
        html = (SITE / "index.html").read_text(encoding="utf-8")
        sentence = "This blog serves as an outlet to explore ideas which naturally interest me."
        self.assertIn(sentence, html)
        self.assertIn("fifty-four.png", html)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the smoke test and verify it fails**

Run: `python3 -m unittest tests/test_rendered_site.py -v`

Expected: FAIL because `_site/index.html` does not exist.

- [ ] **Step 4: Create the Quarto configuration**

Create `_quarto.yml`:

```yaml
project:
  type: website
  output-dir: _site
  resources:
    - figs/**
    - robots.txt
  render:
    - "*.qmd"
    - "about/**/*.qmd"
    - "research/**/*.qmd"
    - "subjects/**/*.qmd"
    - "archive/**/*.qmd"
    - "background/**/*.qmd"
    - "goalies/**/*.qmd"
    - "tennis/**/*.qmd"
    - "draft/**/*.qmd"
    - "post-regulation/**/*.qmd"
    - "20*/**/*.qmd"
    - "posts/**/*.qmd"

website:
  title: "jeremie.spagnolo"
  site-url: "https://spazznolo.github.io"
  description: "Sports statistics, applied modeling, and research notes by Jeremie Spagnolo."
  google-analytics: "G-DGRHZS5DNM"
  open-graph: true
  search: false
  navbar:
    title: "jeremie.spagnolo"
    collapse: true
    right:
      - text: "Research"
        href: /research/
      - text: "Subjects"
        href: /subjects/
      - text: "About"
        href: /about/
      - text: "GitHub"
        href: "https://github.com/spazznolo"
  page-footer:
    border: false

format:
  html:
    theme:
      dark: [cosmo, styles/dark.scss, styles/site.scss]
      light: [cosmo, styles/light.scss, styles/site.scss]
    respect-user-color-scheme: false
    toc: true
    toc-location: body
    code-fold: true
    code-summary: "Show code"
    syntax-highlighting: arrow
    fig-cap-location: bottom
    link-external-newwindow: true
    include-after-body: []

execute:
  freeze: auto

filters:
  - filters/reading-time.lua
```

- [ ] **Step 5: Create the approved homepage content**

Create `index.qmd`:

```markdown
---
title: false
description: "Sports statistics, applied modeling, and research notes by Jeremie Spagnolo."
toc: false
page-layout: full
---

::: {.home-stream}
::: {.home-image}
![A warm, grainy overhead image from the original blog homepage.](/figs/fifty-four.png)
:::

::: {.home-about}
# About

This blog serves as an outlet to explore ideas which naturally interest me. I try to keep an informal, back-of-the-napkin style to these posts, hopefully a little like [Tom Tango](http://www.tangotiger.com/index.php). Posts are grouped by topic in the header, but can be accessed in chronological order below.
:::

## Featured research

- [Goalie Performance](/2023/05/17/goalie-performance-1.html) — Estimating talent while respecting small-sample uncertainty. · 12 min
- [NHL Pick Probability](/2023/06/16/draft-probabilities-2.html) — Turning rankings into pick distributions and decisions. · 9 min

## Statistical subjects

### Bayesian statistics
Empirical Bayes, priors and posteriors, and shrinkage.

### Probability and simulation
Draft uncertainty, overtime formats, and expected value.

### Distributions and sampling
Beta-binomial models, mixture models, and sample size.

### Regression and calibration
Logistic models, age curves, and model reliability.

## Recent writing

The complete chronological collection is available under [Research](/research/).
:::
```

- [ ] **Step 6: Create the dark, light, and shared theme files**

Create `styles/dark.scss`:

```scss
/*-- scss:defaults --*/
$body-bg: #0b0a08;
$body-color: #f2f0eb;
$link-color: #e8c872;
$navbar-bg: #0b0a08;
$navbar-fg: #f2f0eb;
$border-color: #393228;
$code-bg: #15120e;
$code-color: #f2f0eb;
```

Create `styles/light.scss`:

```scss
/*-- scss:defaults --*/
$body-bg: #f7f2e8;
$body-color: #211d17;
$link-color: #76580c;
$navbar-bg: #f7f2e8;
$navbar-fg: #211d17;
$border-color: #c9bda9;
$code-bg: #eee5d6;
$code-color: #211d17;
```

Create `styles/site.scss`:

```scss
/*-- scss:defaults --*/
$font-family-sans-serif: "Source Code Pro", monospace;
$font-family-monospace: "Source Code Pro", monospace;
$font-size-root: 13px;

/*-- scss:rules --*/
@import url("https://fonts.googleapis.com/css2?family=Source+Code+Pro:wght@400;500;700&display=swap");

:root {
  --warm-accent: #ddb85c;
  --warm-divider: #393228;
  --reading-width: 800px;
}

body { line-height: 1.65; }
.navbar { border-bottom: 1px solid var(--warm-divider); }
.navbar-brand { font-size: 0.92rem; font-weight: 500; }
.navbar-nav { gap: 0.55rem; }
.nav-link, .quarto-color-scheme-toggle { color: var(--warm-accent) !important; }

#quarto-content, .page-layout-full main { max-width: var(--reading-width); margin-inline: auto; }
.home-stream { display: block; }
.home-image { border-bottom: 1px solid var(--warm-divider); margin-bottom: 2rem; }
.home-image img { display: block; width: 100%; max-height: 420px; object-fit: cover; }
.home-about { border-bottom: 1px solid var(--warm-divider); padding-bottom: 2rem; margin-bottom: 2.4rem; }
.home-about h1, main > h2 { color: var(--warm-accent); font-size: 0.82rem; letter-spacing: 0.08em; text-transform: uppercase; }
.home-about p { color: #f2f0eb; font-size: 1rem; }
body.quarto-light .home-about p { color: #211d17; }
.article-reading-time, .archive-notice, .article-context { color: var(--warm-accent); font-size: 0.84rem; }
.listing-table, .quarto-listing { width: 100%; }
img, video, iframe { max-width: 100%; }

@media (max-width: 680px) {
  #quarto-content, .page-layout-full main { width: min(100% - 2rem, var(--reading-width)); }
  .navbar > .container-fluid { align-items: flex-start; }
}
```

- [ ] **Step 7: Create the opt-in reading-time filter**

Create `filters/reading-time.lua`:

```lua
local function enabled(meta)
  return meta["reading-time"] ~= nil and pandoc.utils.stringify(meta["reading-time"]) == "true"
end

function Pandoc(doc)
  if not FORMAT:match("html") or not enabled(doc.meta) then
    return doc
  end

  local words = 0
  local text = pandoc.utils.stringify(doc.blocks)
  for _ in text:gmatch("%S+") do
    words = words + 1
  end
  local minutes = math.max(1, math.ceil(words / 200))
  local line = pandoc.Para({pandoc.Str(tostring(minutes) .. " min read")})
  table.insert(doc.blocks, 1, pandoc.Div({line}, pandoc.Attr("", {"article-reading-time"})))
  return doc
end
```

- [ ] **Step 8: Add static resources and ignore rules**

Create `robots.txt`:

```text
User-agent: *
Allow: /
Sitemap: https://spazznolo.github.io/sitemap.xml
```

Append to `.gitignore`:

```gitignore
.quarto/
node_modules/
test-results/
playwright-report/
.superpowers/
```

- [ ] **Step 9: Render and run the smoke test**

Run:

```bash
quarto render
python3 -m unittest tests/test_rendered_site.py -v
```

Expected: render succeeds and both tests PASS.

- [ ] **Step 10: Commit the foundation**

```bash
git add _quarto.yml index.qmd styles filters robots.txt tests/test_rendered_site.py .gitignore
git commit -m "feat: establish Quarto site foundation"
```

---

### Task 2: Primary Pages and Responsive Accessibility Harness

**Files:**
- Create: `about/index.qmd`
- Create: `research/index.qmd`
- Create: `subjects/index.qmd`
- Create: `archive/index.qmd`
- Create: `404.qmd`
- Create: `templates/post.qmd`
- Create: `package.json`
- Create: `package-lock.json`
- Create: `playwright.config.mjs`
- Create: `tests/site.spec.mjs`

**Interfaces:**
- Consumes: the navigation, theme classes, `_site/`, and `reading-time: true` contract from Task 1.
- Produces: stable primary page routes and `npm test` browser/a11y contract used by every later task.

- [ ] **Step 1: Create the browser test dependencies**

Create `package.json`:

```json
{
  "name": "spazznolo-quarto-site",
  "private": true,
  "engines": { "node": "20.20.1" },
  "scripts": {
    "test": "playwright test",
    "test:site": "playwright test"
  },
  "devDependencies": {
    "@axe-core/playwright": "4.13.0",
    "@playwright/test": "1.62.1"
  }
}
```

Run:

```bash
npm install
npx playwright install chromium
```

Expected: `package-lock.json` is generated and Chromium installs successfully.

- [ ] **Step 2: Configure Playwright and write the failing page-shell tests**

Create `playwright.config.mjs`:

```javascript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  testMatch: /site\.spec\.mjs/,
  use: { baseURL: 'http://127.0.0.1:4173' },
  webServer: {
    command: 'python3 -m http.server 4173 --directory _site',
    url: 'http://127.0.0.1:4173',
    reuseExistingServer: true
  }
});
```

Create `tests/site.spec.mjs`:

```javascript
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
```

- [ ] **Step 3: Run the browser tests and verify they fail**

Run: `npm test`

Expected: FAIL because `/about/`, `/research/`, `/subjects/`, `/archive/`, and `/404.html` do not exist.

- [ ] **Step 4: Create the About page with approved factual wording**

Create `about/index.qmd`:

```markdown
---
title: "About"
description: "About Jeremie Spagnolo and the ideas behind this sports statistics blog."
toc: false
---

Around 2016, a few years removed from a mathematics degree, my interest in proofs, statistics, and even logic puzzles was waning. I was leaning toward creative pursuits—working odd jobs, reading fiction, and making music. During that time, my brother lent me *[Stat Shot](http://www.hockeyabstract.com/statshot)*.

The book was written as an entry point for casual fans to understand advanced hockey statistics. I read it as a blueprint. It helped me understand the research process as a creative one: curiosity gives way to a qualitative argument, possible quantitative frameworks take shape, and an idea is either pursued or set aside.

That process led from independent hockey research to an internship at the St. Lawrence River Institute, then to applied research at Statistics Canada. I now work as a **Data science contractor for the Chicago Blackhawks**.

I have also been building a tennis-tracking program intended to scale from individual matches to tournament-level data. That project is **paused with intent to return**.

My public work currently lives in sports, but the statistical subjects are broader: Bayesian inference, probability, simulation, distributions, sampling, regression, and calibration.

[GitHub](https://github.com/spazznolo)
```

- [ ] **Step 5: Create Research, Subjects, Archive, and 404 pages**

Create `research/index.qmd`:

```markdown
---
title: "Research"
description: "Sports statistics research in chronological order."
toc: false
---

Current and renovated work will appear here first. The complete historical collection remains available in the [Archive](/archive/).
```

Create `subjects/index.qmd`:

```markdown
---
title: "Statistical subjects"
description: "Research organized by the statistical ideas used."
toc: false
---

## Bayesian statistics

Empirical Bayes, priors and posteriors, and shrinkage.

## Probability and simulation

Draft uncertainty, overtime formats, and expected value.

## Distributions and sampling

Beta-binomial models, mixture models, and sample-size questions.

## Regression and calibration

Logistic models, age curves, and model reliability.
```

Create `archive/index.qmd`:

```markdown
---
title: "Archive"
description: "Earlier sports statistics posts, preserved in their original context."
toc: false
---

The archive preserves earlier work and its original publication context. Some installments now point to a consolidated article, but the original pages remain available.
```

Create `404.qmd`:

```markdown
---
title: "Page not found"
description: "The requested page could not be found."
toc: false
---

That page is not here. Try [Research](/research/), browse the [Archive](/archive/), or return [home](/).
```

- [ ] **Step 6: Create the new-post template**

Create `templates/post.qmd`:

```markdown
---
title: "New statistical note"
description: "A draft sports-statistics analysis."
date: 2026-08-28
date-modified: 2026-08-28
categories:
  - Bayesian statistics
sports:
  - Hockey
status: current
reading-time: true
draft: true
execute:
  freeze: auto
toc: true
---

## Question

State the sports question and why it matters before introducing the model.

## Data and assumptions

Identify the data source, sampling unit, exclusions, assumptions, and any unavailable inputs.

## Analysis

Keep executable code close to the result it creates. Prefer a static figure unless interaction adds analytical value.

## Validation and uncertainty

Report calibration, out-of-sample behavior, uncertainty, and important failure modes.

## Takeaway

Return to the sports question and separate the evidence from the interpretation.
```

- [ ] **Step 7: Render and run the browser contract**

Run:

```bash
quarto render
npm test
```

Expected: all page-shell, accessibility, responsive, type, color, and navigation tests PASS.

- [ ] **Step 8: Commit the primary pages and test harness**

```bash
git add about research subjects archive 404.qmd templates package.json package-lock.json playwright.config.mjs tests/site.spec.mjs
git commit -m "feat: add primary pages and browser checks"
```

---
### Task 3: Legacy Route Manifest and Rendered-Site Validator

**Files:**
- Create: `tests/legacy-routes.json`
- Create: `scripts/validate_rendered_site.py`
- Create: `tests/test_validate_rendered_site.py`

**Interfaces:**
- Consumes: `_site/` and the route-to-source mapping below.
- Produces: `route_to_output(route: str) -> Path`, `validate_routes(site: Path, routes: list[str]) -> list[str]`, `validate_internal_links(site: Path) -> list[str]`, and the command `python3 scripts/validate_rendered_site.py --site _site --routes tests/legacy-routes.json [--series NAME]`.

- [ ] **Step 1: Record the complete production-route contract**

Create `tests/legacy-routes.json` with this exact structure:

```json
{
  "pages": [
    {"route": "/", "source": "index.qmd", "series": "page"},
    {"route": "/background/", "source": "background/index.qmd", "series": "page"},
    {"route": "/goalies/", "source": "goalies/index.qmd", "series": "page"},
    {"route": "/tennis/", "source": "tennis/index.qmd", "series": "page"},
    {"route": "/draft/", "source": "draft/index.qmd", "series": "page"},
    {"route": "/post-regulation/", "source": "post-regulation/index.qmd", "series": "page"}
  ],
  "posts": [
    {"route": "/2021/11/28/draft-probabilities-1.html", "source": "2021/11/28/draft-probabilities-1.qmd", "series": "draft"},
    {"route": "/2022/03/28/goalie-consistency-1.html", "source": "2022/03/28/goalie-consistency-1.qmd", "series": "goalie"},
    {"route": "/2022/03/29/goalie-consistency-2.html", "source": "2022/03/29/goalie-consistency-2.qmd", "series": "goalie"},
    {"route": "/2022/04/02/goalie-consistency-3.html", "source": "2022/04/02/goalie-consistency-3.qmd", "series": "goalie"},
    {"route": "/2022/04/07/goalie-consistency-4.html", "source": "2022/04/07/goalie-consistency-4.qmd", "series": "goalie"},
    {"route": "/2022/04/20/post-regulation-1.html", "source": "2022/04/20/post-regulation-1.qmd", "series": "post-regulation"},
    {"route": "/2022/04/26/post-regulation-2.html", "source": "2022/04/26/post-regulation-2.qmd", "series": "post-regulation"},
    {"route": "/2022/04/29/post-regulation-3.html", "source": "2022/04/29/post-regulation-3.qmd", "series": "post-regulation"},
    {"route": "/2022/04/30/post-regulation-4.html", "source": "2022/04/30/post-regulation-4.qmd", "series": "post-regulation"},
    {"route": "/2022/09/16/tennis-liveblog.html", "source": "2022/09/16/tennis-liveblog.qmd", "series": "tennis"},
    {"route": "/2023/01/15/tennis-framework.html", "source": "2023/01/15/tennis-framework.qmd", "series": "tennis"},
    {"route": "/2023/05/17/goalie-performance-1.html", "source": "2023/05/17/goalie-performance-1.qmd", "series": "goalie"},
    {"route": "/2023/05/22/goalie-performance-2.html", "source": "2023/05/22/goalie-performance-2.qmd", "series": "goalie"},
    {"route": "/2023/06/16/draft-probabilities-2.html", "source": "2023/06/16/draft-probabilities-2.qmd", "series": "draft"},
    {"route": "/2023/06/20/draft-probabilities-3.html", "source": "2023/06/20/draft-probabilities-3.qmd", "series": "draft"},
    {"route": "/2023/07/02/draft-probabilities-4.html", "source": "2023/07/02/draft-probabilities-4.qmd", "series": "draft"},
    {"route": "/2023/07/07/draft-probabilities-5.html", "source": "2023/07/07/draft-probabilities-5.qmd", "series": "draft"},
    {"route": "/2023/07/08/goalie-performance-3.html", "source": "2023/07/08/goalie-performance-3.qmd", "series": "goalie"},
    {"route": "/2023/07/30/tennis-data.html", "source": "2023/07/30/tennis-data.qmd", "series": "tennis"},
    {"route": "/2024/07/20/draft-probabilities-6.html", "source": "2024/07/20/draft-probabilities-6.qmd", "series": "draft"},
    {"route": "/2024/07/25/tennis-object-detection.html", "source": "2024/07/25/tennis-object-detection.qmd", "series": "tennis"},
    {"route": "/2024/07/30/goalie-performance-4.html", "source": "2024/07/30/goalie-performance-4.qmd", "series": "goalie"},
    {"route": "/2024/07/30/goalie-performance-5.html", "source": "2024/07/30/goalie-performance-5.qmd", "series": "goalie"},
    {"route": "/2024/07/30/tennis-pipeline.html", "source": "2024/07/30/tennis-pipeline.qmd", "series": "tennis"}
  ]
}
```

- [ ] **Step 2: Write validator unit tests first**

Create `tests/test_validate_rendered_site.py`:

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.validate_rendered_site import route_to_output, validate_internal_links, validate_routes


class RouteValidationTest(unittest.TestCase):
    def test_route_to_output_handles_pages_and_html_posts(self):
        self.assertEqual(route_to_output("/"), Path("index.html"))
        self.assertEqual(route_to_output("/about/"), Path("about/index.html"))
        self.assertEqual(
            route_to_output("/2023/05/17/goalie-performance-1.html"),
            Path("2023/05/17/goalie-performance-1.html"),
        )

    def test_missing_route_is_reported(self):
        with TemporaryDirectory() as directory:
            errors = validate_routes(Path(directory), ["/missing/"])
        self.assertEqual(errors, ["missing route: /missing/ -> missing/index.html"])

    def test_broken_relative_link_is_reported(self):
        with TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "index.html").write_text('<a href="/missing/">missing</a>', encoding="utf-8")
            errors = validate_internal_links(site)
        self.assertEqual(errors, ["index.html: broken internal link /missing/"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the validator tests and verify they fail**

Run: `python3 -m unittest tests/test_validate_rendered_site.py -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.validate_rendered_site'`.

- [ ] **Step 4: Implement the validator**

Create `scripts/validate_rendered_site.py` with these public functions and CLI behavior:

```python
#!/usr/bin/env python3
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit


class ReferenceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.images = []
        self.title = False
        self.description = False

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a" and values.get("href"):
            self.references.append(values["href"])
        if tag in {"img", "script", "video", "source"} and values.get("src"):
            self.references.append(values["src"])
        if tag == "img":
            self.images.append(values)
        if tag == "title":
            self.title = True
        if tag == "meta" and values.get("name") == "description" and values.get("content", "").strip():
            self.description = True


def route_to_output(route: str) -> Path:
    path = unquote(urlsplit(route).path).lstrip("/")
    if not path:
        return Path("index.html")
    if path.endswith("/"):
        return Path(path) / "index.html"
    return Path(path)


def validate_routes(site: Path, routes: list[str]) -> list[str]:
    errors = []
    for route in routes:
        output = route_to_output(route)
        if not (site / output).is_file():
            errors.append(f"missing route: {route} -> {output.as_posix()}")
    return errors


def _resolve_reference(site: Path, html_file: Path, reference: str) -> Path | None:
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc or reference.startswith(("mailto:", "tel:", "#", "data:")):
        return None
    route = unquote(parsed.path)
    if not route:
        return None
    if route.startswith("/"):
        candidate = site / route_to_output(route)
    else:
        candidate = html_file.parent / route
        if route.endswith("/"):
            candidate = candidate / "index.html"
    if candidate.is_dir():
        candidate = candidate / "index.html"
    return candidate.resolve()


def validate_internal_links(site: Path) -> list[str]:
    errors = []
    for html_file in sorted(site.rglob("*.html")):
        parser = ReferenceParser()
        parser.feed(html_file.read_text(encoding="utf-8"))
        for reference in parser.references:
            target = _resolve_reference(site, html_file, reference)
            if target is not None and not target.exists():
                rel = html_file.relative_to(site).as_posix()
                errors.append(f"{rel}: broken internal link {reference}")
    return sorted(set(errors))


def validate_document_contract(site: Path) -> list[str]:
    errors = []
    for html_file in sorted(site.rglob("*.html")):
        parser = ReferenceParser()
        parser.feed(html_file.read_text(encoding="utf-8"))
        rel = html_file.relative_to(site).as_posix()
        if not parser.title:
            errors.append(f"{rel}: missing title")
        if not parser.description:
            errors.append(f"{rel}: missing meta description")
        for image in parser.images:
            if not image.get("alt", "").strip():
                errors.append(f"{rel}: image missing alt text: {image.get('src', '')}")
    return errors


def validate_asset_sizes(site: Path, limit_bytes: int = 5_000_000) -> list[str]:
    errors = []
    for path in sorted(site.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".mov", ".mp4", ".webm"}:
            if path.stat().st_size > limit_bytes:
                errors.append(f"oversized asset: {path.relative_to(site).as_posix()} ({path.stat().st_size} bytes)")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, default=Path("_site"))
    parser.add_argument("--routes", type=Path, default=Path("tests/legacy-routes.json"))
    parser.add_argument("--series")
    args = parser.parse_args()

    manifest = json.loads(args.routes.read_text(encoding="utf-8"))
    records = manifest["pages"] + manifest["posts"]
    if args.series:
        records = [record for record in records if record["series"] == args.series]
    routes = [record["route"] for record in records]

    errors = []
    errors.extend(validate_routes(args.site, routes))
    if not args.series:
        errors.extend(validate_internal_links(args.site))
        errors.extend(validate_document_contract(args.site))
        errors.extend(validate_asset_sizes(args.site))

    for error in sorted(set(errors)):
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 5: Run unit tests and demonstrate the production contract currently fails**

Run:

```bash
python3 -m unittest tests/test_validate_rendered_site.py -v
python3 scripts/validate_rendered_site.py --site _site --routes tests/legacy-routes.json
```

Expected: unit tests PASS; the full command exits 1 and lists the legacy routes not yet migrated.

- [ ] **Step 6: Commit the validator contract**

```bash
git add tests/legacy-routes.json tests/test_validate_rendered_site.py scripts/validate_rendered_site.py
git commit -m "test: define legacy route contract"
```

---

### Task 4: Preserve Legacy Collection Pages

**Files:**
- Create: `background/index.qmd`
- Create: `goalies/index.qmd`
- Create: `tennis/index.qmd`
- Create: `draft/index.qmd`
- Create: `post-regulation/index.qmd`

**Interfaces:**
- Consumes: route records with `series: page` and the primary About, Research, Subjects, and Archive routes.
- Produces: intentional content at all five non-home legacy collection paths.

- [ ] **Step 1: Verify the collection-route contract fails**

Run: `python3 scripts/validate_rendered_site.py --site _site --routes tests/legacy-routes.json --series page`

Expected: FAIL for `/background/`, `/goalies/`, `/tennis/`, `/draft/`, and `/post-regulation/`.

- [ ] **Step 2: Create the Background compatibility page**

Create `background/index.qmd`:

```markdown
---
title: "Background"
description: "The original background page now lives in the expanded About page."
toc: false
---

This material now lives on the expanded [About](/about/) page. The original story—from *Stat Shot*, through independent research and Statistics Canada, to current work—has been retained there.
```

- [ ] **Step 3: Create the four sports-context compatibility pages**

Create `goalies/index.qmd`:

```markdown
---
title: "Goalies"
description: "Archived and consolidated research about goalie performance and consistency."
toc: false
---

Goalie research is now organized by statistical subject. Start with [Goalie Performance](/research/goalie-performance/) or browse the complete [Archive](/archive/).
```

Create `draft/index.qmd`:

```markdown
---
title: "NHL Draft"
description: "Archived and consolidated research about NHL pick probability."
toc: false
---

Draft research is now organized by statistical subject. Start with [NHL Pick Probability](/research/nhl-pick-probability/) or browse the complete [Archive](/archive/).
```

Create `post-regulation/index.qmd`:

```markdown
---
title: "Post-regulation"
description: "Research about overtime, shootouts, randomness, and standings uncertainty."
toc: false
---

The original four-part post-regulation analysis remains in the [Archive](/archive/). It will be consolidated in a later editorial pass.
```

Create `tennis/index.qmd`:

```markdown
---
title: "Tennis tracking"
description: "Computer-vision notes from a tennis-tracking project."
toc: false
---

The tennis-tracking project is **paused with intent to return**. Its framework, object-detection, pipeline, data, and liveblog posts remain in the [Archive](/archive/).
```

- [ ] **Step 4: Render and verify all compatibility paths**

Run:

```bash
quarto render
python3 scripts/validate_rendered_site.py --site _site --routes tests/legacy-routes.json --series page
```

Expected: PASS.

- [ ] **Step 5: Commit the compatibility pages**

```bash
git add background goalies tennis draft post-regulation
git commit -m "feat: preserve legacy collection routes"
```

---

### Task 5: Migrate the Nine Goalie Archive Posts

**Files:**
- Move: `_posts/2022-03-28-goalie-consistency-1.md` → `2022/03/28/goalie-consistency-1.qmd`
- Move: `_posts/2022-03-30-goalie-consistency-2.md` → `2022/03/29/goalie-consistency-2.qmd`
- Move: `_posts/2022-04-02-goalie-consistency-3.md` → `2022/04/02/goalie-consistency-3.qmd`
- Move: `_posts/2022-04-07-goalie-consistency-4.md` → `2022/04/07/goalie-consistency-4.qmd`
- Move: `_posts/2023-05-17-goalie-performance-1.md` → `2023/05/17/goalie-performance-1.qmd`
- Move: `_posts/2023-05-22-goalie-performance-2.md` → `2023/05/22/goalie-performance-2.qmd`
- Move: `_posts/2023-07-08-goalie-performance-3.md` → `2023/07/08/goalie-performance-3.qmd`
- Move: `_posts/2024-07-21-goalie-performance-4.md` → `2024/07/30/goalie-performance-4.qmd`
- Move: `_posts/2024-07-30-goalie-performance-5.md` → `2024/07/30/goalie-performance-5.qmd`

**Interfaces:**
- Consumes: the `goalie` records in `tests/legacy-routes.json`, existing prose, and existing `/figs/goalie-*` and `/figs/goalie-performance-*` assets.
- Produces: nine static archive pages at the exact production routes, all with `status: archived`, `reading-time: true`, `sports: [Hockey, Goalies]`, valid descriptions, and no executable code.

- [ ] **Step 1: Confirm the goalie route subset fails**

Run: `python3 scripts/validate_rendered_site.py --site _site --routes tests/legacy-routes.json --series goalie`

Expected: FAIL with nine missing routes.

- [ ] **Step 2: Move the source files to production-dated Quarto paths**

Run the nine `git mv` operations listed in **Files**. The two non-obvious destinations are required by production history: Goalie Consistency part 2 uses `2022/03/29`, and Goalie Performance part 4 uses `2024/07/30`.

- [ ] **Step 3: Normalize archive front matter without changing analysis**

Use this structure in each moved file, keeping its existing title and production date and writing a one-sentence description from its opening question:

```yaml
---
title: "Goalie Performance: Empirical Bayes Save Percentage"
description: "An empirical Bayes framework for estimating goalie performance while accounting for uncertainty."
date: 2023-05-17
categories:
  - Bayesian statistics
  - Distributions and sampling
sports:
  - Hockey
  - Goalies
status: archived
reading-time: true
toc: true
execute:
  enabled: false
---
```

Apply these subject categories consistently:

- Goalie Consistency parts 1–4: `Probability and simulation`, `Distributions and sampling`.
- Goalie Performance parts 1–2: `Bayesian statistics`, `Distributions and sampling`.
- Goalie Performance part 3: `Bayesian statistics`, `Regression and calibration`.
- Goalie Performance parts 4–5: `Bayesian statistics`, `Distributions and sampling`.

Apply the contract as nine separately checked edits:

- [ ] Normalize front matter in `2022/03/28/goalie-consistency-1.qmd`.
- [ ] Normalize front matter in `2022/03/29/goalie-consistency-2.qmd`.
- [ ] Normalize front matter in `2022/04/02/goalie-consistency-3.qmd`.
- [ ] Normalize front matter in `2022/04/07/goalie-consistency-4.qmd`.
- [ ] Normalize front matter in `2023/05/17/goalie-performance-1.qmd`.
- [ ] Normalize front matter in `2023/05/22/goalie-performance-2.qmd`.
- [ ] Normalize front matter in `2023/07/08/goalie-performance-3.qmd`.
- [ ] Normalize front matter in `2024/07/30/goalie-performance-4.qmd`.
- [ ] Normalize front matter in `2024/07/30/goalie-performance-5.qmd`.

- [ ] **Step 4: Make the bodies valid Quarto Markdown**

For each moved file:

- remove the embedded `<head>`/Google Analytics block;
- remove the duplicate `[Post N]` heading beneath the title block;
- replace `<h5>` and `<h2>` body headings with `##` and `###` Markdown headings in hierarchical order;
- remove unmatched `<p>` wrappers and convert indented hyphen text into real Markdown lists;
- replace `length=` image attributes and centered image `<div>` blocks with Markdown figures;
- use adjacent prose to write alt text that states the quantity or scene, such as `Career adjusted save percentage distribution for the goalie sample`, rather than `chart` or a filename;
- keep all existing numerical results and figures; do not add executable chunks or regenerate output.

The expected figure form is:

```markdown
![Career adjusted save percentage distribution for the goalie sample.](/figs/goalie-six-one.png){fig-alt="Career adjusted save percentage distribution for the goalie sample." width="70%"}
```

Complete body cleanup one file at a time:

- [ ] Clean `2022/03/28/goalie-consistency-1.qmd`.
- [ ] Clean `2022/03/29/goalie-consistency-2.qmd`.
- [ ] Clean `2022/04/02/goalie-consistency-3.qmd`.
- [ ] Clean `2022/04/07/goalie-consistency-4.qmd`.
- [ ] Clean `2023/05/17/goalie-performance-1.qmd`.
- [ ] Clean `2023/05/22/goalie-performance-2.qmd`.
- [ ] Clean `2023/07/08/goalie-performance-3.qmd`.
- [ ] Clean `2024/07/30/goalie-performance-4.qmd`.
- [ ] Clean `2024/07/30/goalie-performance-5.qmd`.

- [ ] **Step 5: Repair the four known goalie link defects**

Make these exact replacements:

```text
/2022/04/04/goalie-consistency-1.html -> /2022/03/29/goalie-consistency-2.html
/2022/04/04/goalie-consistency-2.html -> /2022/04/02/goalie-consistency-3.html
/2022/04/04/goalie-consistency-3.html -> /2022/04/07/goalie-consistency-4.html
/2022/03/30/goalie-consistency-2.html -> /2022/03/29/goalie-consistency-2.html
```

The obsolete `/2023/06/26/goalie-performance-3.html` link in the legacy `goalies` collection source is not carried into the new compatibility page; the correct archived route is `/2023/07/08/goalie-performance-3.html`.

- [ ] **Step 6: Render, scan, and verify the goalie subset**

Run:

```bash
quarto render
rg -n "<head>|UA-177238175-1|length=" 2022/03/28 2022/03/29 2022/04/02 2022/04/07 2023/05/17 2023/05/22 2023/07/08 2024/07/30/goalie-performance-4.qmd 2024/07/30/goalie-performance-5.qmd
python3 scripts/validate_rendered_site.py --site _site --routes tests/legacy-routes.json --series goalie
```

Expected: `rg` prints no matches; the goalie route validator PASSes.

- [ ] **Step 7: Commit the goalie archive migration**

```bash
git add 2022/03/28 2022/03/29 2022/04/02 2022/04/07 2023/05/17 2023/05/22 2023/07/08 2024/07/30 _posts
git commit -m "content: migrate goalie archive posts"
```

---

### Task 6: Migrate the Six NHL Draft Archive Posts

**Files:**
- Move: `_posts/2021-11-28-draft-probabilities-1.md` → `2021/11/28/draft-probabilities-1.qmd`
- Move: `_posts/2023-06-16-draft-probabilities-2.md` → `2023/06/16/draft-probabilities-2.qmd`
- Move: `_posts/2023-06-20-draft-probabilities-3.md` → `2023/06/20/draft-probabilities-3.qmd`
- Move: `_posts/2023-07-02-draft-probabilities-4.md` → `2023/07/02/draft-probabilities-4.qmd`
- Move: `_posts/2023-07-07-draft-probabilities-5.md` → `2023/07/07/draft-probabilities-5.qmd`
- Move: `_posts/2024-07-30-draft-probabilities-6.md` → `2024/07/20/draft-probabilities-6.qmd`

**Interfaces:**
- Consumes: the `draft` route records, original draft prose, and existing `/figs/draft-*` assets.
- Produces: six static archive pages at exact production routes with `sports: [Hockey, NHL Draft]`, archive metadata, reading time, and no executable code.

- [ ] **Step 1: Confirm the draft route subset fails**

Run: `python3 scripts/validate_rendered_site.py --site _site --routes tests/legacy-routes.json --series draft`

Expected: FAIL with six missing routes.

- [ ] **Step 2: Move sources and normalize metadata**

Run the six `git mv` operations listed above. Preserve the front-matter publication dates, including `2024-07-20` for the source whose filename previously said `2024-07-30`.

Use the same archive fields as Task 5 with `sports: [Hockey, NHL Draft]` and these categories:

- part 1: `Probability and simulation`, `Distributions and sampling`;
- part 2: `Probability and simulation`, `Regression and calibration`;
- parts 3–6: `Probability and simulation`.

The part 2 front matter is the reference form:

```yaml
---
title: "NHL Draft: Deriving pick probabilities from draft rankings"
description: "A rank-ordered model that turns draft rankings into prospect pick distributions."
date: 2023-06-16
categories:
  - Probability and simulation
  - Regression and calibration
sports:
  - Hockey
  - NHL Draft
status: archived
reading-time: true
toc: true
execute:
  enabled: false
---
```

Apply metadata one file at a time:

- [ ] Normalize `2021/11/28/draft-probabilities-1.qmd` front matter.
- [ ] Normalize `2023/06/16/draft-probabilities-2.qmd` front matter.
- [ ] Normalize `2023/06/20/draft-probabilities-3.qmd` front matter.
- [ ] Normalize `2023/07/02/draft-probabilities-4.qmd` front matter.
- [ ] Normalize `2023/07/07/draft-probabilities-5.qmd` front matter.
- [ ] Normalize `2024/07/20/draft-probabilities-6.qmd` front matter.

- [ ] **Step 3: Normalize bodies without rerunning the models**

Apply Task 5's HTML, heading, list, figure, alt-text, and embedded-analytics cleanup rules. Preserve every existing result and figure. Do not convert prose code examples into executable chunks.

- [ ] Clean `2021/11/28/draft-probabilities-1.qmd`.
- [ ] Clean `2023/06/16/draft-probabilities-2.qmd`.
- [ ] Clean `2023/06/20/draft-probabilities-3.qmd`.
- [ ] Clean `2023/07/02/draft-probabilities-4.qmd`.
- [ ] Clean `2023/07/07/draft-probabilities-5.qmd`.
- [ ] Clean `2024/07/20/draft-probabilities-6.qmd`.

- [ ] **Step 4: Repair the known draft-series link defect**

In the archived part 5 source, replace:

```text
/2023/06/25/draft-probabilities-4.html -> /2023/07/02/draft-probabilities-4.html
```

- [ ] **Step 5: Render, scan, and verify the draft subset**

Run:

```bash
quarto render
rg -n "<head>|UA-177238175-1|length=" 2021/11/28 2023/06/16 2023/06/20 2023/07/02 2023/07/07 2024/07/20
python3 scripts/validate_rendered_site.py --site _site --routes tests/legacy-routes.json --series draft
```

Expected: `rg` prints no matches; the draft route validator PASSes.

- [ ] **Step 6: Commit the draft archive migration**

```bash
git add 2021/11/28 2023/06/16 2023/06/20 2023/07/02 2023/07/07 2024/07/20 _posts
git commit -m "content: migrate NHL draft archive posts"
```

---

### Task 7: Migrate the Four Post-Regulation Archive Posts

**Files:**
- Move: `_posts/2022-04-20-post-regulation-1.md` → `2022/04/20/post-regulation-1.qmd`
- Move: `_posts/2022-04-26-post-regulation-2.md` → `2022/04/26/post-regulation-2.qmd`
- Move: `_posts/2022-04-29-post-regulation-3.md` → `2022/04/29/post-regulation-3.qmd`
- Move: `_posts/2022-04-30-post-regulation-4.md` → `2022/04/30/post-regulation-4.qmd`

**Interfaces:**
- Consumes: the `post-regulation` route records and `/figs/post-regulation-*` assets.
- Produces: four static archive pages with `categories: [Probability and simulation, Distributions and sampling]`, `sports: [Hockey, Overtime]`, archive status, and exact routes.

- [ ] **Step 1: Confirm the post-regulation route subset fails**

Run: `python3 scripts/validate_rendered_site.py --site _site --routes tests/legacy-routes.json --series post-regulation`

Expected: FAIL with four missing routes.

- [ ] **Step 2: Move sources and apply the archive front-matter contract**

Run the four `git mv` operations. Preserve each title and production date. Use `execute: {enabled: false}`, `reading-time: true`, `status: archived`, both approved statistical categories, both sports contexts, and a one-sentence description derived from the post's opening question.

- [ ] **Step 3: Normalize the four bodies**

Apply Task 5's HTML, heading, list, figure, alt-text, and analytics cleanup. Preserve all simulations and numerical conclusions as historical output; do not rerun them.

- [ ] Clean `2022/04/20/post-regulation-1.qmd`.
- [ ] Clean `2022/04/26/post-regulation-2.qmd`.
- [ ] Clean `2022/04/29/post-regulation-3.qmd`.
- [ ] Clean `2022/04/30/post-regulation-4.qmd`.

- [ ] **Step 4: Repair the two known post-regulation links**

Make these exact replacements:

```text
/2022/04/24/post-regulation-1.html -> /2022/04/29/post-regulation-3.html
/2022/04/30/post-regulation-3.html -> /2022/04/30/post-regulation-4.html
```

- [ ] **Step 5: Render, scan, and verify the post-regulation subset**

Run:

```bash
quarto render
rg -n "<head>|UA-177238175-1|length=" 2022/04/20 2022/04/26 2022/04/29 2022/04/30/post-regulation-4.qmd
python3 scripts/validate_rendered_site.py --site _site --routes tests/legacy-routes.json --series post-regulation
```

Expected: `rg` prints no matches; the route validator PASSes.

- [ ] **Step 6: Commit the post-regulation archive migration**

```bash
git add 2022/04/20 2022/04/26 2022/04/29 2022/04/30 _posts
git commit -m "content: migrate post-regulation archive posts"
```

---

### Task 8: Migrate the Five Tennis Archive Posts and Video

**Files:**
- Move: `_posts/2022-09-16-tennis-liveblog.md` → `2022/09/16/tennis-liveblog.qmd`
- Move: `_posts/2023-01-15-tennis-framework.md` → `2023/01/15/tennis-framework.qmd`
- Move: `_posts/2023-08-01-tennis-data.md` → `2023/07/30/tennis-data.qmd`
- Move: `_posts/2023-07-25-tennis-object-detection.md` → `2024/07/25/tennis-object-detection.qmd`
- Move: `_posts/2023-07-30-tennis-pipeline.md` → `2024/07/30/tennis-pipeline.qmd`
- Create: `figs/player-detect-demo.mp4`

**Interfaces:**
- Consumes: `figs/player-detect-demo.mov`, tennis JPG/PNG figures, and the `tennis` route records.
- Produces: five static archive pages with `sports: [Tennis]`, `categories: []`, exact production dates/routes, and a browser-compatible MP4 embed with a textual fallback.

- [ ] **Step 1: Confirm the tennis route subset fails**

Run: `python3 scripts/validate_rendered_site.py --site _site --routes tests/legacy-routes.json --series tennis`

Expected: FAIL with five missing routes.

- [ ] **Step 2: Move sources to their production-dated paths**

Run the five `git mv` operations listed above. The object-detection and pipeline destinations deliberately use their 2024 production dates; the tennis-data destination deliberately uses `2023/07/30`.

- [ ] **Step 3: Normalize tennis metadata and bodies**

Use the archive front-matter contract with `sports: [Tennis]`, an empty `categories: []`, `status: archived`, `reading-time: true`, `toc: true`, and `execute: {enabled: false}`. The tennis work stays visible as a sports/technical project without inventing a statistical category that the posts do not use.

Apply Task 5's body cleanup rules. Retain computer-vision terminology, images, code excerpts, and project-history details, but do not execute the code or claim the old pipeline was reproduced.

- [ ] Normalize and clean `2022/09/16/tennis-liveblog.qmd`.
- [ ] Normalize and clean `2023/01/15/tennis-framework.qmd`.
- [ ] Normalize and clean `2023/07/30/tennis-data.qmd`.
- [ ] Normalize and clean `2024/07/25/tennis-object-detection.qmd`.
- [ ] Normalize and clean `2024/07/30/tennis-pipeline.qmd`.

- [ ] **Step 4: Replace the nonexistent liveblog link**

In the liveblog, change the linked heading that points to `/2022/09/18/classifying-game-state.html` into an unlinked heading with the same words:

```markdown
### 1. Classify game states
```

- [ ] **Step 5: Create and embed the browser-compatible video**

Run:

```bash
ffmpeg -i figs/player-detect-demo.mov -c:v libx264 -crf 23 -preset slow -movflags +faststart -an figs/player-detect-demo.mp4
ffprobe -v error -show_entries format=format_name,duration -of default=noprint_wrappers=1 figs/player-detect-demo.mp4
```

Expected: `format_name` contains `mov,mp4` and duration is greater than zero.

Replace the `.mov` image/embed markup in the relevant tennis article with:

```markdown
{{< video /figs/player-detect-demo.mp4 width="100%" title="Player detection demonstration" >}}

The clip demonstrates the player-detection stage of the original tracking pipeline.
```

Retain `figs/player-detect-demo.mov` so the historical asset URL remains available.

- [ ] **Step 6: Render, scan, and verify the tennis subset**

Run:

```bash
quarto render
rg -n "<head>|UA-177238175-1|length=|classifying-game-state.html" 2022/09/16 2023/01/15 2023/07/30 2024/07/25 2024/07/30/tennis-pipeline.qmd
python3 scripts/validate_rendered_site.py --site _site --routes tests/legacy-routes.json --series tennis
```

Expected: `rg` prints no matches; the route validator PASSes.

- [ ] **Step 7: Commit the tennis archive migration**

```bash
git add 2022/09/16 2023/01/15 2023/07/30 2024/07/25 2024/07/30 figs/player-detect-demo.mp4 _posts
git commit -m "content: migrate tennis archive posts"
```

---

### Task 9: Consolidate Goalie Performance into One Canonical Article

**Files:**
- Create: `research/goalie-performance/index.qmd`
- Create: `tests/test_canonical_articles.py`
- Modify: `2023/05/17/goalie-performance-1.qmd`
- Modify: `2023/05/22/goalie-performance-2.qmd`
- Modify: `2023/07/08/goalie-performance-3.qmd`
- Modify: `2024/07/30/goalie-performance-4.qmd`
- Modify: `2024/07/30/goalie-performance-5.qmd`
- Modify: `index.qmd`

**Interfaces:**
- Consumes: the five migrated Goalie Performance archive sources and their existing figures.
- Produces: `/research/goalie-performance/`, a canonical source contract, and archive-to-canonical notices.

- [ ] **Step 1: Write the canonical source test**

Create `tests/test_canonical_articles.py`:

```python
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


def source_contract(relative_path, headings, minimum_words, maximum_words):
    text = (ROOT / relative_path).read_text(encoding="utf-8")
    for heading in headings:
        if f"## {heading}" not in text:
            raise AssertionError(f"{relative_path}: missing heading {heading}")
    words = re.findall(r"\b[\w’'-]+\b", text)
    if not minimum_words <= len(words) <= maximum_words:
        raise AssertionError(f"{relative_path}: {len(words)} words outside {minimum_words}-{maximum_words}")
    if "retains the original analysis" not in text:
        raise AssertionError(f"{relative_path}: missing historical-analysis note")


class CanonicalArticleTest(unittest.TestCase):
    def test_goalie_performance_contract(self):
        source_contract(
            "research/goalie-performance/index.qmd",
            [
                "Why goalie performance needs shrinkage",
                "Estimating talent with empirical Bayes",
                "Adjusting for shot quality",
                "Age, opportunity, and selection",
                "What the distribution looks like",
                "How much evidence is enough?",
                "Limitations",
                "Technical appendix",
            ],
            2500,
            4200,
        )

    def test_nhl_pick_probability_contract(self):
        source_contract(
            "research/nhl-pick-probability/index.qmd",
            [
                "From rankings to probabilities",
                "The rank-ordered logit model",
                "Prospect pick distributions",
                "Applying uncertainty to draft value",
                "A probability-aware drafting strategy",
                "What the post-draft results showed",
                "Limitations",
                "Technical appendix",
            ],
            3200,
            5500,
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the goalie canonical test and verify it fails**

Run: `python3 -m unittest tests.test_canonical_articles.CanonicalArticleTest.test_goalie_performance_contract -v`

Expected: FAIL because `research/goalie-performance/index.qmd` does not exist.

- [ ] **Step 3: Write the canonical front matter and historical note**

Use this exact front matter at `research/goalie-performance/index.qmd`:

```yaml
---
title: "Goalie Performance"
description: "Estimating NHL goalie performance with empirical Bayes, shot-quality adjustment, age context, and honest sample-size limits."
date: 2023-05-17
date-modified: 2026-08-28
categories:
  - Bayesian statistics
  - Distributions and sampling
  - Regression and calibration
sports:
  - Hockey
  - Goalies
status: canonical
reading-time: true
toc: true
execute:
  enabled: false
---

::: {.archive-notice}
This article consolidates five posts published between 2023 and 2024. It reorganizes the original prose, results, and figures, and retains the original analysis; the underlying data and models were not reconstructed for this edition.
:::
```

- [ ] **Step 4: Assemble the complete article under the tested headings**

Use this source map and remove repetition instead of merely concatenating installments:

- **Why goalie performance needs shrinkage:** the motivating unpredictability discussion and sample-size problem from part 1.
- **Estimating talent with empirical Bayes:** the prior/posterior explanation, initial save-percentage model, and `goalie-performance-1-*` figures from part 1.
- **Adjusting for shot quality:** adjusted save percentage, likelihood/prior discussion, and `goalie-performance-2-*` figures from part 2.
- **Age, opportunity, and selection:** age adjustment and career-window caveats from part 3, plus the selection issue exposed in part 5.
- **What the distribution looks like:** the mixture/distribution exploration and corresponding figures from part 4.
- **How much evidence is enough?:** the career-length, shots-faced, and posterior-path material from part 5, with duplicated population summaries included once.
- **Limitations:** explicitly distinguish observed performance from latent talent; identify prior sensitivity, survivor/selection bias, age confounding, possible outcome leakage in derived adjustments, and the absence of a fresh validation run.
- **Technical appendix:** retain the existing equations and derivation details, but correct notation only where the intended quantity is unambiguous from the original text.

Do not introduce new estimates. When the original sources conflict or a number cannot be verified without rerunning data, omit the disputed derived number and explain the qualitative conclusion instead.

Draft and review one section at a time:

- [ ] Write `Why goalie performance needs shrinkage` from part 1.
- [ ] Write `Estimating talent with empirical Bayes` from part 1.
- [ ] Write `Adjusting for shot quality` from part 2.
- [ ] Write `Age, opportunity, and selection` from parts 3 and 5.
- [ ] Write `What the distribution looks like` from part 4.
- [ ] Write `How much evidence is enough?` from part 5.
- [ ] Write `Limitations` without adding new empirical claims.
- [ ] Write `Technical appendix` from the existing derivations.
- [ ] Read the assembled article once for duplicated claims and transitions.

- [ ] **Step 5: Add archive supersession notices**

Immediately after front matter in each of the five archived installments, add:

```markdown
::: {.archive-notice}
This installment is preserved in its original context. Read the consolidated [Goalie Performance](/research/goalie-performance/) article for the complete argument.
:::
```

- [ ] **Step 6: Point the homepage feature to the canonical article**

In `index.qmd`, replace the Goalie Performance archive URL with:

```markdown
- [Goalie Performance](/research/goalie-performance/) — Estimating talent while respecting small-sample uncertainty. · 18 min
```

- [ ] **Step 7: Run article, route, and browser tests**

Run:

```bash
python3 -m unittest tests.test_canonical_articles.CanonicalArticleTest.test_goalie_performance_contract -v
quarto render
python3 scripts/validate_rendered_site.py --site _site --routes tests/legacy-routes.json --series goalie
npm test
```

Expected: every command PASSes.

- [ ] **Step 8: Commit the canonical goalie article**

```bash
git add research/goalie-performance tests/test_canonical_articles.py 2023/05/17 2023/05/22 2023/07/08 2024/07/30 index.qmd
git commit -m "content: consolidate goalie performance research"
```

---

### Task 10: Consolidate NHL Pick Probability into One Canonical Article

**Files:**
- Create: `research/nhl-pick-probability/index.qmd`
- Modify: `2021/11/28/draft-probabilities-1.qmd`
- Modify: `2023/06/16/draft-probabilities-2.qmd`
- Modify: `2023/06/20/draft-probabilities-3.qmd`
- Modify: `2023/07/02/draft-probabilities-4.qmd`
- Modify: `2023/07/07/draft-probabilities-5.qmd`
- Modify: `2024/07/20/draft-probabilities-6.qmd`
- Modify: `index.qmd`

**Interfaces:**
- Consumes: six migrated draft archive sources and existing draft figures.
- Produces: `/research/nhl-pick-probability/` and archive-to-canonical notices.

- [ ] **Step 1: Run the draft canonical test and verify it fails**

Run: `python3 -m unittest tests.test_canonical_articles.CanonicalArticleTest.test_nhl_pick_probability_contract -v`

Expected: FAIL because `research/nhl-pick-probability/index.qmd` does not exist.

- [ ] **Step 2: Write the canonical front matter and historical note**

Create `research/nhl-pick-probability/index.qmd` with:

```yaml
---
title: "NHL Pick Probability"
description: "Turning draft rankings into prospect pick distributions, decision value, and a probability-aware drafting strategy."
date: 2021-11-28
date-modified: 2026-08-28
categories:
  - Probability and simulation
  - Regression and calibration
  - Distributions and sampling
sports:
  - Hockey
  - NHL Draft
status: canonical
reading-time: true
toc: true
execute:
  enabled: false
---

::: {.archive-notice}
This article consolidates six posts published between 2021 and 2024. It reorganizes the original prose, results, and figures, and retains the original analysis; the underlying data and models were not reconstructed for this edition.
:::
```

- [ ] **Step 3: Assemble the complete article under the tested headings**

Use this source map:

- **From rankings to probabilities:** the user-mock-draft origin story from part 1 and the move to professional rankings from part 2.
- **The rank-ordered logit model:** the methodology and assumptions from part 2, retaining existing equations and visuals.
- **Prospect pick distributions:** distribution construction, interpretation, and calibration discussion from parts 1–2.
- **Applying uncertainty to draft value:** the decision framework and prospect-value uncertainty from parts 3–4.
- **A probability-aware drafting strategy:** the strategy and tradeoff logic from part 5.
- **What the post-draft results showed:** the concise retrospective from part 6, framed as an observation of that draft rather than a fresh validation.
- **Limitations:** ranking-source dependence, confidence/calibration limits, value-model dependence, untested temporal generalization, and the absence of a new model run.
- **Technical appendix:** existing formulas, definitions, and supplementary figures needed to follow the method.

Resolve the two known numerical-writing problems without rerunning analysis:

- The original `25% chance of -22 WAR` wording must not be presented as a general empirical probability; either attribute it narrowly to the original model scenario or remove the numeric flourish.
- The original text/table conflict between `3.683` and `3.564` must not be silently resolved. Omit the disputed total from the canonical narrative and state the directional comparison supported by both versions.

Draft and review one section at a time:

- [ ] Write `From rankings to probabilities` from parts 1–2.
- [ ] Write `The rank-ordered logit model` from part 2.
- [ ] Write `Prospect pick distributions` from parts 1–2.
- [ ] Write `Applying uncertainty to draft value` from parts 3–4.
- [ ] Write `A probability-aware drafting strategy` from part 5.
- [ ] Write `What the post-draft results showed` from part 6.
- [ ] Write `Limitations` with the two numerical-writing rules above.
- [ ] Write `Technical appendix` from the existing formulas and definitions.
- [ ] Read the assembled article once for duplicated claims and transitions.

- [ ] **Step 4: Add archive supersession notices**

Immediately after front matter in each of the six archived installments, add:

```markdown
::: {.archive-notice}
This installment is preserved in its original context. Read [NHL Pick Probability](/research/nhl-pick-probability/) for the consolidated argument.
:::
```

- [ ] **Step 5: Point the homepage feature to the canonical article**

In `index.qmd`, replace the draft archive URL with:

```markdown
- [NHL Pick Probability](/research/nhl-pick-probability/) — Turning rankings into pick distributions and decisions. · 23 min
```

- [ ] **Step 6: Run article, route, and browser tests**

Run:

```bash
python3 -m unittest tests.test_canonical_articles.CanonicalArticleTest.test_nhl_pick_probability_contract -v
quarto render
python3 scripts/validate_rendered_site.py --site _site --routes tests/legacy-routes.json --series draft
npm test
```

Expected: every command PASSes.

- [ ] **Step 7: Commit the canonical draft article**

```bash
git add research/nhl-pick-probability 2021/11/28 2023/06/16 2023/06/20 2023/07/02 2023/07/07 2024/07/20 index.qmd
git commit -m "content: consolidate NHL pick probability research"
```

---

### Task 11: Complete Listings, Subjects, Feed, and Full Site Contract

**Files:**
- Modify: `index.qmd`
- Modify: `research/index.qmd`
- Modify: `subjects/index.qmd`
- Modify: `archive/index.qmd`
- Modify: `tests/test_rendered_site.py`
- Modify: `scripts/validate_rendered_site.py`

**Interfaces:**
- Consumes: both canonical articles, all 24 archive sources, and Quarto's listing fields `reading-time`, `categories`, and custom `sports`.
- Produces: root RSS at `/index.xml`, chronological current/archive listings, statistical-subject navigation, sitemap/discovery checks, and a full passing local content contract.

- [ ] **Step 1: Extend the rendered-site smoke test for discovery output**

Add to `RenderedSiteSmokeTest` in `tests/test_rendered_site.py`:

```python
    def test_discovery_outputs_exist(self):
        required = [
            SITE / "index.xml",
            SITE / "sitemap.xml",
            SITE / "404.html",
            SITE / "research" / "index.html",
            SITE / "subjects" / "index.html",
            SITE / "archive" / "index.html",
        ]
        missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
        self.assertEqual(missing, [])
```

- [ ] **Step 2: Run the discovery test and verify it fails**

Run: `python3 -m unittest tests.test_rendered_site.RenderedSiteSmokeTest.test_discovery_outputs_exist -v`

Expected: FAIL because the root RSS feed is not yet configured.

- [ ] **Step 3: Add current and recent listings to the homepage**

Add this `listing` block to `index.qmd` front matter:

```yaml
listing:
  id: recent-writing
  contents:
    - "research/goalie-performance/index.qmd"
    - "research/nhl-pick-probability/index.qmd"
    - "posts/**/index.qmd"
  sort: "date desc"
  type: table
  fields: [date, title, reading-time, categories]
  field-required: [title, date, description, status]
  sort-ui: false
  filter-ui: false
  page-size: 5
  feed: true
```

Replace the sentence beneath `## Recent writing` with the listing location and archive link:

```markdown
::: {#recent-writing}
:::

[Browse all research and the historical archive.](/research/)
```

- [ ] **Step 4: Create current and historical listings on Research**

Replace `research/index.qmd` with:

```markdown
---
title: "Research"
description: "Sports statistics research in chronological order."
toc: false
listing:
  - id: current-research
    contents:
      - "goalie-performance/index.qmd"
      - "nhl-pick-probability/index.qmd"
      - "../posts/**/index.qmd"
    sort: "date desc"
    type: table
    fields: [date, title, reading-time, categories, sports]
    field-required: [title, date, description, status]
    sort-ui: false
    filter-ui: false
  - id: historical-research
    contents: "../20*/**/*.qmd"
    sort: "date desc"
    type: table
    fields: [date, title, reading-time, categories, sports]
    field-required: [title, date, description, status]
    sort-ui: false
    filter-ui: false
    page-size: 30
---

## Current and consolidated

::: {#current-research}
:::

## Archive

Earlier work remains available in its original context.

::: {#historical-research}
:::
```

- [ ] **Step 5: Turn Archive into the complete historical listing**

Replace `archive/index.qmd` with:

```markdown
---
title: "Archive"
description: "Earlier sports statistics posts, preserved in their original context."
toc: false
listing:
  id: archive-list
  contents: "../20*/**/*.qmd"
  sort: "date desc"
  type: table
  fields: [date, title, reading-time, categories, sports]
  field-required: [title, date, description, status]
  sort-ui: false
  filter-ui: false
  page-size: 30
---

The archive preserves earlier work and its original publication context. Some installments now point to a consolidated article, but the original pages remain available.

::: {#archive-list}
:::
```

- [ ] **Step 6: Link statistical subjects to actual writing**

Replace `subjects/index.qmd` with the approved four-subject index and compact reading lists:

```markdown
---
title: "Statistical subjects"
description: "Research organized by the statistical ideas used."
toc: false
---

## Bayesian statistics

Empirical Bayes, priors and posteriors, and shrinkage.

- [Goalie Performance](/research/goalie-performance/)
- [Empirical Bayes Save Percentage](/2023/05/17/goalie-performance-1.html)
- [Empirical Bayes Adjusted Save Percentage](/2023/05/22/goalie-performance-2.html)

## Probability and simulation

Draft uncertainty, overtime formats, and expected value.

- [NHL Pick Probability](/research/nhl-pick-probability/)
- [Goalie Consistency: Does it matter?](/2022/03/28/goalie-consistency-1.html)
- [Post-regulation: Measuring uncertainty](/2022/04/26/post-regulation-2.html)

## Distributions and sampling

Beta-binomial models, mixture models, and sample-size questions.

- [Goalie Performance](/research/goalie-performance/)
- [NHL Pick Probability](/research/nhl-pick-probability/)
- [Goalie Performance: Sample Sizes](/2024/07/30/goalie-performance-5.html)

## Regression and calibration

Logistic models, age curves, and model reliability.

- [NHL Pick Probability](/research/nhl-pick-probability/)
- [Goalie Performance: Adjusting for Age](/2023/07/08/goalie-performance-3.html)
```

- [ ] **Step 7: Set the validator's media ceiling to the known legacy envelope**

Change the signature in `scripts/validate_rendered_site.py` to:

```python
def validate_asset_sizes(site: Path, limit_bytes: int = 7_000_000) -> list[str]:
```

This preserves the 5.3 MB original hero image and 6.4 MB historical MOV while still failing newly introduced web assets above 7 MB. The browser-compatible MP4 should be materially smaller than the MOV.

- [ ] **Step 8: Render and run the complete local content contract**

Run:

```bash
quarto render
python3 -m unittest discover -s tests -p "test_*.py" -v
python3 scripts/validate_rendered_site.py --site _site --routes tests/legacy-routes.json
npm test
```

Expected: all Python tests PASS; all 30 legacy page/post routes resolve; internal links, local assets, metadata, alt text, and media-size checks PASS; Playwright and axe PASS.

- [ ] **Step 9: Commit listings and discovery behavior**

```bash
git add index.qmd research/index.qmd subjects/index.qmd archive/index.qmd tests/test_rendered_site.py scripts/validate_rendered_site.py
git commit -m "feat: complete research and archive discovery"
```

---

### Task 12: Remove Jekyll, Add CI/Deployment, and Launch

**Files:**
- Create: `.github/workflows/site.yml`
- Modify: `README.md`
- Delete: `_config.yml`
- Delete: `Gemfile`
- Delete: `Gemfile.lock`
- Delete: `home.md`
- Delete: `background.md`
- Delete: `goalies.md`
- Delete: `tennis.md`
- Delete: `draft.md`
- Delete: `post-regulation.md`
- Delete: `.DS_Store`
- Delete: `_posts/.DS_Store`
- Delete: `figs/.DS_Store`

**Interfaces:**
- Consumes: a fully passing local Quarto site and the `master` source branch.
- Produces: one GitHub Actions workflow that validates pull requests and deploys `_site` from `master` through GitHub Pages.

- [ ] **Step 1: Write the GitHub Actions workflow**

Create `.github/workflows/site.yml`:

```yaml
name: Build and publish Quarto site

on:
  pull_request:
  push:
    branches: [master]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Quarto
        uses: quarto-dev/quarto-actions/setup@v2
        with:
          version: 1.10.18

      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: 20.20.1
          cache: npm

      - name: Install test dependencies
        run: npm ci

      - name: Install Chromium
        run: npx playwright install --with-deps chromium

      - name: Render site
        run: quarto render

      - name: Run Python contracts
        run: python3 -m unittest discover -s tests -p "test_*.py" -v

      - name: Validate rendered output
        run: python3 scripts/validate_rendered_site.py --site _site --routes tests/legacy-routes.json

      - name: Run browser and accessibility checks
        run: npm test

      - name: Configure Pages
        if: github.event_name != 'pull_request'
        uses: actions/configure-pages@v5

      - name: Upload Pages artifact
        if: github.event_name != 'pull_request'
        uses: actions/upload-pages-artifact@v3
        with:
          path: _site

  deploy:
    if: github.event_name != 'pull_request' && github.ref == 'refs/heads/master'
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 2: Replace README with exact authoring and verification instructions**

Replace `README.md` with:

````markdown
# spazznolo.github.io

Jeremie Spagnolo's sports-statistics blog, built with Quarto 1.10.18 and published to GitHub Pages.

## Local preview

Requirements: Quarto 1.10.18, Node.js 20.20.1, npm, Python 3, and Chromium installed by Playwright.

```bash
npm ci
npx playwright install chromium
quarto preview
```

## Verify a production render

```bash
quarto render
python3 -m unittest discover -s tests -p "test_*.py" -v
python3 scripts/validate_rendered_site.py --site _site --routes tests/legacy-routes.json
npm test
```

## Start a new post

Copy `templates/post.qmd` to `posts/<slug>/index.qmd`, replace its example metadata and instructional prose, and leave `draft: true` until publication. New computational posts may use frozen R, Python, Julia, Observable, or Shinylive output; historical archive posts are intentionally non-executable.

## Publishing

Pull requests run the full render and test contract. A passing push to `master` deploys the rendered `_site` artifact through GitHub Pages.
````

- [ ] **Step 3: Prove Jekyll and legacy analytics are no longer referenced**

Run before deleting files:

```bash
rg -n "jekyll|remote_theme|UA-177238175-1|googletagmanager.com/gtag/js" --glob '!docs/**' --glob '!_site/**' --glob '!node_modules/**'
```

Expected: matches are confined to the Jekyll configuration, Gem files, and old root Markdown sources scheduled for deletion. GA4 is configured once in `_quarto.yml` and is not manually embedded in content.

- [ ] **Step 4: Remove the obsolete publishing stack and tracked Finder metadata**

Run:

```bash
git rm _config.yml Gemfile Gemfile.lock home.md background.md goalies.md tennis.md draft.md post-regulation.md
git rm .DS_Store _posts/.DS_Store figs/.DS_Store
```

If `_posts/` is empty after the earlier `git mv` operations, let Git remove the directory naturally; do not use a recursive broad delete command.

- [ ] **Step 5: Run the final clean-build verification**

Render from a clean `_site` directory using a recoverable move rather than deletion:

```bash
site_backup_dir="$(mktemp -d /tmp/spazznolo-quarto-site.XXXXXX)"
mv _site "$site_backup_dir/_site"
quarto render
python3 -m unittest discover -s tests -p "test_*.py" -v
python3 scripts/validate_rendered_site.py --site _site --routes tests/legacy-routes.json
npm test
rg -n "remote_theme|UA-177238175-1|<head>|length=" --glob '*.qmd' --glob '*.yml'
```

Expected: render and all tests PASS; the final `rg` prints no matches. The moved prior render can be discarded through Finder after verification.

- [ ] **Step 6: Perform visual review at required widths and modes**

Run `quarto preview --port 4174`, then inspect the homepage, both canonical articles, one archive article containing formulas, and the tennis video at 320px, 768px, and 1440px. Verify dark default, light toggle, keyboard navigation, no horizontal overflow, visible focus, readable 13px copy, white dark-mode About text, correct figure captions, code folding, and a working video fallback.

Expected: no clipping, duplicate site name, split content grid, empty alt text, or mint-green accent remains.

- [ ] **Step 7: Commit the production workflow and Jekyll removal**

```bash
git add .github/workflows/site.yml README.md
git add -u
git commit -m "build: replace Jekyll publishing with Quarto"
```

- [ ] **Step 8: Configure GitHub Pages for workflow deployment**

Run:

```bash
gh auth status
gh api --method PUT repos/spazznolo/spazznolo.github.io/pages -f build_type=workflow
```

Expected: authentication succeeds and the Pages API accepts `build_type=workflow`. If repository policy rejects the API update, set **Repository Settings → Pages → Build and deployment → Source** to **GitHub Actions**, then rerun the next step.

- [ ] **Step 9: Push and watch the production deployment**

Run:

```bash
git push origin master
gh run watch "$(gh run list --workflow site.yml --limit 1 --json databaseId --jq '.[0].databaseId')" --exit-status
curl -fsS https://spazznolo.github.io/robots.txt
curl -fsS https://spazznolo.github.io/index.xml
curl -fsS https://spazznolo.github.io/2023/05/17/goalie-performance-1.html
curl -fsS https://spazznolo.github.io/research/goalie-performance/
```

Expected: the workflow exits successfully and all four production requests return content.

- [ ] **Step 10: Review the live site and record the release**

Open `https://spazznolo.github.io/` and repeat the Task 12 Step 6 visual sample against production. If it matches the verified local build, create an annotated tag:

```bash
git tag -a quarto-relaunch-2026-08-28 -m "Quarto blog relaunch"
git push origin quarto-relaunch-2026-08-28
```

Expected: the homepage, canonical articles, archive route, video, RSS, sitemap, 404 page, dark/light toggle, and all legacy links behave like the local release candidate.

---

## Final Acceptance Checklist

- [ ] Quarto 1.10.18 renders the site from a clean checkout.
- [ ] All 6 legacy pages and all 24 legacy post routes resolve.
- [ ] Both canonical articles pass their structure, historical-note, and word-count contracts.
- [ ] No historical analysis is executable or described as freshly reproduced.
- [ ] New-post template is executable-ready, frozen by default, and excluded from rendering while it remains under `templates/`.
- [ ] Homepage has one visible name treatment, one vertical stream, Source Code Pro, white About text, warm yellow accent, original introduction, and the original image.
- [ ] Research, Subjects, About, Archive, GitHub, RSS, sitemap, robots, and 404 paths work.
- [ ] GA4 appears once; Universal Analytics and inline analytics are absent.
- [ ] Internal links, local assets, metadata, alt text, media sizes, accessibility, keyboard operation, and responsive widths pass.
- [ ] Jekyll files and tracked `.DS_Store` files are absent.
- [ ] GitHub Actions passes before Pages deploys.
- [ ] The production release is tagged `quarto-relaunch-2026-08-28` only after the live review passes.

## Primary Documentation References

- Quarto GitHub Pages publishing: `https://quarto.org/docs/publishing/github-pages.html`
- Quarto blogs, feeds, drafts, and frozen posts: `https://quarto.org/docs/websites/website-blog.html`
- Quarto listings and reading-time fields: `https://quarto.org/docs/websites/website-listings.html`
- Quarto dark/light theming: `https://quarto.org/docs/output-formats/html-themes.html`
- Quarto video embedding: `https://quarto.org/docs/authoring/videos.html`
