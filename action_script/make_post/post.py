import datetime
import os
from pathlib import Path

from cover import generate_img
from naming import name_cleaning


def post_fc() -> None:
    year = str(datetime.datetime.now().year)
    name = input("Give me the title\n")
    title = name_cleaning(name)
    index_path = Path(f"content/post/{year}/{title}/index.md")

    if index_path.exists():
        print(f"Already exists, skipping: {index_path}")
        return

    os.system(f"hugo new post/{year}/{title}/index.md")
    generate_img(name, f"post/{year}/{title}")
