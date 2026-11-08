"""Embed lecture 03 assets and code attachments into one offline-readable HTML."""
from pathlib import Path
import re
from urllib.parse import quote


def build() -> Path:
    root = Path(__file__).resolve().parents[1]
    course = root / "extras" / "lecture-03"
    page = course / "index.html"
    html = page.read_text(encoding="utf-8")
    assets = {"style": (course / "course.css").read_text(encoding="utf-8"),
              "script": (course / "course.js").read_text(encoding="utf-8")}
    for tag, source in assets.items():
        if f"</{tag}" in source.lower():
            raise ValueError(f"Unsafe closing {tag} in embedded asset")
        block = f'<!-- course-{tag}:start -->\n<{tag}>\n{source.rstrip()}\n</{tag}>\n<!-- course-{tag}:end -->'
        marker = f"<!-- course-{tag}:start -->"
        if marker in html:
            html, n = re.subn(rf"{marker}.*?<!-- course-{tag}:end -->", lambda _: block, html, flags=re.S)
            if n != 1:
                raise ValueError(f"Expected one {tag} marker")
        elif tag == "style":
            html, n = re.subn('<link rel="stylesheet" href="course.css">', lambda _: block, html)
            if n != 1:
                raise ValueError("Expected one stylesheet link")
        else:
            html = html.replace('<script src="course.js" defer></script>', "")
            if html.count("</body>") != 1:
                raise ValueError("Expected one body end")
            html = html.replace("</body>", block + "\n</body>")
    for name in ("factor_lab.py", "requirements.txt", "plot_factors.py", "requirements-plot.txt"):
        source = (course / name).read_text(encoding="utf-8")
        mime = "text/x-python" if name.endswith(".py") else "text/plain"
        data = f"data:{mime};charset=utf-8," + quote(source, safe="")
        pattern = rf'<a\b[^>]*(?:href="{re.escape(name)}"|data-course-file="{re.escape(name)}")[^>]*>'
        def embed(match):
            tag = re.sub(r'\s(?:href|data-course-file|download)="[^"]*"|\sdownload(?=\s|>)', "", match.group(0))
            return tag[:-1] + f' data-course-file="{name}" href="{data}" download="{name}">'
        html, n = re.subn(pattern, embed, html)
        if n == 0:
            raise ValueError(f"Missing attachment link: {name}")
    base = "https://github.com/ThreshoLdnnis/Quant-for-babies/blob/main/"
    for local, remote in {"../../README.md": "README.md", "README.md": "extras/lecture-03/README.md",
                          "../lecture-02/index.html": "extras/lecture-02/index.html"}.items():
        html = html.replace(f'href="{local}"', f'href="{base}{remote}"')
    page.write_text(html, encoding="utf-8")
    return page


if __name__ == "__main__":
    print(build())
