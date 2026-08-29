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

    def test_goalie_performance_retains_source_facts_and_matching_figures(self):
        text = (ROOT / "research/goalie-performance/index.qmd").read_text(encoding="utf-8")
        for fact in [
            "SV%: 0.948638",
            "SQ AdjSV%: 0.947320",
            "Age SQ AdjSV%: 0.948619",
            "posterior SQ AdjSV%: 0.947082",
            "posterior Age SQ AdjSV%: 0.948338",
            "mean shots against changed from 4,198 to 4,286",
            "mean adjusted save percentage changed from .932 to .933",
        ]:
            self.assertIn(fact, text)
        self.assertNotIn(
            "![Braden Holtby's posterior adjusted save percentage over shots faced.]"
            "(/figs/goalie-six-three.png)",
            text,
        )
        self.assertIn(
            "![Average posterior adjusted save percentage paths by career-size group.]"
            "(/figs/goalie-six-seven.png)",
            text,
        )
        self.assertIn(
            "![Average goalie age through shots faced by career-size group.]"
            "(/figs/goalie-six-six.png)",
            text,
        )
        self.assertIn(
            "weighting observed careers by shots emphasizes the high-opportunity careers and can introduce performance-selection bias",
            text,
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
