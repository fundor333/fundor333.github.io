from typing import Annotated

import typer
from micro import micro_fc
from notebook import notebook_fc
from now import now_fc
from photo import post_photo
from post import post_fc
from redirect import post_redirect
from weekly import weeklycover

ANSWER = {
    "post": post_fc,
    "micro": micro_fc,
    "photo": post_photo,
    "redirect": post_redirect,
    "weekly_cover": weeklycover,
    "now": now_fc,
    "notebook": notebook_fc,
}


def main(text: Annotated[str, typer.Argument()] = None):
    if text is None:
        text = input("You need a new [post], a new [photo], a new [micro], a [weekly_cover] or [now]\n")
    ANSWER.get(text, main)()


if __name__ == "__main__":
    typer.run(main)
