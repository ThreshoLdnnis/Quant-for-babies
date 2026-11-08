"""Embed lecture 02 assets so downloading index.html alone preserves the course.

Run from any directory: python scripts/build_lecture02_standalone.py
The HTML is its own content source; CSS, JS and downloadable labs stay editable.
"""
from pathlib import Path
import re
from urllib.parse import quote


def build() -> Path:
    root = Path(__file__).resolve().parents[1]
    course = root / "extras" / "lecture-02"
    page = course / "index.html"
    html = page.read_text(encoding="utf-8")
    css = (course / "course.css").read_text(encoding="utf-8")
    js = (course / "course.js").read_text(encoding="utf-8")
    if "</style" in css.lower() or "</script" in js.lower():
        raise ValueError("Embedded assets must not contain closing HTML tags")
    style = f'<!-- course-style:start -->\n<style>\n{css.rstrip()}\n</style>\n<!-- course-style:end -->'
    script = f'<!-- course-script:start -->\n<script>\n{js.rstrip()}\n</script>\n<!-- course-script:end -->'
    if "<!-- course-style:start -->" in html:
        html, count = re.subn(r"<!-- course-style:start -->.*?<!-- course-style:end -->",
                             lambda _: style, html, flags=re.S)
    else:
        html, count = re.subn(r'<link rel="stylesheet" href="course.css">',
                             lambda _: style, html)
    if count != 1:
        raise ValueError("Expected exactly one course style block")
    html = html.replace('<script src="course.js" defer></script>', "")
    if "<!-- course-script:start -->" in html:
        html, count = re.subn(r"<!-- course-script:start -->.*?<!-- course-script:end -->",
                             lambda _: script, html, flags=re.S)
        if count != 1:
            raise ValueError("Expected exactly one course script block")
    else:
        if html.count("</body>") != 1:
            raise ValueError("Expected exactly one body end")
        html = html.replace("</body>", script + "\n</body>")
    # Embed downloadable code as data URLs too: a solitary file has no sibling labs.
    for name in ("lab.py", "collect_akshare.py"):
        data = "data:text/x-python;charset=utf-8," + quote(
            (course / name).read_text(encoding="utf-8"), safe="")
        pattern = rf'<a\b[^>]*(?:href="{re.escape(name)}"|data-course-file="{re.escape(name)}")[^>]*>'
        def embed_download(match):
            tag = re.sub(r'\s(?:href|data-course-file|download)="[^"]*"|\sdownload(?=\s|>)',
                         "", match.group(0))
            return tag[:-1] + f' data-course-file="{name}" href="{data}" download="{name}">'
        html, count = re.subn(pattern, embed_download, html)
        if count == 0:
            raise ValueError(f"Missing downloadable course file: {name}")
    base = "https://github.com/ThreshoLdnnis/Quant-for-babies/blob/main/"
    for relative, remote in {
        "../../README.md": "README.md",
        "../lecture-01/index.html": "extras/lecture-01/index.html",
        "README.md": "extras/lecture-02/README.md",
    }.items():
        html = html.replace(f'href="{relative}"', f'href="{base}{remote}"')
    page.write_text(html, encoding="utf-8")
    return page


if __name__ == "__main__":
    print(build())
