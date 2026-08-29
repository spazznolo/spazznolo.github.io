# Task 12 report — local release candidate (Steps 1–7)

## Result

Task 12 Steps 1–7 are implemented in the Quarto worktree. The production workflow and authoring README are present, the obsolete Jekyll publishing stack and tracked Finder metadata are removed, and the clean local release candidate passes the content, route, accessibility, responsive, and browser contracts.

Steps 8–10 were not executed: GitHub Pages configuration, push, production deployment/live review, and release tagging were intentionally not performed.

## Exact approved deletions

The following files were removed with `git rm`:

- `_config.yml`
- `Gemfile`
- `Gemfile.lock`
- `home.md`
- `background.md`
- `goalies.md`
- `tennis.md`
- `draft.md`
- `post-regulation.md`
- `.DS_Store`
- `_posts/.DS_Store`
- `figs/.DS_Store`

No recursive directory deletion was used. The prior generated `_site` was moved recoverably to `/private/tmp/spazznolo-quarto-site.EPH6I1/_site` before rendering.

## Implementation

- Created `.github/workflows/site.yml` with pull-request validation, `master` build/deploy gating, Quarto 1.10.18, Node 20.20.1, npm/Chromium installation, Python contracts, rendered-output validation, Playwright/Axe checks, and Pages artifact/deployment steps.
- Replaced `README.md` with the approved Quarto preview, production verification, new-post, and publishing instructions.

The pre-deletion scan found legacy references only in the scheduled files: Jekyll references in `Gemfile`, `Gemfile.lock`, and `_config.yml`; the old Universal Analytics property in `_config.yml`; and old inline gtag snippets in `home.md` and `background.md`. The post-deletion scan produced no Jekyll, Universal Analytics, or inline gtag matches. The only remaining analytics configuration is `_quarto.yml:26` (`G-DGRHZS5DNM`).

## Verification commands and results

- `/tmp/quarto-1.10.18-expanded/quarto-core.pkg/Payload/bin/quarto --version` — PASS, `1.10.18`.
- `/tmp/quarto-1.10.18-expanded/quarto-core.pkg/Payload/bin/quarto render` after the recoverable `_site` move — PASS, all 37 configured inputs.
- `python3 -m unittest discover -s tests -p "test_*.py" -v` — PASS, 24/24.
- `python3 scripts/validate_rendered_site.py --site _site --routes tests/legacy-routes.json` — PASS, including all 30 legacy routes, links/assets, metadata/canonical URLs, alt text, listing sources, and the 7 MB media ceiling.
- `npm test` — PASS, 19/19 Playwright/Axe, responsive, homepage, and navigation tests. The initial sandboxed server bind was denied; the unchanged command passed with local socket permission.
- `rg -n "remote_theme|UA-177238175-1|<head>|length=" --glob '*.qmd' --glob '*.yml'` — PASS, no matches.
- `rg -n 'google-analytics|G-DGRHZS5DNM|UA-177238175-1|googletagmanager.com/gtag/js' ...` — PASS, one GA4 declaration in `_quarto.yml` only.
- Ruby YAML workflow contract — PASS: name/triggers, build/deploy jobs, Quarto version, Node version, validator, and browser test steps verified. `actionlint` was unavailable locally.
- `git diff --check` — PASS.

## Local visual evidence

Ran `/tmp/quarto-1.10.18-expanded/quarto-core.pkg/Payload/bin/quarto preview --port 4174` and inspected the homepage, both canonical articles, the formula-bearing archive article `/2022/03/28/goalie-consistency-1.html`, and the tennis video page `/2022/09/16/tennis-liveblog.html`.

Automated browser evidence at 320px, 768px, and 1440px found no horizontal overflow on all five sampled routes, no empty image alt text, the warm dark background (`rgb(11, 10, 8)`), and the expected video source. The formula archive page exposed one formula figure with an accurate alt text. The video loaded locally with `readyState=4` and `Loaded: 100.00%`. The homepage light toggle rendered the light background (`rgb(247, 242, 232)`) and restored the dark default. Keyboard Tab focus produced `:focus-visible` on the navbar link. Screenshots were inspected for the 320px dark homepage, 1440px dark canonical article, and 768px light homepage.

### Manual-review residuals

- The historical fenced code excerpts render as accessible code blocks, but Quarto emits no `<details>` folding control for these non-executable excerpts (`code-fold: true` remains configured globally). This is consistent with the historical/non-reproducible boundary but should be reconsidered if collapsible historical snippets are required.
- The video element has no native fallback text node; its adjacent explanatory paragraph is present and the MP4 loads successfully locally. A future content pass could add explicit fallback text if desired.

## Commit and scope

The Step 7 commit command is:

```bash
git add .github/workflows/site.yml README.md task-12-report.md
git add -u
git commit -m "build: replace Jekyll publishing with Quarto"
```

Only Steps 1–7 changes are in scope. `.superpowers/`, generated `_site/`, temporary render backups, and generated Python caches were not staged. Steps 8–10 were explicitly not executed.
