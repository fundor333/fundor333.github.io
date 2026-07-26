import datetime
from pathlib import Path

from cover import generate_img


def weeklycover() -> None:
    print("Make a weekly cover")
    today = datetime.datetime.now()
    year = today.strftime("%Y")
    week = str(int(today.strftime("%W")) + 1)
    target_dir = Path(f"content/weeknotes/{year}/{week}")

    if not target_dir.is_dir():
        print(f"Weeknote not found yet, skipping cover: {target_dir}")
        return

    file_string = f"Week Note Nº {week}/{year}"
    generate_img(file_string, f"weeknotes/{year}/{week}")
