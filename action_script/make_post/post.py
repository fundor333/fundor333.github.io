import datetime
import os
from pathlib import Path

from categories import known_categories, set_post_categories, update_archetype_categories
from cover import generate_img
from naming import name_cleaning
from series import known_series, set_post_series, update_archetype_series
from tags import known_tags, set_post_tags, update_archetype_tags
from taxonomy import resolve_against_known


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


def _prompt_multi_value(label: str, choices: list[str]) -> list[str]:
    """Ask for one or more values, either picked by number from what's known
    already or typed fresh. A typed value that matches an existing one
    case-insensitively is resolved to the existing spelling, so it never
    creates a near-duplicate (e.g. typing "Django" reuses "django")."""
    if choices:
        print(f"Existing {label} (pick by number, or type new ones):")
        for i, choice in enumerate(choices, start=1):
            print(f"{i}. {choice}")

    raw = input(f"{label.capitalize()} (comma-separated numbers and/or names)\n> ").strip()
    if not raw:
        return []

    selected: list[str] = []
    seen = set()
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if part.isdigit():
            idx = int(part)
            if not (1 <= idx <= len(choices)):
                continue
            value = choices[idx - 1]
        else:
            value = resolve_against_known(part, choices)

        if value.casefold() not in seen:
            seen.add(value.casefold())
            selected.append(value)
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
    selected_tags = _prompt_multi_value("tags", known_tags())
    selected_categories = _prompt_multi_value("categories", known_categories())

    os.system(f"hugo new post/{year}/{title}/index.md")
    generate_img(name, f"post/{year}/{title}")
    set_post_series(str(index_path), selected_series)
    set_post_tags(str(index_path), selected_tags)
    set_post_categories(str(index_path), selected_categories)
    update_archetype_series()
    update_archetype_tags()
    update_archetype_categories()
