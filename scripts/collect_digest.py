"""Collect recent RSS/Atom article candidates for human curation.

Usage: python3 scripts/collect_digest.py --days 14 --output /tmp/digest-candidates.md
"""

import argparse
import datetime as dt
import email.utils
import html
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATOM = "{http://www.w3.org/2005/Atom}"


def clean(value):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value or ""))).strip()


def parse_date(value):
    if not value:
        return None
    try:
        parsed = email.utils.parsedate_to_datetime(value)
    except (TypeError, ValueError):
        try:
            parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def entries(xml_bytes):
    root = ET.fromstring(xml_bytes)
    if root.tag == "rss":
        for item in root.findall("./channel/item"):
            yield {
                "title": clean(item.findtext("title")),
                "url": (item.findtext("link") or "").strip(),
                "date": parse_date(item.findtext("pubDate")),
                "summary": clean(item.findtext("description"))[:300],
            }
    elif root.tag == ATOM + "feed":
        for item in root.findall(ATOM + "entry"):
            link = next((node.get("href", "") for node in item.findall(ATOM + "link") if node.get("rel", "alternate") == "alternate"), "")
            yield {
                "title": clean(item.findtext(ATOM + "title")),
                "url": link,
                "date": parse_date(item.findtext(ATOM + "published") or item.findtext(ATOM + "updated")),
                "summary": clean(item.findtext(ATOM + "summary"))[:300],
            }
    else:
        raise ValueError("Unsupported feed format")


def collect(sources, since):
    seen = set()
    results = []
    errors = []
    for source in sources:
        try:
            request = urllib.request.Request(source["url"], headers={"User-Agent": "SportsDigest/1.0 (personal reading list)"})
            with urllib.request.urlopen(request, timeout=20) as response:
                feed_entries = list(entries(response.read()))
            for entry in feed_entries:
                if not entry["url"] or not entry["date"] or entry["date"] < since:
                    continue
                key = entry["url"].rstrip("/")
                if key in seen:
                    continue
                seen.add(key)
                results.append({**entry, "source": source["name"], "category": source["category"]})
        except (OSError, ET.ParseError, ValueError) as exc:
            errors.append(f'{source["name"]}: {exc}')
    results.sort(key=lambda item: item["date"], reverse=True)
    return results, errors


def markdown(results, errors, since):
    lines = ["# Digest candidates", "", f"Published since {since.date().isoformat()}. Review the originals before writing summaries; this list contains feed metadata only.", ""]
    for category, label in (("hockey", "Hockey"), ("other", "Other sports and methods")):
        lines.extend([f"## {label}", ""])
        for item in results:
            if item["category"] != category:
                continue
            lines.extend([f'- [{item["title"]}]({item["url"]}) — {item["source"]}, {item["date"].date().isoformat()}', f'  {item["summary"]}', ""])
    if errors:
        lines.extend(["## Feed errors", ""] + [f"- {error}" for error in errors] + [""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, default=14)
    parser.add_argument("--output", type=Path, default=Path("/tmp/digest-candidates.md"))
    args = parser.parse_args()
    if args.days < 1:
        parser.error("--days must be positive")
    sources = json.loads((ROOT / "digest/sources.json").read_text(encoding="utf-8"))
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=args.days)
    results, errors = collect(sources, since)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(markdown(results, errors, since), encoding="utf-8")
    print(f"{len(results)} candidates; {len(errors)} feed errors; wrote {args.output}")


if __name__ == "__main__":
    main()
