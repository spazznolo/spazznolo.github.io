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
