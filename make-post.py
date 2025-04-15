import datetime
import os
import re


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


def micro_fc():
    print("Make a micro")
    name = input("Give me the title\n")
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    title = name_cleaning(name)

    generated = f"{year.rjust(4, "0")}/{month.rjust(2, "0")}/{title}"

    os.system(f"hugo new micro/{generated}/index.md")
    print(f"Generated {generated}/index.md")


ANSWER = {
    "post": post_fc,
    "micro": micro_fc,
    "photo": post_photo,
    "redirect": post_redirect,
}


def main_checker():
    text = input("You need a new [post], a new [photo] or a new [micro]\n")  # Python 3
    # text = "post"
    ANSWER.get(text, main_checker)()


if __name__ == "__main__":
    main_checker()
