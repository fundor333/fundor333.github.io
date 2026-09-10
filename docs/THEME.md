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

Tutto il resto (header, footer, single/list, feed, ricerca, palette,
microformats, Webmention, commenti Mastodon, syndication, render hook,
shortcode di base) arriva dal modulo `cyberlavandatea`.
