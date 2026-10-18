#!/usr/bin/env python3
"""Static regression checks for the SHANXING GitHub Pages site."""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = [ROOT / "index.html", ROOT / "guide.html", ROOT / "404.html"]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.hrefs: list[str] = []
        self.json_ld: list[str] = []
        self._in_json_ld = False
        self._json_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        element_id = attributes.get("id")
        if element_id:
            self.ids.add(element_id)
        href = attributes.get("href")
        if href:
            self.hrefs.append(href)
        if tag == "script" and attributes.get("type") == "application/ld+json":
            self._in_json_ld = True
            self._json_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._in_json_ld:
            self.json_ld.append("".join(self._json_parts))
            self._in_json_ld = False
            self._json_parts = []

    def handle_data(self, data: str) -> None:
        if self._in_json_ld:
            self._json_parts.append(data)


def check(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    pages: dict[Path, tuple[str, PageParser]] = {}

    for path in HTML_FILES:
        check(path.exists(), f"missing file: {path.name}", errors)
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        parser = PageParser()
        parser.feed(text)
        pages[path] = (text, parser)
        for index, block in enumerate(parser.json_ld, start=1):
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                errors.append(f"{path.name}: invalid JSON-LD block {index}: {exc}")

    combined = "\n".join(text for text, _ in pages.values())
    banned = [
        "in-house mold shop",
        "hold a physical sample",
        "Lowest MOQ in market",
        "15yrs",
        "unlimited revisions",
        "must upload CPSIA-compliant",
        "$2+ billion",
        "130% year-over-year",
        "No commitment, no upfront payment",
        "retained forever",
        "test reports are available",
    ]
    for phrase in banned:
        check(phrase.lower() not in combined.lower(), f"unsupported/ambiguous claim remains: {phrase}", errors)

    index_text = pages.get(ROOT / "index.html", ("", PageParser()))[0]
    guide_text = pages.get(ROOT / "guide.html", ("", PageParser()))[0]
    required_index = [
        "Products made in our Fujian factory",
        "specialist mold-making partners",
        "Third-party lab testing arranged on request",
        "100 pcs per design",
        "Budgetary pricing assumptions",
        "Source: SHANXING website",
        "Send Quote via WhatsApp",
        "Number of Designs",
        "Delivery City",
        "Postal Code",
    ]
    for phrase in required_index:
        check(phrase.lower() in index_text.lower(), f"index.html missing: {phrase}", errors)

    required_guide = [
        "mold manufacturing is handled by specialist partners",
        "shoe-charm production stays in our Fujian factory",
        "accredited third-party lab",
        "finished-product or batch testing",
        "This guide is commercial sourcing information, not legal advice",
    ]
    for phrase in required_guide:
        check(phrase.lower() in guide_text.lower(), f"guide.html missing: {phrase}", errors)

    for path, (text, parser) in pages.items():
        check('href="/"' not in text, f"{path.name}: project Pages must not link to site root /", errors)
        for href in parser.hrefs:
            if href.startswith(("//", "http://", "https://", "mailto:", "tel:", "#")):
                if href.startswith("#") and href[1:]:
                    check(href[1:] in parser.ids, f"{path.name}: missing anchor target {href}", errors)
                continue
            target, _, anchor = href.partition("#")
            target_path = (path.parent / target).resolve() if target else path
            check(target_path.exists(), f"{path.name}: broken internal link {href}", errors)
            if anchor and target_path in pages:
                check(anchor in pages[target_path][1].ids, f"{path.name}: missing target anchor {href}", errors)

    whatsapp_links = re.findall(r'href="([^"]*wa\.me[^"]*)"', index_text)
    check(bool(whatsapp_links), "index.html: no WhatsApp links", errors)
    for link in whatsapp_links:
        decoded = unquote(link)
        check("Source: SHANXING website" in decoded, f"WhatsApp link lacks source attribution: {link}", errors)

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    check("<lastmod>2026-08-09</lastmod>" in sitemap, "sitemap lastmod not updated to 2026-08-09", errors)
    llms = ROOT / "llms.txt"
    check(llms.exists(), "missing file: llms.txt", errors)
    if llms.exists():
        llms_text = llms.read_text(encoding="utf-8")
        check("The HTML pages above are the authoritative public content" in llms_text, "llms.txt missing authority boundary", errors)

    if errors:
        print("SITE VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("SITE VALIDATION PASSED")
    print(f"- HTML pages: {len(pages)}")
    print(f"- JSON-LD blocks: {sum(len(parser.json_ld) for _, parser in pages.values())}")
    print(f"- WhatsApp links checked: {len(whatsapp_links)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
