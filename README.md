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
