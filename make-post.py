import datetime
import os
from os import listdir
from os.path import isfile, join
import random


def post_photo():
    # get the current year as variable
    year = str(datetime.datetime.now().year)
    name = input("Give me the title\n")
    os.system(f"hugo new photos/{year}/{name.replace(' ','-').replace(',','').lower()}/index.md")


def post_redirect():
    # get the current year as variable
    name = input("Give me the title\n")
    os.system(f"hugo new redirect/{name.replace(' ','-').replace(',','').lower()}/index.md")


def post_fc():
    # get the current year as variable
    year = str(datetime.datetime.now().year)
    name = input("Give me the title\n")
    os.system(f"hugo new post/{year}/{name.replace(' ','-').replace(',','').lower()}/index.md")


def micro_fc():
    print("Make a micro")
    name = input("Give me the title\n")
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    generated = f"{year.ljust(4,"0")}/{month.ljust(2,"0")}/{name.replace(' ', '-').replace(',', '').lower()}"

    os.system(f"hugo new micro/{generated}/index.md")
    print(f"Generated {generated}/index.md")


ANSWER = {"post": post_fc, "micro": micro_fc, 'photo': post_photo, 'redirect': post_redirect}


def main_checker():
    text = input("You need a new [post], a new [photo] or a new [micro]\n")  # Python 3
    # text = "post"
    ANSWER.get(text, main_checker)()


if __name__ == "__main__":
    main_checker()
