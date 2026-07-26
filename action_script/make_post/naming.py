import re


def name_cleaning(name: str) -> str:
    title = re.sub("[^A-Za-z0-9 ]+", " ", name)
    title = title.replace("  ", " ")
    title = title.replace(" ", "-")
    return title.lower()
