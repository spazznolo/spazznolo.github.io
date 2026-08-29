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
    if text.count("This article consolidates") != 1:
        raise AssertionError(f"{relative_path}: consolidation note must be one sentence")
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
                "Goalie Performance: Empirical Bayes Save Percentage",
                "Goalie Performance: Empirical Bayes Adjusted Save Percentage",
                "Goalie Performance: Adjusting for Age",
                "Goalie Performance: Exploring the Distribution",
                "Goalie Performance: Sample Sizes",
            ],
            3400,
            4200,
        )

    def test_goalie_performance_retains_source_facts_and_matching_figures(self):
        text = (ROOT / "research/goalie-performance/index.qmd").read_text(encoding="utf-8")
        for fact in [
            "SV%: 0.948638",
            "SQ AdjSV%: 0.947320",
            "Age SQ AdjSV%: 0.948619",
            "posterior SQ AdjSV%: 0.947082",
            "posterior Age SQ AdjSV%: 0.948338",
            "mean rises, 4,198 to 4,286",
            "mean rises, .932 to .933",
            "The fit is... not really good",
            "surprise, surprise",
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

    def test_nhl_pick_probability_contract(self):
        source_contract(
            "research/nhl-pick-probability/index.qmd",
            [
                "NHL Draft: Assigning pick probabilities from user mock drafts",
                "NHL Draft: Deriving pick probabilities from draft rankings",
                "NHL Draft: An Application of Prospect Pick Probabilities [Part 1]",
                "NHL Draft: An Application of Prospect Pick Probabilities [Part 2]",
                "NHL Draft: Introducing a new NHL drafting strategy",
                "NHL Draft: Post-Draft Analysis",
            ],
            4400,
            5500,
        )

    def test_nhl_pick_probability_preserves_historical_presentation_notes(self):
        text = (ROOT / "research/nhl-pick-probability/index.qmd").read_text(encoding="utf-8")
        self.assertIn(
            "draft_simulations <- replicate(100000, sample(1:skaters, skaters, replace = FALSE, prob = mle_estimates))",
            text,
        )
        self.assertIn("probability Mikko Rantanen would be selected in the first five picks was 16.3%", text)
        self.assertIn("adjusted user data (score ~ 0.0604)", text)
        self.assertIn("Unless!", text)
        self.assertIn("the sportsbooks cooked us", text)


if __name__ == "__main__":
    unittest.main()
