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


def quiet_fc():
    print("Make a quiet")
    onlyfiles = [f for f in listdir("content/quiet") if isfile(join("content/quiet", f))]
    numbs = []
    for e in onlyfiles:
        s = filter(str.isdigit, e)
        s = "".join(s)
        if s:
            numbs.append(int(s))
    generated = max(numbs) + random.randint(151, 839)
    os.system(f"hugo new quiet/{generated}.md")
    print(f"Generated {generated}.md")


ANSWER = {"post": post_fc, "quiet": quiet_fc, 'photo': post_photo, 'redirect': post_redirect}


def main_checker():
    text = input("You need a new [post], a new [photo] or a new [quiet]\n")  # Python 3
    # text = "post"
    ANSWER.get(text, main_checker)()


if __name__ == "__main__":
    main_checker()
