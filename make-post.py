import datetime
import os
import re
import typer
from typing import Annotated
from PIL import Image, ImageDraw, ImageFont
import glob


def get_latest_now_file():
    # Cerca ricorsivamente tutti i file .md nella cartella now
    files = glob.glob("content/now/**/*.md", recursive=True)
    if not files:
        return None
    # Escludiamo eventuali file temporanei o cartelle, prendiamo il più recente
    return max(files, key=os.path.getmtime)


def generate_img(message: str, path: str, image_name: str = "cover.jpg"):
    font_path = "Futura Book font.ttf"  # 👉️ Font .ttf Path
    font_size = 100  # 👉️ Font Size
    img = Image.open(image_name)  # 👉️ Open Image
    dr = ImageDraw.Draw(img)  # 👉️ Create New Image
    my_font = ImageFont.truetype(font_path, font_size)  # 👉️ Initialize Font
    text_x = (img.width) // 2
    text_y = (img.height) // 2
    dr.text((text_x, text_y), message, font=my_font, fill=(255, 255, 255), anchor="mm")
    print("Generated content/" + path + "/cover.png")
    img.save("content/" + path + "/cover.png")


def name_cleaning(name: str) -> str:

    title = re.sub("[^A-Za-z0-9 ]+", " ", name)
    title = title.replace("  ", " ")
    title = title.replace(" ", "-")
    title = title.lower()
    return title


def post_photo():
    # get the current year as variable
    year = str(datetime.datetime.now().year)
    name = input("Give me the title\n")
    title = name_cleaning(name)
    os.system(f"hugo new photos/{year}/{title}/index.md")
    generate_img(name, f"photos/{year}/{title}")


def post_redirect():
    # get the current year as variable
    name = input("Give me the title\n")
    title = name_cleaning(name)
    os.system(f"hugo new redirect/{title}/index.md")


def post_fc():
    # get the current year as variable
    year = str(datetime.datetime.now().year)
    name = input("Give me the title\n")
    title = name_cleaning(name)
    os.system(f"hugo new post/{year}/{title}/index.md")
    generate_img(name, f"post/{year}/{title}")


def notebook_fc():
    # get the current year as variable
    year = str(datetime.datetime.now().year)
    name = input("Give me the title\n")
    title = name_cleaning(name)
    os.system(f"hugo_nbnew ./content/post/{year}/{title}")
    generate_img(name, f"post/{year}/{title}", "alternative_cover.jpg")
    with open(f"notescript/{title}.sh", "w") as rsh:
        rsh.write("""\
    #! /bin/bash
    uv run hugo_nbconvert content/post/""" + f"{year}/{title}/index.ipynb")
    os.system(f"chmod +x  notescript/{title}.sh")


def micro_fc():
    print("Make a micro")
    name = input("Give me the title\n")
    year = str(datetime.datetime.now().year).rjust(4, "0")
    month = str(datetime.datetime.now().month).rjust(2, "0")
    title = name_cleaning(name)

    generated = f"{year}/{month}/{title}"
    os.system(f"hugo new micro/{generated}/index.md")
    print(f"Generated {generated}/index.md")


def weeklycover():
    print("Make a weekly cover")
    today = datetime.datetime.now()
    year = today.strftime("%Y")
    week = str(int(today.strftime("%W")) + 1)
    file_string = f"Week Note Nº {week}/{year}"
    generate_img(file_string, f"weeknotes/{year}/{week}")


def now_fc():
    print("Make a now")
    now = datetime.datetime.now()
    year = str(now.year).rjust(4, "0")
    month = str(now.month).rjust(2, "0")
    day = str(now.day).rjust(2, "0")

    last_file = get_latest_now_file()
    new_relative_path = f"now/{year}/{month}/{day}/{year}-{month}-{day}.md"
    os.system(f"hugo new {new_relative_path}")

    full_new_path = f"content/{new_relative_path}"

    if last_file and os.path.exists(full_new_path):
        with open(last_file, encoding="utf-8") as f:
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
                f'date: {now.strftime("%Y-%m-%d")}',
                frontmatter,
                flags=re.MULTILINE,
            )

            # 3. Aggiorna Titolo
            frontmatter = re.sub(
                r"^title:.*",
                f'title: "Now {now.strftime("%d/%m/%Y")}"',
                frontmatter,
                flags=re.MULTILINE,
            )

            # 4. Pulizia righe vuote nel frontmatter
            frontmatter = frontmatter.strip()

            # Ricostruiamo il file mantenendo i delimitatori ---
            new_content = f"---\n{frontmatter}\n---{body}"

            with open(full_new_path, "w", encoding="utf-8") as f:
                f.write(new_content)

    print(f"Generato con successo: {full_new_path}")


ANSWER = {
    "post": post_fc,
    "micro": micro_fc,
    "photo": post_photo,
    "redirect": post_redirect,
    "weekly_cover": weeklycover,
    "now": now_fc,
    "notebook": notebook_fc,
}


def main_checker():
    text = input("You need a new [post], a new [photo] or a new [micro]\n")  # Python 3
    # text = "post"
    ANSWER.get(text, main_checker)()


def main(text: Annotated[str, typer.Argument()] = None):
    if text is None:
        text = input(
            "You need a new [post], a new [photo], a new [micro], a [weekly_cover] or [now]\n"
        )
    ANSWER.get(text, main)()


if __name__ == "__main__":
    typer.run(main)
