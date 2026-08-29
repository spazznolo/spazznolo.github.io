# Quarto Blog Rebuild Design

**Date:** 2026-08-28

**Status:** Approved design

## 1. Purpose

Rebuild `spazznolo.github.io` as a modern Quarto publication while preserving the character of the existing blog. The new site should be a personal home and a serious body of public sports-statistics work. It should welcome technically curious sports readers while giving applied statisticians enough methodological structure to take the work seriously.

The relaunch updates the publishing technology, information architecture, personal information, visual design, and editorial organization. It is not a replication project for the historical analyses.

## 2. Goals

- Replace the outdated Jekyll stack with one maintainable Quarto site.
- Preserve every current public post and legacy URL.
- Keep the blog personal, informal, curious, and warm rather than presenting it as an employer-facing portfolio.
- Make statistical subjects the primary intellectual taxonomy and sports the contextual taxonomy.
- Consolidate the Goalie Performance series into one canonical article.
- Consolidate the NHL Pick Probability series into one canonical article.
- Improve reading comfort, navigation, accessibility, metadata, and mobile behavior.
- Give new posts a clean path to executable code, embedded output, interactive plots, and video.
- Publish reliably to GitHub Pages through automated checks.

## 3. Non-goals

- Reconstructing datasets or rerunning the analyses in existing posts.
- Retrofitting reproducibility into historical work.
- Rewriting the blog into academic prose or a conventional professional portfolio.
- Optimizing the site specifically for recruiters or employers.
- Adding comments, a newsletter, a search service, accounts, or a content-management system.
- Expanding the public subject matter beyond sports before public non-sports work exists.
- Completing the paused tennis-tracking project as part of the rebuild.

## 4. Audience and editorial identity

The primary audience is a technically curious sports reader. The secondary audience is applied statisticians who want to inspect assumptions, models, uncertainty, and limitations. Articles should introduce the sports question first, preserve the author's back-of-the-napkin voice, and offer methodological depth through good structure rather than formal posturing.

The site is sports-focused because that is the author's current body of public work. Its architecture must allow non-sports statistical work to be added later without a redesign.

The public professional description is **“Data science contractor for the Chicago Blackhawks.”** The About page also retains Statistics Canada as an important part of the career narrative. The tennis-tracking project is described as **“paused with intent to return.”** GitHub is the only social/profile link exposed by the blog; the blog does not link to LinkedIn.

## 5. Architecture and publishing

The site will be a single Quarto website. Pages and articles are authored as `.qmd` files and rendered to a static site. GitHub Actions builds the site and deploys the generated artifact to GitHub Pages. Generated site output does not need to be maintained manually on the source branch.

The site has one shared visual theme and common article behavior for metadata, reading time, citations, code visibility, figure captions, and series or archive notices. Quarto's frozen computations are available for new computational work so ordinary site builds can reuse intentional outputs instead of rerunning expensive analysis.

New posts may contain:

- build-time R, Python, or Julia output;
- interactive HTML widgets such as Plotly where interaction clarifies the result;
- Observable JS for useful browser-side exploration;
- Shinylive only for rare self-contained demonstrations that benefit from browser execution;
- embedded MP4/WebM, YouTube, or Vimeo video.

Interactive elements must be selective. A static figure is preferred when interaction adds no analytical value.

## 6. Information architecture

The top navigation contains:

1. `jeremie.spagnolo`
2. Research
3. Subjects
4. About
5. GitHub

The author's name appears once, quietly, at the top. There is no oversized name or repeated personal title.

### Homepage

The homepage is one continuous reading column, with no split hero and no two-up content grid. Its order is:

1. the existing warm, grainy `fifty-four.png` image;
2. an About label and the author's original introduction;
3. two featured research articles;
4. the statistical-subject index;
5. recent writing.

The introduction is preserved verbatim:

> This blog serves as an outlet to explore ideas which naturally interest me. I try to keep an informal, back-of-the-napkin style to these posts, hopefully a little like Tom Tango. Posts are grouped by topic in the header, but can be accessed in chronological order below.

The Tom Tango text remains a link. The introduction is not rewritten during the rebuild.

### Research

Research is the complete chronological index. Current and renovated work appears first. Untouched historical work remains visible under an explicit Archive heading rather than being hidden or deleted.

### Subjects

The initial statistical subjects are:

- Bayesian statistics;
- probability and simulation;
- distributions and sampling;
- regression and calibration.

These reflect methods actually present in the existing writing. Sports terms such as hockey, goalies, NHL draft, overtime, and tennis are tags or contexts rather than the primary subject navigation. The subject list can grow when new public work introduces a genuinely new statistical area.

### About

The About page expands on the brief homepage introduction. It includes the personal transition back toward mathematics and research, Statistics Canada, the current Chicago Blackhawks contract description, the paused tennis-tracking project, and a GitHub link. It should remain narrative and human rather than resembling a résumé.

### Articles and series

Articles use a single readable column. Related archived installments can expose previous/next links, but the two consolidated subjects each have one canonical article rather than a multipart replacement series.

## 7. Visual system

The approved direction retains the strongest qualities of the old site without reproducing all of its terminal decoration.

- Source Code Pro is the site typeface, including paragraph text.
- The default appearance is dark.
- The background is a warm near-black rather than a cool blue-black.
- Primary copy, including the homepage About paragraph, is white or warm white.
- Warm yellow replaces mint green as the accent color.
- Body copy starts near the old site's 13px scale, with comfortable line height and a constrained reading width.
- Reading-time metadata is included.
- Dividers and labels may echo the old console theme, but command prompts, fake terminal output, and excessive monospace flourishes are excluded.
- The `fifty-four.png` image remains a prominent source of character and warmth.
- The layout avoids sidebars, card-heavy magazine patterns, split heroes, and oversized branding.
- The site supports mobile layouts down to 320px without shrinking essential text below an accessible size.
- A light appearance is available as a secondary user choice, but the dark design is the primary and default presentation.

## 8. Content migration and preservation

All 24 existing posts are mechanically migrated into Quarto-compatible source while preserving their wording, figures, publication dates, and an intentional route for every current public URL. Initial migration fixes only issues required for valid rendering and navigation, such as malformed HTML, broken internal paths, missing asset references, and basic metadata.

Historical posts remain reachable even when superseded. They receive archive treatment and, where relevant, a short notice directing readers to a newer canonical article. They are not silently deleted or replaced.

Substantive editorial revisions show both the original publication date and the revision date. Major reinterpretation or consolidation receives a brief editor's note so the site's history remains legible.

## 9. Canonical legacy articles

### Goalie Performance

The five existing Goalie Performance installments are consolidated editorially into one canonical article named **Goalie Performance**. The target is approximately 3,000–3,500 edited words after repetition is removed. The article covers the model and assumptions, contextual and age adjustments, distributional exploration, sample-size implications, uncertainty, and limitations in one coherent narrative.

### NHL Pick Probability

The six existing draft-probability installments are consolidated editorially into one canonical article named **NHL Pick Probability**. The target is approximately 4,000–4,500 edited words after repetition is removed. The article covers deriving pick distributions, applying them to draft decisions, retrospective evaluation, model confidence, and limitations.

Both canonical articles use compact tables of contents and strong section headings. Existing derivations, diagnostics, and supplementary figures may be placed in expandable appendices within the same page rather than split into separate posts.

The consolidation uses the existing prose, results, and figures. It may correct presentation problems, arithmetic, notation, broken code excerpts, and unsupported wording, but it does not reconstruct the underlying data or rerun the models. Each canonical article states that it consolidates earlier work and retains the original analysis.

The original installments remain in the archive at their legacy URLs with notices pointing to the canonical version.

## 10. Later editorial work

The following work does not block the relaunch:

- consolidate the four Goalie Consistency installments into one article, or two only if the NHL application genuinely needs separate treatment;
- consolidate the four Post-Regulation installments into a focused analysis of competitive impact, randomness, and format design;
- create a Tennis Tracking project overview and retain the strongest technical articles beneath it;
- leave the tennis liveblog and incomplete fragments in the archive unless later replaced by a retrospective.

## 11. Reproducibility boundary

Historical work, including the two canonical consolidations, is not rebuilt as executable analysis. The relaunch must not imply that old models were independently reproduced when they were not.

Reproducible Quarto execution is the default for new computational posts. For those posts:

- dependencies are pinned for the languages used;
- computations can be rerun intentionally;
- expensive outputs may be frozen;
- public data and code are linked or included where licensing and practicality allow;
- unavailable or private inputs are disclosed plainly;
- interactive or video output has a useful static or textual fallback.

## 12. URLs, metadata, and discovery

Every current production URL is captured in a legacy-route manifest. Each route must continue to return the corresponding archived article or an intentional redirect. The original installment URLs for the two canonical subjects remain archive pages rather than disappearing.

New standalone writing uses clean `/posts/<slug>/` paths. The two canonical articles use stable research paths based on their plain subject names. Redirect pages are generated only when an old path cannot be rendered directly.

The rebuilt site provides valid titles, descriptions, canonical metadata, Open Graph metadata, an RSS feed, a sitemap, `robots.txt`, and a useful custom 404 page. Missing or generic identifiers such as `b2a3e8.github.io` are removed from public metadata.

The existing GA4 property (`G-DGRHZS5DNM`) is retained as the only analytics integration. The obsolete Universal Analytics property and duplicated page-level analytics snippets are removed. No new tracking service is added.

## 13. Build behavior and failure handling

The automated build fails when:

- Quarto cannot render a page;
- a required local image, video, stylesheet, or script is missing;
- an internal link is broken;
- a required legacy route disappears;
- required article metadata is absent or invalid;
- generated HTML contains a material structural error.

External-link checks produce a report for review but do not block publication, because third-party failures can be temporary.

New executable posts fail clearly when their code fails. Previously frozen outputs remain usable for normal builds, while an intentional refresh is a separate verification action. Interactive content must degrade to an explanatory fallback if browser execution is unavailable.

## 14. Verification

Before launch, verification covers:

- a clean Quarto production render;
- all legacy routes and intentional redirects;
- internal links and local assets;
- required metadata, feed, sitemap, robots file, and 404 page;
- semantic heading order, image alt text, captions, keyboard navigation, and color contrast;
- desktop and mobile widths, including at least 320px, a tablet width, and a wide desktop width;
- the primary dark presentation and secondary light presentation;
- representative code blocks, tables, figures, citations, embedded video, and an interactive-output fallback;
- performance checks sufficient to catch oversized media, layout shift, and unnecessary script weight.

The rendered site receives a visual review before deployment. A known-good prior Git revision remains deployable as the rollback path.

## 15. Implementation sequence

1. Establish the Quarto project, theme, shared metadata, and deployment workflow.
2. Build the approved homepage, Research, Subjects, About, archive, article template, and error/discovery pages.
3. Create the legacy-route manifest and mechanically migrate all existing pages and posts.
4. Add archive and supersession notices without deleting original installments.
5. Assemble the two canonical legacy articles from the existing material.
6. Add automated rendering, URL, link, asset, metadata, HTML, accessibility, and responsive checks.
7. Review the complete rendered site and deploy it to GitHub Pages.

The detailed implementation plan will break these stages into small, verifiable tasks after this specification is approved.

## 16. Launch criteria

The relaunch is complete when:

- the approved single-column, Source Code Pro, warm-yellow dark design is live;
- the homepage uses the original introduction and `fifty-four.png` image;
- the About information is current and accurate;
- all 24 historical posts remain reachable;
- every known old public URL resolves intentionally;
- Research, Subjects, About, GitHub, archive, feed, sitemap, robots file, and 404 behavior work;
- the Goalie Performance and NHL Pick Probability canonical articles are published without claims of reconstructed reproducibility;
- obsolete analytics and Jekyll-specific publishing code are gone;
- automated checks pass;
- a new-post template supports reproducible Quarto work, interactive output, and video without requiring those features in every article.
