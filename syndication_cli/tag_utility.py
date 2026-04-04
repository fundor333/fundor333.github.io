import re
from pathlib import Path

import ollama


def genera_tag_seo(testo_input, numero=10):
    # Definizione del prompt per istruire il modello
    prompt = f"""
    Analizza il seguente testo e restituisci un elenco di {numero} tag SEO (parole chiave).
    I tag devono essere rilevanti, ottimizzati per la ricerca e separati da virgole.
    Restituisci solo i tag, senza introduzioni o spiegazioni.

    Testo: {testo_input}
    """

    try:
        response = ollama.generate(model="llama3", prompt=prompt)

        return response["response"].strip()

    except Exception as e:
        return f"Errore durante la generazione: {e}"


def extract_clean_text(filepath):
    try:
        with Path(filepath).open("r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return "Errore: File non trovato."

    content = re.sub(r"^---.*?---", "", content, flags=re.DOTALL)
    content = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    content = re.sub(r"\{\{.*?\}\}", "", content, flags=re.DOTALL)
    content = re.sub(r"!\[.*?\]\(.*?\)", "", content)
    content = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", content)
    content = re.sub(r"<.*?>", "", content)

    lines = [line.strip() for line in content.splitlines() if line.strip()]
    return "\n".join(lines)
