import os
import re
import requests
import frontmatter
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# --- Funzioni di Supporto ---

HUGO_CONTENT_PATH = "content"
MAX_LENGHT = 800


def get_instance_and_id(url):
    """
    Estrae l'istanza (hostname) e un potenziale ID da un URL,
    basandosi su pattern comuni di Mastodon.

    Args:
        url (str): La stringa URL da analizzare.

    Returns:
        tuple: Una tupla contenente (istanza, id).
               Restituisce (None, None) se l'URL non è ben formato
               o se non è possibile estrarre un'istanza.
    """
    parsed_url = urlparse(url)

    instance = parsed_url.netloc if parsed_url.netloc else None

    if not instance:
        return None, None

    path_segments = parsed_url.path.strip("/").split("/")

    # Logica per trovare l'ID basandosi sui pattern di Mastodon
    if len(path_segments) >= 2 and path_segments[0].startswith("@"):
        if len(path_segments) == 2:
            if path_segments[1].isdigit():
                return instance, path_segments[1]
            else:
                return instance, path_segments[0]
        elif (
            len(path_segments) > 2
            and path_segments[1] == "statuses"
            and path_segments[2].isdigit()
        ):
            return instance, path_segments[2]
        elif len(path_segments) > 2 and path_segments[2].isdigit():
            return instance, path_segments[2]

    elif (
        len(path_segments) >= 3
        and path_segments[0] == "web"
        and path_segments[1] == "statuses"
        and path_segments[2].isdigit()
    ):
        return instance, path_segments[2]

    elif (
        len(path_segments) >= 4
        and path_segments[0] == "users"
        and path_segments[2] == "statuses"
        and path_segments[3].isdigit()
    ):
        return instance, path_segments[3]

    if path_segments:
        if path_segments[-1].isdigit():
            return instance, path_segments[-1]
        elif path_segments[0].startswith("@") and len(path_segments) == 1:
            return instance, path_segments[0]

    return instance, None  # Nessun ID specifico trovato per URL di base o generici


def get_page_content(url):
    """
    Recupera il contenuto HTML di una pagina web dato il suo URL.
    Gestisce errori di rete e timeout.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Errore nel recupero dell'URL {url}: {e}")
        return None


def extract_preview_from_html(html_content, max_length=MAX_LENGHT):
    """
    Estrae una porzione di testo pulita dal contenuto HTML per una preview.
    Prioritizza l'estrazione da:
    1. Primo elemento con classe 'e-content'.
    2. Se 'e-content' manca, il primo elemento con classe 'p-summary'.
    Se entrambi mancano, restituisce una stringa vuota.
    Rimuove il markup HTML, gli script e gli stili in modo robusto.
    """
    if not html_content:
        return ""

    soup = BeautifulSoup(html_content, "html.parser")

    # Rimuove tutti i tag <script> e <style>
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()

    text = ""

    # 1. Cerca il primo elemento con la classe 'e-content'
    e_content_element = soup.find(class_="e-content")

    if e_content_element:
        text = e_content_element.get_text()
    else:
        # 2. Se 'e-content' manca, cerca il primo elemento con la classe 'p-summary'
        p_summary_element = soup.find(class_="p-summary")
        if p_summary_element:
            text = p_summary_element.get_text()
        # 3. Se entrambi mancano, 'text' rimane una stringa vuota

    text = re.sub(r"\s+", " ", text).strip()

    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def is_mastodon_link(url):
    """
    Checks if a given URL is a Mastodon link.

    Args:
        url: The URL string to check.

    Returns:
        True if the URL is a Mastodon link, False otherwise.
    """
    # Regular expression to match common Mastodon URL patterns.
    # This includes:
    # - https:// or http://
    # - A domain name (e.g., example.social, mastodon.online)
    # - Optional port number (:port)
    # - Optional path components, including user profiles (@user or /@user)
    # - Handles various subdomains and TLDs.
    mastodon_pattern = re.compile(
        r"^(https?://)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(:\d{1,5})?(/.*)?$"
    )

    # Some common Mastodon instance keywords or patterns in the domain
    # This is a heuristic and might not catch all Mastodon instances,
    # but covers many common ones.
    mastodon_keywords = [
        "mastodon",
        "masto",
        "social",
        "toot",
        "floss.social",
        "fosstodon",
        "pleroma.social",  # Pleroma is compatible and often hosted similarly
        # Add more specific instance names if known
    ]

    # Check for the presence of '@' in the path, which is common for user profiles
    # (e.g., https://mastodon.social/@username)
    if "@" in url:
        return True

    # Check if the URL matches the general pattern
    if mastodon_pattern.match(url):
        # Further refine by checking for common Mastodon keywords in the hostname
        from urllib.parse import urlparse

        parsed_url = urlparse(url)
        hostname = parsed_url.hostname.lower()

        for keyword in mastodon_keywords:
            if keyword in hostname:
                return True

    return False


# --- Funzione Principale ---


def process_hugo_markdown_files(root_dir):
    """
    Scorre ricorsivamente i file Markdown di un sito Hugo.
    Trova i campi 'reply' nel front matter, genera una preview
    dal contenuto della pagina collegata e aggiunge un flag Mastodon se applicabile.
    """
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith((".md", ".markdown")):
                filepath = os.path.join(dirpath, filename)
                print(f"Elaborazione del file: {filepath}")

                modified = False  # Flag per sapere se il file è stato modificato e deve essere salvato

                try:
                    with open(filepath, encoding="utf-8") as f:
                        post = frontmatter.load(f)

                    if "reply" in post.metadata and post.metadata["reply"]:
                        reply_url = post.metadata["reply"]
                        print(f"  Trovata URL di risposta: {reply_url}")

                        # --- Rilevamento Mastodon ---
                        if is_mastodon_link(reply_url):
                            if post.metadata.get("mastodon_reply") is not True:
                                post.metadata["mastodon_reply"] = True
                                (
                                    post.metadata["mastodon_instance"],
                                    post.metadata["mastodon_id"],
                                ) = get_instance_and_id(reply_url)
                                modified = True
                                print(
                                    f"  Flag 'mastodon_reply: true' aggiunto/aggiornato per {reply_url}"
                                )
                        elif post.metadata.get("mastodon_reply") is True:
                            # Se non è più un link Mastodon ma il flag era presente, rimuovilo
                            del post.metadata["mastodon_reply"]
                            del post.metadata["mastodon_instance"]
                            del post.metadata["mastodon_id"]
                            modified = True
                            print(
                                f"  Flag 'mastodon_reply' rimosso per {reply_url} (non più Mastodon)."
                            )
                        # --- Fine Rilevamento Mastodon ---

                        html_content = get_page_content(reply_url)
                        if html_content:
                            preview_text = extract_preview_from_html(html_content)

                            if preview_text:
                                # Aggiunge o aggiorna il campo 'preview_text_from_reply'
                                if (
                                    post.metadata.get("preview_text_from_reply")
                                    != preview_text
                                ):
                                    post.metadata["preview_text_from_reply"] = (
                                        preview_text
                                    )
                                    modified = True
                                    print(
                                        f"  Preview generata/aggiornata: {preview_text}"
                                    )
                            else:
                                # Se la preview è vuota e il campo esisteva, rimuovilo
                                if "preview_text_from_reply" in post.metadata:
                                    del post.metadata["preview_text_from_reply"]
                                    modified = True
                                    print(
                                        f"  Nessun contenuto valido. Rimosso il campo preview da {filename}."
                                    )
                                else:
                                    print(
                                        f"  Nessun contenuto valido da estrarre per {reply_url}. Nessun campo preview aggiunto."
                                    )
                        else:
                            # Se impossibile recuperare, rimuovi la preview se esisteva
                            if "preview_text_from_reply" in post.metadata:
                                del post.metadata["preview_text_from_reply"]
                                modified = True
                                print(
                                    f"  Impossibile recuperare il contenuto per {reply_url}."
                                    + " Rimosso il campo preview da {filename}."
                                )
                            else:
                                print(
                                    f"  Impossibile recuperare il contenuto per {reply_url}. Nessun campo preview presente."
                                )
                    else:
                        print("  Nessun campo 'reply' trovato o è vuoto.")
                        # Se il campo 'reply' non c'è, assicurati che i campi di preview e mastodon_reply siano rimossi
                        if "preview_text_from_reply" in post.metadata:
                            del post.metadata["preview_text_from_reply"]
                            modified = True
                            print(
                                f"  Campo 'reply' mancante. Rimosso il campo preview da {filename}."
                            )
                        if "mastodon_reply" in post.metadata:
                            del post.metadata["mastodon_reply"]
                            modified = True
                            print(
                                f"  Campo 'reply' mancante. Rimosso il flag Mastodon da {filename}."
                            )

                    # Salva il file SOLO se sono state apportate modifiche
                    if modified:
                        with open(filepath, "wb") as f_write:
                            frontmatter.dump(post, f_write)
                        print(f"  File {filename} salvato con le modifiche.")

                except Exception as e:
                    print(f"Errore durante l'elaborazione del file {filepath}: {e}")


# --- Configurazione e Esecuzione ---


if __name__ == "__main__":
    if not os.path.isdir(HUGO_CONTENT_PATH):
        print(f"Errore: La cartella {HUGO_CONTENT_PATH} non esiste.")
        print(
            "Assicurati di impostare il percorso corretto alla cartella 'content' del tuo sito Hugo."
        )
    else:
        print(
            "Avvio del processo di generazione delle preview e rilevamento Mastodon..."
        )
        process_hugo_markdown_files(HUGO_CONTENT_PATH)
        print("Processo completato.")
