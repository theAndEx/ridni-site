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

TEMPLATE = '<!doctype html>\n<html lang="{lang}" dir="ltr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="color-scheme" content="light dark">\n<title>{title} · Ridni</title>\n<meta name="description" content="{description}">\n<link rel="canonical" href="https://ridni.app{path}">\n{hreflang}\n<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n<link rel="icon" href="/assets/icon-32.png" sizes="32x32" type="image/png">\n<link rel="apple-touch-icon" href="/assets/icon-180.png">\n<link rel="manifest" href="/site.webmanifest">\n<meta property="og:type" content="website">\n<meta property="og:site_name" content="Ridni">\n<meta property="og:title" content="{title}">\n<meta property="og:description" content="{description}">\n<meta property="og:url" content="https://ridni.app{path}">\n<meta property="og:image" content="https://ridni.app/assets/og-{lang}.png">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta name="twitter:card" content="summary_large_image">\n<link rel="stylesheet" href="/style.css">\n{redirect}</head>\n<body>\n\n<header class="site-header">\n  <a class="wordmark" href="{home}" aria-label="Ridni">\n    <svg class="mark" viewBox="-2.5 -1.5 105 101" aria-hidden="true" focusable="false">\n      <path d="M50 80 C24 63 17 48 17 37 C17 25 26 18 35 18 C43 18 50 24 50 33 M83.5 46 C81 60 70 69 50 80"\n            fill="none" stroke="currentColor" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>\n      <circle cx="73.5" cy="27.5" r="15" fill="currentColor"/>\n    </svg>\n    <svg class="word" viewBox="0 0 114.65 37.5" aria-hidden="true" focusable="false">\n      <path transform="translate(-3.5 36.75) scale(0.025)" fill="currentColor" d="M140 0V-1440H748Q769 -1440 804.5 -1438.5Q840 -1437 868 -1432Q997 -1412 1079.5 -1347.0Q1162 -1282 1201.0 -1183.5Q1240 -1085 1240 -964Q1240 -783 1150.0 -654.5Q1060 -526 868 -496L748 -488H412V0ZM952 0 668 -586 948 -640 1260 0ZM412 -742H736Q757 -742 782.0 -744.0Q807 -746 828 -752Q883 -767 913.0 -802.5Q943 -838 954.5 -881.5Q966 -925 966 -964Q966 -1003 954.5 -1046.5Q943 -1090 913.0 -1125.5Q883 -1161 828 -1176Q807 -1182 782.0 -1184.0Q757 -1186 736 -1186H412ZM1460.0 -1230V-1470H1732.0V-1230ZM1460.0 0V-1080H1732.0V0ZM2430.0 30Q2281.0 30 2169.0 -45.0Q2057.0 -120 1994.5 -249.0Q1932.0 -378 1932.0 -540Q1932.0 -705 1995.5 -833.5Q2059.0 -962 2174.0 -1036.0Q2289.0 -1110 2444.0 -1110Q2598.0 -1110 2703.0 -1035.0Q2808.0 -960 2862.0 -831.0Q2916.0 -702 2916.0 -540Q2916.0 -378 2861.5 -249.0Q2807.0 -120 2699.0 -45.0Q2591.0 30 2430.0 30ZM2474.0 -212Q2565.0 -212 2619.5 -253.0Q2674.0 -294 2698.0 -368.0Q2722.0 -442 2722.0 -540Q2722.0 -638 2698.0 -712.0Q2674.0 -786 2621.5 -827.0Q2569.0 -868 2484.0 -868Q2393.0 -868 2334.5 -823.5Q2276.0 -779 2248.0 -704.5Q2220.0 -630 2220.0 -540Q2220.0 -449 2247.0 -374.5Q2274.0 -300 2330.0 -256.0Q2386.0 -212 2474.0 -212ZM2722.0 0V-740H2688.0V-1440H2962.0V0ZM3938.0 0V-510Q3938.0 -547 3934.0 -604.5Q3930.0 -662 3909.0 -720.0Q3888.0 -778 3840.5 -817.0Q3793.0 -856 3706.0 -856Q3671.0 -856 3631.0 -845.0Q3591.0 -834 3556.0 -802.5Q3521.0 -771 3498.5 -710.0Q3476.0 -649 3476.0 -548L3320.0 -622Q3320.0 -750 3372.0 -862.0Q3424.0 -974 3528.5 -1043.0Q3633.0 -1112 3792.0 -1112Q3919.0 -1112 3999.0 -1069.0Q4079.0 -1026 4123.5 -960.0Q4168.0 -894 4187.0 -822.5Q4206.0 -751 4210.0 -692.0Q4214.0 -633 4214.0 -606V0ZM3200.0 0V-1080H3442.0V-722H3476.0V0ZM4454.0 -1230V-1470H4726.0V-1230ZM4454.0 0V-1080H4726.0V0Z"/>\n    </svg>\n  </a>\n  <ul class="langs">{langs}</ul>\n</header>\n\n<main class="{mainClass}">\n{body}\n</main>\n\n<footer class="site-footer">\n  <nav>{footerLinks}</nav>\n  <p>{footerNote}</p>\n</footer>\n\n</body>\n</html>\n'

# On English pages only: send a first-time visitor whose browser prefers one of our
# other languages to that version. An explicit click on a language link is remembered.
REDIRECT = """<script>
(function () {{
  try {{
    if (location.search.indexOf('lang=en') !== -1) {{ localStorage.setItem('ridni-lang', 'en'); return; }}
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
            target = "index" if slug == "404" else slug
            langs = "".join(
                f'<li><a href="{page_path(l, target)}" hreflang="{l}" lang="{l}" title="{LANG_NAMES[l]}"'
                + (' aria-current="true"' if l == lang else f' onclick="{LANG_CLICK % l}"')
                + f'>{l.upper()}</a></li>'
                for l in LANGS
            )
            hreflang = ""
            if slug != "404":
                hreflang = "\n".join(
                    f'<link rel="alternate" hreflang="{l}" href="{SITE}{page_path(l, slug)}">' for l in LANGS
                ) + f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{page_path("en", slug)}">'
            redirect = ""
            if lang == "en" and slug != "404":
                redirect = REDIRECT.format(supported=str([l for l in LANGS if l != "en"]).replace("'", '"'))
            footer_links = " ".join(
                f'<a href="{prefix(lang)}{s}/">{ui[k]}</a>'
                for s, k in (("privacy", "privacy"), ("terms", "terms"), ("support", "support"), ("delete-account", "delete"))
            )
            title = re.sub(r"\s*[—-]\s*Ridni$", "", m.group(1))
            title = re.sub(r"^Ridni\s*[—-]\s*", "", title)
            title = title[:1].upper() + title[1:]
            html = TEMPLATE.format(
                lang=lang, title=title, description=m.group(2), path=page_path(lang, target) if slug != "404" else "/404.html",
                hreflang=hreflang, redirect=redirect, home=prefix(lang), langs=langs,
                mainClass="" if slug in ("index", "404") else "prose", body=body.strip(),
                footerLinks=footer_links, footerNote='<span class="copy">© 2026 Ridni</span>',
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
