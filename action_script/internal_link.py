import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse, urljoin


def get_internal_links_pointing_to_pages(sitemap_url):
    """
    Analizza una sitemap e restituisce un JSON con i link interni che
    puntano a ciascuna pagina web del sito.

    Args:
        sitemap_url (str): L'URL della sitemap del sito (es. "https://example.com/sitemap.xml").

    Returns:
        str: Una stringa JSON con il formato:
             {
                 "pagina_url_1": ["link_referrer_1", "link_referrer_2", ...],
                 "pagina_url_2": ["link_referrer_3", ...],
                 ...
             }
             Restituisce una stringa JSON vuota ({}) in caso di errori critici o assenza di dati.
    """
    site_pages = []
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()  # Solleva un'eccezione per risposte HTTP errate (4xx o 5xx)
        soup = BeautifulSoup(response.content, "xml")
        for loc in soup.find_all("loc"):
            if "post/2" in loc.text:
                site_pages.append(loc.text)
    except requests.exceptions.RequestException as e:
        print(f"Errore nello scaricare o analizzare la sitemap: {e}")
        return json.dumps({})  # Ritorna un JSON vuoto in caso di errore sitemap

    if not site_pages:
        print("Nessuna URL trovata nella sitemap.")
        return json.dumps({})  # Ritorna un JSON vuoto se la sitemap è vuota

    base_url = urlparse(sitemap_url).scheme + "://" + urlparse(sitemap_url).netloc

    # Inizializza il dizionario per memorizzare i link che puntano a ciascuna pagina
    page_referrers = {page: [] for page in site_pages}

    for page_url in site_pages:
        print(f"Analizzando: {page_url}")
        try:
            page_response = requests.get(page_url)
            page_response.raise_for_status()
            page_soup = BeautifulSoup(page_response.content, "html.parser")

            for link in page_soup.find_all("a", href=True):
                href = link.get("href")
                absolute_href = urljoin(page_url, href)
                parsed_absolute_href = urlparse(absolute_href)

                # Controlla se il link è interno al dominio e se è una delle pagine del sito
                if (
                    parsed_absolute_href.netloc == urlparse(base_url).netloc
                    and absolute_href in site_pages
                ):
                    # Aggiunge il page_url (la pagina che contiene il link) all'elenco dei referrer
                    if page_url not in page_referrers[absolute_href]:
                        page_referrers[absolute_href].append(page_url)

        except requests.exceptions.RequestException as e:
            print(f"Errore nello scaricare o analizzare la pagina {page_url}: {e}")
            continue
        except Exception as e:
            print(f"Errore generico durante l'analisi di {page_url}: {e}")
            continue

    return json.dumps(page_referrers, indent=4)


if __name__ == "__main__":
    # Sostituisci con l'URL della sitemap del sito che vuoi analizzare
    sitemap_url_to_analyze = "https://fundor333.com/sitemap.xml"  # Esempio

    print(f"Inizio dell'analisi della sitemap: {sitemap_url_to_analyze}")
    result_json = get_internal_links_pointing_to_pages(sitemap_url_to_analyze)

    print("\n--- Risultato JSON ---")
    print(result_json)

    # Puoi anche salvare il risultato in un file per un uso successivo
    # with open("internal_links.json", "w") as f:
    #     f.write(result_json)
    # print("\nRisultato salvato in internal_links.json")
