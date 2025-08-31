import datetime
import os
import re
import typer
from typing import Annotated
from PIL import Image, ImageDraw, ImageFont


def generate_img(message: str, path: str):
    font_path = "Futura Book font.ttf"  # 👉️ Font .ttf Path
    font_size = 100  # 👉️ Font Size
    img = Image.open("cover.jpg")  # 👉️ Open Image
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
    generate_img(name, f"post/{year}/{title}")


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
    year = str(datetime.datetime.now().year).rjust(4, "0")
    month = str(datetime.datetime.now().month).rjust(2, "0")
    day = str(datetime.datetime.now().day).rjust(2, "0")

    generated = f"{year}/{month}/{day}"
    os.system(f"hugo new now/{generated}/{year}-{month}-{day}.md")
    print(f"Generated {generated}/index.md")


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
