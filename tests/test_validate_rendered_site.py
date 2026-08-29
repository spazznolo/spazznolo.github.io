from contextlib import redirect_stdout
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts.validate_rendered_site import (
    main,
    listing_input_paths,
    route_to_output,
    validate_asset_sizes,
    validate_document_contract,
    validate_internal_links,
    validate_listing_inputs,
    validate_routes,
    validate_source_front_matter,
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
                '<title>  </title>'
                '<meta name="description" content="A description">'
                '<link rel="canonical" href="https://spazznolo.github.io/">'
                '<img src="figure.png" alt="  ">', encoding="utf-8"
            )
            errors = validate_document_contract(site)
        self.assertEqual(
            errors,
            [
                "index.html: missing title",
                "index.html: image missing alt text: figure.png",
            ],
        )

    def test_document_contract_accepts_valid_metadata_and_alt_text(self):
        with TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "index.html").write_text(
                '<title>Home</title>'
                '<meta name="description" content="A useful description.">'
                '<link rel="canonical" href="https://spazznolo.github.io/">'
                '<img src="figure.png" alt="A plotted result">',
                encoding="utf-8",
            )
            errors = validate_document_contract(site)
        self.assertEqual(errors, [])

    def test_document_contract_rejects_missing_canonical_url(self):
        with TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "index.html").write_text(
                '<title>Home</title>'
                '<meta name="description" content="A useful description.">',
                encoding="utf-8",
            )
            errors = validate_document_contract(site)
        self.assertEqual(errors, ["index.html: expected exactly one canonical URL, found 0"])

    def test_document_contract_rejects_duplicate_or_mismatched_canonical_url(self):
        with TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "about").mkdir()
            (site / "about" / "index.html").write_text(
                '<title>About</title>'
                '<meta name="description" content="About this site.">'
                '<link rel="canonical" href="https://spazznolo.github.io/about/">'
                '<link rel="canonical" href="https://example.com/about/">',
                encoding="utf-8",
            )
            errors = validate_document_contract(site)
        self.assertEqual(
            errors,
            ["about/index.html: expected exactly one canonical URL, found 2"],
        )

    def test_document_contract_rejects_canonical_url_that_does_not_match_route(self):
        with TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "about").mkdir()
            (site / "about" / "index.html").write_text(
                '<title>About</title>'
                '<meta name="description" content="About this site.">'
                '<link rel="canonical" href="https://example.com/about/">',
                encoding="utf-8",
            )
            errors = validate_document_contract(site)
        self.assertEqual(
            errors,
            [
                "about/index.html: canonical URL must be absolute and use "
                "https://spazznolo.github.io/about/"
            ],
        )

    def test_listing_input_discovery_is_complete(self):
        root = Path(__file__).resolve().parents[1]
        paths = listing_input_paths(root)
        self.assertEqual(len(paths), 26)
        self.assertEqual(
            {path.relative_to(root).as_posix() for path in paths[:2]},
            {
                "research/goalie-performance/index.qmd",
                "research/nhl-pick-probability/index.qmd",
            },
        )
        relative_paths = [path.relative_to(root) for path in paths]
        self.assertEqual(sum(path.parts[0].startswith("20") for path in relative_paths), 24)
        self.assertEqual(validate_listing_inputs(root), [])

    def test_listing_input_discovery_includes_current_posts_and_excludes_templates(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            post = root / "posts" / "current-note" / "index.qmd"
            post.parent.mkdir(parents=True)
            post.write_text(
                "---\n"
                'title: "Current note"\n'
                "date: 2026-08-28\n"
                'description: "A current note."\n'
                "status: current\n"
                "---\n",
                encoding="utf-8",
            )
            template = root / "templates" / "post.qmd"
            template.parent.mkdir()
            template.write_text("---\nstatus: current\n---\n", encoding="utf-8")
            paths = listing_input_paths(root)
            self.assertIn(post, paths)
            self.assertNotIn(template, paths)
            self.assertEqual(validate_source_front_matter([post], root=root), [])

    def test_source_front_matter_rejects_missing_or_blank_required_fields(self):
        required = ("title", "date", "description", "status")
        with TemporaryDirectory() as directory:
            source = Path(directory) / "source.qmd"
            for field in required:
                with self.subTest(field=field, mode="missing"):
                    lines = [
                        "---",
                        'title: "Valid title"',
                        "date: 2024-01-01",
                        'description: "Valid description."',
                        "status: archived",
                        "---",
                        "",
                    ]
                    lines = [line for line in lines if not line.startswith(f"{field}:")]
                    source.write_text("\n".join(lines), encoding="utf-8")
                    errors = validate_source_front_matter([source])
                    self.assertEqual(errors, [f"source.qmd: missing required field '{field}'"])

                with self.subTest(field=field, mode="blank"):
                    lines = [
                        "---",
                        'title: "Valid title"',
                        "date: 2024-01-01",
                        'description: "Valid description."',
                        "status: archived",
                        "---",
                        "",
                    ]
                    lines = [
                        f"{field}: \"\"" if line.startswith(f"{field}:") else line
                        for line in lines
                    ]
                    source.write_text("\n".join(lines), encoding="utf-8")
                    errors = validate_source_front_matter([source])
                    self.assertEqual(errors, [f"source.qmd: missing required field '{field}'"])

    def test_source_front_matter_rejects_invalid_dates_and_statuses(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "nested" / "source.qmd"
            source.parent.mkdir()
            source.write_text(
                "---\n"
                'title: "Valid title"\n'
                "date: 2024-02-30\n"
                'description: "Valid description."\n'
                "status: draft\n"
                "---\n",
                encoding="utf-8",
            )
            errors = validate_source_front_matter([source], root=Path(directory))
        self.assertEqual(
            errors,
            [
                "nested/source.qmd: invalid ISO date '2024-02-30'",
                "nested/source.qmd: status must be one of canonical, archived, current (got 'draft')",
            ],
        )

    def test_source_front_matter_diagnostics_are_repository_relative(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "research" / "nested" / "source.qmd"
            source.parent.mkdir(parents=True)
            source.write_text(
                "---\n"
                'title: "Valid title"\n'
                "date: 2024-01-01\n"
                'description: "Valid description."\n'
                "status: canonical\n"
                "---\n",
                encoding="utf-8",
            )
            source.write_text(source.read_text(encoding="utf-8").replace("title: \"Valid title\"", "title: \"\""), encoding="utf-8")
            errors = validate_source_front_matter([source], root=root)
        self.assertEqual(errors, ["research/nested/source.qmd: missing required field 'title'"])
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
