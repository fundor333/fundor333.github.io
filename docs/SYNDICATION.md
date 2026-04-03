# Syndication CLI Guide

CLI per gestire la syndication di contenuti dai social media al blog Hugo.

## Installazione

```bash
# Attiva il virtual environment
source .venv/bin/activate

# Installa le dipendenze
pip install -r requirements.txt
```

## Configurazione

Il file di configurazione si trova in `config/syndication.yaml`:

```yaml
site:
  domain: "https://fundor333.com"
  content_dir: "content"

feeds:
  mastodon: "https://mastodon.social/users/fundor333.rss"
  bluesky: "https://bsky.app/profile/did:plc:u7piwonv4s27ysugjaa6im2q/rss"
  medium: null
  indieweb:
    - url: "https://granary.io/url?input=html&output=atom&url=https://news.indieweb.org/en"
      site: "https://news.indieweb.org/en"

external:
  hacker_news:
    username: "fundor333"
    enabled: true

paths:
  syndication_dir: "data/syndication"
  log_file: "log_feed.csv"

options:
  dry_run: false
  verbose: false
```

### Opzioni di Configurazione

| Sezione | Campo | Descrizione |
|---------|-------|-------------|
| `site` | `domain` | Dominio del sito |
| `site` | `content_dir` | Cartella dei contenuti Hugo |
| `feeds` | `mastodon` | URL feed RSS Mastodon |
| `feeds` | `bluesky` | URL feed RSS Bluesky |
| `feeds` | `medium` | URL feed Medium (null per disabilitare) |
| `feeds` | `indieweb` | Lista di feed IndieWeb |
| `external.hacker_news` | `username` | Username Hacker News |
| `external.hacker_news` | `enabled` | Abilita raccolta HN |
| `paths` | `syndication_dir` | Cartella per file JSON |
| `paths` | `log_file` | File log CSV |
| `options` | `dry_run` | Modalità simulazione |
| `options` | `verbose` | Output dettagliato |

## Comandi

### collect-cmd

Raccoglie i link di syndication dai feed RSS e genera i file JSON.

```bash
python -m syndication_cli collect-cmd [OPTIONS]
```

**Opzioni:**
- `-c, --config PATH` - Percorso file configurazione (default: config/syndication.yaml)
- `--dry-run` - Modalità simulazione
- `-v, --verbose` - Output dettagliato

**Esempio:**
```bash
python -m syndication_cli collect-cmd --verbose
```

### add-cmd

Legge i file JSON e i feed RSS, aggiunge i link di syndication ai post Markdown.

```bash
python -m syndication_cli add-cmd [OPTIONS]
```

**Opzioni:**
- `-c, --config PATH` - Percorso file configurazione
- `--dry-run` - Modalità simulazione
- `-v, --verbose` - Output dettagliato

**Esempio:**
```bash
python -m syndication_cli add-cmd --dry-run
```

### correct-cmd

Correggere i file JSON mancanti del campo "source" usando l'API Mastodon.

```bash
python -m syndication_cli correct-cmd [OPTIONS]
```

**Opzioni:**
- `-c, --config PATH` - Percorso file configurazione
- `--dry-run` - Modalità simulazione
- `-v, --verbose` - Output dettagliato

**Esempio:**
```bash
python -m syndication_cli correct-cmd --verbose
```

### replay-cmd

Elabora i link di risposta nei post e genera le anteprime del contenuto.

```bash
python -m syndication_cli replay-cmd [OPTIONS]
```

**Funzionalità:**
- Estrae preview dal contenuto linked
- Aggiunge flag `mastodon_reply` per link Mastodon
- Popola `mastodon_instance` e `mastodon_id`
- Gestisce `preview_text_from_reply` nel frontmatter

**Opzioni:**
- `-c, --config PATH` - Percorso file configurazione
- `--dry-run` - Modalità simulazione
- `-v, --verbose` - Output dettagliato

**Esempio:**
```bash
python -m syndication_cli replay-cmd --verbose
```

### all-cmd

Esegue tutti i comandi in sequenza: collect → add → correct → replay.

```bash
python -m syndication_cli all-cmd [OPTIONS]
```

**Opzioni:**
- `-c, --config PATH` - Percorso file configurazione
- `--dry-run` - Modalità simulazione
- `-v, --verbose` - Output dettagliato

**Esempio:**
```bash
python -m syndication_cli all-cmd --verbose
```

## Workflow GitHub Actions

### cron_webmentions.yml

Esegue syndication ogni 10 ore.

```yaml
- name: Fetch Syndication
  run: python -m syndication_cli all-cmd
```

### cron_replay.yml

Elabora i reply periodicamente.

```yaml
- name: Fetch Replay
  run: python -m syndication_cli replay-cmd
```

## Struttura Output

### File JSON (data/syndication/)

```json
{
  "source": "https://fundor333.com/post/my-post/",
  "syndication": [
    "https://mastodon.social/@fundor333/1234567890",
    "https://bsky.app/profile/..."
  ]
}
```

### Frontmatter Post

```yaml
---
title: "My Post"
syndication:
  - https://mastodon.social/@fundor333/1234567890
  - https://bsky.app/profile/...
comments:
  host: "mastodon.social"
  username: "fundor333"
  id: "1234567890"
---
```

## Flag Dry Run

Quando `--dry-run` è attivo:
- Nessun file viene modificato
- I log mostrano cosa verrebbe fatto
- Utile per testare le modifiche

## Risoluzione Problemi

### Errore "Config file not found"

Verifica che `config/syndication.yaml` esista.

### Errore "No module named 'yaml'"

Attiva il virtual environment:
```bash
source .venv/bin/activate
```

### Feed non funzionanti

Verifica che gli URL dei feed siano corretti nel file di configurazione.

### Preview non estratte

Alcuni siti bloccano l'accesso. Usa `--verbose` per vedere i dettagli.
