# ridni.app — how this site works and how to change it

Static site for the Ridni app: home, privacy, terms, support, delete-account, 404 — in 7 languages.
Served by **GitHub Pages** from `main` / root at **https://ridni.app**. Owner: Andrii Sotnikov.
Maintained by Claude Code (text and data claims) and Claude Design (look). Read this file before changing anything.

## 1. The one rule: the site follows the code

`_build/CLAIMS.md` lists every statement on the site about data — what is stored, who sees it, how long it is kept,
what is deleted, which emails and pushes go out, which SDKs and permissions the app uses — with the file in the app
(`family-app-rn`) or backend (`family-app/backend`) that makes it true.

- A change in the app or backend that touches a CLAIMS row → update the row **and** the page text in **all 7
  languages** in the same piece of work, rebuild, push.
- Never write site text from design docs alone (`handoff/web/*.md` are superseded). Check the code, then write.
- A promise the code does not keep yet gets ❌ in CLAIMS.md and a task in `family-app-rn/.claude/design/SYNC.md`
  ("Waiting on Code"). Do not leave it unrecorded.
- Why: on 2026-11-20 the privacy page said "no photos" while profile photos shipped.

## 2. Layout

```
_build/
  build.py                   generator — run after every change
  CLAIMS.md                  claim → code ledger (section 1)
  pages/<lang>/<slug>.html   page bodies (the only files you edit for text)
index.html, privacy/, terms/, support/, delete-account/, 404.html   ← English, generated
uk/ ru/ pl/ de/ es/ fr/                                              ← other languages, generated
style.css  favicon.svg  site.webmanifest  assets/   ← Design's look (D-248); change only with Design
CNAME (ridni.app)  .nojekyll                        ← never remove
```

- Languages: `en uk ru pl de es fr` (same as the app). English at the root, others under `/<lang>/`.
- Slugs: `index privacy terms support delete-account` (+ `404` in `en` only).
- First line of every page file: `<!-- title: ... | description: ... -->` (used for `<title>`, meta, OG).
- Body is the inner HTML of `<main>`: `h1`, `h2`, `p`, `ul/li`, `strong/em/a`. Prose pages get class `prose`
  automatically; `index` and `404` do not.
- **All language files of a page have the same block order** (same `h2`/`p` sequence). Keep it that way: edit the
  same block in every language, so the versions can be compared side by side.
- Generated files (`index.html`, `*/index.html`, `404.html`) are never edited by hand — they are overwritten.

## 3. Writing the text

- English is the **binding** version of privacy and terms (each says so); translations link to it with `?lang=en`.
- Register follows the app: informal — uk/ru «ти/ты», pl «ty», de «du», es «tú», fr «tu». uk/ru use paired forms
  where the app does («ти запросив або запросила»).
- Role names and menu paths exactly as the app shows them (owner / parents / caregivers; More → Account → Delete
  account; uk «Ще → …»). Check `family-app-rn/src/i18n/locales/<lang>.json`.
- No medical claims: Ridni records, it does not assess. WHO band and IOM range are "reference lines, not verdicts".
- No prices on the site; subscriptions are described generically (Terms → Subscriptions).
- Contacts on the site: `support@ridni.app` (help, deletion), `privacy@ridni.app` (data requests). Both forward to
  the owner (Porkbun email forwarding). The controller is "Andrii Sotnikov, Kyiv, Ukraine" — no street address.
- **Effective date** (`<p class="effective">` at the top of each page): change it in all 7 languages when the meaning
  of a page changes, not for typo fixes. A material privacy change must also be announced in the app (the page promises it).

## 4. Build, check, publish

```
python3 _build/build.py                 # regenerates every language and page
git diff --stat                         # sources AND generated files should both change
git add -A && git commit -m "…" && git push origin main
```

- GitHub Pages rebuilds in about a minute. Verify in a browser (a sandbox may block ridni.app for curl):
  `https://ridni.app/privacy/?lang=en`, `/uk/privacy/`, … — check the changed sentence in every language.
- `?lang=en` stops the browser-language redirect (English pages send first-time visitors to their language).
- **The repo must stay public** — GitHub Pages on this plan switches off when it goes private (happened on 2026-11-20).
  If the site 404s after a push, check Settings → Pages: source `main` / root, custom domain `ridni.app`, HTTPS on.
- Commit with the owner's git identity already configured on his machine, plus the session attribution lines.

## 5. Do not touch without asking the owner

- DNS at Porkbun (A ×4 / AAAA ×4 to GitHub Pages, `www` CNAME, `mail.ridni.app` records for Resend, `_dmarc`, SPF TXT
  on `mail`). Normal edits need no DNS changes.
- `CNAME`, `.nojekyll`, repository visibility, Pages settings.
- Design files (`style.css`, `favicon.svg`, `assets/`): changes come from Claude Design via SYNC.md.
- Fonts: `assets/fonts/manrope-{500,700,800}.woff2` are Latin+Cyrillic subsets of the app's Manrope TTFs (OFL,
  notice in `assets/fonts/README.md`). If a page needs a character outside the subset, re-subset from the app's
  `assets/fonts/*.ttf` with `pyftsubset` — do not link Google Fonts.

## 6. Where things are decided

- Owner decisions and console setup: `family-app/docs/plans/05-email-google-apple-setup-RESULTS.md`.
- Code ↔ Design channel: `family-app-rn/.claude/design/SYNC.md`.
- Open items across Code / Design / owner: Ridni project doc `claude/OPEN-ITEMS.md`.
- The app links here: `https://ridni.app/{lang}/privacy/`, `/terms/`, `/support/`, `/delete-account/` (English without
  `/en`). Google OAuth branding and App Store Connect use the English URLs — keep those paths stable.
