"""Builds the static ridni.app site from the page bodies in pages/.

Each pages/<slug>.html holds the inner <main> HTML; the first line is
`<!-- title: ... | description: ... -->`. Output: <slug>/index.html (or index.html).
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = pathlib.Path(__file__).resolve().parent / "pages"

NAV = [("privacy", "Privacy"), ("terms", "Terms"), ("support", "Support")]

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="stylesheet" href="/style.css">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
</head>
<body>
<header class="site">
  <a class="brand" href="/">Ridni</a>
  <nav>{nav}</nav>
</header>
<main>
{body}
</main>
<footer class="site">
  <span>© 2026 Ridni</span>
  <span><a href="/privacy">Privacy</a> · <a href="/terms">Terms</a> · <a href="/support">Support</a> · <a href="/delete-account">Delete account</a></span>
</footer>
</body>
</html>
"""


def nav_html(slug: str) -> str:
    parts = []
    for s, label in NAV:
        cur = ' aria-current="page"' if s == slug else ""
        parts.append(f'<a href="/{s}"{cur}>{label}</a>')
    return "".join(parts)


def main() -> None:
    for src in sorted(PAGES.glob("*.html")):
        text = src.read_text(encoding="utf-8")
        first, body = text.split("\n", 1)
        m = re.match(r"<!-- title: (.*?) \| description: (.*?) -->", first)
        if not m:
            raise SystemExit(f"{src.name}: missing header comment")
        slug = src.stem
        html = TEMPLATE.format(
            title=m.group(1), description=m.group(2), nav=nav_html(slug), body=body.strip()
        )
        out = ROOT / "index.html" if slug == "index" else ROOT / slug / "index.html"
        if slug == "404":
            out = ROOT / "404.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
