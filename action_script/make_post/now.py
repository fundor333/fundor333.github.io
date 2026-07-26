import datetime
import os
import re
from pathlib import Path


def get_latest_now_file():
    # Cerca ricorsivamente tutti i file .md nella cartella now
    files = sorted(Path("content/now").rglob("*.md"))
    if not files:
        return None
    # Escludiamo eventuali file temporanei o cartelle, prendiamo quello con year/month/day piu alto.
    # I parametri vengono presi dal path content/now/year/month/day/filename.md
    return files[-2]


def now_fc() -> None:
    print("Make a now")
    now = datetime.datetime.now()
    year = str(now.year).rjust(4, "0")
    month = str(now.month).rjust(2, "0")
    day = str(now.day).rjust(2, "0")

    new_relative_path = f"now/{year}/{month}/{day}/{year}-{month}-{day}.md"
    full_new_path = Path(f"content/{new_relative_path}")

    if full_new_path.exists():
        print(f"Already exists, skipping: {full_new_path}")
        return

    last_file = get_latest_now_file()
    os.system(f"hugo new {new_relative_path}")

    if last_file and full_new_path.exists():
        with Path(last_file).open(encoding="utf-8") as f:
            full_text = f.read()

        # Dividiamo il file usando i delimitatori ---
        # parts[1] sarà il frontmatter, parts[2] sarà il contenuto (body)
        parts = full_text.split("---", 2)

        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]

            # 1. Rimuove blocchi lista per 'comments' e 'syndication'
            frontmatter = re.sub(
                r"^(comments|syndication):(\s*\n(\s+|-).+)*\n?",
                "",
                frontmatter,
                flags=re.MULTILINE,
            )

            # 2. Aggiorna Data
            frontmatter = re.sub(
                r"^date:.*",
                f"date: {now.strftime('%Y-%m-%d')}",
                frontmatter,
                flags=re.MULTILINE,
            )

            # 3. Aggiorna Titolo
            frontmatter = re.sub(
                r"^title:.*",
                f'title: "Now {now.strftime("%Y/%m/%d")}"',
                frontmatter,
                flags=re.MULTILINE,
            )

            # 4. Pulizia righe vuote nel frontmatter
            frontmatter = frontmatter.strip()

            # Ricostruiamo il file mantenendo i delimitatori ---
            new_content = f"---\n{frontmatter}\n---{body}"

            with full_new_path.open("w", encoding="utf-8") as f:
                f.write(new_content)

    print(f"Generato con successo: {full_new_path}")
