# CyberLavandaTea

Tema **Hugo** dark-only per blog di sviluppo/codice.
**Tailwind CSS v4**, palette a **6 ruoli** (un viola + un verde), impianto
**IndieWeb / POSSE**, feed multipli, ricerca client-side.

Deriva da:

- [`docs/THEME.md`](../../docs/THEME.md) — elenco funzioni (Parti 1–3) + **Parte 4**
  (palette a 6 ruoli, verifica WCAG, mapping Chroma);
- [`docs/palette-preview.html`](../../docs/palette-preview.html) — mockup di
  riferimento con i font reali (Audiowide / Rajdhani).

> **Dark-only per scelta.** Nessun toggle chiaro: `docs/THEME.md` §4 definisce una
> palette esclusivamente scura. `assets/js/theme.js` fissa `class="dark"` prima
> del paint.

---

## Requisiti

| | |
|---|---|
| Hugo | **≥ 0.146** *extended* (nuovo sistema di template: `_partials/`, `_shortcodes/`, `_markup/`) |
| Node | per `@tailwindcss/cli` (usato da `css.TailwindCSS`) |

```bash
# nella root del sito
npm install -D @tailwindcss/cli   # oppure: npm install (usa themes/cyberlavandatea/package.json)
```

## Attivazione

### Come submodule / cartella

```bash
git submodule add https://github.com/fundor333/cyberlavandatea themes/cyberlavandatea
```

```toml
# hugo.toml del sito
theme = "cyberlavandatea"
```

Hugo eredita dal tema `params`, `related`, `services`, `mediaTypes`, `build`,
`markup`. **NON** eredita `outputs`, `outputFormats`, `taxonomies`, `security`:
quel pezzo va nel config del sito.

### Configurazione minima del sito

Copia questo blocco nel tuo `hugo.toml` (identico a
`exampleSite/hugo.toml`):

```toml
[taxonomies]
  series = "series"
  category = "categories"
  tag = "tags"
  theme = "themes"
  group = "group"

[mediaTypes."application/atom+xml"]
  suffixes = ["xml"]

[outputFormats.SearchIndex]
  baseName = "search"
  mediaType = "application/json"
  isPlainText = true
[outputFormats.Atom]
  baseName = "atom"
  mediaType = "application/atom+xml"
[outputFormats.humanstxt]
  baseName = "humans"
  mediaType = "text/plain"
  isPlainText = true

[outputs]
  home = ["html", "rss", "json", "SearchIndex", "Atom", "humanstxt"]
  section = ["html", "rss", "json", "Atom"]

# Necessario per css.TailwindCSS (policy di sicurezza di Hugo).
[security]
  [security.exec]
    allow = ['^(dart-)?sass$', '^git$', '^go$', '^node$', '^npx$', '^postcss$', '^tailwindcss$']

# Highlight con classi .chroma (→ palette del tema) e immagini "da sole"
# rese come <figure> + <figcaption>.
[markup]
  [markup.highlight]
    noClasses = false
  [markup.goldmark.parser]
    wrapStandAloneImageWithinParagraph = false
```

### Tailwind — rilevamento delle classi (opzionale)

Il layout del tema è scritto in CSS puro: **funziona senza configurazione**. Le
utility Tailwind usate nei template hanno un fallback in `main.css`. Se vuoi che
Tailwind generi *tutte* le utility che usi nei tuoi contenuti/shortcode, abilita
`hugo_stats.json`:

```toml
[build.buildStats]
  enable = true
[[module.mounts]]
  source = "assets"
  target = "assets"
[[module.mounts]]
  source = "hugo_stats.json"
  target = "assets/notwatching/hugo_stats.json"
  disableWatch = true
```

(`main.css` fa già `@source "hugo_stats.json"`.) In alternativa, aggiungi le
classi extra a `assets/css/safelist.txt` del tema o in un tuo
`assets/css/*.css` che importa `main.css` con un tuo `@source`.

### Provare la demo

```bash
cd themes/cyberlavandatea
npm install
hugo server -s exampleSite --themesDir ../..
```

---

## Palette (docs/THEME.md §4)

Definita una sola volta in [`assets/css/main.css`](assets/css/main.css) dentro il
blocco Tailwind `@theme` → disponibile come utility (`text-content`, `bg-surface`,
`border-border`, …) **e** come `--color-*` per i partial.

| Ruolo | Token Tailwind | Hex | Uso |
|---|---|---|---|
| Primary *(viola)* | `--color-primary` | `#9B8CF8` | accento, `:hover`/`:focus`, nav attiva, focus ring, bordo `blockquote`, keyword |
| Content | `--color-content` | `#DCDCE4` | testo, heading, `strong`, testo codice |
| Links *(verde)* | `--color-link` | `#74D18C` | link non visitati, stringhe, diff aggiunta |
| Visited | `--color-visited` | `#9E8FBE` | `a:visited` |
| Background | `--color-background` | `#1E1E24` | `body`, navbar, footer |
| Inactive | `--color-inactive` | `#8C8C99` | meta, date, bordi, placeholder, commenti |
| *(derivato)* Surface | `--color-surface` | `#2D2D33` | `code`/`pre`/`.toc`/`blockquote`/`tr:nth-child(even)` |
| *(derivato)* Border | `--color-border` | `#39393F` | `hr`, separatori, bordi |

Sintassi Chroma (`.chroma`): solo viola + verde + 2 tint (`--color-code-fn`
`#A6E0B4`, `--color-code-num` `#C3B8F5`) + 1 rosso opzionale per gli errori
(`--color-code-err` `#E1808F`), confinato al `<pre>`.

I font sono caricati da Google Fonts in `_partials/head.html` a partire da
`params.fonts` (`display` = Audiowide, `body` = Rajdhani).

---

## Funzioni implementate (mappa verso docs/THEME.md)

| docs/THEME.md | Dove |
|---|---|
| Fondamenta: `baseof` + blocco `main`, `home`, `list` (per anno), `single`, `404`, `taxonomy`, `term` | `layouts/*.html` |
| `<head>` + SEO: meta, OG, Twitter, JSON-LD `BlogPosting`, `canonical`, `hreflang`, `rel=first/last/prev/next` | `_partials/head.html`, `_partials/meta/*` |
| Asset pipeline: **Tailwind v4** → `minify` → `fingerprint`+`integrity`; `theme.js` in testa, `main.js`+`goToTop` in coda, `additionalScripts` | `_partials/head.html`, `_partials/scripts-*.html` |
| Navigazione: menu `Site.Menus.main` con figli e stato `active`, hamburger CSS-only, selettore lingua, bottone "torna su" | `_partials/header.html`, `_partials/footer.html`, `assets/js/goToTop.js` |
| `postCard` con icona per tipo, starred, speaker, `<time datetime>` | `_partials/postCard.html` |
| Bio + **h-card** (pronomi, nickname, località) | `_partials/bio.html`, `_partials/hcard.html` |
| i18n | `i18n/en.yaml`, `i18n/it.yaml` |
| Feed: RSS (`exclude_from_rss`, `summary`/`full`, namespace `media`), **Atom** (`feedUUID`, `webfeeds`), **JSON Feed 1.1**, **humans.txt**, **robots.txt** dinamico | `layouts/rss.xml`, `list.atom.xml`, `list.json.json`, `index.humanstxt.txt`, `robots.txt` |
| Ricerca: output `SearchIndex` → `/search.json`, sezione `/search`, form `?q=`, indice **Lunr**, rendering da `<template>` | `layouts/index.searchindex.json`, `layouts/search/list.html`, `_partials/search-*.html`, `assets/js/search.js` |
| Tipi di contenuto: `micro`, `photos` (EXIF da `exif.json` o `.Exif`), `weeknote`, `event` (`start`/`end`/`location`), `now`, `series` | `layouts/<tipo>/…` |
| Microformats2: `h-entry` / `e-content` / `u-photo` / `p-category` / `dt-published`; tipi di risposta reply/repost/like/bookmark/rsvp | `layouts/single.html`, `_partials/micro.html` |
| **Webmention** (invio + rendering webmention.io) | `_partials/webmention.html`, `_partials/custom-head.html` |
| **Commenti Mastodon** (fetch `/context` + DOMPurify) + embed toot a build time | `_partials/mastodon.html`, `_partials/toot.html` |
| **Brid.gy Publish** con target configurabili + UTM | `_partials/bridgy.html` |
| **Syndication** ("also posted on") | `_partials/syndication.html` |
| Render hooks: link (UTM+`target=_blank`+icona), immagini (`figure`+`u-photo`), heading (anchor), codeblock (`HighlightCodeBlock`) | `layouts/_markup/render-*.html` |
| Shortcode: `toc`, `embed`, `toot`, `xkcd`, `allpages`, `88x31`, `buzzword`, `heart` | `layouts/_shortcodes/*` |
| Icone per **tipo di contenuto** ("categoria") con Font Awesome (Kit o CDN free), override `params.postIcons` | `_partials/fontawesome.html`, `_partials/type-icon.html`, `_partials/postCard.html` |
| **Angolo LGBT+** (pride.codes, in alto a dx) opt-in `params.prideCorner` (default `false`) | `_partials/pride-corner.html` |
| Extra small-web: badge **88×31** (cartella + JSON, shuffle), **webring** (`webring.html`: icona / prev-next / web component), "cita questo post" (copia URL), "scritto da umano", **backlink** (`findRE`), **related** ("See Also") | `_partials/88x31.html`, `_partials/webring.html`, `_partials/cite.html`, `_partials/inbound-links.html`, `_partials/comments.html`, `footer.html` |
| Palette / theming: 6 ruoli + superfici per opacità, Chroma solo viola/verde | `assets/css/main.css` |

> KaTeX condizionale (`_partials/helpers/katex.html`) e Google Analytics
> (`hugo.IsProduction` + `site.GoogleAnalytics`) sono inclusi come da checklist.

---

## Parametri principali (`params`)

```toml
[params]
  description       = "…"           # meta description di fallback
  dateFormat        = "2 January 2006"
  homeRecentCount   = 20             # post in home
  mainSections      = ["post"]
  secondarysections = ["micro"]      # lista "Recent updates" in home
  feedSections      = ["post", "micro", "photos", "weeknote"]
  commentSections   = ["post", "micro", "photos", "weeknote"]
  suggestionSections= ["post"]       # blocco "See Also" (Related)
  toc = true
  tocOpen = false
  goToTop = true
  linkUTM = false                    # UTM sui link esterni (render hook)
  writtenByHuman = true
  shareButtons = true
  cite = true
  badges88x31 = true
  additionalScripts = []             # asset JS extra, bundle+minify
  themeColor = "#1e1e24"
  feedUUID = ""                      # urn:uuid per l'Atom
  images = ["/img/og.png"]           # og:image di fallback
  prideCorner = false               # angolo LGBT+ pride.codes in alto a dx (opt-in)

  [params.fontawesome]              # icone per tipo di contenuto
    kit = ""                         # URL di un Kit (anche Pro); vuoto = CDN free
    version = "6.7.2"                # versione del CDN free
    disable = false                  # true = niente Font Awesome

  # Icona FA per "categoria" (= tipo di sezione). Default sensati inclusi;
  # override solo le voci che vuoi cambiare.
  [params.postIcons]
    post     = "fa-solid fa-newspaper"
    micro    = "fa-solid fa-thumbtack"
    photos   = "fa-solid fa-camera"
    weeknote = "fa-solid fa-mug-hot"
    event    = "fa-solid fa-calendar-days"
    now      = "fa-solid fa-hourglass-half"
    series   = "fa-solid fa-layer-group"

  [params.fonts]
    display = "Audiowide"
    body = "Rajdhani:wght@400;500;600;700"

  [params.author]
    name = "" ; intro = "" ; description = "" ; url = "" ; email = ""
    fediverseAccount = "@utente@istanza"

  [params.hcard]
    fullName = "" ; nickname = "" ; avatar = "img/logo.png"
    showLocation = true ; city = "" ; region = "" ; country = ""
    [params.hcard.pronouns]
      nominative = "" ; oblique = "" ; possessive = ""

  [params.webmention]
    targetDomain = "example.com"     # dominio canonico per webmention.io
    # endpoint / pingback / script opzionali

  bridgy = ["mastodon", "bluesky"]

  [[params.socialIcons]]
    name = "github" ; url = "https://github.com/utente"

  # Webring nel footer (partial webring.html). Ogni voce:
  #   name, url            link semplice
  #   + icon               link icona (img 30x30)
  #   + prev / next        rende  ← name →
  #   + html [+ script]    markup grezzo (web component) e script defer
  [[params.webrings]]
    name = "XXIIVV webring" ; url = "https://webring.xxiivv.com/#86"
    icon = "https://webring.xxiivv.com/icon.white.svg"
  [[params.webrings]]
    name = "IndieWeb Webring" ; url = "https://xn--sr8hvo.ws"
    prev = "https://xn--sr8hvo.ws/previous" ; next = "https://xn--sr8hvo.ws/next"
  [[params.webrings]]
    name = "djangowebring"
    html = '<webring-css site="https://example.org"></webring-css>'
    script = "https://djangowebring.com/static/webring.js"
```

### Front matter riconosciuto

`description`, `image`, `tags`, `categories`, `series`, `themes`, `group`,
`isStarred`, `speaker`, `math`, `toc`, `tocOpen`, `exclude_from_rss`,
`exclude_from_search`, `robotsdisallow`, `allpage`, `feature_link`/`feature_text`,
`syndication` (lista URL), `comments` (`{host, user, id}` per i commenti
Mastodon), `reply`/`repost`/`like`/`bookmark`/`rsvp`/`preview_text_from_reply`,
`mastodon_instance`+`mastodon_id`, `start`/`end`/`location` (event).

### Estensione lato sito

Crea nel tuo `layouts/_partials/`:

- `custom-head.html` — aggiunge roba in `<head>` (il tema ne fornisce già una che
  emette `rel=webmention`/`pingback`; sovrascrivila per estendere);
- `custom-scripts.html` — script a fine `<body>` (analytics self-hosted, webring
  JS, ecc.).

---

## Struttura

```
themes/cyberlavandatea/
├── theme.toml · go.mod · package.json · hugo.toml · LICENSE · README.md
├── archetypes/            default, post, micro, now, photos, event, weeknote
├── assets/
│   ├── css/main.css       Tailwind v4 + @theme (palette) + base + .chroma
│   └── js/                theme.js · main.js · goToTop.js · search.js
├── data/cyberlavandatea/palette.yaml   riferimento palette
├── i18n/                  en.yaml · it.yaml
├── exampleSite/           demo minima
└── layouts/
    ├── baseof · home · list · single · 404 · taxonomy · term
    ├── rss.xml · list.atom.xml · list.json.json
    ├── index.searchindex.json · index.humanstxt.txt · robots.txt
    ├── micro/ photos/ weeknote/ event/ now/ series/ search/
    ├── _markup/            render-link · render-image · render-heading · render-codeblock
    ├── _shortcodes/        toc · embed · toot · xkcd · allpages · 88x31 · buzzword · heart
    └── _partials/          head · header · footer · scripts-* · meta/* · svgs/*
                            postCard · bio · toc · tags · series · micro · comments
                            mastodon · toot · webmention · syndication · bridgy
                            hcard · socialIcons · search-form · search-index
                            cite · share-buttons · inbound-links · 88x31
                            custom-head · helpers/katex
```

## Licenza

MIT — vedi [`LICENSE`](LICENSE).
