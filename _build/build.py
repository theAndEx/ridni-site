"""Builds the static ridni.app site from the page bodies in pages/<lang>/.

Each pages/<lang>/<slug>.html holds the inner <main> HTML; the first line is
`<!-- title: ... | description: ... -->`.
English is served at the root (/privacy/), other languages under /<lang>/ (/uk/privacy/).
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = pathlib.Path(__file__).resolve().parent / "pages"
SITE = "https://ridni.app"

LANGS = ["en", "uk", "ru", "pl", "de", "es", "fr"]
LANG_NAMES = {
    "en": "English", "uk": "Українська", "ru": "Русский", "pl": "Polski",
    "de": "Deutsch", "es": "Español", "fr": "Français",
}
UI = {
    "en": {"privacy": "Privacy", "terms": "Terms", "support": "Support", "delete": "Delete account", "lang": "Language"},
    "uk": {"privacy": "Конфіденційність", "terms": "Умови", "support": "Підтримка", "delete": "Видалити акаунт", "lang": "Мова"},
    "ru": {"privacy": "Конфиденциальность", "terms": "Условия", "support": "Поддержка", "delete": "Удалить аккаунт", "lang": "Язык"},
    "pl": {"privacy": "Prywatność", "terms": "Regulamin", "support": "Pomoc", "delete": "Usuń konto", "lang": "Język"},
    "de": {"privacy": "Datenschutz", "terms": "Nutzungsbedingungen", "support": "Hilfe", "delete": "Konto löschen", "lang": "Sprache"},
    "es": {"privacy": "Privacidad", "terms": "Términos", "support": "Ayuda", "delete": "Eliminar cuenta", "lang": "Idioma"},
    "fr": {"privacy": "Confidentialité", "terms": "Conditions", "support": "Assistance", "delete": "Supprimer le compte", "lang": "Langue"},
}

TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
{alternates}
<link rel="stylesheet" href="/style.css">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{redirect}</head>
<body>
<header class="site">
  <a class="brand" href="{home}">Ridni</a>
  <nav>{nav}</nav>
</header>
<main>
{body}
</main>
<footer class="site">
  <span>© 2026 Ridni</span>
  <span><a href="{p}privacy/">{privacy}</a> · <a href="{p}terms/">{terms}</a> · <a href="{p}support/">{support}</a> · <a href="{p}delete-account/">{delete}</a></span>
  <span class="langs" aria-label="{lang_label}">{langs}</span>
</footer>
</body>
</html>
"""

# On English pages only: send a first-time visitor whose browser prefers one of our
# other languages to that version. An explicit click on a language link is remembered.
REDIRECT = """<script>
(function () {{
  try {{
    if (/[?&]lang=en\b/.test(location.search)) {{ localStorage.setItem('ridni-lang', 'en'); return; }}
    var saved = localStorage.getItem('ridni-lang');
    var supported = {supported};
    var want = saved || (navigator.language || 'en').slice(0, 2).toLowerCase();
    if (want !== 'en' && supported.indexOf(want) !== -1) {{
      location.replace('/' + want + location.pathname + location.search + location.hash);
    }}
  }} catch (e) {{}}
}})();
</script>
"""

LANG_CLICK = "try{localStorage.setItem('ridni-lang','%s')}catch(e){}"


def prefix(lang: str) -> str:
    return "/" if lang == "en" else f"/{lang}/"


def page_path(lang: str, slug: str) -> str:
    if slug == "index":
        return prefix(lang)
    return f"{prefix(lang)}{slug}/"


def main() -> None:
    slugs = sorted(p.stem for p in (PAGES / "en").glob("*.html"))
    for lang in LANGS:
        ui = UI[lang]
        for slug in slugs:
            if slug == "404" and lang != "en":
                continue
            src = PAGES / lang / f"{slug}.html"
            if not src.exists():
                raise SystemExit(f"missing {src.relative_to(PAGES)}")
            first, body = src.read_text(encoding="utf-8").split("\n", 1)
            m = re.match(r"<!-- title: (.*?) \| description: (.*?) -->", first)
            if not m:
                raise SystemExit(f"{src}: missing header comment")
            nav = "".join(
                f'<a href="{prefix(lang)}{s}/"' + (' aria-current="page"' if s == slug else "") + f">{ui[s]}</a>"
                for s in ("privacy", "terms", "support")
            )
            target = "index" if slug == "404" else slug
            langs = " ".join(
                (f"<strong>{LANG_NAMES[l]}</strong>" if l == lang else
                 f'<a href="{page_path(l, target)}" hreflang="{l}" onclick="{LANG_CLICK % l}">{LANG_NAMES[l]}</a>')
                for l in LANGS
            )
            alternates = ""
            if slug != "404":
                alternates = "\n".join(
                    f'<link rel="alternate" hreflang="{l}" href="{SITE}{page_path(l, slug)}">' for l in LANGS
                ) + f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{page_path("en", slug)}">'
            redirect = ""
            if lang == "en" and slug != "404":
                redirect = REDIRECT.format(supported=str([l for l in LANGS if l != "en"]).replace("'", '"'))
            html = TEMPLATE.format(
                lang=lang, title=m.group(1), description=m.group(2), alternates=alternates,
                redirect=redirect, home=prefix(lang), nav=nav, body=body.strip(), p=prefix(lang),
                privacy=ui["privacy"], terms=ui["terms"], support=ui["support"], delete=ui["delete"],
                lang_label=ui["lang"], langs=langs,
            )
            if slug == "404":
                if lang != "en":
                    continue
                out = ROOT / "404.html"
            elif slug == "index":
                out = ROOT / ("index.html" if lang == "en" else f"{lang}/index.html")
            else:
                out = ROOT / (f"{slug}/index.html" if lang == "en" else f"{lang}/{slug}/index.html")
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(html, encoding="utf-8")
            print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
