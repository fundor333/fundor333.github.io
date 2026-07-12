import datetime
import subprocess

import typer

from generate_cover import generate_img


def week_to_date(year: int, week: int) -> datetime.date:
    """Find the Sunday whose weeknotebot week number (%W + 1) matches `week`."""
    d = datetime.date(year, 1, 1)
    while d.year == year:
        if d.weekday() == 6 and int(d.strftime("%W")) + 1 == week:
            return d
        d += datetime.timedelta(days=1)
    raise ValueError(f"Week {week} not found in year {year}")


def main():
    year = typer.prompt("Year", type=int)
    week = typer.prompt("Week number", type=int)

    today = week_to_date(year, week)
    subprocess.run(
        [
            "weeknote",
            "-config",
            "weeknote-config.json",
            "-t",
            today.strftime("%Y/%m/%d"),
        ],
        check=True,
    )
    generate_img(f"Week Note Nº {week}/{year}", f"weeknotes/{year}/{week}")
    print(f"Generated content/weeknotes/{year}/{week}/index.md and cover.png")


if __name__ == "__main__":
    typer.run(main)
