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
