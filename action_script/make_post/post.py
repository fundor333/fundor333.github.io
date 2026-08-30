import datetime
import os
from pathlib import Path

from cover import generate_img
from naming import name_cleaning
from series import known_series, set_post_series, update_archetype_series


def _prompt_series(choices: list[str]) -> list[str]:
    """Ask whether the post belongs to any series and, if so, let the user pick
    one or more from every series known so far (default: no series)."""
    if not choices:
        return []

    answer = input("Add this post to any series? [y/N]\n").strip().lower()
    if answer not in ("y", "yes"):
        return []

    print("Pick one or more series (comma-separated numbers):")
    for i, series in enumerate(choices, start=1):
        print(f"{i}. {series}")

    raw = input("> ").strip()
    if not raw:
        return []

    selected = []
    for part in raw.split(","):
        part = part.strip()
        if not part.isdigit():
            continue
        idx = int(part)
        if 1 <= idx <= len(choices) and choices[idx - 1] not in selected:
            selected.append(choices[idx - 1])
    return selected


def post_fc() -> None:
    year = str(datetime.datetime.now().year)
    name = input("Give me the title\n")
    title = name_cleaning(name)
    index_path = Path(f"content/post/{year}/{title}/index.md")

    if index_path.exists():
        print(f"Already exists, skipping: {index_path}")
        return

    selected_series = _prompt_series(known_series())

    os.system(f"hugo new post/{year}/{title}/index.md")
    generate_img(name, f"post/{year}/{title}")
    set_post_series(str(index_path), selected_series)
    update_archetype_series()
