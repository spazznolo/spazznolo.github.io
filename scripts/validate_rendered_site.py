#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import date
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


CANONICAL_BASE_URL = "https://spazznolo.github.io"
LISTING_REQUIRED_FIELDS = ("title", "date", "description", "status")
LISTING_ALLOWED_STATUSES = ("canonical", "archived", "current")
CANONICAL_LISTING_INPUTS = (
    "research/goalie-performance/index.qmd",
    "research/nhl-pick-probability/index.qmd",
)


class ReferenceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.images = []
        self.title = False
        self.title_text = ""
        self._in_title = False
        self.description = False
        self.canonical_urls = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a" and values.get("href"):
            self.references.append(values["href"])
        if tag == "link" and values.get("href"):
            self.references.append(values["href"])
            rel = {part.lower() for part in values.get("rel", "").split()}
            if "canonical" in rel:
                self.canonical_urls.append(values["href"])
        if tag in {"img", "script", "video", "source"} and values.get("src"):
            self.references.append(values["src"])
        if tag == "img":
            self.images.append(values)
        if tag == "title":
            self.title = True
            self._in_title = True
        if tag == "meta" and values.get("name") == "description" and values.get("content", "").strip():
            self.description = True

    def handle_data(self, data):
        if self._in_title:
            self.title_text += data

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False


def route_to_output(route: str) -> Path:
    path = unquote(urlsplit(route).path).lstrip("/")
    if not path:
        return Path("index.html")
    if path.endswith("/"):
        return Path(path) / "index.html"
    return Path(path)


def validate_routes(site: Path, routes: list[str]) -> list[str]:
    errors = []
    for route in routes:
        output = route_to_output(route)
        if not (site / output).is_file():
            errors.append(f"missing route: {route} -> {output.as_posix()}")
    return errors


def _resolve_reference(site: Path, html_file: Path, reference: str) -> Path | None:
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc or reference.startswith(("mailto:", "tel:", "#", "data:")):
        return None
    route = unquote(parsed.path)
    if not route:
        return None
    if route.startswith("/"):
        candidate = site.resolve() / route_to_output(route)
    else:
        candidate = html_file.resolve().parent / route
        if route.endswith("/"):
            candidate = candidate / "index.html"
    if candidate.is_dir():
        candidate = candidate / "index.html"
    return candidate.resolve()


def validate_internal_links(site: Path) -> list[str]:
    errors = []
    site_root = site.resolve()
    for html_file in sorted(site.rglob("*.html")):
        parser = ReferenceParser()
        parser.feed(html_file.read_text(encoding="utf-8"))
        for reference in parser.references:
            target = _resolve_reference(site, html_file, reference)
            if target is not None:
                try:
                    target.relative_to(site_root)
                    contained = True
                except ValueError:
                    contained = False
                if contained and target.exists():
                    continue
                rel = html_file.relative_to(site).as_posix()
                errors.append(f"{rel}: broken internal link {reference}")
    return sorted(set(errors))


def validate_document_contract(site: Path) -> list[str]:
    errors = []
    for html_file in sorted(site.rglob("*.html")):
        parser = ReferenceParser()
        parser.feed(html_file.read_text(encoding="utf-8"))
        rel = html_file.relative_to(site).as_posix()
        if not parser.title_text.strip():
            errors.append(f"{rel}: missing title")
        if not parser.description:
            errors.append(f"{rel}: missing meta description")
        expected_canonical = canonical_url_for_output(rel)
        if len(parser.canonical_urls) != 1:
            errors.append(
                f"{rel}: expected exactly one canonical URL, found "
                f"{len(parser.canonical_urls)}"
            )
        elif parser.canonical_urls[0] != expected_canonical:
            errors.append(
                f"{rel}: canonical URL must be absolute and use "
                f"{expected_canonical}"
            )
        for image in parser.images:
            alt = image.get("alt")
            if alt is None or (alt and not alt.strip()):
                errors.append(f"{rel}: image missing alt text: {image.get('src', '')}")
    return errors


def canonical_url_for_output(relative_output: str) -> str:
    """Return Quarto's canonical URL for a rendered HTML output path."""
    relative = Path(relative_output).as_posix()
    if relative == "index.html":
        route = "/"
    elif relative.endswith("/index.html"):
        route = f"/{relative[:-len('index.html')]}"
    else:
        route = f"/{relative}"
    return f"{CANONICAL_BASE_URL}{route}"


def listing_input_paths(root: Path) -> list[Path]:
    """Discover the canonical and historical source files consumed by listings."""
    canonical = [root / relative for relative in CANONICAL_LISTING_INPUTS]
    historical = sorted(root.glob("20*/**/*.qmd"))
    current_posts = sorted(root.glob("posts/**/index.qmd"))
    return canonical + historical + current_posts


def _source_front_matter(source: Path) -> dict[str, str]:
    lines = source.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}
    metadata = {}
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):(\s*(.*))?$", line)
        if match:
            value = (match.group(3) or "").strip()
            metadata[match.group(1)] = value.strip("\"'").strip()
    return metadata


def _relative_source_path(source: Path, root: Path | None) -> str:
    if root is not None:
        try:
            return source.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            pass
    return source.name


def validate_source_front_matter(sources: list[Path], root: Path | None = None) -> list[str]:
    errors = []
    for source in sources:
        rel = _relative_source_path(source, root)
        try:
            metadata = _source_front_matter(source)
        except OSError as error:
            errors.append(f"{rel}: unable to read source ({error})")
            continue
        for field in LISTING_REQUIRED_FIELDS:
            if not metadata.get(field, "").strip():
                errors.append(f"{rel}: missing required field '{field}'")
        raw_date = metadata.get("date", "").strip()
        if raw_date and (not re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw_date) or _invalid_iso_date(raw_date)):
            errors.append(f"{rel}: invalid ISO date '{raw_date}'")
        status = metadata.get("status", "").strip()
        if status and status not in LISTING_ALLOWED_STATUSES:
            allowed = ", ".join(LISTING_ALLOWED_STATUSES)
            errors.append(f"{rel}: status must be one of {allowed} (got '{status}')")
    return errors


def _invalid_iso_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
    except ValueError:
        return True
    return False


def validate_listing_inputs(root: Path) -> list[str]:
    errors = []
    sources = listing_input_paths(root)
    expected_sources = len(CANONICAL_LISTING_INPUTS) + 24 + len(
        list(root.glob("posts/**/index.qmd"))
    )
    if len(sources) != expected_sources:
        errors.append(
            f"listing input discovery expected {expected_sources} sources, "
            f"found {len(sources)}"
        )
    missing = [source for source in sources if not source.is_file()]
    errors.extend(
        f"missing listing input: {source.relative_to(root).as_posix()}"
        for source in missing
    )
    errors.extend(
        validate_source_front_matter(
            [source for source in sources if source.is_file()], root=root
        )
    )
    return errors


def validate_asset_sizes(site: Path, limit_bytes: int = 7_000_000) -> list[str]:
    errors = []
    for path in sorted(site.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".mov", ".mp4", ".webm"}:
            if path.stat().st_size > limit_bytes:
                errors.append(f"oversized asset: {path.relative_to(site).as_posix()} ({path.stat().st_size} bytes)")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, default=Path("_site"))
    parser.add_argument("--routes", type=Path, default=Path("tests/legacy-routes.json"))
    parser.add_argument("--series")
    args = parser.parse_args()

    manifest = json.loads(args.routes.read_text(encoding="utf-8"))
    records = manifest["pages"] + manifest["posts"]
    if args.series is not None:
        known_series = {record["series"] for record in records}
        if args.series not in known_series:
            print(f"unknown series: {args.series}")
            return 1
        records = [record for record in records if record["series"] == args.series]
    routes = [record["route"] for record in records]

    errors = []
    errors.extend(validate_routes(args.site, routes))
    if args.series is None:
        errors.extend(validate_internal_links(args.site))
        errors.extend(validate_document_contract(args.site))
        errors.extend(validate_asset_sizes(args.site))
        errors.extend(validate_listing_inputs(args.routes.resolve().parent.parent))

    for error in sorted(set(errors)):
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
