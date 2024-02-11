---
title: "Following the Elephant's Toots With the Python"
date: 2023-05-26T16:48:25+02:00
feature_link: "https://www.midjourney.com/home/"
feature_text: "by IA Midjourney"
tags:
- pyhton
- mastodon
- pyconit
slug: "following-the-elephant-toots-with-the-python"
categories:
- develop
description: "How I follow all who Toots about PyconIt2023"
type: "post"
mp-syndicate-to:
- https://brid.gy/publish/twitter
- https://brid.gy/publish/mastodon
images:
keywords:
- pyconit2023
- pyconit
---

At the time of the writing I am at the PyconIt 2023[^1], in Florence, and I have a problem.
[^1]: [Link at the event](https://pycon.it/)

All the other Pycon I went, I saved all the user how tweet the official hashtag for the event. This year I won't do it because of the pricing of the Twitter Api, so I was unhappy about of it.

So I decide to implement something similar for Mastodon.

## The theory of the toot

I need to break the task in little steeps for easyer development:

1. I need to get all the Toots with the hashtag: _pycoit2023_
2. I need to collet the users of the toots
3. Follow all the users (you need to follow someone to add to a list)
4. Add all the users in the list _PyconIt2023_

So I wrote this code for a commandline 

~~~ python
from typing import Annotated
import typer
import requests
from rich.console import Console
from rich.table import Table
import logging

logger = logging.getLogger(__name__)
app = typer.Typer()


class MastodonSocial:
    def __init__(self, token: str, domain: str) -> None:
        self.token = token
        self.domain = domain

    def follow(self, account_id: str) -> None:
        url = f"https://{self.domain}/api/v1/accounts/{account_id}/follow"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            logger.info("Success")

    def get_users_from_hashtags(self, hashtag: str) -> None:
        url = f"https://{self.domain}/api/v1/timelines/tag/{hashtag}"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return list({user["account"]["id"] for user in response.json()})
        else:
            raise Exception("Error")

    def get_list(self) -> list[dict]:
        url = f"https://{self.domain}/api/v1/lists"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Error")

    def run_hashtag_follow(self, hashtag: str) -> None:
        users = self.get_users_from_hashtags(hashtag)
        for user in users:
            self.follow(user)

    def add_user_to_list(self, list_id: str, list_users_id: list[str]) -> None:
        url = f"https://{self.domain}/api/v1/lists/{list_id}/accounts"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        present = {user["id"] for user in response.json()}
        list_users_id = list(set(list_users_id) - present)
        url = f"https://{self.domain}/api/v1/lists/{list_id}/accounts"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(
            url, headers=headers, json={"account_ids": list_users_id}
        )
        if response.status_code == 200:
            logger.info("Success")
        else:
            logger.error(response.json())
            raise Exception("Error")

    def run_hashtag_follow_list(self, hashtag: str, list_id: str) -> None:
        users = self.get_users_from_hashtags(hashtag)
        self.add_user_to_list(list_id, users)


@app.command()
def get_lists(
    token: Annotated[str, typer.Argument(help="Token for Mastodon")],
    domain: Annotated[
        str, typer.Argument(help="Mastodon Server")
    ] = "mastodon.social",
):
    ms = MastodonSocial(token=token, domain=domain)
    console = Console()
    table = Table()
    table.add_column("Id")
    table.add_column("Title")
    for e in ms.get_list():
        table.add_row(e["id"], e["title"])
    console.print(table)


@app.command()
def add_list_from_hashtag(
    token: Annotated[str, typer.Argument(help="Token for Mastodon")],
    hashtag: Annotated[
        str, typer.Argument(help="The hash tag to find the followers")
    ],
    list_id: Annotated[
        str, typer.Argument(help="The id of the list to add the followers")
    ],
    domain: Annotated[
        str, typer.Argument(help="Mastodon Server")
    ] = "mastodon.social",
):
    ms = MastodonSocial(token=token, domain=domain)
    users = ms.get_users_from_hashtags(hashtag)
    ms.add_user_to_list(list_id, users)


@app.command()
def follow_from_hashtag(
    token: Annotated[str, typer.Argument(help="Token for Mastodon")],
    hashtag: Annotated[
        str, typer.Argument(help="The hash tag to find the followers")
    ],
    domain: Annotated[
        str, typer.Argument(help="Mastodon Server")
    ] = "mastodon.social",
):
    ms = MastodonSocial(token=token, domain=domain)
    ms.run_hashtag_follow(hashtag=hashtag)


if __name__ == "__main__":
    app()
~~~

With this simple script[^2] now I can populate my Mastodon's List with all the user Tooting about pyconit

[^2]: [Repo Github](https://github.com/fundor333/mastodon_hashtag_and_follow)
