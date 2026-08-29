#!/usr/bin/env python3
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit


class ReferenceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.images = []
        self.title = False
        self.description = False

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a" and values.get("href"):
            self.references.append(values["href"])
        if tag in {"img", "script", "video", "source"} and values.get("src"):
            self.references.append(values["src"])
        if tag == "img":
            self.images.append(values)
        if tag == "title":
            self.title = True
        if tag == "meta" and values.get("name") == "description" and values.get("content", "").strip():
            self.description = True


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
        candidate = site / route_to_output(route)
    else:
        candidate = html_file.parent / route
        if route.endswith("/"):
            candidate = candidate / "index.html"
    if candidate.is_dir():
        candidate = candidate / "index.html"
    return candidate.resolve()


def validate_internal_links(site: Path) -> list[str]:
    errors = []
    for html_file in sorted(site.rglob("*.html")):
        parser = ReferenceParser()
        parser.feed(html_file.read_text(encoding="utf-8"))
        for reference in parser.references:
            target = _resolve_reference(site, html_file, reference)
            if target is not None and not target.exists():
                rel = html_file.relative_to(site).as_posix()
                errors.append(f"{rel}: broken internal link {reference}")
    return sorted(set(errors))


def validate_document_contract(site: Path) -> list[str]:
    errors = []
    for html_file in sorted(site.rglob("*.html")):
        parser = ReferenceParser()
        parser.feed(html_file.read_text(encoding="utf-8"))
        rel = html_file.relative_to(site).as_posix()
        if not parser.title:
            errors.append(f"{rel}: missing title")
        if not parser.description:
            errors.append(f"{rel}: missing meta description")
        for image in parser.images:
            if not image.get("alt", "").strip():
                errors.append(f"{rel}: image missing alt text: {image.get('src', '')}")
    return errors


def validate_asset_sizes(site: Path, limit_bytes: int = 5_000_000) -> list[str]:
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
    if args.series:
        records = [record for record in records if record["series"] == args.series]
    routes = [record["route"] for record in records]

    errors = []
    errors.extend(validate_routes(args.site, routes))
    if not args.series:
        errors.extend(validate_internal_links(args.site))
        errors.extend(validate_document_contract(args.site))
        errors.extend(validate_asset_sizes(args.site))

    for error in sorted(set(errors)):
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
