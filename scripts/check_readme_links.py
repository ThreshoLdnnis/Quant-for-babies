"""Check README navigation and commands without third-party dependencies.

Run from any directory: python scripts/check_readme_links.py
"""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
LOCALES = ("zh-TW", "en", "ru", "ja", "ko", "fr", "de", "es", "hi")
GUIDES = [ROOT / "README.md"] + [
    ROOT / "docs" / "i18n" / f"README.{locale}.md" for locale in LOCALES
]
OTHER_DOCS = [
    ROOT / "docs" / "i18n" / "README.md",
    ROOT / "docs" / "ROADMAP.md",
    ROOT / "notebooks" / "README.md",
]
ANCHORS = {"start", "setup", "curriculum", "labs", "demos", "roadmap", "faq"}
FENCES = re.compile(r"^```[^\n]*\n(.*?)^```[ \t]*$", re.M | re.S)
MD_LINK = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")


class HTMLLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "img" and attrs.get("src"):
            self.links.append(attrs["src"])


def without_code(text):
    return FENCES.sub("", text)


def parse(text):
    clean = without_code(text)
    html = HTMLLinks()
    html.feed(clean)
    return clean, html, MD_LINK.findall(clean) + html.links


def heading_ids(text):
    # GitHub-style punctuation removal, sufficient for these documentation files.
    result, counts = set(), Counter()
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M):
        heading = re.sub(r"<[^>]*>", "", heading).strip().lower()
        slug = "".join(
            ch for ch in heading
            if ch in " _-" or unicodedata.category(ch)[0] in "LN"
        ).replace(" ", "-")
        count = counts[slug]
        counts[slug] += 1
        result.add(f"{slug}-{count}" if count else slug)
    return result


def main():
    errors, checked = [], 0
    texts = {}
    for path in GUIDES + OTHER_DOCS:
        if not path.is_file():
            errors.append(f"Missing document: {path.relative_to(ROOT)}")
            continue
        texts[path] = path.read_text(encoding="utf-8")
        if "\ufffd" in texts[path]:
            errors.append(f"Replacement character: {path.relative_to(ROOT)}")

    english = ROOT / "docs" / "i18n" / "README.en.md"
    reference_commands = FENCES.findall(texts.get(english, ""))
    all_guides = set(GUIDES)
    for path, text in texts.items():
        label = path.relative_to(ROOT).as_posix()
        clean, html, links = parse(text)
        for link in links:
            target = urlsplit(link.strip().strip("<>"))
            if target.scheme or target.netloc:
                continue
            checked += 1
            local = (path.parent / unquote(target.path)).resolve() if target.path else path
            if not local.is_relative_to(ROOT):
                errors.append(f"{label}: target escapes repository: {link}")
            elif not local.exists():
                errors.append(f"{label}: missing target: {link}")
            elif target.fragment and local.suffix.lower() == ".md":
                body = local.read_text(encoding="utf-8")
                body_clean, body_html, _ = parse(body)
                fragment = unquote(target.fragment)
                if fragment not in body_html.ids | heading_ids(body_clean):
                    errors.append(f"{label}: missing anchor: {link}")
        if path not in all_guides:
            continue
        if html.ids != ANCHORS:
            errors.append(f"{label}: expected seven stable section anchors")
        if FENCES.findall(text) != reference_commands:
            errors.append(f"{label}: command blocks differ from English")

        paragraphs = re.findall(r"<p align=\"center\">(.*?)</p>", clean, re.S)
        if len(paragraphs) < 2:
            errors.append(f"{label}: language navigation is missing")
        else:
            nav = HTMLLinks()
            nav.feed(paragraphs[1])
            nav_paths = {(path.parent / urlsplit(link).path).resolve() for link in nav.links}
            if nav_paths != all_guides - {path}:
                errors.append(f"{label}: language navigation must link all other nine guides")

        inventory = {"notebooks": set(), "lectures": set(), "demos": set()}
        for link in links:
            target = (path.parent / urlsplit(link).path).resolve()
            if target.suffix == ".ipynb":
                inventory["notebooks"].add(target)
            elif target.name == "index.html" and "extras" in target.parts:
                inventory["lectures"].add(target)
            elif target.suffix == ".html" and "interactive" in target.parts:
                inventory["demos"].add(target)
        counts = {key: len(value) for key, value in inventory.items()}
        if counts != {"notebooks": 8, "lectures": 5, "demos": 7}:
            errors.append(f"{label}: incomplete inventory: {counts}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"PASS: {len(GUIDES)} language guides, {len(OTHER_DOCS)} supporting documents")
    print(f"PASS: {checked} local links and anchors; all language selectors")
    print("PASS: identical command blocks; 8 notebooks / 5 lectures / 7 demos per guide")
    return 0


if __name__ == "__main__":
    sys.exit(main())
