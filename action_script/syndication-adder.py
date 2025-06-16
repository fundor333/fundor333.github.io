import requests
from bs4 import BeautifulSoup
import os
import re
import yaml
import csv

CARTELLA_POST = "content"
CSV_LOG = "log_feed.csv"
MASTODON_FEED = "https://mastodon.social/users/fundor333.rss"
BSKY_FEED = "https://bsky.app/profile/did:plc:u7piwonv4s27ysugjaa6im2q/rss"  # facoltativo, se disponibile
MEDIUM_FEED = None  # "https://medium.com/feed/@fundor333"


def parse_fediverse_url(url):
    # Mastodon / Akkoma / Pleroma
    match1 = re.match(r"https?://([^/]+)/@([^/]+)/(\d+)", url)
    if match1:
        host, username, post_id = match1.groups()
        return {"host": host, "username": username, "id": post_id}

    # Misskey / Firefish
    match2 = re.match(r"https?://([^/]+)/notes/([a-zA-Z0-9]+)", url)
    if match2:
        host, post_id = match2.groups()
        return {"host": host, "username": None, "id": post_id}

    return None


def process_feed_medium(feed_url, fonte):
    aggiornamenti = []
    resp = requests.get(feed_url)
    soup = BeautifulSoup(resp.content, "xml")

    for item in soup.find_all("item"):
        link_medium = item.find("link").text.strip()
        # Prefer content:encoded, fallback to description
        encoded = item.find("content:encoded")
        descrizione = item.find("description")

        content_html = (
            encoded.text if encoded else (descrizione.text if descrizione else "")
        )
        soup_descr = BeautifulSoup(content_html, "html.parser")
        source_links = [
            a["href"]
            for a in soup_descr.find_all("a", href=True)
            if "fundor333.com" in a["href"]
        ]

        if not source_links:
            continue

        source_url = source_links[0]
        post_path = trova_file_post_da_source(source_url)
        if not post_path:
            continue

        nuovi = aggiungi_syndication_a_post(post_path, [link_medium])
        if nuovi:
            print(f"[✓] Aggiornato {post_path} da {fonte}")
            aggiornamenti.append(
                {
                    "file": post_path,
                    "source": source_url,
                    "syndication": " | ".join(nuovi),
                    "feed": fonte,
                }
            )

    return aggiornamenti


def trova_file_post_da_source(source_url):
    match = re.search(r"https?://[^/]+/(.+?)/?$", source_url)
    if not match:
        return None
    slug_path = match.group(1).rstrip("/")
    percorso_cartella = os.path.join(CARTELLA_POST, slug_path)

    file_index = os.path.join(percorso_cartella, "index.md")
    if os.path.exists(file_index):
        return file_index

    file_slug = os.path.join(CARTELLA_POST, slug_path + ".md")
    if os.path.exists(file_slug):
        return file_slug

    return None


def normalizza_url(url):
    return url.rstrip("/")


def aggiungi_syndication_a_post(percorso_file, nuovi_link):
    with open(percorso_file, encoding="utf-8") as f:
        content = f.read()

    if content.startswith("+++"):
        raise NotImplementedError("Supporto TOML non gestito.")
    elif content.startswith("---"):
        parts = content.split("---")
        if len(parts) < 3:
            print(f"Frontmatter non valido in {percorso_file}")
            return []

        frontmatter = yaml.safe_load(parts[1])
        esistenti = frontmatter.get("syndication", [])
        if isinstance(esistenti, str):
            esistenti = [esistenti]

        esistenti_norm = set(map(normalizza_url, esistenti))
        nuovi_norm = set(map(normalizza_url, nuovi_link))

        da_aggiungere = list(nuovi_norm - esistenti_norm)

        if da_aggiungere:
            # Aggiorna il campo syndication
            frontmatter["syndication"] = sorted(esistenti_norm.union(nuovi_norm))

            # Se troviamo un link Mastodon, estrai info nei meta commenti
            for link in da_aggiungere:
                parsed = parse_fediverse_url(link)
                if parsed:
                    frontmatter["comments"] = (
                        parsed  # Sostituisce se già esiste (puoi estendere a lista se vuoi)
                    )

            nuovo_frontmatter = yaml.dump(
                frontmatter, sort_keys=False, allow_unicode=True
            )
            nuovo_content = f"---\n{nuovo_frontmatter}---{parts[2]}"
            with open(percorso_file, "w", encoding="utf-8") as f:
                f.write(nuovo_content)
            return da_aggiungere
        else:
            return []
    else:
        print(f"Formato frontmatter sconosciuto: {percorso_file}")
        return []


def process_feed(feed_url, fonte):
    aggiornamenti = []

    resp = requests.get(feed_url)
    soup = BeautifulSoup(resp.text, "xml")

    for item in soup.find_all("item"):
        guid = item.find("guid").text.strip()
        content_html = item.find("description").text

        # Cerca link canonico (source) nel contenuto
        soup_descr = BeautifulSoup(content_html, "html.parser")
        source_links = [
            a["href"]
            for a in soup_descr.find_all("a", href=True)
            if "fundor333.com" in a["href"]
        ]

        if not source_links:
            continue

        source_url = source_links[0]
        post_path = trova_file_post_da_source(source_url)
        if not post_path:
            continue

        nuovi = aggiungi_syndication_a_post(post_path, [guid])
        if nuovi:
            print(f"[✓] Aggiornato {post_path} da {fonte}")
            aggiornamenti.append(
                {
                    "file": post_path,
                    "source": source_url,
                    "syndication": " | ".join(nuovi),
                    "feed": fonte,
                }
            )

    return aggiornamenti


def main():
    log = []

    print(">> Processando Mastodon")
    log += process_feed(MASTODON_FEED, "mastodon")

    if BSKY_FEED:
        print(">> Processando Bluesky")
        log += process_feed(BSKY_FEED, "bsky")

    if MEDIUM_FEED:
        print(">> Processando Medium")
        log += process_feed_medium(MEDIUM_FEED, "medium")

    if log:
        with open(CSV_LOG, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["file", "source", "syndication", "feed"]
            )
            writer.writeheader()
            writer.writerows(log)
        print(f"\n[✓] Log salvato in {CSV_LOG}")
    else:
        print("\n[=] Nessuna modifica effettuata.")


if __name__ == "__main__":
    main()
