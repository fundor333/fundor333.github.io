import os
import json
import re
import requests
from bs4 import BeautifulSoup

# Cartella dove sono i file JSON
CARTELLA_JSON = "data/syndication"


def estrai_link_fundor333_da_mastodon(mastodon_url):
    match = re.search(r"/@[^/]+/(\d+)", mastodon_url)
    if not match:
        return None
    post_id = match.group(1)

    api_url = f"https://mastodon.social/api/v1/statuses/{post_id}"
    response = requests.get(api_url)
    if response.status_code != 200:
        return None

    status_data = response.json()
    content_html = status_data.get("content", "")

    soup = BeautifulSoup(content_html, "html.parser")
    links = soup.find_all("a", href=True)
    for link in links:
        href = link["href"]
        if "fundor333.com" in href:
            return href

    return None


def aggiorna_json_con_source(cartella):
    for nome_file in os.listdir(cartella):
        if nome_file.endswith(".json"):
            percorso_file = os.path.join(cartella, nome_file)

            with open(percorso_file, encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    print(f"Errore nel file {nome_file}: JSON non valido.")
                    continue

            # Cerca il link Mastodon
            mastodon_url = next(
                (
                    url
                    for url in data.get("syndication", [])
                    if "mastodon.social" in url
                ),
                None,
            )
            if not mastodon_url:
                print(f"{nome_file}: Nessun link Mastodon trovato.")
                continue

            # Estrai il link fundor333.com
            link_fundor = estrai_link_fundor333_da_mastodon(mastodon_url)
            if link_fundor:
                data["source"] = link_fundor
                print(f"{nome_file}: 'source' aggiornato a {link_fundor}")
            else:
                print(
                    f"{nome_file}: Nessun link fundor333.com trovato nel post Mastodon."
                )

            # Sovrascrivi il file JSON con il nuovo valore di "source"
            with open(percorso_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)


# Esecuzione
aggiorna_json_con_source(CARTELLA_JSON)
