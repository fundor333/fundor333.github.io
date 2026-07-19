# action_script

Script di supporto usati per l'automazione del blog, invocati da `makefile` o dalle GitHub Actions
in `.github/workflows/`.

## send_weeknote_webmentions.py

Legge un post weeknote da `content/weeknotes/{year}/{week}/index.md`, estrae tutti i link markdown
presenti nel corpo dell'articolo e invia una [webmention](https://www.w3.org/TR/webmention/) per
ciascuno di essi, scoprendo automaticamente l'endpoint del sito di destinazione (via header HTTP
`Link` oppure tag `<link>`/`<a rel="webmention">` nella pagina).

I link verso i propri domini (`fundor333.com`, `digitaltearoom.com`, `matteoscarpa.it`, `ko-fi.com`)
vengono sempre esclusi, perché non ha senso inviare una webmention a se stessi (es. la sezione
"My Links" o il link "New post from my blog").

### Uso

```sh
# Nessun parametro -> ultimo weeknote pubblicato
uv run python action_script/send_weeknote_webmentions.py

# Solo l'anno -> tutti i weeknote di quell'anno
uv run python action_script/send_weeknote_webmentions.py 2026

# Anno e settimana -> un weeknote specifico
uv run python action_script/send_weeknote_webmentions.py 2026 29

# --dry-run: mostra gli endpoint trovati senza inviare nulla
uv run python action_script/send_weeknote_webmentions.py --dry-run
```

### Target make equivalenti

```sh
make weeknote_webmentions       # ultimo weeknote
make weeknote_webmentions_year  # tutti i weeknote dell'anno corrente
```

## webmention.py

Interroga [webmention.io](https://webmention.io) per tutte le webmention ricevute dal dominio
`fundor333.com` e le salva come JSON in `data/webmentions/`, un file per pagina target (nome file =
hash MD5 dell'URL) più uno "stats" aggregato (conteggio like/bookmark/mention/repost/reply e lista
commenti con contenuto/autore).

Richiede la variabile d'ambiente `WEBMENTIONS_TOKEN` (il token API di webmention.io).

### Uso

```sh
export WEBMENTIONS_TOKEN="..."
uv run python action_script/webmention.py
```

Eseguito periodicamente da `.github/workflows/cron_webmentions.yml` e `.github/workflows/cron_replay.yml`.

## aniist_run.py

Chiama l'endpoint `https://appletune.fundor333.com/weeklynote/anilist/gen`, che rigenera lato
server le statistiche AniList (anime/manga) usate nei weeknote.

### Uso

```sh
uv run python action_script/aniist_run.py
# oppure
make anime
```

Eseguito da `.github/workflows/cron_anilist.yml`.

## photo_exif.py

Scansiona tutti i post `content/photos/**/index.md`, estrae i metadati EXIF (camera, obiettivo,
apertura, tempo di posa, ISO, lunghezza focale, GPS, ecc.) dalle immagini presenti in ciascuna
cartella e salva il risultato in un `exif.json` accanto all'`index.md`.

### Uso

```sh
uv run python action_script/photo_exif.py

# --dry-run: mostra cosa verrebbe scritto senza salvare i file
uv run python action_script/photo_exif.py --dry-run

# oppure
make photo_exif
```

Eseguito da `.github/workflows/cron_photo.yml`.

## github_issue.py

Cerca su GitHub (`api.github.com/search/issues`) le issue pubbliche che citano `fundor333.com` nel
titolo o nel body (escludendo quelle aperte dallo stesso autore) e salva ciascuna issue trovata come
JSON in `data/github/{issue_id}.json`.

### Uso

```sh
uv run python action_script/github_issue.py
```

Eseguito da `.github/workflows/cron_github_issiue.yml`.

## appletune_run.py

Chiama l'endpoint `http://appletune.fundor333.com/pantalone/genera-spese` per generare lato server
le spese personali. Termina con un'eccezione (facendo fallire la GitHub Action) se la chiamata non
risponde con HTTP 200.

### Uso

```sh
uv run python action_script/appletune_run.py
```

## internal_link.py

Analizza la sitemap del sito (`https://fundor333.com/sitemap.xml`), scarica ogni pagina `post/2*` e
individua i link interni con classe `interlink-script` che puntano da una pagina all'altra,
producendo una mappa JSON `{pagina: [pagine che la linkano]}`. Espone la funzione
`get_internal_links_pointing_to_pages(sitemap_url)`, usabile anche da altri script; se eseguito
direttamente stampa il JSON a schermo (il salvataggio su file è commentato nel codice).

### Uso

```sh
uv run python action_script/internal_link.py
```
