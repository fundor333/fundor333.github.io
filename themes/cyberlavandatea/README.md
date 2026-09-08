# CyberLavandaTea

A **dark-only Hugo theme** for dev / code blogs.
**Tailwind CSS v4**, a **6-role palette** (one violet, one green), an
**IndieWeb / POSSE** stack, multiple feeds, client-side search.

- Dark only, by design — there is no light toggle. `assets/js/theme.js` locks
  `class="dark"` before first paint.
- The full layout is written in plain CSS, so the theme renders correctly even
  without Tailwind's content detection; utilities stay available for
  customisation.

## Requirements

| | |
|---|---|
| Hugo | **≥ 0.146** *extended* (new template system: `_partials/`, `_shortcodes/`, `_markup/`) |
| Node | for `@tailwindcss/cli`, used by `css.TailwindCSS` |

```bash
# in your site root
npm install -D @tailwindcss/cli
```

## Install

### As a Hugo Module (recommended)

```bash
hugo mod init github.com/you/your-site      # if you don't have a module yet
```

```toml
# hugo.toml
[module]
  [[module.imports]]
    path = "github.com/fundor333/cyberlavandatea"
```

```bash
hugo mod get -u github.com/fundor333/cyberlavandatea
```

### As a Git submodule

```bash
git submodule add https://github.com/fundor333/cyberlavandatea themes/cyberlavandatea
```

```toml
# hugo.toml
theme = "cyberlavandatea"
```

## Minimal site configuration

Hugo merges `params`, `related`, `services`, `mediaTypes`, `build` from a theme
config. It does **not** merge `outputs`, `outputFormats`, `taxonomies`,
`security`, `markup` — copy this block into your own site config (it is
identical to `exampleSite/hugo.toml`):

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

# Required for css.TailwindCSS (Hugo's exec security policy).
[security]
  [security.exec]
    allow = ['^(dart-)?sass$', '^git$', '^go$', '^node$', '^npx$', '^postcss$', '^tailwindcss$']

# Class-based highlighting (theme palette) and lone images as <figure> + caption.
[markup]
  [markup.highlight]
    noClasses = false
  [markup.goldmark.parser]
    wrapStandAloneImageWithinParagraph = false
```

### Tailwind — class detection (optional)

The theme's layout is plain CSS: **it works with no extra setup**. The Tailwind
utilities used in the templates have a fallback in `main.css`. If you want
Tailwind to generate *every* utility you use in your own content / shortcodes,
enable `hugo_stats.json`:

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

(`main.css` already does `@source "hugo_stats.json"`.) Otherwise add the extra
classes to `assets/css/safelist.txt`, or to an `assets/css/*.css` of your own
that imports `main.css` with your own `@source`.

## Run the demo

```bash
cd themes/cyberlavandatea      # or wherever the theme lives
npm install
npm --prefix exampleSite install
hugo server -s exampleSite --themesDir ../..
```

## Palette

Defined once in [`assets/css/main.css`](assets/css/main.css) inside the Tailwind
`@theme` block, so it is available as utilities (`text-content`, `bg-surface`,
`border-border`, …) **and** as `--color-*` for the partials.

| Role | Tailwind token | Hex | Use |
|---|---|---|---|
| Primary *(violet)* | `--color-primary` | `#9B8CF8` | accent, `:hover`/`:focus`, active nav, focus ring, `blockquote` border, keyword |
| Content | `--color-content` | `#DCDCE4` | body text, headings, `strong`, code text |
| Links *(green)* | `--color-link` | `#74D18C` | unvisited links, strings, added diff |
| Visited | `--color-visited` | `#9E8FBE` | `a:visited` |
| Background | `--color-background` | `#1E1E24` | `body`, navbar, footer |
| Inactive | `--color-inactive` | `#8C8C99` | meta, dates, borders, placeholders, comments |
| *(derived)* Surface | `--color-surface` | `#2D2D33` | `code`/`pre`/`.toc`/`blockquote`/`tr:nth-child(even)` |
| *(derived)* Border | `--color-border` | `#39393F` | `hr`, separators, borders |

Chroma syntax highlighting stays within violet + green plus two tints
(`--color-code-fn` `#A6E0B4`, `--color-code-num` `#C3B8F5`) plus one optional red
for errors (`--color-code-err` `#E1808F`), inside `<pre>` only.

Fonts are loaded from Google Fonts in `_partials/head.html` from `params.fonts`
(`display` = Audiowide, `body` = Rajdhani).

## Features

| Area | Where |
|---|---|
| `baseof` + `main` block, `home`, `list` (by year), `single`, `404`, `taxonomy`, `term` | `layouts/*.html` |
| `<head>`: meta, OG, Twitter, JSON-LD `BlogPosting`, `canonical`, `hreflang`, `rel=first/last/prev/next` | `_partials/head.html`, `_partials/meta/*` |
| Asset pipeline: **Tailwind v4** → `minify` → `fingerprint`+`integrity`; `theme.js` in the head, `main.js`+`goToTop` at the end, `additionalScripts` | `_partials/head.html`, `_partials/scripts-*.html` |
| Nav: `Site.Menus.main` with children and `active` state, CSS-only hamburger, language switcher, "back to top" | `_partials/header.html`, `_partials/footer.html`, `assets/js/goToTop.js` |
| `postCard` with a per-type icon, starred, speaker, `<time datetime>` | `_partials/postCard.html`, `_partials/type-icon.html` |
| Bio + **h-card** (pronouns, nickname, location) | `_partials/bio.html`, `_partials/hcard.html` |
| i18n | `i18n/en.yaml`, `i18n/it.yaml` |
| Feeds: RSS (`exclude_from_rss`, `summary`/`full`, `media` namespace), **Atom** (`feedUUID`, `webfeeds`), **JSON Feed 1.1**, **humans.txt**, dynamic **robots.txt** | `layouts/rss.xml`, `list.atom.xml`, `list.json.json`, `index.humanstxt.txt`, `robots.txt` |
| Search: `SearchIndex` output → `/search.json`, `/search` section, `?q=` form, **Lunr** index, `<template>` rendering | `layouts/index.searchindex.json`, `layouts/search/list.html`, `_partials/search-*.html`, `assets/js/search.js` |
| Content types: `micro`, `photos` (EXIF from `exif.json` or `.Exif`), `weeknote`, `event` (`start`/`end`/`location`), `now`, `series` | `layouts/<type>/…` |
| Microformats2: `h-entry` / `e-content` / `u-photo` / `p-category` / `dt-published`; response types reply/repost/like/bookmark/rsvp | `layouts/single.html`, `_partials/micro.html` |
| Favicons entirely from config (`favicon`, `faviconSvg`, `appleTouchIcon`, `icon96`, `webmanifest`, `maskIcon`) | `_partials/favicons.html` |
| **Webmention**: `rel=webmention`/`pingback` + the webmention.io client rendering a reactions facepile and inline comments into `#webmentions` (styled) | `_partials/webmention.html`, `_partials/custom-head.html`, `assets/css/main.css` |
| **Mastodon comments** (fetch `/context` + DOMPurify) + build-time toot embed | `_partials/mastodon.html`, `_partials/toot.html` |
| **Brid.gy Publish** with configurable targets + UTM | `_partials/bridgy.html` |
| **Syndication** ("also posted on") | `_partials/syndication.html` |
| Render hooks: link (UTM + `target=_blank` + `↗`), image (`figure` + `u-photo`), heading (anchor), codeblock (`HighlightCodeBlock`) | `layouts/_markup/render-*.html` |
| Shortcodes: `toc`, `embed`, `toot`, `xkcd`, `allpages`, `88x31`, `buzzword`, `heart` | `layouts/_shortcodes/*` |
| Content-type icons ("category") with Font Awesome (Kit or free CDN), `params.postIcons` override | `_partials/fontawesome.html`, `_partials/type-icon.html`, `_partials/postCard.html` |
| **LGBTQ+ corner** (pride.codes, top-right), opt-in `params.prideCorner` (default `false`) | `_partials/pride-corner.html` |
| Small-web extras: **88×31** badges (folder + JSON, shuffled), **webring** (`webring.html`: icon / prev-next / web component), "cite this post" (copy URL), "written by a human", **backlinks** (`findRE`), **related** ("See Also") | `_partials/88x31.html`, `_partials/webring.html`, `_partials/cite.html`, `_partials/inbound-links.html`, `_partials/comments.html`, `footer.html` |
| Palette / theming: 6 roles + surfaces derived by opacity, Chroma within violet/green | `assets/css/main.css` |

KaTeX (conditional, `_partials/helpers/katex.html`) and Google Analytics
(`hugo.IsProduction` + `site.GoogleAnalytics`) are wired up too.

## Params

```toml
[params]
  description       = "…"           # fallback meta description
  dateFormat        = "2 January 2006"
  homeRecentCount   = 20            # posts on the home page
  mainSections      = ["post"]
  secondarysections = ["micro"]     # "Recent updates" list on the home page
  feedSections      = ["post", "micro", "photos", "weeknote"]
  commentSections   = ["post", "micro", "photos", "weeknote"]
  suggestionSections= ["post"]      # "See Also" block (Related)
  toc = true
  tocOpen = false
  goToTop = true
  linkUTM = false                   # UTM on external links (render hook)
  writtenByHuman = true
  shareButtons = true
  cite = true
  badges88x31 = true
  additionalScripts = []            # extra JS assets, bundled + minified
  themeColor = "#1e1e24"
  feedUUID = ""                     # urn:uuid for the Atom feed
  images = ["/img/og.png"]          # fallback og:image
  prideCorner = false               # pride.codes corner top-right (opt-in)

  # Favicons — used verbatim as URLs (relURL). Nothing set -> the theme's
  # bundled /favicon.svg only.
  favicon        = "/favicon.ico"
  faviconSvg     = "/favicon.svg"
  appleTouchIcon = "/apple-touch-icon.png"
  icon96         = "/favicon-96x96.png"
  webmanifest    = "/site.webmanifest"
  maskIcon       = ""               # Safari pinned-tab mono SVG (optional)
  icon           = "/favicon-196x196.png"   # generic icon, also used by the feeds

  [params.fontawesome]              # content-type icons
    kit = ""                         # a Kit URL (Pro too); empty = free CDN
    version = "6.7.2"                # free CDN version
    disable = false                  # true = no Font Awesome

  # FA icon per "category" (= section type). Sensible defaults included;
  # override only the entries you want to change.
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
    fediverseAccount = "@user@instance"

  [params.hcard]
    fullName = "" ; nickname = "" ; avatar = "img/logo.png"
    showLocation = true ; city = "" ; region = "" ; country = ""
    [params.hcard.pronouns]
      nominative = "" ; oblique = "" ; possessive = ""

  [params.webmention]
    targetDomain = "example.com"     # canonical domain (host swap, scheme kept)
    script       = ""                # client script (default: webmention.io hosted)
    wordcount    = 40                # data-wordcount for inline comments
    # endpoint / pingback also read by _partials/custom-head.html
    # Renders the reactions facepile + comments into #webmentions, and emits
    # <link rel="webmention"> / <link rel="pingback">.

  bridgy = ["mastodon", "bluesky"]

  [[params.socialIcons]]
    name = "github" ; url = "https://github.com/user"

  # Footer webring(s) (partial webring.html). Each entry:
  #   name, url            plain link
  #   + icon               icon link (30x30 img)
  #   + prev / next        renders  <- name ->
  #   + html [+ script]    raw markup (web component) and a defer script
  [[params.webrings]]
    name = "XXIIVV webring" ; url = "https://webring.xxiivv.com/#86"
    icon = "https://webring.xxiivv.com/icon.white.svg"
```

### Recognised front matter

`description`, `image`, `tags`, `categories`, `series`, `themes`, `group`,
`isStarred`, `speaker`, `math`, `toc`, `tocOpen`, `exclude_from_rss`,
`exclude_from_search`, `robotsdisallow`, `allpage`, `feature_link`/`feature_text`,
`syndication` (list of URLs), `comments` (`{host, user, id}` for Mastodon
comments), `reply`/`repost`/`like`/`bookmark`/`rsvp`/`preview_text_from_reply`,
`mastodon_instance`+`mastodon_id`, `start`/`end`/`location` (event).

### Site-side extension

Create these in your own `layouts/_partials/`:

- `custom-head.html` — adds to `<head>` (the theme ships one that emits
  `rel=webmention`/`pingback`; override to extend);
- `custom-scripts.html` — end-of-`<body>` scripts (self-hosted analytics, extra
  widgets, …).

## Structure

```
themes/cyberlavandatea/
├── theme.toml · go.mod · package.json · hugo.toml · LICENSE · README.md
│   CHANGELOG.md · CONTRIBUTING.md · .editorconfig · .gitattributes · netlify.toml
├── .github/workflows/ci.yml
├── archetypes/            default, post, micro, now, photos, event, weeknote
├── assets/
│   ├── css/main.css       Tailwind v4 + @theme (palette) + base + .chroma
│   │   safelist.txt
│   └── js/                theme.js · main.js · goToTop.js · search.js
├── data/cyberlavandatea/palette.yaml   palette reference
├── i18n/                  en.yaml · it.yaml
├── exampleSite/           minimal demo (its own hugo.toml + go.mod)
└── layouts/
    ├── baseof · home · list · single · 404 · taxonomy · term
    ├── rss.xml · list.atom.xml · list.json.json
    ├── index.searchindex.json · index.humanstxt.txt · robots.txt
    ├── micro/ photos/ weeknote/ event/ now/ series/ search/
    ├── _markup/            render-link · render-image · render-heading · render-codeblock
    ├── _shortcodes/        toc · embed · toot · xkcd · allpages · 88x31 · buzzword · heart
    └── _partials/          head · header · footer · scripts-* · meta/* · svgs/*
                            postCard · type-icon · fontawesome · bio · toc · tags
                            series · micro · comments · mastodon · toot · webmention
                            syndication · bridgy · hcard · socialIcons · webring
                            search-form · search-index · cite · share-buttons
                            inbound-links · 88x31 · pride-corner · custom-head
                            helpers/katex
```

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Changes are tracked in
[`CHANGELOG.md`](CHANGELOG.md).

## License

MIT — see [`LICENSE`](LICENSE).
