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

    def test_discovery_outputs_exist(self):
        required = [
            SITE / "index.xml",
            SITE / "sitemap.xml",
            SITE / "404.html",
            SITE / "research" / "index.html",
            SITE / "subjects" / "index.html",
            SITE / "archive" / "index.html",
        ]
        missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
        self.assertEqual(missing, [])

    def test_homepage_open_graph_title_is_meaningful(self):
        html = (SITE / "index.html").read_text(encoding="utf-8")
        self.assertIn('property="og:title" content="Home – jeremie.spagnolo"', html)

    def test_historical_code_and_video_fallback_contracts(self):
        canonical = (SITE / "research" / "nhl-pick-probability" / "index.html").read_text(
            encoding="utf-8"
        )
        self.assertIn('class="historical-code-disclosure"', canonical)
        self.assertIn("<summary>Show historical code", canonical)
        video_page = (SITE / "2022" / "09" / "16" / "tennis-liveblog.html").read_text(
            encoding="utf-8"
        )
        self.assertIn("Your browser does not support this video", video_page)
        self.assertIn('href="../../../figs/player-detect-demo.mp4"', video_page)


if __name__ == "__main__":
    unittest.main()
