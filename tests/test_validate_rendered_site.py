from contextlib import redirect_stdout
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts.validate_rendered_site import (
    main,
    route_to_output,
    validate_asset_sizes,
    validate_document_contract,
    validate_internal_links,
    validate_routes,
)


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

    def test_relative_link_outside_site_is_reported(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            site = root / "site"
            site.mkdir()
            (root / "outside.html").write_text("outside", encoding="utf-8")
            (site / "index.html").write_text('<a href="../outside.html">outside</a>', encoding="utf-8")
            errors = validate_internal_links(site)
        self.assertEqual(errors, ["index.html: broken internal link ../outside.html"])

    def test_missing_local_stylesheet_is_reported(self):
        with TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "index.html").write_text(
                '<link rel="stylesheet" href="/missing.css">', encoding="utf-8"
            )
            errors = validate_internal_links(site)
        self.assertEqual(errors, ["index.html: broken internal link /missing.css"])

    def test_query_and_fragment_references_to_existing_outputs_are_valid(self):
        with TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "about").mkdir()
            (site / "about" / "index.html").write_text("about", encoding="utf-8")
            (site / "styles").mkdir()
            (site / "styles" / "site.css").write_text("body {}", encoding="utf-8")
            (site / "index.html").write_text(
                '<a href="/about/?from=home#intro">about</a>'
                '<a href="#top">top</a>'
                '<link rel="stylesheet" href="/styles/site.css?v=1#theme">',
                encoding="utf-8",
            )
            errors = validate_internal_links(site)
        self.assertEqual(errors, [])

    def test_document_contract_rejects_blank_title_and_missing_description_alt(self):
        with TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "index.html").write_text(
                '<title>  </title><img src="figure.png" alt="  ">', encoding="utf-8"
            )
            errors = validate_document_contract(site)
        self.assertEqual(
            errors,
            [
                "index.html: missing title",
                "index.html: missing meta description",
                "index.html: image missing alt text: figure.png",
            ],
        )

    def test_document_contract_accepts_valid_metadata_and_alt_text(self):
        with TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "index.html").write_text(
                '<title>Home</title>'
                '<meta name="description" content="A useful description.">'
                '<img src="figure.png" alt="A plotted result">',
                encoding="utf-8",
            )
            errors = validate_document_contract(site)
        self.assertEqual(errors, [])

    def test_oversized_asset_is_reported(self):
        with TemporaryDirectory() as directory:
            site = Path(directory)
            asset = site / "figure.png"
            asset.write_bytes(b"0123456789")
            errors = validate_asset_sizes(site, limit_bytes=9)
        self.assertEqual(errors, ["oversized asset: figure.png (10 bytes)"])

    def test_cli_rejects_unknown_series(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            site = root / "site"
            site.mkdir()
            (site / "index.html").write_text("", encoding="utf-8")
            routes = root / "routes.json"
            routes.write_text(
                json.dumps(
                    {
                        "pages": [{"route": "/", "source": "index.qmd", "series": "page"}],
                        "posts": [],
                    }
                ),
                encoding="utf-8",
            )
            output = io.StringIO()
            with patch(
                "sys.argv",
                [
                    "validate_rendered_site.py",
                    "--site",
                    str(site),
                    "--routes",
                    str(routes),
                    "--series",
                    "does-not-exist",
                ],
            ), redirect_stdout(output):
                result = main()
        self.assertEqual(result, 1)
        self.assertEqual(output.getvalue().strip(), "unknown series: does-not-exist")

    def test_cli_series_filter_validates_matching_routes_only(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            site = root / "site"
            site.mkdir()
            (site / "index.html").write_text("", encoding="utf-8")
            routes = root / "routes.json"
            routes.write_text(
                json.dumps(
                    {
                        "pages": [{"route": "/", "source": "index.qmd", "series": "page"}],
                        "posts": [],
                    }
                ),
                encoding="utf-8",
            )
            with patch(
                "sys.argv",
                [
                    "validate_rendered_site.py",
                    "--site",
                    str(site),
                    "--routes",
                    str(routes),
                    "--series",
                    "page",
                ],
            ):
                result = main()
        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()
