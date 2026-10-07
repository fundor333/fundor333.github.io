# Struttura e funzionalità del tema

Questo documento descrive **come è composto** il rendering di `fundor333.com`:

1. lo stack dei temi dichiarato in `config/_default/hugo.yaml`;
2. cosa fornisce ciascun componente del tema;
3. cosa aggiunge/sovrascrive lo strato locale in `layouts/` (che ha priorità
   sul tema).

## Stack dei temi

```yaml
# config/_default/hugo.yaml
theme: ["hugo-redirect"]

module:
  imports:
    - path: github.com/fundor333/cyberlavandatea
```

- **`hugo-redirect`** (`themes/hugo-redirect/`, git submodule) — fornisce solo
  la generazione di pagine di redirect a partire dagli `aliases` nel front
  matter. Non è un tema completo, è un componente aggiuntivo.
- **`cyberlavandatea`** — il tema vero e proprio (layout, CSS, JS, feed,
  ricerca, IndieWeb/POSSE, ecc.). Importato come **Hugo Module** (non più come
  git submodule): il codice non vive in questo repository, viene risolto da
  `go.mod`/`go.sum` e scaricato nella cache dei moduli Go al momento della
  build. Sorgente: <https://github.com/fundor333/cyberlavandatea>.

> Regola di risoluzione di Hugo: se un file esiste in `layouts/` **e** nel
> tema, vince quello di `layouts/`.

### Aggiornare il tema

```bash
hugo mod get -u github.com/fundor333/cyberlavandatea   # aggiorna alla HEAD di main
hugo mod tidy                                            # pulisce go.mod/go.sum
```

`Makefile` e `netlify.toml` eseguono già `hugo mod get -u` prima di ogni
build, quindi in produzione il tema segue sempre l'ultimo commit di `main` del
suo repository.

## Documentazione del tema

Il tema `cyberlavandatea` documenta se stesso nel proprio repository — layout,
pipeline CSS/JS (Tailwind v4), palette (6 ruoli semantici, un viola e un
verde), feed, ricerca client-side, tipi di contenuto IndieWeb (`micro`,
`photos`, `weeknote`, `event`, `now`, `series`), microformats2, Webmention,
commenti via Mastodon, syndication/Brid.gy, render hook, shortcode e parametri
di configurazione riconosciuti. Fare riferimento al suo `README.md` per il
dettaglio, invece che duplicarlo qui: essendo un modulo versionato a parte,
qualunque descrizione delle sue funzionalità copiata in questo file
diventerebbe obsoleta al primo aggiornamento del tema.

## Lo strato locale `layouts/`

Quanto resta di override/estensioni locali rispetto al tema:

| File | Funzione |
|------|----------|
| `layouts/_partials/custom-head.html` | Hook incluso da `_partials/head.html` del tema: script di analytics self-hosted (umami, `stats.fundor333.com`), meta di verifica Pinterest, `<link rel="author" href="humans.txt">`. |
| `layouts/_shortcodes/opmlblogroll.html` | Blogroll: legge `https://appletune.fundor333.com/api/blogrollgroup/?format=json` a build time e rende i gruppi come lista di link (`u-bookmark-of`). |
| `layouts/_shortcodes/opmlpodroll.html` | Come sopra, ma per i podcast (`podrollgroup`). |
| `layouts/_shortcodes/recommended.html` | Pagina `/recommended`: legge `https://appletune.fundor333.com/api/media/?format=json&recommended=true` a build time (cache rinnovata una volta al giorno) e rende i media consigliati divisi per tipo (libri, manga, anime, film, serie TV) come griglia di poster con voto, autori, anno e note. Markup `h-review` / `h-cite`. |
| `layouts/_shortcodes/uses.html` | Elenchi di attrezzatura della pagina `/uses`: rende un gruppo di `data/uses.yaml` come kit, card o chip. Vedi [sotto](#lo-shortcode-uses). |

Tutto il resto (header, footer, single/list, feed, ricerca, palette,
microformats, Webmention, commenti Mastodon, syndication, render hook,
shortcode di base) arriva dal modulo `cyberlavandatea`.

## Lo shortcode `uses`

La pagina `/uses` (`content/uses/index.md`) non contiene più liste markdown: i
dati stanno in `data/uses.yaml` e ogni gruppo viene reso con

```go-html-template
{{< uses "canon" >}}
```

I titoli `##`/`###` restano nel markdown, così l'indice della pagina continua a
funzionare; lo shortcode rende solo il blocco sotto il titolo.

### Schema di `data/uses.yaml`

Ogni chiave di primo livello è un gruppo:

```yaml
canon:
  layout: kit             # kit | cards | chips (default: chips)
  image: eos-r5.png       # solo kit: una foto…
  # image: [a.jpg, b.png, c.png]   # …oppure un mosaico (la prima è grande)
  # glyph: "Aa"           # …oppure un pannello tipografico al posto della foto
  # caption: "0O il1"     # riga mono sotto il glyph
  items:
    - name: Canon EOS R5
      kind: Body          # etichetta verde, mono, maiuscola (opzionale)
      url: https://…
      # image: foto.jpg   # solo layout cards
```

Le immagini sono **page resource** del bundle `content/uses/`: vengono
ridimensionate e convertite in webp (900px per la foto principale del kit,
500px per le altre del mosaico, 640px per le card). Un nome di immagine
sbagliato o una chiave di gruppo inesistente fermano la build con `errorf`,
invece di produrre una pagina rotta.

### I tre layout

| Layout | Aspetto | Usato per |
|--------|---------|-----------|
| `kit` | Pannello a sinistra (foto, mosaico o `glyph`) + lista numerata `01`, `02`… a destra, con `kind` allineato a destra. La prima voce è in Audiowide (il "corpo macchina"), le altre sono accessori. Sotto i 40rem il pannello va sopra la lista. | Canon, Fuji, Hardware, Software (VS Code + plugin), Fonts |
| `cards` | Griglia di card con foto 4:3; senza `image` mostra l'iniziale del nome su un alone verde. Tutta la card è il link. | Al momento nessun gruppo: resta disponibile. |
| `chips` | Pillole compatte con `kind` come prefisso. | Gadget fotografico, Gadget |

### Note di implementazione

- **CSS inline, una volta sola per pagina.** Lo `<style>` viene emesso solo
  alla prima chiamata, tramite `.Page.Store` (`uses-css`). Usa solo i token
  del tema (`--c-primary`, `--c-surface`, `--c-border`, `--c-inactive`,
  `--font-display`/`--font-mono`, `--ease-standard`, `--radius-panel`), quindi
  segue la palette se il tema cambia.
- **Neutralizza la prosa del tema.** `.e-content` aggiunge a tutte le liste i
  marker `▸`/`01`, un `padding-left` e `li + li { margin-top }`. Lo shortcode
  li annulla con selettori `ul.uses-* > li` / `ol.uses-list > li`, che hanno la
  stessa specificità del tema e vincono perché lo `<style>` arriva dopo il CSS
  del `<head>`. Se si aggiunge un nuovo layout, va aggiunto anche lì.
- **Helper immagini** come partial inline (`_partials/inline/uses-img.html`),
  privato allo shortcode. Gli SVG non vengono ridimensionati.
- **Hover solo con puntatore fine** (`@media (hover: hover) and (pointer:
  fine)`) e niente transizioni con `prefers-reduced-motion: reduce`.
