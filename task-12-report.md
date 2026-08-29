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

- The original local-review residuals for historical code disclosures and native video fallback were resolved in review fix round 1 below. `actionlint` remains unavailable in the local toolchain; Ruby YAML parsing and explicit workflow contract checks passed.

## Commit and scope

The Step 7 commit command is:

```bash
git add .github/workflows/site.yml README.md task-12-report.md
git add -u
git commit -m "build: replace Jekyll publishing with Quarto"
```

Only Steps 1–7 changes are in scope. `.superpowers/`, generated `_site/`, temporary render backups, and generated Python caches were not staged. Steps 8–10 were explicitly not executed.

## Task 12 review fix round 1 evidence

The review findings were addressed locally without changing the Step 8–10 boundary:

- The build job now has only `contents: read`; Pages and OIDC write permissions exist only on the deploy job. Build creates and uploads the artifact before deploy, while deploy runs only the pinned `deploy-pages` action and no repository-controlled checkout or command.
- At `max-width: 480px`, listing rows become stacked, labeled blocks. The semantic table header remains in the DOM, and title, date, reading time, and subjects values remain readable at 320px.
- The tennis shortcode was replaced by explicit HTML5 `<video>` markup with a native fallback sentence and direct MP4 link. The explanatory paragraph remains in the article, and `figs/player-detect-demo.mov` is unchanged.
- All six third-party actions are pinned to reviewed immutable commits resolved from official GitHub release refs, with release comments: checkout `11d5960a326750d5838078e36cf38b85af677262` (v4), Quarto setup `8a96df13519ee81fd526f2dfca5962811136661b` (v2), setup-node `49933ea5288caeca8642d1e84afbd3f7d6820020` (v4), configure-pages `983d7736d9b0ae728b81ab479565c72886d7745b` (v5), upload-pages-artifact `56afc609e74202658d3ffba0e8f6dda462b719fa` (v3), and deploy-pages `d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e` (v4). `README.md` documents the review-and-update process.
- `filters/historical-code.lua` wraps fenced code blocks on `execute.enabled: false` pages in sitewide native `<details>/<summary>` disclosures. `_quarto.yml` retains `code-fold: true` for future executable cells; formula image/text and source code rendering remain intact.

### Review verification

- A red-first targeted test run confirmed the three new browser contracts and rendered code/video contract failed against the old implementation. After fixes, `python3 -m unittest discover -s tests -v` passed 25/25; `python3 scripts/validate_rendered_site.py --site _site --routes tests/legacy-routes.json` passed; and `npm test` passed 22/22 Playwright/Axe, responsive, video, and disclosure tests.
- Clean-equivalent render: the previous `_site` was moved to the recoverable `/private/tmp/spazznolo-quarto-site-review-round1-final.zFhrqe/_site`, then `/tmp/quarto-1.10.18-expanded/quarto-core.pkg/Payload/bin/quarto render` completed all 37 inputs. Generated Python caches were moved to `/tmp/spazznolo-quarto-pycache-review-round1-final.ErcTu2` rather than deleted.
- `ruby -e 'require "yaml"; YAML.load_file(".github/workflows/site.yml")'` passed. The immutable-reference check passed for all 6 `uses:` lines; permission/isolation checks passed. `actionlint` is not installed locally, so YAML parsing plus contract checks are the available local workflow evidence.
- Prohibited source-pattern scan for Jekyll/Universal Analytics markers passed with no matches. The source analytics scan, excluding documentation and generated output, found only the retained GA4 declaration in `_quarto.yml`.
- Rendered contract checks passed for 7 pages containing historical disclosures, native `code-fold: true`, formula/text output, the video fallback/source/explanation, and the listing. `git diff --check` passed before staging.
- Isolated loopback Playwright probes at 320px, 768px, and 1440px reported no horizontal overflow in both dark and light modes. Dark backgrounds were `rgb(11, 10, 8)` and light backgrounds `rgb(247, 242, 232)`; temporary screenshots were written under `/private/tmp/task12-home-{dark,light}-{320,768,1440}.png` for local inspection only. The 320px screenshot shows the stacked listing labels and full-width values.

### Scope confirmation

No GitHub Pages configuration, push, external publication/deployment, live-site review, or release tag was performed. Steps 8–10 were not executed. `.superpowers/`, generated `_site`, temporary screenshots, and generated caches remain untracked or ignored and are not part of the commit.
