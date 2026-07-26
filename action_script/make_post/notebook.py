import datetime
import os
from pathlib import Path

from cover import generate_img
from naming import name_cleaning


def notebook_fc() -> None:
    year = str(datetime.datetime.now().year)
    name = input("Give me the title\n")
    title = name_cleaning(name)
    notebook_path = Path(f"content/post/{year}/{title}/index.ipynb")

    if notebook_path.exists():
        print(f"Already exists, skipping: {notebook_path}")
        return

    os.system(f"hugo_nbnew ./content/post/{year}/{title}")
    generate_img(name, f"post/{year}/{title}", "alternative_cover.jpg")

    Path("notescript").mkdir(parents=True, exist_ok=True)
    script_path = Path(f"notescript/{title}.sh")
    script_path.write_text(f"#! /bin/bash\nuv run hugo_nbconvert content/post/{year}/{title}/index.ipynb\n")
    script_path.chmod(0o755)
