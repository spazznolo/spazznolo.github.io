# Sports research digest

The published [digest page](index.qmd) lists curated issues. It is intentionally unlisted from the blog homepage and includes `noindex` metadata; anyone with the direct URL can still read it. RSS/Atom is used only to discover candidates; readers open the digest page and then the original articles. The site does not republish article text or bypass subscriptions.

Run `python3 scripts/collect_digest.py --days 14 --output /tmp/digest-candidates.md` to refresh the candidate list. The script reads `sources.json`, deduplicates URLs, keeps publication dates, and reports feed failures. This is a local editorial aid; it never publishes or emails anything.

To make an issue, read the candidate originals, look for relevant new papers and articles outside the feeds, and add `issues/YYYY-MM-DD/index.qmd`. Copy the issue front matter, including its `noindex` header. Aim for six to ten selections and a roughly even hockey/other split. Each note should state why the piece is worth reading, label paid access or a preprint when relevant, and mention a material limitation. Verify claims against the original rather than relying on feed summaries. Run `quarto render` before publication.

The current source list deliberately excludes Dom Luszczyszyn: a dependable public feed for his byline has not been verified. Check his published work manually when curating an issue.
