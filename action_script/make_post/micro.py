import datetime
import os
from pathlib import Path

from naming import name_cleaning


def micro_fc() -> None:
    print("Make a micro")
    name = input("Give me the title\n")
    year = str(datetime.datetime.now().year).rjust(4, "0")
    month = str(datetime.datetime.now().month).rjust(2, "0")
    title = name_cleaning(name)

    generated = f"{year}/{month}/{title}"
    index_path = Path(f"content/micro/{generated}/index.md")

    if index_path.exists():
        print(f"Already exists, skipping: {index_path}")
        return

    os.system(f"hugo new micro/{generated}/index.md")
    print(f"Generated {generated}/index.md")
