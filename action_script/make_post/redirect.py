import os
from pathlib import Path

from naming import name_cleaning


def post_redirect() -> None:
    name = input("Give me the title\n")
    title = name_cleaning(name)
    index_path = Path(f"content/redirect/{title}/index.md")

    if index_path.exists():
        print(f"Already exists, skipping: {index_path}")
        return

    os.system(f"hugo new redirect/{title}/index.md")
