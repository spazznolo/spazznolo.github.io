from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


def source_contract(
    relative_path,
    headings,
    minimum_words,
    maximum_words,
    requires_consolidation_note=True,
):
    text = (ROOT / relative_path).read_text(encoding="utf-8")
    for heading in headings:
        if f"## {heading}" not in text:
            raise AssertionError(f"{relative_path}: missing heading {heading}")
    words = re.findall(r"\b[\w’'-]+\b", text)
    if not minimum_words <= len(words) <= maximum_words:
        raise AssertionError(f"{relative_path}: {len(words)} words outside {minimum_words}-{maximum_words}")
    if requires_consolidation_note and text.count("This article consolidates") != 1:
        raise AssertionError(f"{relative_path}: consolidation note must be one sentence")
    for multipart_marker in [
        'class="part-date"',
        "{.part-break}",
        "Originally published",
    ]:
        if multipart_marker in text:
            raise AssertionError(f"{relative_path}: contains multipart marker: {multipart_marker}")
    for editorial_phrase in [
        "retains the original analysis",
        "underlying data and models were not reconstructed",
        "This is an editorial consolidation",
        "not a fresh analysis",
    ]:
        if editorial_phrase in text:
            raise AssertionError(f"{relative_path}: contains added editorial prose: {editorial_phrase}")


class CanonicalArticleTest(unittest.TestCase):
    def test_goalie_performance_contract(self):
        source_contract(
            "research/goalie-performance/index.qmd",
            [
                "EMPIRICAL BAYES",
                "ACCOUNTING FOR SHOT QUALITY",
                "ADJUSTING FOR AGE",
                "CAREER LENGTH AND THE PRIOR",
                "CONTEXTUALIZING EXPERIENCE",
            ],
            3000,
            4000,
        )

    def test_goalie_performance_retains_source_facts_and_matching_figures(self):
        text = (ROOT / "research/goalie-performance/index.qmd").read_text(encoding="utf-8")
        for fact in [
            "The figures were rebuilt in Python",
            "66.2% probability",
            "980 prior non-goal attempts",
            "$r=.921$",
            "$r=.899$",
            "$r=.814$",
            "All 314 goalies",
            "The fit is... not really good",
        ]:
            self.assertIn(fact, text)
        self.assertNotIn(
            'fig-alt="Braden Holtby\'s posterior adjusted save percentage over shots faced."',
            text,
        )
        self.assertIn(
            "(/figs/goalie-six-seven.png)",
            text,
        )
        self.assertIn(
            "(/figs/goalie-six-six.png)",
            text,
        )
        self.assertIn("fig-align: center", text)
        self.assertNotIn("Code available here", text)
        self.assertEqual(text.count("::: {.equation-note}"), 5)

    def test_nhl_pick_probability_contract(self):
        source_contract(
            "research/nhl-pick-probability/index.qmd",
            [
                "Purpose",
                "System",
                "Contents",
                "Data",
                "Parameters",
                "Model",
                "Estimation",
                "Applications",
                "Validation",
            ],
            1200,
            2600,
            requires_consolidation_note=False,
        )

    def test_nhl_pick_probability_uses_rank_ordered_model_only(self):
        text = (ROOT / "research/nhl-pick-probability/index.qmd").read_text(encoding="utf-8")
        self.assertIn("A Plackett–Luce model", text)
        self.assertIn("One hundred thousand drafts", text)
        self.assertIn("pick four is worth more than pick five in 67.3%", text)
        self.assertIn("model-field-sheet", text)
        self.assertIn('href="#applications">Applications</a>', text)
        self.assertNotIn("Mikko Rantanen", text)
        self.assertNotIn("Show historical code", text)
        self.assertEqual(text.count("equation-note"), 5)


if __name__ == "__main__":
    unittest.main()
