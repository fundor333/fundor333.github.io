# Tema CyberLavandaTea

Tema Hugo **dedicato e a sé stante** in
[`themes/cyberlavandatea/`](../themes/cyberlavandatea/), creato a partire da:

- [`docs/THEME.md`](THEME.md) — elenco funzioni (Parti 1–3) e **Parte 4**
  (palette a 6 ruoli: un viola + un verde, verifica WCAG, mapping Chroma);
- [`docs/palette-preview.html`](palette-preview.html) — mockup di riferimento con
  i font reali (Audiowide / Rajdhani).

Documentazione completa: [`themes/cyberlavandatea/README.md`](../themes/cyberlavandatea/README.md).

## In breve

| | |
|---|---|
| CSS | **Tailwind v4** via `css.TailwindCSS`. Palette definita una volta in `assets/css/main.css` (`@theme` + `@layer`). Layout in CSS puro, quindi il tema è corretto anche senza content-detection; le utility restano per chi personalizza. |
| Tema | **dark-only** (nessun toggle) — `docs/THEME.md` §4. |
| Palette | Primary `#9B8CF8` · Content `#DCDCE4` · Links `#74D18C` · Visited `#9E8FBE` · Background `#1E1E24` · Inactive `#8C8C99` (+ Surface `#2D2D33`, Border `#39393F`). |
| Funzioni | baseof/home/list/single/404/taxonomy/term · `<head>` con OG/Twitter/JSON-LD/canonical/hreflang/pagination · RSS + Atom + JSON Feed + humans.txt + robots.txt · ricerca Lunr (`SearchIndex` → `/search.json`) · tipi `micro`/`photos`(EXIF)/`weeknote`/`event`/`now`/`series` · Microformats2 + Webmention + commenti Mastodon + Brid.gy + syndication · render hook (link UTM, immagini, heading, codeblock) · shortcode `toc`/`embed`/`toot`/`xkcd`/`allpages`/`88x31`/`buzzword`/`heart` · badge 88×31, webring, "cita", "scritto da umano", backlink, related. |

## Provare la demo

```bash
cd themes/cyberlavandatea
npm install
npm --prefix exampleSite install
hugo server -s exampleSite --themesDir ../..
```

## Usarlo su questo sito (fundor333.com)

Non è attivo. Per attivarlo, in `config/_default/hugo.yaml`:

```yaml
theme: ["hugo-redirect", "cyberlavandatea"]
```

e aggiungere al config del sito il blocco **non ereditabile dal tema** (outputs,
outputFormats, mediaTypes, taxonomies, security per Tailwind): vedi
`themes/cyberlavandatea/exampleSite/hugo.toml` → sezione commentata, e il README
del tema → "Configurazione minima del sito".
