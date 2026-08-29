from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.validate_rendered_site import route_to_output, validate_internal_links, validate_routes


class RouteValidationTest(unittest.TestCase):
    def test_route_to_output_handles_pages_and_html_posts(self):
        self.assertEqual(route_to_output("/"), Path("index.html"))
        self.assertEqual(route_to_output("/about/"), Path("about/index.html"))
        self.assertEqual(
            route_to_output("/2023/05/17/goalie-performance-1.html"),
            Path("2023/05/17/goalie-performance-1.html"),
        )

    def test_missing_route_is_reported(self):
        with TemporaryDirectory() as directory:
            errors = validate_routes(Path(directory), ["/missing/"])
        self.assertEqual(errors, ["missing route: /missing/ -> missing/index.html"])

    def test_broken_relative_link_is_reported(self):
        with TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "index.html").write_text('<a href="/missing/">missing</a>', encoding="utf-8")
            errors = validate_internal_links(site)
        self.assertEqual(errors, ["index.html: broken internal link /missing/"])


if __name__ == "__main__":
    unittest.main()
